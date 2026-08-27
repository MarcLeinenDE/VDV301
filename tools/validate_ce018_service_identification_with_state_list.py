#!/usr/bin/env python3
"""Executable evidence for CE-018 ServiceIdentificationWithStateList cardinality.

The PDF tables describe ServiceIdentificationWithState as 1:* while the Common
XSD family models it with minOccurs=0/maxOccurs=unbounded. This tool compiles
an exact Common-version harness and verifies both an empty list and a one-item
list for every Common XSD currently present in the superbranch.
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


COMMON_VERSIONS = ("1.0", "2.0", "2.1", "2.2", "2.3", "2.4")


def link_or_copy(source: Path, target: Path) -> None:
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


def harness(common_filename: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           elementFormDefault="qualified"
           attributeFormDefault="unqualified">
  <xs:include schemaLocation="{common_filename}"/>
  <xs:element name="TestServiceIdentificationWithStateList"
              type="ServiceIdentificationWithStateListStructure"/>
</xs:schema>
'''


EMPTY_LIST = "<TestServiceIdentificationWithStateList/>"

ONE_ITEM = '''<TestServiceIdentificationWithStateList>
  <ServiceIdentificationWithState>
    <ServiceIdentification>
      <Service>
        <ServiceName>TimeService</ServiceName>
        <IBIS-IP-Version><Value>1.0</Value></IBIS-IP-Version>
      </Service>
      <Device>
        <DeviceClass>OnBoardUnit</DeviceClass>
        <DeviceID><Value>ce018-test-device</Value></DeviceID>
      </Device>
    </ServiceIdentification>
    <ServiceState>running</ServiceState>
  </ServiceIdentificationWithState>
</TestServiceIdentificationWithStateList>'''


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    errors = 0

    # Copy/link the complete root XSD inventory so each historical Common file
    # resolves exactly the dependency filenames it declares.
    root_xsds = list(repo.glob("*.xsd"))
    if not root_xsds:
        print("ERROR: no root XSD files found")
        return 2

    with tempfile.TemporaryDirectory(prefix="vdv301_ce018_") as tmp:
        tmpdir = Path(tmp)
        for source in root_xsds:
            link_or_copy(source, tmpdir / source.name)

        for version in COMMON_VERSIONS:
            common_name = f"IBIS-IP_common_V{version}.xsd"
            common_path = repo / common_name
            if not common_path.exists():
                print(f"ERR Common V{version}: missing {common_name}")
                errors += 1
                continue

            harness_path = tmpdir / f"_ce018_common_v{version.replace('.', '_')}.xsd"
            harness_path.write_text(harness(common_name), encoding="utf-8")
            try:
                schema = etree.XMLSchema(etree.parse(str(harness_path)))
                print(f"OK  Common V{version} harness compiled")
            except Exception as exc:  # noqa: BLE001
                print(f"ERR Common V{version} harness compile failed")
                print(f"    {exc}")
                errors += 1
                continue

            empty_ok, empty_msg = validate(schema, EMPTY_LIST)
            if empty_ok:
                print(f"OK  Common V{version} accepts zero ServiceIdentificationWithState items")
            else:
                print(f"ERR Common V{version} rejects empty list")
                print(f"    {empty_msg}")
                errors += 1

            one_ok, one_msg = validate(schema, ONE_ITEM)
            if one_ok:
                print(f"OK  Common V{version} accepts one ServiceIdentificationWithState item")
            else:
                print(f"ERR Common V{version} rejects one-item list")
                print(f"    {one_msg}")
                errors += 1

    if errors:
        print(f"FAILED: {errors} unexpected result(s)")
        return 1

    print("PASSED: CE-018 executable 0:* behaviour confirmed across Common V1.0-V2.4")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
