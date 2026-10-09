#!/usr/bin/env python3
"""EV-127 supplemental positive/negative XML instance tests for DMS-003/-004/-006.

This checker exists so the terminal state ``executable_confirmed`` is backed by
actual XML validity boundaries, not only declaration inspection.  IBIS-IP.*
base types are represented using their real ``<Value>`` wrapper shape.
"""
from __future__ import annotations

from pathlib import Path
import tempfile
from lxml import etree

NS = {"xs": "http://www.w3.org/2001/XMLSchema"}

DMS = {
    "v10": Path("IBIS-IP_DeviceManagementService_V1.0.xsd"),
    "v20": Path("IBIS-IP_DeviceManagementService_V2.0.xsd"),
    "v21": Path("IBIS-IP_DeviceManagementService_V2.1.xsd"),
    "v22": Path("IBIS-IP_DeviceManagementService_V2.2.xsd"),
    "v23": Path("IBIS-IP_DeviceManagementService_V2.3.xsd"),
    "v24": Path("IBIS-IP_DeviceManagementService_V2.4.xsd"),
}
ENUM = {
    "v10": Path("IBIS-IP_Enumerations_V1.0.xsd"),
    "v20": Path("IBIS-IP_Enumerations_V2.0.xsd"),
    "v21": Path("IBIS-IP_Enumerations_V2.1.xsd"),
    "v22": Path("IBIS-IP_Enumerations_V2.2.xsd"),
    "v23": Path("IBIS-IP_Enumerations_V2.2.xsd"),
    "v24": Path("IBIS-IP_Enumerations_V2.4.xsd"),
}


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def first_enum(path: Path, type_name: str) -> str:
    root = etree.parse(str(path)).getroot()
    vals = root.xpath(
        f"./xs:simpleType[@name='{type_name}']//xs:enumeration/@value",
        namespaces=NS,
    )
    require(bool(vals), f"{path}: no values for {type_name}")
    return str(vals[0])


def wrapper_schema(include_path: Path, element_name: str, type_name: str) -> etree.XMLSchema:
    xml = f'''<?xml version="1.0"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified">
  <xs:include schemaLocation="{include_path.name}"/>
  <xs:element name="{element_name}" type="{type_name}"/>
</xs:schema>'''
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".xsd", prefix="ev127-wrapper-", dir=".", delete=False, encoding="utf-8"
    ) as handle:
        handle.write(xml)
        wrapper = Path(handle.name)
    try:
        return etree.XMLSchema(etree.parse(str(wrapper)))
    finally:
        wrapper.unlink(missing_ok=True)


def valid(schema: etree.XMLSchema, xml: str) -> bool:
    return schema.validate(etree.fromstring(xml.encode("utf-8")))


def require_valid(schema: etree.XMLSchema, xml: str, label: str) -> None:
    if valid(schema, xml):
        return
    print(f"VALIDATION_DIAGNOSTIC {label}")
    for entry in schema.error_log:
        print(f"  line={entry.line} domain={entry.domain_name} type={entry.type_name}: {entry.message}")
    fail(f"{label}: expected valid instance was rejected")


def require_invalid(schema: etree.XMLSchema, xml: str, label: str) -> None:
    if not valid(schema, xml):
        return
    fail(f"{label}: expected invalid instance was accepted")


def ibis(name: str, value: str) -> str:
    """Render the repository's IBIS-IP.* wrapper type shape."""
    return f"<{name}><Value>{value}</Value></{name}>"


def message_xml(message_type: str) -> str:
    return (
        "<ErrorMessage>"
        + ibis("Message-ID", "1")
        + ibis("TimeStamp", "2026-09-03T12:00:00Z")
        + f"<MessageType>{message_type}</MessageType>"
        + ibis("MessageText", "e")
        + "</ErrorMessage>"
    )


def error_data_xml(count: int, message_type: str) -> str:
    return (
        "<EV127ErrorData>"
        + ibis("TimeStamp", "2026-09-03T12:00:00Z")
        + message_xml(message_type) * count
        + "</EV127ErrorData>"
    )


