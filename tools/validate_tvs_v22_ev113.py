#!/usr/bin/env python3
"""EV-113: executable/type/name evidence for TicketValidationService V2.2.

Normative inputs are the exact repository XSD files selected for the official
VDV-301-2.2 TicketValidationService route. No source XSD is modified.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
SERVICE = ROOT / "IBIS-IP_TicketValidationService_V2.2.xsd"
COMMON = ROOT / "IBIS-IP_common_V2.2.xsd"
ENUMS = ROOT / "IBIS-IP_Enumerations_V2.2.xsd"
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}

EXPECTED_GIT_BLOBS = {
    SERVICE.name: "5a4be2b2ba66860f035777ec0458dba0790880e1",
    COMMON.name: "468fee6d177e7185dbcd5d3f90cfb114e29e01ae",
    ENUMS.name: "2a23b512379b18e8f122ac1272cef8229fb86283",
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
    with TemporaryDirectory(prefix="ev113_") as td:
        td_path = Path(td)
        # Preserve exact dependency file names because xs:include is relative.
        for src in (SERVICE, COMMON, ENUMS):
            (td_path / src.name).write_bytes(src.read_bytes())
        probe = td_path / "ev113_probe.xsd"
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
        require(
            expected_fragment in text,
            f"negative probe fails because unavailable type contains {expected_fragment!r}",
        )
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
    for path in (SERVICE, COMMON, ENUMS):
        data = path.read_bytes()
        actual = git_blob_sha(data)
        require(actual == EXPECTED_GIT_BLOBS[path.name], f"exact authority blob {path.name} = {actual}")

    service_tree = etree.parse(str(SERVICE))
    common_tree = etree.parse(str(COMMON))
    enum_tree = etree.parse(str(ENUMS))

    includes = service_tree.xpath("/xs:schema/xs:include/@schemaLocation", namespaces=NS)
    require(
        includes == [COMMON.name, ENUMS.name],
        "TVS V2.2 exact include route is Common V2.2 + Enumerations V2.2",
    )

    exact_schema = etree.XMLSchema(service_tree)
    print(f"OK  compiled exact {SERVICE.name}")

    # TVS-002: V2.2 differs materially from V2.1 because both enum names now
    # exist. Prove the actual selected type and the incompatible value sets.
    route_dev_type = service_tree.xpath(
        "string(//xs:complexType[@name='TicketValidationService.VehicleDataStructure']"
        "/xs:sequence/xs:element[@name='RouteDeviation']/@type)",
        namespaces=NS,
    )
    require(
        route_dev_type == "RouteDeviationEnumeration",
        "VehicleData.RouteDeviation exact type is RouteDeviationEnumeration",
    )

    enum_simple_types = schema_names(enum_tree, "simpleType")
    require("RouteDeviationEnumeration" in enum_simple_types, "RouteDeviationEnumeration exists in exact Enumerations V2.2")
    require("RouteDirectionEnumeration" in enum_simple_types, "PDF-printed RouteDirectionEnumeration also exists in exact Enumerations V2.2")

    deviation_values = enum_tree.xpath(
        "//xs:simpleType[@name='RouteDeviationEnumeration']/xs:restriction/xs:enumeration/@value",
        namespaces=NS,
    )
    direction_values = enum_tree.xpath(
        "//xs:simpleType[@name='RouteDirectionEnumeration']/xs:restriction/xs:enumeration/@value",
        namespaces=NS,
    )
    require(
        deviation_values == ["onroute", "offroute", "unknown"],
        "RouteDeviationEnumeration exact value set is onroute/offroute/unknown",
    )
    require(
        direction_values == ["Forward", "Backward", "Clockwise", "Counterclockwise", "Other"],
        "RouteDirectionEnumeration exact value set is Forward/Backward/Clockwise/Counterclockwise/Other",
    )

    deviation_probe = compile_probe('  <xs:element name="EV113.RouteDeviation" type="RouteDeviationEnumeration"/>')
    direction_probe = compile_probe('  <xs:element name="EV113.RouteDirection" type="RouteDirectionEnumeration"/>')
    for value in deviation_values:
        validate_text(deviation_probe, "EV113.RouteDeviation", value, True)
    for value in direction_values:
        validate_text(direction_probe, "EV113.RouteDirection", value, True)
    validate_text(deviation_probe, "EV113.RouteDeviation", "Forward", False)
    validate_text(direction_probe, "EV113.RouteDirection", "onroute", False)

    # CurrentTripRef: exact V2.2 type remains case-sensitive NMTOKEN.
    current_trip_ref_type = service_tree.xpath(
        "string(//xs:complexType[@name='TicketValidationService.CurrentTariffStopDataStructure']"
        "/xs:sequence/xs:element[@name='CurrentTripRef']/@type)",
        namespaces=NS,
    )
    require(current_trip_ref_type == "IBIS-IP.NMTOKEN", "CurrentTripRef exact type is IBIS-IP.NMTOKEN")

    common_complex_types = schema_names(common_tree, "complexType")
    require("IBIS-IP.NMTOKEN" in common_complex_types, "IBIS-IP.NMTOKEN exists in exact Common V2.2")
    require("IBIS-IP.NMToken" not in common_complex_types, "PDF-printed IBIS-IP.NMToken is absent from exact Common V2.2")
    expect_probe_compile_failure(
        '  <xs:element name="EV113.BadNMToken" type="IBIS-IP.NMToken"/>',
        "IBIS-IP.NMToken",
    )

    # CurrentLine display anomaly: executable evidence is limited to the exact
    # type identifier, because PDF display conventions may omit Structure.
    current_line_type = service_tree.xpath(
        "string(//xs:complexType[@name='TicketValidationService.GetCurrentLineResponseStructure']"
        "/xs:choice/xs:element[@name='CurrentLineData']/@type)",
        namespaces=NS,
    )
    require(
        current_line_type == "TicketValidationService.CurrentLineDataStructure",
        "CurrentLineData exact response type is TicketValidationService.CurrentLineDataStructure",
    )
    service_complex_types = schema_names(service_tree, "complexType")
    require(
        "TicketValidationServiceCurrentLineData" not in service_complex_types,
        "PDF missing-dot form TicketValidationServiceCurrentLineData is not an exact service complex type",
    )

    # TVS-003: prove the V2.2 executable rename boundary. The PDF may contain
    # stale labels, but the selected schema exposes only CurrentTariffStop names.
    global_elements = schema_names(service_tree, "element")
    require(
        "TicketValidationService.GetCurrentTariffStopResponse" in global_elements,
        "exact V2.2 global root GetCurrentTariffStopResponse exists",
    )
    require(
        "TicketValidationService.GetCurrentStopPointResponse" not in global_elements,
        "stale PDF GetCurrentStopPointResponse is absent as exact V2.2 global root",
    )
    require(
        "TicketValidationService.CurrentTariffStopDataStructure" in service_complex_types,
        "exact V2.2 CurrentTariffStopDataStructure exists",
    )
    require(
        "TicketValidationService.CurrentStopPointDataStructure" not in service_complex_types,
        "stale PDF CurrentStopPointDataStructure is absent from exact V2.2 service complex types",
    )

    valid_new_root = (
        "<TicketValidationService.GetCurrentTariffStopResponse>"
        "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>"
        "</TicketValidationService.GetCurrentTariffStopResponse>"
    )
    stale_old_root = (
        "<TicketValidationService.GetCurrentStopPointResponse>"
        "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>"
        "</TicketValidationService.GetCurrentStopPointResponse>"
    )
    validate_xml(exact_schema, valid_new_root, True, "exact GetCurrentTariffStopResponse error branch")
    validate_xml(exact_schema, stale_old_root, False, "stale GetCurrentStopPointResponse root")

    print("PASSED: EV-113 TVS V2.2 exact rename/type/value-set behaviour confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
