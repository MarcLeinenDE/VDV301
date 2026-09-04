#!/usr/bin/env python3
"""Fail-closed closure writer for COMMON V2.0 finding DRCOM20-001."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/common_v20_revalidation_evidence_2026-09-04.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.0.md")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_COMMON_V20_2026-09-04.md")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "a76c412e8f16efc57a8f561a02f13bd3d33b757b"
EXPECTED_DEEP_READ_BLOB = "dd436b990a4a80d7c0c2768181a1c3d27befd049"
EXPECTED_COMMON_BLOB = "8608e3dcd665c197c34da7f6ec6af5a3758da164"
EXPECTED_ENUM_BLOB = "27e3c183b00381d959622d13c10543123af8eef6"
EXPECTED_EV118_BLOB = "6db122b1726376b11ac24cfec68dbfbd758b079e"
EXPECTED_EV136_BLOB = "001d5c85aa25db4b0c834bc087d7bd551eb794e3"
FINDING = "DRCOM20-001"
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
        Path("IBIS-IP_common_V2.0.xsd"): EXPECTED_COMMON_BLOB,
        Path("IBIS-IP_Enumerations_V2.0.xsd"): EXPECTED_ENUM_BLOB,
        Path("tools/validate_common_v20_ev118.py"): EXPECTED_EV118_BLOB,
        Path("tools/validate_common_v20_revalidation_ev136.py"): EXPECTED_EV136_BLOB,
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
    require(evidence.get("evidence_id") == "EV-136", "unexpected evidence id")
    require(evidence.get("result") == "PASS", "EV-136 permanent evidence is not PASS")
    require(evidence.get("pdf", {}).get("visual_review_status") == "completed_from_EV-136_rendered_page_13", "EV-136 visual review incomplete")
    finding_record = evidence.get("finding", {})
    require(finding_record.get("id") == FINDING, "EV-136 finding id changed")
    require(finding_record.get("terminal_state") == TERMINAL_STATE, "EV-136 terminal recommendation changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-136 reports mutation")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen", "registry inventory is not frozen")
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry frozen inventory size changed")
    require(registry.get("next_revalidation_block") == "COMMON", f"unexpected next block {registry.get('next_revalidation_block')}")
    prev = registry.get("revalidation_blocks", {}).get("COMMON_V1.0", {})
    require(prev.get("state") == "completed" and prev.get("next_subblock") == "COMMON_V2.0", "COMMON V1.0 closure route changed")
    require("COMMON_V2.0" not in registry.get("revalidation_blocks", {}), "COMMON V2.0 already closed")

    by_id = {item.get("finding_id"): item for item in entries}
    require(FINDING in by_id, f"missing registry entry {FINDING}")
    item = by_id[FINDING]
    require(item.get("revalidation_state") == "pending", f"{FINDING} is not pending: {item.get('revalidation_state')}")
    require(item.get("terminal_state_source") is None, f"{FINDING} already has terminal source")
    require(by_id.get("DRCOM21-001", {}).get("revalidation_state") == "pending", "COMMON V2.1 next finding is not pending")

    item["revalidation_state"] = TERMINAL_STATE
    item["terminal_state_source"] = str(REPORT)

    terminal_count = sum(1 for x in entries if x.get("revalidation_state") != "pending")
    pending_count = sum(1 for x in entries if x.get("revalidation_state") == "pending")
    require(terminal_count == 92, f"post-COMMON-V2.0 terminal count must be 92, got {terminal_count}")
    require(pending_count == 100, f"post-COMMON-V2.0 pending count must be 100, got {pending_count}")

    registry["next_revalidation_block"] = "COMMON"
    registry.setdefault("revalidation_blocks", {})["COMMON_V2.0"] = {
        "date": "2026-09-04",
        "state": "completed",
        "parent_block": "COMMON",
        "authority_lane": "byte-pinned official Common V2.0 PDF plus exact official VDV-301-2.0 Common/Enumerations XSD family",
        "official_pdf_source_id": "COMMON_V2.0",
        "pdf_sha256": "23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088",
        "pdf_size_bytes": 946088,
        "official_release_tag": "VDV-301-2.0",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "base_evidence_id": "EV-118",
        "evidence_id": "EV-136",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": "33851287947",
        "artifact_id": "9928439083",
        "artifact_digest": "sha256:763c065d99a5757202b64256fd883f91568f751316cc997bd56b37c7ba01c568",
        "evidence_record": str(EVIDENCE),
        "visual_page": 13,
        "visual_fallback_reason": "pdftotext line-wraps IBIS-IP.language; exact rendered page 13 visually inspected",
        "findings": {FINDING: TERMINAL_STATE},
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "COMMON",
        "next_subblock": "COMMON_V2.1",
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE frozen count changed")
    require(audit.get("finding_revalidation_completed_findings") == 91, f"unexpected pre-COMMON-V2.0 completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 101, f"unexpected pre-COMMON-V2.0 pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "COMMON", f"unexpected CURRENT_STATE next block {audit.get('finding_revalidation_next_block')}")
    require(audit.get("finding_revalidation_latest_completed_block") == "COMMON_V1.0", f"unexpected prior completed block {audit.get('finding_revalidation_latest_completed_block')}")

    audit["finding_revalidation_next_block"] = "COMMON"
    audit["finding_revalidation_completed_findings"] = 92
    audit["finding_revalidation_pending_findings"] = 100
    audit["finding_revalidation_current_block"] = "COMMON_V2.0"
    audit["finding_revalidation_latest_completed_block"] = "COMMON_V2.0"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-136"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["common_v20_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-136",
        "run_id": run_id,
        "pinned_successful_evidence_run": "33851287947",
        "artifact_id": "9928439083",
        "artifact_digest": "sha256:763c065d99a5757202b64256fd883f91568f751316cc997bd56b37c7ba01c568",
        "terminal_states": {FINDING: TERMINAL_STATE},
        "next_block": "COMMON",
        "next_subblock": "COMMON_V2.1",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report = f"""# Finding revalidation — COMMON V2.0\n\nStatus: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen legacy finding: `DRCOM20-001`. The frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Byte-pinned official Common V2.0 PDF: SHA-256 `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088`, 946088 bytes.\n- Exact official XSD authority: tag `VDV-301-2.0`.\n- Common V2.0 blob: `{EXPECTED_COMMON_BLOB}`.\n- Enumerations V2.0 blob: `{EXPECTED_ENUM_BLOB}`.\n- Preserved base evidence **EV-118** was rerun unchanged and passed.\n- Current revalidation evidence: **EV-136**, closure run **{run_id}**; pinned visual/evidence run **33851287947**, artifact **9928439083**.\n- Page 13 was rendered from the exact pinned PDF and inspected visually because `pdftotext` splits `IBIS-IP.language` across lines.\n- Root XSD pool and tracked-mutation guards passed before closure.\n\n## Terminal state\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n| DRCOM20-001 | `executable_confirmed` | Page 13 visibly types `InternationalTextType.Value` as `IBIS-IP.string` and `Language` as `IBIS-IP.language`; the exact official V2.0 XSD instead declares `xs:string` and `xs:language`. EV-118 confirms the direct primitive instance shape is valid while the literal PDF wrapper-shaped nesting is invalid. |\n\nThe strongest disproof hypothesis — that the PDF type notation could be consumed literally without changing XML instance shape — is therefore rejected by executable validation. The XSD remains the validation authority; no wrapper alias is introduced.\n\n## Closure\n\n- Frozen legacy terminal count: **92 / 192**\n- Frozen legacy pending count: **100 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next revalidation block: **COMMON**\n- Next subblock: **COMMON V2.1** (`DRCOM21-001`)\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED COMMON V2.0: terminal={terminal_count} pending={pending_count} next=COMMON_V2.1 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
