#!/usr/bin/env python3
"""EV-125: CIS legacy finding revalidation executable evidence."""
from __future__ import annotations

import hashlib
import os
import tempfile
from pathlib import Path

from lxml import etree

XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}
ROOT = Path(__file__).resolve().parents[1]
HIST = Path(os.environ["CIS_V11_DIR"])


class EvidenceError(RuntimeError):
    pass


def need(value: bool, message: str) -> None:
    if not value:
        raise EvidenceError(message)
    print("OK ", message)


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def expect_blob(path: Path, sha: str, label: str) -> None:
    need(git_blob_sha(path) == sha, f"{label} blob={sha}")


def parse(path: Path):
    return etree.parse(str(path)).getroot()


def group(root, name: str):
    node = root.find(f"xs:group[@name='{name}']", NS)
    if node is None:
        raise EvidenceError(f"missing group {name}")
    return node


def ctype(root, name: str):
    node = root.find(f"xs:complexType[@name='{name}']", NS)
    if node is None:
        raise EvidenceError(f"missing complexType {name}")
    return node


def elem_in(node, name: str):
    return node.find(f".//xs:element[@name='{name}']", NS)


def occurs(node, key: str) -> str:
    return node.get(key, "1")


def globals_(root) -> set[str | None]:
    return {node.get("name") for node in root.findall("xs:element", NS)}


def compile_schema(path: Path):
    schema = etree.XMLSchema(etree.parse(str(path)))
    print("OK ", path.name, "compiled")
    return schema


def validate(schema, label: str, xml: str, want: bool) -> None:
    document = etree.fromstring(xml.encode())
    got = bool(schema.validate(document))
    if got != want:
        raise EvidenceError(
            f"{label}: got {got}, expected {want}; {schema.error_log.last_error}"
        )
    print("OK ", label, "VALID" if got else "INVALID")


def includes(root) -> list[str | None]:
    return [node.get("schemaLocation") for node in root.findall("xs:include", NS)]


def historical_v11() -> None:
    service = HIST / "IBIS-IP_CustomerInformationService_V1.1.xsd"
    common = HIST / "IBIS-IP_common_V1.1.xsd"
    enums = HIST / "IBIS-IP_Enumerations_V1.1.xsd"
    expect_blob(service, "5957e27f128a191c794b0c8081b531a07126784a", "historical working CIS V1.1")
    expect_blob(common, "bdf839813b4b19dd000a32a684ce985878adaca9", "historical working Common V1.1")
    expect_blob(enums, "5a9957a6931be2e4460665f8a52c76765fbfbcde", "historical working Enumerations V1.1")

    root = parse(service)
    need(
        includes(root)
        == ["IBIS-IP_common_V1.1.xsd", "IBIS-IP_Enumerations_V1.1.xsd"],
        "V1.1 working service includes exact V1.1 dependencies",
    )
    vehicle_group = group(root, "VehicleInformationGroup")
    need(elem_in(vehicle_group, "SpeakerActive") is None, "V1.1 working VehicleInformationGroup lacks SpeakerActive")
    need(elem_in(vehicle_group, "StopInformationActive") is None, "V1.1 working VehicleInformationGroup lacks StopInformationActive")
    compile_schema(service)

    harness = HIST / "_ev125_v11_harness.xsd"
    harness.write_text(
        f'<xs:schema xmlns:xs="{XS}" elementFormDefault="qualified">'
        f'<xs:include schemaLocation="{service.name}"/>'
        '<xs:element name="V" type="CustomerInformationService.VehicleData"/>'
        "</xs:schema>",
        encoding="utf-8",
    )
    try:
        schema = compile_schema(harness)
        base = (
            "<TimeStamp><Value>2026-01-01T00:00:00Z</Value></TimeStamp>"
            "<VehicleRef><Value>V1</Value></VehicleRef>"
            "<RouteDeviation>onroute</RouteDeviation>"
        )
        validate(schema, "V1.1 working base VehicleData", f"<V>{base}</V>", True)
        validate(
            schema,
            "V1.1 working SpeakerActive rejected",
            f"<V>{base}<SpeakerActive><Value>true</Value></SpeakerActive></V>",
            False,
        )
        validate(
            schema,
            "V1.1 working StopInformationActive rejected",
            f"<V>{base}<StopInformationActive><Value>true</Value></StopInformationActive></V>",
            False,
        )
    finally:
        harness.unlink(missing_ok=True)


