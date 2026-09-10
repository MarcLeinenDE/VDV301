#!/usr/bin/env python3
"""Fail-closed closure writer for frozen SystemMonitoringService findings SMS-001..004."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
SOURCE_PINS = Path("audit_registry/pdf_source_pins_v0.1.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/SMS_V2.2.md")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_SMS_2026-09-10.md")
VALIDATOR = Path("tools/validate_sms_revalidation_ev156.py")
EV116 = Path("tools/validate_sms_v22_ev116.py")
SERVICE = Path("IBIS-IP_SystemMonitoringService_V2.2.xsd")
COMMON = Path("IBIS-IP_common_V2.2.xsd")
ENUMS = Path("IBIS-IP_Enumerations_V2.2.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_REGISTRY_PRE_BLOB = "96fa80faade79c5866f6c9d21e550abb56ea282f"
EXPECTED_STATE_PRE_BLOB = "b2e89510ffebd76448f9ff8a99b98bbc8c0d20fd"
EXPECTED_SOURCE_PINS_BLOB = "88349638b423689799af700e8a1c8ec99bbfb67b"
EXPECTED_DEEP_READ_BLOB = "4eb220e43a728a0f719cdcf81fac78df058ecd08"
EXPECTED_VALIDATOR_BLOB = "335aff0aaed1badc60bf5a59aac101897f211161"
EXPECTED_EV116_BLOB = "bac849f6c33e6084e899794564f99f0c6cbd338a"
EXPECTED_SERVICE_BLOB = "d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c"
EXPECTED_COMMON_BLOB = "468fee6d177e7185dbcd5d3f90cfb114e29e01ae"
EXPECTED_ENUMS_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"

PDF_SHA256 = "996f639a81cb91ad20a8e78b6213e7c85d41ff0ec42caba4208d6c4652b140f4"
PDF_SIZE = 847416
PINNED_EV156_RUN = "34460160697"
PINNED_EV156_JOB = "102815828711"
PINNED_EV156_ARTIFACT = "10145182333"
PINNED_EV156_DIGEST = "sha256:67c01039e53841c4fb549af2414c6c957ab8de8a85df7a8ff594f85b2a9ffb19"
SUPPORTING_EV116_RUN = "33269006407"
FRESH_READ_RENDER_RUN = "33268591224"
FRESH_READ_ARTIFACT = "9719396063"
FRESH_READ_DIGEST = "sha256:b7b73746ecdf6b904543c7d6a5312753a57a0b9effec6fe31d1dc83bdfdcec4a"
UPSTREAM_TAG = "VDV-301-2.2"
UPSTREAM_TAG_COMMIT = "f283697124750d12189b960b302b399769bad530"

TARGETS = {
    "SMS-001": "contextual_not_defect",
    "SMS-002": "executable_confirmed",
    "SMS-003": "context_verified",
    "SMS-004": "context_verified",
}
TERMINAL_STATES = {
    "context_verified",
    "executable_confirmed",
    "contextual_not_defect",
    "withdrawn",
    "unresolved",
    "superseded",
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


def counts(entries: list[dict]) -> tuple[int, int]:
    terminal = sum(item.get("revalidation_state") in TERMINAL_STATES for item in entries)
    pending = sum(item.get("revalidation_state") == "pending" for item in entries)
    return terminal, pending


def first_pending(entries: list[dict]) -> str | None:
    for item in entries:
        if item.get("revalidation_state") == "pending":
            return item.get("finding_id")
    return None


def main() -> int:
    run_id = os.environ.get("EVIDENCE_RUN_ID", "").strip()
    run_url = os.environ.get("EVIDENCE_RUN_URL", "").strip()
    require(run_id.isdigit(), "EVIDENCE_RUN_ID must be the successful closure workflow run id")
    require(run_url.startswith("https://github.com/"), "EVIDENCE_RUN_URL missing or invalid")

    immutable = {
        FROZEN: EXPECTED_FROZEN_BLOB,
        REGISTRY: EXPECTED_REGISTRY_PRE_BLOB,
        STATE: EXPECTED_STATE_PRE_BLOB,
        SOURCE_PINS: EXPECTED_SOURCE_PINS_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        VALIDATOR: EXPECTED_VALIDATOR_BLOB,
        EV116: EXPECTED_EV116_BLOB,
        SERVICE: EXPECTED_SERVICE_BLOB,
        COMMON: EXPECTED_COMMON_BLOB,
        ENUMS: EXPECTED_ENUMS_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file(), f"missing authority/prestate file {path}")
        observed = git_blob(path)
        require(observed == expected, f"prestate blob changed for {path}: {observed}")

    pins = load(SOURCE_PINS)
    source = next((x for x in pins.get("sources", []) if x.get("source_id") == "SMS_V2.2"), None)
    require(source is not None, "SMS_V2.2 source pin missing")
    require(source.get("expected_sha256") == PDF_SHA256, "SMS source pin SHA changed")
    require(source.get("expected_size_bytes") == PDF_SIZE, "SMS source pin size changed")
    require(str(source.get("evidence_run_id")) == "33268541691", "SMS source pin run changed")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen", "frozen inventory state changed")
    require(frozen.get("entry_count") == 192, "frozen inventory entry count changed")
    frozen_ids = frozen.get("finding_ids", [])
    require(all(fid in frozen_ids for fid in TARGETS), "SMS target missing from frozen inventory")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen", "registry inventory state changed")
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory cardinality changed")
    require(registry.get("next_revalidation_block") == "SMS", f"unexpected registry next block {registry.get('next_revalidation_block')}")

    ids = [item.get("finding_id") for item in entries]
    require(len(ids) == len(set(ids)) == 192, "registry finding IDs are not unique")
    by_id = {item["finding_id"]: item for item in entries}
    require(set(TARGETS).issubset(by_id), "SMS targets missing from registry")
    for fid in TARGETS:
        item = by_id[fid]
        require(item.get("revalidation_state") == "pending", f"{fid} is not pending")
        require(item.get("terminal_state_source") is None, f"{fid} already has terminal source")

    require(counts(entries) == (140, 52), f"pre-SMS counts must be 140/52, got {counts(entries)}")
    require(first_pending(entries) == "SMS-001", f"pre-SMS first pending must be SMS-001, got {first_pending(entries)}")
    require(by_id.get("SUB-001", {}).get("revalidation_state") == "pending", "SUB-001 is not pending before SMS closure")

    for fid, state in TARGETS.items():
        by_id[fid]["revalidation_state"] = state
        by_id[fid]["terminal_state_source"] = str(REPORT)

    require(counts(entries) == (144, 48), f"post-SMS counts must be 144/48, got {counts(entries)}")
    require(first_pending(entries) == "SUB-001", f"post-SMS first pending must be SUB-001, got {first_pending(entries)}")

    blocks = registry.setdefault("revalidation_blocks", {})
    require("SMS" not in blocks, "SMS block already exists")
    registry["next_revalidation_block"] = "SUB"
    blocks["SMS"] = {
        "date": "2026-09-10",
        "state": "completed",
        "authority_lane": "official byte-pinned SystemMonitoringService V2.2 PDF plus exact VDV-301-2.2 service/Common/Enumerations XSD family",
        "evidence_id": "EV-156",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": PINNED_EV156_RUN,
        "pinned_successful_evidence_job": PINNED_EV156_JOB,
        "artifact_id": PINNED_EV156_ARTIFACT,
        "artifact_digest": PINNED_EV156_DIGEST,
        "supporting_ev116_run": SUPPORTING_EV116_RUN,
        "fresh_read_render_run": FRESH_READ_RENDER_RUN,
        "fresh_read_artifact": FRESH_READ_ARTIFACT,
        "fresh_read_artifact_digest": FRESH_READ_DIGEST,
        "pdf_authority": {
            "SMS_V2.2": {
                "sha256": PDF_SHA256,
                "size_bytes": PDF_SIZE,
                "pages": 15
            }
        },
        "visual_pages": [4, 9, 10, 11, 12, 13],
        "upstream_authority": {
            "tag": UPSTREAM_TAG,
            "commit": UPSTREAM_TAG_COMMIT,
            SERVICE.name: EXPECTED_SERVICE_BLOB,
            COMMON.name: EXPECTED_COMMON_BLOB,
            ENUMS.name: EXPECTED_ENUMS_BLOB,
        },
        "findings": TARGETS,
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "SUB",
        "next_finding": "SUB-001",
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE inventory count changed")
    require(audit.get("finding_revalidation_completed_findings") == 140, "unexpected CURRENT_STATE completed count")
    require(audit.get("finding_revalidation_pending_findings") == 52, "unexpected CURRENT_STATE pending count")
    require(audit.get("finding_revalidation_next_block") == "SMS", f"unexpected CURRENT_STATE next block {audit.get('finding_revalidation_next_block')}")
    require(audit.get("finding_revalidation_latest_completed_block") == "PCS", "unexpected prior completed block")

    audit["finding_revalidation_next_block"] = "SUB"
    audit["finding_revalidation_completed_findings"] = 144
    audit["finding_revalidation_pending_findings"] = 48
    audit["finding_revalidation_current_block"] = "SMS"
    audit["finding_revalidation_latest_completed_block"] = "SMS"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_revalidation_evidence_id"] = "EV-156"
    audit["latest_executable_evidence_id"] = "EV-156"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["sms_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-156",
        "run_id": run_id,
        "pinned_successful_evidence_run": PINNED_EV156_RUN,
        "pinned_successful_evidence_job": PINNED_EV156_JOB,
        "artifact_id": PINNED_EV156_ARTIFACT,
        "artifact_digest": PINNED_EV156_DIGEST,
        "supporting_ev116_run": SUPPORTING_EV116_RUN,
        "terminal_states": TARGETS,
        "pdf_v22_sha256": PDF_SHA256,
        "pdf_v22_size_bytes": PDF_SIZE,
        "visual_pages": [4, 9, 10, 11, 12, 13],
        "official_tag": UPSTREAM_TAG,
        "official_tag_commit": UPSTREAM_TAG_COMMIT,
        "next_block": "SUB",
        "next_finding": "SUB-001",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report = f"""# Finding revalidation — SystemMonitoringService (SMS)\n\nStatus: **completed** on 2026-09-10 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen findings: `SMS-001`, `SMS-002`, `SMS-003`, `SMS-004`. Frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Evidence: **EV-156**; successful closure run **{run_id}**.\n- Independently successful EV-156 run: **{PINNED_EV156_RUN}**, job **{PINNED_EV156_JOB}**, artifact **{PINNED_EV156_ARTIFACT}**, digest `{PINNED_EV156_DIGEST}`.\n- Supporting executable boundary: **EV-116**, run **{SUPPORTING_EV116_RUN}**.\n- Earlier independent full render/read evidence: run **{FRESH_READ_RENDER_RUN}**, artifact **{FRESH_READ_ARTIFACT}**, digest `{FRESH_READ_DIGEST}`.\n- Official SMS V2.2 PDF: SHA-256 `{PDF_SHA256}`, {PDF_SIZE} bytes, 15 pages.\n- Physical pages 4, 9, 10, 11, 12 and 13 are the targeted visual evidence set.\n- Official upstream tag `{UPSTREAM_TAG}` resolves to commit `{UPSTREAM_TAG_COMMIT}`.\n- Exact XSD blobs: service `{EXPECTED_SERVICE_BLOB}`, Common `{EXPECTED_COMMON_BLOB}`, Enumerations `{EXPECTED_ENUMS_BLOB}`.\n- The complete root XSD pool was revalidated and byte-hashed before/after EV-156; no XSD changed.\n\n## Terminal states\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n| `SMS-001` | `contextual_not_defect` | The SMS PDF explicitly routes Subscribe/Unsubscribe payload structures to VDV 301-2-1, and exact Common V2.2 contains the generic Subscribe/Unsubscribe structures. Their absence as service-local SMS elements is therefore not a schema defect. |\n| `SMS-002` | `executable_confirmed` | The PDF operation table/body and exact XSD use `ServiceStatus`, while headings 2.5–2.7 use `SystemStatus`. Exact `GetServiceStatusResponse` validates; invented `GetSystemStatusResponse` is rejected. The defect is the PDF naming/headings, not executable behavior. |\n| `SMS-003` | `context_verified` | Official SMS PDF page 4 visibly contains an unrelated HTMLDisplayService paragraph in the English foreword. Documentation-only copy/paste defect. |\n| `SMS-004` | `context_verified` | Version history page 12 cites `VDV 302-2`, while page 13 identifies the Base Services source as `VDV 301-2-0`. This is a documentation reference-number error. |\n\n## Closure\n\n- Frozen terminal count: **144 / 192**\n- Frozen pending count: **48 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next revalidation block: **SUB**\n- First pending finding: **SUB-001**\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED SMS: terminal=144 pending=48 next=SUB first_pending=SUB-001 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
