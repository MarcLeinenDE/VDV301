#!/usr/bin/env python3
"""Fail-closed closure writer for DR3011-001..DR3011-003."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
VISUAL = Path("audit_registry/vdv3011_visual_revalidation_evidence_2026-09-03.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_VDV3011_2026-09-03.md")
XSD = Path("IBIS-IP_SystemManagementService_V1.0.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_VISUAL_BLOB = "4bf69c495d96c0c471749f5ad5279c6ab7c2d8d7"
EXPECTED_XSD_BLOB = "2d32630a0f1981e980e6a466e3f6a69136410f24"
TERMINAL_STATES = {
    "DR3011-001": "context_verified",
    "DR3011-002": "context_verified",
    "DR3011-003": "context_verified",
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


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def main() -> int:
    run_id = os.environ.get("EVIDENCE_RUN_ID", "").strip()
    run_url = os.environ.get("EVIDENCE_RUN_URL", "").strip()
    require(run_id.isdigit(), "EVIDENCE_RUN_ID missing")
    require(run_url.startswith("https://github.com/"), "EVIDENCE_RUN_URL invalid")

    require(blob(FROZEN) == EXPECTED_FROZEN_BLOB, f"frozen inventory changed: {blob(FROZEN)}")
    require(blob(VISUAL) == EXPECTED_VISUAL_BLOB, f"VDV301-1 visual evidence changed: {blob(VISUAL)}")
    require(blob(XSD) == EXPECTED_XSD_BLOB, f"SystemManagement V1.0 XSD changed: {blob(XSD)}")

    frozen = load(FROZEN)
    require(frozen.get("entry_count") == 192 and frozen.get("state") == "frozen", "frozen inventory invariant failed")
    for finding_id in TERMINAL_STATES:
        require(finding_id in frozen.get("finding_ids", []), f"{finding_id} missing from frozen inventory")

    visual = load(VISUAL)
    require(visual.get("visual_review_status") == "completed_for_DR3011_001_003", "visual review incomplete")
    require(visual.get("render_run_id") == "33725750019", "visual render run changed")
    require(visual.get("render_artifact_id") == "9881897572", "visual artifact changed")
    require(visual.get("xsd_mutated") is False and visual.get("frozen_inventory_mutated") is False, "visual record mutation invariant failed")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory count changed")
    require(registry.get("next_revalidation_block") == "VDV301-1", f"unexpected next block {registry.get('next_revalidation_block')}")
    require("VDV301-1" not in registry.get("revalidation_blocks", {}), "VDV301-1 already closed")

    by_id = {item.get("finding_id"): item for item in entries}
    for finding_id, terminal_state in TERMINAL_STATES.items():
        item = by_id.get(finding_id)
        require(item is not None, f"missing registry entry {finding_id}")
        require(item.get("revalidation_state") == "pending", f"{finding_id} is not pending")
        require(item.get("terminal_state_source") is None, f"{finding_id} already has terminal source")
        item["revalidation_state"] = terminal_state
        item["terminal_state_source"] = str(REPORT)

    terminal = sum(1 for item in entries if item.get("revalidation_state") != "pending")
    pending = sum(1 for item in entries if item.get("revalidation_state") == "pending")
    require((terminal, pending) == (60, 132), f"unexpected closure counts terminal={terminal} pending={pending}")

    registry["next_revalidation_block"] = "VDV301-2"
    registry.setdefault("revalidation_blocks", {})["VDV301-1"] = {
        "date": "2026-09-03",
        "state": "completed",
        "authority_lane": "official byte-pinned VDV301-1 V1.0 architecture PDF; DR3011-002 additionally cross-checked against official byte-pinned VDV301-2 V1.0 PDF and selected historical SystemManagement V1.0 XSD",
        "official_pdf_source_ids": ["VDV301-1_V1.0_DE", "VDV301-2_V1.0_DE"],
        "part1_pdf_sha256": "5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2",
        "part2_pdf_sha256": "2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75",
        "system_management_xsd_blob": EXPECTED_XSD_BLOB,
        "evidence_id": "EV-128",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "visual_render_run": "33725750019",
        "visual_artifact_id": "9881897572",
        "visual_evidence_record": str(VISUAL),
        "findings": TERMINAL_STATES,
        "terminal_state_source": str(REPORT),
        "executable_evidence_reason_not_applicable": "All three findings are documentation/context issues and do not define XML validity behavior. DR3011-002 explicitly forbids inventing stale Part-1 operation aliases.",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE inventory count changed")
    require(audit.get("finding_revalidation_completed_findings") == 57, f"unexpected pre-VDV301-1 completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 135, f"unexpected pre-VDV301-1 pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "VDV301-1", "CURRENT_STATE next block is not VDV301-1")
    require(audit.get("finding_revalidation_latest_completed_block") == "DMS", "prior completed block is not DMS")

    audit["finding_revalidation_next_block"] = "VDV301-2"
    audit["finding_revalidation_completed_findings"] = 60
    audit["finding_revalidation_pending_findings"] = 132
    audit["finding_revalidation_current_block"] = "VDV301-1"
    audit["finding_revalidation_latest_completed_block"] = "VDV301-1"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-128"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["vdv3011_revalidation"] = {
        "status": "complete",
        "evidence_id": "EV-128",
        "run_id": run_id,
        "visual_render_run_id": "33725750019",
        "visual_artifact_id": "9881897572",
        "terminal_states": TERMINAL_STATES,
        "validation_behavior": "none",
        "next_block": "VDV301-2",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report = f"""# Finding revalidation — VDV 301-1 V1.0\n\nStatus: **completed** on 2026-09-03 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen legacy entries: `DR3011-001` … `DR3011-003`. The frozen inventory remains exactly **192 entries**.\n\n## Evidence\n\n- Evidence gate: **EV-128**, workflow run **{run_id}**.\n- Official Part 1 V1.0 PDF SHA-256: `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2`.\n- Official Part 2 V1.0 PDF SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`.\n- Existing full Part-1 visual render: run **33725750019**, artifact **9881897572**; relevant pages 2, 10, 11 and 34 were re-inspected.\n- `DR3011-002` is additionally cross-checked against the selected historical `IBIS-IP_SystemManagementService_V1.0.xsd`.\n- Root XSD pool regression gate rerun after EV-128.\n\n## Terminal states\n\n| Finding | Terminal state | Result |\n|---|---|---|\n| DR3011-001 | `context_verified` | Page 2 visibly assigns 5.1.2 to System-Dokumentation and 5.1.3 to System-Management; page 10 nevertheless points the SystemManagementService example to 5.1.2. |\n| DR3011-002 | `context_verified` | Part 1 visibly uses stale/conceptual `GetDeviceState` / `GetSystemStatus` / `SystemStatus` subscription names. Official Part 2 V1.0 and the selected historical XSD use `GetDeviceStatus` / `GetServiceStatus` terminology. No aliases are created. |\n| DR3011-003 | `context_verified` | Page 34 visibly contains two consecutive `IBIS-IP` abbreviation rows with slightly different expansion wording. |\n\nAll three are documentation/context findings. They do not alter XML validity behavior and are not promoted into SDK conformance rules.\n\n## Closure\n\n- Frozen legacy terminal count: **60 / 192**\n- Frozen legacy pending count: **132 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next revalidation block: **VDV301-2**\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED VDV301-1: terminal={terminal} pending={pending} next=VDV301-2 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
