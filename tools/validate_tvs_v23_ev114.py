#!/usr/bin/env python3
"""EV-114: TicketValidationService V2.3 official-route vs candidate authority guard.

The official VDV-301-2.3 release tag routes TicketValidationService V2.3
through the V2.2-named service XSD and its V2.2 dependencies. The integration
branch also contains a separately sourced V2.3-named candidate file. This
checker proves the repository-side identity/behavior boundary without changing
any XSD and without treating semantic similarity as provenance equivalence.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL = ROOT / "IBIS-IP_TicketValidationService_V2.2.xsd"
CANDIDATE = ROOT / "IBIS-IP_TicketValidationService_V2.3.xsd"
COMMON = ROOT / "IBIS-IP_common_V2.2.xsd"
ENUMS = ROOT / "IBIS-IP_Enumerations_V2.2.xsd"
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}

EXPECTED_GIT_BLOBS = {
    OFFICIAL.name: "5a4be2b2ba66860f035777ec0458dba0790880e1",
    CANDIDATE.name: "b17591c5b067254dd3e2260f3ef2acd2e18394a9",
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


def schema_names(tree: etree._ElementTree, kind: str) -> list[str]:
    return [
        n
        for n in tree.xpath(f"//xs:{kind}/@name", namespaces=NS)
        if isinstance(n, str)
    ]


def critical_signature(tree: etree._ElementTree) -> dict[str, object]:
    return {
        "includes": tree.xpath("/xs:schema/xs:include/@schemaLocation", namespaces=NS),
        "global_elements": tree.xpath("/xs:schema/xs:element/@name", namespaces=NS),
        "complex_types": schema_names(tree, "complexType"),
        "operation_members": tree.xpath(
            "//xs:group[@name='TicketValidationServiceOperations']/xs:sequence/xs:element/@name",
            namespaces=NS,
        ),
        "route_deviation_type": tree.xpath(
            "string(//xs:complexType[@name='TicketValidationService.VehicleDataStructure']"
            "/xs:sequence/xs:element[@name='RouteDeviation']/@type)",
            namespaces=NS,
        ),
        "current_trip_ref_type": tree.xpath(
            "string(//xs:complexType[@name='TicketValidationService.CurrentTariffStopDataStructure']"
            "/xs:sequence/xs:element[@name='CurrentTripRef']/@type)",
            namespaces=NS,
        ),
        "current_line_type": tree.xpath(
            "string(//xs:complexType[@name='TicketValidationService.GetCurrentLineResponseStructure']"
            "/xs:choice/xs:element[@name='CurrentLineData']/@type)",
            namespaces=NS,
        ),
    }


def compile_family(service: Path) -> etree.XMLSchema:
    with TemporaryDirectory(prefix="ev114_") as td:
        td_path = Path(td)
        for src in (service, COMMON, ENUMS):
            (td_path / src.name).write_bytes(src.read_bytes())
        return etree.XMLSchema(etree.parse(str(td_path / service.name)))


def compile_probe(service: Path, body: str) -> etree.XMLSchema:
    with TemporaryDirectory(prefix="ev114_probe_") as td:
        td_path = Path(td)
        for src in (service, COMMON, ENUMS):
            (td_path / src.name).write_bytes(src.read_bytes())
        probe = td_path / "ev114_probe.xsd"
        probe.write_text(
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
            f"<xs:schema xmlns:xs=\"{XS}\" elementFormDefault=\"qualified\">\n"
            f"  <xs:include schemaLocation=\"{service.name}\"/>\n"
            f"{body}\n"
            "</xs:schema>\n",
            encoding="utf-8",
        )
        return etree.XMLSchema(etree.parse(str(probe)))


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
    for path in (OFFICIAL, CANDIDATE, COMMON, ENUMS):
        actual = git_blob_sha(path.read_bytes())
        require(actual == EXPECTED_GIT_BLOBS[path.name], f"exact repository blob {path.name} = {actual}")

    require(
        EXPECTED_GIT_BLOBS[OFFICIAL.name] != EXPECTED_GIT_BLOBS[CANDIDATE.name],
        "V2.2-named official-route service blob and V2.3-named candidate blob are provenance-distinct",
    )

    official_tree = etree.parse(str(OFFICIAL))
    candidate_tree = etree.parse(str(CANDIDATE))
    enum_tree = etree.parse(str(ENUMS))

    expected_includes = [COMMON.name, ENUMS.name]
    require(
        official_tree.xpath("/xs:schema/xs:include/@schemaLocation", namespaces=NS) == expected_includes,
        "official V2.3 release route service file includes Common V2.2 + Enumerations V2.2",
    )
    require(
        candidate_tree.xpath("/xs:schema/xs:include/@schemaLocation", namespaces=NS) == expected_includes,
        "candidate V2.3-named file currently includes the same V2.2 dependencies",
    )

    compile_family(OFFICIAL)
    print(f"OK  compiled official-route family via {OFFICIAL.name}")
    compile_family(CANDIDATE)
    print(f"OK  compiled candidate/integration family via {CANDIDATE.name}")

    official_sig = critical_signature(official_tree)
    candidate_sig = critical_signature(candidate_tree)
    require(
        candidate_sig == official_sig,
        "candidate and official-route files currently match for TVS critical declarations despite distinct provenance/blobs",
    )

    require(
        official_sig["route_deviation_type"] == "RouteDeviationEnumeration",
        "official-route VehicleData.RouteDeviation type is RouteDeviationEnumeration",
    )
    require(
        official_sig["current_trip_ref_type"] == "IBIS-IP.NMTOKEN",
        "official-route CurrentTripRef type is IBIS-IP.NMTOKEN",
    )
    require(
        official_sig["current_line_type"] == "TicketValidationService.CurrentLineDataStructure",
        "official-route CurrentLineData exact type is TicketValidationService.CurrentLineDataStructure",
    )

    global_elements = set(official_sig["global_elements"])
    complex_types = set(official_sig["complex_types"])
    require(
        "TicketValidationService.GetCurrentTariffStopResponse" in global_elements,
        "official-route GetCurrentTariffStopResponse global root exists",
    )
    require(
        "TicketValidationService.GetCurrentStopPointResponse" not in global_elements,
        "stale GetCurrentStopPointResponse is absent from official-route global roots",
    )
    require(
        "TicketValidationService.CurrentTariffStopDataStructure" in complex_types,
        "official-route CurrentTariffStopDataStructure exists",
    )
    require(
        "TicketValidationService.CurrentStopPointDataStructure" not in complex_types,
        "stale CurrentStopPointDataStructure is absent from official-route complex types",
    )

    deviation_values = enum_tree.xpath(
        "//xs:simpleType[@name='RouteDeviationEnumeration']/xs:restriction/xs:enumeration/@value",
        namespaces=NS,
    )
    direction_values = enum_tree.xpath(
        "//xs:simpleType[@name='RouteDirectionEnumeration']/xs:restriction/xs:enumeration/@value",
        namespaces=NS,
    )
    require(deviation_values == ["onroute", "offroute", "unknown"], "official-route RouteDeviationEnumeration value set is exact")
    require(direction_values == ["Forward", "Backward", "Clockwise", "Counterclockwise", "Other"], "official-route RouteDirectionEnumeration value set is exact")

    deviation_probe = compile_probe(OFFICIAL, '  <xs:element name="EV114.RouteDeviation" type="RouteDeviationEnumeration"/>')
    validate_text(deviation_probe, "EV114.RouteDeviation", "onroute", True)
    validate_text(deviation_probe, "EV114.RouteDeviation", "Forward", False)

    official_schema = compile_family(OFFICIAL)
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
    validate_xml(official_schema, valid_new_root, True, "official-route GetCurrentTariffStopResponse sample")
    validate_xml(official_schema, stale_old_root, False, "stale GetCurrentStopPointResponse sample")

    print("PASSED: EV-114 TVS V2.3 official-route/candidate authority guard confirmed")
    print("NOTE: provenance authority is not inferred from semantic equality; official release routing remains external/tag evidence.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
