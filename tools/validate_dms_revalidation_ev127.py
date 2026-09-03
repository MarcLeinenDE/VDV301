#!/usr/bin/env python3
"""EV-127: fail-closed revalidation for legacy findings DMS-001..DMS-007.

The validator reads the exact stored DMS XSD families and byte-pinned official
VDV PDFs.  It does not modify any schema.  Candidate/integration DMS V2.4 XSD
material remains explicitly labelled candidate/integration evidence.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.request

from lxml import etree

NS = {"xs": "http://www.w3.org/2001/XMLSchema"}
PDF_SOURCE_IDS = (
    "VDV301-2_BASE_V2.0",
    "VDV301-2_BASE_V2.1",
    "DMS_V2.2",
    "DMS_V2.4",
)
XSD_PATHS = {
    "v20": Path("IBIS-IP_DeviceManagementService_V2.0.xsd"),
    "v21": Path("IBIS-IP_DeviceManagementService_V2.1.xsd"),
    "v22": Path("IBIS-IP_DeviceManagementService_V2.2.xsd"),
    "v24": Path("IBIS-IP_DeviceManagementService_V2.4.xsd"),
}
SOURCE_REGISTRY = Path("audit_registry/pdf_source_registry_v0.1.json")
PIN_REGISTRY = Path("audit_registry/pdf_source_pins_v0.1.json")


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def by_source_id(data: dict, source_id: str) -> dict:
    matches = [item for item in data.get("sources", []) if item.get("source_id") == source_id]
    require(len(matches) == 1, f"{source_id}: expected exactly one registry record, found {len(matches)}")
    return matches[0]


def fetch(url: str, attempts: int = 4, timeout: int = 60) -> bytes:
    last: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": "VDV301-audit-EV127/1.0",
                    "Accept": "application/pdf,application/octet-stream;q=0.9,*/*;q=0.1",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.read()
        except (OSError, urllib.error.URLError) as exc:
            last = exc
            if attempt < attempts:
                time.sleep(attempt * 2)
    raise RuntimeError(f"unable to fetch {url} after {attempts} attempts: {last}")


def fetch_pinned_pdfs(tmp: Path) -> dict[str, Path]:
    sources = load_json(SOURCE_REGISTRY)
    pins = load_json(PIN_REGISTRY)
    out: dict[str, Path] = {}
    for source_id in PDF_SOURCE_IDS:
        source = by_source_id(sources, source_id)
        pin = by_source_id(pins, source_id)
        require(bool(pin.get("deep_read_source_ready")), f"{source_id}: not deep_read_source_ready")
        data = fetch(str(source["official_url"]))
        observed_sha = hashlib.sha256(data).hexdigest()
        observed_size = len(data)
        require(data.startswith(b"%PDF-"), f"{source_id}: payload is not PDF")
        require(observed_sha == str(pin["expected_sha256"]).lower(), f"{source_id}: SHA-256 changed: {observed_sha}")
        require(observed_size == int(pin["expected_size_bytes"]), f"{source_id}: size changed: {observed_size}")
        path = tmp / f"{source_id}.pdf"
        path.write_bytes(data)
        out[source_id] = path
        print(f"PIN_OK {source_id} sha256={observed_sha} size={observed_size}")
    return out


def page_text(pdf: Path, page: int) -> str:
    proc = subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(pdf), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return " ".join(proc.stdout.split())


def full_text(pdf: Path) -> str:
    proc = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return "\n".join(line.rstrip() for line in proc.stdout.splitlines())


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def parse_xsd(path: Path) -> etree._Element:
    require(path.is_file(), f"missing XSD {path}")
    tree = etree.parse(str(path))
    # Compilation is part of the executable evidence and also checks includes.
    etree.XMLSchema(tree)
    print(f"XSD_COMPILE_OK {path}")
    return tree.getroot()


def group_names(root: etree._Element) -> list[str]:
    nodes = root.xpath("./xs:group[@name='DeviceManagementServiceGroup']/xs:sequence/xs:element/@name", namespaces=NS)
    require(bool(nodes), "DeviceManagementServiceGroup missing or empty")
    return list(nodes)


def global_names(root: etree._Element) -> set[str]:
    return set(root.xpath("./xs:element/@name", namespaces=NS))


def ctype(root: etree._Element, name: str) -> etree._Element:
    nodes = root.xpath(f"./xs:complexType[@name={json.dumps(name)}]", namespaces=NS)
    require(len(nodes) == 1, f"expected exactly one complexType {name!r}, found {len(nodes)}")
    return nodes[0]


def seq_element(root: etree._Element, type_name: str, element_name: str) -> etree._Element:
    ct = ctype(root, type_name)
    nodes = ct.xpath(f"./xs:sequence/xs:element[@name={json.dumps(element_name)}]", namespaces=NS)
    require(len(nodes) == 1, f"{type_name}.{element_name}: expected one sequence element, found {len(nodes)}")
    return nodes[0]


def occurs(el: etree._Element) -> tuple[str, str]:
    return el.get("minOccurs", "1"), el.get("maxOccurs", "1")


def status_requiredness(root: etree._Element) -> dict[str, str]:
    ct = ctype(root, "DeviceStatusStructure")
    nodes = ct.xpath("./xs:sequence/xs:element", namespaces=NS)
    return {str(el.get("name")): str(el.get("minOccurs", "1")) for el in nodes}


def install_requiredness(root: etree._Element) -> dict[str, str]:
    ct = ctype(root, "DeviceManagementService.InstallUpdateRequestStructure")
    nodes = ct.xpath("./xs:sequence/xs:element", namespaces=NS)
    wanted = {"UpdateID", "UpdateTimestamp", "UpdateURL", "UpdateFileChecksum", "UpdateFileSize"}
    return {str(el.get("name")): str(el.get("minOccurs", "1")) for el in nodes if el.get("name") in wanted}


def update_timestamp_annotation(root: etree._Element) -> str:
    el = seq_element(root, "DeviceManagementService.InstallUpdateRequestStructure", "UpdateTimestamp")
    return " ".join(el.xpath(".//xs:documentation//text()", namespaces=NS)).strip()


def response_choice_names(root: etree._Element) -> list[str]:
    ct = ctype(root, "DeviceManagementService.GetDeviceStatusInformationResponseStructure")
    return list(ct.xpath("./xs:choice/xs:element/@name", namespaces=NS))


def main() -> int:
    if shutil.which("pdftotext") is None:
        fail("EV-127 requires pdftotext (poppler-utils)")

    roots = {version: parse_xsd(path) for version, path in XSD_PATHS.items()}

    with tempfile.TemporaryDirectory(prefix="vdv301-ev127-") as tmp_name:
        pdfs = fetch_pinned_pdfs(Path(tmp_name))

        # ------------------------------------------------------------------
        # DMS-001: refine the old broad claim.  Generic subscribe/unsubscribe
        # use Common structures by design; the surviving V2.0 asymmetry is the
        # incomplete DMS-specific wrapper/group model itself.
        # ------------------------------------------------------------------
        v20_group = group_names(roots["v20"])
        v20_globals = global_names(roots["v20"])
        v21_group = group_names(roots["v21"])
        v21_globals = global_names(roots["v21"])

        expected_v20_group = [
            "DeviceManagementService.GetDeviceInformationResponse",
            "DeviceManagementService.GetDeviceConfigurationResponse",
            "DeviceManagementService.SetDeviceConfigurationRequest",
            "DeviceManagementService.GetDeviceStatusResponse",
            "DeviceManagementService.GetDeviceErrorMessagesResponse",
            "DeviceManagementService.GetServiceInformationResponse",
            "DeviceManagementService.GetServiceStatusResponse",
            "DeviceManagementService.StartServiceRequest",
            "DeviceManagementService.RestartServiceRequest",
            "DeviceManagementService.StopServiceRequest",
        ]
        require(v20_group == expected_v20_group, f"DMS-001: V2.0 group changed: {v20_group!r}")
        for name in (
            "DeviceManagementService.SetDeviceConfigurationResponse",
            "DeviceManagementService.RestartDeviceResponse",
        ):
            require(name in v20_globals, f"DMS-001: expected V2.0 global {name} missing")
            require(name not in v20_group, f"DMS-001: expected V2.0 group omission no longer present: {name}")
        for name in (
            "DeviceManagementService.ActivateDeviceResponse",
            "DeviceManagementService.DeactivateDeviceResponse",
        ):
            require(name not in v20_globals, f"DMS-001: unexpected V2.0 global wrapper exists: {name}")
            require(name in v21_globals and name in v21_group, f"DMS-001: V2.1 expansion wrapper missing: {name}")
        for name in (
            "DeviceManagementService.SetDeviceConfigurationResponse",
            "DeviceManagementService.RestartDeviceResponse",
            "DeviceManagementService.SubscribeDeviceInformationRequest",
            "DeviceManagementService.SubscribeDeviceInformationResponse",
        ):
            require(name in v21_group, f"DMS-001: V2.1 explicit group model missing {name}")

        v20_ops = page_text(pdfs["VDV301-2_BASE_V2.0"], 90) + " " + page_text(pdfs["VDV301-2_BASE_V2.0"], 91)
        for phrase in (
            "SubscribeDeviceInformation",
            "SubscribeRequestStructure",
            "SubscribeResponseStructure",
            "RestartDevice",
            "DeactivateDevice",
            "ActivateDevice",
            "DataAcceptedResponseStructure",
        ):
            require(phrase in v20_ops, f"DMS-001: V2.0 PDF operation evidence missing {phrase!r}")
        print("OK DMS-001 refined historical service-group/wrapper asymmetry confirmed; generic Common subscription modelling separated")

        # ------------------------------------------------------------------
        # DMS-002: documentation-only unresolved cross references in V2.0.
        # ------------------------------------------------------------------
        broken = "Fehler! Verweisquelle konnte nicht gefunden werden."
        base20_text = full_text(pdfs["VDV301-2_BASE_V2.0"])
        base21_text = full_text(pdfs["VDV301-2_BASE_V2.1"])
        count20 = base20_text.count(broken)
        count21 = base21_text.count(broken)
        require(count20 >= 2, f"DMS-002: expected repeated V2.0 unresolved reference marker, found {count20}")
        require(count21 == 0, f"DMS-002: V2.1 unexpectedly still has unresolved reference marker count={count21}")
        print(f"OK DMS-002 unresolved V2.0 reference markers count={count20}; V2.1 count=0")

        # ------------------------------------------------------------------
        # DMS-003: 10:* through official V2.2; V2.4 correction is 0:*.
        # ------------------------------------------------------------------
        for version in ("v20", "v21", "v22"):
            el = seq_element(roots[version], "DeviceManagementService.GetDeviceErrorMessagesResponseDataStructure", "ErrorMessage")
            require(occurs(el) == ("10", "unbounded"), f"DMS-003: {version} ErrorMessage cardinality {occurs(el)} != 10:*")
        v24_error = seq_element(roots["v24"], "DeviceManagementService.GetDeviceErrorMessagesResponseDataStructure", "ErrorMessage")
        require(occurs(v24_error) == ("0", "unbounded"), f"DMS-003: V2.4 candidate ErrorMessage cardinality {occurs(v24_error)} != 0:*")
        require("ErrorMessage 10:*" in page_text(pdfs["DMS_V2.2"], 20), "DMS-003: V2.2 PDF 10:* evidence missing")
        require("ErrorMessage 0:*" in page_text(pdfs["DMS_V2.4"], 19), "DMS-003: V2.4 PDF 0:* evidence missing")
        print("OK DMS-003 historical 10:* rule and V2.4 0:* correction confirmed")

        # ------------------------------------------------------------------
        # DMS-004: three required InstallUpdate identity/location fields in
        # V2.1/V2.2; all five checked fields optional in V2.4.
        # ------------------------------------------------------------------
        expected_old = {
            "UpdateID": "1",
            "UpdateTimestamp": "1",
            "UpdateURL": "1",
            "UpdateFileChecksum": "0",
            "UpdateFileSize": "0",
        }
        for version in ("v21", "v22"):
            actual = install_requiredness(roots[version])
            require(actual == expected_old, f"DMS-004: {version} InstallUpdate requiredness {actual!r} != {expected_old!r}")
        expected_v24 = {name: "0" for name in expected_old}
        actual_v24 = install_requiredness(roots["v24"])
        require(actual_v24 == expected_v24, f"DMS-004: V2.4 candidate InstallUpdate requiredness {actual_v24!r} != {expected_v24!r}")
        v22_install = page_text(pdfs["DMS_V2.2"], 26)
        v24_install = page_text(pdfs["DMS_V2.4"], 25)
        for phrase in ("UpdateID 1:1", "UpdateTimestamp 1:1", "UpdateURL 1:1"):
            require(phrase in v22_install, f"DMS-004: V2.2 PDF missing {phrase!r}")
        for phrase in ("UpdateID 0:1", "UpdateTimestamp 0:1", "UpdateURL 0:1"):
            require(phrase in v24_install, f"DMS-004: V2.4 PDF missing {phrase!r}")
        print("OK DMS-004 V2.1/V2.2 requiredness and V2.4 optionality correction confirmed")

        # ------------------------------------------------------------------
        # DMS-005: PDF branch spelling lacks Get; exact selected XSDs use Get.
        # ------------------------------------------------------------------
        exact_branch = "DeviceManagementService.GetDeviceStatusInformationResponseData"
        pdf_branch = "DeviceManagementService.DeviceStatusInformationResponseData"
        for version in ("v22", "v24"):
            branches = response_choice_names(roots[version])
            require(exact_branch in branches, f"DMS-005: {version} exact Get-prefixed branch missing: {branches!r}")
            require(pdf_branch not in branches, f"DMS-005: {version} PDF-only alias unexpectedly exists")
        for source_id, page in (("DMS_V2.2", 23), ("DMS_V2.4", 22)):
            text = compact(page_text(pdfs[source_id], page))
            require(pdf_branch in text, f"DMS-005: {source_id} PDF branch spelling not reconstructable on page {page}")
            require(exact_branch in text, f"DMS-005: {source_id} same table should also expose Get-prefixed type/reference context")
        print("OK DMS-005 PDF branch-name mismatch against exact XSD declaration confirmed")

        # ------------------------------------------------------------------
        # DMS-006: V2.2 PDF table lists only Name/Flag while selected V2.2 XSD
        # requires Name/Flag/Impact/Priority; V2.4 aligns with optional latter two.
        # ------------------------------------------------------------------
        req22 = status_requiredness(roots["v22"])
        require(req22 == {
            "DeviceStatusName": "1",
            "DeviceStatusFlag": "1",
            "DeviceStatusImpact": "1",
            "DeviceStatusPriority": "1",
        }, f"DMS-006: V2.2 DeviceStatus requiredness changed: {req22!r}")
        req24 = status_requiredness(roots["v24"])
        require(req24 == {
            "DeviceStatusName": "1",
            "DeviceStatusFlag": "1",
            "DeviceStatusImpact": "0",
            "DeviceStatusPriority": "0",
        }, f"DMS-006: V2.4 candidate DeviceStatus requiredness changed: {req24!r}")
        p22 = page_text(pdfs["DMS_V2.2"], 23)
        require("DeviceStatusName 1:1" in p22 and "DeviceStatusFlag 1:1" in p22, "DMS-006: V2.2 PDF Name/Flag table evidence missing")
        require("DeviceStatusImpact" not in p22 and "DeviceStatusPriority" not in p22, "DMS-006: V2.2 PDF unexpectedly lists Impact/Priority on DeviceStatus page")
        p24 = page_text(pdfs["DMS_V2.4"], 23)
        require("DeviceStatusImpact 0:1" in p24 and "DeviceStatusPriority 0:1" in p24, "DMS-006: V2.4 PDF correction evidence missing")
        print("OK DMS-006 V2.2 PDF omission / XSD requirement and V2.4 alignment confirmed")

        # ------------------------------------------------------------------
        # DMS-007: documentation reference typo; no new operation alias.
        # ------------------------------------------------------------------
        ann22 = update_timestamp_annotation(roots["v22"])
        ann24 = update_timestamp_annotation(roots["v24"])
        for version, annotation in (("v22", ann22), ("v24", ann24)):
            require("GetUpdateHistory" in annotation, f"DMS-007: {version} XSD annotation lacks GetUpdateHistory: {annotation!r}")
            require("RetrieveUpdateState" in annotation, f"DMS-007: {version} XSD annotation lacks RetrieveUpdateState: {annotation!r}")
            require("GetUpdateStates" not in annotation, f"DMS-007: {version} XSD annotation unexpectedly contains GetUpdateStates")
        require("GetUpdateStates" in page_text(pdfs["DMS_V2.2"], 26), "DMS-007: V2.2 PDF typo evidence missing")
        require("GetUpdateStates" in page_text(pdfs["DMS_V2.4"], 25), "DMS-007: V2.4 PDF typo evidence missing")
        for version in ("v21", "v22", "v24"):
            all_names = group_names(roots[version]) + list(global_names(roots[version]))
            require(any("GetUpdateHistory" in name for name in all_names), f"DMS-007: {version} operation model lacks GetUpdateHistory")
            require(not any("GetUpdateStates" in name for name in all_names), f"DMS-007: {version} unexpectedly exposes GetUpdateStates operation alias")
        print("OK DMS-007 GetUpdateStates PDF reference typo / GetUpdateHistory operation model confirmed")

    result = {
        "evidence_id": "EV-127",
        "finding_block": [f"DMS-{i:03d}" for i in range(1, 8)],
        "result": "PASS",
        "terminal_revalidation_recommendations": {
            "DMS-001": "context_verified",
            "DMS-002": "context_verified",
            "DMS-003": "executable_confirmed",
            "DMS-004": "executable_confirmed",
            "DMS-005": "executable_confirmed",
            "DMS-006": "executable_confirmed",
            "DMS-007": "context_verified",
        },
        "dms_001_refinement": "generic Common subscribe/unsubscribe modelling is intentional context; surviving V2.0 finding is incomplete DMS-specific wrapper/group modelling, with V2.1 expansion as history evidence",
        "v24_authority": "candidate/integration XSD comparison only; public V2.4 PDF remains official writing",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    print("PASSED: EV-127 DMS-001..007 legacy finding revalidation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
