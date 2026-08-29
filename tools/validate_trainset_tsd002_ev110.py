#!/usr/bin/env python3
"""EV-110: executable evidence for TrainSetDataService V2.2 TSD-002.

The V2.2 PDF operation overview still lists Retrieve*RequestStructure for the
UnsubscribeTripRef/UnsubscribeTripInformation requests, while the detailed PDF
text and exact official XSD use TrainSetUnsubscribeRequestStructure.

This harness proves the actual XSD validation behaviour without modifying any XSD.
"""
from __future__ import annotations

from pathlib import Path
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
XSD = ROOT / "IBIS-IP_TrainSetDataService_V2.2.xsd"


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


def specialized(root: str) -> str:
    return f'''<{root}>
  <Client-IP-Address><Value>192.0.2.10</Value></Client-IP-Address>
  <CoachNumber><Value>4711</Value></CoachNumber>
</{root}>'''


def retrieve_shaped(root: str) -> str:
    return f'''<{root}>
  <CoachNumber><Value>4711</Value></CoachNumber>
</{root}>'''


def main() -> int:
    schema = etree.XMLSchema(etree.parse(str(XSD)))
    print(f"OK  compiled {XSD.name}")
    failures = 0

    for root in (
        "TrainSetDataService.UnsubscribeTripRefRequest",
        "TrainSetDataService.UnsubscribeTripInformationRequest",
    ):
        failures += validate(
            schema,
            specialized(root),
            True,
            f"{root} accepts TrainSetUnsubscribeRequestStructure shape",
        )
        failures += validate(
            schema,
            retrieve_shaped(root),
            False,
            f"{root} rejects PDF-overview Retrieve*RequestStructure-like shape without Client-IP-Address",
        )

    if failures:
        print(f"FAILED: {failures} EV-110 check(s) did not match expectation")
        return 1
    print("PASSED: EV-110 TSD-002 executable request-shape mismatch confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
