#!/usr/bin/env python3
"""EV-116: official SystemMonitoringService V2.2 executable evidence.

Authority is the exact official VDV-301-2.2 family. This checker does not
modify XSDs and does not revalidate Common PDF findings merely by observing
shared-schema declarations.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
SERVICE = ROOT / "IBIS-IP_SystemMonitoringService_V2.2.xsd"
COMMON = ROOT / "IBIS-IP_common_V2.2.xsd"
ENUMS = ROOT / "IBIS-IP_Enumerations_V2.2.xsd"
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}

EXPECTED_GIT_BLOBS = {
    SERVICE.name: "d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c",
    COMMON.name: "468fee6d177e7185dbcd5d3f90cfb114e29e01ae",
    ENUMS.name: "2a23b512379b18e8f122ac1272cef8229fb86283",
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"OK  {message}")


def validate_xml(schema: etree.XMLSchema, xml: str, expected: bool, label: str) -> None:
    doc = etree.fromstring(xml.encode("utf-8"))
    actual = schema.validate(doc)
    require(actual is expected, f"{label} -> {'valid' if expected else 'invalid'}")
    if not expected:
        print(f"    evidence: {schema.error_log.last_error}")


def main() -> int:
    print("AUTHORITY: official VDV-301-2.2 exact SystemMonitoringService family")

    for path in (SERVICE, COMMON, ENUMS):
        actual = git_blob_sha(path.read_bytes())
        require(actual == EXPECTED_GIT_BLOBS[path.name], f"exact official blob {path.name} = {actual}")

    service_tree = etree.parse(str(SERVICE))
    common_tree = etree.parse(str(COMMON))
    includes = service_tree.xpath("/xs:schema/xs:include/@schemaLocation", namespaces=NS)
    require(includes == [COMMON.name, ENUMS.name], "SMS V2.2 include route is exact Common V2.2 + Enumerations V2.2")

    schema = etree.XMLSchema(service_tree)
    print(f"OK  compiled official {SERVICE.name}")

    group_names = service_tree.xpath(
        "//xs:group[@name='SystemMonitoringServiceGroup']/xs:sequence/xs:element/@name",
        namespaces=NS,
    )
    require(
        group_names == [
            "SystemMonitoringService.GetDeviceStatusResponse",
            "SystemMonitoringService.GetServiceStatusResponse",
        ],
        "service-local operation group contains the two exact Get response elements",
    )

    common_types = set(common_tree.xpath("//xs:complexType/@name", namespaces=NS))
    for type_name in (
        "SubscribeRequestStructure",
        "SubscribeResponseStructure",
        "UnsubscribeRequestStructure",
        "UnsubscribeResponseStructure",
    ):
        require(type_name in common_types, f"generic Common subscription type exists: {type_name}")

    valid_service = (
        "<SystemMonitoringService.GetServiceStatusResponse>"
        "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>"
        "</SystemMonitoringService.GetServiceStatusResponse>"
    )
    invalid_system = (
        "<SystemMonitoringService.GetSystemStatusResponse>"
        "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>"
        "</SystemMonitoringService.GetSystemStatusResponse>"
    )
    valid_device = (
        "<SystemMonitoringService.GetDeviceStatusResponse>"
        "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>"
        "</SystemMonitoringService.GetDeviceStatusResponse>"
    )
    validate_xml(schema, valid_service, True, "exact GetServiceStatusResponse error branch")
    validate_xml(schema, invalid_system, False, "invented GetSystemStatusResponse root")
    validate_xml(schema, valid_device, True, "exact GetDeviceStatusResponse error branch")

    device_min = service_tree.xpath(
        "string(//xs:complexType[@name='SystemMonitoringService.GetDeviceStatusResponseDataStructure']"
        "/xs:sequence/xs:element[@name='DeviceSpecificationWithStateList']/@minOccurs)", namespaces=NS
    ) or "1"
    service_min = service_tree.xpath(
        "string(//xs:complexType[@name='SystemMonitoringService.GetServiceStatusResponseDataStructure']"
        "/xs:sequence/xs:element[@name='ServiceIdentificationWithStateList']/@minOccurs)", namespaces=NS
    ) or "1"
    require(device_min == "1" and service_min == "1", "SMS response-data list wrappers are required 1:1")

    device_item_min = common_tree.xpath(
        "string(//xs:complexType[@name='DeviceSpecificationWithStateListStructure']"
        "/xs:sequence/xs:element[@name='DeviceSpecificationWithState']/@minOccurs)", namespaces=NS
    ) or "1"
    service_item_min = common_tree.xpath(
        "string(//xs:complexType[@name='ServiceIdentificationWithStateListStructure']"
        "/xs:sequence/xs:element[@name='ServiceIdentificationWithState']/@minOccurs)", namespaces=NS
    ) or "1"
    require(device_item_min == "0" and service_item_min == "0", "shared Common list declarations are observed as 0:* for routing context")
    print("NOTE: this Common declaration observation does not by itself revalidate CE-012/CE-018 or any Common PDF interpretation")

    print("PASSED: EV-116 official SMS V2.2 compile, naming boundary and generic-subscription structure evidence confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
