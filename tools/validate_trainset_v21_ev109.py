#!/usr/bin/env python3
"""EV-109: executable evidence for TrainSet V2.1 deep-read findings.

Confirms against the exact stored official V2.1 service schemas:
- TSI-001: GetTrainSetCompositionResponse models one flat coach record and
  cannot carry the PDF-described sequence of multiple coach records.
- TSM-001: V2.1 exposes TrainSetManagementService.GetTrainSetComposition
  as the global response payload root; the later ...Response name does not
  exist in V2.1.
- TSD-001: the V2.1 TrainSetDataService service schema exposes only Retrieve
  operations; the PDF-described Subscribe/Unsubscribe service operations are
  absent even though generic Common subscription structures exist.

No schema is changed by this harness.
"""
from __future__ import annotations

from pathlib import Path
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}


def parse(name: str) -> etree._ElementTree:
    return etree.parse(str(ROOT / name))


def compile_schema(name: str) -> etree.XMLSchema:
    return etree.XMLSchema(parse(name))


def validate(schema: etree.XMLSchema, xml: str, expected: bool, label: str) -> bool:
    node = etree.fromstring(xml.encode("utf-8"))
    actual = bool(schema.validate(node))
    if actual == expected:
        print(f"OK  {label} (expected {'valid' if expected else 'invalid'})")
        if not actual and schema.error_log.last_error is not None:
            print(f"    evidence: {schema.error_log.last_error}")
        return True
    print(f"ERR {label}: expected {'valid' if expected else 'invalid'}, got {'valid' if actual else 'invalid'}")
    if schema.error_log.last_error is not None:
        print(f"    {schema.error_log.last_error}")
    return False


def coach_fields(number: str, position: int, state: str) -> str:
    return f'''<CoachNumber><Value>{number}</Value></CoachNumber>
  <FrontCabin><Value>A</Value></FrontCabin>
  <RearCabin><Value>B</Value></RearCabin>
  <CoachPositionInTrainSet><Value>{position}</Value></CoachPositionInTrainSet>
  <CoupledSide>A</CoupledSide>
  <CoachState>{state}</CoachState>'''


def run_tsi001() -> int:
    failures = 0
    filename = "IBIS-IP_TrainSetInformationService_V2.1.xsd"
    tree = parse(filename)
    schema = etree.XMLSchema(tree)
    print("\nTSI-001 - TrainSetInformationService V2.1")
    print(f"OK  compiled {filename}")

    seq = tree.xpath(
        "/xs:schema/xs:complexType[@name='TrainSetInformationService.GetTrainSetCompositionResponseStructure']/xs:sequence",
        namespaces=NS,
    )
    if not seq:
        print("ERR response structure sequence not found")
        failures += 1
    else:
        elems = seq[0].xpath("./xs:element", namespaces=NS)
        names = [e.get("name") for e in elems]
        repeated = [e.get("name") for e in elems if e.get("maxOccurs", "1") not in ("1", None)]
        expected_names = [
            "CoachType", "CoachNumber", "FrontCabin", "RearCabin",
            "CoachPositionInTrainSet", "CoupledSide", "CoachState",
        ]
        ok_names = names == expected_names
        ok_flat = not repeated and all(e.get("maxOccurs", "1") == "1" for e in elems)
        print(("OK  " if ok_names else "ERR ") + f"flat coach-field order = {names}")
        print(("OK  " if ok_flat else "ERR ") + "no repeated coach wrapper / no repeated coach field in response structure")
        failures += 0 if ok_names else 1
        failures += 0 if ok_flat else 1

    one = f'''<TrainSetInformationService.GetTrainSetCompositionResponse>
  {coach_fields("coach-1", 1, "Master")}
</TrainSetInformationService.GetTrainSetCompositionResponse>'''
    if not validate(schema, one, True, "one flat coach record validates"):
        failures += 1

    two = f'''<TrainSetInformationService.GetTrainSetCompositionResponse>
  {coach_fields("coach-1", 1, "Master")}
  {coach_fields("coach-2", 2, "Slave")}
</TrainSetInformationService.GetTrainSetCompositionResponse>'''
    if not validate(schema, two, False, "second PDF-described coach record is rejected"):
        failures += 1

    if failures == 0:
        print("PASSED: TSI-001 V2.1 multi-coach modelling limitation executable-confirmed")
    return failures


