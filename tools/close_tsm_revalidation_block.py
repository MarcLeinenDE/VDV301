#!/usr/bin/env python3
"""Fail-closed closure writer for frozen TrainSetManagementService findings TSM-001..003."""
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
ADDENDUM = Path("docs/pdf_xsd_semantic_audit/TRAIN_SET_SERVICES_FINDINGS_REGISTER_ADDENDUM.md")
DEEP21 = Path("docs/pdf_xsd_semantic_audit/deep_read/TRAINSET_V2.1.md")
DEEP22 = Path("docs/pdf_xsd_semantic_audit/deep_read/TRAINSET_V2.2.md")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_TSM_2026-09-14.md")
VALIDATOR = Path("tools/validate_tsm_revalidation_ev162.py")
EV109 = Path("tools/validate_trainset_v21_ev109.py")
EV104 = Path("tools/validate_trainset_ev104.py")
XSD_POOL = Path("tools/validate_xsd_pool.py")
TSM21 = Path("IBIS-IP_TrainSetManagementService_V2.1.xsd")
TSM22 = Path("IBIS-IP_TrainSetManagementService_V2.2.xsd")
TSI22 = Path("IBIS-IP_TrainSetInformationService_V2.2.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_REGISTRY_PRE_BLOB = "84f4b647c2910c27550bdd8f62d7c072d56714ba"
EXPECTED_STATE_PRE_BLOB = "efa00ed4ffc2fad76f50b000377ef1f8def0d486"
EXPECTED_SOURCE_REGISTRY_BLOB = "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8"
EXPECTED_SOURCE_PINS_BLOB = "88349638b423689799af700e8a1c8ec99bbfb67b"
EXPECTED_EVIDENCE_GATE_BLOB = "969cce8b14b50ded2ca5eb745674b894428ecf1a"
EXPECTED_ADDENDUM_BLOB = "8b1ac3db4c3603d04cca9001c82d7f4de6b5459e"
EXPECTED_DEEP21_BLOB = "6d5680f438e7e592aaf1d056e39224e7c2a3f2d9"
EXPECTED_DEEP22_BLOB = "61850045c26fb2a848c4670f1418fdb809ab475c"
EXPECTED_VALIDATOR_BLOB = "141ac346548cee5f00dee34b356df5262e098178"
EXPECTED_EV109_BLOB = "f88208bff7e39bb38a86a310dc121f486984f807"
EXPECTED_EV104_BLOB = "0d7bc30b56dd3e61771e0ac0ddd7c9f06a6b0d31"
EXPECTED_XSD_POOL_BLOB = "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd"
EXPECTED_TSM21_BLOB = "add9d1cb37e5759ff7a77855b239108d38373206"
EXPECTED_TSM22_BLOB = "da9465d6683e3f7d54a546ab4a13739fb3c3e902"
EXPECTED_TSI22_BLOB = "7ab1f8f892bfcea2a8b8a055f07de92c143356f9"

PINNED_EV162_RUN = "34823353897"
PINNED_EV162_JOB = "103909732702"
PINNED_EV162_ARTIFACT = "10339282538"
PINNED_EV162_DIGEST = "sha256:8083d5badea1af9922302b202f06c33f4961d53878dfbc5d84324a4e4d65a4a0"
PINNED_EV162_HEAD = "41a491ad41b1f03a786610f64fc54979a38faf4f"

SOURCE_PIN_RUN = "34816735900"
SOURCE_PIN_JOB = "103888867262"
SOURCE_PIN_ARTIFACT = "10336466475"
SOURCE_PIN_DIGEST = "sha256:30089b9d4f2c86dd57f8bb184844a428ee08e91b0d327517c84f6689ea231bfb"
SOURCE_PIN_HEAD = "20785d8ee41e812a5902d49b6d4b800ef238e311"

PDF_V21_SHA = "8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e"
PDF_V22_SHA = "c1946694a1809933a9a4a23adff1c551effdb0a2fbc6a7f7f68faec0b0c7bd6e"
TARGETS = {
    "TSM-001": "executable_confirmed",
    "TSM-002": "executable_confirmed",
    "TSM-003": "context_verified",
}
TERMINAL = {"context_verified","executable_confirmed","contextual_not_defect","withdrawn","unresolved","superseded"}


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
    return subprocess.check_output(["git","hash-object",str(path)], text=True).strip()


def counts(entries: list[dict]) -> tuple[int,int]:
    return (sum(x.get("revalidation_state") in TERMINAL for x in entries), sum(x.get("revalidation_state") == "pending" for x in entries))


def first_pending(entries: list[dict]) -> str | None:
    return next((x.get("finding_id") for x in entries if x.get("revalidation_state") == "pending"), None)


def main() -> int:
    run_id = os.environ.get("EVIDENCE_RUN_ID", "").strip()
    run_url = os.environ.get("EVIDENCE_RUN_URL", "").strip()
    require(run_id.isdigit(), "EVIDENCE_RUN_ID is numeric")
    require(run_url == f"https://github.com/MarcLeinenDE/VDV301/actions/runs/{run_id}", "EVIDENCE_RUN_URL matches run id")

    immutable = {
        FROZEN: EXPECTED_FROZEN_BLOB, REGISTRY: EXPECTED_REGISTRY_PRE_BLOB, STATE: EXPECTED_STATE_PRE_BLOB,
        SOURCE_REGISTRY: EXPECTED_SOURCE_REGISTRY_BLOB, SOURCE_PINS: EXPECTED_SOURCE_PINS_BLOB,
        EVIDENCE_GATE: EXPECTED_EVIDENCE_GATE_BLOB, ADDENDUM: EXPECTED_ADDENDUM_BLOB,
        DEEP21: EXPECTED_DEEP21_BLOB, DEEP22: EXPECTED_DEEP22_BLOB, VALIDATOR: EXPECTED_VALIDATOR_BLOB,
        EV109: EXPECTED_EV109_BLOB, EV104: EXPECTED_EV104_BLOB, XSD_POOL: EXPECTED_XSD_POOL_BLOB,
        TSM21: EXPECTED_TSM21_BLOB, TSM22: EXPECTED_TSM22_BLOB, TSI22: EXPECTED_TSI22_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file() and blob(path) == expected, f"exact prestate/authority blob {path} = {expected}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory remains exactly 192")
    require(all(fid in frozen.get("finding_ids", []) for fid in TARGETS), "all TSM targets are frozen inventory members")

    registry = load(REGISTRY)
    entries = registry["inventory"]["entries"]
    ids = [x["finding_id"] for x in entries]
    require(len(ids) == len(set(ids)) == 192, "registry contains exactly 192 unique findings")
    require(registry.get("next_revalidation_block") == "TSM", "prestate next block is TSM")
    require(counts(entries) == (162,30), f"pre-TSM counts are 162/30, got {counts(entries)}")
    require(first_pending(entries) == "TSM-001", "pre-TSM first pending is TSM-001")
    by_id = {x["finding_id"]: x for x in entries}
    for fid in TARGETS:
        require(by_id[fid].get("revalidation_state") == "pending" and by_id[fid].get("terminal_state_source") is None, f"{fid} is pending without premature source")
    require(by_id["TVS-001"].get("revalidation_state") == "pending", "TVS-001 remains pending before TSM closure")
    require(registry.get("revalidation_blocks", {}).get("TSI", {}).get("state") == "completed", "TSI is prior completed block")
    require("TSM" not in registry.get("revalidation_blocks", {}), "TSM block is not already closed")

    audit = load(STATE)["audit"]
    require(audit.get("finding_revalidation_completed_findings") == 162, "CURRENT_STATE pre-TSM terminal count is 162")
    require(audit.get("finding_revalidation_pending_findings") == 30, "CURRENT_STATE pre-TSM pending count is 30")
    require(audit.get("finding_revalidation_next_block") == "TSM", "CURRENT_STATE pre-TSM next block is TSM")
    require(audit.get("finding_revalidation_latest_completed_block") == "TSI", "TSI is prior CURRENT_STATE completed block")
    require(audit.get("latest_executable_evidence_id") == "EV-161", "EV-161 is prior executable evidence")

    for fid, terminal_state in TARGETS.items():
        by_id[fid]["revalidation_state"] = terminal_state
        by_id[fid]["terminal_state_source"] = str(REPORT)

    require(counts(entries) == (165,27), f"post-TSM counts are 165/27, got {counts(entries)}")
    next_finding = first_pending(entries)
    require(next_finding == "TVS-001", f"post-TSM first pending is TVS-001, got {next_finding}")

    registry["next_revalidation_block"] = "TVS"
    registry.setdefault("revalidation_blocks", {})["TSM"] = {
        "date": "2026-09-14", "state": "completed",
        "authority_lane": "official byte-pinned TrainSetServices V2.1/V2.2 PDFs plus exact official V2.1/V2.2 TrainSetManagementService XSDs, V2.2 correction history, EV-109/EV-104 and EV-162",
        "evidence_id": "EV-162", "evidence_run_id": run_id, "evidence_run_url": run_url,
        "pinned_successful_evidence_run": PINNED_EV162_RUN, "pinned_successful_evidence_job": PINNED_EV162_JOB,
        "artifact_id": PINNED_EV162_ARTIFACT, "artifact_digest": PINNED_EV162_DIGEST, "evidence_head_sha": PINNED_EV162_HEAD,
        "source_pin": {"reused_from":"EV-160 source acquisition","run_id":SOURCE_PIN_RUN,"job_id":SOURCE_PIN_JOB,"artifact_id":SOURCE_PIN_ARTIFACT,"artifact_digest":SOURCE_PIN_DIGEST,"head_sha":SOURCE_PIN_HEAD},
        "pdf_authority": {
            "TRAINSET_V2.1": {"sha256":PDF_V21_SHA,"visual_pages":[30]},
            "TRAINSET_V2.2": {"sha256":PDF_V22_SHA,"visual_pages":[31,51],"page_31_embedded_diagram_evidence_mode":"visual_not_Poppler_text"},
        },
        "xsd_authority": {"TSM_V2.1_blob":EXPECTED_TSM21_BLOB,"TSM_V2.2_blob":EXPECTED_TSM22_BLOB,"TSI_V2.2_blob":EXPECTED_TSI22_BLOB,"latest_wins":False},
        "underlying_executable_evidence": ["EV-109","EV-104"],
        "full_xsd_regression_pool": {"root_xsd_count":50,"result":"PASS"},
        "findings": TARGETS, "terminal_state_source": str(REPORT),
        "xsd_mutation": False, "frozen_inventory_mutation": False, "next_block":"TVS", "next_finding":next_finding,
    }

    audit["finding_revalidation_next_block"] = "TVS"
    audit["finding_revalidation_completed_findings"] = 165
    audit["finding_revalidation_pending_findings"] = 27
    audit["finding_revalidation_current_block"] = "TSM"
    audit["finding_revalidation_latest_completed_block"] = "TSM"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_revalidation_evidence_id"] = "EV-162"
    audit["latest_executable_evidence_id"] = "EV-162"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["tsm_revalidation"] = {
        "status":"complete","completed_at_run":run_id,"evidence_id":"EV-162","run_id":run_id,
        "pinned_successful_evidence_run":PINNED_EV162_RUN,"pinned_successful_evidence_job":PINNED_EV162_JOB,
        "artifact_id":PINNED_EV162_ARTIFACT,"artifact_digest":PINNED_EV162_DIGEST,
        "source_pin_run":SOURCE_PIN_RUN,"source_pin_artifact":SOURCE_PIN_ARTIFACT,"terminal_states":TARGETS,
        "underlying_evidence":["EV-109","EV-104"],"xsd_pool_result":"PASS_50_root_XSDs",
        "next_block":"TVS","next_finding":next_finding,"xsd_mutation":False,"frozen_inventory_mutation":False,
    }

    report = f"""# Finding revalidation — TrainSetManagementService (TSM)\n\nStatus: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen findings: `TSM-001` through `TSM-003`. Frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Aggregate evidence: **EV-162**; successful closure run **{run_id}**.\n- Successful EV-162 validation run: **{PINNED_EV162_RUN}**, job **{PINNED_EV162_JOB}**, artifact **{PINNED_EV162_ARTIFACT}**, digest `{PINNED_EV162_DIGEST}`.\n- Exact TrainSet V2.1/V2.2 PDFs reused from the EV-160 source lane and re-acquired during validation.\n- V2.1 physical page 30 and exact V2.1 XSD show `TrainSetManagementService.GetTrainSetComposition`; EV-109 executable-confirms that the later corrected `...Response` root is not valid in V2.1.\n- V2.2 physical page 51 explicitly records the correction to `TrainSetManagementService.GetTrainSetCompositionResponse`. The exact V2.2 global root is corrected, but the `TrainSetManagementServiceOperations` group still contains the stale old name; EV-104 executable-confirms this mismatch.\n- V2.2 physical page 31 uses the corrected global name but its embedded XSD diagram visibly expands the old flat coach fields. The exact V2.2 reused response structure instead has repeatable `SingleCoach -> SingleCoachInATrainSet`; this is documentation-only and does not change XSD authority.\n- Complete **50-root-XSD pool** passed again; no schema mutation.\n\n## Terminal states\n\n| Finding | Terminal state | Result |\n|---|---|---|\n| `TSM-001` | `executable_confirmed` | Historical V2.1 response-root naming discrepancy confirmed by exact XSD behaviour and V2.2 correction history. |\n| `TSM-002` | `executable_confirmed` | V2.2 corrected global root conflicts with stale operation-group member; EV-104 confirms validation behaviour. |\n| `TSM-003` | `context_verified` | V2.2 page-31 embedded diagram remains stale relative to the exact repeated `SingleCoach` structure. |\n\n## Mutation decision\n\n- XSD mutation: **none**.\n- Frozen inventory mutation: **none**.\n- PDF source registry/pin mutation: **none**.\n- Registry/status mutation: only `TSM-001`…`TSM-003` and the TSM block/counter handoff.\n\n## State transition\n\n- Before: **162/192 terminal**, **30 pending**, first pending `TSM-001`.\n- After: **165/192 terminal**, **27 pending**, first pending `{next_finding}`.\n- Next block: **TVS**.\n"""

    REPORT.write_text(report, encoding="utf-8")
    write_json(REGISTRY, registry)
    state = load(STATE)
    state["audit"] = audit
    write_json(STATE, state)

    require(blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory unchanged after writes")
    require(blob(SOURCE_REGISTRY) == EXPECTED_SOURCE_REGISTRY_BLOB and blob(SOURCE_PINS) == EXPECTED_SOURCE_PINS_BLOB, "PDF source registries unchanged after writes")
    require(blob(TSM21) == EXPECTED_TSM21_BLOB and blob(TSM22) == EXPECTED_TSM22_BLOB and blob(TSI22) == EXPECTED_TSI22_BLOB, "TrainSet XSD authority files unchanged after writes")
    post = load(REGISTRY)
    require(counts(post["inventory"]["entries"]) == (165,27), "written registry counts are 165/27")
    require(first_pending(post["inventory"]["entries"]) == "TVS-001" and post["next_revalidation_block"] == "TVS", "written registry handoff is TVS-001/TVS")
    require(post["revalidation_blocks"]["TSM"]["artifact_digest"] == PINNED_EV162_DIGEST, "written TSM block pins EV-162 artifact digest")
    post_audit = load(STATE)["audit"]
    require(post_audit["finding_revalidation_completed_findings"] == 165 and post_audit["finding_revalidation_pending_findings"] == 27, "written CURRENT_STATE counts are 165/27")
    require(post_audit["finding_revalidation_next_block"] == "TVS" and post_audit["finding_revalidation_latest_completed_block"] == "TSM", "written CURRENT_STATE handoff is TSM -> TVS")
    require(REPORT.is_file(), "TSM revalidation report written")
    print("PASS TSM closure writer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
