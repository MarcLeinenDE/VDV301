#!/usr/bin/env python3
"""Fail-closed closure writer for COMMON V2.1 finding DRCOM21-001."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/common_v21_revalidation_evidence_2026-09-04.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.1.md")
DELTA = Path("audit_registry/deep_read_findings_delta_common_v21_2026-09-02.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_COMMON_V21_2026-09-04.md")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "83aeb33c8a290b4ab045a8b74e4b8e67194040d7"
EXPECTED_DEEP_READ_BLOB = "91cf693217d3b0df5309a0f8a242cfd4895a59fa"
EXPECTED_DELTA_BLOB = "44e06e66b65d7a7909d0e37ac3e6657f94e6a092"
EXPECTED_COMMON_BLOB = "05977c9f86c7c9dd0b48f36a4a4e9be32e94659e"
EXPECTED_ENUM_BLOB = "311464690ad60749ed8d326217787e4b8ed0b718"
EXPECTED_EV119_BLOB = "fb892931b74d32a69177fbe32356a08fc758534a"
EXPECTED_EV137_BLOB = "e88731f35970b2f0147a8d60ca546d6165a43ccd"
FINDING = "DRCOM21-001"
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
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        DELTA: EXPECTED_DELTA_BLOB,
        Path("IBIS-IP_common_V2.1.xsd"): EXPECTED_COMMON_BLOB,
        Path("IBIS-IP_Enumerations_V2.1.xsd"): EXPECTED_ENUM_BLOB,
        Path("tools/validate_common_v21_ev119.py"): EXPECTED_EV119_BLOB,
        Path("tools/validate_common_v21_revalidation_ev137.py"): EXPECTED_EV137_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file(), f"missing immutable authority/evidence {path}")
        observed = git_blob(path)
        require(observed == expected, f"immutable blob changed for {path}: {observed}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen", "finding inventory is not frozen")
    require(frozen.get("entry_count") == 192, "frozen finding count is not 192")
    require(FINDING in frozen.get("finding_ids", []), f"{FINDING} missing from frozen inventory")

    evidence = load(EVIDENCE)
    require(evidence.get("evidence_id") == "EV-137", "unexpected evidence id")
    require(evidence.get("result") == "PASS", "EV-137 permanent evidence is not PASS")
    require(evidence.get("pdf", {}).get("visual_review_status") == "completed_from_EV-137_rendered_page_29", "EV-137 visual review incomplete")
    finding_record = evidence.get("finding", {})
    require(finding_record.get("id") == FINDING, "EV-137 finding id changed")
    require(finding_record.get("terminal_state") == TERMINAL_STATE, "EV-137 terminal recommendation changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-137 reports mutation")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen", "registry inventory is not frozen")
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry frozen inventory size changed")
    require(registry.get("next_revalidation_block") == "COMMON", f"unexpected next block {registry.get('next_revalidation_block')}")
    prev = registry.get("revalidation_blocks", {}).get("COMMON_V2.0", {})
    require(prev.get("state") == "completed" and prev.get("next_subblock") == "COMMON_V2.1", "COMMON V2.0 closure route changed")
    require("COMMON_V2.1" not in registry.get("revalidation_blocks", {}), "COMMON V2.1 already closed")

    by_id = {item.get("finding_id"): item for item in entries}
    require(FINDING in by_id, f"missing registry entry {FINDING}")
    item = by_id[FINDING]
    require(item.get("revalidation_state") == "pending", f"{FINDING} is not pending: {item.get('revalidation_state')}")
    require(item.get("terminal_state_source") is None, f"{FINDING} already has terminal source")
    require(by_id.get("DRCOM22-001", {}).get("revalidation_state") == "pending", "COMMON V2.2 next finding is not pending")

    item["revalidation_state"] = TERMINAL_STATE
    item["terminal_state_source"] = str(REPORT)

    terminal_count = sum(1 for x in entries if x.get("revalidation_state") != "pending")
    pending_count = sum(1 for x in entries if x.get("revalidation_state") == "pending")
    require(terminal_count == 93, f"post-COMMON-V2.1 terminal count must be 93, got {terminal_count}")
    require(pending_count == 99, f"post-COMMON-V2.1 pending count must be 99, got {pending_count}")

    registry["next_revalidation_block"] = "COMMON"
    registry.setdefault("revalidation_blocks", {})["COMMON_V2.1"] = {
        "date": "2026-09-04",
        "state": "completed",
        "parent_block": "COMMON",
        "authority_lane": "byte-pinned official Common V2.1 PDF plus exact official VDV-301-2.1 Common/Enumerations XSD family",
        "official_pdf_source_id": "COMMON_V2.1",
        "pdf_sha256": "a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32",
        "pdf_size_bytes": 1274051,
        "official_release_tag": "VDV-301-2.1",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "base_evidence_id": "EV-119",
        "evidence_id": "EV-137",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": "33856800289",
        "artifact_id": "9930503494",
        "artifact_digest": "sha256:3e28953401560f104c075128928a17931666e0d0ec8ef5deb6f23f79f8e775d6",
        "evidence_record": str(EVIDENCE),
        "visual_page": 29,
        "findings": {FINDING: TERMINAL_STATE},
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "COMMON",
        "next_subblock": "COMMON_V2.2"
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE frozen count changed")
    require(audit.get("finding_revalidation_completed_findings") == 92, f"unexpected pre-COMMON-V2.1 completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 100, f"unexpected pre-COMMON-V2.1 pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "COMMON", f"unexpected CURRENT_STATE next block {audit.get('finding_revalidation_next_block')}")
    require(audit.get("finding_revalidation_latest_completed_block") == "COMMON_V2.0", f"unexpected prior completed block {audit.get('finding_revalidation_latest_completed_block')}")

    audit["finding_revalidation_next_block"] = "COMMON"
    audit["finding_revalidation_completed_findings"] = 93
    audit["finding_revalidation_pending_findings"] = 99
    audit["finding_revalidation_current_block"] = "COMMON_V2.1"
    audit["finding_revalidation_latest_completed_block"] = "COMMON_V2.1"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-137"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["common_v21_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-137",
        "run_id": run_id,
        "pinned_successful_evidence_run": "33856800289",
        "artifact_id": "9930503494",
        "artifact_digest": "sha256:3e28953401560f104c075128928a17931666e0d0ec8ef5deb6f23f79f8e775d6",
        "terminal_states": {FINDING: TERMINAL_STATE},
        "next_block": "COMMON",
        "next_subblock": "COMMON_V2.2",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False
    }

    report = f"""# Finding revalidation — COMMON V2.1\n\nStatus: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen legacy finding: `DRCOM21-001`. The frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Byte-pinned official Common V2.1 PDF: SHA-256 `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32`, 1274051 bytes.\n- Exact official XSD authority: tag `VDV-301-2.1`.\n- Common V2.1 blob: `{EXPECTED_COMMON_BLOB}`.\n- Enumerations V2.1 blob: `{EXPECTED_ENUM_BLOB}`.\n- Frozen observation mapping: `FR-COM21-OBS-013` -> `DRCOM21-001`.\n- Preserved base evidence **EV-119** was rerun unchanged and passed.\n- Current revalidation evidence: **EV-137**, closure run **{run_id}**; pinned visual/evidence run **33856800289**, artifact **9930503494**.\n- Page 29 was rendered from the exact pinned PDF and inspected visually.\n- Root XSD pool and tracked-mutation guards passed before closure.\n\n## Terminal state\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n| DRCOM21-001 | `executable_confirmed` | Page 29 visibly specifies `StopInformationRequest.StopName 0:1`; exact V2.1 XSD declares `minOccurs=0 maxOccurs=unbounded`; preserved EV-119 validates an instance containing two `StopName` entries. |\n\nThe strongest disproof hypothesis — that the PDF 0:1 maximum is merely non-executable prose compatible with the XSD — is rejected because the exact XSD demonstrably accepts an instance shape beyond that visible maximum.\n\n## Closure\n\n- Frozen legacy terminal count: **93 / 192**\n- Frozen legacy pending count: **99 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next revalidation block: **COMMON**\n- Next subblock: **COMMON V2.2** (`DRCOM22-001`)\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED COMMON V2.1: terminal={terminal_count} pending={pending_count} next=COMMON_V2.2 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