def run_tsm001() -> int:
    failures = 0
    filename = "IBIS-IP_TrainSetManagementService_V2.1.xsd"
    tree = parse(filename)
    schema = etree.XMLSchema(tree)
    print("\nTSM-001 - TrainSetManagementService V2.1")
    print(f"OK  compiled {filename}")

    globals_ = {
        n.get("name"): n.get("type")
        for n in tree.xpath("/xs:schema/xs:element", namespaces=NS)
    }
    group = {
        n.get("name"): n.get("type")
        for n in tree.xpath(
            "/xs:schema/xs:group[@name='TrainSetManagementServiceOperations']//xs:element",
            namespaces=NS,
        )
    }
    old = "TrainSetManagementService.GetTrainSetComposition"
    corrected = "TrainSetManagementService.GetTrainSetCompositionResponse"
    expected_type = "TrainSetInformationService.GetTrainSetCompositionResponseStructure"

    checks = [
        (globals_.get(old) == expected_type, f"global V2.1 root {old} -> {globals_.get(old)!r}"),
        (corrected not in globals_, f"later corrected root {corrected} absent globally in V2.1"),
        (group.get(old) == expected_type, f"V2.1 operation group uses {old}"),
        (corrected not in group, f"later corrected root absent from V2.1 operation group"),
    ]
    for ok, label in checks:
        print(("OK  " if ok else "ERR ") + label)
        failures += 0 if ok else 1

    old_xml = f'''<{old}>
  {coach_fields("coach-1", 1, "Master")}
</{old}>'''
    if not validate(schema, old_xml, True, "V2.1 old-name composition payload root validates"):
        failures += 1

    corrected_xml = f'''<{corrected}>
  {coach_fields("coach-1", 1, "Master")}
</{corrected}>'''
    if not validate(schema, corrected_xml, False, "later corrected ...Response root is not a V2.1 global root"):
        failures += 1

    if failures == 0:
        print("PASSED: TSM-001 V2.1 response-root naming discrepancy executable-confirmed")
    return failures


def run_tsd001() -> int:
    failures = 0
    filename = "IBIS-IP_TrainSetDataService_V2.1.xsd"
    tree = parse(filename)
    etree.XMLSchema(tree)
    print("\nTSD-001 - TrainSetDataService V2.1")
    print(f"OK  compiled {filename}")

    group_names = {
        n.get("name")
        for n in tree.xpath(
            "/xs:schema/xs:group[@name='TrainSetDataServiceOperations']//xs:element",
            namespaces=NS,
        )
    }
    global_names = {
        n.get("name")
        for n in tree.xpath("/xs:schema/xs:element", namespaces=NS)
    }
    expected_retrieve = {
        "TrainSetDataService.RetrieveTripRefRequest",
        "TrainSetDataService.RetrieveTripRefResponse",
        "TrainSetDataService.RetrieveTripInformationRequest",
        "TrainSetDataService.RetrieveTripInformationResponse",
    }
    missing_service_subscription = {
        "TrainSetDataService.SubscribeTripRefRequest",
        "TrainSetDataService.SubscribeTripRefResponse",
        "TrainSetDataService.UnsubscribeTripRefRequest",
        "TrainSetDataService.UnsubscribeTripRefResponse",
        "TrainSetDataService.SubscribeTripInformationRequest",
        "TrainSetDataService.SubscribeTripInformationResponse",
        "TrainSetDataService.UnsubscribeTripInformationRequest",
        "TrainSetDataService.UnsubscribeTripInformationResponse",
    }

    ok_retrieve_group = expected_retrieve <= group_names
    ok_retrieve_global = expected_retrieve <= global_names
    ok_sub_group_absent = not (missing_service_subscription & group_names)
    ok_sub_global_absent = not (missing_service_subscription & global_names)
    for ok, label in [
        (ok_retrieve_group, "all four Retrieve request/response members exist in V2.1 operation group"),
        (ok_retrieve_global, "all four Retrieve request/response roots exist globally"),
        (ok_sub_group_absent, "PDF-described service-specific Subscribe/Unsubscribe members are absent from V2.1 operation group"),
        (ok_sub_global_absent, "PDF-described service-specific Subscribe/Unsubscribe roots are absent globally in V2.1 service XSD"),
    ]:
        print(("OK  " if ok else "ERR ") + label)
        failures += 0 if ok else 1

    # Control: absence is service-specific, not absence of generic subscription infrastructure.
    common = parse("IBIS-IP_common_V2.0.xsd")
    common_types = {
        n.get("name")
        for n in common.xpath("/xs:schema/xs:complexType", namespaces=NS)
    }
    generic_expected = {
        "SubscribeRequestStructure", "SubscribeResponseStructure",
        "UnsubscribeRequestStructure", "UnsubscribeResponseStructure",
    }
    ok_generic = generic_expected <= common_types
    print(("OK  " if ok_generic else "ERR ") + "generic Common V2.0 subscription request/response structures exist")
    failures += 0 if ok_generic else 1

    if failures == 0:
        print("PASSED: TSD-001 V2.1 service-specific subscription operation gap executable-confirmed")
        print("NOTE: generic Common subscription infrastructure exists; gap is in TrainSetDataService operation/root modelling")
    return failures


def main() -> int:
    failures = run_tsi001() + run_tsm001() + run_tsd001()
    if failures:
        print(f"\nFAILED: {failures} EV-109 check(s) did not match expectation")
        return 1
    print("\nPASSED: EV-109 TrainSet V2.1 deep-read evidence completed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
