#!/usr/bin/env python3
"""EV-120: exact historical-upstream Common V2.2 Deep Read executable evidence."""

from __future__ import annotations

import hashlib
import tempfile
from pathlib import Path

from lxml import etree

XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}
COMMON = "IBIS-IP_common_V2.2.xsd"
ENUMS = "IBIS-IP_Enumerations_V2.2.xsd"
COMMON_BLOB = "468fee6d177e7185dbcd5d3f90cfb114e29e01ae"
ENUMS_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"


class EvidenceError(RuntimeError):
    pass


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


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
    return {n.get("value", "") for n in node.findall(".//xs:enumeration", NS)}


def validate(schema: etree.XMLSchema, xml: str) -> tuple[bool, str]:
    doc = etree.fromstring(xml.encode("utf-8"))
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
    need(
        include is not None and include.get("schemaLocation") == ENUMS,
        "Common V2.2 includes Enumerations V2.2 exactly",
    )

    # FR-COM22-001: PDF wrapper names vs exact primitive XSD declarations.
    expect_elem(common, "InternationalTextType", "Value", typ="xs:string")
    expect_elem(common, "InternationalTextType", "Language", typ="xs:language")

    # FR-COM22-002: PDF requires a one-of in both rows; XSD makes both choices optional.
    netex = ctype(common, "NetexMode")
    choices = netex.findall("./xs:sequence/xs:choice", NS)
    need(len(choices) == 2, "NetexMode has exactly two top-level xs:choice compositors")
    for index, choice in enumerate(choices, start=1):
        need(
            occurs(choice, "minOccurs") == "0",
            f"NetexMode choice {index} minOccurs=0",
        )
    need(
        [n.get("name") for n in choices[0].findall("xs:element", NS)]
        == ["PtMainMode", "PrivateMainMode"],
        "NetexMode main-mode choice branches confirmed",
    )
    need(
        [n.get("ref") for n in choices[1].findall("xs:group", NS)]
        == ["PtSubmodeChoiceGroup", "PrivateSubmodeChoiceGroup"],
        "NetexMode submode choice groups confirmed",
    )

    # FR-COM22-003: AdditionalAnnouncement optional one-of and exact third branch.
    add_choice = ctype(common, "AdditionalAnnouncementStructure").find(".//xs:choice", NS)
    need(add_choice is not None, "AdditionalAnnouncementStructure contains xs:choice")
    assert add_choice is not None
    need(occurs(add_choice, "minOccurs") == "0", "AdditionalAnnouncement xs:choice minOccurs=0")
    need(
        [x.get("name") for x in add_choice.findall("xs:element", NS)]
        == ["ImmediateInformation", "PeriodicalInformation", "SpecificPoint"],
        "AdditionalAnnouncement exact choice names confirmed",
    )

    # FR-COM22-004: PDF 0:* vs XSD effective 0:1.
    expect_elem(common, "ConnectionStructure", "TransportMode", minimum="0", maximum="1")
    expect_elem(common, "ConnectionStructure", "ConnectionMode", minimum="0", maximum="1")

    # FR-COM22-005: DataAcceptedResponse is an exclusive XSD choice.
    response_choice = ctype(common, "DataAcceptedResponseStructure").find(".//xs:choice", NS)
    need(response_choice is not None, "DataAcceptedResponseStructure contains xs:choice")
    assert response_choice is not None
    need(
        [x.get("name") for x in response_choice.findall("xs:element", NS)]
        == ["DataAcceptedResponseData", "OperationErrorMessage"],
        "DataAcceptedResponse exact choice branches confirmed",
    )

    # FR-COM22-006 / 007: cardinality boundaries.
    expect_elem(common, "DataVersionListStructure", "DataVersion", minimum="0", maximum="unbounded")
    for type_name, child in [
        ("DeviceSpecificationWithStateListStructure", "DeviceSpecificationWithState"),
        ("ServiceIdentificationWithStateListStructure", "ServiceIdentificationWithState"),
        ("ServiceSpecificationWithStateListStructure", "ServiceSpecificationWithState"),
    ]:
        expect_elem(common, type_name, child, minimum="0", maximum="unbounded")
    expect_elem(common, "JourneyStopInformationStructure", "Announcement", minimum="0", maximum="1")
    expect_elem(common, "JourneyStopInformationStructure", "FareZone", minimum="0", maximum="1")
    expect_elem(common, "StopInformationRequestStructure", "StopName", minimum="0", maximum="unbounded")
    expect_elem(
        common,
        "TripInformationStructure",
        "AdditionalTextMessage",
        typ="InternationalTextType",
        minimum="0",
        maximum="1",
    )
    expect_elem(common, "UnsubscribeResponseStructure", "Active", minimum="1", maximum="1")

    # FR-COM22-008 / 009 / 010: exact name/type boundaries.
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

    for good in ("FareZoneID", "FareZoneType", "FareZoneLongName", "FareZoneShortName"):
        expect_elem(common, "FareZoneInformationStructure", good)
    for bad in ("FarezoneID", "FarezoneType", "FarezoneLongName", "FarezoneShortName"):
        expect_absent(common, "FareZoneInformationStructure", bad)

    expect_elem(common, "LogMessageStructure", "Message", typ="MessageStructure")
    expect_elem(common, "ServiceIdentificationStructure", "Service", typ="ServiceSpecificationStructure")
    expect_absent(common, "ServiceIdentificationStructure", "ServiceName")
    expect_elem(
        common,
        "ServiceIdentificationWithStateListStructure",
        "ServiceIdentificationWithState",
        typ="ServiceIdentificationWithStateStructure",
        minimum="0",
        maximum="unbounded",
    )
    expect_elem(
        common,
        "ShortTripStopListStructure",
        "ShortTripStop",
        typ="ShortTripStopStructure",
        minimum="1",
        maximum="unbounded",
    )
    expect_absent(common, "ShortTripStopListStructure", "ShortTripStopList")

    # FR-COM22-012 / 013: exact enumeration inventories and lexical boundaries.
    checks = [
        ("DeviceStateEnumeration", "warning", None),
        ("ServiceNameEnumeration", "SystemMonitoringService", "SystemDocumentationService"),
        ("ServiceNameEnumeration", "SystemMonitoringService", "SystemManagementService"),
        ("DoorCountingObjectClassEnumeration", "WheelChair", "Wheelchair"),
        ("DoorCountingObjectClassEnumeration", "Other", "Others"),
        ("GNSSTypeEnumeration", "other", "Other"),
        ("TicketValidationEnumeration", "valid", "Valid"),
        ("VehicleModeEnumeration", "air", "Air"),
        ("RailSubmodeEnumeration", "specialTrain", "specialRail"),
        ("AirSubmodeEnumeration", "canalBarge", None),
        ("FunicularSubmodeEnumeration", "unknown", "Unknown"),
        ("TaxiSubmodeEnumeration", "unknown", "Unknown"),
        ("TaxiSubmodeEnumeration", "undefined", "Undefined"),
    ]
    for type_name, present, absent in checks:
        values = enum_values(enums, type_name)
        need(present in values, f"{type_name} contains exact XSD value {present}")
        if absent is not None:
            need(absent not in values, f"{type_name} excludes PDF-side/stale value {absent}")


