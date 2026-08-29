#!/usr/bin/env python3
"""EV-117: exact-authority executable evidence for COMMON V1.0 Deep Read.

This checker is deliberately pinned to the historical official V1.0 Common/
Enumerations blobs imported by VDVde/VDV301 in commit
604a5a5c7608977e483072f7e450d7381cc182e4.

It does not treat the 05/2017 PDF's internal document revision "Version 1.1"
as a different executable XSD authority. Instead it confirms the selected
V1.0 XSD behaviour that matters for the Deep Read reconciliation.
"""

from __future__ import annotations

import hashlib
import sys
import tempfile
from pathlib import Path
from typing import Iterable

try:
    from lxml import etree
except ImportError:
    print("ERROR: lxml is required. Install with: python -m pip install lxml", file=sys.stderr)
    raise


XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}

COMMON_NAME = "IBIS-IP_common_V1.0.xsd"
ENUM_NAME = "IBIS-IP_Enumerations_V1.0.xsd"
EXPECTED_COMMON_BLOB = "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c"
EXPECTED_ENUM_BLOB = "a9bea5bc73003ed91ded8519db06c32c4067831d"


class EvidenceError(RuntimeError):
    pass


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def fail(message: str) -> None:
    raise EvidenceError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)
    print(f"OK  {message}")


def occurs(element: etree._Element, attr: str) -> str:
    default = "1"
    return element.get(attr, default)


def complex_type(root: etree._Element, name: str) -> etree._Element:
    node = root.find(f"xs:complexType[@name='{name}']", NS)
    if node is None:
        fail(f"missing complexType {name}")
    return node


def type_element(root: etree._Element, type_name: str, element_name: str) -> etree._Element | None:
    node = complex_type(root, type_name)
    return node.find(f".//xs:element[@name='{element_name}']", NS)


def require_element(
    root: etree._Element,
    type_name: str,
    element_name: str,
    *,
    type_value: str | None = None,
    min_occurs: str | None = None,
    max_occurs: str | None = None,
) -> etree._Element:
    node = type_element(root, type_name, element_name)
    require(node is not None, f"{type_name}.{element_name} exists")
    assert node is not None
    if type_value is not None:
        require(node.get("type") == type_value, f"{type_name}.{element_name} type={type_value}")
    if min_occurs is not None:
        require(occurs(node, "minOccurs") == min_occurs, f"{type_name}.{element_name} minOccurs={min_occurs}")
    if max_occurs is not None:
        require(occurs(node, "maxOccurs") == max_occurs, f"{type_name}.{element_name} maxOccurs={max_occurs}")
    return node


def require_absent_element(root: etree._Element, type_name: str, element_name: str) -> None:
    require(type_element(root, type_name, element_name) is None, f"{type_name}.{element_name} is absent")


def enum_values(root: etree._Element, name: str) -> list[str]:
    node = root.find(f"xs:simpleType[@name='{name}']", NS)
    if node is None:
        fail(f"missing simpleType {name}")
    return [x.get("value", "") for x in node.findall(".//xs:enumeration", NS)]


def validate(schema: etree.XMLSchema, xml: str) -> tuple[bool, str]:
    try:
        doc = etree.fromstring(xml.encode("utf-8"))
    except etree.XMLSyntaxError as exc:
        return False, f"XML parse error: {exc}"
    ok = bool(schema.validate(doc))
    if ok:
        return True, "OK"
    last = schema.error_log.last_error
    return False, str(last) if last is not None else "validation failed"


def expect_instance(schema: etree.XMLSchema, label: str, xml: str, expected: bool) -> None:
    ok, detail = validate(schema, xml)
    if ok != expected:
        state = "VALID" if ok else "INVALID"
        wanted = "VALID" if expected else "INVALID"
        fail(f"{label}: got {state}, expected {wanted}: {detail}")
    print(f"OK  {label}: {'VALID' if ok else 'INVALID'} as expected")


