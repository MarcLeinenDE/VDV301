#!/usr/bin/env python3
"""Fail-closed closure writer for frozen VideoDisplayService findings VDS-001..008."""
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
ADDENDUM = Path("docs/pdf_xsd_semantic_audit/VIDEO_DISPLAY_SERVICE_FINDINGS_REGISTER_ADDENDUM.md")
CORRECTION = Path("docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_CHOICE_NOTATION_2026-08-29.md")
DEEP_V10 = Path("docs/pdf_xsd_semantic_audit/deep_read/VDS_V1.0.md")
DEEP_V20 = Path("docs/pdf_xsd_semantic_audit/deep_read/VDS_V2.0.md")
EV103_DOC = Path("docs/pdf_xsd_semantic_audit/24c_executable_validation_video_compositors.md")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_VDS_2026-09-14.md")
VALIDATOR = Path("tools/validate_vds_revalidation_ev164.py")
EV103 = Path("tools/validate_video_v20_compositors.py")
XSD_POOL = Path("tools/validate_xsd_pool.py")
VDS20 = Path("IBIS-IP_VideoDisplayService_V2.0.xsd")
COMMON20 = Path("IBIS-IP_common_V2.0.xsd")
ENUM20 = Path("IBIS-IP_Enumerations_V2.0.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_REGISTRY_PRE_BLOB = "13ef10dfe353ad51b2cecd371333bd12e35c8e6b"
EXPECTED_STATE_PRE_BLOB = "81d24c501c5fd483853075fbdc9edeecdc7d6df7"
EXPECTED_SOURCE_REGISTRY_BLOB = "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8"
EXPECTED_SOURCE_PINS_BLOB = "88349638b423689799af700e8a1c8ec99bbfb67b"
EXPECTED_EVIDENCE_GATE_BLOB = "969cce8b14b50ded2ca5eb745674b894428ecf1a"
EXPECTED_ADDENDUM_BLOB = "d5d2903ed04448ba3793b4eb1b7aa2c192ca5b3a"
EXPECTED_CORRECTION_BLOB = "fe024798ba1b9803ec70ee3b97def63ee03d298f"
EXPECTED_DEEP_V10_BLOB = "9ee386d7b2c869b1dd74c330797a30a49aedde1d"
EXPECTED_DEEP_V20_BLOB = "0989aa830dba52a8b562c7abc8d72f63b8c27f3d"
EXPECTED_EV103_DOC_BLOB = "77bceaea8c3a6d4f113d9b38ba6ef4062859c6d7"
EXPECTED_VALIDATOR_BLOB = "fe2e11a9389accd4c3b111530d56bda1621e2036"
EXPECTED_EV103_BLOB = "9c85d362a597b357a69577477bacc8dc8fcbe177"
EXPECTED_XSD_POOL_BLOB = "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd"
EXPECTED_VDS20_BLOB = "fcfdadd3b62a584370cae326004050b4dc832e23"
EXPECTED_COMMON20_BLOB = "8608e3dcd665c197c34da7f6ec6af5a3758da164"
EXPECTED_ENUM20_BLOB = "27e3c183b00381d959622d13c10543123af8eef6"

PINNED_EV164_RUN = "34838003303"
PINNED_EV164_JOB = "103956188197"
PINNED_EV164_ARTIFACT = "10345007994"
PINNED_EV164_DIGEST = "sha256:ef85ea5999c2fee585b493fb3705031d6a231e251efab7bcce6d92e30d6f05dd"
PINNED_EV164_HEAD = "233e54e59bb027a629c9f16274666b336866951d"

TARGETS = {
    "VDS-001": "context_verified",
    "VDS-002": "executable_confirmed",
    "VDS-003": "executable_confirmed",
    "VDS-004": "executable_confirmed",
    "VDS-005": "context_verified",
    "VDS-006": "context_verified",
    "VDS-007": "context_verified",
    "VDS-008": "context_verified",
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

    immutable = {
        FROZEN: EXPECTED_FROZEN_BLOB,
        REGISTRY: EXPECTED_REGISTRY_PRE_BLOB,
        STATE: EXPECTED_STATE_PRE_BLOB,
        SOURCE_REGISTRY: EXPECTED_SOURCE_REGISTRY_BLOB,
        SOURCE_PINS: EXPECTED_SOURCE_PINS_BLOB,
        EVIDENCE_GATE: EXPECTED_EVIDENCE_GATE_BLOB,
        ADDENDUM: EXPECTED_ADDENDUM_BLOB,
        CORRECTION: EXPECTED_CORRECTION_BLOB,
        DEEP_V10: EXPECTED_DEEP_V10_BLOB,
        DEEP_V20: EXPECTED_DEEP_V20_BLOB,
        EV103_DOC: EXPECTED_EV103_DOC_BLOB,
        VALIDATOR: EXPECTED_VALIDATOR_BLOB,
        EV103: EXPECTED_EV103_BLOB,
        XSD_POOL: EXPECTED_XSD_POOL_BLOB,
        VDS20: EXPECTED_VDS20_BLOB,
        COMMON20: EXPECTED_COMMON20_BLOB,
        ENUM20: EXPECTED_ENUM20_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file() and blob(path) == expected, f"exact prestate/authority blob {path} = {expected}")

    require(not REPORT.exists(), "VDS closure report does not pre-exist")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory remains exactly 192")
    require(all(fid in frozen.get("finding_ids", []) for fid in TARGETS), "all VDS targets are frozen inventory members")

    registry = load(REGISTRY)
    entries = registry["inventory"]["entries"]
    ids = [x["finding_id"] for x in entries]
    require(len(ids) == len(set(ids)) == 192, "registry contains exactly 192 unique findings")
    require(registry.get("next_revalidation_block") == "VDS", "prestate next block is VDS")
    require(counts(entries) == (168, 24), f"pre-VDS counts are 168/24, got {counts(entries)}")
    require(first_pending(entries) == "VDS-001", "pre-VDS first pending is VDS-001")
    by_id = {x["finding_id"]: x for x in entries}
    for fid in TARGETS:
        require(by_id[fid].get("revalidation_state") == "pending" and by_id[fid].get("terminal_state_source") is None, f"{fid} is pending without premature source")
    require(by_id["VLS-001"].get("revalidation_state") == "pending", "VLS-001 remains pending before VDS closure")
    require(registry.get("revalidation_blocks", {}).get("TVS", {}).get("state") == "completed", "TVS is prior completed block")
    require("VDS" not in registry.get("revalidation_blocks", {}), "VDS block is not already closed")

    audit = load(STATE)["audit"]
    require(audit.get("finding_revalidation_completed_findings") == 168, "CURRENT_STATE pre-VDS terminal count is 168")
    require(audit.get("finding_revalidation_pending_findings") == 24, "CURRENT_STATE pre-VDS pending count is 24")
    require(audit.get("finding_revalidation_next_block") == "VDS", "CURRENT_STATE pre-VDS next block is VDS")
    require(audit.get("finding_revalidation_latest_completed_block") == "TVS", "TVS is prior CURRENT_STATE completed block")
    require(audit.get("latest_revalidation_evidence_id") == "EV-163", "EV-163 is prior revalidation evidence")
    require(audit.get("latest_executable_evidence_id") == "EV-163", "EV-163 is prior executable evidence")

    for fid, terminal_state in TARGETS.items():
        by_id[fid]["revalidation_state"] = terminal_state
        by_id[fid]["terminal_state_source"] = str(REPORT)

    require(counts(entries) == (176, 16), f"post-VDS counts are 176/16, got {counts(entries)}")
    next_finding = first_pending(entries)
    require(next_finding == "VLS-001", f"post-VDS first pending is VLS-001, got {next_finding}")

    authority_boundary = {
        "VDS_V1.0": "official public VDV PDF authority; exact official V1.0 VideoDisplayService XSD unresolved; V2.0 XSD is not substituted",
        "VDS_V2.0": "official VDV-301-2.0 release family; service/Common/Enums exact upstream blobs",
        "EV-103": "official V2.0 executable compositor evidence for VDS-002..004",
        "VDS-006": "leading minus is valid VDV XML-choice notation; only the refined incomplete/degenerate application anomaly is retained",
        "VDS-008": "RTP/SOA terminology cross-checked against RFC 3550 and OASIS SOA Reference Model; documentation-only",
    }

    registry["next_revalidation_block"] = "VLS"
    registry.setdefault("revalidation_blocks", {})["VDS"] = {
        "date": "2026-09-14",
        "state": "completed",
        "authority_lane": "byte-pinned official VDS V1.0/V2.0 PDFs, exact official V2.0 release XSD route, EV-103 executable evidence, visual evidence, correction overlay, and external terminology authority",
        "authority_boundary": authority_boundary,
        "evidence_id": "EV-164",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": PINNED_EV164_RUN,
        "pinned_successful_evidence_job": PINNED_EV164_JOB,
        "artifact_id": PINNED_EV164_ARTIFACT,
        "artifact_digest": PINNED_EV164_DIGEST,
        "evidence_head_sha": PINNED_EV164_HEAD,
        "underlying_executable_evidence": ["EV-103"],
        "visual_evidence_runs": ["33225843645", "33226294383"],
        "full_xsd_regression_pool": {"root_xsd_count": 50, "result": "PASS"},
        "findings": TARGETS,
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "VLS",
        "next_finding": next_finding,
    }

    audit["finding_revalidation_next_block"] = "VLS"
    audit["finding_revalidation_completed_findings"] = 176
    audit["finding_revalidation_pending_findings"] = 16
    audit["finding_revalidation_current_block"] = "VDS"
    audit["finding_revalidation_latest_completed_block"] = "VDS"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_revalidation_evidence_id"] = "EV-164"
    audit["latest_executable_evidence_id"] = "EV-164"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["vds_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-164",
        "run_id": run_id,
        "pinned_successful_evidence_run": PINNED_EV164_RUN,
        "pinned_successful_evidence_job": PINNED_EV164_JOB,
        "artifact_id": PINNED_EV164_ARTIFACT,
        "artifact_digest": PINNED_EV164_DIGEST,
        "evidence_head_sha": PINNED_EV164_HEAD,
        "terminal_states": TARGETS,
        "authority_boundary": authority_boundary,
        "xsd_pool_result": "PASS_50_root_XSDs",
        "next_block": "VLS",
        "next_finding": next_finding,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report = f"""# Finding revalidation — VideoDisplayService (VDS)\n\nStatus: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen findings: `VDS-001` through `VDS-008`. Frozen inventory remains exactly **192 entries**.\n\n## Evidence\n\n- Aggregate evidence: **EV-164**; closure run **{run_id}**.\n- Successful EV-164 validation run: **{PINNED_EV164_RUN}**, job **{PINNED_EV164_JOB}**, artifact **{PINNED_EV164_ARTIFACT}**, digest `{PINNED_EV164_DIGEST}`, head `{PINNED_EV164_HEAD}`.\n- Underlying executable compositor evidence: **EV-103**, run `33111119723`, job `98653897734`, artifact `9662552176`.\n- VDS V1.0 PDF: official byte pin `9280cc239cf71bb158ab5941b522a2c4c822420e07ed44f4d4111d9689418480`, visual run `33225843645`.\n- VDS V2.0 PDF: official byte pin `c287df20d8225af2afcd37dfdb487eb4922b89ce78c287da91745d12b410c8a2`, visual run `33226294383`.\n- Official V2.0 XSD authority: `VDV-301-2.0` / commit `f2569a91f0a7c737a0ca7c0280b28ad223d7ee08`; VDS blob `fcfdadd3b62a584370cae326004050b4dc832e23`, Common `8608e3dcd665c197c34da7f6ec6af5a3758da164`, Enums `27e3c183b00381d959622d13c10543123af8eef6`.\n- Complete regression pool: **50 root XSDs — PASS**.\n\n## Terminal decisions\n\n| Finding | State | Decision |\n|---|---|---|\n| VDS-001 | `context_verified` | The provenance gap itself is verified: the official V1.0 publication exists, but no exact official V1.0 VideoDisplayService service XSD is confirmed in the checked official release route. V2.0 is explicitly not substituted. |\n| VDS-002 | `executable_confirmed` | Official V2.0 PDF describes a multi-field capability record; exact V2.0 XSD uses `xs:choice`. EV-103 confirms the executable boundary. |\n| VDS-003 | `executable_confirmed` | Official V2.0 PDF requires `ViewID + Timeout`; exact V2.0 XSD uses `xs:choice`. EV-103 confirms the executable boundary. |\n| VDS-004 | `executable_confirmed` | Official V2.0 response tables group related fields; exact V2.0 XSD response structures use `xs:choice`. EV-103 confirms the executable boundary. |\n| VDS-005 | `context_verified` | Broken generated cross references are visibly present in byte-pinned V1.0 and corrected/absent in V2.0. Documentation-only. |\n| VDS-006 | `context_verified` | Corrected finding only: the leading minus is valid VDV XML-choice notation. The surviving issue is the visually verified incomplete/degenerate application (`a`/`-1:1` without a visible peer alternative). The older invalid-cardinality interpretation is superseded and must not be reused. |\n| VDS-007 | `context_verified` | Cross-document `VideoDisplayService v1.1` reference label conflicts with the dedicated official VDS V1.0 identity. No V1.1 validation profile or schema alias is inferred. |\n| VDS-008 | `context_verified` | VDS expands RTP/SOA incorrectly; terminology was rechecked against RFC 3550 and the OASIS SOA Reference Model. No XML/XSD validation behavior changes. |\n\n## Authority boundaries\n\n- VDS V1.0 remains documentation authority only for this audit because the exact strict V1.0 service-XSD route remains unresolved.\n- VDS V2.0 executable conclusions use the exact official release-tag XSD family only.\n- `VDS-006` must always be read through the 2026-08-29 choice-notation correction overlay.\n- Documentation terminology/reference findings do not override XSD authority and do not create SDK rejection/acceptance rules.\n\n## Closure\n\nPrestate: **168 terminal / 24 pending**, first pending `VDS-001`.\n\nPoststate: **176 terminal / 16 pending**, first pending `VLS-001`. Next block: **VLS**.\n\nNo XSD, frozen inventory, PDF source registry, or PDF source-pin mutation is part of this closure.\n"""

    write_json(REGISTRY, registry)
    state = load(STATE)
    state["audit"] = audit
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")

    require(blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory unchanged after write")
    require(blob(SOURCE_REGISTRY) == EXPECTED_SOURCE_REGISTRY_BLOB, "PDF source registry unchanged after write")
    require(blob(SOURCE_PINS) == EXPECTED_SOURCE_PINS_BLOB, "PDF source pins unchanged after write")
    require(blob(VDS20) == EXPECTED_VDS20_BLOB and blob(COMMON20) == EXPECTED_COMMON20_BLOB and blob(ENUM20) == EXPECTED_ENUM20_BLOB, "selected V2.0 XSD authority unchanged after write")

    print("PASSED: VDS closure files prepared; expected poststate 176/16 -> VLS-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
