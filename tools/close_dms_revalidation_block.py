#!/usr/bin/env python3
"""Fail-closed closure writer for legacy findings DMS-001..DMS-007.

This script is intentionally narrow.  It may only move the frozen 192-entry
revalidation inventory from the verified DISC state (50/192 terminal) to the
verified DMS state (57/192 terminal).  It never modifies XSD files or the frozen
inventory snapshot itself.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
VISUAL = Path("audit_registry/dms_visual_revalidation_evidence_2026-09-03.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_DMS_2026-09-03.md")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_VISUAL_BLOB = "d7748ed81015f2224155138f89cf259fd6973690"
EXPECTED_DMS_BLOBS = {
    "IBIS-IP_DeviceManagementService_V2.0.xsd": "74189e0da65563eeb084ec2f3c400e9668d1ee1a",
    "IBIS-IP_DeviceManagementService_V2.1.xsd": "191b43e01cdaba14b247725689a913c244a67eed",
    "IBIS-IP_DeviceManagementService_V2.2.xsd": "c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d",
    "IBIS-IP_DeviceManagementService_V2.4.xsd": "d222dfd98b2be3777576388da7ace8f333d24c3f",
}

TERMINAL_STATES = {
    "DMS-001": "context_verified",
    "DMS-002": "context_verified",
    "DMS-003": "executable_confirmed",
    "DMS-004": "executable_confirmed",
    "DMS-005": "context_verified",
    "DMS-006": "executable_confirmed",
    "DMS-007": "context_verified",
}


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

    # Immutable and selected-authority guards.
    require(FROZEN.is_file(), f"missing frozen inventory {FROZEN}")
    require(git_blob(FROZEN) == EXPECTED_FROZEN_BLOB, f"frozen 192-entry inventory blob changed: {git_blob(FROZEN)}")
    require(VISUAL.is_file(), f"missing visual evidence {VISUAL}")
    require(git_blob(VISUAL) == EXPECTED_VISUAL_BLOB, f"DMS visual evidence blob changed: {git_blob(VISUAL)}")
    for path_text, expected in EXPECTED_DMS_BLOBS.items():
        path = Path(path_text)
        require(path.is_file(), f"missing selected DMS XSD {path}")
        observed = git_blob(path)
        require(observed == expected, f"selected DMS XSD blob changed for {path}: {observed}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen", "finding inventory is not frozen")
    require(frozen.get("entry_count") == 192, f"frozen inventory count changed: {frozen.get('entry_count')}")
    require(all(fid in frozen.get("finding_ids", []) for fid in TERMINAL_STATES), "one or more DMS IDs missing from frozen inventory")
    require("DRDMS24-002" not in frozen.get("finding_ids", []), "post-freeze visual delta was incorrectly inserted into frozen inventory")

    visual = load(VISUAL)
    require(visual.get("visual_review_status") == "completed", "DMS visual review is not complete")
    require(visual.get("render_run_id") == "33758274931", "unexpected DMS visual render run")
    require(visual.get("render_artifact_id") == "9894357560", "unexpected DMS visual artifact")
    delta = visual.get("post_freeze_visual_delta", {})
    require(delta.get("id") == "DRDMS24-002", "post-freeze visual delta id changed")
    require(delta.get("state") == "context_verified", "post-freeze visual delta is not terminal")
    require(delta.get("validation_behavior", "").startswith("none;"), "post-freeze visual delta unexpectedly changes validation behavior")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen", "revalidation registry inventory not frozen")
    require(inventory.get("entry_count") == 192, "revalidation registry inventory count is not 192")
    require(len(entries) == 192, f"revalidation registry entries length changed: {len(entries)}")
    require(registry.get("next_revalidation_block") == "DMS", f"unexpected next block: {registry.get('next_revalidation_block')}")
    require("DMS" not in registry.get("revalidation_blocks", {}), "DMS block is already closed")

    by_id = {item.get("finding_id"): item for item in entries}
    for finding_id, terminal_state in TERMINAL_STATES.items():
        require(finding_id in by_id, f"missing registry entry {finding_id}")
        item = by_id[finding_id]
        require(item.get("revalidation_state") == "pending", f"{finding_id} is not pending: {item.get('revalidation_state')}")
        require(item.get("terminal_state_source") is None, f"{finding_id} already has terminal source")
        item["revalidation_state"] = terminal_state
        item["terminal_state_source"] = str(REPORT)

    terminal_count = sum(1 for item in entries if item.get("revalidation_state") != "pending")
    pending_count = sum(1 for item in entries if item.get("revalidation_state") == "pending")
    require(terminal_count == 57, f"post-DMS terminal count must be 57, got {terminal_count}")
    require(pending_count == 135, f"post-DMS pending count must be 135, got {pending_count}")

    registry["next_revalidation_block"] = "VDV301-1"
    registry.setdefault("revalidation_blocks", {})["DMS"] = {
        "date": "2026-09-03",
        "state": "completed",
        "authority_lane": "official byte-pinned VDV PDFs plus exact selected historical XSD families; DMS V2.4 XSD remains candidate/integration authority",
        "official_pdf_source_ids": [
            "VDV301-2_BASE_V2.0",
            "VDV301-2_BASE_V2.1",
            "DMS_V2.2",
            "DMS_V2.4"
        ],
        "selected_service_blobs": EXPECTED_DMS_BLOBS,
        "executable_evidence_id": "EV-127",
        "executable_run_id": run_id,
        "executable_run_url": run_url,
        "executable_checkers": [
            "tools/validate_dms_revalidation_ev127_final.py",
            "tools/validate_dms_instance_boundaries_ev127.py"
        ],
        "visual_render_run": "33758274931",
        "visual_artifact_id": "9894357560",
        "visual_evidence_record": str(VISUAL),
        "post_freeze_visual_delta": {
            "id": "DRDMS24-002",
            "state": "context_verified",
            "validation_behavior": "none",
            "frozen_inventory_mutated": False
        },
        "findings": TERMINAL_STATES,
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE frozen count changed")
    require(audit.get("finding_revalidation_completed_findings") == 50, f"unexpected pre-DMS completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 142, f"unexpected pre-DMS pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "DMS", f"unexpected CURRENT_STATE next block {audit.get('finding_revalidation_next_block')}")
    require(audit.get("finding_revalidation_latest_completed_block") == "DISC", f"unexpected prior completed block {audit.get('finding_revalidation_latest_completed_block')}")

    audit["finding_revalidation_next_block"] = "VDV301-1"
    audit["finding_revalidation_completed_findings"] = 57
    audit["finding_revalidation_pending_findings"] = 135
    audit["finding_revalidation_current_block"] = "DMS"
    audit["finding_revalidation_latest_completed_block"] = "DMS"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-127"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["latest_dms_finding"] = "DRDMS24-002"
    audit["dms_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-127",
        "run_id": run_id,
        "preclosure_validation_run_id": "33761193163",
        "visual_render_run_id": "33758274931",
        "visual_artifact_id": "9894357560",
        "terminal_states": TERMINAL_STATES,
        "post_freeze_visual_delta": "DRDMS24-002_context_verified_documentation_only_no_validation_rule",
        "next_block": "VDV301-1",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False
    }

    report = f"""# Finding revalidation — Device Management Service (DMS)\n\nStatus: **completed** on 2026-09-03 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen legacy inventory entries: `DMS-001` … `DMS-007`.  The frozen inventory remains exactly **192 entries** and is not rewritten by this closure.\n\n## Evidence\n\n- Final executable evidence: **EV-127**, workflow run **{run_id}**.\n- Pre-closure full EV-127 run: **33761193163**, PASS.\n- Independent byte-pinned visual render: run **33758274931**, artifact **9894357560**.\n- Official PDF identities are rechecked against `audit_registry/pdf_source_pins_v0.1.json`.\n- Exact selected DMS service XSD blobs are pinned in `audit_registry/finding_revalidation_registry_v0.1.json`.\n- Positive/negative XML instance boundaries are executed by `tools/validate_dms_instance_boundaries_ev127.py`.\n- Root XSD pool validation is rerun after EV-127.\n\n## Terminal states\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n| DMS-001 | `context_verified` | Historical V2.0 DMS wrapper/service-group asymmetry confirmed. Generic Common subscribe/unsubscribe structures are intentional context and are **not** treated as defects. |\n| DMS-002 | `context_verified` | Repeated unresolved Word cross-reference markers are visibly and textually present in V2.0 and absent in checked V2.1 context. |\n| DMS-003 | `executable_confirmed` | V2.0–V2.2 `ErrorMessage` lower bound `10` is confirmed with 9=reject, 10/11=accept; V2.4 correction `0:*` is confirmed with 0/1=accept. |\n| DMS-004 | `executable_confirmed` | V2.1/V2.2 require UpdateID, UpdateTimestamp and UpdateURL; omission of each is rejected. V2.4 permits the empty optional request as documented. |\n| DMS-005 | `context_verified` | The public PDF visibly uses `DeviceManagementService.DeviceStatusInformationResponseData`; the selected XSD uses `DeviceManagementService.GetDeviceStatusInformationResponseData`. This is a documentation identifier mismatch, so no artificial executable label is assigned. |\n| DMS-006 | `executable_confirmed` | The V2.2 PDF-visible Name+Flag-only shape is rejected by the selected V2.2 XSD; adding required Impact+Priority is accepted. V2.4 accepts the two-field shape after the later optionality correction. |\n| DMS-007 | `context_verified` | PDF prose says `GetUpdateStates`; operation inventory/XSD use `GetUpdateHistory`. No `GetUpdateStates` operation alias is introduced. |\n\n## Post-freeze visual delta\n\nThe independent visual review additionally discovered **`DRDMS24-002`**: DMS V2.4 table 20 visibly prints `eDeviceStatusPriority`, whereas the selected candidate/integration XSD declares `DeviceStatusPriority`.  The delta is recorded additively as `context_verified`, has **no validation behavior**, creates no alias, and does not mutate the frozen 192-entry legacy inventory.\n\n## Closure\n\n- Frozen legacy terminal count: **57 / 192**\n- Frozen legacy pending count: **135 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next revalidation block: **VDV301-1** (`DR3011-001…003`)\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")

    print(f"CLOSED DMS: terminal={terminal_count} pending={pending_count} next=VDV301-1 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
