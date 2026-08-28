#!/usr/bin/env python3
"""EV-108: deterministic declaration checks for the DMS V2.4 candidate/integration XSD.

The public V2.4 PDF is an official VDV writing. The XSD checked here is explicitly
candidate/integration material in dev/schema-integration and must not be relabelled
as an official release schema by this test.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
from lxml import etree

NS = {"xs": "http://www.w3.org/2001/XMLSchema"}
XSD = Path("IBIS-IP_DeviceManagementService_V2.4.xsd")


def fail(msg: str) -> None:
    print(f"FAIL {msg}", file=sys.stderr)
    raise SystemExit(1)


def ctype(root, name: str):
    nodes = root.xpath(f"./xs:complexType[@name={json.dumps(name)}]", namespaces=NS)
    if len(nodes) != 1:
        fail(f"expected one complexType {name}, got {len(nodes)}")
    return nodes[0]


def min_occurs(el) -> int:
    return int(el.get("minOccurs", "1"))


def main() -> int:
    root = etree.parse(str(XSD)).getroot()

    response = ctype(root, "DeviceManagementService.GetDeviceStatusInformationResponseStructure")
    branches = response.xpath("./xs:choice/xs:element/@name", namespaces=NS)
    exact = "DeviceManagementService.GetDeviceStatusInformationResponseData"
    pdf_only = "DeviceManagementService.DeviceStatusInformationResponseData"
    if exact not in branches or pdf_only in branches:
        fail(f"unexpected response branches: {branches}")
    print(f"OK  candidate response branch uses {exact}; PDF-only spelling absent")

    status = ctype(root, "DeviceStatusStructure")
    els = status.xpath("./xs:sequence/xs:element", namespaces=NS)
    mins = {e.get("name"): min_occurs(e) for e in els}
    expected = {
        "DeviceStatusName": 1,
        "DeviceStatusFlag": 1,
        "DeviceStatusImpact": 0,
        "DeviceStatusPriority": 0,
    }
    if mins != expected:
        fail(f"DeviceStatusStructure requiredness {mins!r} != {expected!r}")
    print("OK  candidate DeviceStatusImpact/Priority are optional; name/flag remain required")

    err = ctype(root, "DeviceManagementService.GetDeviceErrorMessagesResponseDataStructure")
    err_el = err.xpath("./xs:sequence/xs:element[@name='ErrorMessage']", namespaces=NS)
    if len(err_el) != 1 or min_occurs(err_el[0]) != 0 or err_el[0].get("maxOccurs") != "unbounded":
        fail("GetDeviceErrorMessages ErrorMessage is not 0:*")
    sub = ctype(root, "SubdeviceErrorMessagesStructure")
    sub_el = sub.xpath("./xs:sequence/xs:element[@name='ErrorMessage']", namespaces=NS)
    if len(sub_el) != 1 or min_occurs(sub_el[0]) != 0 or sub_el[0].get("maxOccurs") != "unbounded":
        fail("SubdeviceErrorMessages ErrorMessage is not 0:*")
    print("OK  candidate device/subdevice ErrorMessage cardinality is 0:*")

    install = ctype(root, "DeviceManagementService.InstallUpdateRequestStructure")
    install_els = {e.get("name"): e for e in install.xpath("./xs:sequence/xs:element", namespaces=NS)}
    for name in ["UpdateID", "UpdateTimestamp", "UpdateURL", "UpdateFileChecksum", "UpdateFileSize"]:
        if name not in install_els or min_occurs(install_els[name]) != 0:
            fail(f"InstallUpdate {name} is not optional")
    annotation = " ".join(install_els["UpdateTimestamp"].xpath(".//xs:documentation//text()", namespaces=NS)).strip()
    if "GetUpdateHistory" not in annotation or "RetrieveUpdateState" not in annotation or "GetUpdateStates" in annotation:
        fail(f"unexpected UpdateTimestamp annotation: {annotation!r}")
    print("OK  candidate InstallUpdate fields are optional and annotation uses GetUpdateHistory")

    enum = root.xpath("./xs:simpleType[@name='UpdateStatusEnumeration']/xs:restriction/xs:enumeration/@value", namespaces=NS)
    if "InstallationSuccessful" not in enum or "InstallationSuccessfull" in enum:
        fail(f"unexpected UpdateStatusEnumeration values: {enum}")
    print("OK  executable enum remains InstallationSuccessful; typo form absent")

    result = {
        "evidence_id": "EV-108",
        "authority": "candidate/integration DMS V2.4 XSD in dev/schema-integration",
        "public_pdf_authority": "official VDV DMS V2.4 writing",
        "schema": str(XSD),
        "dms_005_persists_against_candidate": True,
        "dms_006_v24_alignment": True,
        "dms_007_persists_against_candidate": True,
        "error_message_cardinality": "0:*",
        "install_update_optional_fields": ["UpdateID", "UpdateTimestamp", "UpdateURL", "UpdateFileChecksum", "UpdateFileSize"],
        "repository_mutated": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASSED: EV-108 DMS V2.4 candidate/integration declaration evidence confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
