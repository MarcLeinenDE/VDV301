#!/usr/bin/env python3
"""Fail-closed closure writer for VDV301-2 General Conventions V2.2."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/vdv3012_gc22_revalidation_evidence_2026-09-03.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_VDV3012_GC22_2026-09-03.md")
COMMON_XSD = Path("IBIS-IP_common_V2.2.xsd")
ENUM_XSD = Path("IBIS-IP_Enumerations_V2.2.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "54931eb6c161f7cba3861d59f533a32e931f4b26"
EXPECTED_COMMON_BLOB = "468fee6d177e7185dbcd5d3f90cfb114e29e01ae"
EXPECTED_ENUM_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"
TERMINAL_STATES = {
    "DR3012GC22-001": "context_verified",
    "DR3012GC22-002": "context_verified",
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

    require(blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory changed")
    require(blob(EVIDENCE) == EXPECTED_EVIDENCE_BLOB, "EV-132 evidence record changed")
    require(blob(COMMON_XSD) == EXPECTED_COMMON_BLOB, "Common V2.2 XSD changed")
    require(blob(ENUM_XSD) == EXPECTED_ENUM_BLOB, "Enumerations V2.2 XSD changed")

    frozen = load(FROZEN)
    require(frozen.get("entry_count") == 192 and frozen.get("state") == "frozen", "frozen inventory invariant failed")
    for finding_id in TERMINAL_STATES:
        require(finding_id in frozen.get("finding_ids", []), f"missing frozen finding {finding_id}")

    evidence = load(EVIDENCE)
    require(evidence.get("evidence_id") == "EV-132" and evidence.get("result") == "PASS", "EV-132 not PASS")
    require(evidence.get("evidence_run_id") == "33782124756", "pinned EV-132 run changed")
    require(evidence.get("artifact", {}).get("id") == "9903986586", "EV-132 artifact ID changed")
    require(evidence.get("artifact", {}).get("digest") == "sha256:18dcb5126dd299eef76fd4a73bb6cf73be3ab653b460495a3511e212e474a7f7", "EV-132 artifact digest changed")
    require(evidence.get("findings") == TERMINAL_STATES, "EV-132 terminal map changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-132 mutation invariant failed")

    registry = load(REGISTRY)
    entries = registry.get("inventory", {}).get("entries", [])
    require(len(entries) == 192 and registry.get("inventory", {}).get("entry_count") == 192, "registry inventory count changed")
    require(registry.get("next_revalidation_block") == "VDV301-2", "unexpected next block")
    blocks = registry.setdefault("revalidation_blocks", {})
    require("VDV301-2_BASE_V2.1" in blocks, "V2.1 prerequisite closure missing")
    require("VDV301-2_GC_V2.2" not in blocks, "GC V2.2 already closed")

    by_id = {x.get("finding_id"): x for x in entries}
    for finding_id, terminal_state in TERMINAL_STATES.items():
        item = by_id.get(finding_id)
        require(item is not None, f"missing registry entry {finding_id}")
        require(item.get("revalidation_state") == "pending", f"{finding_id} not pending")
        require(item.get("terminal_state_source") is None, f"{finding_id} already has terminal source")
        item["revalidation_state"] = terminal_state
        item["terminal_state_source"] = str(REPORT)

    terminal = sum(1 for x in entries if x.get("revalidation_state") != "pending")
    pending = sum(1 for x in entries if x.get("revalidation_state") == "pending")
    require((terminal, pending) == (78, 114), f"unexpected counts {terminal}/{pending}")

    blocks["VDV301-2_GC_V2.2"] = {
        "date": "2026-09-03",
        "state": "completed",
        "parent_block": "VDV301-2",
        "authority_lane": "byte-pinned official VDV301-2 General Conventions V2.2 PDF plus byte-identical official VDV-301-2.2 Common/Enumerations release context",
        "official_pdf_source_id": "VDV301-2_GC_V2.2",
        "pdf_sha256": "96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051",
        "pdf_size_bytes": 1562305,
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "evidence_id": "EV-132",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": "33782124756",
        "artifact_id": "9903986586",
        "artifact_digest": "sha256:18dcb5126dd299eef76fd4a73bb6cf73be3ab653b460495a3511e212e474a7f7",
        "evidence_record": str(EVIDENCE),
        "findings": TERMINAL_STATES,
        "terminal_state_source": str(REPORT),
        "executable_evidence_reason_not_applicable": evidence.get("executable_evidence_reason_not_applicable"),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "VDV301-2",
        "next_subblock": "VDV301-2_GC_V2.3"
    }
    registry["next_revalidation_block"] = "VDV301-2"

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE inventory count changed")
    require(audit.get("finding_revalidation_completed_findings") == 76, "unexpected pre-GC22 completed count")
    require(audit.get("finding_revalidation_pending_findings") == 116, "unexpected pre-GC22 pending count")
    require(audit.get("finding_revalidation_latest_completed_block") == "VDV301-2_BASE_V2.1", "prior block mismatch")

    audit["finding_revalidation_next_block"] = "VDV301-2"
    audit["finding_revalidation_completed_findings"] = 78
    audit["finding_revalidation_pending_findings"] = 114
    audit["finding_revalidation_current_block"] = "VDV301-2_GC_V2.2"
    audit["finding_revalidation_latest_completed_block"] = "VDV301-2_GC_V2.2"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-132"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["vdv3012_gc22_revalidation"] = {
        "status": "complete",
        "evidence_id": "EV-132",
        "run_id": run_id,
        "pinned_successful_evidence_run": "33782124756",
        "artifact_id": "9903986586",
        "artifact_digest": "sha256:18dcb5126dd299eef76fd4a73bb6cf73be3ab653b460495a3511e212e474a7f7",
        "terminal_states": TERMINAL_STATES,
        "next_block": "VDV301-2",
        "next_subblock": "VDV301-2_GC_V2.3",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False
    }

    report = f"""# Finding revalidation — VDV 301-2 General Conventions V2.2\n\nStatus: **completed** on 2026-09-03 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen V2.2-specific entries: `DR3012GC22-001` and `DR3012GC22-002`. The frozen inventory remains exactly **192 entries**. Older findings that persist into V2.2 are historical support only and are not counted again.\n\n## Evidence\n\n- Evidence gate: **EV-132**, closure workflow run **{run_id}**; pinned successful evidence run **33782124756**.\n- Official GC V2.2 PDF SHA-256: `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051`, size `1562305` bytes.\n- EV-132 artifact: **9903986586**, digest `sha256:18dcb5126dd299eef76fd4a73bb6cf73be3ab653b460495a3511e212e474a7f7`.\n- Targeted visible pages: 5, 6, 13, 25, 27, 31, 33, 52, 62, 64, 66, 70.\n- Exact VDV-301-2.2 Common blob `{EXPECTED_COMMON_BLOB}` and Enumerations blob `{EXPECTED_ENUM_BLOB}`.\n- Root XSD pool regression gate rerun after EV-132.\n\n## Terminal states\n\n| Finding | Terminal state | Result |\n|---|---|---|\n| DR3012GC22-001 | `context_verified` | Literal unresolved Word-reference placeholders occur independently in multiple contexts/pages. The V2.2 history nevertheless states technical corrections `Keine/none`. |\n| DR3012GC22-002 | `context_verified` | German TOC/body number both SRV and TXT as `3.3.1`; the adjacent English track consistently uses `3.3.1` for SRV and `3.3.2` for TXT, ruling out an intentional shared-number convention. |\n\nBoth findings are documentation/navigation defects and do not alter XML validity.\n\n## Closure\n\n- Frozen legacy terminal count: **78 / 192**\n- Frozen legacy pending count: **114 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next top-level block: **VDV301-2**\n- Next subblock: **General Conventions V2.3**\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED GC V2.2: terminal={terminal} pending={pending} next=VDV301-2/GC-V2.3 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
