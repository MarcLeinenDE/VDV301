#!/usr/bin/env python3
"""Strictly fetch/verify byte-pinned VDV PDF sources without changing pins."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import os
import sys
import tempfile
import urllib.error
import urllib.request

STATUS_CHANGED = "SOURCE_CHANGED_SINCE_AUDIT"
USER_AGENT = "VDV301-Audit-SourceVerifier/0.1 (+https://github.com/MarcLeinenDE/VDV301)"


def digest(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def verify_pdf(path: Path, pin: dict) -> None:
    with path.open("rb") as fh:
        if fh.read(5) != b"%PDF-":
            raise RuntimeError(f"{path}: missing %PDF- signature")
    actual_hash, actual_size = digest(path)
    if actual_hash.lower() != pin["expected_sha256"].lower() or actual_size != int(pin["expected_size_bytes"]):
        raise RuntimeError(
            f"{STATUS_CHANGED}: {pin['source_id']} expected sha256={pin['expected_sha256']} "
            f"size={pin['expected_size_bytes']}, actual sha256={actual_hash} size={actual_size}"
        )


def download(url: str, target: Path, source_id: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{source_id}.", suffix=".part", dir=target.parent)
    os.close(fd)
    tmp = Path(name)
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/pdf,*/*;q=0.1"})
    try:
        with urllib.request.urlopen(request, timeout=90) as response, tmp.open("wb") as out:
            for chunk in iter(lambda: response.read(1024 * 1024), b""):
                out.write(chunk)
        os.replace(tmp, target)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"{source_id}: download failed: {exc}") from exc
    finally:
        tmp.unlink(missing_ok=True)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--catalog", default="audit_registry/pdf_source_registry_v0.1.json")
    p.add_argument("--pins", default="audit_registry/pdf_source_pins_v0.1.json")
    p.add_argument("--cache-dir", default="local_sources/vdv_pdfs")
    p.add_argument("--source-id", action="append", default=[])
    p.add_argument("--all-pinned", action="store_true")
    p.add_argument("--check-only", action="store_true")
    args = p.parse_args()

    catalog = json.loads(Path(args.catalog).read_text(encoding="utf-8"))
    pins = json.loads(Path(args.pins).read_text(encoding="utf-8"))
    sources = {s["source_id"]: s for s in catalog["sources"]}
    pin_map = {s["source_id"]: s for s in pins["sources"]}

    selected = sorted(pin_map) if args.all_pinned else args.source_id
    if not selected:
        raise RuntimeError("Select --source-id or --all-pinned")

    cache_dir = Path(args.cache_dir)
    for source_id in selected:
        if source_id not in pin_map:
            raise RuntimeError(f"No committed pin for {source_id}")
        if source_id not in sources:
            raise RuntimeError(f"Pinned source missing from catalog: {source_id}")
        source = sources[source_id]
        pin = pin_map[source_id]
        target = cache_dir / source["local_filename"]
        if not target.exists():
            if args.check_only:
                raise RuntimeError(f"{source_id}: local cache missing: {target}")
            download(source["official_url"], target, source_id)
        verify_pdf(target, pin)
        actual_hash, actual_size = digest(target)
        print(f"OK {source_id} sha256={actual_hash} size={actual_size}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        raise SystemExit(3)
