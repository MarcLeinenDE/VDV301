#!/usr/bin/env python3
"""EV-143 fail-closed revalidation evidence for DRDOOR21-001..002."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/DOOR_V2.1.pdf")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/DOOR_V2.1.md")
DELTA = Path("audit_registry/deep_read_findings_delta_door_v21_2026-08-29.json")
REG_DELTA = Path("audit_registry/deep_read_registry_delta_door_v21_2026-08-29.json")
PROVENANCE = Path("docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_DOOR_V21_BLOB_PROVENANCE_2026-08-29.md")
DOOR_XSD = Path("IBIS-IP_DoorStateService_V2.1.xsd")
COMMON = Path("IBIS-IP_common_V1.0.xsd")
ENUMS = Path("IBIS-IP_Enumerations_V1.0.xsd")
EV111 = Path("tools/validate_door_v21_ev111.py")
OUT_DIR = Path(os.environ.get("EV143_OUTPUT_DIR", "artifacts/ev143"))

EXPECTED_PDF_SHA256 = "7413c99f2910f125947213561658ae9c808952d5b57700d155b939c899de26e8"
EXPECTED_PDF_SIZE = 851513
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_DEEP_READ_BLOB = "ef81d838be8d42ae9250cddb7e506f978ba75655"
EXPECTED_DELTA_BLOB = "5daf0521652097d141947ccba6811b22e66e2468"
EXPECTED_REG_DELTA_BLOB = "47a0f7ab3c9004bbfd2e01819194718b356c107f"
EXPECTED_PROVENANCE_BLOB = "0eb7f9cb46644a8c526523d42dccac5b3d962994"
EXPECTED_DOOR_BLOB = "abff0f3960e2ec7a9caaa9ddeb6efff8f4183805"
EXPECTED_COMMON_BLOB = "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c"
EXPECTED_ENUM_BLOB = "a9bea5bc73003ed91ded8519db06c32c4067831d"
EXPECTED_EV111_BLOB = "75c7528c2f18dfe35d74a6b27e104ec006661ce1"
FINDINGS = ("DRDOOR21-001", "DRDOOR21-002")
NS = {"xs": "http://www.w3.org/2001/XMLSchema"}


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256(); size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk); size += len(chunk)
    return h.hexdigest(), size


def pdf_pages() -> int:
    info = subprocess.check_output(["pdfinfo", str(PDF)], text=True, errors="replace")
    m = re.search(r"^Pages:\s*(\d+)\s*$", info, re.MULTILINE)
    require(m is not None, "pdfinfo page count missing")
    return int(m.group(1))


def page_text(page: int) -> str:
    return subprocess.check_output(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(PDF), "-"],
        text=True, errors="replace"
    )


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def find_type(root: etree._Element, name: str) -> etree._Element:
    nodes = root.xpath(f"./xs:complexType[@name={json.dumps(name)}]", namespaces=NS)
    require(len(nodes) == 1, f"expected one complexType {name}, found {len(nodes)}")
    return nodes[0]


def main() -> int:
    require(PDF.is_file(), f"missing PDF {PDF}")
    for path, expected in {
        FROZEN: EXPECTED_FROZEN_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        DELTA: EXPECTED_DELTA_BLOB,
        REG_DELTA: EXPECTED_REG_DELTA_BLOB,
        PROVENANCE: EXPECTED_PROVENANCE_BLOB,
        DOOR_XSD: EXPECTED_DOOR_BLOB,
        COMMON: EXPECTED_COMMON_BLOB,
        ENUMS: EXPECTED_ENUM_BLOB,
        EV111: EXPECTED_EV111_BLOB,
    }.items():
        require(path.is_file(), f"missing immutable authority/evidence {path}")
        observed = blob(path)
        require(observed == expected, f"immutable blob changed for {path}: {observed}")

    pdf_hash, pdf_size = sha256_file(PDF)
    require(pdf_hash == EXPECTED_PDF_SHA256, f"PDF hash mismatch {pdf_hash}")
    require(pdf_size == EXPECTED_PDF_SIZE, f"PDF size mismatch {pdf_size}")

    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory invariant failed")
    for fid in FINDINGS:
        require(fid in frozen.get("finding_ids", []), f"{fid} missing from frozen inventory")

    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entries = reg.get("inventory", {}).get("entries", [])
    by_id = {x.get("finding_id"): x for x in entries}
    terminal = sum(x.get("revalidation_state") != "pending" for x in entries)
    pending = sum(x.get("revalidation_state") == "pending" for x in entries)
    require((terminal, pending) == (101, 91), f"unexpected pre-DOOR-V2.1 counts {(terminal, pending)}")
    require(reg.get("next_revalidation_block") == "DOOR", f"unexpected next block {reg.get('next_revalidation_block')}")
    prev = reg.get("revalidation_blocks", {}).get("DMS_V2.4", {})
    require(prev.get("state") == "completed" and prev.get("next_block") == "DOOR" and prev.get("next_subblock") == "DOOR_V2.1", "DMS V2.4 does not route to DOOR V2.1")
    require("DOOR_V2.1" not in reg.get("revalidation_blocks", {}), "DOOR V2.1 already closed")
    for fid in FINDINGS:
        require(by_id.get(fid, {}).get("revalidation_state") == "pending", f"{fid} is not pending")

    delta = json.loads(DELTA.read_text(encoding="utf-8"))
    require(delta.get("document_id") == "DOOR_V2.1", "wrong DOOR delta document id")
    new = {x.get("id"): x for x in delta.get("new_findings", [])}
    require(set(new) == set(FINDINGS), f"DOOR new finding set changed: {sorted(new)}")
    require(new["DRDOOR21-001"].get("classification") == "pdf_operation_name_editorial_error_candidate", "DRDOOR21-001 classification changed")
    require(new["DRDOOR21-002"].get("classification") == "pdf_description_copy_paste_error_candidate", "DRDOOR21-002 classification changed")
    for fid in FINDINGS:
        require(new[fid].get("state") == "context_verified", f"historical deep-read state changed for {fid}")
        require(str(new[fid].get("validation_behavior", "")).startswith("none"), f"unexpected validation behavior for {fid}")

    reg_delta = json.loads(REG_DELTA.read_text(encoding="utf-8"))
    update = reg_delta.get("document_updates", {}).get("DOOR_V2.1", {})
    auth = update.get("exact_xsd_authority", {})
    require(auth.get("tag") == "VDV-301-2.1", "DOOR official authority tag changed")
    require(auth.get("DoorStateService_blob") == EXPECTED_DOOR_BLOB, "DOOR authority blob changed")
    require(auth.get("common_v1_0_blob") == EXPECTED_COMMON_BLOB and auth.get("enumerations_v1_0_blob") == EXPECTED_ENUM_BLOB, "DOOR mixed dependency authority changed")
    require(auth.get("integration_branch_files_match_official_tag") is True and auth.get("mixed_version_dependency_is_authoritative") is True, "DOOR authority route guard changed")

    deep = DEEP_READ.read_text(encoding="utf-8")
    for anchor in (
        "DRDOOR21-001 - RetrieveSpecific operation names are shortened/typoed in table descriptions",
        "RetrieveDoorOpenState",
        "RetrieveDoorOpereationState",
        "DRDOOR21-002 - DoorOpenState description copied from operation-state semantics",
        "SpecificDoorOpenStateStructure",
        "validation impact: none",
    ):
        require(anchor in deep, f"DOOR deep-read anchor missing: {anchor}")

    tree = etree.parse(str(DOOR_XSD))
    etree.XMLSchema(tree)
    root = tree.getroot()
    includes = [x.get("schemaLocation") for x in root.findall("xs:include", NS)]
    require(includes == ["IBIS-IP_common_V1.0.xsd", "IBIS-IP_Enumerations_V1.0.xsd"], f"DOOR include route changed: {includes}")
    group = root.find("xs:group[@name='DoorStateServiceGroup']/xs:sequence", NS)
    require(group is not None, "DoorStateServiceGroup missing")
    op_names = [x.get("name") for x in group.findall("xs:element", NS) if x.get("name")]
    exact_open_req = "DoorStateService.RetrieveSpecificDoorOpenStateRequest"
    exact_op_req = "DoorStateService.RetrieveSpecificDoorOperationStateRequest"
    require(exact_open_req in op_names and exact_op_req in op_names, "exact RetrieveSpecific request operations missing")
    for alias in ("DoorStateService.RetrieveDoorOpenStateRequest", "DoorStateService.RetrieveDoorOpereationStateRequest"):
        require(alias not in op_names, f"PDF-only alias unexpectedly exists in exact service group: {alias}")

    open_resp = find_type(root, "DoorStateService.RetrieveSpecificDoorOpenStateResponseStructure")
    open_el = open_resp.xpath("./xs:choice/xs:element[@name='DoorOpenState']", namespaces=NS)
    require(len(open_el) == 1 and open_el[0].get("type") == "DoorStateService.SpecificDoorOpenStateStructure", "RetrieveSpecificDoorOpenState response type route changed")
    open_struct = find_type(root, "DoorStateService.SpecificDoorOpenStateStructure")
    open_fields = [x.get("name") for x in open_struct.xpath("./xs:sequence/xs:element", namespaces=NS)]
    require("OpenState" in open_fields and "OperationState" not in open_fields, f"SpecificDoorOpenStateStructure semantics changed: {open_fields}")
    op_struct = find_type(root, "DoorStateService.SpecificDoorOperationStateStructure")
    op_fields = [x.get("name") for x in op_struct.xpath("./xs:sequence/xs:element", namespaces=NS)]
    require("OperationState" in op_fields and "OpenState" not in op_fields, f"SpecificDoorOperationStateStructure semantics changed: {op_fields}")

    ev111 = subprocess.run([sys.executable, str(EV111)], text=True, capture_output=True)
    print(ev111.stdout, end="")
    if ev111.stderr:
        print(ev111.stderr, file=sys.stderr, end="")
    require(ev111.returncode == 0, "preserved EV-111 rerun failed")
    require("PASSED: EV-111 DoorState V2.1 DRS-002/DRS-003 executable behaviour confirmed" in ev111.stdout, "EV-111 success boundary missing")

    pages = pdf_pages()
    finding_pages: dict[str, list[int]] = {fid: [] for fid in FINDINGS}
    page_context: dict[str, dict[str, list[str]]] = {}
    shortened_pattern = re.compile(r"(?<!Specific)RetrieveDoorOpenState\b")
    typo_pattern = re.compile(r"RetrieveDoorOpereationState\b")
    for page in range(1, pages + 1):
        text = page_text(page)
        c = compact(text)
        short = shortened_pattern.findall(c)
        typo = typo_pattern.findall(c)
        if short or typo:
            finding_pages["DRDOOR21-001"].append(page)
            page_context.setdefault(str(page), {})["DRDOOR21-001"] = [x for x in (
                "RetrieveDoorOpenState" if short else "",
                "RetrieveDoorOpereationState" if typo else "",
            ) if x]
        low = c.lower()
        if "retrievespecificdooropenstate" in low and "dooropenstate" in low and "operation state" in low:
            finding_pages["DRDOOR21-002"].append(page)
            page_context.setdefault(str(page), {})["DRDOOR21-002"] = ["RetrieveSpecificDoorOpenState", "DoorOpenState", "operation state"]

    require(finding_pages["DRDOOR21-001"], "no PDF page contains the DRDOOR21-001 shortened/typoed names")
    require(finding_pages["DRDOOR21-002"], "no PDF page contains the DRDOOR21-002 open-state/operation-state context")

    # Strong disproofs: the suspect operation names must not be legitimate
    # aliases, and the operation-state wording must not describe the exact type.
    require(not any("RetrieveDoorOpenStateRequest" == name.split(".")[-1] for name in op_names), "shortened RetrieveDoorOpenState is an executable alias")
    require(not any("RetrieveDoorOpereationStateRequest" == name.split(".")[-1] for name in op_names), "typoed RetrieveDoorOpereationState is an executable alias")
    require("OpenState" in open_fields and "OperationState" not in open_fields and "OperationState" in op_fields, "open/operation state type distinction not proven")

    render_pages = sorted(set(finding_pages["DRDOOR21-001"] + finding_pages["DRDOOR21-002"]))
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "render_pages.txt").write_text("".join(f"{p}\n" for p in render_pages), encoding="utf-8")
    (OUT_DIR / "page_map.json").write_text(json.dumps({
        "finding_pages": finding_pages,
        "page_context": page_context,
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    result = {
        "evidence_id": "EV-143",
        "finding_block": list(FINDINGS),
        "pdf_source_id": "DOOR_V2.1",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "pdf_page_count": pages,
        "evidence_pages": finding_pages,
        "render_pages": render_pages,
        "authority": {
            "status": "official_VDV-301-2.1_exact_mixed_version_family",
            "door_xsd_blob": EXPECTED_DOOR_BLOB,
            "common_v1_0_blob": EXPECTED_COMMON_BLOB,
            "enumerations_v1_0_blob": EXPECTED_ENUM_BLOB,
            "mixed_version_dependency_is_authoritative": True,
            "latest_xsd_wins": False,
        },
        "base_evidence": "EV-111 rerun unchanged PASS",
        "active_disproof": {
            "DRDOOR21-001": "rejected alternate-operation-name hypothesis: exact service group contains RetrieveSpecific names and no shortened/typo aliases",
            "DRDOOR21-002": "rejected shared-operation-state-description hypothesis: exact open-state response routes to SpecificDoorOpenStateStructure/OpenState while separate operation-state structure uses OperationState",
        },
        "terminal_revalidation_recommendations": {
            "DRDOOR21-001": "context_verified",
            "DRDOOR21-002": "context_verified",
        },
        "executable_evidence_reason_not_applicable": "Both frozen findings are documentation-only wording/name errors; EV-111 and exact-XSD structure inspection are corroborating context, not an XML validity rule for the typo text.",
        "visual_review": "all discovered substantive pages must be rendered and inspected before permanent evidence record and closure",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS_PENDING_VISUAL_REVIEW",
    }
    (OUT_DIR / "ev143_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED_TEXT_CONTEXT: EV-143 DOOR V2.1 DRDOOR21-001..002; visual page review still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