FAMILIES = {
    "2.0": (
        "IBIS-IP_CustomerInformationService_V2.0.xsd",
        "fa8f0a51ad5f612660c9532c8557ad1ca473a908",
        "IBIS-IP_common_V2.0.xsd",
        "8608e3dcd665c197c34da7f6ec6af5a3758da164",
        "IBIS-IP_Enumerations_V2.0.xsd",
        "27e3c183b00381d959622d13c10543123af8eef6",
    ),
    "2.2": (
        "IBIS-IP_CustomerInformationService_V2.2.xsd",
        "ddc70ed9d6238f1377be1d7728ff46b36a22ee1e",
        "IBIS-IP_common_V2.2.xsd",
        "468fee6d177e7185dbcd5d3f90cfb114e29e01ae",
        "IBIS-IP_Enumerations_V2.2.xsd",
        "2a23b512379b18e8f122ac1272cef8229fb86283",
    ),
    "2.3": (
        "IBIS-IP_CustomerInformationService_V2.3.xsd",
        "bf921c857a3abfcbe9c6c24fe525d6cc7d2d399e",
        "IBIS-IP_common_V2.3.xsd",
        "0d8926c4063c12de9a5e68b6f0addaab35a55dc1",
        "IBIS-IP_Enumerations_V2.2.xsd",
        "2a23b512379b18e8f122ac1272cef8229fb86283",
    ),
}