def harness() -> str:
    enum_elements = {
        "TestDoorClass": "DoorCountingObjectClassEnumeration",
        "TestGNSSType": "GNSSTypeEnumeration",
        "TestTicketValidation": "TicketValidationEnumeration",
        "TestVehicleMode": "VehicleModeEnumeration",
        "TestServiceName": "ServiceNameEnumeration",
        "TestServiceState": "ServiceStateEnumeration",
    }
    complex_elements = {
        "TestAdditionalAnnouncement": "AdditionalAnnouncementStructure",
        "TestDataAcceptedResponse": "DataAcceptedResponseStructure",
        "TestDeviceSpecificationWithStateList": "DeviceSpecificationWithStateListStructure",
        "TestServiceIdentificationWithStateList": "ServiceIdentificationWithStateListStructure",
        "TestServiceSpecificationWithStateList": "ServiceSpecificationWithStateListStructure",
        "TestServiceIdentification": "ServiceIdentificationStructure",
        "TestBeaconPoint": "BeaconPointStructure",
        "TestTSPPoint": "TSPPointStructure",
    }
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<xs:schema xmlns:xs="{XS}" elementFormDefault="qualified" attributeFormDefault="unqualified">',
        f'  <xs:include schemaLocation="{COMMON_NAME}"/>',
    ]
    for elem, typ in {**enum_elements, **complex_elements}.items():
        lines.append(f'  <xs:element name="{elem}" type="{typ}"/>')
    lines.append("</xs:schema>")
    return "\n".join(lines) + "\n"


