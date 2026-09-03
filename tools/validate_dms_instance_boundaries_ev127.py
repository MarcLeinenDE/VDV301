#!/usr/bin/env python3
"""EV-127 supplemental positive/negative XML instance tests for DMS-003/-004/-006.

This checker exists so the terminal state ``executable_confirmed`` is backed by
actual XML validity boundaries, not only declaration inspection.
"""
from __future__ import annotations

from pathlib import Path
import tempfile
from lxml import etree

NS = {"xs": "http://www.w3.org/2001/XMLSchema"}

DMS = {
    "v20": Path("IBIS-IP_DeviceManagementService_V2.0.xsd"),
    "v21": Path("IBIS-IP_DeviceManagementService_V2.1.xsd"),
    "v22": Path("IBIS-IP_DeviceManagementService_V2.2.xsd"),
    "v24": Path("IBIS-IP_DeviceManagementService_V2.4.xsd"),
}
ENUM = {
    "v20": Path("IBIS-IP_Enumerations_V2.0.xsd"),
    "v21": Path("IBIS-IP_Enumerations_V2.1.xsd"),
    "v22": Path("IBIS-IP_Enumerations_V2.2.xsd"),
    "v24": Path("IBIS-IP_Enumerations_V2.4.xsd"),
}


def require(condition: bool, message: str) -> None:
    if not condition:
        print(f"FAIL {message}")
        raise SystemExit(1)


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
    # Place the wrapper beside the selected XSD so all relative includes resolve
    # exactly through the repository's selected dependency route.
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


def message_xml(message_type: str) -> str:
    return (
        "<ErrorMessage>"
        "<Message-ID>1</Message-ID>"
        "<TimeStamp>2026-09-03T12:00:00Z</TimeStamp>"
        f"<MessageType>{message_type}</MessageType>"
        "<MessageText>e</MessageText>"
        "</ErrorMessage>"
    )


def error_data_xml(count: int, message_type: str) -> str:
    return (
        "<EV127ErrorData>"
        "<TimeStamp>2026-09-03T12:00:00Z</TimeStamp>"
        + message_xml(message_type) * count
        + "</EV127ErrorData>"
    )


def test_dms003() -> None:
    for version in ("v20", "v21", "v22"):
        schema = wrapper_schema(
            DMS[version],
            "EV127ErrorData",
            "DeviceManagementService.GetDeviceErrorMessagesResponseDataStructure",
        )
        msg_type = first_enum(ENUM[version], "MessageTypeEnumeration")
        require(not valid(schema, error_data_xml(9, msg_type)), f"DMS-003 {version}: 9 ErrorMessage unexpectedly valid")
        require(valid(schema, error_data_xml(10, msg_type)), f"DMS-003 {version}: 10 ErrorMessage unexpectedly invalid")
        require(valid(schema, error_data_xml(11, msg_type)), f"DMS-003 {version}: 11 ErrorMessage unexpectedly invalid")
        print(f"INSTANCE_OK DMS-003 {version}: 9=reject 10=accept 11=accept")

    schema24 = wrapper_schema(
        DMS["v24"],
        "EV127ErrorData",
        "DeviceManagementService.GetDeviceErrorMessagesResponseDataStructure",
    )
    msg_type24 = first_enum(ENUM["v24"], "MessageTypeEnumeration")
    require(valid(schema24, error_data_xml(0, msg_type24)), "DMS-003 v24: 0 ErrorMessage unexpectedly invalid")
    require(valid(schema24, error_data_xml(1, msg_type24)), "DMS-003 v24: 1 ErrorMessage unexpectedly invalid")
    print("INSTANCE_OK DMS-003 v24: 0=accept 1=accept")


def install_xml(fields: tuple[str, ...]) -> str:
    values = {
        "UpdateID": "UPD1",
        "UpdateTimestamp": "2026-09-03T12:00:00Z",
        "UpdateURL": "https://example.invalid/update.bin",
    }
    body = "".join(f"<{name}>{values[name]}</{name}>" for name in fields)
    return f"<EV127Install>{body}</EV127Install>"


def test_dms004() -> None:
    required = ("UpdateID", "UpdateTimestamp", "UpdateURL")
    for version in ("v21", "v22"):
        schema = wrapper_schema(
            DMS[version],
            "EV127Install",
            "DeviceManagementService.InstallUpdateRequestStructure",
        )
        require(valid(schema, install_xml(required)), f"DMS-004 {version}: complete required trio invalid")
        for missing in required:
            fields = tuple(name for name in required if name != missing)
            require(not valid(schema, install_xml(fields)), f"DMS-004 {version}: missing {missing} unexpectedly valid")
        print(f"INSTANCE_OK DMS-004 {version}: required trio accepted; each single omission rejected")

    schema24 = wrapper_schema(
        DMS["v24"],
        "EV127Install",
        "DeviceManagementService.InstallUpdateRequestStructure",
    )
    require(valid(schema24, install_xml(tuple())), "DMS-004 v24: empty optional request unexpectedly invalid")
    require(valid(schema24, install_xml(required)), "DMS-004 v24: populated optional request unexpectedly invalid")
    print("INSTANCE_OK DMS-004 v24: empty=accept populated=accept")


def status_xml(version: str, include_impact_priority: bool) -> str:
    body = "<DeviceStatusName>status</DeviceStatusName><DeviceStatusFlag>true</DeviceStatusFlag>"
    if include_impact_priority:
        state = first_enum(ENUM[version], "DeviceStateEnumeration")
        body += f"<DeviceStatusImpact>{state}</DeviceStatusImpact><DeviceStatusPriority>1</DeviceStatusPriority>"
    return f"<EV127Status>{body}</EV127Status>"


def test_dms006() -> None:
    schema22 = wrapper_schema(DMS["v22"], "EV127Status", "DeviceStatusStructure")
    require(not valid(schema22, status_xml("v22", False)), "DMS-006 v22: PDF-visible Name+Flag-only instance unexpectedly valid")
    require(valid(schema22, status_xml("v22", True)), "DMS-006 v22: full four-field status unexpectedly invalid")
    print("INSTANCE_OK DMS-006 v22: PDF-visible two-field shape=reject; XSD-required four-field shape=accept")

    schema24 = wrapper_schema(DMS["v24"], "EV127Status", "DeviceStatusStructure")
    require(valid(schema24, status_xml("v24", False)), "DMS-006 v24: Name+Flag-only instance unexpectedly invalid")
    require(valid(schema24, status_xml("v24", True)), "DMS-006 v24: populated optional fields unexpectedly invalid")
    print("INSTANCE_OK DMS-006 v24: two-field=accept four-field=accept")


def main() -> int:
    for path in (*DMS.values(), *ENUM.values()):
        require(path.is_file(), f"missing selected authority file {path}")
    test_dms003()
    test_dms004()
    test_dms006()
    print("PASSED: EV-127 supplemental DMS positive/negative XML instance boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
