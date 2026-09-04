#!/usr/bin/env python3
"""Fail-closed closure writer for COMMON V2.4 finding DRCOM24-001."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/common_v24_revalidation_evidence_2026-09-04.json")
FRESH = Path("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.4_FRESH_2026-09-03.md")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.4.md")
DELTA = Path("audit_registry/deep_read_findings_delta_common_v24_2026-09-03.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_COMMON_V24_2026-09-04.md")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "6eb4cc7a600b6f526c9f4c203afd02ca0de2436b"
EXPECTED_FRESH_BLOB = "1a2f58c60152e14a61257d21a8c2cd4533f2696e"
EXPECTED_DEEP_READ_BLOB = "5800c06781b17775f6763a918568d3e5712210c5"
EXPECTED_DELTA_BLOB = "9744612c607e63659d574c13500cfc611f239f39"
EXPECTED_COMMON_BLOB = "1946fd37e29ced605654f49ea3d98cd2fbbdc8e4"
EXPECTED_ENUM_BLOB = "2afed8cf23afa91db92b0f043cc5b4ad428b0f25"
EXPECTED_EV122_BLOB = "acbca8a808e623030c2ff48bc2e3f3e336cb5f11"
EXPECTED_EV140_BLOB = "75633e50c7de5a469acab226084603dbc0906ae2"
FINDING = "DRCOM24-001"
TERMINAL_STATE = "executable_confirmed"


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
        FRESH: EXPECTED_FRESH_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        DELTA: EXPECTED_DELTA_BLOB,
        Path("IBIS-IP_common_V2.4.xsd"): EXPECTED_COMMON_BLOB,
        Path("IBIS-IP_Enumerations_V2.4.xsd"): EXPECTED_ENUM_BLOB,
        Path("tools/validate_common_v24_ev122.py"): EXPECTED_EV122_BLOB,
        Path("tools/validate_common_v24_revalidation_ev140.py"): EXPECTED_EV140_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file(), f"missing immutable authority/evidence {path}")
        observed = git_blob(path)
        require(observed == expected, f"immutable blob changed for {path}: {observed}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen finding inventory invariant failed")
    require(FINDING in frozen.get("finding_ids", []), f"{FINDING} missing from frozen inventory")

    evidence = load(EVIDENCE)
    require(evidence.get("evidence_id") == "EV-140" and evidence.get("result") == "PASS", "EV-140 permanent evidence is not PASS")
    authority = evidence.get("authority", {})
    require(authority.get("status") == "candidate_integration_explicit_selection", "EV-140 candidate authority status changed")
    require(authority.get("official_release_tag") is None and authority.get("official_release_authority") is False, "EV-140 was incorrectly promoted to official authority")
    require(authority.get("latest_xsd_wins") is False, "EV-140 latest-wins guard changed")
    require(evidence.get("pdf", {}).get("visual_review_status") == "completed_from_EV-140_rendered_page_28", "EV-140 visual review incomplete")
    finding_record = evidence.get("finding", {})
    require(finding_record.get("id") == FINDING and finding_record.get("terminal_state") == TERMINAL_STATE, "EV-140 terminal record changed")
    require(finding_record.get("authority_scope") == "selected_candidate_integration_V2.4_only_until_official_release_exists", "EV-140 authority scope changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-140 reports mutation")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen" and inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory invariant failed")
    require(registry.get("next_revalidation_block") == "COMMON", f"unexpected next block {registry.get('next_revalidation_block')}")
    blocks = registry.get("revalidation_blocks", {})
    prev = blocks.get("COMMON_V2.3", {})
    require(prev.get("state") == "completed" and prev.get("next_subblock") == "COMMON_V2.4", "COMMON V2.3 closure route changed")
    require("COMMON_V2.4" not in blocks, "COMMON V2.4 already closed")
    require(blocks.get("DMS", {}).get("state") == "completed", "existing legacy DMS block unexpectedly missing or changed")
    require("DMS_V2.2" not in blocks, "DMS_V2.2 deep-read subblock already exists")

    by_id = {item.get("finding_id"): item for item in entries}
    item = by_id.get(FINDING)
    require(item is not None and item.get("revalidation_state") == "pending", f"{FINDING} is not pending")
    require(item.get("terminal_state_source") is None, f"{FINDING} already has terminal source")
    for next_id in ("DRDMS22-001", "DRDMS22-002", "DRDMS22-003", "DRDMS22-004"):
        require(by_id.get(next_id, {}).get("revalidation_state") == "pending", f"next DMS V2.2 finding {next_id} is not pending")

    item["revalidation_state"] = TERMINAL_STATE
    item["terminal_state_source"] = str(REPORT)
    terminal_count = sum(x.get("revalidation_state") != "pending" for x in entries)
    pending_count = sum(x.get("revalidation_state") == "pending" for x in entries)
    require((terminal_count, pending_count) == (96, 96), f"post-COMMON-V2.4 counts must be (96,96), got {(terminal_count,pending_count)}")

    registry["next_revalidation_block"] = "DMS"
    blocks["COMMON_V2.4"] = {
        "date": "2026-09-04",
        "state": "completed",
        "parent_block": "COMMON",
        "authority_lane": "byte-pinned official Common V2.4 PDF plus project-frozen candidate/integration Common V2.4 and Enumerations V2.4 authority from upstream draft PR VDVde/VDV301#31; no official V2.4 release tag claimed",
        "official_pdf_source_id": "COMMON_V2.4",
        "pdf_sha256": "01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a",
        "pdf_size_bytes": 1689647,
        "official_release_tag": None,
        "official_release_authority": False,
        "candidate_branch": "candidate/dms-v2.4-xsd",
        "upstream_draft_pr": "VDVde/VDV301#31",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "latest_xsd_wins": False,
        "base_evidence_id": "EV-122",
        "evidence_id": "EV-140",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": "33858121693",
        "artifact_id": "9931012948",
        "artifact_digest": "sha256:1f78c0767d8d610fd41d4edb2211a1e007953daaa2e45abaa5e84caf866a63e4",
        "evidence_record": str(EVIDENCE),
        "visual_page": 28,
        "findings": {FINDING: TERMINAL_STATE},
        "finding_authority_scope": "selected_candidate_integration_V2.4_only_until_official_release_exists",
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "DMS",
        "next_subblock": "DMS_V2.2"
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE frozen count changed")
    require(audit.get("finding_revalidation_completed_findings") == 95, f"unexpected pre-COMMON-V2.4 completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 97, f"unexpected pre-COMMON-V2.4 pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "COMMON", f"unexpected CURRENT_STATE next block {audit.get('finding_revalidation_next_block')}")
    require(audit.get("finding_revalidation_latest_completed_block") == "COMMON_V2.3", f"unexpected prior completed block {audit.get('finding_revalidation_latest_completed_block')}")

    audit["finding_revalidation_next_block"] = "DMS"
    audit["finding_revalidation_completed_findings"] = 96
    audit["finding_revalidation_pending_findings"] = 96
    audit["finding_revalidation_current_block"] = "COMMON_V2.4"
    audit["finding_revalidation_latest_completed_block"] = "COMMON_V2.4"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-140"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["common_v24_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-140",
        "run_id": run_id,
        "pinned_successful_evidence_run": "33858121693",
        "artifact_id": "9931012948",
        "artifact_digest": "sha256:1f78c0767d8d610fd41d4edb2211a1e007953daaa2e45abaa5e84caf866a63e4",
        "authority_status": "candidate_integration_explicit_selection",
        "official_release_authority": False,
        "finding_authority_scope": "selected_candidate_integration_V2.4_only_until_official_release_exists",
        "terminal_states": {FINDING: TERMINAL_STATE},
        "next_block": "DMS",
        "next_subblock": "DMS_V2.2",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False
    }

    report = f"""# Finding revalidation — COMMON V2.4\n\nStatus: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen legacy finding: `DRCOM24-001`. The frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Byte-pinned official Common V2.4 PDF: SHA-256 `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`, 1689647 bytes.\n- Selected XSD authority is **candidate/integration**, not an official V2.4 release.\n- No `VDV-301-2.4` release tag is claimed.\n- Candidate branch: `candidate/dms-v2.4-xsd`; upstream draft provenance: `VDVde/VDV301#31`.\n- Selected Common V2.4 blob: `{EXPECTED_COMMON_BLOB}`.\n- Selected Enumerations V2.4 blob: `{EXPECTED_ENUM_BLOB}`.\n- `latest_xsd_wins=false`; authority remains the explicitly selected frozen candidate route.\n- Frozen observation mapping: `FR-COM24-008` -> `DRCOM24-001`.\n- Preserved base evidence **EV-122** was rerun unchanged and passed.\n- Current revalidation evidence: **EV-140**, closure run **{run_id}**; pinned visual/evidence run **33858121693**, artifact **9931012948**.\n- Page 28 was selected from the exact PDF by the complete `LineInformation`/`LineName`/`LineShortName` table anchors, rendered, and visibly inspected.\n- Root XSD pool and tracked-mutation guards passed before closure.\n\n## Terminal state\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n| DRCOM24-001 | `executable_confirmed` | PDF page 28 visibly documents `LineName` and `LineShortName` as `IBIS-IP.string 0:1`. The selected candidate V2.4 XSD declares both `InternationalTextType 0:*`. Preserved EV-122 confirms candidate InternationalText shapes and repetition as valid and rejects the PDF-derived simple value-only LineName shape. |\n\nThis terminal state is explicitly scoped to `selected_candidate_integration_V2.4_only_until_official_release_exists`; it must not be relabelled as an official VDV-301-2.4 release conclusion.\n\n## Closure\n\n- Frozen legacy terminal count: **96 / 192**\n- Frozen legacy pending count: **96 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- COMMON revalidation family: **complete through V2.4**\n- Next revalidation block: **DMS**\n- Next subblock: **DMS V2.2** (`DRDMS22-001..004`)\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED COMMON V2.4: terminal={terminal_count} pending={pending_count} next=DMS_V2.2 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
