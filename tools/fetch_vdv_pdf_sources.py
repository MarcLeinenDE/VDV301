#!/usr/bin/env python3
"""Fetch and verify local VDV 301 PDF source bytes for the PDF/XSD audit.

The public repository stores only source metadata and checksums. PDF bytes are
kept below local_sources/ and are intentionally ignored by Git.

Default behaviour is strict:
- pinned sources are accepted only when SHA-256 and size match the registry;
- unpinned sources are refused unless --bootstrap-pins is given;
- an already pinned source is never silently re-pinned when its bytes change.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Iterable
import urllib.error
import urllib.request

STATUS_CHANGED = "SOURCE_CHANGED_SINCE_AUDIT"
USER_AGENT = "VDV301-Audit-SourceFetcher/0.1 (+https://github.com/MarcLeinenDE/VDV301)"


class SourceError(RuntimeError):
    pass


def sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as fh:
        while True:
            chunk = fh.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def load_registry(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        data = json.load(fh)
    if data.get("registry_version") != "0.1":
        raise SourceError(f"Unsupported registry_version: {data.get('registry_version')!r}")
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        raise SourceError("Registry contains no sources")
    ids = [s.get("source_id") for s in sources]
    if any(not x for x in ids) or len(ids) != len(set(ids)):
        raise SourceError("source_id values must be present and unique")
    return data


def atomic_write_json(path: Path, data: dict) -> None:
    text = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def select_sources(registry: dict, source_ids: set[str], document_ids: set[str], all_sources: bool) -> list[dict]:
    sources = registry["sources"]
    if all_sources:
        return sources
    selected = [
        s for s in sources
        if s["source_id"] in source_ids or s["document_id"] in document_ids
    ]
    if not selected:
        raise SourceError("No sources selected. Use --all, --source-id or --document-id.")
    known_source_ids = {s["source_id"] for s in sources}
    known_document_ids = {s["document_id"] for s in sources}
    missing_sources = source_ids - known_source_ids
    missing_documents = document_ids - known_document_ids
    if missing_sources:
        raise SourceError(f"Unknown source_id(s): {', '.join(sorted(missing_sources))}")
    if missing_documents:
        raise SourceError(f"Unknown document_id(s): {', '.join(sorted(missing_documents))}")
    return selected


def verify_pdf_signature(path: Path) -> None:
    with path.open("rb") as fh:
        sig = fh.read(5)
    if sig != b"%PDF-":
        raise SourceError(f"{path}: downloaded content is not a PDF (%PDF- signature missing)")


def download_to_temp(url: str, cache_dir: Path, source_id: str) -> Path:
    cache_dir.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{source_id}.", suffix=".part", dir=cache_dir)
    os.close(fd)
    tmp = Path(name)
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response, tmp.open("wb") as out:
            while True:
                chunk = response.read(1024 * 1024)
                if not chunk:
                    break
                out.write(chunk)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        tmp.unlink(missing_ok=True)
        raise SourceError(f"{source_id}: download failed: {exc}") from exc
    return tmp


def verify_against_pin(source: dict, path: Path) -> tuple[str, int]:
    verify_pdf_signature(path)
    actual_hash, actual_size = sha256_file(path)
    expected_hash = source.get("expected_sha256")
    expected_size = source.get("expected_size_bytes")
    if expected_hash and actual_hash.lower() != str(expected_hash).lower():
        raise SourceError(
            f"{STATUS_CHANGED}: {source['source_id']} expected sha256={expected_hash}, actual={actual_hash}"
        )
    if expected_size is not None and actual_size != int(expected_size):
        raise SourceError(
            f"{STATUS_CHANGED}: {source['source_id']} expected size={expected_size}, actual={actual_size}"
        )
    return actual_hash, actual_size


def process_source(
    source: dict,
    cache_dir: Path,
    bootstrap_pins: bool,
    check_only: bool,
) -> tuple[bool, bool]:
    """Return (ok, registry_changed)."""
    target = cache_dir / source["local_filename"]
    pinned = bool(source.get("expected_sha256")) and source.get("expected_size_bytes") is not None

    if target.exists():
        actual_hash, actual_size = verify_against_pin(source, target)
        if pinned:
            print(f"OK {source['source_id']} cached sha256={actual_hash}")
            return True, False
        if not bootstrap_pins:
            raise SourceError(
                f"{source['source_id']}: cached PDF exists but registry is unpinned; "
                "run with --bootstrap-pins to establish the first explicit pin"
            )
        source["expected_sha256"] = actual_hash
        source["expected_size_bytes"] = actual_size
        source["pin_state"] = "pinned"
        source["pinned_at_utc"] = utc_now()
        source["deep_read_source_ready"] = True
        print(f"PIN {source['source_id']} from existing cache sha256={actual_hash}")
        return True, True

    if check_only:
        raise SourceError(f"{source['source_id']}: local cache file missing: {target}")

    if not pinned and not bootstrap_pins:
        raise SourceError(
            f"{source['source_id']}: source is unpinned. "
            "Use --bootstrap-pins only for an intentional first-byte pin."
        )

    tmp = download_to_temp(source["official_url"], cache_dir, source["source_id"])
    try:
        actual_hash, actual_size = verify_against_pin(source, tmp)
        if not pinned:
            source["expected_sha256"] = actual_hash
            source["expected_size_bytes"] = actual_size
            source["pin_state"] = "pinned"
            source["pinned_at_utc"] = utc_now()
            source["deep_read_source_ready"] = True
            changed = True
            print(f"PIN {source['source_id']} sha256={actual_hash}")
        else:
            changed = False
            print(f"OK {source['source_id']} downloaded sha256={actual_hash}")
        os.replace(tmp, target)
        return True, changed
    finally:
        tmp.unlink(missing_ok=True)


def utc_now() -> str:
    from datetime import datetime, timezone
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser()
    p.add_argument(
        "--registry",
        default="audit_registry/pdf_source_registry_v0.1.json",
        help="Path to the public PDF source registry.",
    )
    p.add_argument(
        "--cache-dir",
        default="local_sources/vdv_pdfs",
        help="Local cache directory. This path is gitignored by project policy.",
    )
    p.add_argument("--source-id", action="append", default=[], help="Fetch/check one physical source_id; repeatable.")
    p.add_argument("--document-id", action="append", default=[], help="Fetch/check all physical sources for one semantic document_id; repeatable.")
    p.add_argument("--all", action="store_true", help="Process all registered physical sources.")
    p.add_argument(
        "--bootstrap-pins",
        action="store_true",
        help="Explicitly establish SHA-256/size pins for currently unpinned sources. Existing pins are never overwritten.",
    )
    p.add_argument(
        "--check-only",
        action="store_true",
        help="Do not download. Verify selected local cache files against the registry.",
    )
    return p


def main(argv: Iterable[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    registry_path = Path(args.registry)
    cache_dir = Path(args.cache_dir)
    try:
        registry = load_registry(registry_path)
        selected = select_sources(
            registry,
            set(args.source_id),
            set(args.document_id),
            args.all,
        )
        registry_changed = False
        for source in selected:
            _, changed = process_source(
                source,
                cache_dir=cache_dir,
                bootstrap_pins=args.bootstrap_pins,
                check_only=args.check_only,
            )
            registry_changed = registry_changed or changed
        if registry_changed:
            atomic_write_json(registry_path, registry)
            print(f"UPDATED {registry_path}")
        return 0
    except SourceError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