def test_dms003() -> None:
    for version in ("v10", "v20", "v21", "v22"):
        schema = wrapper_schema(
            DMS[version],
            "EV127ErrorData",
            "DeviceManagementService.GetDeviceErrorMessagesResponseDataStructure",
        )
        msg_type = first_enum(ENUM[version], "MessageTypeEnumeration")
        require_invalid(schema, error_data_xml(9, msg_type), f"DMS-003 {version} 9 ErrorMessage")
        require_valid(schema, error_data_xml(10, msg_type), f"DMS-003 {version} 10 ErrorMessage")
        require_valid(schema, error_data_xml(11, msg_type), f"DMS-003 {version} 11 ErrorMessage")
        print(f"INSTANCE_OK DMS-003 {version}: 9=reject 10=accept 11=accept")

    for version in ("v23", "v24"):
        schema = wrapper_schema(
            DMS[version],
            "EV127ErrorData",
            "DeviceManagementService.GetDeviceErrorMessagesResponseDataStructure",
        )
        msg_type = first_enum(ENUM[version], "MessageTypeEnumeration")
        require_valid(schema, error_data_xml(0, msg_type), f"DMS-003 {version} 0 ErrorMessage")
        require_valid(schema, error_data_xml(1, msg_type), f"DMS-003 {version} 1 ErrorMessage")
        print(f"INSTANCE_OK DMS-003 {version}: 0=accept 1=accept")


def install_xml(fields: tuple[str, ...]) -> str:
    values = {
        "UpdateID": "UPD1",
        "UpdateTimestamp": "2026-09-03T12:00:00Z",
        "UpdateURL": "https://example.invalid/update.bin",
    }
    body = "".join(ibis(name, values[name]) for name in fields)
    return f"<EV127Install>{body}</EV127Install>"


def test_dms004() -> None:
    required = ("UpdateID", "UpdateTimestamp", "UpdateURL")
    for version in ("v21", "v22", "v23"):
        schema = wrapper_schema(
            DMS[version],
            "EV127Install",
            "DeviceManagementService.InstallUpdateRequestStructure",
        )
        require_valid(schema, install_xml(required), f"DMS-004 {version} complete required trio")
        for missing in required:
            fields = tuple(name for name in required if name != missing)
            require_invalid(schema, install_xml(fields), f"DMS-004 {version} missing {missing}")
        print(f"INSTANCE_OK DMS-004 {version}: required trio accepted; each single omission rejected")

    schema24 = wrapper_schema(
        DMS["v24"],
        "EV127Install",
        "DeviceManagementService.InstallUpdateRequestStructure",
    )
    require_valid(schema24, install_xml(tuple()), "DMS-004 v24 empty optional request")
    require_valid(schema24, install_xml(required), "DMS-004 v24 populated optional request")
    print("INSTANCE_OK DMS-004 v24: empty=accept populated=accept")


def status_xml(version: str, include_impact_priority: bool) -> str:
    return status_xml_fields(version, include_impact_priority, include_impact_priority)


def status_xml_fields(version: str, include_impact: bool, include_priority: bool) -> str:
    body = ibis("DeviceStatusName", "status") + ibis("DeviceStatusFlag", "true")
    if include_impact:
        state = first_enum(ENUM[version], "DeviceStateEnumeration")
        body += f"<DeviceStatusImpact>{state}</DeviceStatusImpact>"
    if include_priority:
        body += ibis("DeviceStatusPriority", "1")
    return f"<EV127Status>{body}</EV127Status>"


