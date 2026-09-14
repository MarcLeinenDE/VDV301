#!/usr/bin/env python3
"""Fail-closed closure writer for frozen TrainSetInformationService finding TSI-001."""
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
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/TRAINSET_V2.1.md")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_TSI_2026-09-14.md")
VALIDATOR = Path("tools/validate_tsi_revalidation_ev161.py")
EV109 = Path("tools/validate_trainset_v21_ev109.py")
XSD_POOL = Path("tools/validate_xsd_pool.py")
TSI_V21 = Path("IBIS-IP_TrainSetInformationService_V2.1.xsd")
TSI_V22 = Path("IBIS-IP_TrainSetInformationService_V2.2.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_REGISTRY_PRE_BLOB = "a6105a349483a94998e83772b9eafe5d8aaf7089"
EXPECTED_STATE_PRE_BLOB = "7a42990e4e1d3dad9f19bcc92e77f203a25d12ac"
EXPECTED_SOURCE_REGISTRY_BLOB = "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8"
EXPECTED_SOURCE_PINS_BLOB = "88349638b423689799af700e8a1c8ec99bbfb67b"
EXPECTED_EVIDENCE_GATE_BLOB = "969cce8b14b50ded2ca5eb745674b894428ecf1a"
EXPECTED_ADDENDUM_BLOB = "8b1ac3db4c3603d04cca9001c82d7f4de6b5459e"
EXPECTED_DEEP_READ_BLOB = "6d5680f438e7e592aaf1d056e39224e7c2a3f2d9"
EXPECTED_VALIDATOR_BLOB = "a1c2f14af2fb73115c5c50397e6730395568bbb9"
EXPECTED_EV109_BLOB = "f88208bff7e39bb38a86a310dc121f486984f807"
EXPECTED_XSD_POOL_BLOB = "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd"
EXPECTED_TSI_V21_BLOB = "897f373e31b76aa23d8bc206854b042524e4c102"
EXPECTED_TSI_V22_BLOB = "7ab1f8f892bfcea2a8b8a055f07de92c143356f9"

PINNED_EV161_RUN = "34822675019"
PINNED_EV161_JOB = "103907586878"
PINNED_EV161_ARTIFACT = "10339022101"
PINNED_EV161_DIGEST = "sha256:705aa436963a49f4478099f884b63d19d14f02f79a18c3cde89603ecb31fced8"
PINNED_EV161_HEAD = "c6ee1be2ef346ab5ea61615f6d29de0ea24b06d8"

SOURCE_PIN_RUN = "34816735900"
SOURCE_PIN_JOB = "103888867262"
SOURCE_PIN_ARTIFACT = "10336466475"
SOURCE_PIN_DIGEST = "sha256:30089b9d4f2c86dd57f8bb184844a428ee08e91b0d327517c84f6689ea231bfb"
SOURCE_PIN_HEAD = "20785d8ee41e812a5902d49b6d4b800ef238e311"

PDF_SHA256 = "8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e"
PDF_SIZE = 1708401
PDF_PAGES = 51
PDF_URL = "https://www.vdv.de/vdv-301-2-14-v2-1-sds-trainsetservices.pdfx"

UPSTREAM = {
    "v2_1_commit": "585e0bea34b64887db4276f1c94d5f3e78f06c66",
    "v2_1_tree": "a8472530e840f7b365f6ba1075bfc09758ebda21",
    "v2_2_commit": "f283697124750d12189b960b302b399769bad530",
    "v2_2_tree": "2dbde53864ef07319016b419ff6951f6e90e79dc",
}

TARGETS = {"TSI-001": "executable_confirmed"}
TERMINAL_STATES = {
    "context_verified", "executable_confirmed", "contextual_not_defect",
    "withdrawn", "unresolved", "superseded",
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
        EVIDENCE_GATE: EXPECTED_EVIDENCE_GATE_BLOB,
        ADDENDUM: EXPECTED_ADDENDUM_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        VALIDATOR: EXPECTED_VALIDATOR_BLOB,
        EV109: EXPECTED_EV109_BLOB,
        XSD_POOL: EXPECTED_XSD_POOL_BLOB,
        TSI_V21: EXPECTED_TSI_V21_BLOB,
        TSI_V22: EXPECTED_TSI_V22_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file(), f"authority/prestate file exists: {path}")
        require(git_blob(path) == expected, f"exact prestate blob {path} = {expected}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen", "frozen inventory state unchanged")
    require(frozen.get("entry_count") == 192, "frozen inventory remains 192 entries")
    require("TSI-001" in frozen.get("finding_ids", []), "TSI-001 is a frozen inventory member")

    registry = load(REGISTRY)
    entries = registry.get("inventory", {}).get("entries", [])
    require(len(entries) == 192, "registry inventory remains 192 entries")
    require(registry.get("next_revalidation_block") == "TSI", "prestate next block is TSI")
    ids = [e.get("finding_id") for e in entries]
    require(len(ids) == len(set(ids)) == 192, "registry finding IDs remain unique")
    by_id = {e["finding_id"]: e for e in entries}
    require(by_id["TSI-001"].get("revalidation_state") == "pending", "TSI-001 is pending before closure")
    require(by_id["TSI-001"].get("terminal_state_source") is None, "TSI-001 has no premature terminal source")
    require(counts(entries) == (161, 31), f"pre-TSI counts are 161/31, got {counts(entries)}")
    require(first_pending(entries) == "TSI-001", f"pre-TSI first pending is TSI-001, got {first_pending(entries)}")
    require(by_id.get("TSM-001", {}).get("revalidation_state") == "pending", "TSM-001 remains pending before TSI closure")
    require(registry.get("revalidation_blocks", {}).get("TSD", {}).get("state") == "completed", "TSD is prior completed block")
    require("TSI" not in registry.get("revalidation_blocks", {}), "TSI block is not already closed")

    state = load(STATE)
    audit = state.get("audit")
    require(audit.get("finding_revalidation_completed_findings") == 161, "CURRENT_STATE pre-TSI terminal count is 161")
    require(audit.get("finding_revalidation_pending_findings") == 31, "CURRENT_STATE pre-TSI pending count is 31")
    require(audit.get("finding_revalidation_next_block") == "TSI", "CURRENT_STATE pre-TSI next block is TSI")
    require(audit.get("finding_revalidation_latest_completed_block") == "TSD", "TSD is prior CURRENT_STATE completed block")
    require(audit.get("latest_executable_evidence_id") == "EV-160", "EV-160 is prior executable evidence")

    by_id["TSI-001"]["revalidation_state"] = "executable_confirmed"
    by_id["TSI-001"]["terminal_state_source"] = str(REPORT)

    require(counts(entries) == (162, 30), f"post-TSI counts are 162/30, got {counts(entries)}")
    next_finding = first_pending(entries)
    require(next_finding == "TSM-001", f"post-TSI first pending is TSM-001, got {next_finding}")
    next_block = "TSM"

    registry["next_revalidation_block"] = next_block
    registry.setdefault("revalidation_blocks", {})["TSI"] = {
        "date": "2026-09-14",
        "state": "completed",
        "authority_lane": "official byte-pinned TrainSetServices V2.1 PDF plus exact VDV-301-2.1 XSD, V2.2 correction-history context and executable EV-109/EV-161 evidence",
        "evidence_id": "EV-161",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": PINNED_EV161_RUN,
        "pinned_successful_evidence_job": PINNED_EV161_JOB,
        "artifact_id": PINNED_EV161_ARTIFACT,
        "artifact_digest": PINNED_EV161_DIGEST,
        "evidence_head_sha": PINNED_EV161_HEAD,
        "source_pin": {
            "reused_from": "EV-160 source acquisition",
            "run_id": SOURCE_PIN_RUN,
            "job_id": SOURCE_PIN_JOB,
            "artifact_id": SOURCE_PIN_ARTIFACT,
            "artifact_digest": SOURCE_PIN_DIGEST,
            "head_sha": SOURCE_PIN_HEAD,
        },
        "pdf_authority": {
            "source_id": "TRAINSET_V2.1",
            "official_url": PDF_URL,
            "sha256": PDF_SHA256,
            "size_bytes": PDF_SIZE,
            "pages": PDF_PAGES,
            "visual_pages": [24, 25],
            "page_25_embedded_diagram_evidence_mode": "visual_not_Poppler_text",
        },
        "upstream_authority": UPSTREAM,
        "xsd_authority": {
            "v2_1_blob": EXPECTED_TSI_V21_BLOB,
            "v2_2_historical_correction_blob": EXPECTED_TSI_V22_BLOB,
            "latest_wins": False,
        },
        "underlying_executable_evidence": ["EV-109"],
        "full_xsd_regression_pool": {"root_xsd_count": 50, "result": "PASS"},
        "findings": TARGETS,
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": next_block,
        "next_finding": next_finding,
    }

    audit["finding_revalidation_next_block"] = next_block
    audit["finding_revalidation_completed_findings"] = 162
    audit["finding_revalidation_pending_findings"] = 30
    audit["finding_revalidation_current_block"] = "TSI"
    audit["finding_revalidation_latest_completed_block"] = "TSI"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_revalidation_evidence_id"] = "EV-161"
    audit["latest_executable_evidence_id"] = "EV-161"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["tsi_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-161",
        "run_id": run_id,
        "pinned_successful_evidence_run": PINNED_EV161_RUN,
        "pinned_successful_evidence_job": PINNED_EV161_JOB,
        "artifact_id": PINNED_EV161_ARTIFACT,
        "artifact_digest": PINNED_EV161_DIGEST,
        "source_pin_run": SOURCE_PIN_RUN,
        "source_pin_artifact": SOURCE_PIN_ARTIFACT,
        "terminal_states": TARGETS,
        "pdf_sha256": PDF_SHA256,
        "visual_pages": [24, 25],
        "underlying_evidence": ["EV-109"],
        "xsd_pool_result": "PASS_50_root_XSDs",
        "next_block": next_block,
        "next_finding": next_finding,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report = f"""# Finding revalidation — TrainSetInformationService (TSI)\n\nStatus: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen finding: `TSI-001`. Frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Aggregate evidence: **EV-161**; successful closure run **{run_id}**.\n- Independently successful EV-161 validation run: **{PINNED_EV161_RUN}**, job **{PINNED_EV161_JOB}**, artifact **{PINNED_EV161_ARTIFACT}**, digest `{PINNED_EV161_DIGEST}`.\n- Exact TrainSet V2.1 source reused from EV-160 source acquisition: run **{SOURCE_PIN_RUN}**, artifact **{SOURCE_PIN_ARTIFACT}**, digest `{SOURCE_PIN_DIGEST}`.\n- Official TrainSetServices V2.1 PDF: SHA-256 `{PDF_SHA256}`, {PDF_SIZE} bytes, {PDF_PAGES} pages. Physical page 24 defines the fields of a coach data set; physical page 25 says the response returns a sequence of coach data sets, one per coach. The embedded page-25 XSD diagram was treated as visual evidence because Poppler does not expose its labels reliably.\n- Exact official V2.1 TSI XSD blob `{EXPECTED_TSI_V21_BLOB}` models a single flat coach-field sequence with no repeated coach wrapper. EV-109 and EV-161 both prove one flat record validates and a second documented coach record is rejected.\n- V2.2 blob `{EXPECTED_TSI_V22_BLOB}` introduces `SingleCoach` with `maxOccurs=unbounded`; this is correction-history evidence only and is not back-applied to V2.1.\n- The complete **50-file root XSD pool** passed again and no XSD changed.\n\n## Terminal state\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n| `TSI-001` | `executable_confirmed` | Official V2.1 prose requires multiple coach data sets while exact V2.1 validation cannot represent more than one flat coach record. |\n\n## Mutation decision\n\n- XSD mutation: **none**.\n- Frozen inventory mutation: **none**.\n- PDF source registry/pin mutation: **none**.\n- Registry/status mutation: only `TSI-001` and the TSI block/counter handoff.\n\n## State transition\n\n- Before: **161/192 terminal**, **31 pending**, first pending `TSI-001`.\n- After: **162/192 terminal**, **30 pending**, first pending `{next_finding}`.\n- Next block: **{next_block}**.\n"""

    REPORT.write_text(report, encoding="utf-8")
    write_json(REGISTRY, registry)
    write_json(STATE, state)

    require(git_blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory bytes unchanged after writes")
    require(git_blob(SOURCE_REGISTRY) == EXPECTED_SOURCE_REGISTRY_BLOB, "PDF source registry unchanged after writes")
    require(git_blob(SOURCE_PINS) == EXPECTED_SOURCE_PINS_BLOB, "PDF source pin registry unchanged after writes")
    require(git_blob(TSI_V21) == EXPECTED_TSI_V21_BLOB, "TrainSetInformationService V2.1 XSD unchanged after writes")
    require(git_blob(TSI_V22) == EXPECTED_TSI_V22_BLOB, "TrainSetInformationService V2.2 XSD unchanged after writes")

    post_registry = load(REGISTRY)
    post_entries = post_registry["inventory"]["entries"]
    require(counts(post_entries) == (162, 30), "written registry counts are 162/30")
    require(first_pending(post_entries) == "TSM-001", "written registry first pending is TSM-001")
    require(post_registry.get("next_revalidation_block") == "TSM", "written registry next block is TSM")
    require(post_registry["revalidation_blocks"]["TSI"]["artifact_digest"] == PINNED_EV161_DIGEST, "written TSI block pins EV-161 artifact digest")

    post_audit = load(STATE)["audit"]
    require(post_audit.get("finding_revalidation_completed_findings") == 162, "written CURRENT_STATE terminal count is 162")
    require(post_audit.get("finding_revalidation_pending_findings") == 30, "written CURRENT_STATE pending count is 30")
    require(post_audit.get("finding_revalidation_next_block") == "TSM", "written CURRENT_STATE next block is TSM")
    require(post_audit.get("finding_revalidation_latest_completed_block") == "TSI", "written CURRENT_STATE latest block is TSI")
    require(REPORT.is_file(), "TSI revalidation report written")
    print("PASS TSI closure writer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