def harness() -> str:
    roots = {
        "TestInternationalText": "InternationalTextType",
        "TestNetexMode": "NetexMode",
        "TestAdditionalAnnouncement": "AdditionalAnnouncementStructure",
        "TestConnection": "ConnectionStructure",
        "TestDataAcceptedResponse": "DataAcceptedResponseStructure",
        "TestDataVersionList": "DataVersionListStructure",
        "TestDeviceSpecificationWithStateList": "DeviceSpecificationWithStateListStructure",
        "TestServiceIdentificationWithStateList": "ServiceIdentificationWithStateListStructure",
        "TestServiceSpecificationWithStateList": "ServiceSpecificationWithStateListStructure",
        "TestFareZoneInformation": "FareZoneInformationStructure",
        "TestGlobalCardStatus": "GlobalCardStatus",
        "TestJourneyStopInformation": "JourneyStopInformationStructure",
        "TestLogMessage": "LogMessageStructure",
        "TestServiceIdentification": "ServiceIdentificationStructure",
        "TestStopInformationRequest": "StopInformationRequestStructure",
        "TestSubscribeRequest": "SubscribeRequestStructure",
        "TestUnsubscribeRequest": "UnsubscribeRequestStructure",
        "TestUnsubscribeResponse": "UnsubscribeResponseStructure",
        "TestTripInformation": "TripInformationStructure",
        "TestBeaconPoint": "BeaconPointStructure",
        "TestTSPPoint": "TSPPointStructure",
        "TestZoneType": "ZoneType",
        "TestDeviceState": "DeviceStateEnumeration",
        "TestServiceName": "ServiceNameEnumeration",
        "TestDoorClass": "DoorCountingObjectClassEnumeration",
        "TestGNSSType": "GNSSTypeEnumeration",
        "TestTicketValidation": "TicketValidationEnumeration",
        "TestVehicleMode": "VehicleModeEnumeration",
        "TestRailSubmode": "RailSubmodeEnumeration",
        "TestAirSubmode": "AirSubmodeEnumeration",
        "TestFunicularSubmode": "FunicularSubmodeEnumeration",
        "TestTaxiSubmode": "TaxiSubmodeEnumeration",
    }
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<xs:schema xmlns:xs="{XS}" elementFormDefault="qualified" attributeFormDefault="unqualified">',
        f'  <xs:include schemaLocation="{COMMON}"/>',
    ]
    lines.extend(f'  <xs:element name="{name}" type="{typ}"/>' for name, typ in roots.items())
    lines.append("</xs:schema>")
    return "\n".join(lines) + "\n"