def test_dms006() -> None:
    schema21 = wrapper_schema(DMS["v21"], "EV127Status", "DeviceStatusStructure")
    require_valid(schema21, status_xml("v21", False), "DMS-006 v21 PDF-visible two-field predecessor")
    require_invalid(schema21, status_xml("v21", True), "DMS-006 v21 unexpected future Impact and Priority fields")
    print("INSTANCE_OK DMS-006 v21: two-field predecessor=accept; future four-field form=reject")

    for version in ("v22", "v23"):
        schema = wrapper_schema(DMS[version], "EV127Status", "DeviceStatusStructure")
        require_invalid(schema, status_xml(version, False), f"DMS-006 {version} Name+Flag-only")
        require_valid(schema, status_xml(version, True), f"DMS-006 {version} full required four fields")
        require_invalid(schema, status_xml_fields(version, True, False), f"DMS-006 {version} missing Priority")
        require_invalid(schema, status_xml_fields(version, False, True), f"DMS-006 {version} missing Impact")
        print(f"INSTANCE_OK DMS-006 {version}: two-field=reject four-field=accept each missing Impact/Priority=reject")

    schema24 = wrapper_schema(DMS["v24"], "EV127Status", "DeviceStatusStructure")
    require_valid(schema24, status_xml("v24", False), "DMS-006 v24 Name+Flag-only")
    require_valid(schema24, status_xml("v24", True), "DMS-006 v24 populated optional fields")
    require_valid(schema24, status_xml_fields("v24", True, False), "DMS-006 v24 optional Priority omitted")
    require_valid(schema24, status_xml_fields("v24", False, True), "DMS-006 v24 optional Impact omitted")
    print("INSTANCE_OK DMS-006 v24: both optional 0/1; two-field, four-field, either single optional=accept")


def test_dms005() -> None:
    """Selected-XSD proof: do not accept a PDF-only non-Get response choice name.

    This is a positive/negative XML test of the *actual response choice* in each
    selected service XSD (official V2.1/V2.2, integration V2.3, candidate V2.4).
    The V2.3 XSD check does not assert existence of an official V2.3 PDF.
    """
    root = "EV127DMS005"
    correct = "DeviceManagementService.GetDeviceStatusInformationResponseData"
    pdf_only = "DeviceManagementService.DeviceStatusInformationResponseData"
    for version in ("v21", "v22", "v23", "v24"):
        schema = wrapper_schema(
            DMS[version], root,
            "DeviceManagementService.GetDeviceStatusInformationResponseStructure",
        )
        device_state = first_enum(ENUM[version], "DeviceStateEnumeration")
        body = (
            ibis("TimeStamp", "2026-10-09T08:00:00Z")
            + f"<DeviceStatusInformation><DeviceState>{device_state}</DeviceState></DeviceStatusInformation>"
        )
        good = f"<{root}><{correct}>{body}</{correct}></{root}>"
        wrong = f"<{root}><{pdf_only}>{body}</{pdf_only}></{root}>"
        require_valid(schema, good, f"DMS-005 {version} exact Get-prefixed response data")
        require_invalid(schema, wrong, f"DMS-005 {version} PDF-only non-Get alias")
        print(f"INSTANCE_OK DMS-005 {version}: correct Get=accept PDF-only non-Get=reject")


def test_dms007() -> None:
    """Guard version-exact operation identifiers; PDF prose is not an alias."""
    for version in ("v21", "v22", "v23", "v24"):
        schema_root = etree.parse(str(DMS[version])).getroot()
        element_names = set(schema_root.xpath(".//xs:element/@name", namespaces=NS))
        for operation in ("GetUpdateHistory", "RetrieveUpdateState"):
            for suffix in ("Request", "Response"):
                expected = f"DeviceManagementService.{operation}{suffix}"
                require(expected in element_names, f"DMS-007 {version} declares {expected}")
        require(
            not any("GetUpdateStates" in name for name in element_names),
            f"DMS-007 {version} does not declare fake GetUpdateStates alias",
        )
        update_timestamp_docs = schema_root.xpath(
            "./xs:complexType[@name='DeviceManagementService.InstallUpdateRequestStructure']"
            "/xs:sequence/xs:element[@name='UpdateTimestamp']"
            "/xs:annotation/xs:documentation/text()",
            namespaces=NS,
        )
        require(
            len(update_timestamp_docs) == 1
            and "GetUpdateHistory" in update_timestamp_docs[0]
            and "RetrieveUpdateState" in update_timestamp_docs[0]
            and "GetUpdateStates" not in update_timestamp_docs[0],
            f"DMS-007 {version} exact selected XSD annotation points to actual operations",
        )
        print(f"INSTANCE_OK DMS-007 {version}: correct operations present; GetUpdateStates alias absent")


def main() -> int:
    for path in (*DMS.values(), *ENUM.values()):
        require(path.is_file(), f"missing selected authority file {path}")
    test_dms003()
    test_dms004()
    test_dms006()
    test_dms005()
    test_dms007()
    print("PASSED: EV-127 supplemental DMS positive/negative XML instance boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