def current_family(version: str) -> None:
    service_file, service_sha, common_file, common_sha, enum_file, enum_sha = FAMILIES[version]
    service = ROOT / service_file
    common = ROOT / common_file
    enums = ROOT / enum_file
    expect_blob(service, service_sha, f"CIS V{version}")
    expect_blob(common, common_sha, f"Common dependency for CIS V{version}")
    expect_blob(enums, enum_sha, f"Enumerations dependency for CIS V{version}")

    root = parse(service)
    need(includes(root) == [common_file, enum_file], f"CIS V{version} exact dependency route")
    schema = compile_schema(service)

    operation_group = group(root, "CustomerInformationServiceOperations")
    operation_names = [node.get("name") or "" for node in operation_group.findall(".//xs:element", NS)]
    need(
        not any("Subscribe" in name or "Unsubscribe" in name for name in operation_names),
        f"CIS V{version} operation group has no service-specific Subscribe/Unsubscribe roots",
    )
    common_root = parse(common)
    for name in (
        "SubscribeRequestStructure",
        "SubscribeResponseStructure",
        "UnsubscribeRequestStructure",
        "UnsubscribeResponseStructure",
    ):
        need(ctype(common_root, name) is not None, f"Common route exposes generic {name}")

    global_names = globals_(root)
    correct_connection = "CustomerInformationService.GetCurrentConnectionInformationResponse"
    pdf_connection = "CustomerInformationService.GetCurrentConnectionResponse"
    need(
        correct_connection in global_names and pdf_connection not in global_names,
        f"CIS V{version} exact current-connection root naming",
    )
    connection_data = (
        "<CurrentConnectionData>"
        "<TimeStamp><Value>2026-01-01T00:00:00Z</Value></TimeStamp>"
        "</CurrentConnectionData>"
    )
    validate(
        schema,
        f"CIS V{version} correct current-connection root",
        f"<{correct_connection}>{connection_data}</{correct_connection}>",
        True,
    )
    validate(
        schema,
        f"CIS V{version} PDF short current-connection root",
        f"<{pdf_connection}>{connection_data}</{pdf_connection}>",
        False,
    )

    correct_retrieve = "CustomerInformationService.RetrievePartialStopSequenceRequest"
    pdf_retrieve = "CustomerInformationService.RetrievePartialStopRequest"
    need(
        correct_retrieve in global_names and pdf_retrieve not in global_names,
        f"CIS V{version} exact retrieve root naming",
    )
    request_body = (
        "<StartingStopIndex><Value>1</Value></StartingStopIndex>"
        "<NumberOfStopPoints><Value>1</Value></NumberOfStopPoints>"
    )
    validate(schema, f"CIS V{version} correct retrieve root", f"<{correct_retrieve}>{request_body}</{correct_retrieve}>", True)
    validate(schema, f"CIS V{version} PDF short retrieve root", f"<{pdf_retrieve}>{request_body}</{pdf_retrieve}>", False)

    all_data = ctype(root, "CustomerInformationService.AllData")
    trip_information = elem_in(all_data, "TripInformation")
    need(trip_information is not None and occurs(trip_information, "maxOccurs") == "2", f"CIS V{version} AllData.TripInformation maxOccurs=2")
    vehicle_group = group(root, "VehicleInformationGroup")
    if version == "2.0":
        need(occurs(trip_information, "minOccurs") == "1", "CIS V2.0 AllData.TripInformation required")
        need(elem_in(all_data, "GlobalDisplayContent") is None, "CIS V2.0 GlobalDisplayContent absent")
        need(elem_in(vehicle_group, "MyOwnVehicleMode") is None, "CIS V2.0 MyOwnVehicleMode absent")
        need(elem_in(vehicle_group, "TripState") is None, "CIS V2.0 TripState absent")
    else:
        need(occurs(trip_information, "minOccurs") == "0", f"CIS V{version} AllData.TripInformation optional")
        global_display = elem_in(all_data, "GlobalDisplayContent")
        need(
            global_display is not None
            and occurs(global_display, "minOccurs") == "0"
            and occurs(global_display, "maxOccurs") == "unbounded",
            f"CIS V{version} GlobalDisplayContent 0:*",
        )
        own_mode = elem_in(vehicle_group, "MyOwnVehicleMode")
        need(own_mode is not None and own_mode.get("type") == "NetexMode", f"CIS V{version} MyOwnVehicleMode type=NetexMode")
        need(elem_in(vehicle_group, "TripState") is not None, f"CIS V{version} TripState present")
        with tempfile.NamedTemporaryFile("w", suffix=".xsd", dir=ROOT, delete=False, encoding="utf-8") as stream:
            harness = Path(stream.name)
            stream.write(
                f'<xs:schema xmlns:xs="{XS}" elementFormDefault="qualified">'
                f'<xs:include schemaLocation="{common_file}"/>'
                '<xs:element name="Mode" type="NetexMode"/>'
                "</xs:schema>"
            )
        try:
            mode_schema = compile_schema(harness)
            validate(
                mode_schema,
                f"CIS V{version} NetexMode structured value",
                "<Mode><PtMainMode>RailSubmode</PtMainMode><RailSubmode>local</RailSubmode></Mode>",
                True,
            )
            validate(mode_schema, f"CIS V{version} scalar PtModes-like value rejected", "<Mode>bus</Mode>", False)
        finally:
            harness.unlink(missing_ok=True)

    connection_type = ctype(root, "CustomerInformationService.CurrentConnectionInformationData")
    current_connection = elem_in(connection_type, "CurrentConnection")
    need(
        occurs(current_connection, "minOccurs") == "0" and occurs(current_connection, "maxOccurs") == "unbounded",
        f"CIS V{version} CurrentConnection 0:*",
    )
    display_type = ctype(root, "CustomerInformationService.CurrentDisplayContentData")
    current_display = elem_in(display_type, "CurrentDisplayContent")
    need(
        occurs(current_display, "minOccurs") == "1" and occurs(current_display, "maxOccurs") == "unbounded",
        f"CIS V{version} CurrentDisplayContent 1:*",
    )


def main() -> int:
    try:
        historical_v11()
        for version in ("2.0", "2.2", "2.3"):
            current_family(version)
    except (OSError, etree.XMLSyntaxError, etree.XMLSchemaParseError, EvidenceError) as error:
        print("FAILED: EV-125 CIS revalidation:", error)
        return 1
    print("PASSED: EV-125 CIS V1.1 historical-working provenance and V2.0/V2.2/V2.3 executable boundaries confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
