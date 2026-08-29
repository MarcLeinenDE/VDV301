#!/usr/bin/env python3
"""EV-111: DoorStateService V2.1 executable evidence.

Covers:
- DRS-002: RetrieveSpecific response error branch uses ErrorMessage in the exact XSD,
  not the PDF's OperationErrorMessage.
- DRS-003: the exact Get*Request declarations have no explicit type; XML Schema
  therefore gives them xs:anyType semantics. A probe schema reuses the exact
  declaration form to demonstrate that both an empty request and arbitrary
  unexpected child content validate.

No normative XSD is modified.
"""
from __future__ import annotations

from pathlib import Path
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
DOOR_XSD = ROOT / "IBIS-IP_DoorStateService_V2.1.xsd"
XS = "http://www.w3.org/2001/XMLSchema"


def validate(schema: etree.XMLSchema, xml: str, expected: bool, label: str) -> int:
    doc = etree.fromstring(xml.encode("utf-8"))
    actual = bool(schema.validate(doc))
    if actual == expected:
        print(f"OK  {label} -> {'valid' if actual else 'invalid'}")
        if not actual and schema.error_log.last_error is not None:
            print(f"    evidence: {schema.error_log.last_error}")
        return 0
    print(f"ERR {label}: expected {'valid' if expected else 'invalid'}, got {'valid' if actual else 'invalid'}")
    if schema.error_log.last_error is not None:
        print(f"    evidence: {schema.error_log.last_error}")
    return 1


def assert_untyped_local_request(name: str) -> None:
    doc = etree.parse(str(DOOR_XSD))
    found = doc.xpath(
        f"//xs:group[@name='DoorStateServiceGroup']//xs:element[@name='{name}']",
        namespaces={"xs": XS},
    )
    if len(found) != 1:
        raise SystemExit(f"expected exactly one local declaration for {name}, found {len(found)}")
    elem = found[0]
    if "type" in elem.attrib:
        raise SystemExit(f"{name} unexpectedly has explicit type={elem.attrib['type']}")
    if elem.find(f"{{{XS}}}complexType") is not None or elem.find(f"{{{XS}}}simpleType") is not None:
        raise SystemExit(f"{name} unexpectedly has an inline type")
    print(f"OK  exact declaration {name}: no explicit/inline type -> xs:anyType default semantics")


def build_probe_schema() -> etree.XMLSchema:
    # The include is resolved relative to the repository root via base_url.
    # The two response probes reference exact normative DoorState complex types.
    # The two request probes reproduce the exact original declaration form
    # (<xs:element name='...'/>) at global scope so its default-type semantics can
    # be exercised without changing the source XSD or constructing every member
    # of the service's all-operations sequence.
    probe = f'''<?xml version="1.0"?>
<xs:schema xmlns:xs="{XS}" elementFormDefault="qualified" attributeFormDefault="unqualified">
  <xs:include schemaLocation="IBIS-IP_DoorStateService_V2.1.xsd"/>
  <xs:element name="ProbeRetrieveOpenResponse" type="DoorStateService.RetrieveSpecificDoorOpenStateResponseStructure"/>
  <xs:element name="ProbeRetrieveOperationResponse" type="DoorStateService.RetrieveSpecificDoorOperationStateResponseStructure"/>
  <xs:element name="DoorStateService.GetDoorOpenStatesRequest"/>
  <xs:element name="DoorStateService.GetDoorOperationStatesRequest"/>
</xs:schema>'''
    base_url = (ROOT / "EV111_DoorState_probe.xsd").as_uri()
    tree = etree.ElementTree(etree.fromstring(probe.encode("utf-8"), base_url=base_url))
    return etree.XMLSchema(tree)


def error_branch(root: str, element_name: str) -> str:
    return f'''<{root}>
  <{element_name}><Value>diagnostic</Value></{element_name}>
</{root}>'''


def request(root: str, extra: bool) -> str:
    if not extra:
        return f"<{root}/>"
    return f'''<{root}>
  <UnexpectedPayload>
    <Nested>accepted-by-anyType</Nested>
  </UnexpectedPayload>
</{root}>'''


def main() -> int:
    # Compile exact source schema first to prove the selected family is coherent.
    etree.XMLSchema(etree.parse(str(DOOR_XSD)))
    print(f"OK  compiled exact {DOOR_XSD.name}")

    for name in (
        "DoorStateService.GetDoorOpenStatesRequest",
        "DoorStateService.GetDoorOperationStatesRequest",
    ):
        assert_untyped_local_request(name)

    schema = build_probe_schema()
    print("OK  compiled EV-111 probe schema against exact DoorState V2.1 types/declarations")
    failures = 0

    for root in ("ProbeRetrieveOpenResponse", "ProbeRetrieveOperationResponse"):
        failures += validate(schema, error_branch(root, "ErrorMessage"), True,
                             f"{root} exact-XSD <ErrorMessage> branch")
        failures += validate(schema, error_branch(root, "OperationErrorMessage"), False,
                             f"{root} PDF-shaped <OperationErrorMessage> branch")

    for root in (
        "DoorStateService.GetDoorOpenStatesRequest",
        "DoorStateService.GetDoorOperationStatesRequest",
    ):
        failures += validate(schema, request(root, False), True,
                             f"{root} empty request")
        failures += validate(schema, request(root, True), True,
                             f"{root} arbitrary unexpected child content under xs:anyType")

    if failures:
        print(f"FAILED: {failures} EV-111 check(s) did not match expectation")
        return 1
    print("PASSED: EV-111 DoorState V2.1 DRS-002/DRS-003 executable behaviour confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
