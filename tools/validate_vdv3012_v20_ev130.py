#!/usr/bin/env python3
"""EV-130 evidence gate for VDV301-2 Base V2.0 DR3012V20-001..008.

Fail-closed revalidation against the exact byte-pinned 02/2018 Base Services PDF,
external RFC primary authorities where delegated, the exact official VDV-301-2.0
XSD family (with historical SystemManagement V1.0), visible-page anchors, and an
executable HeartbeatInterval identifier/type boundary test.
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

PDF = Path("local_sources/vdv_pdfs/VDV301-2_BASE_V2.0.pdf")
SOURCE_REGISTRY = Path("audit_registry/pdf_source_registry_v0.1.json")
PIN_REGISTRY = Path("audit_registry/pdf_source_pins_v0.1.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
SYSTEM_DOC_XSD = Path("IBIS-IP_SystemDocumentationService_V2.0.xsd")
DMS_XSD = Path("IBIS-IP_DeviceManagementService_V2.0.xsd")
SYSTEM_MGMT_XSD = Path("IBIS-IP_SystemManagementService_V1.0.xsd")
COMMON_XSD = Path("IBIS-IP_common_V2.0.xsd")
ENUM_XSD = Path("IBIS-IP_Enumerations_V2.0.xsd")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/VDV301-2_BASE_V2.0.md")
OUT_DIR = Path(os.environ.get("EV130_OUTPUT_DIR", "artifacts/ev130"))

EXPECTED_PDF_SHA256 = "fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37"
EXPECTED_PDF_SIZE = 2374295
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_SYSTEM_DOC_BLOB = "ab959dddbfa2b8ca420af1b079501f94cff38051"
EXPECTED_DMS_BLOB = "74189e0da65563eeb084ec2f3c400e9668d1ee1a"
EXPECTED_SYSTEM_MGMT_BLOB = "2d32630a0f1981e980e6a466e3f6a69136410f24"
EXPECTED_COMMON_BLOB = "8608e3dcd665c197c34da7f6ec6af5a3758da164"
EXPECTED_ENUM_BLOB = "27e3c183b00381d959622d13c10543123af8eef6"
FINDINGS = [f"DR3012V20-{i:03d}" for i in range(1, 9)]
TERMINAL_RECOMMENDATIONS = {
    "DR3012V20-001": "context_verified",
    "DR3012V20-002": "context_verified",
    "DR3012V20-003": "executable_confirmed",
    "DR3012V20-004": "context_verified",
    "DR3012V20-005": "context_verified",
    "DR3012V20-006": "context_verified",
    "DR3012V20-007": "context_verified",
    "DR3012V20-008": "context_verified",
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


def full_text() -> str:
    out = subprocess.check_output(["pdftotext", "-layout", str(PDF), "-"], text=True, errors="replace")
    return normalize(out)


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "VDV301-EV130/0.1"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return normalize(response.read().decode("utf-8", errors="replace"))


def find_source(registry: dict, source_id: str) -> dict:
    for item in registry.get("sources", []):
        if item.get("source_id") == source_id:
            return item
    fail(f"source not found: {source_id}")


def local_element(root: etree._Element, complex_type: str, element_name: str) -> etree._Element:
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    nodes = root.xpath(
        f"./xs:complexType[@name='{complex_type}']/xs:sequence/xs:element[@name='{element_name}']",
        namespaces=ns,
    )
    require(len(nodes) == 1, f"expected one {complex_type}/{element_name}, got {len(nodes)}")
    return nodes[0]


def compile_aux_schema(root_name: str, ibis_type: str) -> etree.XMLSchema:
    schema_text = f'''<?xml version="1.0"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified">
  <xs:include schemaLocation="IBIS-IP_common_V2.0.xsd"/>
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
    require(git_blob(SYSTEM_DOC_XSD) == EXPECTED_SYSTEM_DOC_BLOB, "SystemDocumentation V2.0 XSD changed")
    require(git_blob(DMS_XSD) == EXPECTED_DMS_BLOB, "DeviceManagement V2.0 XSD changed")
    require(git_blob(SYSTEM_MGMT_XSD) == EXPECTED_SYSTEM_MGMT_BLOB, "SystemManagement V1.0 XSD changed")
    require(git_blob(COMMON_XSD) == EXPECTED_COMMON_BLOB, "Common V2.0 XSD changed")
    require(git_blob(ENUM_XSD) == EXPECTED_ENUM_BLOB, "Enumerations V2.0 XSD changed")

    pdf_hash, pdf_size = sha256_file(PDF)
    require(pdf_hash == EXPECTED_PDF_SHA256, f"VDV301-2 Base V2.0 PDF hash mismatch: {pdf_hash}")
    require(pdf_size == EXPECTED_PDF_SIZE, f"VDV301-2 Base V2.0 PDF size mismatch: {pdf_size}")

    frozen = load(FROZEN)
    require(frozen.get("entry_count") == 192 and frozen.get("state") == "frozen", "frozen inventory invariant failed")
    for finding_id in FINDINGS:
        require(finding_id in frozen.get("finding_ids", []), f"missing frozen finding {finding_id}")

    source_registry = load(SOURCE_REGISTRY)
    pins = load(PIN_REGISTRY)
    src = find_source(source_registry, "VDV301-2_BASE_V2.0")
    require(src.get("vdv_part") == "301-2" and src.get("version") == "2.0", "Base V2.0 source identity changed")
    pin = find_source(pins, "VDV301-2_BASE_V2.0")
    require(pin.get("expected_sha256") == EXPECTED_PDF_SHA256, "Base V2.0 pin hash changed")
    require(int(pin.get("expected_size_bytes")) == EXPECTED_PDF_SIZE, "Base V2.0 pin size changed")

    # Compile exact service authorities before semantic checks.
    sysdoc_tree = etree.parse(str(SYSTEM_DOC_XSD))
    dms_tree = etree.parse(str(DMS_XSD))
    etree.XMLSchema(sysdoc_tree)
    etree.XMLSchema(dms_tree)
    etree.XMLSchema(etree.parse(str(SYSTEM_MGMT_XSD)))

    # DR3012V20-001: German side corrected to RFC 3927; English translation remains RFC 2927.
    p21 = page_text(21)
    p110 = page_text(110)
    require("RFC 3927 zur automatischen Adressvergabe" in p21, "DR3012V20-001 German RFC 3927 anchor missing")
    require("RFC 2927 for automatic address allocation" in p21, "DR3012V20-001 English RFC 2927 anchor missing")
    require("169.254.xxx.xxx" in p21, "DR3012V20-001 link-local range anchor missing")
    require("RFC 3927 Dynamic Configuration of IPv4 Link-Local Addresses" in p110, "DR3012V20-001 bibliography authority anchor missing")
    rfc2927 = fetch_text("https://www.rfc-editor.org/rfc/rfc2927.txt")
    rfc3927 = fetch_text("https://www.rfc-editor.org/rfc/rfc3927.txt")
    require("MIME Directory Profile for LDAP Schema" in rfc2927, "RFC 2927 authority title unexpected")
    require("Dynamic Configuration of IPv4 Link-Local Addresses" in rfc3927, "RFC 3927 authority title unexpected")
    require("169.254/16" in rfc3927 or "169.254.0.0/16" in rfc3927, "RFC 3927 range anchor missing")
    print("OK DR3012V20-001 bilingual RFC 3927/RFC 2927 conflict confirmed")

    # DR3012V20-002: both languages retain inverted lower-Weight preference wording.
    p33 = page_text(33)
    p34 = page_text(34)
    require("bei gleichem Gewicht wird der Dienst mit dem geringeren Gewicht bevorzugt" in p33, "DR3012V20-002 German Weight anchor missing")
    require("service with the lower weight is preferred" in p34, "DR3012V20-002 English Weight anchor missing")
    rfc2782 = fetch_text("https://www.rfc-editor.org/rfc/rfc2782.txt")
    require("Larger weights SHOULD be given a proportionately higher probability" in rfc2782, "RFC 2782 Weight authority anchor missing")
    print("OK DR3012V20-002 SRV Weight semantics conflict with RFC 2782 confirmed")

    # DR3012V20-003: history claims HeartbeatInterval correction, tables remain stale; exact XSD is corrected.
    p100 = page_text(100)
    p105 = page_text(105)
    require(p100.count("HertbeatIntervall") >= 2 and p100.count("xs:duration") >= 2, "DR3012V20-003 stale table anchors missing")
    require("Schreibfehler korrigiert nach HeartbeatInterval" in p105 and "typo corrected to HeartbeatInterval" in p105, "DR3012V20-003 version-history anchors missing")
    sysdoc_root = sysdoc_tree.getroot()
    syscfg = local_element(sysdoc_root, "SystemDocumentationService.SystemConfigurationData", "HeartbeatInterval")
    store = local_element(sysdoc_root, "SystemDocumentationService.StoreSystemConfigurationRequestStructure", "HeartbeatInterval")
    require(syscfg.get("type") == "IBIS-IP.duration" and syscfg.get("minOccurs") == "0", "unexpected SystemConfigurationData HeartbeatInterval declaration")
    require(store.get("type") == "IBIS-IP.duration" and store.get("minOccurs") == "0", "unexpected StoreSystemConfiguration HeartbeatInterval declaration")
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    require(not sysdoc_root.xpath(".//xs:element[@name='HertbeatIntervall']", namespaces=ns), "unexpected HertbeatIntervall alias in exact V2.0 XSD")
    require(not sysdoc_root.xpath(".//xs:element[@name='HeartbeatIntervall']", namespaces=ns), "unexpected HeartbeatIntervall alias in exact V2.0 XSD")
    duration_schema = compile_aux_schema("HeartbeatInterval", "IBIS-IP.duration")
    require(xml_valid(duration_schema, "<HeartbeatInterval><Value>PT5S</Value></HeartbeatInterval>"), "HeartbeatInterval PT5S should validate as IBIS-IP.duration")
    require(not xml_valid(duration_schema, "<HeartbeatInterval><Value>5.5</Value></HeartbeatInterval>"), "numeric value unexpectedly validates as IBIS-IP.duration")
    require(not xml_valid(duration_schema, "<HertbeatIntervall><Value>PT5S</Value></HertbeatIntervall>"), "HertbeatIntervall unexpectedly validates as declared identifier")
    require(not xml_valid(duration_schema, "<HeartbeatIntervall><Value>PT5S</Value></HeartbeatIntervall>"), "HeartbeatIntervall unexpectedly validates as declared identifier")
    print("OK DR3012V20-003 stale PDF tables vs corrected exact HeartbeatInterval duration XSD confirmed executable")

    # DR3012V20-004: German narrative service-name typo; surrounding heading and exact XSD are correct.
    p98 = page_text(98)
    require("7.2 Dienst SystemDocumentationService" in p98 and "Der Dienst SystemDocumenationService" in p98, "DR3012V20-004 visible service-name typo anchors missing")
    require(sysdoc_root.xpath("./xs:group[@name='SystemDocumentationServiceGroup']", namespaces=ns), "SystemDocumentationServiceGroup missing in exact XSD")
    print("OK DR3012V20-004 SystemDocumenationService narrative typo confirmed")

    # DR3012V20-005: unresolved SystemManagement chapter range exists in both languages.
    p101 = page_text(101)
    p102 = page_text(102)
    require("vgl. Kapitel bis" in p101, "DR3012V20-005 German unresolved chapter-range anchor missing")
    require("cf capitel bis" in p102, "DR3012V20-005 English unresolved chapter-range anchor missing")
    print("OK DR3012V20-005 unresolved SystemManagement chapter range confirmed")

    # DR3012V20-006: operation inventory includes SubscribeDeviceInformation, but dedicated heading is absent.
    p90 = page_text(90)
    p92 = page_text(92)
    all_text = full_text()
    require("SubscribeDeviceInformation" in p90 and "UnsubscribeDeviceInformation" in p90, "DR3012V20-006 operation inventory anchors missing")
    require("7.1.2 Data Structure of Operation GetDeviceInformation" in p92, "DR3012V20-006 GetDeviceInformation heading missing")
    require("7.1.3 Data Structure of OperationUnsubscribeDeviceInformation" in p92, "DR3012V20-006 UnsubscribeDeviceInformation heading missing")
    require("The data structures described in VDV 301-2-1 are used to set up subscriptions" in p92, "DR3012V20-006 generic subscription context missing")
    require("Data Structure of Operation SubscribeDeviceInformation" not in all_text, "DR3012V20-006 dedicated SubscribeDeviceInformation heading unexpectedly exists")
    print("OK DR3012V20-006 missing SubscribeDeviceInformation subsection heading confirmed")

    # DR3012V20-007: GetDeviceConfiguration prose describes setting; SetDeviceConfiguration is actual setter.
    p93 = page_text(93)
    require("GetDeviceConfiguration operation enables to set the single variable parameter" in p93, "DR3012V20-007 getter-as-setter prose anchor missing")
    require("Data Structure of Operation SetDeviceConfiguration" in p93 and "possible to set the device-ID" in p93, "DR3012V20-007 actual setter context missing")
    dms_root = dms_tree.getroot()
    require(dms_root.xpath("./xs:element[@name='DeviceManagementService.GetDeviceConfigurationResponse']", namespaces=ns), "exact DMS getter response declaration missing")
    require(dms_root.xpath("./xs:element[@name='DeviceManagementService.SetDeviceConfigurationRequest']", namespaces=ns), "exact DMS setter request declaration missing")
    print("OK DR3012V20-007 GetDeviceConfiguration setter-description error confirmed")

    # DR3012V20-008: response table labels the response structures as request structures.
    require("DeviceManagementService.GetDeviceInformatio" in p92 and "Request structure with non configuration able device" in p92, "DR3012V20-008 response-labelled-request anchor missing")
    require("Detailed request structure with the non configurable" in p92, "DR3012V20-008 nested response-labelled-request anchor missing")
    require(dms_root.xpath("./xs:complexType[@name='DeviceManagementService.GetDeviceInformationResponseStructure']", namespaces=ns), "exact DMS GetDeviceInformationResponseStructure missing")
    require(dms_root.xpath("./xs:complexType[@name='DeviceManagementService.GetDeviceInformationResponseDataStructure']", namespaces=ns), "exact DMS GetDeviceInformationResponseDataStructure missing")
    print("OK DR3012V20-008 GetDeviceInformation response labelled as request confirmed")

    deep_read = DEEP_READ.read_text(encoding="utf-8")
    for finding_id in FINDINGS:
        require(finding_id in deep_read, f"historical deep-read record missing {finding_id}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    result = {
        "evidence_id": "EV-130",
        "finding_block": FINDINGS,
        "pdf_source_id": "VDV301-2_BASE_V2.0",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "selected_xsd_family": "official VDV-301-2.0 tag with mixed-version SystemManagement V1.0",
        "system_documentation_xsd_blob": EXPECTED_SYSTEM_DOC_BLOB,
        "device_management_xsd_blob": EXPECTED_DMS_BLOB,
        "system_management_xsd_blob": EXPECTED_SYSTEM_MGMT_BLOB,
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "external_authorities": ["RFC 2927", "RFC 3927", "RFC 2782"],
        "visual_pages": [21, 33, 34, 90, 92, 93, 98, 100, 101, 102, 105, 110],
        "terminal_revalidation_recommendations": TERMINAL_RECOMMENDATIONS,
        "heartbeat_executable_boundary": {
            "declared_identifier": "HeartbeatInterval",
            "declared_type": "IBIS-IP.duration",
            "accepted_sample": "PT5S",
            "rejected_numeric_sample": "5.5",
            "rejected_aliases": ["HertbeatIntervall", "HeartbeatIntervall"],
        },
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS",
    }
    (OUT_DIR / "ev130_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED: EV-130 VDV301-2 Base V2.0 DR3012V20-001..008 revalidation evidence gate")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
