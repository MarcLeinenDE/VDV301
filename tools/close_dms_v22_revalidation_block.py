#!/usr/bin/env python3
"""Fail-closed closure writer for frozen DMS V2.2 findings DRDMS22-001..004."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/dms_v22_revalidation_evidence_2026-09-05.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/DMS_V2.2.md")
DELTA = Path("audit_registry/deep_read_findings_delta_dms_v22_2026-08-28.json")
REGISTRY_DELTA = Path("audit_registry/deep_read_registry_delta_dms_v22_2026-08-28.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_DMS_V22_2026-09-05.md")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "4d755389e4db598d0d1dfb13eed4af3f9a064010"
EXPECTED_DEEP_READ_BLOB = "009243f56e8a81e9fdac82ff96d0fb714c7ba45b"
EXPECTED_DELTA_BLOB = "e350612884c8c22ca7fc0e4839a03ac924abc076"
EXPECTED_REGISTRY_DELTA_BLOB = "d44cc214ebd85172579065b8091d2e91d9dbb4a4"
EXPECTED_DMS_BLOB = "c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d"
EXPECTED_COMMON_BLOB = "468fee6d177e7185dbcd5d3f90cfb114e29e01ae"
EXPECTED_ENUM_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"
EXPECTED_EV107_BLOB = "6acd2dc75131455e220ae18ce5131eeb5ad44789"
EXPECTED_EV141_INITIAL_BLOB = "9c3bfe506709f2ee11003ce2ddaa4ccbeaf8cb2f"
EXPECTED_EV141_FINAL_BLOB = "cd89c37f6bcc3f3279ac19fa557c89eb824cf964"

TERMINAL_STATES = {
    "DRDMS22-001": "context_verified",
    "DRDMS22-002": "context_verified",
    "DRDMS22-003": "executable_confirmed",
    "DRDMS22-004": "context_verified",
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

    immutable = {
        FROZEN: EXPECTED_FROZEN_BLOB,
        EVIDENCE: EXPECTED_EVIDENCE_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        DELTA: EXPECTED_DELTA_BLOB,
        REGISTRY_DELTA: EXPECTED_REGISTRY_DELTA_BLOB,
        Path("IBIS-IP_DeviceManagementService_V2.2.xsd"): EXPECTED_DMS_BLOB,
        Path("IBIS-IP_common_V2.2.xsd"): EXPECTED_COMMON_BLOB,
        Path("IBIS-IP_Enumerations_V2.2.xsd"): EXPECTED_ENUM_BLOB,
        Path("tools/validate_dms_v22_deep_read_ev107.py"): EXPECTED_EV107_BLOB,
        Path("tools/validate_dms_v22_revalidation_ev141.py"): EXPECTED_EV141_INITIAL_BLOB,
        Path("tools/validate_dms_v22_revalidation_ev141_final.py"): EXPECTED_EV141_FINAL_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file(), f"missing immutable authority/evidence {path}")
        observed = git_blob(path)
        require(observed == expected, f"immutable blob changed for {path}: {observed}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory invariant failed")
    for fid in TERMINAL_STATES:
        require(fid in frozen.get("finding_ids", []), f"{fid} missing from frozen inventory")

    evidence = load(EVIDENCE)
    require(evidence.get("evidence_id") == "EV-141" and evidence.get("result") == "PASS", "EV-141 permanent evidence is not PASS")
    require(evidence.get("visual_review_status") == "completed_all_EV-141_discovered_pages", "EV-141 visual review incomplete")
    require(evidence.get("successful_run_id") == "33974267275", "EV-141 successful run changed")
    require(evidence.get("artifact_id") == "9971840037", "EV-141 artifact id changed")
    require(evidence.get("artifact_digest") == "sha256:ea779d9299761142a250bdbf5a42730794f13881999deb5f69240690a9701b8a", "EV-141 artifact digest changed")
    authority = evidence.get("authority", {})
    require(authority.get("status") == "official_historical_DMS_V2.2_exact_XSD_family", "EV-141 authority lane changed")
    require(authority.get("latest_xsd_wins") is False and authority.get("later_v24_candidate_corrections_back_applied") is False, "EV-141 version-route guard changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-141 reports mutation")
    findings_evidence = evidence.get("findings", {})
    for fid, state in TERMINAL_STATES.items():
        require(findings_evidence.get(fid, {}).get("terminal_state") == state, f"EV-141 terminal state changed for {fid}")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen" and inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory invariant failed")
    require(registry.get("next_revalidation_block") == "DMS", f"unexpected next block {registry.get('next_revalidation_block')}")
    blocks = registry.get("revalidation_blocks", {})
    require(blocks.get("DMS", {}).get("state") == "completed", "existing legacy DMS block missing or changed")
    common24 = blocks.get("COMMON_V2.4", {})
    require(common24.get("state") == "completed" and common24.get("next_block") == "DMS" and common24.get("next_subblock") == "DMS_V2.2", "COMMON V2.4 closure route changed")
    require("DMS_V2.2" not in blocks, "DMS V2.2 already closed")

    by_id = {item.get("finding_id"): item for item in entries}
    for fid in TERMINAL_STATES:
        item = by_id.get(fid)
        require(item is not None and item.get("revalidation_state") == "pending", f"{fid} is not pending")
        require(item.get("terminal_state_source") is None, f"{fid} already has terminal source")
    require(by_id.get("DRDMS24-001", {}).get("revalidation_state") == "pending", "next DMS V2.4 frozen finding is not pending")

    pre_terminal = sum(x.get("revalidation_state") != "pending" for x in entries)
    pre_pending = sum(x.get("revalidation_state") == "pending" for x in entries)
    require((pre_terminal, pre_pending) == (96, 96), f"pre-DMS-V2.2 counts must be (96,96), got {(pre_terminal,pre_pending)}")

    for fid, terminal_state in TERMINAL_STATES.items():
        by_id[fid]["revalidation_state"] = terminal_state
        by_id[fid]["terminal_state_source"] = str(REPORT)
    terminal_count = sum(x.get("revalidation_state") != "pending" for x in entries)
    pending_count = sum(x.get("revalidation_state") == "pending" for x in entries)
    require((terminal_count, pending_count) == (100, 92), f"post-DMS-V2.2 counts must be (100,92), got {(terminal_count,pending_count)}")

    registry["next_revalidation_block"] = "DMS"
    blocks["DMS_V2.2"] = {
        "date": "2026-09-05",
        "state": "completed",
        "parent_block": "DMS",
        "scope_kind": "post_freeze_deep_read_findings_subblock",
        "authority_lane": "byte-pinned official DMS V2.2 PDF plus exact official historical DMS V2.2/Common V2.2/Enumerations V2.2 XSD family; later V2.4 candidate corrections are not back-applied",
        "official_pdf_source_id": "DMS_V2.2",
        "pdf_sha256": "72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e",
        "pdf_size_bytes": 1173719,
        "pdf_page_count": 36,
        "device_management_xsd_blob": EXPECTED_DMS_BLOB,
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "latest_xsd_wins": False,
        "base_evidence_id": "EV-107",
        "evidence_id": "EV-141",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": "33974267275",
        "failed_closed_attempt_run": "33974145598",
        "artifact_id": "9971840037",
        "artifact_digest": "sha256:ea779d9299761142a250bdbf5a42730794f13881999deb5f69240690a9701b8a",
        "evidence_record": str(EVIDENCE),
        "visual_pages": [7, 19, 23, 24, 26, 28, 29, 30, 32, 33],
        "findings": dict(TERMINAL_STATES),
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "existing_legacy_DMS_block_mutated": False,
        "next_block": "DMS",
        "next_subblock": "DMS_V2.4"
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE frozen count changed")
    require(audit.get("finding_revalidation_completed_findings") == 96, f"unexpected pre-DMS-V2.2 completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 96, f"unexpected pre-DMS-V2.2 pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "DMS", f"unexpected CURRENT_STATE next block {audit.get('finding_revalidation_next_block')}")
    require(audit.get("finding_revalidation_latest_completed_block") == "COMMON_V2.4", f"unexpected prior completed block {audit.get('finding_revalidation_latest_completed_block')}")
    require(audit.get("dms_revalidation", {}).get("status") == "complete", "existing legacy DMS current-state record missing")
    require("dms_v22_deep_revalidation" not in audit, "DMS V2.2 current-state record already exists")

    audit["finding_revalidation_next_block"] = "DMS"
    audit["finding_revalidation_completed_findings"] = 100
    audit["finding_revalidation_pending_findings"] = 92
    audit["finding_revalidation_current_block"] = "DMS_V2.2"
    audit["finding_revalidation_latest_completed_block"] = "DMS_V2.2"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-141"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["dms_v22_deep_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-141",
        "run_id": run_id,
        "pinned_successful_evidence_run": "33974267275",
        "failed_closed_attempt_run": "33974145598",
        "artifact_id": "9971840037",
        "artifact_digest": "sha256:ea779d9299761142a250bdbf5a42730794f13881999deb5f69240690a9701b8a",
        "authority_status": "official_historical_DMS_V2.2_exact_XSD_family",
        "terminal_states": dict(TERMINAL_STATES),
        "next_block": "DMS",
        "next_subblock": "DMS_V2.4",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "existing_legacy_DMS_block_mutated": False
    }

    report = f"""# Finding revalidation — DMS V2.2 deep-read findings\n\nStatus: **completed** on 2026-09-05 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen findings: `DRDMS22-001` … `DRDMS22-004`. The frozen inventory remains exactly **192 entries**. The previously closed legacy `DMS` block (`DMS-001` … `DMS-007`) remains unchanged.\n\n## Authority and evidence\n\n- Byte-pinned official DMS V2.2 PDF: SHA-256 `72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e`, 1173719 bytes, 36 pages.\n- Exact historical DMS V2.2 blob: `{EXPECTED_DMS_BLOB}`.\n- Exact Common V2.2 blob: `{EXPECTED_COMMON_BLOB}`.\n- Exact Enumerations V2.2 blob: `{EXPECTED_ENUM_BLOB}`.\n- Later V2.4 candidate corrections are explanatory history only and are **not** back-applied.\n- Preserved **EV-107** was rerun unchanged and passed.\n- Current evidence: **EV-141**, closure run **{run_id}**; pinned successful evidence run **33974267275**, artifact **9971840037**.\n- Initial EV-141 run **33974145598** failed closed because a service-group member was incorrectly tested as a global root; no finding/evidence/registry state was mutated. The corrected gate tests the actual `DeviceManagementServiceGroup` declaration boundary.\n- All automatically discovered original pages were rendered and visibly inspected: 7, 19, 23, 24, 26, 28, 29, 30, 32, 33.\n- Root XSD pool and tracked-mutation guards passed before closure.\n\n## Terminal states\n\n| Finding | Terminal state | Result |\n|---|---|---|\n| DRDMS22-001 | `context_verified` | Table 23 visibly points `DeviceStatusInformation` to table 27, while table 19 and the table index identify `DeviceStatusInformationStructure`; table 27 and the index identify `InstallUpdateRequestStructure`. Documentation cross-reference error only. |\n| DRDMS22-002 | `context_verified` | TOC visibly uses 1.33/1.34/1.35; the body visibly uses 2.33/2.34/2.35. Documentation navigation error only. |\n| DRDMS22-003 | `executable_confirmed` | PDF enumeration table visibly uses `InstallationSuccessful`; update-history prose visibly uses `InstallationSuccessfull`. Exact V2.2 schema validates only `InstallationSuccessful`; typo form is rejected and is not an alias. |\n| DRDMS22-004 | `context_verified` | Section title/schema operation family use plural `GetDeviceErrorMessages`, while request prose visibly says singular `GetDeviceErrorMessage`. Exact service group contains the plural request and no singular alias. |\n\n## Closure\n\n- Frozen legacy terminal count: **100 / 192**\n- Frozen legacy pending count: **92 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Existing legacy DMS block mutation: **none**\n- Next revalidation block: **DMS**\n- Next subblock: **DMS V2.4** (`DRDMS24-001`)\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED DMS V2.2: terminal={terminal_count} pending={pending_count} next=DMS_V2.4 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
