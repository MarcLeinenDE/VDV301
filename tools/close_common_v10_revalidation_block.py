#!/usr/bin/env python3
"""Fail-closed closure writer for COMMON V1.0 findings DRCOM10-001..007."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/common_v10_revalidation_evidence_2026-09-04.json")
DELTA = Path("audit_registry/deep_read_findings_delta_common_v10_2026-08-30.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_COMMON_V10_2026-09-04.md")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "47f40823a50266fdfd79dd5dcb9f96f6221f988f"
EXPECTED_DELTA_BLOB = "da56c957f654c47207908f9a6e0808ecf9928ea1"
EXPECTED_COMMON_BLOB = "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c"
EXPECTED_ENUM_BLOB = "a9bea5bc73003ed91ded8519db06c32c4067831d"
EXPECTED_EV117_BLOB = "5d2b69aabd8de7b69575d6f98e6b6517c4d66fb4"
EXPECTED_EV135_MAIN_BLOB = "8f265f127330cf384b3bac2749ac0c5124626080"
EXPECTED_EV135_RUNNER_BLOB = "c0f2fb021a16e98f41c889ab2372960cdc0431a1"

TERMINAL_STATES = {
    "DRCOM10-001": "executable_confirmed",
    "DRCOM10-002": "executable_confirmed",
    "DRCOM10-003": "executable_confirmed",
    "DRCOM10-004": "executable_confirmed",
    "DRCOM10-005": "executable_confirmed",
    "DRCOM10-006": "executable_confirmed",
    "DRCOM10-007": "context_verified",
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
        DELTA: EXPECTED_DELTA_BLOB,
        Path("IBIS-IP_common_V1.0.xsd"): EXPECTED_COMMON_BLOB,
        Path("IBIS-IP_Enumerations_V1.0.xsd"): EXPECTED_ENUM_BLOB,
        Path("tools/validate_common_v10_ev117.py"): EXPECTED_EV117_BLOB,
        Path("tools/validate_common_v10_revalidation_ev135.py"): EXPECTED_EV135_MAIN_BLOB,
        Path("tools/run_common_v10_revalidation_ev135.py"): EXPECTED_EV135_RUNNER_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file(), f"missing immutable authority/evidence {path}")
        observed = git_blob(path)
        require(observed == expected, f"immutable blob changed for {path}: {observed}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen", "finding inventory is not frozen")
    require(frozen.get("entry_count") == 192, "frozen finding count is not 192")
    require(all(fid in frozen.get("finding_ids", []) for fid in TERMINAL_STATES), "one or more COMMON V1.0 finding IDs missing from frozen inventory")

    evidence = load(EVIDENCE)
    require(evidence.get("evidence_id") == "EV-135", "unexpected evidence id")
    require(evidence.get("result") == "PASS", "EV-135 permanent evidence is not PASS")
    require(evidence.get("pdf", {}).get("visual_review_status") == "completed_from_EV-135_rendered_PNGs", "EV-135 visual review is not complete")
    require(evidence.get("findings") == TERMINAL_STATES, "EV-135 terminal recommendations changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-135 reports mutation")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen", "registry inventory is not frozen")
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry frozen inventory size changed")
    require(registry.get("next_revalidation_block") == "COMMON", f"unexpected next block {registry.get('next_revalidation_block')}")
    require("COMMON_V1.0" not in registry.get("revalidation_blocks", {}), "COMMON V1.0 already closed")

    by_id = {item.get("finding_id"): item for item in entries}
    for finding_id, terminal_state in TERMINAL_STATES.items():
        require(finding_id in by_id, f"missing registry entry {finding_id}")
        item = by_id[finding_id]
        require(item.get("revalidation_state") == "pending", f"{finding_id} is not pending: {item.get('revalidation_state')}")
        require(item.get("terminal_state_source") is None, f"{finding_id} already has terminal source")
        item["revalidation_state"] = terminal_state
        item["terminal_state_source"] = str(REPORT)

    require(by_id.get("DRCOM20-001", {}).get("revalidation_state") == "pending", "COMMON V2.0 next finding is not pending")

    terminal_count = sum(1 for item in entries if item.get("revalidation_state") != "pending")
    pending_count = sum(1 for item in entries if item.get("revalidation_state") == "pending")
    require(terminal_count == 91, f"post-COMMON-V1.0 terminal count must be 91, got {terminal_count}")
    require(pending_count == 101, f"post-COMMON-V1.0 pending count must be 101, got {pending_count}")

    registry["next_revalidation_block"] = "COMMON"
    registry.setdefault("revalidation_blocks", {})["COMMON_V1.0"] = {
        "date": "2026-09-04",
        "state": "completed",
        "parent_block": "COMMON",
        "authority_lane": "byte-pinned official Common V1.0 PDF plus exact official historical Common V1.0 / Enumerations V1.0 XSD family from VDVde/VDV301 import commit 604a5a5c7608977e483072f7e450d7381cc182e4",
        "official_pdf_source_id": "COMMON_V1.0",
        "pdf_sha256": "a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf",
        "pdf_size_bytes": 892769,
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "official_import_commit": "604a5a5c7608977e483072f7e450d7381cc182e4",
        "common_v1_1_xsd_found": False,
        "base_evidence_id": "EV-117",
        "evidence_id": "EV-135",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": "33850418941",
        "artifact_id": "9928121371",
        "artifact_digest": "sha256:8c2e42238577f29bb9f79e8de31692db739d8cf89fe13d4532d7c92cac500acf",
        "evidence_record": str(EVIDENCE),
        "visual_page_fallbacks": {
            "DRCOM10-002": 9,
            "DRCOM10-005": 18,
        },
        "findings": TERMINAL_STATES,
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "COMMON",
        "next_subblock": "COMMON_V2.0",
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE frozen count changed")
    require(audit.get("finding_revalidation_completed_findings") == 84, f"unexpected pre-COMMON-V1.0 completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 108, f"unexpected pre-COMMON-V1.0 pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "COMMON", f"unexpected CURRENT_STATE next block {audit.get('finding_revalidation_next_block')}")
    require(audit.get("finding_revalidation_latest_completed_block") == "VDV301-2_GC_V2.4", f"unexpected prior completed block {audit.get('finding_revalidation_latest_completed_block')}")

    audit["finding_revalidation_next_block"] = "COMMON"
    audit["finding_revalidation_completed_findings"] = 91
    audit["finding_revalidation_pending_findings"] = 101
    audit["finding_revalidation_current_block"] = "COMMON_V1.0"
    audit["finding_revalidation_latest_completed_block"] = "COMMON_V1.0"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-135"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["common_v10_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-135",
        "run_id": run_id,
        "pinned_successful_evidence_run": "33850418941",
        "artifact_id": "9928121371",
        "artifact_digest": "sha256:8c2e42238577f29bb9f79e8de31692db739d8cf89fe13d4532d7c92cac500acf",
        "terminal_states": TERMINAL_STATES,
        "next_block": "COMMON",
        "next_subblock": "COMMON_V2.0",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report = f"""# Finding revalidation — COMMON V1.0\n\nStatus: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen legacy findings: `DRCOM10-001` … `DRCOM10-007`. The frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Byte-pinned official Common V1.0 PDF: SHA-256 `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf`, 892769 bytes.\n- Exact official historical Common V1.0 blob: `{EXPECTED_COMMON_BLOB}`.\n- Exact official historical Enumerations V1.0 blob: `{EXPECTED_ENUM_BLOB}`.\n- Historical upstream import commit: `604a5a5c7608977e483072f7e450d7381cc182e4`.\n- No synthetic Common V1.1 XSD authority is inferred from the document's internal Version 1.1 history.\n- Preserved EV-117 was rerun unchanged and passed.\n- Current evidence: **EV-135**, successful closure rerun **{run_id}**; pinned visual/evidence artifact run **33850418941**, artifact **9928121371**.\n- Visual page fallbacks are explicit, not inferred text matches: DRCOM10-002 page 9 and DRCOM10-005 page 18.\n- Root XSD pool and tracked-mutation guards passed before closure.\n\n## Terminal states\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n| DRCOM10-001 | `executable_confirmed` | Document Version 1.1 changes are visibly present, while the exact V1.0 XSD remains the historical authority. Required DisplayContent/legacy spelling boundaries and absence of V1.1 aliases/additions are executable-confirmed. |\n| DRCOM10-002 | `executable_confirmed` | PDF page 9 prints the two DataAcceptedResponse branches as ordinary rows; exact XSD uses `xs:choice`. Either branch validates alone and both together are rejected. |\n| DRCOM10-003 | `executable_confirmed` | PDF prints ServiceSpecificationWithStateList as `1:*`; exact XSD is `0:*`, and an empty list validates. |\n| DRCOM10-004 | `executable_confirmed` | PDF prints JourneyStopInformation Announcement/FareZone as `0:*`; exact XSD is `0:1`. One validates and two repeated instances are rejected for both fields. |\n| DRCOM10-005 | `executable_confirmed` | PDF page 18 uses inner `ShortTripStopList` / `StopPointTariffInformation`; exact XSD uses `ShortTripStop` / `ShortTripStopStructure`. The child-name boundary is executable-confirmed; the two type alternatives are instance-shape equivalent and therefore not overstated as a separate instance distinction. |\n| DRCOM10-006 | `executable_confirmed` | PDF `Wheelchair` / `Others` differ from exact enum lexemes `WheelChair` / `Other`; positive/negative enum probes confirm the boundary. |\n| DRCOM10-007 | `context_verified` | Grouped editorial spelling/naming residue is visibly confirmed and does not define XML validity behavior or aliases. |\n\n## Closure\n\n- Frozen legacy terminal count: **91 / 192**\n- Frozen legacy pending count: **101 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next revalidation block: **COMMON**\n- Next subblock: **COMMON V2.0** (`DRCOM20-001`)\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")

    print(f"CLOSED COMMON V1.0: terminal={terminal_count} pending={pending_count} next=COMMON_V2.0 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
