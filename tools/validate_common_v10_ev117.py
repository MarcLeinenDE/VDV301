#!/usr/bin/env python3
"""EV-117 exact-authority executable evidence for COMMON V1.0 Deep Read."""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path

from lxml import etree

XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}
COMMON = "IBIS-IP_common_V1.0.xsd"
ENUMS = "IBIS-IP_Enumerations_V1.0.xsd"
COMMON_BLOB = "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c"
ENUMS_BLOB = "a9bea5bc73003ed91ded8519db06c32c4067831d"


class EvidenceError(RuntimeError):
    pass


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def need(ok: bool, message: str) -> None:
    if not ok:
        raise EvidenceError(message)
    print(f"OK  {message}")


def ctype(root: etree._Element, name: str) -> etree._Element:
    node = root.find(f"xs:complexType[@name='{name}']", NS)
    if node is None:
        raise EvidenceError(f"missing complexType {name}")
    return node


def elem(root: etree._Element, type_name: str, name: str) -> etree._Element | None:
    return ctype(root, type_name).find(f".//xs:element[@name='{name}']", NS)


def occurs(node: etree._Element, attr: str) -> str:
    return node.get(attr, "1")


def expect_elem(
    root: etree._Element,
    type_name: str,
    name: str,
    *,
    typ: str | None = None,
    minimum: str | None = None,
    maximum: str | None = None,
) -> etree._Element:
    node = elem(root, type_name, name)
    need(node is not None, f"{type_name}.{name} exists")
    assert node is not None
    if typ is not None:
        need(node.get("type") == typ, f"{type_name}.{name} type={typ}")
    if minimum is not None:
        need(occurs(node, "minOccurs") == minimum, f"{type_name}.{name} minOccurs={minimum}")
    if maximum is not None:
        need(occurs(node, "maxOccurs") == maximum, f"{type_name}.{name} maxOccurs={maximum}")
    return node


def expect_absent(root: etree._Element, type_name: str, name: str) -> None:
    need(elem(root, type_name, name) is None, f"{type_name}.{name} is absent")


def enum_values(root: etree._Element, name: str) -> set[str]:
    node = root.find(f"xs:simpleType[@name='{name}']", NS)
    if node is None:
        raise EvidenceError(f"missing simpleType {name}")
    return {x.get("value", "") for x in node.findall(".//xs:enumeration", NS)}


def validate(schema: etree.XMLSchema, xml: str) -> tuple[bool, str]:
    doc = etree.fromstring(xml.encode())
    ok = bool(schema.validate(doc))
    if ok:
        return True, "OK"
    last = schema.error_log.last_error
    return False, str(last) if last is not None else "validation failed"


def probe(schema: etree.XMLSchema, label: str, xml: str, expected: bool) -> None:
    ok, detail = validate(schema, xml)
    if ok != expected:
        raise EvidenceError(
            f"{label}: got {'VALID' if ok else 'INVALID'}, expected "
            f"{'VALID' if expected else 'INVALID'}: {detail}"
        )
    print(f"OK  {label}: {'VALID' if ok else 'INVALID'} as expected")