def check_static_common(common_root: etree._Element, enum_root: etree._Element) -> None:
    include = common_root.find("xs:include", NS)
    require(include is not None and include.get("schemaLocation") == ENUM_NAME, "Common V1.0 includes Enumerations V1.0 exactly")

    # FR-COM10-001: explicit 1.1 document changes are absent from exact 2014 V1.0 XSD.
    require_element(common_root, "ConnectionStructure", "DisplayContent", min_occurs="1", max_occurs="1")
    require_element(common_root, "ConnectionStructure", "ExpectedDepatureTime", type_value="IBIS-IP.dateTime", min_occurs="0", max_occurs="1")
    require_absent_element(common_root, "ConnectionStructure", "ExpectedDepartureTime")
    require_absent_element(common_root, "ConnectionStructure", "ScheduledDepartureTime")
    require_element(common_root, "TripInformationStructure", "AdditionalTextMessage", type_value="IBIS-IP.string", min_occurs="0", max_occurs="1")
    require_absent_element(common_root, "TripInformationStructure", "RouteDirection")
    require(enum_root.find("xs:simpleType[@name='RouteDirectionEnumeration']", NS) is None, "Enumerations V1.0 has no RouteDirectionEnumeration")

    # FR-COM10-002 / FR-COM10-003: compositor facts.
    add = complex_type(common_root, "AdditionalAnnouncementStructure")
    add_choice = add.find(".//xs:choice", NS)
    require(add_choice is not None, "AdditionalAnnouncementStructure contains xs:choice")
    assert add_choice is not None
    require(occurs(add_choice, "minOccurs") == "0", "AdditionalAnnouncement xs:choice minOccurs=0")
    require([n.get("name") for n in add_choice.findall("xs:element", NS)] == ["ImmediateInformation", "PeriodicalInformation", "SpecificPoint"], "AdditionalAnnouncement exact XSD choice names confirmed")

    dar = complex_type(common_root, "DataAcceptedResponseStructure")
    dar_choice = dar.find(".//xs:choice", NS)
    require(dar_choice is not None, "DataAcceptedResponseStructure contains xs:choice")
    assert dar_choice is not None
    require([n.get("name") for n in dar_choice.findall("xs:element", NS)] == ["DataAcceptedResponseData", "OperationErrorMessage"], "DataAcceptedResponse exact XSD choice branches confirmed")

    # FR-COM10-004: selected case/spelling-sensitive XML names.
    require_element(common_root, "BeaconPointStructure", "Desciption")
    require_absent_element(common_root, "BeaconPointStructure", "Description")
    require_element(common_root, "TSPPointStructure", "Desciption")
    require_absent_element(common_root, "TSPPointStructure", "Description")
    require_element(common_root, "SubscribeRequestStructure", "ReplyPath")
    require_absent_element(common_root, "SubscribeRequestStructure", "Reply-Path")
    require_element(common_root, "UnsubscribeRequestStructure", "ReplyPath")
    require_absent_element(common_root, "UnsubscribeRequestStructure", "Reply-Path")
    require_element(common_root, "FareZoneInformationStructure", "FareZoneID")
    require_element(common_root, "FareZoneInformationStructure", "FareZoneType")
    require_element(common_root, "FareZoneInformationStructure", "FareZoneLongName")
    require_element(common_root, "FareZoneInformationStructure", "FareZoneShortName")
    require_absent_element(common_root, "FareZoneInformationStructure", "FarezoneID")
    require_element(common_root, "GlobalCardStatus", "GlobalCardStausID")
    require_absent_element(common_root, "GlobalCardStatus", "GlobalCardStatusID")
    require_element(common_root, "ZoneType", "FareZoneTypeName")
    require_absent_element(common_root, "ZoneType", "FarezoneTypeName")
    require_element(common_root, "LogMessageStructure", "Message", type_value="MessageStructure")
    require_absent_element(common_root, "LogMessageStructure", "MessageBody")

    # FR-COM10-005: cardinality and named-type boundary.
    require_element(common_root, "DeviceSpecificationWithStateListStructure", "DeviceSpecificationWithState", min_occurs="0", max_occurs="unbounded")
    require_element(common_root, "ServiceIdentificationWithStateListStructure", "ServiceIdentificationWithState", min_occurs="0", max_occurs="unbounded")
    require_element(common_root, "ServiceSpecificationWithStateListStructure", "ServiceSpecificationWithState", min_occurs="0", max_occurs="unbounded")
    require_element(common_root, "JourneyStopInformationStructure", "Announcement", min_occurs="0", max_occurs="1")
    require_element(common_root, "JourneyStopInformationStructure", "FareZone", min_occurs="0", max_occurs="1")
    require(common_root.find("xs:complexType[@name='DataVersionListStructure']", NS) is None, "V1.0 has no named DataVersionListStructure")
    devinfo = complex_type(common_root, "DeviceInformationStructure")
    data_version = devinfo.find(".//xs:element[@name='DataVersionList']/xs:complexType/xs:sequence/xs:element[@name='DataVersion']", NS)
    require(data_version is not None, "DeviceInformation anonymous DataVersionList/DataVersion exists")
    assert data_version is not None
    require(occurs(data_version, "minOccurs") == "0" and occurs(data_version, "maxOccurs") == "unbounded", "anonymous DataVersionList permits DataVersion 0:*")

    # FR-COM10-006: ServiceIdentification element/type substitutions.
    require_element(common_root, "ServiceIdentificationStructure", "Service", type_value="ServiceSpecificationStructure")
    require_absent_element(common_root, "ServiceIdentificationStructure", "ServiceName")
    require_element(common_root, "ServiceIdentificationWithStateListStructure", "ServiceIdentificationWithState", type_value="ServiceIdentificationWithStateStructure", min_occurs="0", max_occurs="unbounded")

    # FR-COM10-007: ShortTripStop list/member model.
    require_element(common_root, "ShortTripStopListStructure", "ShortTripStop", type_value="ShortTripStopStructure", min_occurs="1", max_occurs="unbounded")
    require_absent_element(common_root, "ShortTripStopListStructure", "ShortTripStopList")
    require_element(common_root, "ShortTripStopStructure", "JourneyStopInformation", type_value="JourneyStopInformationStructure")
    require_element(common_root, "ShortTripStopStructure", "FareZoneInformation", type_value="FareZoneInformationStructure")
    require_element(common_root, "StopPointTariffInformationStructure", "JourneyStopInformation", type_value="JourneyStopInformationStructure")
    require_element(common_root, "StopPointTariffInformationStructure", "FareZoneInformation", type_value="FareZoneInformationStructure")

    # FR-COM10-008: exact historical enum inventory/lexemes.
    expected_pairs: Iterable[tuple[str, str, str]] = [
        ("DoorCountingObjectClassEnumeration", "WheelChair", "Wheelchair"),
        ("DoorCountingObjectClassEnumeration", "Other", "Others"),
        ("GNSSTypeEnumeration", "other", "Other"),
        ("TicketValidationEnumeration", "valid", "Valid"),
        ("VehicleModeEnumeration", "air", "Air"),
    ]
    for type_name, present, absent in expected_pairs:
        values = enum_values(enum_root, type_name)
        require(present in values, f"{type_name} contains exact XSD value {present}")
        require(absent not in values, f"{type_name} does not contain PDF-side value {absent}")
    require("PassengerCountingService" not in enum_values(enum_root, "ServiceNameEnumeration"), "ServiceNameEnumeration V1.0 lacks PassengerCountingService")
    require("starting" not in enum_values(enum_root, "ServiceStateEnumeration"), "ServiceStateEnumeration V1.0 lacks starting")


