#!/usr/bin/env python3
"""Executable evidence for EV-104 TrainSet modelling findings.

TSM-002 is tested as an actual V2.2 operation-group/global-root mismatch.
TSD-003 is tested as dual typing by context: the operation group binds the
Subscribe*Response names to SubscribeResponseStructure while the global roots
bind the same names to the corresponding Retrieve*ResponseStructure.

No schema is changed by this harness.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}


def parse_xsd(name: str) -> etree._ElementTree:
    return etree.parse(str(ROOT / name))


def compile_xsd(name: str) -> etree.XMLSchema:
    return etree.XMLSchema(parse_xsd(name))


def validate(schema: etree.XMLSchema, xml: str, expected: bool, label: str) -> bool:
    doc = etree.fromstring(xml.encode("utf-8"))
    actual = bool(schema.validate(doc))
    if actual == expected:
        print(f"OK  {label} (expected {'valid' if expected else 'invalid'})")
        if not actual and schema.error_log.last_error is not None:
            print(f"    evidence: {schema.error_log.last_error}")
        return True
    print(f"ERR {label}: expected {'valid' if expected else 'invalid'}, got {'valid' if actual else 'invalid'}")
    if schema.error_log.last_error is not None:
        print(f"    {schema.error_log.last_error}")
    return False


def temp_harness(include_name: str, body: str) -> tuple[tempfile.TemporaryDirectory, Path]:
    tmp = tempfile.TemporaryDirectory(prefix="vdv301_ev104_")
    tmp_path = Path(tmp.name)
    for xsd in ROOT.glob("*.xsd"):
        target = tmp_path / xsd.name
        try:
            target.symlink_to(xsd.resolve())
        except OSError:
            target.write_bytes(xsd.read_bytes())
    harness = tmp_path / "harness.xsd"
    harness.write_text(
        f'''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="{XS}" elementFormDefault="qualified" attributeFormDefault="unqualified">
  <xs:include schemaLocation="{include_name}"/>
  {body}
</xs:schema>
''',
        encoding="utf-8",
    )
    return tmp, harness


def management_composition_element(name: str) -> str:
    return f'''<{name}>
    <SingleCoach>
      <CoachNumber><Value>coach-1</Value></CoachNumber>
      <FrontCabin><Value>A</Value></FrontCabin>
      <RearCabin><Value>B</Value></RearCabin>
      <CoachPositionInTrainSet><Value>1</Value></CoachPositionInTrainSet>
      <CoachState>Master</CoachState>
    </SingleCoach>
  </{name}>'''


def management_group_payload(last_name: str) -> str:
    return f'''<TestTrainSetManagementOperations>
  <TrainSetManagementService.SetSlaveModeRequest>
    <CoachNumberOfMaster><Value>coach-1</Value></CoachNumberOfMaster>
  </TrainSetManagementService.SetSlaveModeRequest>
  <TrainSetManagementService.SetSlaveModeResponse>
    <OperationErrorMessage><Value>example</Value></OperationErrorMessage>
  </TrainSetManagementService.SetSlaveModeResponse>
  <TrainSetManagementService.SetNeutralModeRequest/>
  <TrainSetManagementService.SetNeutralModeResponse>
    <OperationErrorMessage><Value>example</Value></OperationErrorMessage>
  </TrainSetManagementService.SetNeutralModeResponse>
  {management_composition_element(last_name)}
</TestTrainSetManagementOperations>'''


def run_tsm002() -> int:
    failures = 0
    filename = "IBIS-IP_TrainSetManagementService_V2.2.xsd"
    tree = parse_xsd(filename)
    schema = etree.XMLSchema(tree)
    print("\nTSM-002 - TrainSetManagementService V2.2")
    print(f"OK  compiled {filename}")

    global_elements = {
        node.get("name"): node.get("type")
        for node in tree.xpath("/xs:schema/xs:element", namespaces=NS)
    }
    group_elements = {
        node.get("name"): node.get("type")
        for node in tree.xpath(
            "/xs:schema/xs:group[@name='TrainSetManagementServiceOperations']//xs:element",
            namespaces=NS,
        )
    }

    checks = [
        ("TrainSetManagementService.GetTrainSetCompositionResponse" in global_elements,
         "corrected GetTrainSetCompositionResponse exists as global root"),
        ("TrainSetManagementService.GetTrainSetComposition" not in global_elements,
         "stale GetTrainSetComposition does not exist as global root"),
        ("TrainSetManagementService.GetTrainSetComposition" in group_elements,
         "operation group still contains stale GetTrainSetComposition"),
        ("TrainSetManagementService.GetTrainSetCompositionResponse" not in group_elements,
         "operation group does not contain corrected GetTrainSetCompositionResponse"),
    ]
    for ok, label in checks:
        print(("OK  " if ok else "ERR ") + label)
        failures += 0 if ok else 1

    corrected_global = management_composition_element(
        "TrainSetManagementService.GetTrainSetCompositionResponse"
    )
    if not validate(schema, corrected_global, True, "corrected global response root validates"):
        failures += 1

    stale_global = management_composition_element(
        "TrainSetManagementService.GetTrainSetComposition"
    )
    if not validate(schema, stale_global, False, "stale old name is not a global response root"):
        failures += 1

    tmp, harness_path = temp_harness(
        filename,
        '''<xs:element name="TestTrainSetManagementOperations">
  <xs:complexType>
    <xs:group ref="TrainSetManagementServiceOperations"/>
  </xs:complexType>
</xs:element>''',
    )
    try:
        group_schema = etree.XMLSchema(etree.parse(str(harness_path)))
        print("OK  operation-group harness compiled")
        if not validate(
            group_schema,
            management_group_payload("TrainSetManagementService.GetTrainSetComposition"),
            True,
            "operation group accepts stale old composition element name",
        ):
            failures += 1
        if not validate(
            group_schema,
            management_group_payload("TrainSetManagementService.GetTrainSetCompositionResponse"),
            False,
            "operation group rejects corrected composition response name",
        ):
            failures += 1
    finally:
        tmp.cleanup()

    if failures == 0:
        print("PASSED: TSM-002 executable operation-group/global-root mismatch confirmed")
    return failures


def run_tsd003() -> int:
    failures = 0
    filename = "IBIS-IP_TrainSetDataService_V2.2.xsd"
    tree = parse_xsd(filename)
    schema = etree.XMLSchema(tree)
    print("\nTSD-003 - TrainSetDataService V2.2")
    print(f"OK  compiled {filename}")

    global_elements = {
        node.get("name"): node.get("type")
        for node in tree.xpath("/xs:schema/xs:element", namespaces=NS)
    }
    group_elements = {
        node.get("name"): node.get("type")
        for node in tree.xpath(
            "/xs:schema/xs:group[@name='TrainSetDataServiceOperations']//xs:element",
            namespaces=NS,
        )
    }

    expected = {
        "TrainSetDataService.SubscribeTripRefResponse": (
            "TrainSetDataService.RetrieveTripRefResponseStructure",
            "SubscribeResponseStructure",
        ),
        "TrainSetDataService.SubscribeTripInformationResponse": (
            "TrainSetDataService.RetrieveTripInformationResponseStructure",
            "SubscribeResponseStructure",
        ),
    }

    for name, (global_type, group_type) in expected.items():
        ok_global = global_elements.get(name) == global_type
        ok_group = group_elements.get(name) == group_type
        print(("OK  " if ok_global else "ERR ") + f"global {name} -> {global_elements.get(name)!r}")
        print(("OK  " if ok_group else "ERR ") + f"group  {name} -> {group_elements.get(name)!r}")
        failures += 0 if ok_global else 1
        failures += 0 if ok_group else 1

    data_event = '''<TrainSetDataService.SubscribeTripRefResponse>
  <TripRef><Value>trip-1</Value></TripRef>
</TrainSetDataService.SubscribeTripRefResponse>'''
    if not validate(schema, data_event, True, "global SubscribeTripRefResponse accepts Retrieve-style data event"):
        failures += 1

    ack_as_global_ref = '''<TrainSetDataService.SubscribeTripRefResponse>
  <Active><Value>true</Value></Active>
</TrainSetDataService.SubscribeTripRefResponse>'''
    if not validate(schema, ack_as_global_ref, False, "global SubscribeTripRefResponse rejects generic Subscribe acknowledgement"):
        failures += 1

    ack_as_global_info = '''<TrainSetDataService.SubscribeTripInformationResponse>
  <Active><Value>true</Value></Active>
</TrainSetDataService.SubscribeTripInformationResponse>'''
    if not validate(schema, ack_as_global_info, False, "global SubscribeTripInformationResponse rejects generic Subscribe acknowledgement"):
        failures += 1

    tmp, harness_path = temp_harness(
        filename,
        '''<xs:element name="TestTripRefSubscribeAcknowledgement" type="SubscribeResponseStructure"/>
<xs:element name="TestTripInformationSubscribeAcknowledgement" type="SubscribeResponseStructure"/>''',
    )
    try:
        ack_schema = etree.XMLSchema(etree.parse(str(harness_path)))
        print("OK  generic SubscribeResponseStructure acknowledgement harness compiled")
        ack_ref = '''<TestTripRefSubscribeAcknowledgement>
  <Active><Value>true</Value></Active>
</TestTripRefSubscribeAcknowledgement>'''
        ack_info = '''<TestTripInformationSubscribeAcknowledgement>
  <Active><Value>true</Value></Active>
</TestTripInformationSubscribeAcknowledgement>'''
        if not validate(ack_schema, ack_ref, True, "SubscribeResponseStructure accepts TripRef immediate acknowledgement shape"):
            failures += 1
        if not validate(ack_schema, ack_info, True, "SubscribeResponseStructure accepts TripInformation immediate acknowledgement shape"):
            failures += 1
    finally:
        tmp.cleanup()

    if failures == 0:
        print("PASSED: TSD-003 dual response typing by context confirmed")
        print("NOTE: evidence supports contextual modelling / resolver requirement, not an automatic XSD defect classification")
    return failures


def main() -> int:
    failures = run_tsm002() + run_tsd003()
    if failures:
        print(f"\nFAILED: {failures} EV-104 check(s) did not match expectation")
        return 1
    print("\nPASSED: EV-104 TrainSet evidence completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