def static_checks(common: etree._Element, enums: etree._Element) -> None:
    include = common.find("xs:include", NS)
    need(include is not None and include.get("schemaLocation") == ENUMS, "Common V1.0 includes Enumerations V1.0 exactly")

    # Explicit document-revision 1.1 changes absent from unchanged official V1.0 XSD.
    expect_elem(common, "ConnectionStructure", "DisplayContent", minimum="1", maximum="1")
    expect_elem(common, "ConnectionStructure", "ExpectedDepatureTime", typ="IBIS-IP.dateTime", minimum="0", maximum="1")
    expect_absent(common, "ConnectionStructure", "ExpectedDepartureTime")
    expect_absent(common, "ConnectionStructure", "ScheduledDepartureTime")
    expect_elem(common, "TripInformationStructure", "AdditionalTextMessage", typ="IBIS-IP.string", minimum="0", maximum="1")
    expect_absent(common, "TripInformationStructure", "RouteDirection")
    need(enums.find("xs:simpleType[@name='RouteDirectionEnumeration']", NS) is None, "Enumerations V1.0 has no RouteDirectionEnumeration")

    # Choice/compositor boundaries.
    add_choice = ctype(common, "AdditionalAnnouncementStructure").find(".//xs:choice", NS)
    need(add_choice is not None, "AdditionalAnnouncementStructure contains xs:choice")
    assert add_choice is not None
    need(occurs(add_choice, "minOccurs") == "0", "AdditionalAnnouncement xs:choice minOccurs=0")
    need([x.get("name") for x in add_choice.findall("xs:element", NS)] == ["ImmediateInformation", "PeriodicalInformation", "SpecificPoint"], "AdditionalAnnouncement exact choice names confirmed")

    response_choice = ctype(common, "DataAcceptedResponseStructure").find(".//xs:choice", NS)
    need(response_choice is not None, "DataAcceptedResponseStructure contains xs:choice")
    assert response_choice is not None
    need([x.get("name") for x in response_choice.findall("xs:element", NS)] == ["DataAcceptedResponseData", "OperationErrorMessage"], "DataAcceptedResponse exact choice branches confirmed")

    # Case-/spelling-sensitive element names.
    for type_name, good, bad in [
        ("BeaconPointStructure", "Desciption", "Description"),
        ("TSPPointStructure", "Desciption", "Description"),
        ("SubscribeRequestStructure", "ReplyPath", "Reply-Path"),
        ("UnsubscribeRequestStructure", "ReplyPath", "Reply-Path"),
        ("GlobalCardStatus", "GlobalCardStausID", "GlobalCardStatusID"),
        ("ZoneType", "FareZoneTypeName", "FarezoneTypeName"),
        ("LogMessageStructure", "Message", "MessageBody"),
    ]:
        expect_elem(common, type_name, good)
        expect_absent(common, type_name, bad)

    for name in ("FareZoneID", "FareZoneType", "FareZoneLongName", "FareZoneShortName"):
        expect_elem(common, "FareZoneInformationStructure", name)
    expect_absent(common, "FareZoneInformationStructure", "FarezoneID")
    expect_elem(common, "LogMessageStructure", "Message", typ="MessageStructure")

    # Cardinality/list boundaries.
    for type_name, child in [
        ("DeviceSpecificationWithStateListStructure", "DeviceSpecificationWithState"),
        ("ServiceIdentificationWithStateListStructure", "ServiceIdentificationWithState"),
        ("ServiceSpecificationWithStateListStructure", "ServiceSpecificationWithState"),
    ]:
        expect_elem(common, type_name, child, minimum="0", maximum="unbounded")
    expect_elem(common, "JourneyStopInformationStructure", "Announcement", minimum="0", maximum="1")
    expect_elem(common, "JourneyStopInformationStructure", "FareZone", minimum="0", maximum="1")
    need(common.find("xs:complexType[@name='DataVersionListStructure']", NS) is None, "V1.0 has no named DataVersionListStructure")
    data_version = ctype(common, "DeviceInformationStructure").find(".//xs:element[@name='DataVersionList']/xs:complexType/xs:sequence/xs:element[@name='DataVersion']", NS)
    need(data_version is not None, "DeviceInformation anonymous DataVersionList/DataVersion exists")
    assert data_version is not None
    need(occurs(data_version, "minOccurs") == "0" and occurs(data_version, "maxOccurs") == "unbounded", "anonymous DataVersionList permits DataVersion 0:*")

    # ServiceIdentification and ShortTripStop model identity.
    expect_elem(common, "ServiceIdentificationStructure", "Service", typ="ServiceSpecificationStructure")
    expect_absent(common, "ServiceIdentificationStructure", "ServiceName")
    expect_elem(common, "ServiceIdentificationWithStateListStructure", "ServiceIdentificationWithState", typ="ServiceIdentificationWithStateStructure", minimum="0", maximum="unbounded")
    expect_elem(common, "ShortTripStopListStructure", "ShortTripStop", typ="ShortTripStopStructure", minimum="1", maximum="unbounded")
    expect_absent(common, "ShortTripStopListStructure", "ShortTripStopList")
    for type_name in ("ShortTripStopStructure", "StopPointTariffInformationStructure"):
        expect_elem(common, type_name, "JourneyStopInformation", typ="JourneyStopInformationStructure")
        expect_elem(common, type_name, "FareZoneInformation", typ="FareZoneInformationStructure")

    # Historical enum lexemes/inventory.
    for type_name, present, absent in [
        ("DoorCountingObjectClassEnumeration", "WheelChair", "Wheelchair"),
        ("DoorCountingObjectClassEnumeration", "Other", "Others"),
        ("GNSSTypeEnumeration", "other", "Other"),
        ("TicketValidationEnumeration", "valid", "Valid"),
        ("VehicleModeEnumeration", "air", "Air"),
    ]:
        values = enum_values(enums, type_name)
        need(present in values, f"{type_name} contains {present}")
        need(absent not in values, f"{type_name} excludes PDF-side {absent}")
    need("PassengerCountingService" not in enum_values(enums, "ServiceNameEnumeration"), "ServiceNameEnumeration V1.0 lacks PassengerCountingService")
    need("starting" not in enum_values(enums, "ServiceStateEnumeration"), "ServiceStateEnumeration V1.0 lacks starting")


