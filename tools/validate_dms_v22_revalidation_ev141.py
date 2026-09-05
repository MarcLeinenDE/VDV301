#!/usr/bin/env python3
"""EV-141 fail-closed revalidation evidence for frozen DMS V2.2 deep-read findings."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/DMS_V2.2.pdf")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/DMS_V2.2.md")
DELTA = Path("audit_registry/deep_read_findings_delta_dms_v22_2026-08-28.json")
REGISTRY_DELTA = Path("audit_registry/deep_read_registry_delta_dms_v22_2026-08-28.json")
DMS = Path("IBIS-IP_DeviceManagementService_V2.2.xsd")
COMMON = Path("IBIS-IP_common_V2.2.xsd")
ENUMS = Path("IBIS-IP_Enumerations_V2.2.xsd")
EV107 = Path("tools/validate_dms_v22_deep_read_ev107.py")
OUT_DIR = Path(os.environ.get("EV141_OUTPUT_DIR", "artifacts/ev141"))

EXPECTED_PDF_SHA256 = "72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e"
EXPECTED_PDF_SIZE = 1173719
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_DEEP_READ_BLOB = "009243f56e8a81e9fdac82ff96d0fb714c7ba45b"
EXPECTED_DELTA_BLOB = "e350612884c8c22ca7fc0e4839a03ac924abc076"
EXPECTED_REGISTRY_DELTA_BLOB = "d44cc214ebd85172579065b8091d2e91d9dbb4a4"
EXPECTED_DMS_BLOB = "c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d"
EXPECTED_COMMON_BLOB = "468fee6d177e7185dbcd5d3f90cfb114e29e01ae"
EXPECTED_ENUM_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"
EXPECTED_EV107_BLOB = "6acd2dc75131455e220ae18ce5131eeb5ad44789"
FINDINGS = ("DRDMS22-001", "DRDMS22-002", "DRDMS22-003", "DRDMS22-004")
NS = {"xs": "http://www.w3.org/2001/XMLSchema"}


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def file_sha(path: Path) -> tuple[str, int]:
    h = hashlib.sha256(); size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk); size += len(chunk)
    return h.hexdigest(), size


def pdf_page_count() -> int:
    text = subprocess.check_output(["pdfinfo", str(PDF)], text=True, errors="replace")
    m = re.search(r"^Pages:\s*(\d+)\s*$", text, flags=re.M)
    require(m is not None, "pdfinfo did not expose page count")
    return int(m.group(1))


def page_text(page: int) -> str:
    return subprocess.check_output(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(PDF), "-"],
        text=True, errors="replace"
    )


def compact(text: str) -> str:
    return " ".join(text.split())


def pages_matching(page_count: int, predicate) -> list[int]:
    out = []
    for page in range(1, page_count + 1):
        text = page_text(page)
        if predicate(text):
            out.append(page)
    return out


def main() -> int:
    require(PDF.is_file(), f"missing {PDF}")
    for path, expected in {
        FROZEN: EXPECTED_FROZEN_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        DELTA: EXPECTED_DELTA_BLOB,
        REGISTRY_DELTA: EXPECTED_REGISTRY_DELTA_BLOB,
        DMS: EXPECTED_DMS_BLOB,
        COMMON: EXPECTED_COMMON_BLOB,
        ENUMS: EXPECTED_ENUM_BLOB,
        EV107: EXPECTED_EV107_BLOB,
    }.items():
        require(path.is_file(), f"missing immutable source {path}")
        require(blob(path) == expected, f"immutable blob changed for {path}: {blob(path)}")

    sha, size = file_sha(PDF)
    require(sha == EXPECTED_PDF_SHA256, f"PDF hash mismatch {sha}")
    require(size == EXPECTED_PDF_SIZE, f"PDF size mismatch {size}")
    pages = pdf_page_count()

    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory invariant failed")
    for fid in FINDINGS:
        require(fid in frozen.get("finding_ids", []), f"{fid} missing from frozen inventory")

    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entries = reg.get("inventory", {}).get("entries", [])
    by_id = {x.get("finding_id"): x for x in entries}
    terminal = sum(x.get("revalidation_state") != "pending" for x in entries)
    pending = sum(x.get("revalidation_state") == "pending" for x in entries)
    require((terminal, pending) == (96, 96), f"unexpected pre-DMS-V2.2 counts {(terminal, pending)}")
    require(reg.get("next_revalidation_block") == "DMS", f"unexpected next block {reg.get('next_revalidation_block')}")
    common24 = reg.get("revalidation_blocks", {}).get("COMMON_V2.4", {})
    require(common24.get("state") == "completed" and common24.get("next_subblock") == "DMS_V2.2", "COMMON V2.4 does not route to DMS V2.2")
    require("DMS_V2.2" not in reg.get("revalidation_blocks", {}), "DMS V2.2 already closed")
    for fid in FINDINGS:
        require(by_id.get(fid, {}).get("revalidation_state") == "pending", f"{fid} is not pending")
    require(by_id.get("DRDMS24-001", {}).get("revalidation_state") == "pending", "next DMS V2.4 finding is not pending")

    delta = json.loads(DELTA.read_text(encoding="utf-8"))
    require(delta.get("document_id") == "DMS_V2.2", "wrong DMS V2.2 finding delta")
    delta_by_id = {x.get("id"): x for x in delta.get("new_findings", [])}
    require(set(delta_by_id) == set(FINDINGS), f"unexpected DMS V2.2 finding set {sorted(delta_by_id)}")
    deep = DEEP_READ.read_text(encoding="utf-8")
    for fid in FINDINGS:
        require(fid in deep, f"deep-read record missing {fid}")
    require("DMS V2.2 is an official historical profile in this repository" in deep, "official historical authority statement missing")
    require("c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d" in deep, "DMS V2.2 authority blob missing from deep read")

    root = etree.parse(str(DMS)).getroot()
    includes = [x.get("schemaLocation") for x in root.findall("xs:include", NS)]
    require("IBIS-IP_common_V2.2.xsd" in includes and "IBIS-IP_Enumerations_V2.2.xsd" in includes, f"DMS V2.2 include route changed: {includes}")
    schema = etree.XMLSchema(etree.parse(str(DMS)))

    # Preserved EV-107 must still pass unchanged.
    ev107 = subprocess.run([sys.executable, str(EV107)], text=True, capture_output=True)
    print(ev107.stdout, end="")
    if ev107.stderr:
        print(ev107.stderr, file=sys.stderr, end="")
    require(ev107.returncode == 0, "preserved EV-107 rerun failed")
    require("InstallationSuccessful" in ev107.stdout and "InstallationSuccessfull" in ev107.stdout, "EV-107 enum boundary output changed")

    # Stronger executable boundary for DRDMS22-003: use the selected schema's
    # UpdateStatusEnumeration in a temporary root adapter.
    adapter = """<?xml version='1.0'?>\n<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>\n  <xs:include schemaLocation='IBIS-IP_DeviceManagementService_V2.2.xsd'/>\n  <xs:element name='ProbeUpdateStatus' type='UpdateStatusEnumeration'/>\n</xs:schema>\n"""
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".xsd", prefix="ev141_", dir=".", delete=False, encoding="utf-8") as fh:
            fh.write(adapter); tmp_path = Path(fh.name)
        probe_schema = etree.XMLSchema(etree.parse(str(tmp_path)))
        good = etree.fromstring(b"<ProbeUpdateStatus>InstallationSuccessful</ProbeUpdateStatus>")
        bad = etree.fromstring(b"<ProbeUpdateStatus>InstallationSuccessfull</ProbeUpdateStatus>")
        require(probe_schema.validate(good), "InstallationSuccessful should validate")
        require(not probe_schema.validate(bad), "InstallationSuccessfull typo unexpectedly validates")
    finally:
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()
    print("OK DRDMS22-003 InstallationSuccessful VALID; InstallationSuccessfull INVALID")

    # DRDMS22-004: prove the selected schema exposes only the plural operation
    # as a global XML element; the singular prose spelling is not an alias.
    plural = etree.fromstring(b"<DeviceManagementService.GetDeviceErrorMessagesRequest/>")
    singular = etree.fromstring(b"<DeviceManagementService.GetDeviceErrorMessageRequest/>")
    require(schema.validate(plural), "plural GetDeviceErrorMessagesRequest should validate")
    require(not schema.validate(singular), "singular GetDeviceErrorMessageRequest unexpectedly validates")
    print("OK DRDMS22-004 plural GetDeviceErrorMessagesRequest VALID; singular alias INVALID")

    # Discover every substantive source page from the exact byte-pinned PDF.
    wrong_ref = pages_matching(pages, lambda t: "SubdeviceStatusInformation" in t and "DeviceStatusInformation" in t and "27" in t)
    table19 = pages_matching(pages, lambda t: "DeviceStatusInformationStructure" in t and re.search(r"(?:Table|Tabelle)\s+19\b", compact(t), flags=re.I) is not None)
    table27 = pages_matching(pages, lambda t: "InstallUpdateRequestStructure" in t and re.search(r"(?:Table|Tabelle)\s+27\b", compact(t), flags=re.I) is not None)
    require(wrong_ref, "DRDMS22-001 wrong table-27 reference page not found")
    require(table19, "DRDMS22-001 table 19 status-definition page not found")
    require(table27, "DRDMS22-001 table 27 InstallUpdate page not found")

    toc = pages_matching(pages, lambda t: all(x in t for x in ("GetUpdateHistory", "FinalizeUpdate", "FinalizeAllPendingUpdates")) and all(x in t for x in ("1.33", "1.34", "1.35")))
    body33 = pages_matching(pages, lambda t: "GetUpdateHistory" in t and "2.33" in t)
    body34 = pages_matching(pages, lambda t: "FinalizeUpdate" in t and "2.34" in t)
    body35 = pages_matching(pages, lambda t: "FinalizeAllPendingUpdates" in t and "2.35" in t)
    require(toc, "DRDMS22-002 TOC 1.33/1.34/1.35 page not found")
    require(body33 and body34 and body35, "DRDMS22-002 body 2.33/2.34/2.35 evidence incomplete")

    typo_pages = pages_matching(pages, lambda t: "InstallationSuccessfull" in t)
    correct_pages = pages_matching(pages, lambda t: "InstallationSuccessful" in t)
    require(typo_pages, "DRDMS22-003 typo prose page not found")
    require(correct_pages, "DRDMS22-003 correct enumeration page not found")

    singular_pages = pages_matching(pages, lambda t: "GetDeviceErrorMessages" in t and re.search(r"GetDeviceErrorMessage(?!s)", t) is not None)
    require(singular_pages, "DRDMS22-004 singular/plural wording page not found")

    evidence_pages = {
        "DRDMS22-001": sorted(set(wrong_ref + table19 + table27)),
        "DRDMS22-002": sorted(set(toc + body33 + body34 + body35)),
        "DRDMS22-003": sorted(set(typo_pages + correct_pages)),
        "DRDMS22-004": sorted(set(singular_pages)),
    }
    all_pages = sorted({p for values in evidence_pages.values() for p in values})
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "render_pages.txt").write_text("".join(f"{p}\n" for p in all_pages), encoding="utf-8")
    (OUT_DIR / "page_map.json").write_text(json.dumps(evidence_pages, indent=2) + "\n", encoding="utf-8")

    result = {
        "evidence_id": "EV-141",
        "finding_block": list(FINDINGS),
        "pdf_source_id": "DMS_V2.2",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "pdf_page_count": pages,
        "evidence_pages": evidence_pages,
        "authority_lane": "official_historical_DMS_V2.2_exact_XSD_family",
        "dms_xsd_blob": EXPECTED_DMS_BLOB,
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "base_evidence": "EV-107 rerun unchanged",
        "active_disproof": {
            "DRDMS22-001": "table 27 is independently located as InstallUpdateRequestStructure while table 19 is DeviceStatusInformationStructure",
            "DRDMS22-002": "TOC 1.33/1.34/1.35 is compared against body headings 2.33/2.34/2.35",
            "DRDMS22-003": "InstallationSuccessfull is tested as a possible enum alias and rejected; InstallationSuccessful validates",
            "DRDMS22-004": "singular GetDeviceErrorMessageRequest is tested as a possible operation alias and rejected; plural GetDeviceErrorMessagesRequest validates",
        },
        "terminal_revalidation_recommendations": {
            "DRDMS22-001": "context_verified",
            "DRDMS22-002": "context_verified",
            "DRDMS22-003": "executable_confirmed",
            "DRDMS22-004": "context_verified",
        },
        "visual_review": "all discovered substantive pages must be rendered and inspected before permanent evidence record and closure",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS_PENDING_VISUAL_REVIEW",
    }
    (OUT_DIR / "ev141_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED_TEXT_XSD: EV-141 DMS V2.2 DRDMS22-001..004; visual review still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
