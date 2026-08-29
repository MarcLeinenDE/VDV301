#!/usr/bin/env python3
"""EV-112: executable/type-reference evidence for TicketValidationService V2.1.

Normative inputs are the exact repository XSD files selected for the official
VDV-301-2.1 TicketValidationService route.  No source XSD is modified.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
SERVICE = ROOT / "IBIS-IP_TicketValidationService_V2.1.xsd"
COMMON = ROOT / "IBIS-IP_common_V1.0.xsd"
ENUMS = ROOT / "IBIS-IP_Enumerations_V1.0.xsd"
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}

EXPECTED_GIT_BLOBS = {
    SERVICE.name: "f6497e6469b82ee19b185c4de749d13a7ca60bed",
    COMMON.name: "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c",
    ENUMS.name: "a9bea5bc73003ed91ded8519db06c32c4067831d",
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
    with TemporaryDirectory(prefix="ev112_") as td:
        td_path = Path(td)
        # Preserve exact dependency file names because xs:include is relative.
        for src in (SERVICE, COMMON, ENUMS):
            (td_path / src.name).write_bytes(src.read_bytes())
        probe = td_path / "ev112_probe.xsd"
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
        "TVS V2.1 exact include route is Common V1.0 + Enumerations V1.0",
    )

    # Compile the untouched selected service family first.
    etree.XMLSchema(service_tree)
    print(f"OK  compiled exact {SERVICE.name}")

    route_dev_type = service_tree.xpath(
        "string(//xs:complexType[@name='TicketValidationService.VehicleDataStructure']"
        "/xs:sequence/xs:element[@name='RouteDeviation']/@type)",
        namespaces=NS,
    )
    require(route_dev_type == "RouteDeviationEnumeration", "VehicleData.RouteDeviation exact type is RouteDeviationEnumeration")

    enum_simple_types = schema_names(enum_tree, "simpleType")
    require("RouteDeviationEnumeration" in enum_simple_types, "RouteDeviationEnumeration exists in exact Enumerations V1.0")
    require("RouteDirectionEnumeration" not in enum_simple_types, "PDF-printed RouteDirectionEnumeration is absent from exact Enumerations V1.0")

    route_values = enum_tree.xpath(
        "//xs:simpleType[@name='RouteDeviationEnumeration']/xs:restriction/xs:enumeration/@value",
        namespaces=NS,
    )
    require(route_values == ["onroute", "offroute", "unknown"], "RouteDeviationEnumeration exact value set is onroute/offroute/unknown")

    # Executable probe uses the exact normative enum type.  The probe root itself
    # is non-normative and exists only to exercise the selected type.
    route_probe = compile_probe('  <xs:element name="EV112.RouteDeviation" type="RouteDeviationEnumeration"/>')
    for value in route_values:
        validate_text(route_probe, "EV112.RouteDeviation", value, True)
    validate_text(route_probe, "EV112.RouteDeviation", "NOT_A_ROUTE_DEVIATION", False)

    # Supporting declaration evidence for the visible PDF IBIS-IP.NMToken typo.
    current_trip_ref_type = service_tree.xpath(
        "string(//xs:complexType[@name='TicketValidationService.CurrentStopPointDataStructure']"
        "/xs:sequence/xs:element[@name='CurrentTripRef']/@type)",
        namespaces=NS,
    )
    require(current_trip_ref_type == "IBIS-IP.NMTOKEN", "CurrentTripRef exact type is IBIS-IP.NMTOKEN")

    common_complex_types = schema_names(common_tree, "complexType")
    require("IBIS-IP.NMTOKEN" in common_complex_types, "IBIS-IP.NMTOKEN exists in exact Common V1.0")
    require("IBIS-IP.NMToken" not in common_complex_types, "PDF-printed IBIS-IP.NMToken is absent from exact Common V1.0")

    # A probe referencing the PDF spelling must fail to compile; this is type-name
    # evidence only, not a claim that the PDF is executable authority.
    expect_probe_compile_failure(
        '  <xs:element name="EV112.BadNMToken" type="IBIS-IP.NMToken"/>',
        "IBIS-IP.NMToken",
    )

    # Supporting declaration evidence for the visible missing-dot CurrentLineData
    # type reference.  PDF display conventions omit Structure suffix elsewhere, so
    # the executable claim here is limited to the exact service type spelling.
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

    print("PASSED: EV-112 TVS V2.1 exact type-reference behaviour confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
