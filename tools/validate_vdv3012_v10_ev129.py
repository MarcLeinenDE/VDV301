#!/usr/bin/env python3
"""EV-129 evidence gate for VDV301-2 V1.0 findings DR3012-001..007.

The gate is deliberately fail-closed. It verifies the exact byte-pinned VDV301-2
V1.0 PDF, visible-page text anchors, external RFC authority, historical TimeService
context, the exact official V1.0 SystemDocumentation/SystemManagement XSD route,
and executable identifier/type behaviour for DR3012-003.
"""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import urllib.request

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/VDV301-2_V1.0_DE.pdf")
SOURCE_REGISTRY = Path("audit_registry/pdf_source_registry_v0.1.json")
PIN_REGISTRY = Path("audit_registry/pdf_source_pins_v0.1.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
SYSTEM_DOC_XSD = Path("IBIS-IP_SystemDocumentationService_v1.0.xsd")
SYSTEM_MGMT_XSD = Path("IBIS-IP_SystemManagementService_V1.0.xsd")
TIME_REPORT = Path("docs/pdf_xsd_semantic_audit/deep_read/TIME_V1.0.md")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/VDV301-2_V1.0_DE.md")
OUT_DIR = Path(os.environ.get("EV129_OUTPUT_DIR", "artifacts/ev129"))

EXPECTED_PDF_SHA256 = "2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75"
EXPECTED_PDF_SIZE = 1790447
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_SYSTEM_DOC_BLOB = "8995c4a230bf81d5e47b9313ee7725ff3cd4b7b5"
EXPECTED_SYSTEM_MGMT_BLOB = "2d32630a0f1981e980e6a466e3f6a69136410f24"
FINDINGS = [f"DR3012-{i:03d}" for i in range(1, 8)]
TERMINAL_RECOMMENDATIONS = {
    "DR3012-001": "context_verified",
    "DR3012-002": "context_verified",
    "DR3012-003": "executable_confirmed",
    "DR3012-004": "context_verified",
    "DR3012-005": "context_verified",
    "DR3012-006": "context_verified",
    "DR3012-007": "context_verified",
}


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


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "VDV301-EV129/0.1"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read().decode("utf-8", errors="replace")


def find_source(registry: dict, source_id: str) -> dict:
    for item in registry.get("sources", []):
        if item.get("source_id") == source_id:
            return item
    fail(f"source not found: {source_id}")


def find_local_element(root: etree._Element, complex_type: str, element_name: str) -> etree._Element:
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    nodes = root.xpath(
        f"./xs:complexType[@name='{complex_type}']/xs:sequence/xs:element[@name='{element_name}']",
        namespaces=ns,
    )
    require(len(nodes) == 1, f"expected exactly one {complex_type}/{element_name}, got {len(nodes)}")
    return nodes[0]


def compile_aux_schema(root_name: str, ibis_type: str) -> etree.XMLSchema:
    schema_text = f'''<?xml version="1.0"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified">
  <xs:include schemaLocation="IBIS-IP_common_V1.0.xsd"/>
  <xs:element name="{root_name}" type="{ibis_type}"/>
</xs:schema>
'''
    with tempfile.NamedTemporaryFile("w", suffix=".xsd", dir=".", encoding="utf-8", delete=False) as fh:
        fh.write(schema_text)
        tmp = Path(fh.name)
    try:
        return etree.XMLSchema(etree.parse(str(tmp)))
    finally:
        tmp.unlink(missing_ok=True)


def xml_valid(schema: etree.XMLSchema, xml: str) -> bool:
    return schema.validate(etree.fromstring(xml.encode("utf-8")))


def main() -> int:
    require(PDF.exists(), f"missing fetched PDF: {PDF}")
    require(git_blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory changed")
    require(git_blob(SYSTEM_DOC_XSD) == EXPECTED_SYSTEM_DOC_BLOB, "SystemDocumentation V1.0 XSD changed")
    require(git_blob(SYSTEM_MGMT_XSD) == EXPECTED_SYSTEM_MGMT_BLOB, "SystemManagement V1.0 XSD changed")

    pdf_hash, pdf_size = sha256_file(PDF)
    require(pdf_hash == EXPECTED_PDF_SHA256, f"VDV301-2 V1.0 PDF hash mismatch: {pdf_hash}")
    require(pdf_size == EXPECTED_PDF_SIZE, f"VDV301-2 V1.0 PDF size mismatch: {pdf_size}")

    frozen = load(FROZEN)
    require(frozen.get("entry_count") == 192 and frozen.get("state") == "frozen", "frozen inventory invariant failed")
    for finding_id in FINDINGS:
        require(finding_id in frozen.get("finding_ids", []), f"missing frozen finding {finding_id}")

    source_registry = load(SOURCE_REGISTRY)
    pins = load(PIN_REGISTRY)
    src = find_source(source_registry, "VDV301-2_V1.0_DE")
    require(src.get("vdv_part") == "301-2" and src.get("version") == "1.0", "VDV301-2 source identity changed")
    pin = find_source(pins, "VDV301-2_V1.0_DE")
    require(pin.get("expected_sha256") == EXPECTED_PDF_SHA256, "VDV301-2 pin hash changed")
    require(int(pin.get("expected_size_bytes")) == EXPECTED_PDF_SIZE, "VDV301-2 pin size changed")

    # DR3012-001: visible VDV reference says RFC 2927 for ZeroConf/169.254; RFC authority disagrees.
    p20 = page_text(20)
    require("RFC 2927" in p20 and "169.254" in p20 and "Zero Conf" in p20, "DR3012-001 PDF page 20 anchors missing")
    rfc2927 = fetch_text("https://www.rfc-editor.org/rfc/rfc2927.txt")
    rfc3927 = fetch_text("https://www.rfc-editor.org/rfc/rfc3927.txt")
    require("MIME Directory Profile for LDAP Schema" in rfc2927, "RFC 2927 authority title unexpected")
    require("Dynamic Configuration of IPv4 Link-Local Addresses" in rfc3927, "RFC 3927 authority title unexpected")
    require("169.254/16" in rfc3927 or "169.254.0.0/16" in rfc3927, "RFC 3927 link-local range anchor missing")
    print("OK DR3012-001 visible RFC 2927 citation conflicts with RFC authority for IPv4 link-local addressing")

    # DR3012-002: VDV table says lower Weight is preferred; RFC 2782 says larger weight => higher probability.
    p26 = page_text(26)
    require("RFC 2782" in p26 and "Weight" in p26 and "geringeren Gewicht bevorzugt" in p26, "DR3012-002 PDF page 26 anchors missing")
    rfc2782 = fetch_text("https://www.rfc-editor.org/rfc/rfc2782.txt")
    require("Larger weights SHOULD be given a proportionately higher probability" in rfc2782, "RFC 2782 Weight authority anchor missing")
    print("OK DR3012-002 visible Weight explanation contradicts RFC 2782 selection semantics")

    # DR3012-003: visible PDF spelling/type vs exact official V1.0 XSD, plus executable behaviour.
    p65 = page_text(65)
    require(p65.count("HertbeatIntervall") >= 2 and "IBIS-IP.duration" in p65, "DR3012-003 PDF page 65 anchors missing")
    xsd_tree = etree.parse(str(SYSTEM_DOC_XSD))
    xsd_root = xsd_tree.getroot()
    syscfg = find_local_element(xsd_root, "SystemDocumentationService.SystemConfigurationData", "HeartbeatIntervall")
    store = find_local_element(xsd_root, "SystemDocumentationService.StoreSystemConfigurationRequestStructure", "HeartbeatIntervall")
    require(syscfg.get("type") == "IBIS-IP.double" and syscfg.get("minOccurs") == "0", "unexpected SystemConfigurationData HeartbeatIntervall declaration")
    require(store.get("type") == "IBIS-IP.duration" and store.get("minOccurs") == "0", "unexpected StoreSystemConfiguration HeartbeatIntervall declaration")
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    require(not xsd_root.xpath(".//xs:element[@name='HertbeatIntervall']", namespaces=ns), "unexpected misspelled HertbeatIntervall element exists in exact XSD")
    etree.XMLSchema(xsd_tree)

    double_schema = compile_aux_schema("HeartbeatIntervall", "IBIS-IP.double")
    duration_schema = compile_aux_schema("StoreHeartbeatIntervall", "IBIS-IP.duration")
    require(xml_valid(double_schema, "<HeartbeatIntervall><Value>5.5</Value></HeartbeatIntervall>"), "numeric HeartbeatIntervall should validate as IBIS-IP.double")
    require(not xml_valid(double_schema, "<HeartbeatIntervall><Value>PT5S</Value></HeartbeatIntervall>"), "duration lexical value unexpectedly validates as IBIS-IP.double")
    require(not xml_valid(double_schema, "<HertbeatIntervall><Value>5.5</Value></HertbeatIntervall>"), "misspelled HertbeatIntervall unexpectedly validates as the declared element")
    require(xml_valid(duration_schema, "<StoreHeartbeatIntervall><Value>PT5S</Value></StoreHeartbeatIntervall>"), "duration control sample should validate as IBIS-IP.duration")
    print("OK DR3012-003 executable identifier/type mismatch confirmed: PDF HertbeatIntervall duration; XSD HeartbeatIntervall double in SystemConfigurationData")

    # DR3012-004: DeviceState row points to 9.3 while the actual enum section is 9.4.
    p59 = page_text(59)
    p75 = page_text(75)
    require("DeviceState" in p59 and "vgl. 9.3" in p59, "DR3012-004 page 59 cross-reference anchor missing")
    require("9.4" in p75 and "DeviceStateEnumeration" in p75, "DR3012-004 page 75 target-section anchor missing")
    print("OK DR3012-004 DeviceState cross-reference 9.3 vs visible 9.4 DeviceStateEnumeration confirmed")

    # DR3012-005: operation table uses ServiceStatus, later detailed headings use SystemStatus.
    p67 = page_text(67)
    p69 = page_text(69)
    require("SubscribeServiceStatus" in p67 and "UnsubscribeServiceStatus" in p67 and "GetServiceStatus" in p67, "DR3012-005 page 67 operation inventory anchors missing")
    require("SubscribeSystemStatus" in p69 and "UnsubscribeSystemStatus" in p69, "DR3012-005 page 69 heading anchors missing")
    mgmt_text = SYSTEM_MGMT_XSD.read_text(encoding="utf-8")
    require("SystemManagementService.GetServiceStatusResponse" in mgmt_text and "SystemManagementService.GetDeviceStatusResponse" in mgmt_text, "historical SystemManagement XSD terminology anchors missing")
    print("OK DR3012-005 ServiceStatus operation inventory vs SystemStatus detailed headings confirmed")

    # DR3012-006: stale TimeService document-number reference resolved by historical source context.
    p22 = page_text(22)
    require("VDV 301-2-11" in p22 and "SNTP" in p22, "DR3012-006 page 22 stale reference anchor missing")
    time_src = find_source(source_registry, "TIME_V1.0")
    vls_src = find_source(source_registry, "VLS_V1.0")
    require(time_src.get("vdv_part") == "301-2-10", "TimeService source no longer identified as 301-2-10")
    require(vls_src.get("vdv_part") == "301-2-11", "VideoLiveService source no longer identified as 301-2-11")
    time_report = TIME_REPORT.read_text(encoding="utf-8")
    require("VDV-Mitteilung 3002 | 10/2016" in time_report and "VDV-Schrift 301-2-11 | 05/2017" in time_report, "historical TimeService chronology evidence missing")
    require("historical_context_resolved" in time_report and "wrong/stale VDV 301-2-11 reference" in time_report, "DR3012-006 historical resolution record missing")
    print("OK DR3012-006 historical context resolves 301-2-11 as wrong/stale TimeService reference")

    # DR3012-007: StopService request field description says service to be started.
    p63 = page_text(63)
    require("Operation StopService" in p63 and "gestoppt wird" in p63 and "zu startenden Dienst" in p63, "DR3012-007 page 63 copy/paste anchors missing")
    print("OK DR3012-007 StopService field-description copy/paste error confirmed")

    # Keep the correction trail explicit: old Deep Read contains the imprecise shared-spelling claim.
    deep_read = DEEP_READ.read_text(encoding="utf-8")
    require("The misspelling `HertbeatIntervall` appears in both PDF and XSD" in deep_read, "expected historical DR3012-003 subclaim not found for correction trail")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result = {
        "evidence_id": "EV-129",
        "finding_block": FINDINGS,
        "pdf_source_id": "VDV301-2_V1.0_DE",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "selected_xsd_family": "official VDV-301-1.0 historical V1.0 family",
        "system_documentation_xsd_blob": EXPECTED_SYSTEM_DOC_BLOB,
        "system_management_xsd_blob": EXPECTED_SYSTEM_MGMT_BLOB,
        "external_authorities": ["RFC 2927", "RFC 3927", "RFC 2782"],
        "visual_pages": [20, 22, 26, 59, 63, 65, 67, 69, 75, 80],
        "terminal_revalidation_recommendations": TERMINAL_RECOMMENDATIONS,
        "dr3012_003_correction_required": True,
        "dr3012_003_corrected_claim": "PDF uses HertbeatIntervall and IBIS-IP.duration in both visible rows; exact official V1.0 XSD uses HeartbeatIntervall, with IBIS-IP.double in SystemConfigurationData and IBIS-IP.duration in StoreSystemConfigurationRequestStructure.",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS",
    }
    (OUT_DIR / "ev129_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED: EV-129 VDV301-2 V1.0 DR3012-001..007 revalidation evidence gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
