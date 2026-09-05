#!/usr/bin/env python3
"""Fail-closed closure writer for frozen DMS V2.4 finding DRDMS24-001."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/dms_v24_revalidation_evidence_2026-09-05.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/DMS_V2.4.md")
DELTA = Path("audit_registry/deep_read_findings_delta_dms_v24_2026-08-28.json")
REGISTRY_DELTA = Path("audit_registry/deep_read_registry_delta_dms_v24_2026-08-28.json")
DOOR_DELTA = Path("audit_registry/deep_read_findings_delta_door_v21_2026-08-29.json")
DOOR_REGISTRY_DELTA = Path("audit_registry/deep_read_registry_delta_door_v21_2026-08-29.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_DMS_V24_2026-09-05.md")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "7fc23edbfafd9d3e507679f015ad36ffc02e2fd0"
EXPECTED_DEEP_READ_BLOB = "dba69e23579186f1c6c26451f93d9f04ba5728b3"
EXPECTED_DELTA_BLOB = "3e07eec98384744b113cb25c37916c67ac23cc6f"
EXPECTED_REGISTRY_DELTA_BLOB = "edffb50eeb6e12c7eae8f6d5fcac3e6566482adc"
EXPECTED_DOOR_DELTA_BLOB = "5daf0521652097d141947ccba6811b22e66e2468"
EXPECTED_DOOR_REGISTRY_DELTA_BLOB = "47a0f7ab3c9004bbfd2e01819194718b356c107f"
EXPECTED_DMS_BLOB = "d222dfd98b2be3777576388da7ace8f333d24c3f"
EXPECTED_COMMON_BLOB = "1946fd37e29ced605654f49ea3d98cd2fbbdc8e4"
EXPECTED_ENUM_BLOB = "2afed8cf23afa91db92b0f043cc5b4ad428b0f25"
EXPECTED_EV108_BLOB = "6a88fbc6546d73d9f68936889087a8120b118358"
EXPECTED_EV142_BLOB = "e7a97dd9d705a8a7d578cc5794a4c3841a5509d5"
FINDING = "DRDMS24-001"
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


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def main() -> int:
    run_id = os.environ.get("EVIDENCE_RUN_ID", "").strip()
    run_url = os.environ.get("EVIDENCE_RUN_URL", "").strip()
    require(run_id.isdigit(), "EVIDENCE_RUN_ID must be the successful closure workflow run id")
    require(run_url.startswith("https://github.com/"), "EVIDENCE_RUN_URL missing or invalid")

    immutable = {
        FROZEN: EXPECTED_FROZEN_BLOB,
        EVIDENCE: EXPECTED_EVIDENCE_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        DELTA: EXPECTED_DELTA_BLOB,
        REGISTRY_DELTA: EXPECTED_REGISTRY_DELTA_BLOB,
        DOOR_DELTA: EXPECTED_DOOR_DELTA_BLOB,
        DOOR_REGISTRY_DELTA: EXPECTED_DOOR_REGISTRY_DELTA_BLOB,
        Path("IBIS-IP_DeviceManagementService_V2.4.xsd"): EXPECTED_DMS_BLOB,
        Path("IBIS-IP_common_V2.4.xsd"): EXPECTED_COMMON_BLOB,
        Path("IBIS-IP_Enumerations_V2.4.xsd"): EXPECTED_ENUM_BLOB,
        Path("tools/validate_dms_v24_deep_read_ev108.py"): EXPECTED_EV108_BLOB,
        Path("tools/validate_dms_v24_revalidation_ev142.py"): EXPECTED_EV142_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file(), f"missing immutable authority/evidence {path}")
        observed = git_blob(path)
        require(observed == expected, f"immutable blob changed for {path}: {observed}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory invariant failed")
    require(FINDING in frozen.get("finding_ids", []), f"{FINDING} missing from frozen inventory")
    for fid in ("DRDOOR21-001", "DRDOOR21-002"):
        require(fid in frozen.get("finding_ids", []), f"next DOOR finding {fid} missing from frozen inventory")

    evidence = load(EVIDENCE)
    require(evidence.get("evidence_id") == "EV-142" and evidence.get("result") == "PASS", "EV-142 permanent evidence is not PASS")
    require(evidence.get("successful_run_id") == "33976298388", "EV-142 successful run changed")
    require(evidence.get("artifact_id") == "9972412891", "EV-142 artifact id changed")
    require(evidence.get("artifact_digest") == "sha256:55caffc0755707a4b8b0f5f18d2b344e3bc89eb6721ca3870c8aebdb59aece63", "EV-142 artifact digest changed")
    pdf = evidence.get("pdf", {})
    require(pdf.get("source_id") == "DMS_V2.4" and pdf.get("visual_review_status") == "completed_from_EV-142_rendered_pages_1_3_4", "EV-142 visual review incomplete or source changed")
    authority = evidence.get("authority", {})
    require(authority.get("pdf_authority") == "official_public_VDV_writing", "EV-142 PDF authority changed")
    require(authority.get("xsd_authority") == "candidate_or_integration_material_in_dev_schema_integration", "EV-142 candidate XSD authority changed")
    require(authority.get("official_release_xsd_claimed") is False and authority.get("latest_xsd_wins") is False, "EV-142 candidate/latest-wins guard changed")
    finding_evidence = evidence.get("finding", {})
    require(finding_evidence.get("id") == FINDING and finding_evidence.get("terminal_state") == TERMINAL_STATE, "EV-142 terminal finding record changed")
    require(finding_evidence.get("validation_behavior") == "none; do not infer HTMLDisplay semantics, routes or validation rules for DeviceManagementService", "EV-142 validation behavior changed")
    require(evidence.get("text_gate", {}).get("active_disproof_result") == "rejected_by_visible_foreword_identity_language_plus_HTML_Web_server_purpose_context", "EV-142 active disproof result changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-142 reports mutation")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen" and inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory invariant failed")
    require(registry.get("next_revalidation_block") == "DMS", f"unexpected next block {registry.get('next_revalidation_block')}")
    blocks = registry.get("revalidation_blocks", {})
    legacy_dms_before = copy.deepcopy(blocks.get("DMS"))
    dms22_before = copy.deepcopy(blocks.get("DMS_V2.2"))
    require(isinstance(legacy_dms_before, dict) and legacy_dms_before.get("state") == "completed", "legacy DMS block missing or changed")
    require(isinstance(dms22_before, dict) and dms22_before.get("state") == "completed" and dms22_before.get("next_block") == "DMS" and dms22_before.get("next_subblock") == "DMS_V2.4", "DMS V2.2 closure route changed")
    require("DMS_V2.4" not in blocks, "DMS V2.4 already closed")

    by_id = {item.get("finding_id"): item for item in entries}
    item = by_id.get(FINDING)
    require(item is not None and item.get("revalidation_state") == "pending", f"{FINDING} is not pending")
    require(item.get("terminal_state_source") is None, f"{FINDING} already has terminal source")
    for next_id in ("DRDOOR21-001", "DRDOOR21-002"):
        require(by_id.get(next_id, {}).get("revalidation_state") == "pending", f"next DOOR finding {next_id} is not pending")
        require(by_id.get(next_id, {}).get("terminal_state_source") is None, f"next DOOR finding {next_id} already has terminal source")

    door_delta = load(DOOR_DELTA)
    require(door_delta.get("document_id") == "DOOR_V2.1", "DOOR next-subblock delta document id changed")
    door_new_ids = [x.get("id") for x in door_delta.get("new_findings", [])]
    require(door_new_ids == ["DRDOOR21-001", "DRDOOR21-002"], f"DOOR V2.1 frozen-next finding mapping changed: {door_new_ids}")
    door_reg_delta = load(DOOR_REGISTRY_DELTA)
    require(door_reg_delta.get("document_updates", {}).get("DOOR_V2.1", {}).get("new_findings") == ["DRDOOR21-001", "DRDOOR21-002"], "DOOR V2.1 registry next-subblock mapping changed")

    pre_terminal = sum(x.get("revalidation_state") != "pending" for x in entries)
    pre_pending = sum(x.get("revalidation_state") == "pending" for x in entries)
    require((pre_terminal, pre_pending) == (100, 92), f"pre-DMS-V2.4 counts must be (100,92), got {(pre_terminal,pre_pending)}")

    item["revalidation_state"] = TERMINAL_STATE
    item["terminal_state_source"] = str(REPORT)
    terminal_count = sum(x.get("revalidation_state") != "pending" for x in entries)
    pending_count = sum(x.get("revalidation_state") == "pending" for x in entries)
    require((terminal_count, pending_count) == (101, 91), f"post-DMS-V2.4 counts must be (101,91), got {(terminal_count,pending_count)}")

    registry["next_revalidation_block"] = "DOOR"
    blocks["DMS_V2.4"] = {
        "date": "2026-09-05",
        "state": "completed",
        "parent_block": "DMS",
        "scope_kind": "post_freeze_deep_read_findings_subblock",
        "authority_lane": "byte-pinned official public DMS V2.4 PDF for documentation evidence plus explicitly candidate/integration DMS V2.4/Common V2.4/Enumerations V2.4 XSD context; no official V2.4 release XSD is claimed",
        "official_pdf_source_id": "DMS_V2.4",
        "pdf_sha256": "347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd",
        "pdf_size_bytes": 1298127,
        "pdf_page_count": 35,
        "pdf_authority": "official_public_VDV_writing",
        "xsd_authority": "candidate_or_integration_material_in_dev_schema_integration",
        "official_release_xsd_claimed": False,
        "device_management_xsd_blob": EXPECTED_DMS_BLOB,
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "latest_xsd_wins": False,
        "base_evidence_id": "EV-108",
        "evidence_id": "EV-142",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": "33976298388",
        "artifact_id": "9972412891",
        "artifact_digest": "sha256:55caffc0755707a4b8b0f5f18d2b344e3bc89eb6721ca3870c8aebdb59aece63",
        "evidence_record": str(EVIDENCE),
        "visual_pages": [1, 3, 4],
        "findings": {FINDING: TERMINAL_STATE},
        "active_disproof_result": "rejected_by_visible_foreword_identity_language_plus_HTML_Web_server_purpose_context",
        "executable_evidence_reason_not_applicable": finding_evidence.get("executable_evidence_reason_not_applicable"),
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "existing_legacy_DMS_block_mutated": False,
        "existing_DMS_V2.2_block_mutated": False,
        "next_block": "DOOR",
        "next_subblock": "DOOR_V2.1"
    }
    require(blocks.get("DMS") == legacy_dms_before, "legacy DMS block was mutated")
    require(blocks.get("DMS_V2.2") == dms22_before, "DMS V2.2 block was mutated")

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE frozen count changed")
    require(audit.get("finding_revalidation_completed_findings") == 100, f"unexpected pre-DMS-V2.4 completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 92, f"unexpected pre-DMS-V2.4 pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "DMS", f"unexpected CURRENT_STATE next block {audit.get('finding_revalidation_next_block')}")
    require(audit.get("finding_revalidation_latest_completed_block") == "DMS_V2.2", f"unexpected prior completed block {audit.get('finding_revalidation_latest_completed_block')}")
    require(audit.get("dms_revalidation", {}).get("status") == "complete", "existing legacy DMS current-state record missing")
    require(audit.get("dms_v22_deep_revalidation", {}).get("status") == "complete", "existing DMS V2.2 current-state record missing")
    require("dms_v24_deep_revalidation" not in audit, "DMS V2.4 current-state record already exists")

    audit["finding_revalidation_next_block"] = "DOOR"
    audit["finding_revalidation_completed_findings"] = 101
    audit["finding_revalidation_pending_findings"] = 91
    audit["finding_revalidation_current_block"] = "DMS_V2.4"
    audit["finding_revalidation_latest_completed_block"] = "DMS_V2.4"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-142"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["dms_v24_deep_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-142",
        "run_id": run_id,
        "pinned_successful_evidence_run": "33976298388",
        "artifact_id": "9972412891",
        "artifact_digest": "sha256:55caffc0755707a4b8b0f5f18d2b344e3bc89eb6721ca3870c8aebdb59aece63",
        "pdf_authority": "official_public_VDV_writing",
        "xsd_authority": "candidate_or_integration_material_in_dev_schema_integration",
        "official_release_xsd_claimed": False,
        "terminal_states": {FINDING: TERMINAL_STATE},
        "next_block": "DOOR",
        "next_subblock": "DOOR_V2.1",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "existing_legacy_DMS_block_mutated": False,
        "existing_DMS_V2.2_block_mutated": False
    }

    report = f"""# Finding revalidation — DMS V2.4 deep-read finding\n\nStatus: **completed** on 2026-09-05 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen finding: `DRDMS24-001`. The frozen inventory remains exactly **192 entries**. The previously closed legacy `DMS` and `DMS_V2.2` blocks remain unchanged.\n\n## Authority and evidence\n\n- Byte-pinned official DMS V2.4 PDF: SHA-256 `347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd`, 1298127 bytes, 35 pages.\n- The PDF is official public VDV writing.\n- The repository DMS V2.4 XSD family remains explicitly **candidate/integration** and is not promoted to official release authority.\n- Candidate DMS V2.4 blob: `{EXPECTED_DMS_BLOB}`.\n- Candidate Common V2.4 blob: `{EXPECTED_COMMON_BLOB}`.\n- Candidate Enumerations V2.4 blob: `{EXPECTED_ENUM_BLOB}`.\n- `latest_xsd_wins=false`.\n- Preserved **EV-108** was rerun unchanged and passed as corroborating structure context only.\n- Current evidence: **EV-142**, closure run **{run_id}**; pinned successful evidence run **33976298388**, artifact **9972412891**.\n- Original PDF pages 1, 3 and 4 were rendered and visibly inspected. Pages 1 and 3 establish `DeviceManagementService V2.4` document identity. Page 4 visibly states in German and English that the document describes `HtmlDisplayService`; the English paragraph additionally carries its URL/web-server/HTML-display purpose.\n- Active disproof attempt: the hypothesis that `HtmlDisplayService` is merely a related-service reference is rejected by the visible document-identity language plus copied service-purpose prose.\n- Root XSD pool and tracked-mutation guards passed before closure.\n\n## Terminal state\n\n| Finding | Terminal state | Result |\n|---|---|---|\n| DRDMS24-001 | `context_verified` | The DMS V2.4 foreword visibly contains copied HtmlDisplayService identity/purpose text despite the publication being DeviceManagementService V2.4. This is documentation-only and creates no HTMLDisplay route, alias or XML validation rule for DMS. |\n\nExecutable XML accept/reject evidence is not applicable to the defect itself because the erroneous foreword does not define XML validity; the candidate XSD execution is supporting service-identity context only.\n\n## Closure\n\n- Frozen legacy terminal count: **101 / 192**\n- Frozen legacy pending count: **91 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Existing legacy DMS block mutation: **none**\n- Existing DMS V2.2 block mutation: **none**\n- DMS deep-read revalidation family: **complete through V2.4**\n- Next revalidation block: **DOOR**\n- Next subblock: **DOOR V2.1** (`DRDOOR21-001..002`)\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED DMS V2.4: terminal={terminal_count} pending={pending_count} next=DOOR_V2.1 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
