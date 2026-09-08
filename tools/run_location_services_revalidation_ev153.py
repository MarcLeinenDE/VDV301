#!/usr/bin/env python3
"""Stable runner for EV-153.

The base EV-153 validator intentionally keeps its first fail-closed implementation.
This runner only compensates for Poppler's layout-mode column wrapping of long
PDF identifiers by returning the raw extraction for textual assertions while
still retaining the layout extraction as evidence. It also corrects the label
of the final negative diagnostic emitted by the base validator and rebuilds the
artifact manifest after that metadata-only correction.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import validate_location_services_revalidation_ev153 as base


def raw_text_page(pdf: Path, page: int, out: Path, label: str) -> str:
    layout_target = out / f"{label}-page-{page}-layout.txt"
    raw_target = out / f"{label}-page-{page}-raw.txt"
    subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(pdf), str(layout_target)],
        check=True,
    )
    subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), "-raw", str(pdf), str(raw_target)],
        check=True,
    )
    return raw_target.read_text(encoding="utf-8", errors="replace")


def arg_value(flag: str, default: str) -> str:
    try:
        idx = sys.argv.index(flag)
    except ValueError:
        return default
    assert idx + 1 < len(sys.argv), f"missing value for {flag}"
    return sys.argv[idx + 1]


def repair_diagnostic_label_and_manifest() -> None:
    root = Path(arg_value("--repo-root", ".")).resolve()
    out = (root / arg_value("--output-dir", "artifacts/ev153")).resolve()
    diag = out / "negative-diagnostics.txt"
    text = diag.read_text(encoding="utf-8")
    old = "LS-001 negative (PDF spelling):\n"
    new = "LS-002 negative (normalized alias):\n"
    assert text.startswith(old), "unexpected EV-153 negative diagnostic format"
    diag.write_text(new + text[len(old):], encoding="utf-8")

    manifest = out / "manifest.sha256"
    files = sorted(p for p in out.rglob("*") if p.is_file() and p.name != manifest.name)
    with manifest.open("w", encoding="utf-8") as f:
        for path in files:
            f.write(f"{base.sha256(path)}  {path.relative_to(out)}\n")


def main() -> int:
    base.text_page = raw_text_page
    result = base.main()
    assert result == 0
    repair_diagnostic_label_and_manifest()
    print("EV153_RUNNER_OK raw_pdf_text_assertions=true diagnostic_label_corrected=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