def intl(text: str = "Text", lang: str = "de") -> str:
    return f"<Value>{text}</Value><Language>{lang}</Language>"


def display_content() -> str:
    return (
        "<DisplayContent>"
        "<LineInformation><LineRef><Value>L1</Value></LineRef></LineInformation>"
        "<Destination><DestinationRef><Value>D1</Value></DestinationRef></Destination>"
        "</DisplayContent>"
    )


def journey_stop_base() -> str:
    return (
        "<StopRef><Value>S1</Value></StopRef>"
        f"<StopName>{intl('Stop')}</StopName>"
        f"{display_content()}"
    )


def stop_information(index: int) -> str:
    return (
        "<StopPoint>"
        f"<StopIndex><Value>{index}</Value></StopIndex>"
        f"<StopRef><Value>S{index}</Value></StopRef>"
        f"<StopName>{intl(f'Stop{index}')}</StopName>"
        f"{display_content()}"
        "</StopPoint>"
    )


def connection_base() -> str:
    return (
        "<StopRef><Value>S1</Value></StopRef>"
        "<ConnectionRef><Value>C1</Value></ConnectionRef>"
        "<ConnectionType>Interchange</ConnectionType>"
    )


def executable_checks(schema: etree.XMLSchema) -> None:
    # FR-COM22-001.
    probe(
        schema,
        "InternationalTextType exact primitive shape",
        "<TestInternationalText><Value>Hello</Value><Language>de</Language></TestInternationalText>",
        True,
    )
    probe(
        schema,
        "InternationalTextType PDF wrapper-shaped Value/Language",
        "<TestInternationalText><Value><Value>Hello</Value></Value>"
        "<Language><Value>de</Value></Language></TestInternationalText>",
        False,
    )

    # FR-COM22-002: empty NetexMode is executable proof of XSD permissiveness.
    probe(schema, "NetexMode empty structure accepted by XSD", "<TestNetexMode/>", True)
    probe(
        schema,
        "NetexMode populated exact main/submode",
        "<TestNetexMode><PtMainMode>AirSubmode</PtMainMode><AirSubmode>unknown</AirSubmode></TestNetexMode>",
        True,
    )

    # FR-COM22-003.
    probe(
        schema,
        "AdditionalAnnouncement omitted optional choice",
        "<TestAdditionalAnnouncement><AnnouncementRef><Value>a1</Value></AnnouncementRef></TestAdditionalAnnouncement>",
        True,
    )
    specific = (
        "<SpecificPoint><PointRef><Value>p1</Value></PointRef>"
        "<DistanceToPreviousPoint><Value>1.0</Value></DistanceToPreviousPoint></SpecificPoint>"
    )
    pdf_specific = specific.replace("SpecificPoint", "InformationAtSpecificPoint")
    probe(
        schema,
        "AdditionalAnnouncement exact SpecificPoint",
        f"<TestAdditionalAnnouncement><AnnouncementRef><Value>a1</Value></AnnouncementRef>"
        f"{specific}</TestAdditionalAnnouncement>",
        True,
    )
    probe(
        schema,
        "AdditionalAnnouncement PDF-only InformationAtSpecificPoint",
        f"<TestAdditionalAnnouncement><AnnouncementRef><Value>a1</Value></AnnouncementRef>"
        f"{pdf_specific}</TestAdditionalAnnouncement>",
        False,
    )

    # FR-COM22-004: XSD allows at most one TransportMode / ConnectionMode.
    vehicle = "<TransportMode><VehicleTypeRef><Value>bus</Value></VehicleTypeRef></TransportMode>"
    mode = "<ConnectionMode/>"
    base = connection_base()
    probe(schema, "Connection one TransportMode", f"<TestConnection>{base}{vehicle}</TestConnection>", True)
    probe(
        schema,
        "Connection two TransportMode entries",
        f"<TestConnection>{base}{vehicle}{vehicle}</TestConnection>",
        False,
    )
    probe(schema, "Connection one ConnectionMode", f"<TestConnection>{base}{mode}</TestConnection>", True)
    probe(
        schema,
        "Connection two ConnectionMode entries",
        f"<TestConnection>{base}{mode}{mode}</TestConnection>",
        False,
    )

    # FR-COM22-005.
    data = (
        "<DataAcceptedResponseData><TimeStamp><Value>2026-01-01T00:00:00Z</Value></TimeStamp>"
        "<DataAccepted><Value>true</Value></DataAccepted></DataAcceptedResponseData>"
    )
    error = "<OperationErrorMessage><Value>ev120</Value></OperationErrorMessage>"
    probe(schema, "DataAcceptedResponse data branch", f"<TestDataAcceptedResponse>{data}</TestDataAcceptedResponse>", True)
    probe(schema, "DataAcceptedResponse error branch", f"<TestDataAcceptedResponse>{error}</TestDataAcceptedResponse>", True)
    probe(
        schema,
        "DataAcceptedResponse both branches",
        f"<TestDataAcceptedResponse>{data}{error}</TestDataAcceptedResponse>",
        False,
    )

    # FR-COM22-006.
    for root in (
        "TestDataVersionList",
        "TestDeviceSpecificationWithStateList",
        "TestServiceIdentificationWithStateList",
        "TestServiceSpecificationWithStateList",
    ):
        probe(schema, f"{root} empty", f"<{root}/>", True)

    # FR-COM22-007: selected executable cardinality boundaries.
    announcement = "<Announcement><AnnouncementRef><Value>A1</Value></AnnouncementRef></Announcement>"
    base_stop = journey_stop_base()
    probe(
        schema,
        "JourneyStopInformation one Announcement",
        f"<TestJourneyStopInformation>{base_stop}{announcement}</TestJourneyStopInformation>",
        True,
    )
    probe(
        schema,
        "JourneyStopInformation two Announcements",
        f"<TestJourneyStopInformation>{base_stop}{announcement}{announcement}</TestJourneyStopInformation>",
        False,
    )
    fare = "<FareZone><Value>F1</Value></FareZone>"
    probe(
        schema,
        "JourneyStopInformation one FareZone",
        f"<TestJourneyStopInformation>{base_stop}{fare}</TestJourneyStopInformation>",
        True,
    )
    probe(
        schema,
        "JourneyStopInformation two FareZones",
        f"<TestJourneyStopInformation>{base_stop}{fare}{fare}</TestJourneyStopInformation>",
        False,
    )
    names = f"<StopName>{intl('One')}</StopName><StopName>{intl('Two')}</StopName>"
    probe(
        schema,
        "StopInformationRequest two StopName entries accepted by XSD",
        f"<TestStopInformationRequest>{names}{display_content()}</TestStopInformationRequest>",
        True,
    )
    stops = f"<StopSequence>{stop_information(1)}{stop_information(2)}</StopSequence>"
    trip_base = f"<TripRef><Value>T1</Value></TripRef>{stops}"
    msg = f"<AdditionalTextMessage>{intl('Info')}</AdditionalTextMessage>"
    probe(
        schema,
        "TripInformation one AdditionalTextMessage",
        f"<TestTripInformation>{trip_base}{msg}</TestTripInformation>",
        True,
    )
    probe(
        schema,
        "TripInformation two AdditionalTextMessage entries",
        f"<TestTripInformation>{trip_base}{msg}{msg}</TestTripInformation>",
        False,
    )
    active = "<Active><Value>true</Value></Active>"
    probe(schema, "UnsubscribeResponse exact required Active", f"<TestUnsubscribeResponse>{active}</TestUnsubscribeResponse>", True)
    probe(schema, "UnsubscribeResponse missing Active", "<TestUnsubscribeResponse/>", False)

    # FR-COM22-008: spelling/case boundaries.
    probe(
        schema,
        "FareZoneInformation XSD FareZoneID",
        "<TestFareZoneInformation><FareZoneID><Value>Z1</Value></FareZoneID></TestFareZoneInformation>",
        True,
    )
    probe(
        schema,
        "FareZoneInformation PDF FarezoneID",
        "<TestFareZoneInformation><FarezoneID><Value>Z1</Value></FarezoneID></TestFareZoneInformation>",
        False,
    )
    probe(
        schema,
        "GlobalCardStatus XSD GlobalCardStausID",
        "<TestGlobalCardStatus><GlobalCardStausID><Value>1</Value></GlobalCardStausID></TestGlobalCardStatus>",
        True,
    )
    probe(
        schema,
        "GlobalCardStatus PDF GlobalCardStatusID",
        "<TestGlobalCardStatus><GlobalCardStatusID><Value>1</Value></GlobalCardStatusID></TestGlobalCardStatus>",
        False,
    )

    provider = (
        "<MessageProvider><DeviceClass>OnBoardUnit</DeviceClass>"
        "<DeviceID><Value>D1</Value></DeviceID></MessageProvider>"
    )
    message_inner = (
        "<Message-ID><Value>1</Value></Message-ID>"
        "<TimeStamp><Value>2026-01-01T00:00:00Z</Value></TimeStamp>"
        "<MessageType>Status</MessageType><MessageText><Value>ok</Value></MessageText>"
    )
    probe(
        schema,
        "LogMessage exact Message",
        f"<TestLogMessage>{provider}<Message>{message_inner}</Message></TestLogMessage>",
        True,
    )
    probe(
        schema,
        "LogMessage PDF MessageBody",
        f"<TestLogMessage>{provider}<MessageBody>{message_inner}</MessageBody></TestLogMessage>",
        False,
    )

    for root in ("TestSubscribeRequest", "TestUnsubscribeRequest"):
        client = "<Client-IP-Address><Value>192.0.2.1</Value></Client-IP-Address>"
        probe(
            schema,
            f"{root} exact ReplyPath",
            f"<{root}>{client}<ReplyPath><Value>/reply</Value></ReplyPath></{root}>",
            True,
        )
        probe(
            schema,
            f"{root} PDF Reply-Path",
            f"<{root}>{client}<Reply-Path><Value>/reply</Value></Reply-Path></{root}>",
            False,
        )

    probe(
        schema,
        "BeaconPoint XSD Desciption",
        f"<TestBeaconPoint><BeaconCode><Value>B1</Value></BeaconCode><Desciption>{intl()}</Desciption></TestBeaconPoint>",
        True,
    )
    probe(
        schema,
        "BeaconPoint PDF Description",
        f"<TestBeaconPoint><BeaconCode><Value>B1</Value></BeaconCode><Description>{intl()}</Description></TestBeaconPoint>",
        False,
    )
    probe(
        schema,
        "TSPPoint XSD Desciption",
        f"<TestTSPPoint><TSPCode><Value>T1</Value></TSPCode><Desciption>{intl()}</Desciption></TestTSPPoint>",
        True,
    )
    probe(
        schema,
        "TSPPoint PDF Description",
        f"<TestTSPPoint><TSPCode><Value>T1</Value></TSPCode><Description>{intl()}</Description></TestTSPPoint>",
        False,
    )
    probe(
        schema,
        "ZoneType XSD FareZoneTypeName",
        f"<TestZoneType><FarezoneTypeID><Value>Z1</Value></FarezoneTypeID>"
        f"<FareZoneTypeName>{intl()}</FareZoneTypeName></TestZoneType>",
        True,
    )
    probe(
        schema,
        "ZoneType PDF FarezoneTypeName",
        f"<TestZoneType><FarezoneTypeID><Value>Z1</Value></FarezoneTypeID>"
        f"<FarezoneTypeName>{intl()}</FarezoneTypeName></TestZoneType>",
        False,
    )

    # FR-COM22-009.
    service_inner = (
        "<ServiceName>TimeService</ServiceName>"
        "<IBIS-IP-Version><Value>2.2</Value></IBIS-IP-Version>"
    )
    device = (
        "<Device><DeviceClass>OnBoardUnit</DeviceClass>"
        "<DeviceID><Value>D1</Value></DeviceID></Device>"
    )
    probe(
        schema,
        "ServiceIdentification exact outer Service",
        f"<TestServiceIdentification><Service>{service_inner}</Service>{device}</TestServiceIdentification>",
        True,
    )
    probe(
        schema,
        "ServiceIdentification PDF outer ServiceName",
        f"<TestServiceIdentification><ServiceName>{service_inner}</ServiceName>{device}</TestServiceIdentification>",
        False,
    )

    # FR-COM22-012 / 013: enumeration boundaries.
    enum_probes = [
        ("TestDeviceState", "warning", True),
        ("TestServiceName", "SystemMonitoringService", True),
        ("TestServiceName", "SystemDocumentationService", False),
        ("TestServiceName", "SystemManagementService", False),
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
        ("TestRailSubmode", "specialTrain", True),
        ("TestRailSubmode", "specialRail", False),
        ("TestAirSubmode", "canalBarge", True),
        ("TestFunicularSubmode", "unknown", True),
        ("TestFunicularSubmode", "Unknown", False),
        ("TestTaxiSubmode", "unknown", True),
        ("TestTaxiSubmode", "Unknown", False),
        ("TestTaxiSubmode", "undefined", True),
        ("TestTaxiSubmode", "Undefined", False),
    ]
    for root, value, expected in enum_probes:
        probe(schema, f"{root}={value}", f"<{root}>{value}</{root}>", expected)


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    try:
        common_bytes = (repo / COMMON).read_bytes()
        enum_bytes = (repo / ENUMS).read_bytes()
        need(
            git_blob_sha(common_bytes) == COMMON_BLOB,
            f"Common V2.2 exact historical-upstream blob {COMMON_BLOB}",
        )
        need(
            git_blob_sha(enum_bytes) == ENUMS_BLOB,
            f"Enumerations V2.2 exact historical-upstream blob {ENUMS_BLOB}",
        )
        common_root = etree.fromstring(common_bytes)
        enum_root = etree.fromstring(enum_bytes)
        static_checks(common_root, enum_root)

        with tempfile.TemporaryDirectory(prefix="vdv301_ev120_") as tmp:
            tmpdir = Path(tmp)
            (tmpdir / COMMON).write_bytes(common_bytes)
            (tmpdir / ENUMS).write_bytes(enum_bytes)
            hp = tmpdir / "ev120_harness.xsd"
            hp.write_text(harness(), encoding="utf-8")
            schema = etree.XMLSchema(etree.parse(str(hp)))
            print("OK  EV-120 exact Common V2.2 harness compiled")
            executable_checks(schema)
    except (OSError, etree.XMLSyntaxError, etree.XMLSchemaParseError, EvidenceError) as exc:
        print(f"FAILED: EV-120 Common V2.2 evidence check: {exc}")
        return 1

    print(
        "PASSED: EV-120 exact historical-upstream Common V2.2 authority "
        "and Deep Read boundaries confirmed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
