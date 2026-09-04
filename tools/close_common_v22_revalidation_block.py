#!/usr/bin/env python3
"""Fail-closed closure writer for COMMON V2.2 finding DRCOM22-001."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/common_v22_revalidation_evidence_2026-09-04.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.2.md")
DELTA = Path("audit_registry/deep_read_findings_delta_common_v22_2026-09-02.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_COMMON_V22_2026-09-04.md")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "f13574bb0e5ec0ec850ed4c22bbd323cc6b54c68"
EXPECTED_DEEP_READ_BLOB = "38e3c3f0f96486acf7aea40652398e00f575a1b4"
EXPECTED_DELTA_BLOB = "6b0208d153761bef6e0cbf0041888251b99cdca4"
EXPECTED_COMMON_BLOB = "468fee6d177e7185dbcd5d3f90cfb114e29e01ae"
EXPECTED_ENUM_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"
EXPECTED_EV120_BLOB = "ca6aa03c50f7f63057e46623df639da77a1b67d7"
EXPECTED_EV138_BLOB = "d488d829a14b16fa8a49ff6749b2e189089a560b"
FINDING = "DRCOM22-001"
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
        Path("IBIS-IP_common_V2.2.xsd"): EXPECTED_COMMON_BLOB,
        Path("IBIS-IP_Enumerations_V2.2.xsd"): EXPECTED_ENUM_BLOB,
        Path("tools/validate_common_v22_ev120.py"): EXPECTED_EV120_BLOB,
        Path("tools/validate_common_v22_revalidation_ev138.py"): EXPECTED_EV138_BLOB,
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
    require(evidence.get("evidence_id") == "EV-138", "unexpected evidence id")
    require(evidence.get("result") == "PASS", "EV-138 permanent evidence is not PASS")
    require(evidence.get("pdf", {}).get("visual_review_status") == "completed_from_EV-138_rendered_page_15", "EV-138 visual review incomplete")
    finding_record = evidence.get("finding", {})
    require(finding_record.get("id") == FINDING, "EV-138 finding id changed")
    require(finding_record.get("terminal_state") == TERMINAL_STATE, "EV-138 terminal recommendation changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-138 reports mutation")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen", "registry inventory is not frozen")
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry frozen inventory size changed")
    require(registry.get("next_revalidation_block") == "COMMON", f"unexpected next block {registry.get('next_revalidation_block')}")
    prev = registry.get("revalidation_blocks", {}).get("COMMON_V2.1", {})
    require(prev.get("state") == "completed" and prev.get("next_subblock") == "COMMON_V2.2", "COMMON V2.1 closure route changed")
    require("COMMON_V2.2" not in registry.get("revalidation_blocks", {}), "COMMON V2.2 already closed")

    by_id = {item.get("finding_id"): item for item in entries}
    require(FINDING in by_id, f"missing registry entry {FINDING}")
    item = by_id[FINDING]
    require(item.get("revalidation_state") == "pending", f"{FINDING} is not pending: {item.get('revalidation_state')}")
    require(item.get("terminal_state_source") is None, f"{FINDING} already has terminal source")
    require(by_id.get("DRCOM23-001", {}).get("revalidation_state") == "pending", "COMMON V2.3 next finding is not pending")

    item["revalidation_state"] = TERMINAL_STATE
    item["terminal_state_source"] = str(REPORT)

    terminal_count = sum(1 for x in entries if x.get("revalidation_state") != "pending")
    pending_count = sum(1 for x in entries if x.get("revalidation_state") == "pending")
    require(terminal_count == 94, f"post-COMMON-V2.2 terminal count must be 94, got {terminal_count}")
    require(pending_count == 98, f"post-COMMON-V2.2 pending count must be 98, got {pending_count}")

    registry["next_revalidation_block"] = "COMMON"
    registry.setdefault("revalidation_blocks", {})["COMMON_V2.2"] = {
        "date": "2026-09-04",
        "state": "completed",
        "parent_block": "COMMON",
        "authority_lane": "byte-pinned official Common V2.2 PDF plus exact historical-upstream V2.2 Common/Enumerations file lineage",
        "official_pdf_source_id": "COMMON_V2.2",
        "pdf_sha256": "85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203",
        "pdf_size_bytes": 1411558,
        "official_release_tag": None,
        "release_tag_status": "no_VDV-301-2.2_tag_resolved_in_upstream_repository",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "common_last_modification_commit": "775def7b24901bfd515c80fa5fe57f12562873fd",
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "enumerations_last_modification_commit": "591ca66d8b94bb5c2a7f9440b3e31e28f8261a88",
        "latest_xsd_wins": False,
        "base_evidence_id": "EV-120",
        "evidence_id": "EV-138",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": "33857241506",
        "artifact_id": "9930671790",
        "artifact_digest": "sha256:43e1dce9285a6295c8a7ef3b92f3a5eb627e6973e2170bd1207242bffe5c0b92",
        "evidence_record": str(EVIDENCE),
        "visual_page": 15,
        "findings": {FINDING: TERMINAL_STATE},
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "COMMON",
        "next_subblock": "COMMON_V2.3"
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE frozen count changed")
    require(audit.get("finding_revalidation_completed_findings") == 93, f"unexpected pre-COMMON-V2.2 completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 99, f"unexpected pre-COMMON-V2.2 pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "COMMON", f"unexpected CURRENT_STATE next block {audit.get('finding_revalidation_next_block')}")
    require(audit.get("finding_revalidation_latest_completed_block") == "COMMON_V2.1", f"unexpected prior completed block {audit.get('finding_revalidation_latest_completed_block')}")

    audit["finding_revalidation_next_block"] = "COMMON"
    audit["finding_revalidation_completed_findings"] = 94
    audit["finding_revalidation_pending_findings"] = 98
    audit["finding_revalidation_current_block"] = "COMMON_V2.2"
    audit["finding_revalidation_latest_completed_block"] = "COMMON_V2.2"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-138"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["common_v22_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-138",
        "run_id": run_id,
        "pinned_successful_evidence_run": "33857241506",
        "artifact_id": "9930671790",
        "artifact_digest": "sha256:43e1dce9285a6295c8a7ef3b92f3a5eb627e6973e2170bd1207242bffe5c0b92",
        "authority_route": "historical_upstream_V2.2_file_lineage_exact_family",
        "terminal_states": {FINDING: TERMINAL_STATE},
        "next_block": "COMMON",
        "next_subblock": "COMMON_V2.3",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False
    }

    report = f"""# Finding revalidation — COMMON V2.2\n\nStatus: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen legacy finding: `DRCOM22-001`. The frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Byte-pinned official Common V2.2 PDF: SHA-256 `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`, 1411558 bytes.\n- No upstream `VDV-301-2.2` release tag is invented.\n- Exact authority route: historical upstream V2.2 file lineage.\n- Common V2.2 blob: `{EXPECTED_COMMON_BLOB}` at last V2.2 file modification `775def7b24901bfd515c80fa5fe57f12562873fd`.\n- Enumerations V2.2 blob: `{EXPECTED_ENUM_BLOB}` at last modification `591ca66d8b94bb5c2a7f9440b3e31e28f8261a88`.\n- Frozen observation mapping: `FR-COM22-002` -> `DRCOM22-001`.\n- Preserved base evidence **EV-120** was rerun unchanged and passed.\n- Current revalidation evidence: **EV-138**, closure run **{run_id}**; pinned visual/evidence run **33857241506**, artifact **9930671790**.\n- Page 15 was rendered from the exact pinned PDF and inspected visually.\n- Root XSD pool and tracked-mutation guards passed before closure.\n\n## Terminal state\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n| DRCOM22-001 | `executable_confirmed` | Page 15 visibly marks both `NetexMode` choice groups as `-1:1` in VDV choice notation; exact historical V2.2 XSD defines two top-level `xs:choice` compositors with `minOccurs=0`; preserved EV-120 validates an empty `NetexMode`. |\n\nThe strongest disproof hypothesis — that the PDF one-of presentation and XSD optional compositors have no executable instance-shape consequence — is rejected by the empty-instance validation.\n\n## Closure\n\n- Frozen legacy terminal count: **94 / 192**\n- Frozen legacy pending count: **98 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next revalidation block: **COMMON**\n- Next subblock: **COMMON V2.3** (`DRCOM23-001`)\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED COMMON V2.2: terminal={terminal_count} pending={pending_count} next=COMMON_V2.3 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
