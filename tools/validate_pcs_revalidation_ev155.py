#!/usr/bin/env python3
"""EV-155 fail-closed revalidation for PCS-001 and PCS-002.

PCS-001 authority lane:
- official byte-pinned VDV 301-2-8 PassengerCountingService V2.1 PDF,
- exact official PCS V2.1 XSD dependency route (Common V1.0 + Enumerations V1.0),
- executable validator tools/validate_pcs_v21_operation_not_supported.py.

PCS-002 authority lane:
- original official upstream VDV-301-1.0 aggregate packaging,
- later official VDV-301-2.0 self-contained packaging of service version V1.0,
- executable root-validation comparison using the same PCS payload sample.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from lxml import etree

PDF_V1_SHA = "372be7a5d39c72e4bf405e3058f5af3d809eb611ac3548b70c526788d364c402"
PDF_V1_SIZE = 918762
PDF_V1_PAGES = 18
PDF_V21_SHA = "572f07adbb6999463433a3e764e47f29c8157a4e63aa88ea7c927393da7ec043"
PDF_V21_SIZE = 1084925
PDF_V21_PAGES = 22

EXPECTED_STATES = {
    "PCS-001": "executable_confirmed",
    "PCS-002": "contextual_not_defect",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


def pdf_pages(path: Path) -> int:
    proc = run(["pdfinfo", str(path)])
    if proc.returncode != 0:
        raise AssertionError(proc.stdout)
    for line in proc.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise AssertionError(f"Pages missing in pdfinfo for {path}")


def page_text(path: Path, page: int, out_dir: Path) -> str:
    target = out_dir / f"{path.stem}-page-{page}.txt"
    proc = run(["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(path), str(target)])
    if proc.returncode != 0:
        raise AssertionError(proc.stdout)
    return target.read_text(encoding="utf-8", errors="replace")


def schema(path: Path) -> etree.XMLSchema:
    return etree.XMLSchema(etree.parse(str(path)))


def validate_xml(xsd: etree.XMLSchema, xml: str) -> tuple[bool, str]:
    doc = etree.fromstring(xml.encode("utf-8"))
    ok = bool(xsd.validate(doc))
    if ok:
        return True, "OK"
    last = xsd.error_log.last_error
    return False, str(last) if last is not None else "validation failed"


def global_names(root: etree._Element, local_name: str) -> list[str]:
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    return [x.get("name") for x in root.xpath(f"./xs:{local_name}", namespaces=ns) if x.get("name")]


def complex_type_signature(root: etree._Element, name: str) -> tuple:
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    found = root.xpath(f"./xs:complexType[@name='{name}']", namespaces=ns)
    assert len(found) == 1, (name, len(found))

    def sig(node: etree._Element) -> tuple:
        if not isinstance(node.tag, str):
            return ()
        local = etree.QName(node).localname
        if local in {"annotation", "documentation"}:
            return ()
        attrs = tuple(sorted((etree.QName(k).localname, v) for k, v in node.attrib.items()))
        kids = tuple(s for child in node if (s := sig(child)))
        return (local, attrs, kids)

    return sig(found[0])


def enum_values(path: Path, type_name: str) -> list[str]:
    root = etree.parse(str(path)).getroot()
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    nodes = root.xpath(f"./xs:simpleType[@name='{type_name}']//xs:enumeration", namespaces=ns)
    return [n.get("value") for n in nodes if n.get("value")]


def include_locations(path: Path) -> list[str]:
    root = etree.parse(str(path)).getroot()
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    return [n.get("schemaLocation") for n in root.xpath("./xs:include", namespaces=ns)]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--pdf-v1", required=True)
    ap.add_argument("--pdf-v21", required=True)
    ap.add_argument("--upstream-v1-dir", required=True)
    ap.add_argument("--upstream-v20-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    repo = Path(args.repo_root).resolve()
    pdf_v1 = Path(args.pdf_v1).resolve()
    pdf_v21 = Path(args.pdf_v21).resolve()
    up_v1 = Path(args.upstream_v1_dir).resolve()
    up_v20 = Path(args.upstream_v20_dir).resolve()
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    text_out = out / "pdf_text"
    text_out.mkdir(exist_ok=True)

    registry = json.loads((repo / "audit_registry/finding_revalidation_registry_v0.1.json").read_text(encoding="utf-8"))
    entries = registry["inventory"]["entries"]
    assert registry["inventory"]["state"] == "frozen"
    assert registry["inventory"]["entry_count"] == 192 and len(entries) == 192
    assert registry["next_revalidation_block"] == "PCS"
    terminal = sum(x["revalidation_state"] != "pending" for x in entries)
    pending = sum(x["revalidation_state"] == "pending" for x in entries)
    assert (terminal, pending) == (138, 54), (terminal, pending)
    first_pending = next(x["finding_id"] for x in entries if x["revalidation_state"] == "pending")
    assert first_pending == "PCS-001", first_pending
    by_id = {x["finding_id"]: x for x in entries}
    assert by_id["PCS-001"]["revalidation_state"] == "pending"
    assert by_id["PCS-002"]["revalidation_state"] == "pending"
    pcs_indexes = [i for i, x in enumerate(entries) if x["finding_id"] in EXPECTED_STATES]
    simulated = [dict(x) for x in entries]
    for i in pcs_indexes:
        simulated[i]["revalidation_state"] = EXPECTED_STATES[simulated[i]["finding_id"]]
    simulated_first_pending = next(x["finding_id"] for x in simulated if x["revalidation_state"] == "pending")
    simulated_terminal = sum(x["revalidation_state"] != "pending" for x in simulated)
    simulated_pending = sum(x["revalidation_state"] == "pending" for x in simulated)
    assert (simulated_terminal, simulated_pending, simulated_first_pending) == (140, 52, "SMS-001")

    # Fresh PDF authority pins and visible semantics.
    assert sha256(pdf_v1) == PDF_V1_SHA and pdf_v1.stat().st_size == PDF_V1_SIZE
    assert sha256(pdf_v21) == PDF_V21_SHA and pdf_v21.stat().st_size == PDF_V21_SIZE
    assert pdf_pages(pdf_v1) == PDF_V1_PAGES
    assert pdf_pages(pdf_v21) == PDF_V21_PAGES
    p12 = page_text(pdf_v21, 12, text_out)
    p16 = page_text(pdf_v21, 16, text_out)
    p17 = page_text(pdf_v21, 17, text_out)
    assert "Data Structures of Operation RetrieveSpecificDoorData" in p12
    assert "PassengerCountingService.RetrieveSpecificDoorDataResponse" in p12
    assert "OperationNotSupported" not in p12
    assert "Optional Operation StartCounting" in p16
    assert "Optional Operation StopCounting" in p16
    assert p16.count("OperationNotSupported") >= 2
    assert "Optional Operation GetCountingState" in p16
    assert "OperationNotSupported" in p17
    assert "Optional Operation SubscribeCountingState" in p17
    assert "Optional Operation UnsubscribeCountingState" in p17
    assert p17.count("OperationNotSupported") >= 3

    # PCS-001 exact schema-family/dependency route.
    pcs_v21 = repo / "IBIS-IP_PassengerCountingService_V2.1.xsd"
    common_v1 = repo / "IBIS-IP_common_V1.0.xsd"
    enums_v1 = repo / "IBIS-IP_Enumerations_V1.0.xsd"
    enums_v21 = repo / "IBIS-IP_Enumerations_V2.1.xsd"
    assert include_locations(pcs_v21) == ["IBIS-IP_common_V1.0.xsd", "IBIS-IP_Enumerations_V1.0.xsd"]
    v1_codes = enum_values(enums_v1, "ErrorCodeEnumeration")
    v21_codes = enum_values(enums_v21, "ErrorCodeEnumeration")
    assert "OperationNotSupported" not in v1_codes
    assert "OperationNotSupported" in v21_codes
    common_root = etree.parse(str(common_v1)).getroot()
    ns = {"xs": "http://www.w3.org/2001/XMLSchema"}
    error_nodes = common_root.xpath("./xs:complexType[@name='DataAcceptedResponseDataStructure']//xs:element[@name='ErrorCode']", namespaces=ns)
    assert len(error_nodes) == 1 and error_nodes[0].get("type") == "ErrorCodeEnumeration"

    pcs001_proc = run([sys.executable, str(repo / "tools/validate_pcs_v21_operation_not_supported.py")], cwd=repo)
    assert pcs001_proc.returncode == 0, pcs001_proc.stdout
    assert "PASSED: PCS-001 executable dependency/value-set mismatch confirmed" in pcs001_proc.stdout

    # PCS-002: exact historical packaging behavior, then later self-contained V1.0.
    old_service = up_v1 / "IBIS-IP_PassengerCountingService_V1.0.xsd"
    old_root_path = up_v1 / "IBIS_IP_V1.0.xsd"
    new_service = up_v20 / "IBIS-IP_PassengerCountingService_V1.0.xsd"
    for p in (old_service, old_root_path, new_service):
        assert p.exists(), p

    old_doc = etree.parse(str(old_service))
    old_root_doc = etree.parse(str(old_root_path))
    new_doc = etree.parse(str(new_service))
    old_schema_root = old_doc.getroot()
    aggregate_root = old_root_doc.getroot()
    new_schema_root = new_doc.getroot()

    old_elements = global_names(old_schema_root, "element")
    old_groups = global_names(old_schema_root, "group")
    aggregate_elements = global_names(aggregate_root, "element")
    aggregate_groups = global_names(aggregate_root, "group")
    new_elements = global_names(new_schema_root, "element")
    new_groups = global_names(new_schema_root, "group")

    assert not [x for x in old_elements if x.startswith("PassengerCountingService.")]
    assert "PassengerCountingServiceGroup" not in old_groups
    assert "PassengerCountingService.GetAllDataResponse" in aggregate_elements
    assert "PassengerCountingServiceGroup" in aggregate_groups
    assert "PassengerCountingService.GetAllDataResponse" in new_elements
    assert "PassengerCountingServiceGroup" in new_groups

    checked_types = [
        "PassengerCountingService.AllDataStructure",
        "PassengerCountingService.GetAllDataResponseStructure",
        "PassengerCountingService.RetrieveSpecificDoorDataRequestStructure",
        "PassengerCountingService.RetrieveSpecificDoorDataResponseStructure",
        "PassengerCountingService.SpecificDoorDataStructure",
        "PassengerCountingService.SetCounterDataRequestStructure",
    ]
    for name in checked_types:
        assert complex_type_signature(old_schema_root, name) == complex_type_signature(new_schema_root, name), name

    old_service_schema = schema(old_service)
    old_aggregate_schema = schema(old_root_path)
    new_service_schema = schema(new_service)
    root_sample = """<PassengerCountingService.GetAllDataResponse><OperationErrorMessage><Value>probe</Value></OperationErrorMessage></PassengerCountingService.GetAllDataResponse>"""
    old_service_ok, old_service_msg = validate_xml(old_service_schema, root_sample)
    old_aggregate_ok, old_aggregate_msg = validate_xml(old_aggregate_schema, root_sample)
    new_service_ok, new_service_msg = validate_xml(new_service_schema, root_sample)
    assert old_service_ok is False, (old_service_ok, old_service_msg)
    assert old_aggregate_ok is True, old_aggregate_msg
    assert new_service_ok is True, new_service_msg

    result = {
        "evidence_id": "EV-155",
        "result": "PASS",
        "scope": ["PCS-001", "PCS-002"],
        "prestate": {"terminal": 138, "pending": 54, "first_pending": "PCS-001"},
        "expected_poststate_if_closed": {"terminal": 140, "pending": 52, "first_pending": "SMS-001", "next_block": "SMS"},
        "pdf_authority": {
            "PCS_V1.0": {"sha256": PDF_V1_SHA, "size_bytes": PDF_V1_SIZE, "pages": PDF_V1_PAGES},
            "PCS_V2.1": {"sha256": PDF_V21_SHA, "size_bytes": PDF_V21_SIZE, "pages": PDF_V21_PAGES},
        },
        "fresh_visual_context": {
            "PCS_V2.1_physical_pages": [12, 16, 17],
            "retrieve_specific_door_data_page_has_operation_not_supported": False,
            "optional_operation_pages_explicitly_extend_operation_not_supported": True,
        },
        "finding_results": {
            "PCS-001": {
                "recommended_terminal_state": "executable_confirmed",
                "exact_dependency_route": include_locations(pcs_v21),
                "operation_not_supported_in_enums_v1": False,
                "operation_not_supported_in_enums_v21_control": True,
                "executable_validator": "tools/validate_pcs_v21_operation_not_supported.py",
                "executable_result": "PASS",
            },
            "PCS-002": {
                "recommended_terminal_state": "contextual_not_defect",
                "old_service_has_operation_root": False,
                "old_aggregate_has_operation_root": True,
                "later_self_contained_service_has_operation_root": True,
                "same_payload_sample_valid_old_service_only": old_service_ok,
                "same_payload_sample_valid_old_aggregate": old_aggregate_ok,
                "same_payload_sample_valid_later_self_contained_service": new_service_ok,
                "checked_payload_type_signatures_unchanged": checked_types,
                "classification": "historical_aggregate_routing_later_self_contained_packaging",
            },
        },
        "pcs001_validator_output": pcs001_proc.stdout,
    }
    (out / "ev155_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("EV155_PASS PCS-001=executable_confirmed PCS-002=contextual_not_defect next=SMS-001/SMS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