def harness() -> str:
    roots = {
        "TestAdditionalAnnouncement": "AdditionalAnnouncementStructure",
        "TestDataAcceptedResponse": "DataAcceptedResponseStructure",
        "TestDeviceSpecificationWithStateList": "DeviceSpecificationWithStateListStructure",
        "TestServiceIdentificationWithStateList": "ServiceIdentificationWithStateListStructure",
        "TestServiceSpecificationWithStateList": "ServiceSpecificationWithStateListStructure",
        "TestServiceIdentification": "ServiceIdentificationStructure",
        "TestBeaconPoint": "BeaconPointStructure",
        "TestTSPPoint": "TSPPointStructure",
        "TestDoorClass": "DoorCountingObjectClassEnumeration",
        "TestGNSSType": "GNSSTypeEnumeration",
        "TestTicketValidation": "TicketValidationEnumeration",
        "TestVehicleMode": "VehicleModeEnumeration",
        "TestServiceName": "ServiceNameEnumeration",
        "TestServiceState": "ServiceStateEnumeration",
    }
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<xs:schema xmlns:xs="{XS}" elementFormDefault="qualified" attributeFormDefault="unqualified">',
        f'  <xs:include schemaLocation="{COMMON}"/>',
    ]
    lines.extend(f'  <xs:element name="{name}" type="{typ}"/>' for name, typ in roots.items())
    lines.append("</xs:schema>")
    return "\n".join(lines) + "\n"


