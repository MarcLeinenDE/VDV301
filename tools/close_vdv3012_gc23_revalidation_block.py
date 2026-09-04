#!/usr/bin/env python3
"""Fail-closed closure writer for VDV301-2 General Conventions V2.3."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/vdv3012_gc23_revalidation_evidence_2026-09-04.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_VDV3012_GC23_2026-09-04.md")
COMMON_XSD = Path("IBIS-IP_common_V2.3.xsd")
ENUM_XSD = Path("IBIS-IP_Enumerations_V2.2.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "604cefcd5f9db5070072ca35b0b0e623a4336a6d"
EXPECTED_COMMON_BLOB = "0d8926c4063c12de9a5e68b6f0addaab35a55dc1"
EXPECTED_ENUM_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"
PINNED_EVIDENCE_RUN = "33842952649"
ARTIFACT_ID = "9925516670"
ARTIFACT_DIGEST = "sha256:7fb77ca6ca5c1950b45d49fe983118831e4cae187997d2568b203e97a89f4b33"
TERMINAL_STATES = {"DR3012GC23-001": "context_verified"}


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
    require(blob(EVIDENCE) == EXPECTED_EVIDENCE_BLOB, "EV-133 evidence record changed")
    require(blob(COMMON_XSD) == EXPECTED_COMMON_BLOB, "Common V2.3 XSD changed")
    require(blob(ENUM_XSD) == EXPECTED_ENUM_BLOB, "Enumerations V2.2 XSD changed")

    frozen = load(FROZEN)
    require(frozen.get("entry_count") == 192 and frozen.get("state") == "frozen", "frozen inventory invariant failed")
    for finding_id in TERMINAL_STATES:
        require(finding_id in frozen.get("finding_ids", []), f"missing frozen finding {finding_id}")

    evidence = load(EVIDENCE)
    require(evidence.get("evidence_id") == "EV-133" and evidence.get("result") == "PASS", "EV-133 not PASS")
    require(evidence.get("evidence_run_id") == PINNED_EVIDENCE_RUN, "pinned EV-133 run changed")
    require(str(evidence.get("artifact", {}).get("id")) == ARTIFACT_ID, "EV-133 artifact ID changed")
    require(evidence.get("artifact", {}).get("digest") == ARTIFACT_DIGEST, "EV-133 artifact digest changed")
    require(evidence.get("pdf", {}).get("visual_review_status") == "confirmed_from_EV-133_rendered_PNGs", "EV-133 visual review incomplete")
    require(evidence.get("findings") == TERMINAL_STATES, "EV-133 terminal map changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-133 mutation invariant failed")

    authority = evidence.get("selected_xsd_authority", {})
    require(authority.get("common_blob") == EXPECTED_COMMON_BLOB, "EV-133 Common authority changed")
    require(authority.get("enumerations_blob") == EXPECTED_ENUM_BLOB, "EV-133 Enumerations authority changed")
    require(authority.get("official_upstream_blobs_identical") is True, "EV-133 upstream identity not confirmed")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory count changed")
    require(registry.get("next_revalidation_block") == "VDV301-2", "unexpected top-level next block")
    blocks = registry.setdefault("revalidation_blocks", {})
    require("VDV301-2_GC_V2.2" in blocks, "GC V2.2 prerequisite closure missing")
    require("VDV301-2_GC_V2.3" not in blocks, "GC V2.3 already closed")

    by_id = {item.get("finding_id"): item for item in entries}
    for finding_id, terminal_state in TERMINAL_STATES.items():
        item = by_id.get(finding_id)
        require(item is not None, f"missing registry entry {finding_id}")
        require(item.get("revalidation_state") == "pending", f"{finding_id} not pending")
        require(item.get("terminal_state_source") is None, f"{finding_id} already has terminal source")
        item["revalidation_state"] = terminal_state
        item["terminal_state_source"] = str(REPORT)

    terminal = sum(1 for item in entries if item.get("revalidation_state") != "pending")
    pending = sum(1 for item in entries if item.get("revalidation_state") == "pending")
    require((terminal, pending) == (79, 113), f"unexpected closure counts terminal={terminal} pending={pending}")

    blocks["VDV301-2_GC_V2.3"] = {
        "date": "2026-09-04",
        "state": "completed",
        "parent_block": "VDV301-2",
        "authority_lane": "byte-pinned official VDV301-2 General Conventions V2.3 PDF plus byte-identical official VDV-301-2.3 Common V2.3 / Enumerations V2.2 release context",
        "official_pdf_source_id": "VDV301-2_GC_V2.3",
        "pdf_sha256": "4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603",
        "pdf_size_bytes": 1057483,
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "evidence_id": "EV-133",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": PINNED_EVIDENCE_RUN,
        "artifact_id": ARTIFACT_ID,
        "artifact_digest": ARTIFACT_DIGEST,
        "evidence_record": str(EVIDENCE),
        "findings": TERMINAL_STATES,
        "terminal_state_source": str(REPORT),
        "executable_evidence_reason_not_applicable": evidence.get("executable_evidence_reason_not_applicable"),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "VDV301-2",
        "next_subblock": "VDV301-2_GC_V2.4"
    }
    registry["next_revalidation_block"] = "VDV301-2"

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE inventory count changed")
    require(audit.get("finding_revalidation_completed_findings") == 78, "unexpected pre-GC23 completed count")
    require(audit.get("finding_revalidation_pending_findings") == 114, "unexpected pre-GC23 pending count")
    require(audit.get("finding_revalidation_latest_completed_block") == "VDV301-2_GC_V2.2", "prior block mismatch")

    audit["finding_revalidation_next_block"] = "VDV301-2"
    audit["finding_revalidation_completed_findings"] = 79
    audit["finding_revalidation_pending_findings"] = 113
    audit["finding_revalidation_current_block"] = "VDV301-2_GC_V2.3"
    audit["finding_revalidation_latest_completed_block"] = "VDV301-2_GC_V2.3"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-133"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["vdv3012_gc23_revalidation"] = {
        "status": "complete",
        "evidence_id": "EV-133",
        "run_id": run_id,
        "pinned_successful_evidence_run": PINNED_EVIDENCE_RUN,
        "artifact_id": ARTIFACT_ID,
        "artifact_digest": ARTIFACT_DIGEST,
        "terminal_states": TERMINAL_STATES,
        "visual_pages": [70, 71],
        "next_block": "VDV301-2",
        "next_subblock": "VDV301-2_GC_V2.4",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False
    }

    report = f"""# Finding revalidation — VDV 301-2 General Conventions V2.3\n\nStatus: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen V2.3-specific entry: `DR3012GC23-001`. The frozen inventory remains exactly **192 entries**. Older findings persisting into V2.3 are historical support only and are not counted again.\n\n## Evidence\n\n- Evidence gate: **EV-133**, closure workflow run **{run_id}**; pinned successful evidence run **{PINNED_EVIDENCE_RUN}**.\n- Official GC V2.3 PDF SHA-256: `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603`, size `1057483` bytes.\n- EV-133 artifact: **{ARTIFACT_ID}**, digest `{ARTIFACT_DIGEST}`.\n- Targeted visible pages: **70 and 71**.\n- Page 70 visibly establishes the predecessor German `7.1.1` / `7.1.2` numbering under `7.1 Version 2.2`.\n- Page 71 visibly shows `7.2 Version 2.3` followed by German `7.1.3` / `7.1.4`, while the adjacent English headings correctly use `7.2.1` / `7.2.2`.\n- Exact official Common V2.3 blob `{EXPECTED_COMMON_BLOB}` and Enumerations V2.2 blob `{EXPECTED_ENUM_BLOB}`.\n- EV-133 also confirms that the literal unresolved Word-reference placeholders from V2.2 are absent in V2.3.\n- Root XSD pool regression gate and tracked-mutation guard passed.\n\n## Terminal state\n\n| Finding | Terminal state | Result |\n|---|---|---|\n| DR3012GC23-001 | `context_verified` | German V2.3 version-history subsection numbers remain in the 7.1 namespace despite being placed under 7.2; the adjacent English track provides a direct same-page corrective control. |\n\nThis is a documentation/navigation defect and does not alter XML instance validity or create an XSD alias.\n\n## Closure\n\n- Frozen legacy terminal count: **79 / 192**\n- Frozen legacy pending count: **113 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next top-level block: **VDV301-2**\n- Next subblock: **General Conventions V2.4 (`DR3012GC24-001…005`)**\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED GC V2.3: terminal={terminal} pending={pending} next=VDV301-2/GC-V2.4 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
