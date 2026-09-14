#!/usr/bin/env python3
"""Fail-closed closure writer for frozen VideoLiveService findings VLS-001..005."""
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
EVIDENCE_GATE = Path("docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md")
ADDENDUM = Path("docs/pdf_xsd_semantic_audit/VIDEO_LIVE_SERVICE_FINDINGS_REGISTER_ADDENDUM.md")
CORRECTION = Path("docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_CHOICE_NOTATION_2026-08-29.md")
DEEP_V10 = Path("docs/pdf_xsd_semantic_audit/deep_read/VLS_V1.0.md")
DEEP_V20 = Path("docs/pdf_xsd_semantic_audit/deep_read/VLS_V2.0.md")
EV103_DOC = Path("docs/pdf_xsd_semantic_audit/24c_executable_validation_video_compositors.md")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_VLS_2026-09-14.md")
VALIDATOR = Path("tools/validate_vls_revalidation_ev165.py")
EV103 = Path("tools/validate_video_v20_compositors.py")
XSD_POOL = Path("tools/validate_xsd_pool.py")
VLS20 = Path("IBIS-IP_VideoLiveService_V2.0.xsd")
COMMON20 = Path("IBIS-IP_common_V2.0.xsd")
ENUM20 = Path("IBIS-IP_Enumerations_V2.0.xsd")

EXPECTED = {
    FROZEN: "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
    REGISTRY: "62a3ecdd3f77c25dc6ed8e6754bc351db824ebb5",
    STATE: "1c496ec0e0f3a45c0120650adf4df1a62659b225",
    SOURCE_REGISTRY: "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
    SOURCE_PINS: "88349638b423689799af700e8a1c8ec99bbfb67b",
    EVIDENCE_GATE: "969cce8b14b50ded2ca5eb745674b894428ecf1a",
    ADDENDUM: "fa3c1be9dfb34726fdf73ae8c518a051021c39ed",
    CORRECTION: "fe024798ba1b9803ec70ee3b97def63ee03d298f",
    DEEP_V10: "1fa2c8949144c902feeba4aeaa714e029f993fa0",
    DEEP_V20: "d719cebafd51d07b486d9f6ccd1b65e9b101329d",
    EV103_DOC: "77bceaea8c3a6d4f113d9b38ba6ef4062859c6d7",
    VALIDATOR: "dc806353e912ae69cc2eb3d8cc04d380c9b8c7da",
    EV103: "9c85d362a597b357a69577477bacc8dc8fcbe177",
    XSD_POOL: "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd",
    VLS20: "d8c52f5de9ef3f5915524fef12da11eabf0ca041",
    COMMON20: "8608e3dcd665c197c34da7f6ec6af5a3758da164",
    ENUM20: "27e3c183b00381d959622d13c10543123af8eef6",
}

PINNED_RUN = "34839986276"
PINNED_JOB = "103962447178"
PINNED_ARTIFACT = "10345886539"
PINNED_DIGEST = "sha256:20d85319cc0d8014102abaf9ce6bf985c5510d59d631403030f172be5c5c90b7"
PINNED_HEAD = "b22d3d2840b68b62f5135ba8a583dc5fe63e496f"

TARGETS = {
    "VLS-001": "context_verified",
    "VLS-002": "executable_confirmed",
    "VLS-003": "context_verified",
    "VLS-004": "context_verified",
    "VLS-005": "context_verified",
}
TERMINAL = {"context_verified", "executable_confirmed", "contextual_not_defect", "withdrawn", "unresolved", "superseded"}


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


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def counts(entries: list[dict]) -> tuple[int, int]:
    return (
        sum(x.get("revalidation_state") in TERMINAL for x in entries),
        sum(x.get("revalidation_state") == "pending" for x in entries),
    )


def first_pending(entries: list[dict]) -> str | None:
    return next((x.get("finding_id") for x in entries if x.get("revalidation_state") == "pending"), None)