def check_executable(schema: etree.XMLSchema) -> None:
    # xs:choice behaviour that is materially different from the visible PDF tables.
    expect_instance(
        schema,
        "AdditionalAnnouncement with omitted choice",
        "<TestAdditionalAnnouncement><AnnouncementRef><Value>ann1</Value></AnnouncementRef></TestAdditionalAnnouncement>",
        True,
    )
    expect_instance(
        schema,
        "AdditionalAnnouncement with XSD SpecificPoint branch",
        "<TestAdditionalAnnouncement><AnnouncementRef><Value>ann1</Value></AnnouncementRef><SpecificPoint><PointRef><Value>p1</Value></PointRef><DistanceToPreviousPoint><Value>1.0</Value></DistanceToPreviousPoint></SpecificPoint></TestAdditionalAnnouncement>",
        True,
    )
    expect_instance(
        schema,
        "AdditionalAnnouncement with PDF-only InformationAtSpecificPoint name",
        "<TestAdditionalAnnouncement><AnnouncementRef><Value>ann1</Value></AnnouncementRef><InformationAtSpecificPoint><PointRef><Value>p1</Value></PointRef><DistanceToPreviousPoint><Value>1.0</Value></DistanceToPreviousPoint></InformationAtSpecificPoint></TestAdditionalAnnouncement>",
        False,
    )

    data_branch = "<DataAcceptedResponseData><TimeStamp><Value>2026-01-01T00:00:00Z</Value></TimeStamp><DataAccepted><Value>true</Value></DataAccepted></DataAcceptedResponseData>"
    error_branch = "<OperationErrorMessage><Value>ev117</Value></OperationErrorMessage>"
    expect_instance(schema, "DataAcceptedResponse data branch only", f"<TestDataAcceptedResponse>{data_branch}</TestDataAcceptedResponse>", True)
    expect_instance(schema, "DataAcceptedResponse error branch only", f"<TestDataAcceptedResponse>{error_branch}</TestDataAcceptedResponse>", True)
    expect_instance(schema, "DataAcceptedResponse both branches", f"<TestDataAcceptedResponse>{data_branch}{error_branch}</TestDataAcceptedResponse>", False)

    # Empty list behaviour: XSD permits zero items even where checked PDF tables say 1:*.
    for root_name in (
        "TestDeviceSpecificationWithStateList",
        "TestServiceIdentificationWithStateList",
        "TestServiceSpecificationWithStateList",
    ):
        expect_instance(schema, f"{root_name} empty", f"<{root_name}/>", True)

    # Case-sensitive spellings / element substitutions.
    expect_instance(schema, "BeaconPoint XSD Desciption", "<TestBeaconPoint><BeaconCode><Value>b1</Value></BeaconCode><Desciption><Value>text</Value></Desciption></TestBeaconPoint>", True)
    expect_instance(schema, "BeaconPoint PDF Description alias", "<TestBeaconPoint><BeaconCode><Value>b1</Value></BeaconCode><Description><Value>text</Value></Description></TestBeaconPoint>", False)
    expect_instance(schema, "TSPPoint XSD Desciption", "<TestTSPPoint><TSPCode><Value>t1</Value></TSPCode><Desciption><Value>text</Value></Desciption></TestTSPPoint>", True)
    expect_instance(schema, "TSPPoint PDF Description alias", "<TestTSPPoint><TSPCode><Value>t1</Value></TSPCode><Description><Value>text</Value></Description></TestTSPPoint>", False)

    service = "<Service><ServiceName>TimeService</ServiceName><IBIS-IP-Version><Value>1.0</Value></IBIS-IP-Version></Service>"
    bad_service = "<ServiceName><ServiceName>TimeService</ServiceName><IBIS-IP-Version><Value>1.0</Value></IBIS-IP-Version></ServiceName>"
    device = "<Device><DeviceClass>OnBoardUnit</DeviceClass><DeviceID><Value>ev117-device</Value></DeviceID></Device>"
    expect_instance(schema, "ServiceIdentification XSD outer Service", f"<TestServiceIdentification>{service}{device}</TestServiceIdentification>", True)
    expect_instance(schema, "ServiceIdentification PDF outer ServiceName", f"<TestServiceIdentification>{bad_service}{device}</TestServiceIdentification>", False)

    # Exact enumeration lexemes are executable and case-sensitive.
    probes = [
        ("TestDoorClass", "WheelChair", True),
        ("TestDoorClass", "Wheelchair", False),
        ("TestDoorClass", "Other", True),
        ("TestDoorClass", "Others", False),
        ("TestGNSSType", "other", True),
        ("TestGNSSType", "Other", False),
        ("TestTicketValidation", "valid", True),
        ("TestTicketValidation", "Valid", False),
        ("TestVehicleMode", "air", True),
        ("TestVehicleMode", "Air", False),
        ("TestServiceName", "TimeService", True),
        ("TestServiceName", "PassengerCountingService", False),
        ("TestServiceState", "running", True),
        ("TestServiceState", "starting", False),
    ]
    for root_name, value, expected in probes:
        expect_instance(schema, f"{root_name}={value}", f"<{root_name}>{value}</{root_name}>", expected)


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    common_path = repo / COMMON_NAME
    enum_path = repo / ENUM_NAME

    try:
        common_bytes = common_path.read_bytes()
        enum_bytes = enum_path.read_bytes()
        require(git_blob_sha(common_bytes) == EXPECTED_COMMON_BLOB, f"Common V1.0 exact official blob {EXPECTED_COMMON_BLOB}")
        require(git_blob_sha(enum_bytes) == EXPECTED_ENUM_BLOB, f"Enumerations V1.0 exact official blob {EXPECTED_ENUM_BLOB}")

        common_root = etree.fromstring(common_bytes)
        enum_root = etree.fromstring(enum_bytes)
        check_static_common(common_root, enum_root)

        with tempfile.TemporaryDirectory(prefix="vdv301_ev117_") as tmp:
            tmpdir = Path(tmp)
            (tmpdir / COMMON_NAME).write_bytes(common_bytes)
            (tmpdir / ENUM_NAME).write_bytes(enum_bytes)
            harness_path = tmpdir / "ev117_harness.xsd"
            harness_path.write_text(harness(), encoding="utf-8")
            schema = etree.XMLSchema(etree.parse(str(harness_path)))
            print("OK  EV-117 exact Common V1.0 harness compiled")
            check_executable(schema)

    except (OSError, etree.XMLSchemaParseError, etree.XMLSyntaxError, EvidenceError) as exc:
        print(f"FAILED: EV-117 Common V1.0 evidence check: {exc}")
        return 1

    print("PASSED: EV-117 exact Common V1.0 authority and Deep Read executable boundaries confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
