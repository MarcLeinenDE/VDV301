#!/usr/bin/env python3
"""Render selected pages from a byte-pinned VDV PDF source.

The source PDF is never written into the repository tree. The script resolves the
official URL from the source registry, verifies the downloaded/local bytes
against the SHA-256 + byte-size pin registry, renders requested 1-based pages to
PNG using PyMuPDF, and writes a JSON manifest with per-render hashes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import urllib.request


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def find_by_source_id(items: list[dict], source_id: str) -> dict:
    matches = [item for item in items if item.get("source_id") == source_id]
    if len(matches) != 1:
        raise SystemExit(f"expected exactly one source_id={source_id!r}, found {len(matches)}")
    return matches[0]


def parse_pages(spec: str) -> list[int]:
    pages: set[int] = set()
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            start_s, end_s = chunk.split("-", 1)
            start, end = int(start_s), int(end_s)
            if start < 1 or end < start:
                raise argparse.ArgumentTypeError(f"invalid page range: {chunk}")
            pages.update(range(start, end + 1))
        else:
            page = int(chunk)
            if page < 1:
                raise argparse.ArgumentTypeError(f"invalid page: {chunk}")
            pages.add(page)
    if not pages:
        raise argparse.ArgumentTypeError("no pages selected")
    return sorted(pages)


def fetch(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "VDV301-Audit-PDFRenderer/0.1 (+https://github.com/MarcLeinenDE/VDV301)",
            "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.1",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as response:
        return response.read()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--pages", required=True, type=parse_pages, help="1-based list/ranges, e.g. 1,4,39-40")
    parser.add_argument("--out-dir", required=True, type=Path)
    parser.add_argument("--dpi", type=int, default=180)
    parser.add_argument("--source-registry", type=Path, default=Path("audit_registry/pdf_source_registry_v0.1.json"))
    parser.add_argument("--pin-registry", type=Path, default=Path("audit_registry/pdf_source_pins_v0.1.json"))
    parser.add_argument("--local-pdf", type=Path, default=None, help="optional already-downloaded source PDF")
    args = parser.parse_args()

    if args.dpi < 72 or args.dpi > 600:
        raise SystemExit("dpi must be between 72 and 600")

    try:
        import fitz  # PyMuPDF
    except Exception as exc:
        raise SystemExit("PyMuPDF is required (pip install pymupdf)") from exc

    source_catalog = load_json(args.source_registry)
    pin_catalog = load_json(args.pin_registry)
    source = find_by_source_id(source_catalog.get("sources", []), args.source_id)
    pin = find_by_source_id(pin_catalog.get("sources", []), args.source_id)

    if not pin.get("deep_read_source_ready"):
        raise SystemExit(f"source {args.source_id} is not marked deep_read_source_ready")

    if args.local_pdf is not None:
        data = args.local_pdf.read_bytes()
        retrieval = "local_pdf"
    else:
        data = fetch(source["official_url"])
        retrieval = "official_url"

    if not data.startswith(b"%PDF-"):
        raise SystemExit("source bytes do not start with %PDF-")

    observed_sha = sha256_bytes(data)
    observed_size = len(data)
    expected_sha = str(pin["expected_sha256"]).lower()
    expected_size = int(pin["expected_size_bytes"])
    if observed_sha.lower() != expected_sha or observed_size != expected_size:
        raise SystemExit(
            "SOURCE_CHANGED_SINCE_AUDIT: "
            f"sha256={observed_sha} size={observed_size}; "
            f"expected sha256={expected_sha} size={expected_size}"
        )

    doc = fitz.open(stream=data, filetype="pdf")
    page_count = doc.page_count
    args.out_dir.mkdir(parents=True, exist_ok=True)

    scale = args.dpi / 72.0
    matrix = fitz.Matrix(scale, scale)
    rendered: list[dict] = []

    for page_no in args.pages:
        if page_no > page_count:
            raise SystemExit(f"requested page {page_no} exceeds PDF page count {page_count}")
        page = doc.load_page(page_no - 1)
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        filename = f"{args.source_id}_page_{page_no:04d}_{args.dpi}dpi.png"
        out_path = args.out_dir / filename
        png = pix.tobytes("png")
        out_path.write_bytes(png)
        rendered.append({
            "page": page_no,
            "filename": filename,
            "width_px": pix.width,
            "height_px": pix.height,
            "png_sha256": sha256_bytes(png),
            "png_size_bytes": len(png),
        })

    manifest = {
        "render_manifest_version": "0.1",
        "source_id": args.source_id,
        "official_url": source["official_url"],
        "retrieval": retrieval,
        "source_sha256": observed_sha,
        "source_size_bytes": observed_size,
        "source_pin_evidence_run_id": pin.get("evidence_run_id"),
        "pdf_page_count": page_count,
        "render_engine": "PyMuPDF",
        "render_engine_version": getattr(fitz, "VersionBind", None),
        "dpi": args.dpi,
        "pages": rendered,
    }
    (args.out_dir / "render_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
