#!/usr/bin/env python3
"""Executable evidence for PCS-001 (OperationNotSupported dependency mismatch).

The official PassengerCountingService V2.1 XSD includes Common V1.0 and
Enumerations V1.0. The PCS V2.1 service document describes
OperationNotSupported for optional operations, while that enumeration value is
absent from Enumerations V1.0 and present in Enumerations V2.1.

This test deliberately keeps two authorities separate:

1. exact PCS V2.1 route: PCS V2.1 -> Common V1.0 -> Enums V1.0
2. explanatory enum-only control: Enums V2.1

The control is not an alternative PCS production route.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

try:
    from lxml import etree
except ImportError:
    print("ERROR: lxml is required. Install with: python -m pip install lxml", file=sys.stderr)
    raise


def write_link_or_copy(source: Path, target: Path) -> None:
    try:
        target.symlink_to(source.resolve())
    except OSError:
        target.write_bytes(source.read_bytes())


def validate(schema: etree.XMLSchema, xml: str) -> tuple[bool, str]:
    doc = etree.fromstring(xml.encode("utf-8"))
    ok = bool(schema.validate(doc))
    if ok:
        return True, "OK"
    last = schema.error_log.last_error
    return False, str(last) if last is not None else "validation failed"


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    required = [
        repo / "IBIS-IP_PassengerCountingService_V2.1.xsd",
        repo / "IBIS-IP_common_V1.0.xsd",
        repo / "IBIS-IP_Enumerations_V1.0.xsd",
        repo / "IBIS-IP_Enumerations_V2.1.xsd",
    ]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        for path in missing:
            print(f"ERROR missing: {path}")
        return 2

    exact_harness = '''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           elementFormDefault="qualified"
           attributeFormDefault="unqualified">
  <xs:include schemaLocation="IBIS-IP_PassengerCountingService_V2.1.xsd"/>
  <xs:element name="TestStartCountingResponse" type="DataAcceptedResponseStructure"/>
</xs:schema>
'''

    control_harness = '''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           elementFormDefault="qualified"
           attributeFormDefault="unqualified">
  <xs:include schemaLocation="IBIS-IP_Enumerations_V2.1.xsd"/>
  <xs:element name="TestErrorCode" type="ErrorCodeEnumeration"/>
</xs:schema>
'''

    valid_v1_code = '''<TestStartCountingResponse>
  <DataAcceptedResponseData>
    <TimeStamp><Value>2026-01-01T00:00:00Z</Value></TimeStamp>
    <DataAccepted><Value>false</Value></DataAccepted>
    <ErrorCode>DataNotValid</ErrorCode>
  </DataAcceptedResponseData>
</TestStartCountingResponse>'''

    operation_not_supported_exact = '''<TestStartCountingResponse>
  <DataAcceptedResponseData>
    <TimeStamp><Value>2026-01-01T00:00:00Z</Value></TimeStamp>
    <DataAccepted><Value>false</Value></DataAccepted>
    <ErrorCode>OperationNotSupported</ErrorCode>
  </DataAcceptedResponseData>
</TestStartCountingResponse>'''

    operation_not_supported_control = "<TestErrorCode>OperationNotSupported</TestErrorCode>"

    errors = 0
    with tempfile.TemporaryDirectory(prefix="vdv301_pcs_001_") as tmp:
        tmpdir = Path(tmp)
        for source in required:
            write_link_or_copy(source, tmpdir / source.name)

        exact_path = tmpdir / "_pcs_v21_exact_harness.xsd"
        exact_path.write_text(exact_harness, encoding="utf-8")
        exact_schema = etree.XMLSchema(etree.parse(str(exact_path)))
        print("OK  exact PCS V2.1 dependency route compiled")

        ok, msg = validate(exact_schema, valid_v1_code)
        if ok:
            print("OK  exact route accepts existing V1.0 ErrorCode DataNotValid")
        else:
            print("ERR exact route unexpectedly rejects DataNotValid")
            print(f"    {msg}")
            errors += 1

        ok, msg = validate(exact_schema, operation_not_supported_exact)
        if not ok:
            print("OK  exact route rejects OperationNotSupported as expected")
            print(f"    evidence: {msg}")
        else:
            print("ERR exact route unexpectedly accepts OperationNotSupported")
            errors += 1

        control_path = tmpdir / "_enum_v21_control.xsd"
        control_path.write_text(control_harness, encoding="utf-8")
        control_schema = etree.XMLSchema(etree.parse(str(control_path)))
        print("OK  Enums V2.1 explanatory control compiled")

        ok, msg = validate(control_schema, operation_not_supported_control)
        if ok:
            print("OK  Enums V2.1 control accepts OperationNotSupported")
        else:
            print("ERR Enums V2.1 control unexpectedly rejects OperationNotSupported")
            print(f"    {msg}")
            errors += 1

    if errors:
        print(f"FAILED: {errors} unexpected result(s)")
        return 1

    print("PASSED: PCS-001 executable dependency/value-set mismatch confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
