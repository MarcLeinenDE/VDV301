#!/usr/bin/env python3
"""Fail-closed closure writer for VDV301-2 V1.0 DR3012-001..007."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/vdv3012_v10_revalidation_evidence_2026-09-03.json")
CORRECTION = Path("docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_DR3012_003_V10_IDENTIFIER_TYPE_2026-09-03.md")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_VDV3012_V10_2026-09-03.md")
SYSTEM_DOC_XSD = Path("IBIS-IP_SystemDocumentationService_v1.0.xsd")
SYSTEM_MGMT_XSD = Path("IBIS-IP_SystemManagementService_V1.0.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "2d3d39c2ac5c374a7e43dd768e101c6ead83e44b"
EXPECTED_CORRECTION_BLOB = "7d79087ad3d850af16a6571f2c7a82b1350a8218"
EXPECTED_SYSTEM_DOC_BLOB = "8995c4a230bf81d5e47b9313ee7725ff3cd4b7b5"
EXPECTED_SYSTEM_MGMT_BLOB = "2d32630a0f1981e980e6a466e3f6a69136410f24"
TERMINAL_STATES = {
    "DR3012-001": "context_verified",
    "DR3012-002": "context_verified",
    "DR3012-003": "executable_confirmed",
    "DR3012-004": "context_verified",
    "DR3012-005": "context_verified",
    "DR3012-006": "context_verified",
    "DR3012-007": "context_verified",
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

    require(blob(FROZEN) == EXPECTED_FROZEN_BLOB, f"frozen inventory changed: {blob(FROZEN)}")
    require(blob(EVIDENCE) == EXPECTED_EVIDENCE_BLOB, f"EV-129 evidence record changed: {blob(EVIDENCE)}")
    require(blob(CORRECTION) == EXPECTED_CORRECTION_BLOB, f"DR3012-003 correction record changed: {blob(CORRECTION)}")
    require(blob(SYSTEM_DOC_XSD) == EXPECTED_SYSTEM_DOC_BLOB, f"SystemDocumentation V1.0 XSD changed: {blob(SYSTEM_DOC_XSD)}")
    require(blob(SYSTEM_MGMT_XSD) == EXPECTED_SYSTEM_MGMT_BLOB, f"SystemManagement V1.0 XSD changed: {blob(SYSTEM_MGMT_XSD)}")

    frozen = load(FROZEN)
    require(frozen.get("entry_count") == 192 and frozen.get("state") == "frozen", "frozen inventory invariant failed")
    for finding_id in TERMINAL_STATES:
        require(finding_id in frozen.get("finding_ids", []), f"{finding_id} missing from frozen inventory")

    evidence = load(EVIDENCE)
    require(evidence.get("evidence_id") == "EV-129", "unexpected evidence ID")
    require(evidence.get("evidence_run_id") == "33765167655", "pinned EV-129 evidence run changed")
    require(evidence.get("result") == "PASS", "EV-129 evidence record is not PASS")
    require(evidence.get("artifact", {}).get("id") == "9897171006", "EV-129 artifact ID changed")
    require(evidence.get("artifact", {}).get("digest") == "sha256:a410cdc7103b2ed01f61570b6435a5b2319d2b80f4fec2802929359058a51cc7", "EV-129 artifact digest changed")
    require(evidence.get("findings") == TERMINAL_STATES, "EV-129 terminal recommendations changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-129 mutation invariant failed")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory count changed")
    require(registry.get("next_revalidation_block") == "VDV301-2", f"unexpected next block {registry.get('next_revalidation_block')}")
    require("VDV301-2_V1.0" not in registry.get("revalidation_blocks", {}), "VDV301-2 V1.0 already closed")

    by_id = {item.get("finding_id"): item for item in entries}
    for finding_id, terminal_state in TERMINAL_STATES.items():
        item = by_id.get(finding_id)
        require(item is not None, f"missing registry entry {finding_id}")
        require(item.get("revalidation_state") == "pending", f"{finding_id} is not pending")
        require(item.get("terminal_state_source") is None, f"{finding_id} already has terminal source")
        item["revalidation_state"] = terminal_state
        item["terminal_state_source"] = str(REPORT)

    terminal = sum(1 for item in entries if item.get("revalidation_state") != "pending")
    pending = sum(1 for item in entries if item.get("revalidation_state") == "pending")
    require((terminal, pending) == (67, 125), f"unexpected closure counts terminal={terminal} pending={pending}")

    # VDV301-2 remains the next top-level block because V2.0/V2.1/GC findings are still pending.
    registry["next_revalidation_block"] = "VDV301-2"
    registry.setdefault("revalidation_blocks", {})["VDV301-2_V1.0"] = {
        "date": "2026-09-03",
        "state": "completed",
        "parent_block": "VDV301-2",
        "authority_lane": "byte-pinned official VDV301-2 V1.0 PDF plus exact official historical VDV-301-1.0 XSD family and RFC primary authorities where delegated",
        "official_pdf_source_id": "VDV301-2_V1.0_DE",
        "pdf_sha256": "2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75",
        "pdf_size_bytes": 1790447,
        "system_documentation_xsd_blob": EXPECTED_SYSTEM_DOC_BLOB,
        "system_management_xsd_blob": EXPECTED_SYSTEM_MGMT_BLOB,
        "evidence_id": "EV-129",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": "33765167655",
        "artifact_id": "9897171006",
        "artifact_digest": "sha256:a410cdc7103b2ed01f61570b6435a5b2319d2b80f4fec2802929359058a51cc7",
        "evidence_record": str(EVIDENCE),
        "correction_trail": str(CORRECTION),
        "findings": TERMINAL_STATES,
        "terminal_state_source": str(REPORT),
        "dr3012_003_refinement": "PDF HertbeatIntervall duration vs exact XSD HeartbeatIntervall double in SystemConfigurationData; Store request type duration aligns but identifier still differs",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "VDV301-2",
        "next_subblock": "VDV301-2_BASE_V2.0"
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE inventory count changed")
    require(audit.get("finding_revalidation_completed_findings") == 60, f"unexpected pre-V1.0 completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 132, f"unexpected pre-V1.0 pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "VDV301-2", "CURRENT_STATE next block is not VDV301-2")
    require(audit.get("finding_revalidation_latest_completed_block") == "VDV301-1", "prior completed block is not VDV301-1")

    audit["finding_revalidation_next_block"] = "VDV301-2"
    audit["finding_revalidation_completed_findings"] = 67
    audit["finding_revalidation_pending_findings"] = 125
    audit["finding_revalidation_current_block"] = "VDV301-2_V1.0"
    audit["finding_revalidation_latest_completed_block"] = "VDV301-2_V1.0"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-129"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["latest_audit_correction"] = str(CORRECTION)
    audit["vdv3012_v10_revalidation"] = {
        "status": "complete",
        "evidence_id": "EV-129",
        "run_id": run_id,
        "pinned_successful_evidence_run": "33765167655",
        "artifact_id": "9897171006",
        "artifact_digest": "sha256:a410cdc7103b2ed01f61570b6435a5b2319d2b80f4fec2802929359058a51cc7",
        "terminal_states": TERMINAL_STATES,
        "correction_trail": str(CORRECTION),
        "next_block": "VDV301-2",
        "next_subblock": "VDV301-2_BASE_V2.0",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report = f"""# Finding revalidation — VDV 301-2 V1.0\n\nStatus: **completed** on 2026-09-03 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen legacy entries: `DR3012-001` … `DR3012-007`. The frozen inventory remains exactly **192 entries**. This is the V1.0 subblock of the larger `VDV301-2` revalidation block.\n\n## Evidence\n\n- Evidence gate: **EV-129**, closure workflow run **{run_id}**; independently pinned successful evidence run **33765167655**.\n- Official VDV301-2 V1.0 PDF SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`, size `1790447` bytes.\n- EV-129 visual artifact: **9897171006**, digest `sha256:a410cdc7103b2ed01f61570b6435a5b2319d2b80f4fec2802929359058a51cc7`.\n- Targeted visible pages: 20, 22, 26, 59, 63, 65, 67, 69, 75, 80.\n- External primary authorities: RFC 2927, RFC 3927 and RFC 2782.\n- Exact historical SystemDocumentation V1.0 XSD blob: `{EXPECTED_SYSTEM_DOC_BLOB}`; byte-identical to the official upstream `VDV-301-1.0` tag.\n- Exact historical SystemManagement V1.0 XSD blob: `{EXPECTED_SYSTEM_MGMT_BLOB}`.\n- Root XSD pool regression gate rerun after EV-129.\n\n## Terminal states\n\n| Finding | Terminal state | Result |\n|---|---|---|\n| DR3012-001 | `context_verified` | VDV page 20 cites RFC 2927 for ZeroConf/169.254 addressing. RFC 2927 is the LDAP-schema MIME profile; RFC 3927 is the IPv4 link-local authority. |\n| DR3012-002 | `context_verified` | VDV page 26 says lower SRV Weight is preferred at equal Priority; RFC 2782 defines proportional selection with larger Weight receiving higher probability. |\n| DR3012-003 | `executable_confirmed` | Refined correction: PDF page 65 uses `HertbeatIntervall` + `IBIS-IP.duration`; exact XSD uses `HeartbeatIntervall`, with `IBIS-IP.double` in SystemConfigurationData and `IBIS-IP.duration` in StoreSystemConfigurationRequestStructure. Positive/negative XML tests confirm identifier and lexical-type boundaries. |\n| DR3012-004 | `context_verified` | DeviceState points to 9.3 although visible section 9.4 is DeviceStateEnumeration. |\n| DR3012-005 | `context_verified` | Operation inventory uses ServiceStatus names while detailed headings use SystemStatus; exact historical SystemManagement XSD supports the ServiceStatus terminology. |\n| DR3012-006 | `context_verified` | Historical context resolves the TimeService reference to VDV 301-2-11 as wrong/stale, not merely a modern numbering difference. |\n| DR3012-007 | `context_verified` | StopService request description visibly refers to the service to be started; retained as a copy/paste documentation defect. |\n\n## DR3012-003 correction trail\n\nThe historical statement that `HertbeatIntervall` appears in both PDF and XSD is explicitly superseded by `{CORRECTION}`. The finding itself remains valid and is strengthened; no schema alias or typo normalization is introduced.\n\n## Closure\n\n- Frozen legacy terminal count: **67 / 192**\n- Frozen legacy pending count: **125 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next top-level revalidation block: **VDV301-2**\n- Next VDV301-2 subblock: **VDV301-2 Base V2.0** (`DR3012V20-001…008`)\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED VDV301-2 V1.0: terminal={terminal} pending={pending} next=VDV301-2/V2.0 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
