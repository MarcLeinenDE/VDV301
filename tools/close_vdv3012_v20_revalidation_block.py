#!/usr/bin/env python3
"""Fail-closed closure writer for VDV301-2 Base V2.0 DR3012V20-001..008."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
EVIDENCE = Path("audit_registry/vdv3012_v20_revalidation_evidence_2026-09-03.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_VDV3012_V20_2026-09-03.md")
SYSTEM_DOC_XSD = Path("IBIS-IP_SystemDocumentationService_V2.0.xsd")
DMS_XSD = Path("IBIS-IP_DeviceManagementService_V2.0.xsd")
SYSTEM_MGMT_XSD = Path("IBIS-IP_SystemManagementService_V1.0.xsd")
COMMON_XSD = Path("IBIS-IP_common_V2.0.xsd")
ENUM_XSD = Path("IBIS-IP_Enumerations_V2.0.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_EVIDENCE_BLOB = "ab356be80ebb00790295ba15c5c4c8748a4a3f25"
EXPECTED_SYSTEM_DOC_BLOB = "ab959dddbfa2b8ca420af1b079501f94cff38051"
EXPECTED_DMS_BLOB = "74189e0da65563eeb084ec2f3c400e9668d1ee1a"
EXPECTED_SYSTEM_MGMT_BLOB = "2d32630a0f1981e980e6a466e3f6a69136410f24"
EXPECTED_COMMON_BLOB = "8608e3dcd665c197c34da7f6ec6af5a3758da164"
EXPECTED_ENUM_BLOB = "27e3c183b00381d959622d13c10543123af8eef6"
TERMINAL_STATES = {
    "DR3012V20-001": "context_verified",
    "DR3012V20-002": "context_verified",
    "DR3012V20-003": "executable_confirmed",
    "DR3012V20-004": "context_verified",
    "DR3012V20-005": "context_verified",
    "DR3012V20-006": "context_verified",
    "DR3012V20-007": "context_verified",
    "DR3012V20-008": "context_verified",
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
    require(blob(EVIDENCE) == EXPECTED_EVIDENCE_BLOB, f"EV-130 evidence record changed: {blob(EVIDENCE)}")
    require(blob(SYSTEM_DOC_XSD) == EXPECTED_SYSTEM_DOC_BLOB, f"SystemDocumentation V2.0 XSD changed: {blob(SYSTEM_DOC_XSD)}")
    require(blob(DMS_XSD) == EXPECTED_DMS_BLOB, f"DeviceManagement V2.0 XSD changed: {blob(DMS_XSD)}")
    require(blob(SYSTEM_MGMT_XSD) == EXPECTED_SYSTEM_MGMT_BLOB, f"SystemManagement V1.0 XSD changed: {blob(SYSTEM_MGMT_XSD)}")
    require(blob(COMMON_XSD) == EXPECTED_COMMON_BLOB, f"Common V2.0 XSD changed: {blob(COMMON_XSD)}")
    require(blob(ENUM_XSD) == EXPECTED_ENUM_BLOB, f"Enumerations V2.0 XSD changed: {blob(ENUM_XSD)}")

    frozen = load(FROZEN)
    require(frozen.get("entry_count") == 192 and frozen.get("state") == "frozen", "frozen inventory invariant failed")
    for finding_id in TERMINAL_STATES:
        require(finding_id in frozen.get("finding_ids", []), f"{finding_id} missing from frozen inventory")

    evidence = load(EVIDENCE)
    require(evidence.get("evidence_id") == "EV-130", "unexpected evidence ID")
    require(evidence.get("evidence_run_id") == "33780668141", "pinned EV-130 evidence run changed")
    require(evidence.get("result") == "PASS", "EV-130 evidence record is not PASS")
    require(evidence.get("artifact", {}).get("id") == "9903434312", "EV-130 artifact ID changed")
    require(evidence.get("artifact", {}).get("digest") == "sha256:d5e003a68cce78cff35882a98cd418876482e80a87ff3f8975fc30d5e1970b1c", "EV-130 artifact digest changed")
    require(evidence.get("findings") == TERMINAL_STATES, "EV-130 terminal recommendations changed")
    require(evidence.get("xsd_mutated") is False and evidence.get("frozen_inventory_mutated") is False, "EV-130 mutation invariant failed")
    heartbeat = evidence.get("heartbeat_executable_boundary", {})
    require(heartbeat.get("declared_identifier") == "HeartbeatInterval", "EV-130 HeartbeatInterval identifier changed")
    require(heartbeat.get("declared_type") == "IBIS-IP.duration", "EV-130 HeartbeatInterval type changed")
    require(heartbeat.get("rejected_aliases") == ["HertbeatIntervall", "HeartbeatIntervall"], "EV-130 rejected alias set changed")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory count changed")
    require(registry.get("next_revalidation_block") == "VDV301-2", f"unexpected next block {registry.get('next_revalidation_block')}")
    blocks = registry.get("revalidation_blocks", {})
    require("VDV301-2_V1.0" in blocks, "VDV301-2 V1.0 prerequisite closure missing")
    require("VDV301-2_BASE_V2.0" not in blocks, "VDV301-2 Base V2.0 already closed")

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
    require((terminal, pending) == (75, 117), f"unexpected closure counts terminal={terminal} pending={pending}")

    # VDV301-2 stays the top-level block until its later subblocks are complete.
    registry["next_revalidation_block"] = "VDV301-2"
    blocks["VDV301-2_BASE_V2.0"] = {
        "date": "2026-09-03",
        "state": "completed",
        "parent_block": "VDV301-2",
        "authority_lane": "byte-pinned official VDV301-2 Base V2.0 PDF plus byte-identical official VDV-301-2.0 XSD family, historical SystemManagement V1.0, and RFC primary authorities where delegated",
        "official_pdf_source_id": "VDV301-2_BASE_V2.0",
        "pdf_sha256": "fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37",
        "pdf_size_bytes": 2374295,
        "system_documentation_xsd_blob": EXPECTED_SYSTEM_DOC_BLOB,
        "device_management_xsd_blob": EXPECTED_DMS_BLOB,
        "system_management_xsd_blob": EXPECTED_SYSTEM_MGMT_BLOB,
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "evidence_id": "EV-130",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": "33780668141",
        "artifact_id": "9903434312",
        "artifact_digest": "sha256:d5e003a68cce78cff35882a98cd418876482e80a87ff3f8975fc30d5e1970b1c",
        "evidence_record": str(EVIDENCE),
        "findings": TERMINAL_STATES,
        "terminal_state_source": str(REPORT),
        "heartbeat_executable_boundary": heartbeat,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "VDV301-2",
        "next_subblock": "VDV301-2_BASE_V2.1"
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE inventory count changed")
    require(audit.get("finding_revalidation_completed_findings") == 67, f"unexpected pre-V2.0 completed count {audit.get('finding_revalidation_completed_findings')}")
    require(audit.get("finding_revalidation_pending_findings") == 125, f"unexpected pre-V2.0 pending count {audit.get('finding_revalidation_pending_findings')}")
    require(audit.get("finding_revalidation_next_block") == "VDV301-2", "CURRENT_STATE next block is not VDV301-2")
    require(audit.get("finding_revalidation_latest_completed_block") == "VDV301-2_V1.0", "prior completed block is not VDV301-2_V1.0")

    audit["finding_revalidation_next_block"] = "VDV301-2"
    audit["finding_revalidation_completed_findings"] = 75
    audit["finding_revalidation_pending_findings"] = 117
    audit["finding_revalidation_current_block"] = "VDV301-2_BASE_V2.0"
    audit["finding_revalidation_latest_completed_block"] = "VDV301-2_BASE_V2.0"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_executable_evidence_id"] = "EV-130"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["vdv3012_v20_revalidation"] = {
        "status": "complete",
        "evidence_id": "EV-130",
        "run_id": run_id,
        "pinned_successful_evidence_run": "33780668141",
        "artifact_id": "9903434312",
        "artifact_digest": "sha256:d5e003a68cce78cff35882a98cd418876482e80a87ff3f8975fc30d5e1970b1c",
        "terminal_states": TERMINAL_STATES,
        "heartbeat_executable_boundary": heartbeat,
        "next_block": "VDV301-2",
        "next_subblock": "VDV301-2_BASE_V2.1",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False
    }

    report = f"""# Finding revalidation — VDV 301-2 Base V2.0\n\nStatus: **completed** on 2026-09-03 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen legacy entries: `DR3012V20-001` … `DR3012V20-008`. The frozen inventory remains exactly **192 entries**. This is the Base V2.0 subblock of the larger `VDV301-2` revalidation block.\n\n## Evidence\n\n- Evidence gate: **EV-130**, closure workflow run **{run_id}**; independently pinned successful evidence run **33780668141**.\n- Official VDV301-2 Base V2.0 PDF SHA-256: `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`, size `2374295` bytes.\n- EV-130 visual artifact: **9903434312**, digest `sha256:d5e003a68cce78cff35882a98cd418876482e80a87ff3f8975fc30d5e1970b1c`.\n- Targeted visible pages: 21, 33, 34, 90, 92, 93, 98, 100, 101, 102, 105, 110.\n- External primary authorities: RFC 2927, RFC 3927 and RFC 2782.\n- Exact official `VDV-301-2.0` XSD blobs: SystemDocumentation `{EXPECTED_SYSTEM_DOC_BLOB}`, DeviceManagement `{EXPECTED_DMS_BLOB}`, Common `{EXPECTED_COMMON_BLOB}`, Enumerations `{EXPECTED_ENUM_BLOB}`.\n- SystemManagement remains historical V1.0 in this release family: `{EXPECTED_SYSTEM_MGMT_BLOB}`.\n- Root XSD pool regression gate rerun after EV-130.\n\n## Terminal states\n\n| Finding | Terminal state | Result |\n|---|---|---|\n| DR3012V20-001 | `context_verified` | German ZeroConf text uses RFC 3927 while the English translation still cites RFC 2927 for the same 169.254 link-local behavior; the bibliography points to RFC 3927. |\n| DR3012V20-002 | `context_verified` | Both languages state that lower SRV Weight is preferred; RFC 2782 defines proportional selection with larger Weight receiving higher probability. |\n| DR3012V20-003 | `executable_confirmed` | Version history claims correction to `HeartbeatInterval`, but both visible tables still print `HertbeatIntervall`. Exact V2.0 XSD uses `HeartbeatInterval` as `IBIS-IP.duration` in both structures. `PT5S` validates; numeric `5.5` and both stale aliases reject. |\n| DR3012V20-004 | `context_verified` | Correct SystemDocumentation heading is followed by narrative typo `SystemDocumenationService`; exact XSD uses `SystemDocumentationService`. |\n| DR3012V20-005 | `context_verified` | SystemManagement introduction visibly contains unresolved chapter-range placeholders in German and English. |\n| DR3012V20-006 | `context_verified` | Operation inventory includes `SubscribeDeviceInformation`, but the detailed subsection sequence omits a dedicated heading; full-text disproof search confirms no such heading exists while generic subscription context remains. |\n| DR3012V20-007 | `context_verified` | `GetDeviceConfiguration` prose describes setting the parameter; the following `SetDeviceConfiguration` is the actual setter and the exact DMS XSD preserves getter/setter direction. |\n| DR3012V20-008 | `context_verified` | `GetDeviceInformationResponseStructure` and its response data are visibly described as request structures; exact DMS XSD confirms they are response structures. |\n\n## Executable HeartbeatInterval boundary\n\nThe authoritative V2.0 identifier is exactly `HeartbeatInterval`; both SystemDocumentation structures use `IBIS-IP.duration`. No alias is introduced for V1.0 `HeartbeatIntervall` or PDF-stale `HertbeatIntervall`.\n\n## Closure\n\n- Frozen legacy terminal count: **75 / 192**\n- Frozen legacy pending count: **117 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next top-level revalidation block: **VDV301-2**\n- Next VDV301-2 subblock: **VDV301-2 Base V2.1** (`DR3012V21-…`)\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED VDV301-2 Base V2.0: terminal={terminal} pending={pending} next=VDV301-2/V2.1 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
