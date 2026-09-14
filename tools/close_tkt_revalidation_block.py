#!/usr/bin/env python3
"""Fail-closed closure writer for frozen TicketingService findings TKT-001..009."""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
SOURCE_REGISTRY = Path("audit_registry/pdf_source_registry_v0.1.json")
EVIDENCE_GATE = Path("docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md")
ADDENDUM = Path("docs/pdf_xsd_semantic_audit/TICKETING_SERVICE_FINDINGS_REGISTER_ADDENDUM.md")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_TKT_2026-09-14.md")
VALIDATOR = Path("tools/validate_tkt_revalidation_ev158.py")
XSD_POOL = Path("tools/validate_xsd_pool.py")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_REGISTRY_PRE_BLOB = "287e3bbcf4130567b288b1d039e8f576b668012b"
EXPECTED_STATE_PRE_BLOB = "a911f050fa5e7affc3d03ec9f2b21c68c848d364"
EXPECTED_SOURCE_REGISTRY_BLOB = "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8"
EXPECTED_EVIDENCE_GATE_BLOB = "969cce8b14b50ded2ca5eb745674b894428ecf1a"
EXPECTED_ADDENDUM_BLOB = "5f526763b2c68beb58b40922b52b6f0c7c9b554b"
EXPECTED_VALIDATOR_BLOB = "be3016b326e013b587621d59402ee57bb39ff318"
EXPECTED_XSD_POOL_BLOB = "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd"

EXPECTED_XSDS = {
    "IBIS-IP_TicketInformationService_V1.0.xsd": "3fda66d872ab0d1c511247f13e715cf3ad56afe7",
    "IBIS-IP_common_V1.0.xsd": "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c",
    "IBIS-IP_Enumerations_V1.0.xsd": "a9bea5bc73003ed91ded8519db06c32c4067831d",
}

PDF_SHA256 = "96241226c7a25b0384527dd3de5fcd9448c8e75f38bfb4ffd7b607680bfc6b43"
PDF_SIZE = 627099
PDF_PAGES = 16
PDF_TEXT_SHA256 = "8f23aa2b8c7c12b601ca603a4154624c66989acf36642ae64cf119ef0b268ca8"
PDF_URL = "https://www.vdv.de/301-2-9sds-v1-0.pdfx"

SOURCE_PIN_RUN = "34771722424"
SOURCE_PIN_JOB = "103762406542"
SOURCE_PIN_ARTIFACT = "10322336797"
SOURCE_PIN_DIGEST = "sha256:df661f9444ab7e26b563b0c748fee583314b19d789b316c6405e45e1fe99589c"

PINNED_EV158_RUN = "34813527845"
PINNED_EV158_JOB = "103879396942"
PINNED_EV158_ARTIFACT = "10336185560"
PINNED_EV158_DIGEST = "sha256:ba5ee246787f58d4cf690421fda683fb1dd072106d5c4e7eb6376c218b717870"
PINNED_EV158_HEAD = "c4550faa535b012f19cf4f5f909e813cfcac7bb1"

UPSTREAM = {
    "v1_0_tag_object": "ef38d3babebfbb72e6bcdc42c7026e13bab77f69",
    "v1_0_commit": "f5b53785f703e898632603eec3bfa3555a79fdba",
    "v1_0_tree": "729bbe3270e52fed3e0641466048a745d5a09b32",
    "v1_0_ticket_blob": "017ca64666e25d757fc0cde1f1be817f06a743fc",
    "v1_0_common_blob": "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c",
    "v1_0_enums_blob": "a9bea5bc73003ed91ded8519db06c32c4067831d",
    "v1_0_aggregate_blob": "41289eaed2674a169fdf77a10a2eff293c76d5c4",
    "v2_0_commit": "f2569a91f0a7c737a0ca7c0280b28ad223d7ee08",
    "v2_0_tree": "11daf0ebb3b26745c036ee19a547ad16d39f922c",
    "v2_0_ticket_blob": "3fda66d872ab0d1c511247f13e715cf3ad56afe7",
    "v2_0_common_v1_blob": "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c",
    "v2_0_enums_v1_blob": "a9bea5bc73003ed91ded8519db06c32c4067831d",
}

