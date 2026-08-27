#!/usr/bin/env python3
"""Validate the VDV301 XSD pool and optional DMS V2.4 sample cases.

This helper is intended for local review work. It is not required for an
upstream schema-only pull request.

Requirements:
    python -m pip install lxml

Typical usage from a repository checkout:
    python tools/validate_xsd_pool.py --repo-root . --dms-v24-tests
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

try:
    from lxml import etree
except ImportError:  # pragma: no cover - user-facing dependency message
    print("ERROR: lxml is required. Install with: python -m pip install lxml", file=sys.stderr)
    raise


@dataclass(frozen=True)
class XmlCase:
    name: str
    xml: str
    expected_valid: bool


def compile_schema(path: Path) -> tuple[bool, str]:
    try:
        etree.XMLSchema(etree.parse(str(path)))
        return True, "OK"
    except Exception as exc:  # noqa: BLE001 - diagnostic tool
        return False, str(exc)


def compile_all_xsd(repo_root: Path) -> int:
    errors = 0
    xsd_files = sorted(repo_root.glob("*.xsd"))
    print(f"Schema compile check: {len(xsd_files)} XSD files")
    for path in xsd_files:
        ok, message = compile_schema(path)
        status = "OK" if ok else "ERR"
        print(f"{status:3} {path.name}")
        if not ok:
            errors += 1
            print(f"    {message}")
    return errors


def dms_harness_schema_text(dms_filename: str = "IBIS-IP_DeviceManagementService_V2.4.xsd") -> str:
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           elementFormDefault="qualified"
           attributeFormDefault="unqualified">
    <xs:include schemaLocation="{dms_filename}"/>
    <xs:element name="TestDeviceStatus" type="DeviceStatusStructure"/>
    <xs:element name="TestSubdeviceErrorMessages" type="SubdeviceErrorMessagesStructure"/>
    <xs:element name="TestInstallUpdateRequest" type="DeviceManagementService.InstallUpdateRequestStructure"/>
    <xs:element name="TestUpdateStateData" type="DeviceManagementService.UpdateStateDataStructure"/>
</xs:schema>
'''


def dms_cases() -> list[XmlCase]:
    """Targeted DMS V2.4 regression cases.

    Common scalar wrapper types such as TimeStamp, SubdeviceName,
    DeviceStatusName and DeviceStatusFlag are structures with a required Value
    child. The positive samples therefore model the wrapper shape explicitly
    instead of placing scalar text directly on the wrapper element.
    """
    return [
        XmlCase(
            "device-error-messages-empty-is-valid",
            """<DeviceManagementService.GetDeviceErrorMessagesResponse>
  <DeviceManagementService.GetDeviceErrorMessagesResponseData>
    <TimeStamp><Value>2026-01-01T00:00:00Z</Value></TimeStamp>
  </DeviceManagementService.GetDeviceErrorMessagesResponseData>
</DeviceManagementService.GetDeviceErrorMessagesResponse>""",
            True,
        ),
        XmlCase(
            "subdevice-error-messages-empty-is-valid",
            """<TestSubdeviceErrorMessages>
  <SubdeviceName><Value>subdevice-1</Value></SubdeviceName>
</TestSubdeviceErrorMessages>""",
            True,
        ),
        XmlCase(
            "device-status-impact-priority-omitted-is-valid",
            """<TestDeviceStatus>
  <DeviceStatusName><Value>status-1</Value></DeviceStatusName>
  <DeviceStatusFlag><Value>true</Value></DeviceStatusFlag>
</TestDeviceStatus>""",
            True,
        ),
        XmlCase(
            "device-status-flag-still-required-is-invalid",
            """<TestDeviceStatus>
  <DeviceStatusName><Value>status-1</Value></DeviceStatusName>
</TestDeviceStatus>""",
            False,
        ),
        XmlCase(
            "install-update-request-empty-is-valid",
            "<TestInstallUpdateRequest/>",
            True,
        ),
        XmlCase(
            "update-state-data-timestamp-still-required-is-invalid",
            """<TestUpdateStateData>
  <UpdateID>update-1</UpdateID>
  <UpdateStatus>UpdateRunning</UpdateStatus>
</TestUpdateStateData>""",
            False,
        ),
    ]


def validate_xml(schema: etree.XMLSchema, case: XmlCase) -> tuple[bool, str]:
    doc = etree.fromstring(case.xml.encode("utf-8"))
    valid = bool(schema.validate(doc))
    if valid == case.expected_valid:
        return True, "OK"
    last_error = schema.error_log.last_error
    return False, str(last_error) if last_error is not None else "unexpected validation result"


def run_dms_v24_tests(repo_root: Path) -> int:
    dms_path = repo_root / "IBIS-IP_DeviceManagementService_V2.4.xsd"
    if not dms_path.exists():
        print("SKIP DMS V2.4 tests: IBIS-IP_DeviceManagementService_V2.4.xsd not found")
        return 0

    errors = 0
    print("DMS V2.4 XML sample tests")
    with tempfile.TemporaryDirectory(prefix="vdv301_dms_v24_") as tmpdir:
        harness = Path(tmpdir) / "_dms_v24_harness.xsd"
        harness.write_text(dms_harness_schema_text(), encoding="utf-8")

        # lxml resolves includes relative to the harness file. Use a symlink where
        # possible, otherwise copy the selected schema pool into the temporary dir.
        for xsd in repo_root.glob("*.xsd"):
            target = Path(tmpdir) / xsd.name
            try:
                target.symlink_to(xsd.resolve())
            except OSError:
                target.write_text(xsd.read_text(encoding="utf-8"), encoding="utf-8")

        schema = etree.XMLSchema(etree.parse(str(harness)))
        for case in dms_cases():
            ok, message = validate_xml(schema, case)
            status = "OK" if ok else "ERR"
            expectation = "valid" if case.expected_valid else "invalid"
            print(f"{status:3} {case.name} (expected {expectation})")
            if not ok:
                errors += 1
                print(f"    {message}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--dms-v24-tests", action="store_true", help="run DMS V2.4 XML sample tests")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    errors = compile_all_xsd(repo_root)
    if args.dms_v24_tests:
        errors += run_dms_v24_tests(repo_root)

    if errors:
        print(f"FAILED: {errors} validation error(s)")
        return 1
    print("PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
