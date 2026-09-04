#!/usr/bin/env python3
"""EV-140 fail-closed revalidation evidence for COMMON V2.4 DRCOM24-001."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/COMMON_V2.4.pdf")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
FRESH = Path("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.4_FRESH_2026-09-03.md")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.4.md")
DELTA = Path("audit_registry/deep_read_findings_delta_common_v24_2026-09-03.json")
COMMON = Path("IBIS-IP_common_V2.4.xsd")
ENUMS = Path("IBIS-IP_Enumerations_V2.4.xsd")
EV122 = Path("tools/validate_common_v24_ev122.py")
OUT_DIR = Path(os.environ.get("EV140_OUTPUT_DIR", "artifacts/ev140"))

EXPECTED_PDF_SHA256 = "01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a"
EXPECTED_PDF_SIZE = 1689647
EXPECTED_PDF_PAGES = 63
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_FRESH_BLOB = "1a2f58c60152e14a61257d21a8c2cd4533f2696e"
EXPECTED_DEEP_READ_BLOB = "5800c06781b17775f6763a918568d3e5712210c5"
EXPECTED_DELTA_BLOB = "9744612c607e63659d574c13500cfc611f239f39"
EXPECTED_COMMON_BLOB = "1946fd37e29ced605654f49ea3d98cd2fbbdc8e4"
EXPECTED_ENUM_BLOB = "2afed8cf23afa91db92b0f043cc5b4ad428b0f25"
EXPECTED_EV122_BLOB = "acbca8a808e623030c2ff48bc2e3f3e336cb5f11"
FINDING = "DRCOM24-001"
NS = {"xs": "http://www.w3.org/2001/XMLSchema"}


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256(); size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk); size += len(chunk)
    return h.hexdigest(), size


def page_text(page: int) -> str:
    return subprocess.check_output(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(PDF), "-"],
        text=True, errors="replace"
    )


def occurs(node: etree._Element, attr: str) -> str:
    return node.get(attr, "1")


def main() -> int:
    require(PDF.exists(), f"missing PDF {PDF}")
    for path, expected in {
        FROZEN: EXPECTED_FROZEN_BLOB,
        FRESH: EXPECTED_FRESH_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        DELTA: EXPECTED_DELTA_BLOB,
        COMMON: EXPECTED_COMMON_BLOB,
        ENUMS: EXPECTED_ENUM_BLOB,
        EV122: EXPECTED_EV122_BLOB,
    }.items():
        require(path.is_file(), f"missing immutable source {path}")
        observed = blob(path)
        require(observed == expected, f"immutable blob changed for {path}: {observed}")

    pdf_hash, pdf_size = sha256_file(PDF)
    require(pdf_hash == EXPECTED_PDF_SHA256, f"PDF hash mismatch {pdf_hash}")
    require(pdf_size == EXPECTED_PDF_SIZE, f"PDF size mismatch {pdf_size}")

    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory invariant failed")
    require(FINDING in frozen.get("finding_ids", []), f"{FINDING} missing from frozen inventory")

    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entries = reg.get("inventory", {}).get("entries", [])
    by_id = {x.get("finding_id"): x for x in entries}
    terminal = sum(x.get("revalidation_state") != "pending" for x in entries)
    pending = sum(x.get("revalidation_state") == "pending" for x in entries)
    require((terminal, pending) == (95, 97), f"unexpected pre-V2.4 counts {(terminal, pending)}")
    require(reg.get("next_revalidation_block") == "COMMON", f"unexpected next block {reg.get('next_revalidation_block')}")
    prev = reg.get("revalidation_blocks", {}).get("COMMON_V2.3", {})
    require(prev.get("state") == "completed" and prev.get("next_subblock") == "COMMON_V2.4", "COMMON V2.3 does not route to COMMON V2.4")
    require("COMMON_V2.4" not in reg.get("revalidation_blocks", {}), "COMMON V2.4 already closed")
    require(by_id.get(FINDING, {}).get("revalidation_state") == "pending", f"{FINDING} is not pending")

    delta = json.loads(DELTA.read_text(encoding="utf-8"))
    require(delta.get("document_id") == "COMMON_V2.4", "wrong V2.4 delta document id")
    auth = delta.get("selected_xsd_authority", {})
    require(auth.get("status") == "candidate_integration_explicit_selection", "V2.4 candidate authority status changed")
    require(auth.get("release_tag") is None and auth.get("official_release_authority") is False, "V2.4 was incorrectly promoted to official release authority")
    require(auth.get("candidate_branch") == "candidate/dms-v2.4-xsd", "V2.4 candidate branch changed")
    require(auth.get("upstream_draft_pr") == "VDVde/VDV301#31", "V2.4 draft PR provenance changed")
    require(auth.get("latest_xsd_wins") is False, "V2.4 latest-wins guard changed")
    unique = delta.get("new_unique_findings", {}).get(FINDING, {})
    require(unique.get("state") == "executable_confirmed_EV-122", "historical V2.4 finding state changed")
    require(unique.get("classification") == "pdf_xsd_type_shape_and_cardinality_mismatch", "V2.4 finding classification changed")
    require(unique.get("executable_effect") is True, "V2.4 finding lost executable effect")
    require(unique.get("authority_scope") == "selected_candidate_integration_V2.4_only_until_official_release_exists", "V2.4 finding authority scope changed")

    fresh = FRESH.read_text(encoding="utf-8")
    deep = DEEP_READ.read_text(encoding="utf-8")
    for anchor in (
        "FR-COM24-008",
        "LineInformation LineName / LineShortName type and multiplicity",
        "`LineName` `0:1` `IBIS-IP.string`",
        "`LineShortName` `0:1` `IBIS-IP.string`",
        "InternationalTextType",
        "maxOccurs=\"unbounded\"",
    ):
        require(anchor in fresh, f"Fresh Read anchor missing: {anchor}")
    require("DRCOM24-001" in deep and "EV-122" in deep, "V2.4 closure record lacks DRCOM24-001 / EV-122")

    root = etree.parse(str(COMMON)).getroot()
    includes = [x.get("schemaLocation") for x in root.findall("xs:include", NS)]
    require("IBIS-IP_Enumerations_V2.4.xsd" in includes, "Common V2.4 include route changed")
    line = root.find("xs:complexType[@name='LineInformationStructure']", NS)
    require(line is not None, "LineInformationStructure missing")
    for name in ("LineName", "LineShortName"):
        node = line.find(f".//xs:element[@name='{name}']", NS)
        require(node is not None, f"LineInformation.{name} missing")
        require(node.get("type") == "InternationalTextType", f"LineInformation.{name} type changed")
        require(occurs(node, "minOccurs") == "0" and occurs(node, "maxOccurs") == "unbounded", f"LineInformation.{name} cardinality changed")
    etree.XMLSchema(etree.parse(str(COMMON)))

    ev122 = subprocess.run([sys.executable, str(EV122)], text=True, capture_output=True)
    print(ev122.stdout, end="")
    if ev122.stderr: print(ev122.stderr, file=sys.stderr, end="")
    require(ev122.returncode == 0, "preserved EV-122 rerun failed")
    for line_text in (
        "LineInformation candidate InternationalText LineName VALID",
        "LineInformation repeated LineName candidate-valid VALID",
        "LineInformation PDF IBIS-IP.string LineName shape INVALID",
        "LineInformation candidate InternationalText LineShortName VALID",
        "LineInformation repeated LineShortName candidate-valid VALID",
    ):
        require(line_text in ev122.stdout, f"EV-122 executable boundary missing: {line_text}")

    # Discover the substantive LineInformation table page directly from the exact PDF.
    matches = []
    for page in range(1, EXPECTED_PDF_PAGES + 1):
        text = page_text(page)
        if all(token in text for token in ("LineInformation", "LineName", "LineShortName", "IBIS-IP.string")):
            matches.append(page)
    require(matches, "no PDF page contains the full LineInformation/LineName/LineShortName/IBIS-IP.string evidence set")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "render_pages.txt").write_text("".join(f"{p}\n" for p in matches), encoding="utf-8")
    result = {
        "evidence_id": "EV-140",
        "finding_block": [FINDING],
        "pdf_source_id": "COMMON_V2.4",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "pdf_page_count": EXPECTED_PDF_PAGES,
        "evidence_pages": {FINDING: matches},
        "authority_lane": "candidate_integration_explicit_selection",
        "official_release_tag": None,
        "official_release_authority": False,
        "candidate_branch": "candidate/dms-v2.4-xsd",
        "upstream_draft_pr": "VDVde/VDV301#31",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "base_evidence": "EV-122 rerun unchanged",
        "active_disproof": {
            "PDF_claim": "LineName and LineShortName are IBIS-IP.string 0:1",
            "selected_candidate_XSD": "both are InternationalTextType 0:*",
            "candidate_InternationalText_shapes": "VALID in preserved EV-122 rerun",
            "repeated_LineName_and_LineShortName": "VALID in preserved EV-122 rerun",
            "PDF_value_only_LineName_shape": "INVALID in preserved EV-122 rerun"
        },
        "terminal_revalidation_recommendations": {FINDING: "executable_confirmed"},
        "visual_review": "all discovered substantive pages must be rendered and inspected before permanent evidence record and closure",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS_PENDING_VISUAL_REVIEW"
    }
    (OUT_DIR / "ev140_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED_TEXT_XSD: EV-140 COMMON V2.4 DRCOM24-001; visual page review still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
