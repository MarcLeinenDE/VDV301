#!/usr/bin/env python3
"""EV-133 evidence gate for VDV301-2 General Conventions V2.3 DR3012GC23-001."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/VDV301-2_GC_V2.3.pdf")
SOURCE_REGISTRY = Path("audit_registry/pdf_source_registry_v0.1.json")
PIN_REGISTRY = Path("audit_registry/pdf_source_pins_v0.1.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
COMMON_XSD = Path("IBIS-IP_common_V2.3.xsd")
ENUM_XSD = Path("IBIS-IP_Enumerations_V2.2.xsd")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/VDV301-2_GC_V2.3.md")
OUT_DIR = Path(os.environ.get("EV133_OUTPUT_DIR", "artifacts/ev133"))

EXPECTED_PDF_SHA256 = "4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603"
EXPECTED_PDF_SIZE = 1057483
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_COMMON_BLOB = "0d8926c4063c12de9a5e68b6f0addaab35a55dc1"
EXPECTED_ENUM_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"
FINDING_ID = "DR3012GC23-001"


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256(); size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk); size += len(chunk)
    return h.hexdigest(), size


def normalize(text: str) -> str:
    return " ".join(text.replace("\u00ad", "").split())


def page_text(page: int) -> str:
    return normalize(subprocess.check_output(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(PDF), "-"],
        text=True, errors="replace"
    ))


def full_text() -> str:
    return normalize(subprocess.check_output(["pdftotext", "-layout", str(PDF), "-"], text=True, errors="replace"))


def find_source(registry: dict, source_id: str) -> dict:
    for item in registry.get("sources", []):
        if item.get("source_id") == source_id:
            return item
    fail(f"source not found: {source_id}")


def main() -> int:
    require(PDF.exists(), f"missing fetched PDF: {PDF}")
    require(blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory changed")
    require(blob(COMMON_XSD) == EXPECTED_COMMON_BLOB, "official Common V2.3 root changed")
    require(blob(ENUM_XSD) == EXPECTED_ENUM_BLOB, "Enumerations V2.2 dependency changed")

    pdf_hash, pdf_size = sha256_file(PDF)
    require((pdf_hash, pdf_size) == (EXPECTED_PDF_SHA256, EXPECTED_PDF_SIZE), "GC V2.3 PDF pin mismatch")

    frozen = load(FROZEN)
    require(frozen.get("entry_count") == 192 and frozen.get("state") == "frozen", "frozen inventory invariant failed")
    require(FINDING_ID in frozen.get("finding_ids", []), f"missing frozen finding {FINDING_ID}")

    sources = load(SOURCE_REGISTRY); pins = load(PIN_REGISTRY)
    src = find_source(sources, "VDV301-2_GC_V2.3")
    pin = find_source(pins, "VDV301-2_GC_V2.3")
    require(src.get("vdv_part") == "301-2" and src.get("version") == "2.3", "GC V2.3 source identity changed")
    require(pin.get("expected_sha256") == EXPECTED_PDF_SHA256 and int(pin.get("expected_size_bytes")) == EXPECTED_PDF_SIZE, "GC V2.3 pin registry changed")

    common_text = COMMON_XSD.read_text(encoding="utf-8")
    require('schemaLocation="IBIS-IP_Enumerations_V2.2.xsd"' in common_text, "official Common V2.3 dependency route changed")
    etree.XMLSchema(etree.parse(str(COMMON_XSD)))

    # Active predecessor/successor context and visible V2.3 defect.
    p70 = page_text(70)
    p71 = page_text(71)
    require("7.1 Version 2.2" in p70, "V2.2 history heading missing")
    require("7.1.1 Funktionale Erweiterungen" in p70 and "7.1.2 Technische Ergänzungen/Korrekturen" in p70, "V2.2 German numbering baseline missing")
    require("7.2 Version 2.3" in p71, "V2.3 history heading missing")
    require("7.1.3 Funktionale Erweiterungen" in p71, "V2.3 German 7.1.3 defect missing")
    require("7.1.4 Technische Ergänzungen/Korrekturen" in p71, "V2.3 German 7.1.4 defect missing")
    require("7.2.1 Functional Upgrade" in p71 and "7.2.2 Technical Upgrade/Corrections" in p71, "V2.3 English corrective numbering disproof missing")
    print("OK DR3012GC23-001 German V2.3 version-history numbering remains in 7.1 namespace while English uses 7.2.x")

    all_text = full_text()
    require("Fehler! Verweisquelle konnte nicht gefunden werden" not in all_text, "V2.2 unresolved Word placeholder unexpectedly persists in V2.3")

    deep_read = DEEP_READ.read_text(encoding="utf-8")
    require(FINDING_ID in deep_read, "historical Deep Read finding missing")
    require("resolved_in_successor_version" in deep_read, "V2.2 Word-reference repair context missing")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result = {
        "evidence_id": "EV-133",
        "finding_block": [FINDING_ID],
        "pdf_source_id": "VDV301-2_GC_V2.3",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "release_context": "official VDV-301-2.3 General Conventions; official Common V2.3 root with Enumerations V2.2 dependency",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "visual_pages": [70, 71],
        "active_disproof": {
            "previous_section_baseline": "V2.2 correctly uses German 7.1.1/7.1.2 under 7.1",
            "same_page_language_disproof": "English V2.3 correctly uses 7.2.1/7.2.2 under 7.2",
            "predecessor_word_placeholder": "DR3012GC22-001 literal unresolved Word placeholders are absent in V2.3"
        },
        "terminal_revalidation_recommendations": {FINDING_ID: "context_verified"},
        "executable_evidence_reason_not_applicable": "The finding concerns printed version-history subsection numbering and does not define XML instance validity. The exact Common V2.3 root is compiled only to preserve release authority context.",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS"
    }
    (OUT_DIR / "ev133_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED: EV-133 VDV301-2 General Conventions V2.3 DR3012GC23-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
