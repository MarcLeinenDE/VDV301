#!/usr/bin/env python3
"""Fail-closed closure writer for VDV301-2 General Conventions V2.4."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/vdv3012_gc24_revalidation_evidence_2026-09-04.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_VDV3012_GC24_2026-09-04.md")
COMMON_XSD = Path("IBIS-IP_common_V2.4.xsd")
ENUM_XSD = Path("IBIS-IP_Enumerations_V2.4.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "82e09d930f3a69c197a695d5ea64d64b56fe92e4"
EXPECTED_COMMON_BLOB = "1946fd37e29ced605654f49ea3d98cd2fbbdc8e4"
EXPECTED_ENUM_BLOB = "2afed8cf23afa91db92b0f043cc5b4ad428b0f25"
PINNED_EVIDENCE_RUN = "33843888080"
ARTIFACT_ID = "9925822375"
ARTIFACT_DIGEST = "sha256:f69b3f678b5f9153aac90c03a1995d1ece7941e5c3db45ec96a55537f16731a2"
TERMINAL_STATES = {
    "DR3012GC24-001": "executable_confirmed",
    "DR3012GC24-002": "context_verified",
    "DR3012GC24-003": "context_verified",
    "DR3012GC24-004": "executable_confirmed",
    "DR3012GC24-005": "context_verified",
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
    require(blob(EVIDENCE) == EXPECTED_EVIDENCE_BLOB, "EV-134 evidence record changed")
    require(blob(COMMON_XSD) == EXPECTED_COMMON_BLOB, "selected Common V2.4 XSD changed")
    require(blob(ENUM_XSD) == EXPECTED_ENUM_BLOB, "selected Enumerations V2.4 XSD changed")

    frozen = load(FROZEN)
    require(frozen.get("entry_count") == 192 and frozen.get("state") == "frozen", "frozen inventory invariant failed")
    for finding_id in TERMINAL_STATES:
        require(finding_id in frozen.get("finding_ids", []), f"missing frozen finding {finding_id}")

    evidence = load(EVIDENCE)
    require(evidence.get("evidence_id") == "EV-134" and evidence.get("result") == "PASS", "EV-134 not PASS")
    require(evidence.get("evidence_run_id") == PINNED_EVIDENCE_RUN, "pinned EV-134 run changed")
    require(str(evidence.get("artifact", {}).get("id")) == ARTIFACT_ID, "EV-134 artifact ID changed")
    require(evidence.get("artifact", {}).get("digest") == ARTIFACT_DIGEST, "EV-134 artifact digest changed")
    require(evidence.get("pdf", {}).get("visual_review_status") == "completed_from_EV-134_rendered_PNGs", "EV-134 visual review incomplete")
    require(evidence.get("findings") == TERMINAL_STATES, "EV-134 terminal map changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-134 mutation invariant failed")

    authority = evidence.get("authority", {})
    require(authority.get("status") == "candidate_integration_explicit_selection", "V2.4 authority lane changed")
    require(authority.get("official_release_tag") is None, "unexpected official V2.4 release tag")
    require(authority.get("upstream_draft_pr") == "VDVde/VDV301#31", "V2.4 upstream draft provenance changed")
    require(authority.get("common_blob") == EXPECTED_COMMON_BLOB, "EV-134 Common authority changed")
    require(authority.get("enumerations_blob") == EXPECTED_ENUM_BLOB, "EV-134 Enumerations authority changed")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory count changed")
    require(registry.get("next_revalidation_block") == "VDV301-2", f"unexpected top-level next block {registry.get('next_revalidation_block')}")
    blocks = registry.setdefault("revalidation_blocks", {})
    require("VDV301-2_GC_V2.3" in blocks, "GC V2.3 prerequisite closure missing")
    require("VDV301-2_GC_V2.4" not in blocks, "GC V2.4 already closed")

    by_id = {item.get("finding_id"): item for item in entries}
    for finding_id, terminal_state in TERMINAL_STATES.items():
        item = by_id.get(finding_id)
        require(item is not None, f"missing registry entry {finding_id}")
        require(item.get("revalidation_state") == "pending", f"{finding_id} not pending")
        require(item.get("terminal_state_source") is None, f"{finding_id} already has terminal source")
        item["revalidation_state"] = terminal_state
        item["terminal_state_source"] = str(REPORT)

    # The next not-yet-revalidated deep-read family begins with Common V1.0 deltas.
    for common_id in [f"DRCOM10-{i:03d}" for i in range(1, 8)]:
        require(by_id.get(common_id, {}).get("revalidation_state") == "pending", f"expected next Common V1.0 finding not pending: {common_id}")

    terminal = sum(1 for item in entries if item.get("revalidation_state") != "pending")
    pending = sum(1 for item in entries if item.get("revalidation_state") == "pending")
    require((terminal, pending) == (84, 108), f"unexpected closure counts terminal={terminal} pending={pending}")

    registry["next_revalidation_block"] = "COMMON"
    blocks["VDV301-2_GC_V2.4"] = {
        "date": "2026-09-04",
        "state": "completed",
        "parent_block": "VDV301-2",
        "authority_lane": "byte-pinned official GC V2.4 PDF plus project-frozen candidate/integration Common V2.4 and Enumerations V2.4 authority from upstream draft PR VDVde/VDV301#31; no official V2.4 release tag claimed",
        "official_pdf_source_id": "VDV301-2_GC_V2.4",
        "pdf_sha256": "048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d",
        "pdf_size_bytes": 1767094,
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "upstream_draft_pr": "VDVde/VDV301#31",
        "official_release_tag": None,
        "evidence_id": "EV-134",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": PINNED_EVIDENCE_RUN,
        "artifact_id": ARTIFACT_ID,
        "artifact_digest": ARTIFACT_DIGEST,
        "evidence_record": str(EVIDENCE),
        "findings": TERMINAL_STATES,
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "COMMON",
        "next_subblock": "COMMON_V1.0",
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE inventory count changed")
    require(audit.get("finding_revalidation_completed_findings") == 79, f"unexpected pre-GC24 completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 113, f"unexpected pre-GC24 pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "VDV301-2", "CURRENT_STATE next block is not VDV301-2")
    require(audit.get("finding_revalidation_latest_completed_block") == "VDV301-2_GC_V2.3", "prior completed block is not GC V2.3")

    audit["finding_revalidation_next_block"] = "COMMON"
    audit["finding_revalidation_completed_findings"] = 84
    audit["finding_revalidation_pending_findings"] = 108
    audit["finding_revalidation_current_block"] = "VDV301-2_GC_V2.4"
    audit["finding_revalidation_latest_completed_block"] = "VDV301-2_GC_V2.4"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-134"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["vdv3012_gc24_revalidation"] = {
        "status": "complete",
        "evidence_id": "EV-134",
        "run_id": run_id,
        "pinned_successful_evidence_run": PINNED_EVIDENCE_RUN,
        "artifact_id": ARTIFACT_ID,
        "artifact_digest": ARTIFACT_DIGEST,
        "terminal_states": TERMINAL_STATES,
        "authority_lane": "candidate_integration_explicit_selection",
        "upstream_draft_pr": "VDVde/VDV301#31",
        "official_release_tag": None,
        "next_block": "COMMON",
        "next_subblock": "COMMON_V1.0",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report = f"""# Finding revalidation — VDV 301-2 General Conventions V2.4\n\nStatus: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen V2.4-specific entries: `DR3012GC24-001` … `DR3012GC24-005`. The frozen inventory remains exactly **192 entries**. Older findings that recur in V2.4 are context evidence only and are not counted a second time.\n\n## Evidence\n\n- Evidence gate: **EV-134**, closure workflow run **{run_id}**; pinned successful evidence run **{PINNED_EVIDENCE_RUN}**.\n- Official GC V2.4 PDF SHA-256: `048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d`, size `1767094` bytes.\n- EV-134 artifact: **{ARTIFACT_ID}**, digest `{ARTIFACT_DIGEST}`.\n- All finding pages were rendered at 180 dpi and visually inspected before closure.\n- Selected V2.4 schema authority remains explicitly **candidate/integration**, not an official release tag: Common blob `{EXPECTED_COMMON_BLOB}`, Enumerations blob `{EXPECTED_ENUM_BLOB}`, provenance `VDVde/VDV301#31`.\n- Root XSD pool regression gate and tracked-mutation guard passed.\n\n## Terminal states\n\n| Finding | Terminal state | Result |\n|---|---|---|\n| DR3012GC24-001 | `executable_confirmed` | German PDF uses `OnBordUnit`; English and selected `DeviceClassEnumeration` use `OnBoardUnit`. Positive/negative validation confirms only `OnBoardUnit`. |\n| DR3012GC24-002 | `context_verified` | German numbering duplicates `2.1.1` for IP addresses and subnet masks/gateways; English uses `2.1.1` / `2.1.2`. |\n| DR3012GC24-003 | `context_verified` | English allowed-version-character list visibly duplicates digit `2`; this is documentation residue, not an extension of executable version syntax. |\n| DR3012GC24-004 | `executable_confirmed` | Multiple typo-like service identifiers are visible in examples/glossary, while selected `ServiceNameEnumeration` contains the correct identifiers and executable negative samples reject the typo forms. |\n| DR3012GC24-005 | `context_verified` | The document states there is no common IBIS-IP version, yet later uses stale `Version 1.0 of IBIS-IP` wording. No umbrella schema version is inferred. |\n\n## Context controls\n\n- The V2.3 history numbering defect `DR3012GC23-001` is visibly repaired in V2.4 (`7.2.1` / `7.2.2`).\n- Literal Word cross-reference errors visibly recur in V2.4. This strengthens historical `DR3012GC22-001` context but does not create or terminalize a duplicate frozen finding.\n- The document explicitly states that XSD definitions take precedence over documentation when inconsistent; the audit preserves the selected XSD authority for executable spelling boundaries.\n\n## Closure\n\n- Frozen legacy terminal count: **84 / 192**\n- Frozen legacy pending count: **108 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- VDV301-2 Base/General-Conventions revalidation sequence: **completed through V2.4**\n- Next revalidation block: **COMMON**\n- Next subblock: **COMMON V1.0 (`DRCOM10-001…007`)**\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED GC V2.4: terminal={terminal} pending={pending} next=COMMON/COMMON_V1.0 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
