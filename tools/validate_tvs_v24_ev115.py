#!/usr/bin/env python3
"""EV-115: candidate/integration TicketValidationService V2.4 evidence.

IMPORTANT AUTHORITY BOUNDARY
----------------------------
The tested V2.4 schema family is candidate/integration material in
`dev/schema-integration`. No VDV-301-2.4 release tag exists, and current
upstream master is dependency-incomplete for the referenced Common V2.4 file.
Therefore a PASS here is NOT official-release V2.4 XSD conformance.

No source XSD is modified.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
SERVICE = ROOT / "IBIS-IP_TicketValidationService_V2.4.xsd"
COMMON = ROOT / "IBIS-IP_common_V2.4.xsd"
ENUMS = ROOT / "IBIS-IP_Enumerations_V2.4.xsd"
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}

EXPECTED_GIT_BLOBS = {
    SERVICE.name: "34b18b8c874e325dd923b366a72bb0ebee32e59e",
    COMMON.name: "1946fd37e29ced605654f49ea3d98cd2fbbdc8e4",
    ENUMS.name: "2afed8cf23afa91db92b0f043cc5b4ad428b0f25",
}


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"OK  {message}")


def schema_names(tree: etree._ElementTree, kind: str) -> set[str]:
    return {
        n
        for n in tree.xpath(f"//xs:{kind}/@name", namespaces=NS)
        if isinstance(n, str)
    }


def compile_probe(body: str) -> etree.XMLSchema:
    with TemporaryDirectory(prefix="ev115_") as td:
        td_path = Path(td)
        for src in (SERVICE, COMMON, ENUMS):
            (td_path / src.name).write_bytes(src.read_bytes())
        probe = td_path / "ev115_probe.xsd"
        probe.write_text(
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            f"<xs:schema xmlns:xs=\"{XS}\" elementFormDefault=\"qualified\">\n"
            f"  <xs:include schemaLocation=\"{SERVICE.name}\"/>\n"
            f"{body}\n"
            "</xs:schema>\n",
            encoding="utf-8",
        )
        return etree.XMLSchema(etree.parse(str(probe)))


def expect_probe_compile_failure(body: str, expected_fragment: str) -> None:
    try:
        compile_probe(body)
    except etree.XMLSchemaParseError as exc:
        text = str(exc.error_log)
        require(expected_fragment in text, f"negative probe fails because unavailable type contains {expected_fragment!r}")
        return
    raise AssertionError("negative probe unexpectedly compiled")


def validate_text(schema: etree.XMLSchema, root: str, text: str, expected: bool) -> None:
    doc = etree.fromstring(f"<{root}>{text}</{root}>".encode("utf-8"))
    actual = schema.validate(doc)
    require(actual is expected, f"{root} value {text!r} -> {'valid' if expected else 'invalid'}")
    if not expected:
        print(f"    evidence: {schema.error_log.last_error}")


def validate_xml(schema: etree.XMLSchema, xml: str, expected: bool, label: str) -> None:
    doc = etree.fromstring(xml.encode("utf-8"))
    actual = schema.validate(doc)
    require(actual is expected, f"{label} -> {'valid' if expected else 'invalid'}")
    if not expected:
        print(f"    evidence: {schema.error_log.last_error}")


def main() -> int:
    print("AUTHORITY: candidate/integration V2.4 family; NOT official-release V2.4 conformance")

    for path in (SERVICE, COMMON, ENUMS):
        data = path.read_bytes()
        actual = git_blob_sha(data)
        require(actual == EXPECTED_GIT_BLOBS[path.name], f"exact candidate/integration blob {path.name} = {actual}")

    service_tree = etree.parse(str(SERVICE))
    common_tree = etree.parse(str(COMMON))
    enum_tree = etree.parse(str(ENUMS))

    service_includes = service_tree.xpath("/xs:schema/xs:include/@schemaLocation", namespaces=NS)
    require(
        service_includes == [COMMON.name, ENUMS.name],
        "candidate TVS V2.4 include route is Common V2.4 + Enumerations V2.4",
    )
    common_includes = common_tree.xpath("/xs:schema/xs:include/@schemaLocation", namespaces=NS)
    require(ENUMS.name in common_includes, "candidate Common V2.4 includes Enumerations V2.4")

    exact_schema = etree.XMLSchema(service_tree)
    print(f"OK  compiled candidate/integration {SERVICE.name}")

    global_elements = schema_names(service_tree, "element")
    service_complex_types = schema_names(service_tree, "complexType")

    # TVS-001: the new ShortHaul response is globally declared and structured,
    # but it is absent from the service operation inventory group.
    short_root = "TicketValidationService.GetCurrentShortHaulStopsResponse"
    require(short_root in global_elements, "TVS-001: ShortHaul response exists as a global element")
    require(
        "TicketValidationService.GetCurrentShortHaulStopsResponseStructure" in service_complex_types,
        "TVS-001: ShortHaul response structure exists",
    )
    require(
        "TicketValidationService.CurrentShortHaulStopsDataStructure" in service_complex_types,
        "TVS-001: ShortHaul data structure exists",
    )
    group_names = service_tree.xpath(
        "//xs:group[@name='TicketValidationServiceOperations']/xs:sequence/xs:element/@name",
        namespaces=NS,
    )
    require(short_root not in group_names, "TVS-001: ShortHaul response is omitted from TicketValidationServiceOperations")
    require(
        "TicketValidationService.GetCurrentTariffStopResponse" in group_names,
        "control: CurrentTariffStop response remains present in TicketValidationServiceOperations",
    )

    short_error = (
        "<TicketValidationService.GetCurrentShortHaulStopsResponse>"
        "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>"
        "</TicketValidationService.GetCurrentShortHaulStopsResponse>"
    )
    validate_xml(exact_schema, short_error, True, "candidate ShortHaul global response error branch")

    # ShortHaul field declarations: independently confirm the new V2.4 body.
    current_stops_min = service_tree.xpath(
        "string(//xs:complexType[@name='TicketValidationService.CurrentShortHaulStopsDataStructure']"
        "/xs:sequence/xs:element[@name='CurrentTariffStop']/@minOccurs)", namespaces=NS
    )
    current_stops_max = service_tree.xpath(
        "string(//xs:complexType[@name='TicketValidationService.CurrentShortHaulStopsDataStructure']"
        "/xs:sequence/xs:element[@name='CurrentTariffStop']/@maxOccurs)", namespaces=NS
    )
    require(current_stops_min == "0" and current_stops_max == "unbounded", "ShortHaul CurrentTariffStop is 0:* in candidate XSD")

    short_trip_type = service_tree.xpath(
        "string(//xs:complexType[@name='TicketValidationService.CurrentShortHaulStopsDataStructure']"
        "/xs:sequence/xs:element[@name='CurrentTripRef']/@type)", namespaces=NS
    )
    require(short_trip_type == "IBIS-IP.NMTOKEN", "ShortHaul CurrentTripRef exact type is IBIS-IP.NMTOKEN")

    # TVS-002: RouteDeviation PDF type vs candidate XSD type/value set.
    route_dev_type = service_tree.xpath(
        "string(//xs:complexType[@name='TicketValidationService.VehicleDataStructure']"
        "/xs:sequence/xs:element[@name='RouteDeviation']/@type)", namespaces=NS
    )
    require(route_dev_type == "RouteDeviationEnumeration", "VehicleData.RouteDeviation exact candidate type is RouteDeviationEnumeration")
    enum_simple_types = schema_names(enum_tree, "simpleType")
    require("RouteDeviationEnumeration" in enum_simple_types, "RouteDeviationEnumeration exists in candidate Enums V2.4")
    require("RouteDirectionEnumeration" in enum_simple_types, "PDF-printed RouteDirectionEnumeration also exists in candidate Enums V2.4")
    deviation_values = enum_tree.xpath(
        "//xs:simpleType[@name='RouteDeviationEnumeration']/xs:restriction/xs:enumeration/@value", namespaces=NS
    )
    direction_values = enum_tree.xpath(
        "//xs:simpleType[@name='RouteDirectionEnumeration']/xs:restriction/xs:enumeration/@value", namespaces=NS
    )
    require(deviation_values == ["onroute", "offroute", "unknown"], "RouteDeviationEnumeration values are onroute/offroute/unknown")
    require(direction_values == ["Forward", "Backward", "Clockwise", "Counterclockwise", "Other"], "RouteDirectionEnumeration retains its distinct direction values")
    deviation_probe = compile_probe('  <xs:element name="EV115.RouteDeviation" type="RouteDeviationEnumeration"/>')
    validate_text(deviation_probe, "EV115.RouteDeviation", "onroute", True)
    validate_text(deviation_probe, "EV115.RouteDeviation", "Forward", False)

    # DRTVS21-001: both CurrentTripRef occurrences use exact NMTOKEN.
    tariff_trip_type = service_tree.xpath(
        "string(//xs:complexType[@name='TicketValidationService.CurrentTariffStopDataStructure']"
        "/xs:sequence/xs:element[@name='CurrentTripRef']/@type)", namespaces=NS
    )
    require(tariff_trip_type == "IBIS-IP.NMTOKEN", "CurrentTariffStop CurrentTripRef exact type is IBIS-IP.NMTOKEN")
    common_complex_types = schema_names(common_tree, "complexType")
    require("IBIS-IP.NMTOKEN" in common_complex_types, "IBIS-IP.NMTOKEN exists in candidate Common V2.4")
    require("IBIS-IP.NMToken" not in common_complex_types, "PDF spelling IBIS-IP.NMToken is absent from candidate Common V2.4")
    expect_probe_compile_failure('  <xs:element name="EV115.BadNMToken" type="IBIS-IP.NMToken"/>', "IBIS-IP.NMToken")

    # DRTVS21-002: exact CurrentLineData type identifier.
    current_line_type = service_tree.xpath(
        "string(//xs:complexType[@name='TicketValidationService.GetCurrentLineResponseStructure']"
        "/xs:choice/xs:element[@name='CurrentLineData']/@type)", namespaces=NS
    )
    require(current_line_type == "TicketValidationService.CurrentLineDataStructure", "CurrentLineData exact candidate response type is TicketValidationService.CurrentLineDataStructure")
    require("TicketValidationServiceCurrentLineData" not in service_complex_types, "PDF missing-dot CurrentLine form is not an exact candidate service complex type")

    # TVS-003: CurrentTariffStop rename boundary remains executable.
    new_root = "TicketValidationService.GetCurrentTariffStopResponse"
    stale_root = "TicketValidationService.GetCurrentStopPointResponse"
    require(new_root in global_elements, "CurrentTariffStop response global root exists")
    require(stale_root not in global_elements, "stale CurrentStopPoint response global root is absent")
    valid_new = (
        "<TicketValidationService.GetCurrentTariffStopResponse>"
        "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>"
        "</TicketValidationService.GetCurrentTariffStopResponse>"
    )
    invalid_old = (
        "<TicketValidationService.GetCurrentStopPointResponse>"
        "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>"
        "</TicketValidationService.GetCurrentStopPointResponse>"
    )
    validate_xml(exact_schema, valid_new, True, "candidate CurrentTariffStop response")
    validate_xml(exact_schema, invalid_old, False, "stale CurrentStopPoint response")

    print("PASSED: EV-115 candidate/integration TVS V2.4 structure and behavior confirmed")
    print("GUARD: do not report this PASS as official-release V2.4 XSD conformance")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
