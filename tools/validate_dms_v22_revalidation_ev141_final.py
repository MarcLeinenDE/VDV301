#!/usr/bin/env python3
"""Final EV-141 gate for frozen DMS V2.2 deep-read findings.

The first EV-141 attempt deliberately failed closed because it tried to validate
a service-group member as a global XML root.  DMS operations in this service XSD
are group members, so this final checker tests the actual declaration boundary.
"""
from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from lxml import etree

import validate_dms_v22_revalidation_ev141 as base


def main() -> int:
    base.require(base.PDF.is_file(), f"missing {base.PDF}")
    for path, expected in {
        base.FROZEN: base.EXPECTED_FROZEN_BLOB,
        base.DEEP_READ: base.EXPECTED_DEEP_READ_BLOB,
        base.DELTA: base.EXPECTED_DELTA_BLOB,
        base.REGISTRY_DELTA: base.EXPECTED_REGISTRY_DELTA_BLOB,
        base.DMS: base.EXPECTED_DMS_BLOB,
        base.COMMON: base.EXPECTED_COMMON_BLOB,
        base.ENUMS: base.EXPECTED_ENUM_BLOB,
        base.EV107: base.EXPECTED_EV107_BLOB,
    }.items():
        base.require(path.is_file(), f"missing immutable source {path}")
        observed = base.blob(path)
        base.require(observed == expected, f"immutable blob changed for {path}: {observed}")

    sha, size = base.file_sha(base.PDF)
    base.require(sha == base.EXPECTED_PDF_SHA256, f"PDF hash mismatch {sha}")
    base.require(size == base.EXPECTED_PDF_SIZE, f"PDF size mismatch {size}")
    pages = base.pdf_page_count()

    frozen = json.loads(base.FROZEN.read_text(encoding="utf-8"))
    base.require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory invariant failed")
    for fid in base.FINDINGS:
        base.require(fid in frozen.get("finding_ids", []), f"{fid} missing from frozen inventory")

    reg = json.loads(base.REGISTRY.read_text(encoding="utf-8"))
    entries = reg.get("inventory", {}).get("entries", [])
    by_id = {x.get("finding_id"): x for x in entries}
    terminal = sum(x.get("revalidation_state") != "pending" for x in entries)
    pending = sum(x.get("revalidation_state") == "pending" for x in entries)
    base.require((terminal, pending) == (96, 96), f"unexpected pre-DMS-V2.2 counts {(terminal, pending)}")
    base.require(reg.get("next_revalidation_block") == "DMS", f"unexpected next block {reg.get('next_revalidation_block')}")
    common24 = reg.get("revalidation_blocks", {}).get("COMMON_V2.4", {})
    base.require(common24.get("state") == "completed" and common24.get("next_subblock") == "DMS_V2.2", "COMMON V2.4 does not route to DMS V2.2")
    base.require("DMS_V2.2" not in reg.get("revalidation_blocks", {}), "DMS V2.2 already closed")
    for fid in base.FINDINGS:
        base.require(by_id.get(fid, {}).get("revalidation_state") == "pending", f"{fid} is not pending")
    base.require(by_id.get("DRDMS24-001", {}).get("revalidation_state") == "pending", "next DMS V2.4 finding is not pending")

    delta = json.loads(base.DELTA.read_text(encoding="utf-8"))
    base.require(delta.get("document_id") == "DMS_V2.2", "wrong DMS V2.2 finding delta")
    delta_by_id = {x.get("id"): x for x in delta.get("new_findings", [])}
    base.require(set(delta_by_id) == set(base.FINDINGS), f"unexpected DMS V2.2 finding set {sorted(delta_by_id)}")
    deep = base.DEEP_READ.read_text(encoding="utf-8")
    for fid in base.FINDINGS:
        base.require(fid in deep, f"deep-read record missing {fid}")
    base.require("DMS V2.2 is an official historical profile in this repository" in deep, "official historical authority statement missing")
    base.require(base.EXPECTED_DMS_BLOB in deep, "DMS V2.2 authority blob missing from deep read")

    root = etree.parse(str(base.DMS)).getroot()
    includes = [x.get("schemaLocation") for x in root.findall("xs:include", base.NS)]
    base.require("IBIS-IP_common_V2.2.xsd" in includes and "IBIS-IP_Enumerations_V2.2.xsd" in includes, f"DMS V2.2 include route changed: {includes}")
    etree.XMLSchema(etree.parse(str(base.DMS)))

    ev107 = subprocess.run([sys.executable, str(base.EV107)], text=True, capture_output=True)
    print(ev107.stdout, end="")
    if ev107.stderr:
        print(ev107.stderr, file=sys.stderr, end="")
    base.require(ev107.returncode == 0, "preserved EV-107 rerun failed")
    base.require("InstallationSuccessful" in ev107.stdout and "InstallationSuccessfull" in ev107.stdout, "EV-107 enum boundary output changed")

    # DRDMS22-003: actual executable enum boundary through a temporary root adapter.
    adapter = """<?xml version='1.0'?>\n<xs:schema xmlns:xs='http://www.w3.org/2001/XMLSchema'>\n  <xs:include schemaLocation='IBIS-IP_DeviceManagementService_V2.2.xsd'/>\n  <xs:element name='ProbeUpdateStatus' type='UpdateStatusEnumeration'/>\n</xs:schema>\n"""
    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile("w", suffix=".xsd", prefix="ev141_", dir=".", delete=False, encoding="utf-8") as fh:
            fh.write(adapter); tmp_path = Path(fh.name)
        probe_schema = etree.XMLSchema(etree.parse(str(tmp_path)))
        good = etree.fromstring(b"<ProbeUpdateStatus>InstallationSuccessful</ProbeUpdateStatus>")
        bad = etree.fromstring(b"<ProbeUpdateStatus>InstallationSuccessfull</ProbeUpdateStatus>")
        base.require(probe_schema.validate(good), "InstallationSuccessful should validate")
        base.require(not probe_schema.validate(bad), "InstallationSuccessfull typo unexpectedly validates")
    finally:
        if tmp_path and tmp_path.exists():
            tmp_path.unlink()
    print("OK DRDMS22-003 InstallationSuccessful VALID; InstallationSuccessfull INVALID")

    # DRDMS22-004: the service XSD models operations inside DeviceManagementServiceGroup,
    # not as global roots.  Test that exact declaration boundary instead of inventing
    # a root-validation contract.
    groups = root.xpath("./xs:group[@name='DeviceManagementServiceGroup']", namespaces=base.NS)
    base.require(len(groups) == 1, f"DeviceManagementServiceGroup count changed: {len(groups)}")
    operation_names = list(groups[0].xpath("./xs:sequence/xs:element/@name", namespaces=base.NS))
    plural = "DeviceManagementService.GetDeviceErrorMessagesRequest"
    singular = "DeviceManagementService.GetDeviceErrorMessageRequest"
    base.require(plural in operation_names, f"plural operation declaration missing: {plural}")
    base.require(singular not in operation_names, f"singular prose alias unexpectedly declared: {singular}")
    base.require(any(name == "DeviceManagementService.GetDeviceErrorMessagesResponse" for name in operation_names), "plural response declaration missing")
    print("OK DRDMS22-004 service group declares plural GetDeviceErrorMessages; singular alias absent")

    # Find the exact original pages for all four findings and their strongest disproof context.
    wrong_ref = base.pages_matching(pages, lambda t: "SubdeviceStatusInformation" in t and "DeviceStatusInformation" in t and "27" in t)
    table19 = base.pages_matching(pages, lambda t: "DeviceStatusInformationStructure" in t and re.search(r"(?:Table|Tabelle)\s+19\b", base.compact(t), flags=re.I) is not None)
    table27 = base.pages_matching(pages, lambda t: "InstallUpdateRequestStructure" in t and re.search(r"(?:Table|Tabelle)\s+27\b", base.compact(t), flags=re.I) is not None)
    base.require(wrong_ref, "DRDMS22-001 wrong table-27 reference page not found")
    base.require(table19, "DRDMS22-001 table 19 status-definition page not found")
    base.require(table27, "DRDMS22-001 table 27 InstallUpdate page not found")

    toc = base.pages_matching(pages, lambda t: all(x in t for x in ("GetUpdateHistory", "FinalizeUpdate", "FinalizeAllPendingUpdates")) and all(x in t for x in ("1.33", "1.34", "1.35")))
    body33 = base.pages_matching(pages, lambda t: "GetUpdateHistory" in t and "2.33" in t)
    body34 = base.pages_matching(pages, lambda t: "FinalizeUpdate" in t and "2.34" in t)
    body35 = base.pages_matching(pages, lambda t: "FinalizeAllPendingUpdates" in t and "2.35" in t)
    base.require(toc, "DRDMS22-002 TOC 1.33/1.34/1.35 page not found")
    base.require(body33 and body34 and body35, "DRDMS22-002 body 2.33/2.34/2.35 evidence incomplete")

    typo_pages = base.pages_matching(pages, lambda t: "InstallationSuccessfull" in t)
    correct_pages = base.pages_matching(pages, lambda t: "InstallationSuccessful" in t)
    base.require(typo_pages, "DRDMS22-003 typo prose page not found")
    base.require(correct_pages, "DRDMS22-003 correct enumeration page not found")

    singular_pages = base.pages_matching(pages, lambda t: "GetDeviceErrorMessages" in t and re.search(r"GetDeviceErrorMessage(?!s)", t) is not None)
    base.require(singular_pages, "DRDMS22-004 singular/plural wording page not found")

    evidence_pages = {
        "DRDMS22-001": sorted(set(wrong_ref + table19 + table27)),
        "DRDMS22-002": sorted(set(toc + body33 + body34 + body35)),
        "DRDMS22-003": sorted(set(typo_pages + correct_pages)),
        "DRDMS22-004": sorted(set(singular_pages)),
    }
    all_pages = sorted({p for values in evidence_pages.values() for p in values})
    base.OUT_DIR.mkdir(parents=True, exist_ok=True)
    (base.OUT_DIR / "render_pages.txt").write_text("".join(f"{p}\n" for p in all_pages), encoding="utf-8")
    (base.OUT_DIR / "page_map.json").write_text(json.dumps(evidence_pages, indent=2) + "\n", encoding="utf-8")

    result = {
        "evidence_id": "EV-141",
        "finding_block": list(base.FINDINGS),
        "pdf_source_id": "DMS_V2.2",
        "pdf_sha256": base.EXPECTED_PDF_SHA256,
        "pdf_size_bytes": base.EXPECTED_PDF_SIZE,
        "pdf_page_count": pages,
        "evidence_pages": evidence_pages,
        "authority_lane": "official_historical_DMS_V2.2_exact_XSD_family",
        "dms_xsd_blob": base.EXPECTED_DMS_BLOB,
        "common_xsd_blob": base.EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": base.EXPECTED_ENUM_BLOB,
        "base_evidence": "EV-107 rerun unchanged",
        "failed_attempt_correction": "initial EV-141 root-validation assumption withdrawn; DMS service operations are group members and the corrected gate checks DeviceManagementServiceGroup declarations",
        "active_disproof": {
            "DRDMS22-001": "table 27 is independently located as InstallUpdateRequestStructure while table 19 is DeviceStatusInformationStructure",
            "DRDMS22-002": "TOC 1.33/1.34/1.35 is compared against body headings 2.33/2.34/2.35",
            "DRDMS22-003": "InstallationSuccessfull is tested as a possible enum alias and rejected; InstallationSuccessful validates",
            "DRDMS22-004": "singular GetDeviceErrorMessageRequest is tested as a possible service-group alias and is absent; plural GetDeviceErrorMessagesRequest is declared",
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
    (base.OUT_DIR / "ev141_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED_TEXT_XSD: EV-141 final DMS V2.2 DRDMS22-001..004; visual review still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
