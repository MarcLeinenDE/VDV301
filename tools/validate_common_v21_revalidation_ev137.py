#!/usr/bin/env python3
"""EV-137 fail-closed revalidation evidence for COMMON V2.1 DRCOM21-001."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/COMMON_V2.1.pdf")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.1.md")
DELTA = Path("audit_registry/deep_read_findings_delta_common_v21_2026-09-02.json")
COMMON = Path("IBIS-IP_common_V2.1.xsd")
ENUMS = Path("IBIS-IP_Enumerations_V2.1.xsd")
EV119 = Path("tools/validate_common_v21_ev119.py")
OUT_DIR = Path(os.environ.get("EV137_OUTPUT_DIR", "artifacts/ev137"))

EXPECTED_PDF_SHA256 = "a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32"
EXPECTED_PDF_SIZE = 1274051
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_DEEP_READ_BLOB = "91cf693217d3b0df5309a0f8a242cfd4895a59fa"
EXPECTED_DELTA_BLOB = "44e06e66b65d7a7909d0e37ac3e6657f94e6a092"
EXPECTED_COMMON_BLOB = "05977c9f86c7c9dd0b48f36a4a4e9be32e94659e"
EXPECTED_ENUM_BLOB = "311464690ad60749ed8d326217787e4b8ed0b718"
EXPECTED_EV119_BLOB = "fb892931b74d32a69177fbe32356a08fc758534a"
FINDING = "DRCOM21-001"
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
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def main() -> int:
    require(PDF.exists(), f"missing PDF {PDF}")
    for path, expected in {
        FROZEN: EXPECTED_FROZEN_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        DELTA: EXPECTED_DELTA_BLOB,
        COMMON: EXPECTED_COMMON_BLOB,
        ENUMS: EXPECTED_ENUM_BLOB,
        EV119: EXPECTED_EV119_BLOB,
    }.items():
        require(path.is_file(), f"missing immutable source {path}")
        require(blob(path) == expected, f"immutable blob changed for {path}: {blob(path)}")

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
    require((terminal, pending) == (92, 100), f"unexpected pre-V2.1 counts {(terminal, pending)}")
    require(reg.get("next_revalidation_block") == "COMMON", f"unexpected next block {reg.get('next_revalidation_block')}")
    prev = reg.get("revalidation_blocks", {}).get("COMMON_V2.0", {})
    require(prev.get("state") == "completed" and prev.get("next_subblock") == "COMMON_V2.1", "COMMON V2.0 does not route to COMMON V2.1")
    require("COMMON_V2.1" not in reg.get("revalidation_blocks", {}), "COMMON V2.1 already closed")
    require(by_id.get(FINDING, {}).get("revalidation_state") == "pending", f"{FINDING} is not pending")

    delta = json.loads(DELTA.read_text(encoding="utf-8"))
    require(delta.get("document_id") == "COMMON_V2.1", "wrong V2.1 delta document id")
    require(delta.get("exact_xsd_authority", {}).get("official_tag") == "VDV-301-2.1", "wrong V2.1 official tag")
    unique = delta.get("new_unique_findings", {}).get(FINDING, {})
    require(unique.get("state") == "executable_confirmed_EV-119", "historical V2.1 finding state changed")
    require(unique.get("classification") == "cardinality_xsd_more_permissive_than_pdf", "V2.1 finding classification changed")
    require(unique.get("executable_effect") is True, "V2.1 finding lost executable effect")

    deep = DEEP_READ.read_text(encoding="utf-8")
    for anchor in (
        "FR-COM21-OBS-013",
        "StopInformationRequest.StopName is 0:1 in the PDF but 0:* in the XSD",
        "Page 29 visibly specifies `StopName 0:1`",
        "DRCOM21-001",
    ):
        require(anchor in deep, f"Deep Read anchor missing: {anchor}")

    root = etree.parse(str(COMMON)).getroot()
    include = root.find("xs:include", NS)
    require(include is not None and include.get("schemaLocation") == "IBIS-IP_Enumerations_V2.1.xsd", "Common V2.1 include route changed")
    ctype = root.find("xs:complexType[@name='StopInformationRequestStructure']", NS)
    require(ctype is not None, "StopInformationRequestStructure missing")
    stop_name = ctype.find(".//xs:element[@name='StopName']", NS)
    require(stop_name is not None, "StopInformationRequest.StopName missing")
    require(stop_name.get("minOccurs", "1") == "0", "StopInformationRequest.StopName minOccurs is not 0")
    require(stop_name.get("maxOccurs", "1") == "unbounded", "StopInformationRequest.StopName maxOccurs is not unbounded")
    etree.XMLSchema(etree.parse(str(COMMON)))

    ev119 = subprocess.run([sys.executable, str(EV119)], text=True, capture_output=True)
    print(ev119.stdout, end="")
    if ev119.stderr:
        print(ev119.stderr, file=sys.stderr, end="")
    require(ev119.returncode == 0, "preserved EV-119 rerun failed")
    require(
        "StopInformationRequest two StopName entries accepted by XSD: VALID as expected" in ev119.stdout,
        "EV-119 repeated StopName executable boundary missing",
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "render_pages.txt").write_text("29\n", encoding="utf-8")
    result = {
        "evidence_id": "EV-137",
        "finding_block": [FINDING],
        "pdf_source_id": "COMMON_V2.1",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "evidence_pages": {FINDING: [29]},
        "authority_lane": "exact_official_VDV-301-2.1_release_family",
        "official_release_tag": "VDV-301-2.1",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "base_evidence": "EV-119 rerun unchanged",
        "active_disproof": {
            "PDF_claim": "StopInformationRequest.StopName 0:1 on page 29",
            "exact_XSD_declaration": "StopInformationRequest.StopName minOccurs=0 maxOccurs=unbounded",
            "two_StopName_instance": "VALID in preserved EV-119 rerun"
        },
        "terminal_revalidation_recommendations": {FINDING: "executable_confirmed"},
        "visual_review": "rendered page 29 required before permanent evidence record and closure",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS_PENDING_VISUAL_REVIEW"
    }
    (OUT_DIR / "ev137_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED_TEXT_XSD: EV-137 COMMON V2.1 DRCOM21-001; visual page 29 review still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
