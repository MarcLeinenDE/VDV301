#!/usr/bin/env python3
"""Fail-closed closure writer for VDV301-2 Base V2.1 DR3012V21-001."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/vdv3012_v21_revalidation_evidence_2026-09-03.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_VDV3012_V21_2026-09-03.md")
DMS_XSD = Path("IBIS-IP_DeviceManagementService_V2.1.xsd")
SYSTEM_DOC_XSD = Path("IBIS-IP_SystemDocumentationService_V2.0.xsd")
SYSTEM_MGMT_XSD = Path("IBIS-IP_SystemManagementService_V1.0.xsd")
COMMON_XSD = Path("IBIS-IP_common_V2.1.xsd")
ENUM_XSD = Path("IBIS-IP_Enumerations_V2.1.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "1f65ee085fec7019bbbb77531b0bc584079a9d8c"
EXPECTED_DMS_BLOB = "191b43e01cdaba14b247725689a913c244a67eed"
EXPECTED_SYSTEM_DOC_BLOB = "ab959dddbfa2b8ca420af1b079501f94cff38051"
EXPECTED_SYSTEM_MGMT_BLOB = "2d32630a0f1981e980e6a466e3f6a69136410f24"
EXPECTED_COMMON_BLOB = "05977c9f86c7c9dd0b48f36a4a4e9be32e94659e"
EXPECTED_ENUM_BLOB = "311464690ad60749ed8d326217787e4b8ed0b718"
FINDING_ID = "DR3012V21-001"
TERMINAL_STATE = "context_verified"


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def main() -> int:
    run_id = os.environ.get("EVIDENCE_RUN_ID", "").strip()
    run_url = os.environ.get("EVIDENCE_RUN_URL", "").strip()
    require(run_id.isdigit(), "EVIDENCE_RUN_ID missing")
    require(run_url.startswith("https://github.com/"), "EVIDENCE_RUN_URL invalid")

    require(blob(FROZEN) == EXPECTED_FROZEN_BLOB, f"frozen inventory changed: {blob(FROZEN)}")
    require(blob(EVIDENCE) == EXPECTED_EVIDENCE_BLOB, f"EV-131 evidence record changed: {blob(EVIDENCE)}")
    require(blob(DMS_XSD) == EXPECTED_DMS_BLOB, f"DMS V2.1 XSD changed: {blob(DMS_XSD)}")
    require(blob(SYSTEM_DOC_XSD) == EXPECTED_SYSTEM_DOC_BLOB, f"SystemDocumentation V2.0 XSD changed: {blob(SYSTEM_DOC_XSD)}")
    require(blob(SYSTEM_MGMT_XSD) == EXPECTED_SYSTEM_MGMT_BLOB, f"SystemManagement V1.0 XSD changed: {blob(SYSTEM_MGMT_XSD)}")
    require(blob(COMMON_XSD) == EXPECTED_COMMON_BLOB, f"Common V2.1 XSD changed: {blob(COMMON_XSD)}")
    require(blob(ENUM_XSD) == EXPECTED_ENUM_BLOB, f"Enumerations V2.1 XSD changed: {blob(ENUM_XSD)}")

    frozen = load(FROZEN)
    require(frozen.get("entry_count") == 192 and frozen.get("state") == "frozen", "frozen inventory invariant failed")
    require(FINDING_ID in frozen.get("finding_ids", []), f"{FINDING_ID} missing from frozen inventory")

    evidence = load(EVIDENCE)
    require(evidence.get("evidence_id") == "EV-131", "unexpected evidence ID")
    require(evidence.get("evidence_run_id") == "33781385699", "pinned EV-131 evidence run changed")
    require(evidence.get("result") == "PASS", "EV-131 evidence record is not PASS")
    require(evidence.get("artifact", {}).get("id") == "9903719333", "EV-131 artifact ID changed")
    require(evidence.get("artifact", {}).get("digest") == "sha256:b0fdcb3705e5e95158545d099845184a1effe9b57647011881bb35fdf94df2d8", "EV-131 artifact digest changed")
    require(evidence.get("finding") == {FINDING_ID: TERMINAL_STATE}, "EV-131 terminal recommendation changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-131 mutation invariant failed")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory count changed")
    require(registry.get("next_revalidation_block") == "VDV301-2", f"unexpected next block {registry.get('next_revalidation_block')}")
    blocks = registry.get("revalidation_blocks", {})
    require("VDV301-2_BASE_V2.0" in blocks, "VDV301-2 Base V2.0 prerequisite closure missing")
    require("VDV301-2_BASE_V2.1" not in blocks, "VDV301-2 Base V2.1 already closed")

    by_id = {item.get("finding_id"): item for item in entries}
    item = by_id.get(FINDING_ID)
    require(item is not None, f"missing registry entry {FINDING_ID}")
    require(item.get("revalidation_state") == "pending", f"{FINDING_ID} is not pending")
    require(item.get("terminal_state_source") is None, f"{FINDING_ID} already has terminal source")
    item["revalidation_state"] = TERMINAL_STATE
    item["terminal_state_source"] = str(REPORT)

    terminal = sum(1 for entry in entries if entry.get("revalidation_state") != "pending")
    pending = sum(1 for entry in entries if entry.get("revalidation_state") == "pending")
    require((terminal, pending) == (76, 116), f"unexpected closure counts terminal={terminal} pending={pending}")

    registry["next_revalidation_block"] = "VDV301-2"
    blocks["VDV301-2_BASE_V2.1"] = {
        "date": "2026-09-03",
        "state": "completed",
        "parent_block": "VDV301-2",
        "authority_lane": "byte-pinned official VDV301-2 Base V2.1 PDF plus byte-identical official VDV-301-2.1 mixed XSD route and official source-catalog identities for the referenced service numbers",
        "official_pdf_source_id": "VDV301-2_BASE_V2.1",
        "pdf_sha256": "685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a",
        "pdf_size_bytes": 2671005,
        "device_management_xsd_blob": EXPECTED_DMS_BLOB,
        "system_documentation_xsd_blob": EXPECTED_SYSTEM_DOC_BLOB,
        "system_management_xsd_blob": EXPECTED_SYSTEM_MGMT_BLOB,
        "common_v21_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_v21_xsd_blob": EXPECTED_ENUM_BLOB,
        "evidence_id": "EV-131",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": "33781385699",
        "artifact_id": "9903719333",
        "artifact_digest": "sha256:b0fdcb3705e5e95158545d099845184a1effe9b57647011881bb35fdf94df2d8",
        "evidence_record": str(EVIDENCE),
        "findings": {FINDING_ID: TERMINAL_STATE},
        "terminal_state_source": str(REPORT),
        "executable_evidence_reason_not_applicable": evidence.get("executable_evidence_reason_not_applicable"),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "VDV301-2",
        "next_subblock": "VDV301-2_GC_V2.2"
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE inventory count changed")
    require(audit.get("finding_revalidation_completed_findings") == 75, f"unexpected pre-V2.1 completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 117, f"unexpected pre-V2.1 pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "VDV301-2", "CURRENT_STATE next block is not VDV301-2")
    require(audit.get("finding_revalidation_latest_completed_block") == "VDV301-2_BASE_V2.0", "prior completed block is not VDV301-2_BASE_V2.0")

    audit["finding_revalidation_next_block"] = "VDV301-2"
    audit["finding_revalidation_completed_findings"] = 76
    audit["finding_revalidation_pending_findings"] = 116
    audit["finding_revalidation_current_block"] = "VDV301-2_BASE_V2.1"
    audit["finding_revalidation_latest_completed_block"] = "VDV301-2_BASE_V2.1"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-131"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["vdv3012_v21_revalidation"] = {
        "status": "complete",
        "evidence_id": "EV-131",
        "run_id": run_id,
        "pinned_successful_evidence_run": "33781385699",
        "artifact_id": "9903719333",
        "artifact_digest": "sha256:b0fdcb3705e5e95158545d099845184a1effe9b57647011881bb35fdf94df2d8",
        "terminal_states": {FINDING_ID: TERMINAL_STATE},
        "next_block": "VDV301-2",
        "next_subblock": "VDV301-2_GC_V2.2",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False
    }

    report = f"""# Finding revalidation — VDV 301-2 Base V2.1\n\nStatus: **completed** on 2026-09-03 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen legacy entry: `DR3012V21-001`. The frozen inventory remains exactly **192 entries**. Persistent older Base-Service findings are not duplicated here; this closure changes only the V2.1-specific frozen finding.\n\n## Evidence\n\n- Evidence gate: **EV-131**, closure workflow run **{run_id}**; independently pinned successful evidence run **33781385699**.\n- Official VDV301-2 Base V2.1 PDF SHA-256: `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`, size `2671005` bytes.\n- EV-131 visual artifact: **9903719333**, digest `sha256:b0fdcb3705e5e95158545d099845184a1effe9b57647011881bb35fdf94df2d8`.\n- Targeted visible pages: 59, 60, 69, 70, 75, 76.\n- Exact official VDV-301-2.1 mixed route: DMS 2.1 `{EXPECTED_DMS_BLOB}`, SystemDocumentation 2.0 `{EXPECTED_SYSTEM_DOC_BLOB}`, SystemManagement 1.0 `{EXPECTED_SYSTEM_MGMT_BLOB}`.\n- DMS 2.1 dependencies are Common 2.1 `{EXPECTED_COMMON_BLOB}` and Enumerations 2.1 `{EXPECTED_ENUM_BLOB}`.\n- Root XSD pool regression gate rerun after EV-131.\n\n## Terminal state\n\n| Finding | Terminal state | Result |\n|---|---|---|\n| DR3012V21-001 | `context_verified` | Base V2.1 prose repeatedly routes DeviceManagementService to `VDV 301-2-2` and SystemDocumentationService to `VDV 301-2-4`. The official source catalog assigns 301-2-2 to BeaconLocationService and 301-2-4 to DistanceLocationService, while the exact VDV-301-2.1 release tag directly supplies the mixed DMS/SystemDocumentation/SystemManagement schema family. The prose numbers are stale and must not drive schema routing. |\n\n## Evidence interpretation\n\nThis is a documentation/routing defect, not an XML-validity defect. No artificial negative XML instance is created. The service XSDs are compiled to establish the exact authority route; the active disproof is the conflicting official document identity of 301-2-2 and 301-2-4.\n\nV2.1 also visibly fixes some V2.0-only issues (for example the missing SubscribeDeviceInformation subsection), while other earlier defects persist. Those histories remain attached to their existing finding IDs and are not counted again in this subblock.\n\n## Closure\n\n- Frozen legacy terminal count: **76 / 192**\n- Frozen legacy pending count: **116 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next top-level revalidation block: **VDV301-2**\n- Next VDV301-2 subblock: **General Conventions V2.2**\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED VDV301-2 Base V2.1: terminal={terminal} pending={pending} next=VDV301-2/GC-V2.2 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