TARGETS = {
    "TKT-001": "context_verified",
    "TKT-002": "contextual_not_defect",
    "TKT-003": "context_verified",
    "TKT-004": "executable_confirmed",
    "TKT-005": "context_verified",
    "TKT-006": "executable_confirmed",
    "TKT-007": "context_verified",
    "TKT-008": "executable_confirmed",
    "TKT-009": "context_verified",
}

RATIONALES = {
    "TKT-001": "The same TicketInformationService V1.0 path has distinct official blobs and executable surfaces in the VDV-301-1.0 and VDV-301-2.0 release contexts; resolution therefore requires release context/schema revision rather than the filename version alone.",
    "TKT-002": "TicketInformationService is a filename token; executable schema identities are TicketingService.*. No TicketInformationService.* executable alias is declared.",
    "TKT-003": "The PDF assigns SubscribeResponseStructure to UnsubscribeValidationResult, while Common V1.0 defines UnsubscribeResponseStructure. Both response structures have the same Active/OperationErrorMessage XML choice, so this is a documentation type-name discrepancy without XML-shape delta.",
    "TKT-004": "The exact TicketingService.ValidateTicketRequest root validates, while the PDF heading TicketInformationService.Validation.GetDataRequest is not an executable root and is rejected.",
    "TKT-005": "The PDF overview names TicketingService.ValidationResultStructure, which is absent from the XSD; the executable GetValidationResult root maps to TicketingService.GetValidationResultResponseStructure.",
    "TKT-006": "The XSD sequence is DefaultLanguage before TimeStamp. Executable validation accepts progression in XSD order and rejects the PDF order at the first misplaced field.",
    "TKT-007": "The PDF detailed table labels the outer GetValidationResultResponseStructure while the displayed TimeStamp/ValidationResult fields belong to TicketingService.ValidationResultDataStructure.",
    "TKT-008": "CardApplikationInformation is the schema-declared spelling and validates; the PDF spelling CardApplicationInformation is rejected by the exact XSD. PDF page 11 is preserved as rendered visual evidence because text extraction interleaves the table columns.",
    "TKT-009": "The official PDF visibly uses TicketingSevice in labels, while the XSD exposes no such alias; executable service identity remains TicketingService.",
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
        EVIDENCE_GATE: EXPECTED_EVIDENCE_GATE_BLOB,
        ADDENDUM: EXPECTED_ADDENDUM_BLOB,
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
    require(all(fid in frozen_ids for fid in TARGETS), "all TKT targets are frozen inventory members")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen", "registry inventory remains frozen")
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory remains 192 entries")
    require(registry.get("next_revalidation_block") == "TKT", "prestate next block is TKT")
    ids = [e.get("finding_id") for e in entries]
    require(len(ids) == len(set(ids)) == 192, "registry finding IDs remain unique")
    by_id = {e["finding_id"]: e for e in entries}
    for fid in TARGETS:
        require(by_id[fid].get("revalidation_state") == "pending", f"{fid} is pending before closure")
        require(by_id[fid].get("terminal_state_source") is None, f"{fid} has no premature terminal source")
    require(counts(entries) == (146, 46), f"pre-TKT counts are 146/46, got {counts(entries)}")
    require(first_pending(entries) == "TKT-001", f"pre-TKT first pending is TKT-001, got {first_pending(entries)}")
    require(by_id.get("TS-001", {}).get("revalidation_state") == "pending", "TS-001 remains pending before TKT closure")

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit exists")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE inventory count remains 192")
    require(audit.get("finding_revalidation_completed_findings") == 146, "CURRENT_STATE pre-TKT terminal count is 146")
    require(audit.get("finding_revalidation_pending_findings") == 46, "CURRENT_STATE pre-TKT pending count is 46")
    require(audit.get("finding_revalidation_next_block") == "TKT", "CURRENT_STATE pre-TKT next block is TKT")
    require(audit.get("finding_revalidation_latest_completed_block") == "SUB", "SUB is prior completed block")

    source_registry = load(SOURCE_REGISTRY)
    sources = {x["source_id"]: x for x in source_registry.get("sources", [])}
    require(sources["TICKETING_V1.0"]["official_url"] == PDF_URL, "Ticketing V1.0 source URL unchanged")

    for fid, terminal_state in TARGETS.items():
        by_id[fid]["revalidation_state"] = terminal_state
        by_id[fid]["terminal_state_source"] = str(REPORT)

    require(counts(entries) == (155, 37), f"post-TKT counts are 155/37, got {counts(entries)}")
    next_finding = first_pending(entries)
    require(next_finding == "TS-001", f"post-TKT first pending is TS-001, got {next_finding}")
    next_block = next_finding.split("-", 1)[0] if next_finding else None
    require(next_block == "TS", f"post-TKT next block is TS, got {next_block}")

    blocks = registry.setdefault("revalidation_blocks", {})
    require("TKT" not in blocks, "TKT block is not already closed")
    registry["next_revalidation_block"] = next_block
    blocks["TKT"] = {
        "date": "2026-09-14",
        "state": "completed",
        "authority_lane": "official byte-pinned VDV 301-2-9 TicketingService V1.0 PDF plus exact VDV-301-1.0 and VDV-301-2.0 upstream release contexts",
        "evidence_id": "EV-158",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": PINNED_EV158_RUN,
        "pinned_successful_evidence_job": PINNED_EV158_JOB,
        "artifact_id": PINNED_EV158_ARTIFACT,
        "artifact_digest": PINNED_EV158_DIGEST,
        "evidence_head_sha": PINNED_EV158_HEAD,
        "source_pin": {
            "run_id": SOURCE_PIN_RUN,
            "job_id": SOURCE_PIN_JOB,
            "artifact_id": SOURCE_PIN_ARTIFACT,
            "artifact_digest": SOURCE_PIN_DIGEST,
        },
        "pdf_authority": {
            "source_id": "TICKETING_V1.0",
            "official_url": PDF_URL,
            "sha256": PDF_SHA256,
            "size_bytes": PDF_SIZE,
            "pages": PDF_PAGES,
            "pdftotext_sha256": PDF_TEXT_SHA256,
            "visual_pages": [7, 8, 9, 10, 11, 12],
            "page_11_evidence_mode": "rendered_visual_only_for_CardApplicationInformation_label",
        },
        "upstream_authority": UPSTREAM,
        "xsd_blobs": EXPECTED_XSDS,
        "findings": TARGETS,
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": next_block,
        "next_finding": next_finding,
    }

    audit["finding_revalidation_next_block"] = next_block
    audit["finding_revalidation_completed_findings"] = 155
    audit["finding_revalidation_pending_findings"] = 37
    audit["finding_revalidation_current_block"] = "TKT"
    audit["finding_revalidation_latest_completed_block"] = "TKT"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_revalidation_evidence_id"] = "EV-158"
    audit["latest_executable_evidence_id"] = "EV-158"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["tkt_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-158",
        "run_id": run_id,
        "pinned_successful_evidence_run": PINNED_EV158_RUN,
        "pinned_successful_evidence_job": PINNED_EV158_JOB,
        "artifact_id": PINNED_EV158_ARTIFACT,
        "artifact_digest": PINNED_EV158_DIGEST,
        "source_pin_run": SOURCE_PIN_RUN,
        "source_pin_artifact": SOURCE_PIN_ARTIFACT,
        "terminal_states": TARGETS,
        "pdf_sha256": PDF_SHA256,
        "visual_pages": [7, 8, 9, 10, 11, 12],
        "next_block": next_block,
        "next_finding": next_finding,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    rows = "\n".join(
        f"| `{fid}` | `{TARGETS[fid]}` | {RATIONALES[fid]} |" for fid in TARGETS
    )
    report = f"""# Finding revalidation — TicketingService (TKT)\n\nStatus: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen findings: `TKT-001` through `TKT-009`. Frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Evidence: **EV-158**; successful closure run **{run_id}**.\n- Independently successful EV-158 run: **{PINNED_EV158_RUN}**, job **{PINNED_EV158_JOB}**, artifact **{PINNED_EV158_ARTIFACT}**, digest `{PINNED_EV158_DIGEST}`.\n- Source/render pin run: **{SOURCE_PIN_RUN}**, job **{SOURCE_PIN_JOB}**, artifact **{SOURCE_PIN_ARTIFACT}**, digest `{SOURCE_PIN_DIGEST}`.\n- Official VDV 301-2-9 TicketingService V1.0 PDF: SHA-256 `{PDF_SHA256}`, {PDF_SIZE} bytes, {PDF_PAGES} pages.\n- Targeted physical pages 7-12 were rendered from the exact pinned PDF. Page 11 is visual-only evidence for the visible `CardApplicationInformation` label because Poppler interleaves that table's columns; the executable XSD spelling boundary is tested independently.\n- Official upstream release contexts: VDV-301-1.0 commit `{UPSTREAM['v1_0_commit']}` carries TicketInformationService V1.0 blob `{UPSTREAM['v1_0_ticket_blob']}`; VDV-301-2.0 commit `{UPSTREAM['v2_0_commit']}` carries blob `{UPSTREAM['v2_0_ticket_blob']}`.\n- The complete 50-file root XSD pool was recompiled and byte-hashed before/after EV-158; no XSD changed.\n\n## Terminal states\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n{rows}\n\n## Mutation decision\n\n- XSD mutation: **none**.\n- Frozen inventory mutation: **none**.\n- Registry/status mutation: only the nine frozen TKT findings and block/counter handoff.\n\n## State transition\n\n- Before: **146/192 terminal**, **46 pending**, first pending `TKT-001`.\n- After: **155/192 terminal**, **37 pending**, first pending `{next_finding}`.\n- Next block: **{next_block}**.\n"""

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")
    write_json(REGISTRY, registry)
    write_json(STATE, state)

    require(load(FROZEN).get("entry_count") == 192, "frozen inventory still 192 after writes")
    require(git_blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory bytes unchanged after writes")
    for name, blob in EXPECTED_XSDS.items():
        require(git_blob(Path(name)) == blob, f"XSD unchanged after writes: {name}")
    require(git_blob(SOURCE_REGISTRY) == EXPECTED_SOURCE_REGISTRY_BLOB, "PDF source registry unchanged after writes")

    post_registry = load(REGISTRY)
    post_entries = post_registry["inventory"]["entries"]
    require(counts(post_entries) == (155, 37), "written registry counts are 155/37")
    require(first_pending(post_entries) == "TS-001", "written registry first pending is TS-001")
    require(post_registry.get("next_revalidation_block") == "TS", "written registry next block is TS")
    require(post_registry["revalidation_blocks"]["TKT"]["artifact_digest"] == PINNED_EV158_DIGEST, "written TKT block pins EV-158 artifact digest")

    post_audit = load(STATE)["audit"]
    require(post_audit.get("finding_revalidation_completed_findings") == 155, "written CURRENT_STATE terminal count is 155")
    require(post_audit.get("finding_revalidation_pending_findings") == 37, "written CURRENT_STATE pending count is 37")
    require(post_audit.get("finding_revalidation_next_block") == "TS", "written CURRENT_STATE next block is TS")
    require(post_audit.get("finding_revalidation_latest_completed_block") == "TKT", "written CURRENT_STATE latest block is TKT")
    require(REPORT.is_file(), "TKT revalidation report written")
    print("PASS TKT closure writer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
