#!/usr/bin/env python3
"""Fail-closed closure writer for frozen TrainSetDataService findings TSD-001..004."""
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
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_TSD_2026-09-14.md")
VALIDATOR = Path("tools/validate_tsd_revalidation_ev160.py")
EV109 = Path("tools/validate_trainset_v21_ev109.py")
EV110 = Path("tools/validate_trainset_tsd002_ev110.py")
EV104 = Path("tools/validate_trainset_ev104.py")
XSD_POOL = Path("tools/validate_xsd_pool.py")
TSD_V21 = Path("IBIS-IP_TrainSetDataService_V2.1.xsd")
TSD_V22 = Path("IBIS-IP_TrainSetDataService_V2.2.xsd")
COMMON_V22 = Path("IBIS-IP_common_V2.2.xsd")
ENUM_V22 = Path("IBIS-IP_Enumerations_V2.2.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_REGISTRY_PRE_BLOB = "1449e2c9fe1af2274c0d27f92927d8be74c8f54d"
EXPECTED_STATE_PRE_BLOB = "b30aebef7c89c62a351dbb6b6f756d8c9ceb30af"
EXPECTED_SOURCE_REGISTRY_BLOB = "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8"
EXPECTED_SOURCE_PINS_BLOB = "88349638b423689799af700e8a1c8ec99bbfb67b"
EXPECTED_EVIDENCE_GATE_BLOB = "969cce8b14b50ded2ca5eb745674b894428ecf1a"
EXPECTED_VALIDATOR_BLOB = "3d8cc6415517ecac7052739d3e9f456256704f19"
EXPECTED_EV109_BLOB = "f88208bff7e39bb38a86a310dc121f486984f807"
EXPECTED_EV110_BLOB = "34f16aec78b49af1210de6f4fd4e0ef674a21604"
EXPECTED_EV104_BLOB = "0d7bc30b56dd3e61771e0ac0ddd7c9f06a6b0d31"
EXPECTED_XSD_POOL_BLOB = "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd"
EXPECTED_TSD_V21_BLOB = "c2cdb73fcae265a2e4e0349ac6072e3548e36d8b"
EXPECTED_TSD_V22_BLOB = "7a132894c281d613e16514a6fa1bcbffe713d066"
EXPECTED_COMMON_V22_BLOB = "468fee6d177e7185dbcd5d3f90cfb114e29e01ae"
EXPECTED_ENUM_V22_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"

PINNED_EV160_RUN = "34820627306"
PINNED_EV160_JOB = "103901166925"
PINNED_EV160_ARTIFACT = "10337324977"
PINNED_EV160_DIGEST = "sha256:47c862255c57a90fddbe1948f92ca1ebc991e5c5f19d1f6cc78ae117ae77fbac"
PINNED_EV160_HEAD = "7140be15f49b6c633faf62977e5d9ff7ad1e60a4"

SOURCE_PIN_RUN = "34816735900"
SOURCE_PIN_JOB = "103888867262"
SOURCE_PIN_ARTIFACT = "10336466475"
SOURCE_PIN_DIGEST = "sha256:30089b9d4f2c86dd57f8bb184844a428ee08e91b0d327517c84f6689ea231bfb"
SOURCE_PIN_HEAD = "20785d8ee41e812a5902d49b6d4b800ef238e311"

UPSTREAM = {
    "v2_1_commit": "585e0bea34b64887db4276f1c94d5f3e78f06c66",
    "v2_1_tree": "a8472530e840f7b365f6ba1075bfc09758ebda21",
    "v2_2_commit": "f283697124750d12189b960b302b399769bad530",
    "v2_2_tree": "2dbde53864ef07319016b419ff6951f6e90e79dc",
    "v2_1_tsd_blob": EXPECTED_TSD_V21_BLOB,
    "v2_2_tsd_blob": EXPECTED_TSD_V22_BLOB,
    "v2_2_common_blob": EXPECTED_COMMON_V22_BLOB,
    "v2_2_enumerations_blob": EXPECTED_ENUM_V22_BLOB,
}

PDFS = {
    "TRAINSET_V2.1": {
        "url": "https://www.vdv.de/vdv-301-2-14-v2-1-sds-trainsetservices.pdfx",
        "sha256": "8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e",
        "size_bytes": 1708401,
        "pages": 51,
        "visual_pages": [33, 34],
    },
    "TRAINSET_V2.2": {
        "url": "https://www.vdv.de/301-2-14-sdes-v2-2-trainsetservices.pdfx",
        "sha256": "c1946694a1809933a9a4a23adff1c551effdb0a2fbc6a7f7f68faec0b0c7bd6e",
        "size_bytes": 1744296,
        "pages": 54,
        "visual_pages": [34, 35, 38, 40],
    },
    "VDV301-2_GC_V2.2": {
        "url": "https://www.vdv.de/301-2-sdes-v2-2-common-conventions.pdfx",
        "sha256": "96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051",
        "size_bytes": 1562305,
        "pages": 79,
        "visual_pages": [47, 48, 49],
    },
}

TARGETS = {
    "TSD-001": "executable_confirmed",
    "TSD-002": "executable_confirmed",
    "TSD-003": "contextual_not_defect",
    "TSD-004": "context_verified",
}

RATIONALES = {
    "TSD-001": "The byte-pinned V2.1 writing specifies Retrieve/Subscribe/Unsubscribe for the TrainSetDataService while the exact official V2.1 XSD exposes only the service-specific Retrieve roots/operation members. EV-109 and EV-160 reconfirm that boundary together with the generic Common subscription structures.",
    "TSD-002": "The byte-pinned V2.2 operation overview assigns Retrieve*RequestStructure names to UnsubscribeTripRef and UnsubscribeTripInformation, but the detailed definition and exact official XSD use TrainSetUnsubscribeRequestStructure. EV-110 and EV-160 executable checks reconfirm the accepted/rejected shapes.",
    "TSD-003": "The exact V2.2 XSD intentionally uses SubscribeResponseStructure for the immediate operation acknowledgement and the corresponding Retrieve response structures for later event payload roots. General Conventions V2.2 provides the generic Get/Subscribe/Retrieve context; TrainSetDataService explicitly extends the concept for parameter-related Retrieve operations. EV-104 and EV-160 therefore support contextual_not_defect.",
    "TSD-004": "The byte-pinned V2.2 writing on physical page 40 incorrectly names RetrieveTripRefResponseStructure for SubscribeTripInformation event updates. The exact official XSD uses RetrieveTripInformationResponseStructure, while the TripRef parallel on page 38 and in the XSD is internally consistent. This is a documentation reference error.",
}

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
        VALIDATOR: EXPECTED_VALIDATOR_BLOB,
        EV109: EXPECTED_EV109_BLOB,
        EV110: EXPECTED_EV110_BLOB,
        EV104: EXPECTED_EV104_BLOB,
        XSD_POOL: EXPECTED_XSD_POOL_BLOB,
        TSD_V21: EXPECTED_TSD_V21_BLOB,
        TSD_V22: EXPECTED_TSD_V22_BLOB,
        COMMON_V22: EXPECTED_COMMON_V22_BLOB,
        ENUM_V22: EXPECTED_ENUM_V22_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file(), f"authority/prestate file exists: {path}")
        require(git_blob(path) == expected, f"exact prestate blob {path} = {expected}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen", "frozen inventory state unchanged")
    require(frozen.get("entry_count") == 192, "frozen inventory remains 192 entries")
    frozen_ids = frozen.get("finding_ids", [])
    require(all(fid in frozen_ids for fid in TARGETS), "all four TSD targets are frozen inventory members")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen", "registry inventory remains frozen")
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory remains 192 entries")
    require(registry.get("next_revalidation_block") == "TSD", "prestate next block is TSD")
    ids = [e.get("finding_id") for e in entries]
    require(len(ids) == len(set(ids)) == 192, "registry finding IDs remain unique")
    by_id = {e["finding_id"]: e for e in entries}
    for fid in TARGETS:
        require(by_id[fid].get("revalidation_state") == "pending", f"{fid} is pending before closure")
        require(by_id[fid].get("terminal_state_source") is None, f"{fid} has no premature terminal source")
    require(counts(entries) == (157, 35), f"pre-TSD counts are 157/35, got {counts(entries)}")
    require(first_pending(entries) == "TSD-001", f"pre-TSD first pending is TSD-001, got {first_pending(entries)}")
    require(by_id.get("TSI-001", {}).get("revalidation_state") == "pending", "TSI-001 remains pending before TSD closure")
    require(registry.get("revalidation_blocks", {}).get("TS", {}).get("state") == "completed", "TS is prior completed block")
    require("TSD" not in registry.get("revalidation_blocks", {}), "TSD block is not already closed")

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit exists")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE inventory count remains 192")
    require(audit.get("finding_revalidation_completed_findings") == 157, "CURRENT_STATE pre-TSD terminal count is 157")
    require(audit.get("finding_revalidation_pending_findings") == 35, "CURRENT_STATE pre-TSD pending count is 35")
    require(audit.get("finding_revalidation_next_block") == "TSD", "CURRENT_STATE pre-TSD next block is TSD")
    require(audit.get("finding_revalidation_latest_completed_block") == "TS", "TS is prior CURRENT_STATE completed block")
    require(audit.get("latest_executable_evidence_id") == "EV-159", "EV-159 is prior executable evidence")

    for fid, terminal_state in TARGETS.items():
        by_id[fid]["revalidation_state"] = terminal_state
        by_id[fid]["terminal_state_source"] = str(REPORT)

    require(counts(entries) == (161, 31), f"post-TSD counts are 161/31, got {counts(entries)}")
    next_finding = first_pending(entries)
    require(next_finding == "TSI-001", f"post-TSD first pending is TSI-001, got {next_finding}")
    next_block = next_finding.split("-", 1)[0] if next_finding else None
    require(next_block == "TSI", f"post-TSD next block is TSI, got {next_block}")

    blocks = registry.setdefault("revalidation_blocks", {})
    registry["next_revalidation_block"] = next_block
    blocks["TSD"] = {
        "date": "2026-09-14",
        "state": "completed",
        "authority_lane": "official byte-pinned TrainSetServices V2.1/V2.2 PDFs plus exact VDV-301-2.1/2.2 release trees, General Conventions V2.2 context and executable EV-109/EV-110/EV-104 regression evidence",
        "evidence_id": "EV-160",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": PINNED_EV160_RUN,
        "pinned_successful_evidence_job": PINNED_EV160_JOB,
        "artifact_id": PINNED_EV160_ARTIFACT,
        "artifact_digest": PINNED_EV160_DIGEST,
        "evidence_head_sha": PINNED_EV160_HEAD,
        "source_pin": {
            "run_id": SOURCE_PIN_RUN,
            "job_id": SOURCE_PIN_JOB,
            "artifact_id": SOURCE_PIN_ARTIFACT,
            "artifact_digest": SOURCE_PIN_DIGEST,
            "head_sha": SOURCE_PIN_HEAD,
        },
        "pdf_authority": PDFS,
        "upstream_authority": UPSTREAM,
        "underlying_executable_evidence": ["EV-109", "EV-110", "EV-104"],
        "full_xsd_regression_pool": {"root_xsd_count": 50, "result": "PASS"},
        "findings": TARGETS,
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": next_block,
        "next_finding": next_finding,
    }

    audit["finding_revalidation_next_block"] = next_block
    audit["finding_revalidation_completed_findings"] = 161
    audit["finding_revalidation_pending_findings"] = 31
    audit["finding_revalidation_current_block"] = "TSD"
    audit["finding_revalidation_latest_completed_block"] = "TSD"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_revalidation_evidence_id"] = "EV-160"
    audit["latest_executable_evidence_id"] = "EV-160"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["tsd_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-160",
        "run_id": run_id,
        "pinned_successful_evidence_run": PINNED_EV160_RUN,
        "pinned_successful_evidence_job": PINNED_EV160_JOB,
        "artifact_id": PINNED_EV160_ARTIFACT,
        "artifact_digest": PINNED_EV160_DIGEST,
        "source_pin_run": SOURCE_PIN_RUN,
        "source_pin_artifact": SOURCE_PIN_ARTIFACT,
        "terminal_states": TARGETS,
        "trainset_v2_1_pdf_sha256": PDFS["TRAINSET_V2.1"]["sha256"],
        "trainset_v2_2_pdf_sha256": PDFS["TRAINSET_V2.2"]["sha256"],
        "general_conventions_v2_2_pdf_sha256": PDFS["VDV301-2_GC_V2.2"]["sha256"],
        "underlying_evidence": ["EV-109", "EV-110", "EV-104"],
        "xsd_pool_result": "PASS_50_root_XSDs",
        "next_block": next_block,
        "next_finding": next_finding,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    rows = "\n".join(f"| `{fid}` | `{TARGETS[fid]}` | {RATIONALES[fid]} |" for fid in TARGETS)
    report = f"""# Finding revalidation — TrainSetDataService (TSD)\n\nStatus: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen findings: `TSD-001` through `TSD-004`. Frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Aggregate evidence: **EV-160**; successful closure run **{run_id}**.\n- Independently successful EV-160 validation run: **{PINNED_EV160_RUN}**, job **{PINNED_EV160_JOB}**, artifact **{PINNED_EV160_ARTIFACT}**, digest `{PINNED_EV160_DIGEST}`.\n- EV-160 source-acquisition run: **{SOURCE_PIN_RUN}**, job **{SOURCE_PIN_JOB}**, artifact **{SOURCE_PIN_ARTIFACT}**, digest `{SOURCE_PIN_DIGEST}`.\n- Official TrainSetServices V2.1 PDF: SHA-256 `{PDFS['TRAINSET_V2.1']['sha256']}`, {PDFS['TRAINSET_V2.1']['size_bytes']} bytes, {PDFS['TRAINSET_V2.1']['pages']} pages; targeted physical pages 33–34.\n- Official TrainSetServices V2.2 PDF: SHA-256 `{PDFS['TRAINSET_V2.2']['sha256']}`, {PDFS['TRAINSET_V2.2']['size_bytes']} bytes, {PDFS['TRAINSET_V2.2']['pages']} pages; targeted physical pages 34, 35, 38 and 40.\n- Official General Conventions V2.2 PDF: SHA-256 `{PDFS['VDV301-2_GC_V2.2']['sha256']}`, {PDFS['VDV301-2_GC_V2.2']['size_bytes']} bytes, {PDFS['VDV301-2_GC_V2.2']['pages']} pages; targeted physical pages 47–49 for generic Get/Subscribe/Retrieve context.\n- Exact official VDV-301-2.1 commit `{UPSTREAM['v2_1_commit']}` / tree `{UPSTREAM['v2_1_tree']}` and VDV-301-2.2 commit `{UPSTREAM['v2_2_commit']}` / tree `{UPSTREAM['v2_2_tree']}` were fetched and compiled.\n- Historical executable controls **EV-109**, **EV-110** and **EV-104** were rerun successfully before EV-160 closure.\n- The complete **50-file root XSD pool** was recompiled and byte-hashed before/after EV-160; no XSD changed.\n\n## Terminal states\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n{rows}\n\n## Mutation decision\n\n- XSD mutation: **none**.\n- Frozen inventory mutation: **none**.\n- PDF source registry/pin mutation: **none**.\n- Registry/status mutation: only `TSD-001`…`TSD-004` and the TSD block/counter handoff.\n\n## State transition\n\n- Before: **157/192 terminal**, **35 pending**, first pending `TSD-001`.\n- After: **161/192 terminal**, **31 pending**, first pending `{next_finding}`.\n- Next block: **{next_block}**.\n"""

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")
    write_json(REGISTRY, registry)
    write_json(STATE, state)

    require(load(FROZEN).get("entry_count") == 192, "frozen inventory still 192 after writes")
    require(git_blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory bytes unchanged after writes")
    require(git_blob(SOURCE_REGISTRY) == EXPECTED_SOURCE_REGISTRY_BLOB, "PDF source registry unchanged after writes")
    require(git_blob(SOURCE_PINS) == EXPECTED_SOURCE_PINS_BLOB, "PDF source pin registry unchanged after writes")
    require(git_blob(TSD_V21) == EXPECTED_TSD_V21_BLOB, "TrainSetDataService V2.1 XSD unchanged after writes")
    require(git_blob(TSD_V22) == EXPECTED_TSD_V22_BLOB, "TrainSetDataService V2.2 XSD unchanged after writes")

    post_registry = load(REGISTRY)
    post_entries = post_registry["inventory"]["entries"]
    require(counts(post_entries) == (161, 31), "written registry counts are 161/31")
    require(first_pending(post_entries) == "TSI-001", "written registry first pending is TSI-001")
    require(post_registry.get("next_revalidation_block") == "TSI", "written registry next block is TSI")
    require(post_registry["revalidation_blocks"]["TSD"]["artifact_digest"] == PINNED_EV160_DIGEST, "written TSD block pins EV-160 artifact digest")

    post_audit = load(STATE)["audit"]
    require(post_audit.get("finding_revalidation_completed_findings") == 161, "written CURRENT_STATE terminal count is 161")
    require(post_audit.get("finding_revalidation_pending_findings") == 31, "written CURRENT_STATE pending count is 31")
    require(post_audit.get("finding_revalidation_next_block") == "TSI", "written CURRENT_STATE next block is TSI")
    require(post_audit.get("finding_revalidation_latest_completed_block") == "TSD", "written CURRENT_STATE latest block is TSD")
    require(REPORT.is_file(), "TSD revalidation report written")
    print("PASS TSD closure writer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