def executable_checks(schema: etree.XMLSchema) -> None:
    probe(schema, "AdditionalAnnouncement omitted choice", "<TestAdditionalAnnouncement><AnnouncementRef><Value>ann1</Value></AnnouncementRef></TestAdditionalAnnouncement>", True)
    probe(schema, "AdditionalAnnouncement SpecificPoint", "<TestAdditionalAnnouncement><AnnouncementRef><Value>ann1</Value></AnnouncementRef><SpecificPoint><PointRef><Value>p1</Value></PointRef><DistanceToPreviousPoint><Value>1.0</Value></DistanceToPreviousPoint></SpecificPoint></TestAdditionalAnnouncement>", True)
    probe(schema, "AdditionalAnnouncement PDF-only InformationAtSpecificPoint", "<TestAdditionalAnnouncement><AnnouncementRef><Value>ann1</Value></AnnouncementRef><InformationAtSpecificPoint><PointRef><Value>p1</Value></PointRef><DistanceToPreviousPoint><Value>1.0</Value></DistanceToPreviousPoint></InformationAtSpecificPoint></TestAdditionalAnnouncement>", False)

    data = "<DataAcceptedResponseData><TimeStamp><Value>2026-01-01T00:00:00Z</Value></TimeStamp><DataAccepted><Value>true</Value></DataAccepted></DataAcceptedResponseData>"
    error = "<OperationErrorMessage><Value>ev117</Value></OperationErrorMessage>"
    probe(schema, "DataAcceptedResponse data branch", f"<TestDataAcceptedResponse>{data}</TestDataAcceptedResponse>", True)
    probe(schema, "DataAcceptedResponse error branch", f"<TestDataAcceptedResponse>{error}</TestDataAcceptedResponse>", True)
    probe(schema, "DataAcceptedResponse both branches", f"<TestDataAcceptedResponse>{data}{error}</TestDataAcceptedResponse>", False)

    for root in ("TestDeviceSpecificationWithStateList", "TestServiceIdentificationWithStateList", "TestServiceSpecificationWithStateList"):
        probe(schema, f"{root} empty", f"<{root}/>", True)

    intl = "<Value>text</Value><Language>de</Language>"
    probe(schema, "BeaconPoint XSD Desciption", f"<TestBeaconPoint><BeaconCode><Value>b1</Value></BeaconCode><Desciption>{intl}</Desciption></TestBeaconPoint>", True)
    probe(schema, "BeaconPoint PDF Description alias", f"<TestBeaconPoint><BeaconCode><Value>b1</Value></BeaconCode><Description>{intl}</Description></TestBeaconPoint>", False)
    probe(schema, "TSPPoint XSD Desciption", f"<TestTSPPoint><TSPCode><Value>t1</Value></TSPCode><Desciption>{intl}</Desciption></TestTSPPoint>", True)
    probe(schema, "TSPPoint PDF Description alias", f"<TestTSPPoint><TSPCode><Value>t1</Value></TSPCode><Description>{intl}</Description></TestTSPPoint>", False)

    service = "<Service><ServiceName>TimeService</ServiceName><IBIS-IP-Version><Value>1.0</Value></IBIS-IP-Version></Service>"
    bad_service = "<ServiceName><ServiceName>TimeService</ServiceName><IBIS-IP-Version><Value>1.0</Value></IBIS-IP-Version></ServiceName>"
    device = "<Device><DeviceClass>OnBoardUnit</DeviceClass><DeviceID><Value>ev117-device</Value></DeviceID></Device>"
    probe(schema, "ServiceIdentification XSD outer Service", f"<TestServiceIdentification>{service}{device}</TestServiceIdentification>", True)
    probe(schema, "ServiceIdentification PDF outer ServiceName", f"<TestServiceIdentification>{bad_service}{device}</TestServiceIdentification>", False)

    for root, value, expected in [
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
    ]:
        probe(schema, f"{root}={value}", f"<{root}>{value}</{root}>", expected)


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    try:
        common_bytes = (repo / COMMON).read_bytes()
        enum_bytes = (repo / ENUMS).read_bytes()
        need(git_blob_sha(common_bytes) == COMMON_BLOB, f"Common V1.0 exact official blob {COMMON_BLOB}")
        need(git_blob_sha(enum_bytes) == ENUMS_BLOB, f"Enumerations V1.0 exact official blob {ENUMS_BLOB}")
        common_root = etree.fromstring(common_bytes)
        enum_root = etree.fromstring(enum_bytes)
        static_checks(common_root, enum_root)

        with tempfile.TemporaryDirectory(prefix="vdv301_ev117_") as tmp:
            tmpdir = Path(tmp)
            (tmpdir / COMMON).write_bytes(common_bytes)
            (tmpdir / ENUMS).write_bytes(enum_bytes)
            hp = tmpdir / "ev117_harness.xsd"
            hp.write_text(harness(), encoding="utf-8")
            schema = etree.XMLSchema(etree.parse(str(hp)))
            print("OK  EV-117 exact Common V1.0 harness compiled")
            executable_checks(schema)
    except (OSError, etree.XMLSyntaxError, etree.XMLSchemaParseError, EvidenceError) as exc:
        print(f"FAILED: EV-117 Common V1.0 evidence check: {exc}")
        return 1

    print("PASSED: EV-117 exact Common V1.0 authority and Deep Read executable boundaries confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
