#!/usr/bin/env python3
"""EV-107: executable declaration checks for DMS V2.2 deep-read findings.

This evidence intentionally does not mutate or repair the historical schema. It
reads the exact stored DMS V2.2 XSD and verifies the declarations that are
material to the PDF/XSD deep-read findings.
"""

from __future__ import annotations

import json
from pathlib import Path
import sys

from lxml import etree

XSD_NS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XSD_NS}
XSD = Path("IBIS-IP_DeviceManagementService_V2.2.xsd")


def fail(message: str) -> None:
    print(f"FAIL {message}", file=sys.stderr)
    raise SystemExit(1)


def complex_type(root: etree._Element, name: str) -> etree._Element:
    result = root.xpath(f"./xs:complexType[@name={json.dumps(name)}]", namespaces=NS)
    if len(result) != 1:
        fail(f"expected exactly one complexType {name!r}, found {len(result)}")
    return result[0]


def effective_min_occurs(element: etree._Element) -> int:
    return int(element.get("minOccurs", "1"))


def main() -> int:
    if not XSD.is_file():
        fail(f"missing {XSD}")

    root = etree.parse(str(XSD)).getroot()

    response = complex_type(root, "DeviceManagementService.GetDeviceStatusInformationResponseStructure")
    response_names = response.xpath("./xs:choice/xs:element/@name", namespaces=NS)
    expected_response_data = "DeviceManagementService.GetDeviceStatusInformationResponseData"
    pdf_response_data = "DeviceManagementService.DeviceStatusInformationResponseData"
    if expected_response_data not in response_names:
        fail(f"missing exact XSD response-data branch {expected_response_data}")
    if pdf_response_data in response_names:
        fail(f"PDF-only response-data spelling unexpectedly exists in XSD: {pdf_response_data}")
    print(f"OK  response branch uses {expected_response_data}; PDF-only spelling absent")

    status = complex_type(root, "DeviceStatusStructure")
    status_elements = status.xpath("./xs:sequence/xs:element", namespaces=NS)
    actual_names = [el.get("name") for el in status_elements]
    expected_names = [
        "DeviceStatusName",
        "DeviceStatusFlag",
        "DeviceStatusImpact",
        "DeviceStatusPriority",
    ]
    if actual_names != expected_names:
        fail(f"DeviceStatusStructure fields {actual_names!r} != expected {expected_names!r}")
    requiredness = {el.get("name"): effective_min_occurs(el) for el in status_elements}
    if any(requiredness[name] != 1 for name in expected_names):
        fail(f"DeviceStatusStructure requiredness differs from 1:1: {requiredness}")
    print("OK  DeviceStatusStructure has four fields and all are required (effective minOccurs=1)")

    install = complex_type(root, "DeviceManagementService.InstallUpdateRequestStructure")
    timestamps = install.xpath("./xs:sequence/xs:element[@name='UpdateTimestamp']", namespaces=NS)
    if len(timestamps) != 1:
        fail(f"expected one InstallUpdate UpdateTimestamp, found {len(timestamps)}")
    annotation = " ".join(timestamps[0].xpath(".//xs:documentation//text()", namespaces=NS)).strip()
    if "GetUpdateHistory" not in annotation or "RetrieveUpdateState" not in annotation:
        fail(f"UpdateTimestamp annotation lacks expected operation references: {annotation!r}")
    if "GetUpdateStates" in annotation:
        fail(f"PDF-only GetUpdateStates wording unexpectedly exists in XSD annotation: {annotation!r}")
    print("OK  InstallUpdate.UpdateTimestamp XSD annotation references GetUpdateHistory + RetrieveUpdateState, not GetUpdateStates")

    update_status = root.xpath("./xs:simpleType[@name='UpdateStatusEnumeration']/xs:restriction/xs:enumeration/@value", namespaces=NS)
    if "InstallationSuccessful" not in update_status:
        fail("UpdateStatusEnumeration lacks executable value InstallationSuccessful")
    if "InstallationSuccessfull" in update_status:
        fail("typo-like InstallationSuccessfull unexpectedly exists as executable enum value")
    print("OK  executable update-status value is InstallationSuccessful; typo-like InstallationSuccessfull is not an enum value")

    result = {
        "evidence_id": "EV-107",
        "authority": "official DMS V2.2 exact stored XSD",
        "schema": str(XSD),
        "response_data_branch": expected_response_data,
        "pdf_only_response_data_branch_absent": True,
        "device_status_required_fields": expected_names,
        "install_update_timestamp_annotation": annotation,
        "installation_successful_enum": True,
        "repository_mutated": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASSED: EV-107 DMS V2.2 deep-read schema declarations confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
