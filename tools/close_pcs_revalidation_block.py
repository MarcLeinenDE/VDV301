#!/usr/bin/env python3
"""Fail-closed closure writer for frozen PassengerCountingService findings PCS-001/002."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_PCS_2026-09-10.md")
VALIDATOR = Path("tools/validate_pcs_revalidation_ev155.py")
PCS001_VALIDATOR = Path("tools/validate_pcs_v21_operation_not_supported.py")
PCS_V10 = Path("IBIS-IP_PassengerCountingService_V1.0.xsd")
PCS_V21 = Path("IBIS-IP_PassengerCountingService_V2.1.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_REGISTRY_PRE_BLOB = "865a21115cec1beb556af000c71717ae774459cb"
EXPECTED_STATE_PRE_BLOB = "ee9120db8b01e26e888ad6b512c0a49d8751d700"
EXPECTED_VALIDATOR_BLOB = "99483fe79fdffa35b81d6890469499a4546efab6"
EXPECTED_PCS001_VALIDATOR_BLOB = "ffb932f19b669cd0584943063fc14cb4fd5daba8"
EXPECTED_PCS_V10_BLOB = "4161872be76740abfdd1cddf96f8a736333fc8be"
EXPECTED_PCS_V21_BLOB = "59ef2ddb09b92db0d492974e38bad5b6be03865e"

PDF_V10_SHA256 = "372be7a5d39c72e4bf405e3058f5af3d809eb611ac3548b70c526788d364c402"
PDF_V10_SIZE = 918762
PDF_V21_SHA256 = "572f07adbb6999463433a3e764e47f29c8157a4e63aa88ea7c927393da7ec043"
PDF_V21_SIZE = 1084925
PINNED_EV155_RUN = "34447583426"
PINNED_EV155_ARTIFACT = "10140238171"
PINNED_EV155_DIGEST = "sha256:48e3f7ad728660a342124d42976f8a1c88670c06b5ba3a63f7475b462653f633"

TARGETS = {
    "PCS-001": "executable_confirmed",
    "PCS-002": "contextual_not_defect",
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
        VALIDATOR: EXPECTED_VALIDATOR_BLOB,
        PCS001_VALIDATOR: EXPECTED_PCS001_VALIDATOR_BLOB,
        PCS_V10: EXPECTED_PCS_V10_BLOB,
        PCS_V21: EXPECTED_PCS_V21_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file(), f"missing authority/prestate file {path}")
        observed = git_blob(path)
        require(observed == expected, f"prestate blob changed for {path}: {observed}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen", "frozen inventory state changed")
    require(frozen.get("entry_count") == 192, "frozen inventory entry count changed")
    frozen_ids = frozen.get("finding_ids", [])
    require(all(fid in frozen_ids for fid in TARGETS), "PCS target missing from frozen inventory")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen", "registry inventory state changed")
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory cardinality changed")
    require(registry.get("next_revalidation_block") == "PCS", f"unexpected registry next block {registry.get('next_revalidation_block')}")

    ids = [item.get("finding_id") for item in entries]
    require(len(ids) == len(set(ids)) == 192, "registry finding IDs are not unique")
    by_id = {item["finding_id"]: item for item in entries}
    require(set(TARGETS).issubset(by_id), "PCS targets missing from registry")
    for fid in TARGETS:
        item = by_id[fid]
        require(item.get("revalidation_state") == "pending", f"{fid} is not pending")
        require(item.get("terminal_state_source") is None, f"{fid} already has terminal source")

    require(counts(entries) == (138, 54), f"pre-PCS counts must be 138/54, got {counts(entries)}")
    require(first_pending(entries) == "PCS-001", f"pre-PCS first pending must be PCS-001, got {first_pending(entries)}")
    require(by_id.get("SMS-001", {}).get("revalidation_state") == "pending", "SMS-001 is not pending before PCS closure")

    for fid, state in TARGETS.items():
        by_id[fid]["revalidation_state"] = state
        by_id[fid]["terminal_state_source"] = str(REPORT)

    require(counts(entries) == (140, 52), f"post-PCS counts must be 140/52, got {counts(entries)}")
    require(first_pending(entries) == "SMS-001", f"post-PCS first pending must be SMS-001, got {first_pending(entries)}")

    blocks = registry.setdefault("revalidation_blocks", {})
    require("PCS" not in blocks, "PCS block already exists")
    registry["next_revalidation_block"] = "SMS"
    blocks["PCS"] = {
        "date": "2026-09-10",
        "state": "completed",
        "authority_lane": "official byte-pinned PCS V1.0/V2.1 PDFs plus exact official upstream VDV-301-1.0/2.0/2.1 tag provenance and selected integration XSD blobs",
        "evidence_id": "EV-155",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": PINNED_EV155_RUN,
        "artifact_id": PINNED_EV155_ARTIFACT,
        "artifact_digest": PINNED_EV155_DIGEST,
        "pdf_authority": {
            "PCS_V1.0": {"sha256": PDF_V10_SHA256, "size_bytes": PDF_V10_SIZE, "pages": 18},
            "PCS_V2.1": {"sha256": PDF_V21_SHA256, "size_bytes": PDF_V21_SIZE, "pages": 22},
        },
        "visual_pages": [12, 16, 17],
        "upstream_authority": {
            "VDV-301-1.0_tag_object": "ef38d3babebfbb72e6bcdc42c7026e13bab77f69",
            "VDV-301-1.0_commit": "f5b53785f703e898632603eec3bfa3555a79fdba",
            "VDV-301-2.0_commit": "f2569a91f0a7c737a0ca7c0280b28ad223d7ee08",
            "VDV-301-2.1_commit": "585e0bea34b64887db4276f1c94d5f3e78f06c66",
            "original_PCS_V1.0_blob": "600a3ee6290c630a4435fb06ca9803dabaceb788",
            "original_V1.0_aggregate_blob": "41289eaed2674a169fdf77a10a2eff293c76d5c4",
            "later_self_contained_PCS_V1.0_blob": EXPECTED_PCS_V10_BLOB,
            "PCS_V2.1_blob": EXPECTED_PCS_V21_BLOB,
        },
        "findings": TARGETS,
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "SMS",
        "next_finding": "SMS-001",
    }

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit missing")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE inventory count changed")
    require(audit.get("finding_revalidation_completed_findings") == 138, "unexpected CURRENT_STATE completed count")
    require(audit.get("finding_revalidation_pending_findings") == 54, "unexpected CURRENT_STATE pending count")
    require(audit.get("finding_revalidation_next_block") == "PCS", f"unexpected CURRENT_STATE next block {audit.get('finding_revalidation_next_block')}")
    require(audit.get("finding_revalidation_latest_completed_block") == "VDV301-3_02-2020", "unexpected prior completed block")

    audit["finding_revalidation_next_block"] = "SMS"
    audit["finding_revalidation_completed_findings"] = 140
    audit["finding_revalidation_pending_findings"] = 52
    audit["finding_revalidation_current_block"] = "PCS"
    audit["finding_revalidation_latest_completed_block"] = "PCS"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_revalidation_evidence_id"] = "EV-155"
    audit["latest_executable_evidence_id"] = "EV-155"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["pcs_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-155",
        "run_id": run_id,
        "pinned_successful_evidence_run": PINNED_EV155_RUN,
        "artifact_id": PINNED_EV155_ARTIFACT,
        "artifact_digest": PINNED_EV155_DIGEST,
        "terminal_states": TARGETS,
        "pdf_v10_sha256": PDF_V10_SHA256,
        "pdf_v21_sha256": PDF_V21_SHA256,
        "visual_pages_v21": [12, 16, 17],
        "next_block": "SMS",
        "next_finding": "SMS-001",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report = f"""# Finding revalidation — PassengerCountingService (PCS)\n\nStatus: **completed** on 2026-09-10 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen findings: `PCS-001`, `PCS-002`. Frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Evidence: **EV-155**; successful closure run **{run_id}**.\n- Independently pinned successful EV-155 run: **{PINNED_EV155_RUN}**, artifact **{PINNED_EV155_ARTIFACT}**, digest `{PINNED_EV155_DIGEST}`.\n- Official PCS V1.0 PDF: SHA-256 `{PDF_V10_SHA256}`, {PDF_V10_SIZE} bytes, 18 pages.\n- Official PCS V2.1 PDF: SHA-256 `{PDF_V21_SHA256}`, {PDF_V21_SIZE} bytes, 22 pages.\n- V2.1 physical pages 12, 16 and 17 were rendered from the exact byte-pinned PDF and visibly reviewed.\n- Exact upstream provenance was pinned to official tags `VDV-301-1.0`, `VDV-301-2.0`, and `VDV-301-2.1`.\n- The complete root XSD pool (50 files) was revalidated and byte-hashed before/after closure; no XSD changed.\n\n## Terminal states\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n| `PCS-001` | `executable_confirmed` | PCS V2.1 selects Common V1.0 + Enumerations V1.0. The exact route accepts an existing V1.0 code but rejects documented `OperationNotSupported`; an Enums V2.1-only explanatory control accepts it. This confirms the PDF/XSD dependency/value-set discrepancy without substituting a newer enum family. |\n| `PCS-002` | `contextual_not_defect` | Original VDV-301-1.0 PCS service contains the payload structures but not the operation root; the V1.0 aggregate supplies the root. The later official VDV-301-2.0 self-contained PCS V1.0 supplies the same root, and the same sample payload validates through both complete routes while the checked payload type signatures remain unchanged. This is historical packaging/resolver context, not a payload-contract defect. |\n\n## Closure\n\n- Frozen terminal count: **140 / 192**\n- Frozen pending count: **52 / 192**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n- Next revalidation block: **SMS**\n- First pending finding: **SMS-001**\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")
    print(f"CLOSED PCS: terminal=140 pending=52 next=SMS first_pending=SMS-001 run={run_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