def main() -> int:
    run_id = os.environ.get("EVIDENCE_RUN_ID", "").strip()
    run_url = os.environ.get("EVIDENCE_RUN_URL", "").strip()
    require(run_id.isdigit(), "EVIDENCE_RUN_ID is numeric")
    require(run_url == f"https://github.com/MarcLeinenDE/VDV301/actions/runs/{run_id}", "EVIDENCE_RUN_URL matches run id")

    for path, expected in EXPECTED.items():
        require(path.is_file() and blob(path) == expected, f"exact prestate/authority blob {path} = {expected}")
    require(not REPORT.exists(), "VLS closure report does not pre-exist")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory remains exactly 192")
    require(all(fid in frozen.get("finding_ids", []) for fid in TARGETS), "all VLS targets are frozen inventory members")

    registry = load(REGISTRY)
    entries = registry["inventory"]["entries"]
    by_id = {x["finding_id"]: x for x in entries}
    require(len(entries) == len(by_id) == 192, "registry contains exactly 192 unique findings")
    require(registry.get("next_revalidation_block") == "VLS", "prestate next block is VLS")
    require(counts(entries) == (176, 16), f"pre-VLS counts are 176/16, got {counts(entries)}")
    require(first_pending(entries) == "VLS-001", "pre-VLS first pending is VLS-001")
    for fid in TARGETS:
        require(by_id[fid].get("revalidation_state") == "pending" and by_id[fid].get("terminal_state_source") is None, f"{fid} is pending without premature source")
    require(by_id["VRS-001"].get("revalidation_state") == "pending", "VRS-001 remains pending before VLS closure")
    require(registry.get("revalidation_blocks", {}).get("VDS", {}).get("state") == "completed", "VDS is prior completed block")
    require("VLS" not in registry.get("revalidation_blocks", {}), "VLS block is not already closed")

    state_doc = load(STATE)
    audit = state_doc["audit"]
    require(audit.get("finding_revalidation_completed_findings") == 176, "CURRENT_STATE pre-VLS terminal count is 176")
    require(audit.get("finding_revalidation_pending_findings") == 16, "CURRENT_STATE pre-VLS pending count is 16")
    require(audit.get("finding_revalidation_next_block") == "VLS", "CURRENT_STATE pre-VLS next block is VLS")
    require(audit.get("finding_revalidation_latest_completed_block") == "VDS", "VDS is prior CURRENT_STATE completed block")
    require(audit.get("latest_revalidation_evidence_id") == "EV-164", "EV-164 is prior revalidation evidence")

    for fid, terminal_state in TARGETS.items():
        by_id[fid]["revalidation_state"] = terminal_state
        by_id[fid]["terminal_state_source"] = str(REPORT)

    require(counts(entries) == (181, 11), f"post-VLS counts are 181/11, got {counts(entries)}")
    next_finding = first_pending(entries)
    require(next_finding == "VRS-001", f"post-VLS first pending is VRS-001, got {next_finding}")

    authority_boundary = {
        "VLS_V1.0": "official public VDV PDF authority; exact official V1.0 VideoLiveService XSD unresolved; V2.0 is not substituted",
        "VLS_V2.0": "official VDV-301-2.0 release family; service/Common/Enums exact upstream blobs",
        "EV-103": "official V2.0 executable compositor evidence for VLS-002",
        "VLS-005": "leading minus is valid VDV XML-choice notation; only the refined incomplete/ambiguous notation-application issue is retained",
    }

    registry["next_revalidation_block"] = "VRS"
    registry.setdefault("revalidation_blocks", {})["VLS"] = {
        "date": "2026-09-14",
        "state": "completed",
        "authority_lane": "byte-pinned official VLS V1.0/V2.0 PDFs, exact official V2.0 release XSD route, EV-103 executable evidence, visual evidence, and choice-notation correction overlay",
        "authority_boundary": authority_boundary,
        "evidence_id": "EV-165",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": PINNED_RUN,
        "pinned_successful_evidence_job": PINNED_JOB,
        "artifact_id": PINNED_ARTIFACT,
        "artifact_digest": PINNED_DIGEST,
        "evidence_head_sha": PINNED_HEAD,
        "underlying_executable_evidence": ["EV-103"],
        "visual_evidence_runs": ["33202961159", "33203162588", "33203850390"],
        "full_xsd_regression_pool": {"root_xsd_count": 50, "result": "PASS"},
        "findings": TARGETS,
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "VRS",
        "next_finding": next_finding,
    }

    audit["finding_revalidation_next_block"] = "VRS"
    audit["finding_revalidation_completed_findings"] = 181
    audit["finding_revalidation_pending_findings"] = 11
    audit["finding_revalidation_current_block"] = "VLS"
    audit["finding_revalidation_latest_completed_block"] = "VLS"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_revalidation_evidence_id"] = "EV-165"
    audit["latest_executable_evidence_id"] = "EV-165"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["vls_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-165",
        "run_id": run_id,
        "pinned_successful_evidence_run": PINNED_RUN,
        "pinned_successful_evidence_job": PINNED_JOB,
        "artifact_id": PINNED_ARTIFACT,
        "artifact_digest": PINNED_DIGEST,
        "evidence_head_sha": PINNED_HEAD,
        "terminal_states": TARGETS,
        "authority_boundary": authority_boundary,
        "xsd_pool_result": "PASS_50_root_XSDs",
        "next_block": "VRS",
        "next_finding": next_finding,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report = f"""# Finding revalidation — VideoLiveService (VLS)\n\nStatus: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen findings: `VLS-001` through `VLS-005`. Frozen inventory remains exactly **192 entries**.\n\n## Evidence\n\n- Aggregate evidence: **EV-165**; closure run **{run_id}**.\n- Successful EV-165 validation run: **{PINNED_RUN}**, job **{PINNED_JOB}**, artifact **{PINNED_ARTIFACT}**, digest `{PINNED_DIGEST}`, head `{PINNED_HEAD}`.\n- Underlying executable compositor evidence: **EV-103**, run `33111119723`, job `98653897734`, artifact `9662552176`.\n- VLS V1.0 PDF: official byte pin `f535673427ff8f495102e1fc7723ca157408949b981572c4342b862f6d9c2a3c`; visual runs `33202961159`, `33203162588`.\n- VLS V2.0 PDF: official byte pin `d75a543c138f21c4ad370925ca7f306bcde7d692ce793ddc1d51bdcf6032787b`; visual run `33203850390`.\n- Official V2.0 XSD authority: `VDV-301-2.0` / commit `f2569a91f0a7c737a0ca7c0280b28ad223d7ee08`; VLS blob `d8c52f5de9ef3f5915524fef12da11eabf0ca041`, Common `8608e3dcd665c197c34da7f6ec6af5a3758da164`, Enums `27e3c183b00381d959622d13c10543123af8eef6`.\n- Complete regression pool: **50 root XSDs — PASS**.\n\n## Terminal decisions\n\n| Finding | State | Decision |\n|---|---|---|\n| VLS-001 | `context_verified` | The provenance gap itself is verified: the official V1.0 publication exists, but no exact official V1.0 VideoLiveService service XSD is confirmed in the checked release route. V2.0 is not substituted. |\n| VLS-002 | `executable_confirmed` | Official V2.0 PDF presents a multi-field `LiveStreamData`; exact V2.0 XSD uses `xs:choice`. EV-103 confirms the executable boundary. |\n| VLS-003 | `context_verified` | V1.0 German foreword visibly uses the wrong part number `301-2-1`; V2.0 corrects it to `301-2-11`. Documentation-only. |\n| VLS-004 | `context_verified` | VideoLive start/stop prose visibly substitutes `VideoDisplayService`; the error persists into V2.0. No alias/routing rule is inferred. |\n| VLS-005 | `context_verified` | Corrected finding only: leading-minus notation is valid VDV XML-choice notation. The surviving issue is incomplete/ambiguous application in the checked VLS tables. |\n\n## Authority boundaries\n\n- VLS V1.0 remains documentation authority only because no exact strict V1.0 service-XSD route is confirmed.\n- VLS V2.0 executable conclusions use the exact official release-tag XSD family only.\n- `VLS-005` must always be read through the 2026-08-29 choice-notation correction overlay.\n- Runtime RTSP/RTP behavior remains outside XML/XSD validation except where separately established by runtime evidence.\n\n## Closure\n\nPrestate: **176 terminal / 16 pending**.\n\nPoststate: **181 terminal / 11 pending**.\n\nNext finding: **`VRS-001`**. Next block: **VRS**.\n\nNo XSD mutation. No frozen-inventory mutation.\n"""

    write_json(REGISTRY, registry)
    write_json(STATE, state_doc)
    REPORT.write_text(report, encoding="utf-8")

    require(blob(FROZEN) == EXPECTED[FROZEN], "frozen inventory unchanged after write")
    require(blob(SOURCE_REGISTRY) == EXPECTED[SOURCE_REGISTRY], "PDF source registry unchanged after write")
    require(blob(SOURCE_PINS) == EXPECTED[SOURCE_PINS], "PDF source pins unchanged after write")
    require(blob(VLS20) == EXPECTED[VLS20], "selected V2.0 XSD authority unchanged after write")
    print("PASSED: VLS closure files prepared; expected poststate 181/11 -> VRS-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
