#!/usr/bin/env python3
"""Fail-closed closure writer for frozen generic subscription findings SUB-001..002."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
SOURCE_REGISTRY = Path("audit_registry/pdf_source_registry_v0.1.json")
SOURCE_PINS = Path("audit_registry/pdf_source_pins_v0.1.json")
DEEP_READ = Path("audit_registry/deep_read_findings_v0.1.json")
GC24_DELTA = Path("audit_registry/deep_read_findings_delta_gc_v24_2026-08-28.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_SUB_2026-09-10.md")
VALIDATOR = Path("tools/validate_sub_revalidation_ev157.py")
XSD_POOL = Path("tools/validate_xsd_pool.py")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_REGISTRY_PRE_BLOB = "650dc6a45f47e01cef2e5e05f48614e0c5afe819"
EXPECTED_STATE_PRE_BLOB = "612b9217244e7bbb49a09c8f4d94b9036e388dc4"
EXPECTED_SOURCE_REGISTRY_BLOB = "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8"
EXPECTED_SOURCE_PINS_BLOB = "88349638b423689799af700e8a1c8ec99bbfb67b"
EXPECTED_DEEP_READ_BLOB = "f016defa3148400834378ac99ca33b30937f2571"
EXPECTED_GC24_DELTA_BLOB = "2fd4eb48195c27312c73f665d4365bb28ca3a791"
EXPECTED_VALIDATOR_BLOB = "b68091fdc2713c56718d9313187f56d9eef3c9cd"
EXPECTED_XSD_POOL_BLOB = "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd"

EXPECTED_XSDS = {
    "IBIS-IP_common_V1.0.xsd": "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c",
    "IBIS-IP_Enumerations_V1.0.xsd": "a9bea5bc73003ed91ded8519db06c32c4067831d",
    "IBIS-IP_SystemManagementService_V1.0.xsd": "2d32630a0f1981e980e6a466e3f6a69136410f24",
    "IBIS-IP_common_V2.0.xsd": "8608e3dcd665c197c34da7f6ec6af5a3758da164",
    "IBIS-IP_Enumerations_V2.0.xsd": "27e3c183b00381d959622d13c10543123af8eef6",
    "IBIS-IP_SystemDocumentationService_V2.0.xsd": "ab959dddbfa2b8ca420af1b079501f94cff38051",
    "IBIS-IP_common_V2.1.xsd": "05977c9f86c7c9dd0b48f36a4a4e9be32e94659e",
    "IBIS-IP_Enumerations_V2.1.xsd": "311464690ad60749ed8d326217787e4b8ed0b718",
    "IBIS-IP_DeviceManagementService_V2.1.xsd": "191b43e01cdaba14b247725689a913c244a67eed",
}

BASE_V20_SHA256 = "fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37"
BASE_V20_SIZE = 2374295
BASE_V21_SHA256 = "685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a"
BASE_V21_SIZE = 2671005

SOURCE_ACQUISITION_RUN = "34486504933"
SOURCE_ACQUISITION_JOB = "102902042657"
SOURCE_ACQUISITION_ARTIFACT = "10155848626"
SOURCE_ACQUISITION_DIGEST = "sha256:8318472f56fe7c33d85bc5cda3bc02df5cfed7f987dacb832eaa4798a1ff2d4a"
PINNED_EV157_RUN = "34487918692"
PINNED_EV157_JOB = "102906852658"
PINNED_EV157_ARTIFACT = "10156457016"
PINNED_EV157_DIGEST = "sha256:25bf3344ba21c7a98eea97e48d5f637191a91a96bd9132993808691089eabe12"
PINNED_EV157_HEAD = "2f58012b2d6c8b7165d6c283821407fa534d193b"

TARGETS = {
    "SUB-001": "context_verified",
    "SUB-002": "contextual_not_defect",
}
TERMINAL_STATES = {
    "context_verified", "field_validated", "executable_confirmed",
    "contextual_not_defect", "withdrawn", "unresolved", "superseded",
}


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)
    print(f"OK  {message}")


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
    require(run_id.isdigit(), "EVIDENCE_RUN_ID is numeric")
    require(run_url == f"https://github.com/MarcLeinenDE/VDV301/actions/runs/{run_id}", "EVIDENCE_RUN_URL matches run id")

    immutable = {
        FROZEN: EXPECTED_FROZEN_BLOB,
        REGISTRY: EXPECTED_REGISTRY_PRE_BLOB,
        STATE: EXPECTED_STATE_PRE_BLOB,
        SOURCE_REGISTRY: EXPECTED_SOURCE_REGISTRY_BLOB,
        SOURCE_PINS: EXPECTED_SOURCE_PINS_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        GC24_DELTA: EXPECTED_GC24_DELTA_BLOB,
        VALIDATOR: EXPECTED_VALIDATOR_BLOB,
        XSD_POOL: EXPECTED_XSD_POOL_BLOB,
    }
    immutable.update({Path(name): blob for name, blob in EXPECTED_XSDS.items()})
    for path, expected in immutable.items():
        require(path.is_file(), f"authority/prestate file exists: {path}")
        require(git_blob(path) == expected, f"exact prestate blob {path} = {expected}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen", "frozen inventory state unchanged")
    require(frozen.get("entry_count") == 192, "frozen inventory remains 192 entries")
    frozen_ids = frozen.get("finding_ids", [])
    require(all(fid in frozen_ids for fid in TARGETS), "SUB targets are frozen inventory members")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen", "registry inventory remains frozen")
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory remains 192 entries")
    require(registry.get("next_revalidation_block") == "SUB", "prestate next block is SUB")
    ids = [e.get("finding_id") for e in entries]
    require(len(ids) == len(set(ids)) == 192, "registry finding IDs remain unique")
    by_id = {e["finding_id"]: e for e in entries}
    for fid in TARGETS:
        require(by_id[fid].get("revalidation_state") == "pending", f"{fid} is pending before closure")
        require(by_id[fid].get("terminal_state_source") is None, f"{fid} has no premature terminal source")
    require(counts(entries) == (144, 48), f"pre-SUB counts are 144/48, got {counts(entries)}")
    require(first_pending(entries) == "SUB-001", f"pre-SUB first pending is SUB-001, got {first_pending(entries)}")
    require(by_id.get("TKT-001", {}).get("revalidation_state") == "pending", "TKT-001 remains pending before SUB closure")

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit exists")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE inventory count remains 192")
    require(audit.get("finding_revalidation_completed_findings") == 144, "CURRENT_STATE pre-SUB terminal count is 144")
    require(audit.get("finding_revalidation_pending_findings") == 48, "CURRENT_STATE pre-SUB pending count is 48")
    require(audit.get("finding_revalidation_next_block") == "SUB", "CURRENT_STATE pre-SUB next block is SUB")
    require(audit.get("finding_revalidation_latest_completed_block") == "SMS", "SMS is prior completed block")

    # Source catalog is pinned by identity; the new byte pins live in immutable acquisition evidence.
    source_registry = load(SOURCE_REGISTRY)
    sources = {x["source_id"]: x for x in source_registry.get("sources", [])}
    require(sources["VDV301-2_BASE_V2.0"]["official_url"] == "https://www.vdv.de/301-2-sds-v-2-0.pdfx", "Base V2.0 source URL unchanged")
    require(sources["VDV301-2_BASE_V2.1"]["official_url"] == "https://www.vdv.de/301-2-sds-v2-1-basicservices.pdfx", "Base V2.1 source URL unchanged")

    for fid, terminal_state in TARGETS.items():
        by_id[fid]["revalidation_state"] = terminal_state
        by_id[fid]["terminal_state_source"] = str(REPORT)

    require(counts(entries) == (146, 46), f"post-SUB counts are 146/46, got {counts(entries)}")
    require(first_pending(entries) == "TKT-001", f"post-SUB first pending is TKT-001, got {first_pending(entries)}")

    blocks = registry.setdefault("revalidation_blocks", {})
    require("SUB" not in blocks, "SUB block is not already closed")
    registry["next_revalidation_block"] = "TKT"
    blocks["SUB"] = {
        "date": "2026-09-10",
        "state": "completed",
        "authority_lane": "official byte-pinned Base Services V2.0/V2.1 documentation plus exact Common/SystemDocumentation/SystemManagement/DeviceManagement XSD history",
        "evidence_id": "EV-157",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": PINNED_EV157_RUN,
        "pinned_successful_evidence_job": PINNED_EV157_JOB,
        "artifact_id": PINNED_EV157_ARTIFACT,
        "artifact_digest": PINNED_EV157_DIGEST,
        "evidence_head_sha": PINNED_EV157_HEAD,
        "source_acquisition": {
            "run_id": SOURCE_ACQUISITION_RUN,
            "job_id": SOURCE_ACQUISITION_JOB,
            "artifact_id": SOURCE_ACQUISITION_ARTIFACT,
            "artifact_digest": SOURCE_ACQUISITION_DIGEST,
        },
        "pdf_authority": {
            "VDV301-2_BASE_V2.0": {"sha256": BASE_V20_SHA256, "size_bytes": BASE_V20_SIZE, "pages": 115},
            "VDV301-2_BASE_V2.1": {"sha256": BASE_V21_SHA256, "size_bytes": BASE_V21_SIZE, "pages": 130},
        },
        "visual_pages": {
            "VDV301-2_BASE_V2.0": [82, 83, 99, 103],
            "VDV301-2_BASE_V2.1": [83, 84, 112, 116],
        },
        "xsd_blobs": EXPECTED_XSDS,
        "findings": TARGETS,
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "TKT",
        "next_finding": "TKT-001",
    }

    audit["finding_revalidation_next_block"] = "TKT"
    audit["finding_revalidation_completed_findings"] = 146
    audit["finding_revalidation_pending_findings"] = 46
    audit["finding_revalidation_current_block"] = "SUB"
    audit["finding_revalidation_latest_completed_block"] = "SUB"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_revalidation_evidence_id"] = "EV-157"
    audit["latest_executable_evidence_id"] = "EV-157"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["sub_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-157",
        "run_id": run_id,
        "pinned_successful_evidence_run": PINNED_EV157_RUN,
        "pinned_successful_evidence_job": PINNED_EV157_JOB,
        "artifact_id": PINNED_EV157_ARTIFACT,
        "artifact_digest": PINNED_EV157_DIGEST,
        "source_acquisition_run": SOURCE_ACQUISITION_RUN,
        "source_acquisition_artifact": SOURCE_ACQUISITION_ARTIFACT,
        "terminal_states": TARGETS,
        "pdf_v20_sha256": BASE_V20_SHA256,
        "pdf_v21_sha256": BASE_V21_SHA256,
        "next_block": "TKT",
        "next_finding": "TKT-001",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report = f"""# Finding revalidation — Generic Subscription Layer (SUB)\n\nStatus: **completed** on 2026-09-10 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen findings: `SUB-001`, `SUB-002`. Frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Evidence: **EV-157**; successful closure run **{run_id}**.\n- Independently successful EV-157 run: **{PINNED_EV157_RUN}**, job **{PINNED_EV157_JOB}**, artifact **{PINNED_EV157_ARTIFACT}**, digest `{PINNED_EV157_DIGEST}`.\n- Source-acquisition evidence: run **{SOURCE_ACQUISITION_RUN}**, job **{SOURCE_ACQUISITION_JOB}**, artifact **{SOURCE_ACQUISITION_ARTIFACT}**, digest `{SOURCE_ACQUISITION_DIGEST}`.\n- Official Base Services V2.0 PDF: SHA-256 `{BASE_V20_SHA256}`, {BASE_V20_SIZE} bytes, 115 pages.\n- Official Base Services V2.1 PDF: SHA-256 `{BASE_V21_SHA256}`, {BASE_V21_SIZE} bytes, 130 pages.\n- Targeted visual/text pages: V2.0 pages 82, 83, 99, 103; V2.1 pages 83, 84, 112, 116.\n- Exact XSD authority/history blobs are recorded machine-readably in the SUB block registry entry.\n- The complete 50-file root XSD pool was recompiled and byte-hashed before/after EV-157; no XSD changed.\n\n## Terminal states\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n| `SUB-001` | `context_verified` | Base Services V2.0/V2.1 document `UnsubscribeData` with `TerminateSubscribeRequestStructure` / `TerminateSubscribeResponseStructure`, while exact Common V1.0/V2.0/V2.1 expose `UnsubscribeRequestStructure` / `UnsubscribeResponseStructure` and no executable `TerminateSubscribe*` aliases. This is a documentation/XSD naming discrepancy; no alias is synthesized. |\n| `SUB-002` | `contextual_not_defect` | Official Base Services document generic Subscribe/Unsubscribe operations for SystemDocumentation/SystemManagement although their local XSD groups are sparse. DMS V2.1 explicitly expands generic subscription operations in its local group. Service-group membership is therefore service/version dependent and is not by itself a complete supported-operation authority. |\n\n## Mutation decision\n\n- XSD mutation: **none**.\n- Frozen inventory mutation: **none**.\n- Registry/status mutation: only the two frozen SUB findings and block/counter handoff.\n\n## State transition\n\n- Before: **144/192 terminal**, **48 pending**, first pending `SUB-001`.\n- After: **146/192 terminal**, **46 pending**, first pending `TKT-001`.\n- Next block: **TKT**.\n"""

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")
    write_json(REGISTRY, registry)
    write_json(STATE, state)
    print("PASSED: SUB closure writer produced atomic registry/state/report changes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
