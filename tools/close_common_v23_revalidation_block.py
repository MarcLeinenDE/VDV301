#!/usr/bin/env python3
"""Fail-closed closure writer for COMMON V2.3 finding DRCOM23-001."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/common_v23_revalidation_evidence_2026-09-04.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.3_FRESH_2026-09-02.md")
DELTA = Path("audit_registry/deep_read_findings_delta_common_v23_2026-09-02.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_COMMON_V23_2026-09-04.md")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "ce4bcc52ad6497cae9ed9d88ab695f77c5650c5e"
EXPECTED_DEEP_READ_BLOB = "cf6060cc9639de64edacdfa84a4cb336fc28c0e6"
EXPECTED_DELTA_BLOB = "2bf1f8555ecad4c050d78750dd7326dd28c9484a"
EXPECTED_COMMON_BLOB = "0d8926c4063c12de9a5e68b6f0addaab35a55dc1"
EXPECTED_ENUM_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"
EXPECTED_EV121_BLOB = "79a55a6eed8eacdc2f853b4380a987beea14b40c"
EXPECTED_EV139_BLOB = "0b920d09df1d873ba8e2fa623fd3ee402b139fcd"
FINDING = "DRCOM23-001"
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
        Path("IBIS-IP_common_V2.3.xsd"): EXPECTED_COMMON_BLOB,
        Path("IBIS-IP_Enumerations_V2.2.xsd"): EXPECTED_ENUM_BLOB,
        Path("tools/validate_common_v23_ev121.py"): EXPECTED_EV121_BLOB,
        Path("tools/validate_common_v23_revalidation_ev139.py"): EXPECTED_EV139_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file(), f"missing immutable authority/evidence {path}")
        observed = git_blob(path)
        require(observed == expected, f"immutable blob changed for {path}: {observed}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen finding inventory invariant failed")
    require(FINDING in frozen.get("finding_ids", []), f"{FINDING} missing from frozen inventory")

    evidence = load(EVIDENCE)
    require(evidence.get("evidence_id") == "EV-139" and evidence.get("result") == "PASS", "EV-139 permanent evidence is not PASS")
    require(evidence.get("pdf", {}).get("visual_review_status") == "completed_from_EV-139_rendered_page_32", "EV-139 visual review incomplete")
    finding_record = evidence.get("finding", {})
    require(finding_record.get("id") == FINDING and finding_record.get("terminal_state") == TERMINAL_STATE, "EV-139 terminal record changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-139 reports mutation")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen" and inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory invariant failed")
    require(registry.get("next_revalidation_block") == "COMMON", f"unexpected next block {registry.get('next_revalidation_block')}")
    prev = registry.get("revalidation_blocks", {}).get("COMMON_V2.2", {})
    require(prev.get("state") == "completed" and prev.get("next_subblock") == "COMMON_V2.3", "COMMON V2.2 closure route changed")
    require("COMMON_V2.3" not in registry.get("revalidation_blocks", {}), "COMMON V2.3 already closed")

    by_id = {item.get("finding_id"): item for item in entries}
    item = by_id.get(FINDING)
    require(item is not None and item.get("revalidation_state") == "pending", f"{FINDING} is not pending")
    require(item.get("terminal_state_source") is None, f"{FINDING} already has terminal source")
    require(by_id.get("DRCOM24-001", {}).get("revalidation_state") == "pending", "COMMON V2.4 next finding is not pending")

    item["revalidation_state"] = TERMINAL_STATE
    item["terminal_state_source"] = str(REPORT)
    terminal_count = sum(x.get("revalidation_state") != "pending" for x in entries)
    pending_count = sum(x.get("revalidation_state") == "pending" for x in entries)
    require((terminal_count, pending_count) == (95, 97), f"post-COMMON-V2.3 counts must be (95,97), got {(terminal_count,pending_count)}")

    registry["next_revalidation_block"] = "COMMON"
    registry.setdefault("revalidation_blocks", {})["COMMON_V2.3"] = {
        "date": "2026-09-04",
        "state": "completed",
        "parent_block": "COMMON",
        "authority_lane": "byte-pinned official Common V2.3 PDF plus exact official VDV-301-2.3 Common schema and its declared Enumerations V2.2",
        "official_pdf_source_id": "COMMON_V2.3",
        "pdf_sha256": "d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b",
        "pdf_size_bytes": 793521,
        "official_release_tag": "VDV-301-2.3",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_file": "IBIS-IP_Enumerations_V2.2.xsd",
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "base_evidence_id": "EV-121",
        "evidence_id": "EV-139",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": "33857687723",
        "artifact_id": "9930843755",
        "artifact_digest": "sha256:8fd840cf40abfcfb2ac1e7c75e25eb52ccfd961ad6d977d54a86e992239d74a7",
        "evidence_record": str(EVIDENCE),
        "visual_page": 32,
        "findings": {FINDING: TERMINAL_STATE},
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "COMMON",
        "next_subblock": "COMMON_V2.4"
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE frozen count changed")
    require(audit.get("finding_revalidation_completed_findings") == 94, f"unexpected pre-COMMON-V2.3 completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 98, f"unexpected pre-COMMON-V2.3 pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "COMMON", f"unexpected CURRENT_STATE next block {audit.get('finding_revalidation_next_block')}")
    require(audit.get("finding_revalidation_latest_completed_block") == "COMMON_V2.2", f"unexpected prior completed block {audit.get('finding_revalidation_latest_completed_block')}")

    audit["finding_revalidation_next_block"] = "COMMON"
    audit["finding_revalidation_completed_findings"] = 95
    audit["finding_revalidation_pending_findings"] = 97
    audit["finding_revalidation_current_block"] = "COMMON_V2.3"
    audit["finding_revalidation_latest_completed_block"] = "COMMON_V2.3"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-139"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["common_v23_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-139",
        "run_id": run_id,
        "pinned_successful_evidence_run": "33857687723",
        "artifact_id": "9930843755",
        "artifact_digest": "sha256:8fd840cf40abfcfb2ac1e7c75e25eb52ccfd961ad6d977d54a86e992239d74a7",
        "terminal_states": {FINDING: TERMINAL_STATE},
        "next_block": "COMMON",
        "next_subblock": "COMMON_V2.4",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False
    }

    report = f"""# Finding revalidation — COMMON V2.3\n\nStatus: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen legacy finding: `DRCOM23-001`. The frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Byte-pinned official Common V2.3 PDF: SHA-256 `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`, 793521 bytes.\n- Exact official authority tag: `VDV-301-2.3`.\n- Common V2.3 blob: `{EXPECTED_COMMON_BLOB}`.\n- The official Common V2.3 schema explicitly includes Enumerations V2.2 blob `{EXPECTED_ENUM_BLOB}`.\n- Frozen observation mapping: `FR-COM23-011` -> `DRCOM23-001` (plus the pre-existing `DRCOM21-001` StopName facet).\n- Preserved base evidence **EV-121** was rerun unchanged and passed.\n- Current revalidation evidence: **EV-139**, closure run **{run_id}**; pinned visual/evidence run **33857687723**, artifact **9930843755**.\n- The exact PDF was searched for the complete `StopInformationRequest` + `ArrivalExpected` + `DepartureExpected` table anchor; page 32 was uniquely selected, rendered, and visibly inspected.\n- Root XSD pool and tracked-mutation guards passed before closure.\n\n## Terminal state\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n| DRCOM23-001 | `executable_confirmed` | PDF page 32 visibly documents `ArrivalExpected 0:1` and `DepartureExpected 0:1` in `StopInformationRequest`; exact V2.3 XSD contains neither there. Preserved EV-121 rejects either request field and accepts both in `StopInformationStructure`. |\n\nThe strongest disproof hypothesis — that the expected-time fields are merely described in the wrong table while remaining accepted by the request schema — is rejected by executable validation.\n\n## Closure\n\n- Frozen legacy terminal count: **95 / 192**\n- Frozen legacy pending count: **97 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next revalidation block: **COMMON**\n- Next subblock: **COMMON V2.4** (`DRCOM24-001`)\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED COMMON V2.3: terminal={terminal_count} pending={pending_count} next=COMMON_V2.4 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
