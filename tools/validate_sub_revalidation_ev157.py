#!/usr/bin/env python3
"""EV-157: fail-closed generic subscription finding revalidation evidence.

Validates SUB-001/SUB-002 against exact official Base Services V2.0/V2.1 PDF
bytes, the corresponding executable Common/service XSDs, and frozen audit
provenance. This validator is read-only with respect to repository content.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from lxml import etree

BASE_V20_SHA256 = "fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37"
BASE_V20_SIZE = 2374295
BASE_V20_PAGES = 115
BASE_V21_SHA256 = "685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a"
BASE_V21_SIZE = 2671005
BASE_V21_PAGES = 130

EXPECTED_BLOBS = {
    "audit_registry/finding_inventory_frozen_2026-09-03.json": "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
    "audit_registry/finding_revalidation_registry_v0.1.json": "650dc6a45f47e01cef2e5e05f48614e0c5afe819",
    "00_START_HERE/CURRENT_STATE.json": "612b9217244e7bbb49a09c8f4d94b9036e388dc4",
    "audit_registry/pdf_source_registry_v0.1.json": "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
    "audit_registry/pdf_source_pins_v0.1.json": "88349638b423689799af700e8a1c8ec99bbfb67b",
    "audit_registry/deep_read_findings_v0.1.json": "f016defa3148400834378ac99ca33b30937f2571",
    "audit_registry/deep_read_findings_delta_gc_v24_2026-08-28.json": "2fd4eb48195c27312c73f665d4365bb28ca3a791",
    "IBIS-IP_common_V1.0.xsd": "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c",
    "IBIS-IP_Enumerations_V1.0.xsd": "a9bea5bc73003ed91ded8519db06c32c4067831d",
    "IBIS-IP_SystemManagementService_V1.0.xsd": "2d32630a0f1981e980e6a466e3f6a69136410f24",
    "IBIS-IP_common_V2.0.xsd": "8608e3dcd665c197c34da7f6ec6af5a3758da164",
    "IBIS-IP_Enumerations_V2.0.xsd": "27e3c183b00381d959622d13c10543123af8eef6",
    "IBIS-IP_SystemDocumentationService_V2.0.xsd": "ab959dddbfa2b8ca420af1b079501f94cff38051",
    "IBIS-IP_common_V2.1.xsd": "05977c9f86c7c9dd0b48f36a4a4e9be32e94659e",
    "IBIS-IP_Enumerations_V2.1.xsd": "311464690ad60749ed8d326217787e4b8ed0b718",
    "IBIS-IP_DeviceManagementService_V2.1.xsd": "191b43e01cdaba14b247725689a913c244a67eed",
}

XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"OK  {message}")


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def norm(text: str) -> str:
    return " ".join(text.replace("\u2013", "-").replace("\u2014", "-").split())


def page_text(pdf: Path, page: int) -> str:
    done = subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(pdf), "-"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return done.stdout.decode("utf-8", errors="replace")


def pdf_page_count(pdf: Path) -> int:
    done = subprocess.run(["pdfinfo", str(pdf)], check=True, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in done.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise AssertionError("pdfinfo did not expose page count")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def group_names(tree: etree._ElementTree, group: str) -> list[str]:
    return tree.xpath(f"//xs:group[@name='{group}']/xs:sequence/xs:element/@name", namespaces=NS)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--base-v20", required=True)
    ap.add_argument("--base-v21", required=True)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    v20 = Path(args.base_v20).resolve()
    v21 = Path(args.base_v21).resolve()
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    # Immutable repository and audit prestate.
    for rel, expected in EXPECTED_BLOBS.items():
        p = root / rel
        require(p.is_file(), f"authority/prestate file exists: {rel}")
        observed = git_blob_sha(p.read_bytes())
        require(observed == expected, f"exact blob {rel} = {observed}")

    registry = load(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    entries = registry["inventory"]["entries"]
    terminal_states = {"context_verified", "field_validated", "executable_confirmed", "contextual_not_defect", "withdrawn", "unresolved", "superseded"}
    terminal = sum(e.get("revalidation_state") in terminal_states for e in entries)
    pending = sum(e.get("revalidation_state") == "pending" for e in entries)
    first_pending = next(e["finding_id"] for e in entries if e.get("revalidation_state") == "pending")
    by_id = {e["finding_id"]: e for e in entries}
    require((terminal, pending) == (144, 48), f"pre-SUB counts = {terminal}/{pending}")
    require(first_pending == "SUB-001", "pre-SUB first pending is SUB-001")
    require(registry.get("next_revalidation_block") == "SUB", "registry next block is SUB")
    for fid in ("SUB-001", "SUB-002"):
        require(by_id[fid].get("revalidation_state") == "pending", f"{fid} remains pending before EV-157")
        require(by_id[fid].get("terminal_state_source") is None, f"{fid} has no premature terminal source")

    state = load(root / "00_START_HERE/CURRENT_STATE.json")["audit"]
    require(state.get("finding_revalidation_completed_findings") == 144, "CURRENT_STATE terminal count is 144")
    require(state.get("finding_revalidation_pending_findings") == 48, "CURRENT_STATE pending count is 48")
    require(state.get("finding_revalidation_next_block") == "SUB", "CURRENT_STATE next block is SUB")

    # Official source catalog must still route the exact Base Services publications.
    source_registry = load(root / "audit_registry/pdf_source_registry_v0.1.json")
    sources = {s["source_id"]: s for s in source_registry.get("sources", [])}
    require(sources["VDV301-2_BASE_V2.0"]["official_url"] == "https://www.vdv.de/301-2-sds-v-2-0.pdfx",
            "official Base Services V2.0 URL unchanged")
    require(sources["VDV301-2_BASE_V2.1"]["official_url"] == "https://www.vdv.de/301-2-sds-v2-1-basicservices.pdfx",
            "official Base Services V2.1 URL unchanged")

    # Re-acquired official PDF bytes must match the acquisition evidence exactly.
    for pdf, sha, size, pages, label in (
        (v20, BASE_V20_SHA256, BASE_V20_SIZE, BASE_V20_PAGES, "Base Services V2.0"),
        (v21, BASE_V21_SHA256, BASE_V21_SIZE, BASE_V21_PAGES, "Base Services V2.1"),
    ):
        require(pdf.is_file(), f"{label} PDF exists")
        data = pdf.read_bytes()
        require(data.startswith(b"%PDF-"), f"{label} source is PDF")
        require(hashlib.sha256(data).hexdigest() == sha, f"{label} SHA-256 = {sha}")
        require(len(data) == size, f"{label} size = {size}")
        require(pdf_page_count(pdf) == pages, f"{label} page count = {pages}")

    # Canonical frozen provenance explicitly strengthens SUB-001 and SUB-002.
    deep = load(root / "audit_registry/deep_read_findings_v0.1.json")
    strengthened = [x for x in deep.get("existing_findings_strengthened", []) if x.get("id") in {"SUB-001", "SUB-002"}]
    require(any(x.get("id") == "SUB-001" and x.get("new_evidence_document") == "VDV301-2_BASE_V2.0" for x in strengthened),
            "frozen-era provenance links SUB-001 to Base Services V2.0")
    require(any(x.get("id") == "SUB-002" and x.get("new_evidence_document") == "VDV301-2_BASE_V2.0" for x in strengthened),
            "frozen-era provenance links SUB-002 to Base Services V2.0")
    require(any(x.get("id") == "SUB-002" and x.get("new_evidence_document") == "VDV301-2_BASE_V2.1" for x in strengthened),
            "frozen-era provenance links SUB-002 to Base Services V2.1")
    gc24 = load(root / "audit_registry/deep_read_findings_delta_gc_v24_2026-08-28.json")
    require(any(x.get("id") == "SUB-001" and "TerminateSubscribe" in x.get("effect", "") for x in gc24.get("existing_finding_updates", [])),
            "GC V2.4 audit delta confirms SUB-001 persists")

    # SUB-001 visual/document evidence: notation says TerminateSubscribe*, executable Common says Unsubscribe*.
    for pdf, pages, label in ((v20, (82, 83), "V2.0"), (v21, (83, 84), "V2.1")):
        text = norm("\n".join(page_text(pdf, p) for p in pages))
        require("UnsubscribeData" in text, f"{label} notation contains UnsubscribeData")
        require("TerminateSubscribeRequestStructure" in text, f"{label} notation contains TerminateSubscribeRequestStructure")
        require("TerminateSubscribeResponseStructure" in text, f"{label} notation contains TerminateSubscribeResponseStructure")

    common_trees = {}
    for version in ("V1.0", "V2.0", "V2.1"):
        p = root / f"IBIS-IP_common_{version}.xsd"
        tree = etree.parse(str(p))
        common_trees[version] = tree
        types = set(tree.xpath("//xs:complexType/@name", namespaces=NS))
        require("UnsubscribeRequestStructure" in types, f"Common {version} has UnsubscribeRequestStructure")
        require("UnsubscribeResponseStructure" in types, f"Common {version} has UnsubscribeResponseStructure")
        require("TerminateSubscribeRequestStructure" not in types, f"Common {version} has no TerminateSubscribeRequestStructure alias")
        require("TerminateSubscribeResponseStructure" not in types, f"Common {version} has no TerminateSubscribeResponseStructure alias")

    # SUB-002 document evidence: generic subscriptions are documented for sparse services.
    v20_sd = norm(page_text(v20, 99))
    require("SubscribeSystemConfiguration" in v20_sd and "SubscribeRequestStructure" in v20_sd,
            "V2.0 page 99 documents SubscribeSystemConfiguration using generic SubscribeRequestStructure")
    require("UnsubscribeSystemConfiguration" in v20_sd and "UnsubscribeRequestStructure" in v20_sd,
            "V2.0 page 99 documents UnsubscribeSystemConfiguration using generic UnsubscribeRequestStructure")
    v20_sm = norm(page_text(v20, 103))
    for token in ("SubscribeDeviceStatus", "UnsubscribeDeviceStatus", "SubscribeServiceStatus", "UnsubscribeServiceStatus"):
        require(token in v20_sm, f"V2.0 page 103 documents {token}")

    v21_sd = norm(page_text(v21, 112))
    require("SubscribeSystemConfiguration" in v21_sd and "UnsubscribeSystemConfiguration" in v21_sd,
            "V2.1 page 112 retains generic SystemDocumentation subscription operations")
    v21_sm = norm(page_text(v21, 116))
    require("SubscribeDeviceStatus" in v21_sm and "UnsubscribeDeviceStatus" in v21_sm,
            "V2.1 page 116 retains generic SystemManagement subscription operations")

    # SUB-002 executable context: local group style demonstrably differs by service/version.
    sysdoc_tree = etree.parse(str(root / "IBIS-IP_SystemDocumentationService_V2.0.xsd"))
    sysmgmt_tree = etree.parse(str(root / "IBIS-IP_SystemManagementService_V1.0.xsd"))
    dms_tree = etree.parse(str(root / "IBIS-IP_DeviceManagementService_V2.1.xsd"))
    etree.XMLSchema(sysdoc_tree)
    etree.XMLSchema(sysmgmt_tree)
    etree.XMLSchema(dms_tree)
    print("OK  compiled SystemDocumentation V2.0, SystemManagement V1.0 and DMS V2.1")

    sd_group = group_names(sysdoc_tree, "SystemDocumentationServiceGroup")
    sm_group = group_names(sysmgmt_tree, "SystemManagementServiceGroup")
    dms_group = group_names(dms_tree, "DeviceManagementServiceGroup")
    require(sd_group == [
        "SystemDocumentationService.GetSystemConfigurationResponse",
        "SystemDocumentationService.StoreSystemConfigurationRequest",
        "SystemDocumentationService.RetrieveLogMessagesRequest",
        "SystemDocumentationService.RetrieveLogMessagesResponse",
        "SystemDocumentationService.StoreLogMessagesRequest",
    ], "SystemDocumentation V2.0 local group is sparse and omits documented generic subscription operations")
    require(sm_group == [
        "SystemManagementService.GetDeviceStatusResponse",
        "SystemManagementService.GetServiceStatusResponse",
    ], "SystemManagement V1.0 local group is sparse and omits documented generic subscription operations")
    require("DeviceManagementService.SubscribeDeviceInformationRequest" in dms_group,
            "DMS V2.1 local group explicitly includes generic SubscribeDeviceInformationRequest")
    require("DeviceManagementService.UnsubscribeDeviceInformationRequest" in dms_group,
            "DMS V2.1 local group explicitly includes generic UnsubscribeDeviceInformationRequest")
    require("DeviceManagementService.SubscribeDeviceStatusRequest" in dms_group,
            "DMS V2.1 local group explicitly includes generic SubscribeDeviceStatusRequest")
    require("DeviceManagementService.UnsubscribeDeviceStatusRequest" in dms_group,
            "DMS V2.1 local group explicitly includes generic UnsubscribeDeviceStatusRequest")
    require(len(dms_group) > len(sd_group) and len(dms_group) > len(sm_group),
            "service-local operation-group modelling is demonstrably service/version dependent")

    result = {
        "evidence_id": "EV-157",
        "result": "PASS",
        "source_acquisition": {
            "run_id": "34486504933",
            "job_id": "102902042657",
            "artifact_id": "10155848626",
            "artifact_digest": "sha256:8318472f56fe7c33d85bc5cda3bc02df5cfed7f987dacb832eaa4798a1ff2d4a",
        },
        "authority": {
            "base_v20": {"sha256": BASE_V20_SHA256, "size_bytes": BASE_V20_SIZE, "pages": BASE_V20_PAGES},
            "base_v21": {"sha256": BASE_V21_SHA256, "size_bytes": BASE_V21_SIZE, "pages": BASE_V21_PAGES},
            "xsd_blobs": {k: v for k, v in EXPECTED_BLOBS.items() if k.endswith(".xsd")},
            "audit_source_blobs": {k: v for k, v in EXPECTED_BLOBS.items() if not k.endswith(".xsd")},
        },
        "visual_pages": {
            "VDV301-2_BASE_V2.0": [82, 83, 99, 103],
            "VDV301-2_BASE_V2.1": [83, 84, 112, 116],
        },
        "finding_results": {
            "SUB-001": {
                "recommended_terminal_state": "context_verified",
                "result": "PASS",
                "reason": "Official notation uses TerminateSubscribeRequest/ResponseStructure for UnsubscribeData while exact Common V1.0/V2.0/V2.1 expose UnsubscribeRequest/ResponseStructure and no TerminateSubscribe aliases.",
            },
            "SUB-002": {
                "recommended_terminal_state": "contextual_not_defect",
                "result": "PASS",
                "reason": "Official PDFs document generic subscriptions for SystemDocumentation/SystemManagement despite sparse local XSD groups, while DMS V2.1 explicitly expands such operations; local group membership is therefore service/version dependent and not standalone supported-operation authority.",
            },
        },
        "expected_poststate_if_closed": {"terminal": 146, "pending": 46, "next_block": "TKT", "first_pending": "TKT-001"},
        "xsd_mutation_required": False,
        "frozen_inventory_mutation_required": False,
    }
    target = out / "ev157_result.json"
    target.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"PASSED: EV-157 -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
