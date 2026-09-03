#!/usr/bin/env python3
"""EV-132 evidence gate for VDV301-2 General Conventions V2.2 findings.

Revalidates DR3012GC22-001..002 against the exact byte-pinned 08/2019 PDF,
visible German/English page evidence, the exact VDV-301-2.2 Common/Enumeration
release context, and active disproof checks. Both findings are documentation-only.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/VDV301-2_GC_V2.2.pdf")
SOURCE_REGISTRY = Path("audit_registry/pdf_source_registry_v0.1.json")
PIN_REGISTRY = Path("audit_registry/pdf_source_pins_v0.1.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
COMMON_XSD = Path("IBIS-IP_common_V2.2.xsd")
ENUM_XSD = Path("IBIS-IP_Enumerations_V2.2.xsd")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/VDV301-2_GC_V2.2.md")
OUT_DIR = Path(os.environ.get("EV132_OUTPUT_DIR", "artifacts/ev132"))

EXPECTED_PDF_SHA256 = "96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051"
EXPECTED_PDF_SIZE = 1562305
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_COMMON_BLOB = "468fee6d177e7185dbcd5d3f90cfb114e29e01ae"
EXPECTED_ENUM_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"
FINDINGS = ["DR3012GC22-001", "DR3012GC22-002"]
TERMINAL_RECOMMENDATIONS = {finding: "context_verified" for finding in FINDINGS}
PLACEHOLDER = "Fehler! Verweisquelle konnte nicht gefunden werden"


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def normalize(text: str) -> str:
    return " ".join(text.replace("\u00ad", "").split())


def page_text(page: int) -> str:
    out = subprocess.check_output(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(PDF), "-"],
        text=True,
        errors="replace",
    )
    return normalize(out)


def full_text() -> str:
    out = subprocess.check_output(["pdftotext", "-layout", str(PDF), "-"], text=True, errors="replace")
    return normalize(out)


def find_source(registry: dict, source_id: str) -> dict:
    for item in registry.get("sources", []):
        if item.get("source_id") == source_id:
            return item
    fail(f"source not found: {source_id}")


def main() -> int:
    require(PDF.exists(), f"missing fetched PDF: {PDF}")
    require(git_blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory changed")
    require(git_blob(COMMON_XSD) == EXPECTED_COMMON_BLOB, "Common V2.2 XSD changed")
    require(git_blob(ENUM_XSD) == EXPECTED_ENUM_BLOB, "Enumerations V2.2 XSD changed")

    pdf_hash, pdf_size = sha256_file(PDF)
    require(pdf_hash == EXPECTED_PDF_SHA256, f"GC V2.2 PDF hash mismatch: {pdf_hash}")
    require(pdf_size == EXPECTED_PDF_SIZE, f"GC V2.2 PDF size mismatch: {pdf_size}")

    frozen = load(FROZEN)
    require(frozen.get("entry_count") == 192 and frozen.get("state") == "frozen", "frozen inventory invariant failed")
    for finding_id in FINDINGS:
        require(finding_id in frozen.get("finding_ids", []), f"missing frozen finding {finding_id}")

    sources = load(SOURCE_REGISTRY)
    pins = load(PIN_REGISTRY)
    src = find_source(sources, "VDV301-2_GC_V2.2")
    pin = find_source(pins, "VDV301-2_GC_V2.2")
    require(src.get("vdv_part") == "301-2" and src.get("version") == "2.2", "GC V2.2 source identity changed")
    require(pin.get("expected_sha256") == EXPECTED_PDF_SHA256, "GC V2.2 pin hash changed")
    require(int(pin.get("expected_size_bytes")) == EXPECTED_PDF_SIZE, "GC V2.2 pin size changed")

    # Exact release context must still compile, but the findings themselves are not XSD-validity defects.
    etree.XMLSchema(etree.parse(str(COMMON_XSD)))
    etree.XMLSchema(etree.parse(str(ENUM_XSD)))

    all_text = full_text()

    # DR3012GC22-001: repeated literal unresolved Word cross-reference placeholders.
    p13 = page_text(13)
    p52 = page_text(52)
    p62 = page_text(62)
    p64 = page_text(64)
    p66 = page_text(66)
    p70 = page_text(70)
    require(PLACEHOLDER in p13, "page 13 unresolved cross-reference anchor missing")
    require(PLACEHOLDER in p52, "page 52 unresolved cross-reference anchor missing")
    require(PLACEHOLDER in p62, "page 62 unresolved cross-reference anchor missing")
    require(PLACEHOLDER in p64, "page 64 unresolved cross-reference anchor missing")
    require(PLACEHOLDER in p66, "page 66 unresolved cross-reference anchor missing")
    require(all_text.count(PLACEHOLDER) >= 5, "expected repeated independent Word placeholders")
    require("Technische Ergänzungen/Korrekturen Keine" in p70, "German no-technical-corrections history anchor missing")
    require("Technical Upgrade/Corrections none" in p70, "English no-technical-corrections history anchor missing")
    print("OK DR3012GC22-001 repeated unresolved Word cross references confirmed")

    # DR3012GC22-002: German SRV/TXT numbering duplicates 3.3.1; English distinguishes 3.3.1/3.3.2.
    p5 = page_text(5)
    p6 = page_text(6)
    p25 = page_text(25)
    p27 = page_text(27)
    p31 = page_text(31)
    p33 = page_text(33)
    require("3.3.1 Nutzung des SRV-Records" in p5 and "3.3.1 Nutzung des TXT-Records" in p5, "German TOC duplicate 3.3.1 anchors missing")
    require("3.3.1 Use of SRV Records" in p6 and "3.3.2 Use of TXT Records" in p6, "English TOC disproof anchors missing")
    require("SRV-Records (vgl. Kapitel 3.3.1)" in p25 and "TXT-Records (vgl. Kapitel 3.3.1)" in p25, "German intro duplicate references missing")
    require("3.3.1 Nutzung des SRV-Records" in p25, "German SRV heading missing")
    require("3.3.1 Nutzung des TXT-Records" in p27, "German TXT duplicate heading missing")
    require("SRV records (cf. chapter 3.3.1)" in p31 and "TXT records (cf. chapter 3.3.2)" in p31, "English intro correct references missing")
    require("3.3.1 Use of SRV Records" in p31, "English SRV heading missing")
    require("3.3.2 Use of TXT Records" in p33, "English TXT heading missing")
    print("OK DR3012GC22-002 German duplicate TXT subsection number vs correct English 3.3.2 confirmed")

    deep_read = DEEP_READ.read_text(encoding="utf-8")
    for finding_id in FINDINGS:
        require(finding_id in deep_read, f"historical deep-read record missing {finding_id}")
    require("General-Conventions publication" in deep_read, "V2.2 structural publication context missing")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result = {
        "evidence_id": "EV-132",
        "finding_block": FINDINGS,
        "pdf_source_id": "VDV301-2_GC_V2.2",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "release_context": "official VDV-301-2.2 General Conventions; Common/Enumerations V2.2 byte-identical to upstream tag",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "visual_pages": [5, 6, 13, 25, 27, 31, 33, 52, 62, 64, 66, 70],
        "active_disproof": {
            "DR3012GC22-001": "placeholder occurs independently on at least five pages/contexts; V2.2 history states technical corrections none",
            "DR3012GC22-002": "English track and English TOC consistently use 3.3.1 for SRV and 3.3.2 for TXT, disproving an intentional same-number convention"
        },
        "terminal_revalidation_recommendations": TERMINAL_RECOMMENDATIONS,
        "executable_evidence_reason_not_applicable": "Both findings concern printed cross references/section numbering and do not define XML instance validity. Common/Enumerations V2.2 are compiled only to preserve exact release context.",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS"
    }
    (OUT_DIR / "ev132_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED: EV-132 VDV301-2 General Conventions V2.2 DR3012GC22-001..002")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
