#!/usr/bin/env python3
"""EV-139 fail-closed revalidation evidence for COMMON V2.3 DRCOM23-001."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/COMMON_V2.3.pdf")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.3_FRESH_2026-09-02.md")
DELTA = Path("audit_registry/deep_read_findings_delta_common_v23_2026-09-02.json")
COMMON = Path("IBIS-IP_common_V2.3.xsd")
ENUMS = Path("IBIS-IP_Enumerations_V2.2.xsd")
EV121 = Path("tools/validate_common_v23_ev121.py")
OUT_DIR = Path(os.environ.get("EV139_OUTPUT_DIR", "artifacts/ev139"))

EXPECTED_PDF_SHA256 = "d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b"
EXPECTED_PDF_SIZE = 793521
EXPECTED_PDF_PAGES = 58
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_DEEP_READ_BLOB = "cf6060cc9639de64edacdfa84a4cb336fc28c0e6"
EXPECTED_DELTA_BLOB = "2bf1f8555ecad4c050d78750dd7326dd28c9484a"
EXPECTED_COMMON_BLOB = "0d8926c4063c12de9a5e68b6f0addaab35a55dc1"
EXPECTED_ENUM_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"
EXPECTED_EV121_BLOB = "79a55a6eed8eacdc2f853b4380a987beea14b40c"
FINDING = "DRCOM23-001"
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


def main() -> int:
    require(PDF.exists(), f"missing PDF {PDF}")
    for path, expected in {
        FROZEN: EXPECTED_FROZEN_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        DELTA: EXPECTED_DELTA_BLOB,
        COMMON: EXPECTED_COMMON_BLOB,
        ENUMS: EXPECTED_ENUM_BLOB,
        EV121: EXPECTED_EV121_BLOB,
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
    require((terminal, pending) == (94, 98), f"unexpected pre-V2.3 counts {(terminal, pending)}")
    require(reg.get("next_revalidation_block") == "COMMON", f"unexpected next block {reg.get('next_revalidation_block')}")
    prev = reg.get("revalidation_blocks", {}).get("COMMON_V2.2", {})
    require(prev.get("state") == "completed" and prev.get("next_subblock") == "COMMON_V2.3", "COMMON V2.2 does not route to COMMON V2.3")
    require("COMMON_V2.3" not in reg.get("revalidation_blocks", {}), "COMMON V2.3 already closed")
    require(by_id.get(FINDING, {}).get("revalidation_state") == "pending", f"{FINDING} is not pending")

    delta = json.loads(DELTA.read_text(encoding="utf-8"))
    require(delta.get("document_id") == "COMMON_V2.3", "wrong V2.3 delta document id")
    auth = delta.get("exact_xsd_authority", {})
    require(auth.get("official_tag") == "VDV-301-2.3", "wrong V2.3 official tag")
    require(auth.get("enumerations_file") == "IBIS-IP_Enumerations_V2.2.xsd", "V2.3 declared enumeration route changed")
    unique = delta.get("new_unique_findings", {}).get(FINDING, {})
    require(unique.get("state") == "executable_confirmed_EV-121", "historical V2.3 finding state changed")
    require(unique.get("classification") == "pdf_documents_elements_absent_from_xsd", "V2.3 finding classification changed")
    require(unique.get("executable_effect") is True, "V2.3 finding lost executable effect")

    deep = DEEP_READ.read_text(encoding="utf-8")
    for anchor in (
        "FR-COM23-011",
        "StopInformationRequest has cardinality drift plus two PDF fields absent from exact XSD",
        "ArrivalExpected   0:1",
        "DepartureExpected 0:1",
        "neither `ArrivalExpected` nor `DepartureExpected`",
    ):
        require(anchor in deep, f"Deep Read anchor missing: {anchor}")

    root = etree.parse(str(COMMON)).getroot()
    include = root.find("xs:include", NS)
    require(include is not None and include.get("schemaLocation") == "IBIS-IP_Enumerations_V2.2.xsd", "Common V2.3 include route changed")
    req = root.find("xs:complexType[@name='StopInformationRequestStructure']", NS)
    stop = root.find("xs:complexType[@name='StopInformationStructure']", NS)
    require(req is not None and stop is not None, "StopInformation structures missing")
    require(req.find(".//xs:element[@name='ArrivalExpected']", NS) is None, "StopInformationRequest unexpectedly contains ArrivalExpected")
    require(req.find(".//xs:element[@name='DepartureExpected']", NS) is None, "StopInformationRequest unexpectedly contains DepartureExpected")
    arr = stop.find(".//xs:element[@name='ArrivalExpected']", NS)
    dep = stop.find(".//xs:element[@name='DepartureExpected']", NS)
    require(arr is not None and arr.get("type") == "IBIS-IP.dateTime" and arr.get("minOccurs", "1") == "0", "StopInformation.ArrivalExpected authority changed")
    require(dep is not None and dep.get("type") == "IBIS-IP.dateTime" and dep.get("minOccurs", "1") == "0", "StopInformation.DepartureExpected authority changed")
    etree.XMLSchema(etree.parse(str(COMMON)))

    ev121 = subprocess.run([sys.executable, str(EV121)], text=True, capture_output=True)
    print(ev121.stdout, end="")
    if ev121.stderr: print(ev121.stderr, file=sys.stderr, end="")
    require(ev121.returncode == 0, "preserved EV-121 rerun failed")
    for line in (
        "Request ArrivalExpected rejected INVALID",
        "Request DepartureExpected rejected INVALID",
        "StopInformation expected fields valid VALID",
    ):
        require(line in ev121.stdout, f"EV-121 executable boundary missing: {line}")

    # Discover the substantive table page from the exact byte-pinned PDF; do not guess a page number.
    matches = []
    for page in range(1, EXPECTED_PDF_PAGES + 1):
        text = page_text(page)
        if all(token in text for token in ("StopInformationRequest", "ArrivalExpected", "DepartureExpected")):
            matches.append(page)
    require(matches, "no PDF page contains StopInformationRequest + ArrivalExpected + DepartureExpected")
    # Prefer a single substantive table page. Multiple matches are retained for visual inspection instead of silently choosing.
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "render_pages.txt").write_text("".join(f"{p}\n" for p in matches), encoding="utf-8")
    result = {
        "evidence_id": "EV-139",
        "finding_block": [FINDING],
        "pdf_source_id": "COMMON_V2.3",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "pdf_page_count": EXPECTED_PDF_PAGES,
        "evidence_pages": {FINDING: matches},
        "authority_lane": "exact_official_VDV-301-2.3_Common_plus_declared_Enumerations_V2.2",
        "official_release_tag": "VDV-301-2.3",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_file": "IBIS-IP_Enumerations_V2.2.xsd",
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "base_evidence": "EV-121 rerun unchanged",
        "active_disproof": {
            "PDF_claim": "StopInformationRequest contains optional ArrivalExpected and DepartureExpected",
            "exact_XSD_request_shape": "both elements absent",
            "request_ArrivalExpected": "INVALID in preserved EV-121 rerun",
            "request_DepartureExpected": "INVALID in preserved EV-121 rerun",
            "StopInformation_both_expected_fields": "VALID in preserved EV-121 rerun"
        },
        "terminal_revalidation_recommendations": {FINDING: "executable_confirmed"},
        "visual_review": "all discovered substantive pages must be rendered and inspected before permanent evidence record and closure",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS_PENDING_VISUAL_REVIEW"
    }
    (OUT_DIR / "ev139_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED_TEXT_XSD: EV-139 COMMON V2.3 DRCOM23-001; visual page review still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
