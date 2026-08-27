#!/usr/bin/env python3
"""Executable evidence for EV-105 / ARA-003.

The AnalogRadioService V2.4 XSD is candidate/integration material sourced from
open upstream PR #27. This harness therefore proves candidate-profile behavior
only; it does not promote the schema to official authority.
"""

from pathlib import Path

from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
XSD = ROOT / "IBIS-IP_AnalogRadioService_V2.4.xsd"
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}


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


def telegram(transmitter: bool) -> str:
    transmitter_xml = "\n  <Transmitter/>" if transmitter else ""
    return f'''<AnalogRadioService.SendTelegram>
  <RawTelegram><Value>0123456789ABCDEF</Value></RawTelegram>
  <AnalogChannel><Value>1</Value></AnalogChannel>
  <Bitrate>1200</Bitrate>{transmitter_xml}
</AnalogRadioService.SendTelegram>'''


def main() -> int:
    failures = 0
    tree = etree.parse(str(XSD))
    schema = etree.XMLSchema(tree)
    print("OK  compiled candidate IBIS-IP_AnalogRadioService_V2.4.xsd")

    transmitter_nodes = tree.xpath(
        "/xs:schema/xs:complexType[@name='AnalogRadioService.RadioTelegramStructure']"
        "/xs:sequence/xs:element[@name='Transmitter']",
        namespaces=NS,
    )
    if len(transmitter_nodes) != 1:
        print(f"ERR expected exactly one Transmitter declaration, found {len(transmitter_nodes)}")
        failures += 1
    else:
        node = transmitter_nodes[0]
        min_occurs = node.get("minOccurs", "1")
        max_occurs = node.get("maxOccurs", "1")
        if min_occurs == "0" and max_occurs == "1":
            print("OK  candidate declaration Transmitter cardinality is 0:1")
        else:
            print(f"ERR candidate declaration Transmitter cardinality is {min_occurs}:{max_occurs}, expected 0:1")
            failures += 1

    if not validate(schema, telegram(False), True, "SendTelegram without Transmitter is accepted"):
        failures += 1
    if not validate(schema, telegram(True), True, "SendTelegram with Transmitter is accepted"):
        failures += 1

    if failures:
        print(f"FAILED: {failures} EV-105 check(s) did not match expectation")
        return 1

    print("PASSED: ARA-003 candidate XSD 0:1 Transmitter behavior executable-confirmed")
    print("NOTE: result applies only to the explicitly selected candidate/integration profile")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
