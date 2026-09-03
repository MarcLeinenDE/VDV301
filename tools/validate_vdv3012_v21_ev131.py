#!/usr/bin/env python3
"""EV-131 evidence gate for VDV301-2 Base V2.1 DR3012V21-001.

The finding is a documentation/routing cross-reference defect. The gate therefore
verifies the exact byte-pinned PDF, visible stale-reference pages, the official
mixed-version VDV-301-2.1 XSD authority route, and the catalog identities of
VDV 301-2-2 / 301-2-4. No XML-validity defect is invented.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/VDV301-2_BASE_V2.1.pdf")
SOURCE_REGISTRY = Path("audit_registry/pdf_source_registry_v0.1.json")
PIN_REGISTRY = Path("audit_registry/pdf_source_pins_v0.1.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
DMS_XSD = Path("IBIS-IP_DeviceManagementService_V2.1.xsd")
SYSTEM_DOC_XSD = Path("IBIS-IP_SystemDocumentationService_V2.0.xsd")
SYSTEM_MGMT_XSD = Path("IBIS-IP_SystemManagementService_V1.0.xsd")
COMMON_XSD = Path("IBIS-IP_common_V2.1.xsd")
ENUM_XSD = Path("IBIS-IP_Enumerations_V2.1.xsd")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/VDV301-2_BASE_V2.1.md")
OUT_DIR = Path(os.environ.get("EV131_OUTPUT_DIR", "artifacts/ev131"))

EXPECTED_PDF_SHA256 = "685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a"
EXPECTED_PDF_SIZE = 2671005
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_DMS_BLOB = "191b43e01cdaba14b247725689a913c244a67eed"
EXPECTED_SYSTEM_DOC_BLOB = "ab959dddbfa2b8ca420af1b079501f94cff38051"
EXPECTED_SYSTEM_MGMT_BLOB = "2d32630a0f1981e980e6a466e3f6a69136410f24"
EXPECTED_COMMON_BLOB = "05977c9f86c7c9dd0b48f36a4a4e9be32e94659e"
EXPECTED_ENUM_BLOB = "311464690ad60749ed8d326217787e4b8ed0b718"
FINDING_ID = "DR3012V21-001"
TERMINAL_RECOMMENDATION = "context_verified"


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


def find_source(registry: dict, source_id: str) -> dict:
    for item in registry.get("sources", []):
        if item.get("source_id") == source_id:
            return item
    fail(f"source not found: {source_id}")


def main() -> int:
    require(PDF.exists(), f"missing fetched PDF: {PDF}")
    require(git_blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory changed")
    require(git_blob(DMS_XSD) == EXPECTED_DMS_BLOB, "DMS V2.1 XSD changed")
    require(git_blob(SYSTEM_DOC_XSD) == EXPECTED_SYSTEM_DOC_BLOB, "SystemDocumentation V2.0 XSD changed")
    require(git_blob(SYSTEM_MGMT_XSD) == EXPECTED_SYSTEM_MGMT_BLOB, "SystemManagement V1.0 XSD changed")
    require(git_blob(COMMON_XSD) == EXPECTED_COMMON_BLOB, "Common V2.1 XSD changed")
    require(git_blob(ENUM_XSD) == EXPECTED_ENUM_BLOB, "Enumerations V2.1 XSD changed")

    pdf_hash, pdf_size = sha256_file(PDF)
    require(pdf_hash == EXPECTED_PDF_SHA256, f"Base V2.1 PDF hash mismatch: {pdf_hash}")
    require(pdf_size == EXPECTED_PDF_SIZE, f"Base V2.1 PDF size mismatch: {pdf_size}")

    frozen = load(FROZEN)
    require(frozen.get("entry_count") == 192 and frozen.get("state") == "frozen", "frozen inventory invariant failed")
    require(FINDING_ID in frozen.get("finding_ids", []), f"missing frozen finding {FINDING_ID}")

    sources = load(SOURCE_REGISTRY)
    pins = load(PIN_REGISTRY)
    src = find_source(sources, "VDV301-2_BASE_V2.1")
    pin = find_source(pins, "VDV301-2_BASE_V2.1")
    require(src.get("vdv_part") == "301-2" and src.get("version") == "2.1", "Base V2.1 source identity changed")
    require(pin.get("expected_sha256") == EXPECTED_PDF_SHA256, "Base V2.1 pin hash changed")
    require(int(pin.get("expected_size_bytes")) == EXPECTED_PDF_SIZE, "Base V2.1 pin size changed")

    # Exact VDV-301-2.1 release route: DMS 2.1, SystemDocumentation 2.0, SystemManagement 1.0.
    etree.XMLSchema(etree.parse(str(DMS_XSD)))
    etree.XMLSchema(etree.parse(str(SYSTEM_DOC_XSD)))
    etree.XMLSchema(etree.parse(str(SYSTEM_MGMT_XSD)))
    dms_text = DMS_XSD.read_text(encoding="utf-8")
    sysdoc_text = SYSTEM_DOC_XSD.read_text(encoding="utf-8")
    sysmgmt_text = SYSTEM_MGMT_XSD.read_text(encoding="utf-8")
    require('schemaLocation="IBIS-IP_common_V2.1.xsd"' in dms_text and 'schemaLocation="IBIS-IP_Enumerations_V2.1.xsd"' in dms_text, "DMS V2.1 dependency route changed")
    require('schemaLocation="IBIS-IP_common_V2.0.xsd"' in sysdoc_text and 'schemaLocation="IBIS-IP_Enumerations_V2.0.xsd"' in sysdoc_text, "SystemDocumentation V2.0 dependency route changed")
    require('schemaLocation="IBIS-IP_common_V1.0.xsd"' in sysmgmt_text and 'schemaLocation="IBIS-IP_Enumerations_V1.0.xsd"' in sysmgmt_text, "SystemManagement V1.0 dependency route changed")

    # Visible stale-reference evidence.
    p59 = page_text(59)
    p60 = page_text(60)
    p69 = page_text(69)
    p70 = page_text(70)
    p75 = page_text(75)
    p76 = page_text(76)
    require("DeviceManagementService (vgl. VDV 301-2-2)" in p59, "page 59 DMS->301-2-2 anchor missing")
    require("SystemDocumentationService (vgl. VDV 301-2-4)" in p59, "page 59 SystemDocumentation->301-2-4 anchor missing")
    require("DeviceManagementService (cf. VDV 301-2-2)" in p60, "page 60 English DMS->301-2-2 anchor missing")
    require("DeviceManagementService (vgl. VDV 301-2-2)" in p69, "page 69 DMS system-start stale reference missing")
    require("SystemDocumentationService im IBIS-IP-System (vgl. auch VDV 301-2-4)" in p69, "page 69 SystemDocumentation stale reference missing")
    require("SystemDocumentationService exists in the IBIS-IP system" in p70 and "VDV 301-2-4" in p70, "page 70 English SystemDocumentation stale reference missing")
    require("VDV 301-2-2" in p75 and "DeviceManagementServices" in p75, "page 75 repeated DMS stale reference missing")
    require("VDV 301-2-2" in p76 and "DeviceManagementServices" in p76, "page 76 English repeated DMS stale reference missing")

    # Active disproof: those document numbers are assigned to other service documents in the official source catalog.
    bls = find_source(sources, "BLS_V1.0")
    dls = find_source(sources, "DLS_V1.0")
    require(bls.get("vdv_part") == "301-2-2", "official source registry no longer assigns 301-2-2 to BLS")
    require(dls.get("vdv_part") == "301-2-4", "official source registry no longer assigns 301-2-4 to DLS")
    require(bls.get("document_id") == "BLS_V1.0", "BLS identity changed")
    require(dls.get("document_id") == "DLS_V1.0", "DLS identity changed")
    print("OK DR3012V21-001 stale DMS/SystemDocumentation service-document cross references confirmed")

    deep_read = DEEP_READ.read_text(encoding="utf-8")
    require(FINDING_ID in deep_read, "historical deep-read record missing finding")
    require("DR3012V20-006 is a V2.0 documentation issue and is not carried forward as a V2.1 defect" in deep_read, "V2.0 missing-heading resolution context missing")
    require("DMS 2.1 / SystemDocumentation 2.0 / SystemManagement 1.0" in deep_read, "mixed-version resolver context missing")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result = {
        "evidence_id": "EV-131",
        "finding_block": [FINDING_ID],
        "pdf_source_id": "VDV301-2_BASE_V2.1",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "selected_xsd_family": "official VDV-301-2.1 mixed route: DMS 2.1 / SystemDocumentation 2.0 / SystemManagement 1.0",
        "device_management_xsd_blob": EXPECTED_DMS_BLOB,
        "system_documentation_xsd_blob": EXPECTED_SYSTEM_DOC_BLOB,
        "system_management_xsd_blob": EXPECTED_SYSTEM_MGMT_BLOB,
        "common_v21_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_v21_xsd_blob": EXPECTED_ENUM_BLOB,
        "visual_pages": [59, 60, 69, 70, 75, 76],
        "active_disproof": {
            "vdv_301_2_2_catalog_identity": "BLS_V1.0",
            "vdv_301_2_4_catalog_identity": "DLS_V1.0",
            "schema_routing_rule": "ignore stale prose document numbers; use exact release/tag and version-sharp service manifest"
        },
        "terminal_revalidation_recommendations": {FINDING_ID: TERMINAL_RECOMMENDATION},
        "executable_evidence_reason_not_applicable": "The finding concerns stale prose document-number routing and does not define XML instance validity. Exact service XSDs are compiled only to prove the release authority route.",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS"
    }
    (OUT_DIR / "ev131_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED: EV-131 VDV301-2 Base V2.1 DR3012V21-001 revalidation evidence gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
