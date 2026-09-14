#!/usr/bin/env python3
"""Fail-closed closure writer for frozen TimeService findings TS-001..002."""
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
ADDENDUM = Path("docs/pdf_xsd_semantic_audit/TIME_SERVICE_FINDINGS_REGISTER_ADDENDUM.md")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/TIME_V1.0.md")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_TS_2026-09-14.md")
VALIDATOR = Path("tools/validate_ts_revalidation_ev159.py")
XSD_POOL = Path("tools/validate_xsd_pool.py")
RUNTIME_PROFILE = Path("tools/runtime_time_profile.py")
RUNTIME_VALIDATOR = Path("tools/validate_time_runtime_rv003.py")
ENUM_V10 = Path("IBIS-IP_Enumerations_V1.0.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_REGISTRY_PRE_BLOB = "0a4bfcb5d895f25381afd56c32fe5c7d349e4de0"
EXPECTED_STATE_PRE_BLOB = "f3c248261066c3760ac093e73c6bfaca484c67c1"
EXPECTED_SOURCE_REGISTRY_BLOB = "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8"
EXPECTED_SOURCE_PINS_BLOB = "88349638b423689799af700e8a1c8ec99bbfb67b"
EXPECTED_EVIDENCE_GATE_BLOB = "969cce8b14b50ded2ca5eb745674b894428ecf1a"
EXPECTED_ADDENDUM_BLOB = "23723fbb6bb99ffa3aa1eb8c13feae6aa95a0170"
EXPECTED_DEEP_READ_BLOB = "82a88fbd6dae5d22f472bf144770d915fcc902ea"
EXPECTED_VALIDATOR_BLOB = "3d51e97e2127d0d44e45ade9ed9138dd9ac59a07"
EXPECTED_XSD_POOL_BLOB = "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd"
EXPECTED_RUNTIME_PROFILE_BLOB = "acd28ca0bd6ac1917b3d2db29745555b7e17d8dd"
EXPECTED_RUNTIME_VALIDATOR_BLOB = "ff6e3fcd35d4c2f6bff760b3e86f5adb0e72156c"
EXPECTED_ENUM_V10_BLOB = "a9bea5bc73003ed91ded8519db06c32c4067831d"

PDF_URL = "https://www.vdv.de/301-2-10sds-v-1-01.pdfx"
PDF_SHA256 = "d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3"
PDF_SIZE = 515920
PDF_PAGES = 10

SOURCE_PIN_RUN = "34814542791"
SOURCE_PIN_JOB = "103882386972"
SOURCE_PIN_ARTIFACT = "10336172299"
SOURCE_PIN_DIGEST = "sha256:c24cfc7d8b80652a5caaeafa4d131f31c32fcbe85e45cfb4a6bb5edb2f789c94"
SOURCE_PIN_HEAD = "bd158b2a6121a3f7e4612acca5607875ab7ab852"

PINNED_EV159_RUN = "34815684895"
PINNED_EV159_JOB = "103885751905"
PINNED_EV159_ARTIFACT = "10336194085"
PINNED_EV159_DIGEST = "sha256:4d5c36f36c468b92e1a3ca962eb1e76b8670f6460f2ecf667bd1cdc2c2e2d010"
PINNED_EV159_HEAD = "8257c23dfa55e1ba3a425f8860d54913941c79ae"

UPSTREAM = {
    "v1_0_commit": "f5b53785f703e898632603eec3bfa3555a79fdba",
    "v1_0_tree": "729bbe3270e52fed3e0641466048a745d5a09b32",
    "v2_0_commit": "f2569a91f0a7c737a0ca7c0280b28ad223d7ee08",
    "v2_0_tree": "11daf0ebb3b26745c036ee19a547ad16d39f922c",
    "enum_v1_blob": EXPECTED_ENUM_V10_BLOB,
    "dedicated_time_service_xsd": False,
}

TARGETS = {
    "TS-001": "contextual_not_defect",
    "TS-002": "context_verified",
}

RATIONALES = {
    "TS-001": "TimeService V1.0 is a protocol/discovery profile by design, not an XML/XSD service. Exact VDV-301-1.0 and VDV-301-2.0 release trees plus the 50-root integration pool contain no dedicated TimeService XSD; ServiceNameEnumeration still exposes TimeService, and RV-003 executes the SNTP/DNS-SD profile including the no-cyclic and no-XML guards.",
    "TS-002": "The exact byte-pinned official TimeService writing visibly contains the bilingual foreword contradiction on physical page 4: the German text identifies VDV 301-2-10 while the English text says VDV 301-2-1. This is a documentation reference error, not a schema defect.",
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
        EVIDENCE_GATE: EXPECTED_EVIDENCE_GATE_BLOB,
        ADDENDUM: EXPECTED_ADDENDUM_BLOB,
        DEEP_READ: EXPECTED_DEEP_READ_BLOB,
        VALIDATOR: EXPECTED_VALIDATOR_BLOB,
        XSD_POOL: EXPECTED_XSD_POOL_BLOB,
        RUNTIME_PROFILE: EXPECTED_RUNTIME_PROFILE_BLOB,
        RUNTIME_VALIDATOR: EXPECTED_RUNTIME_VALIDATOR_BLOB,
        ENUM_V10: EXPECTED_ENUM_V10_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file(), f"authority/prestate file exists: {path}")
        require(git_blob(path) == expected, f"exact prestate blob {path} = {expected}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen", "frozen inventory state unchanged")
    require(frozen.get("entry_count") == 192, "frozen inventory remains 192 entries")
    frozen_ids = frozen.get("finding_ids", [])
    require(all(fid in frozen_ids for fid in TARGETS), "both TS targets are frozen inventory members")

    registry = load(REGISTRY)
    inventory = registry.get("inventory", {})
    entries = inventory.get("entries", [])
    require(inventory.get("state") == "frozen", "registry inventory remains frozen")
    require(inventory.get("entry_count") == 192 and len(entries) == 192, "registry inventory remains 192 entries")
    require(registry.get("next_revalidation_block") == "TS", "prestate next block is TS")
    ids = [e.get("finding_id") for e in entries]
    require(len(ids) == len(set(ids)) == 192, "registry finding IDs remain unique")
    by_id = {e["finding_id"]: e for e in entries}
    for fid in TARGETS:
        require(by_id[fid].get("revalidation_state") == "pending", f"{fid} is pending before closure")
        require(by_id[fid].get("terminal_state_source") is None, f"{fid} has no premature terminal source")
    require(counts(entries) == (155, 37), f"pre-TS counts are 155/37, got {counts(entries)}")
    require(first_pending(entries) == "TS-001", f"pre-TS first pending is TS-001, got {first_pending(entries)}")
    require(by_id.get("TSD-001", {}).get("revalidation_state") == "pending", "TSD-001 remains pending before TS closure")
    require(registry.get("revalidation_blocks", {}).get("TKT", {}).get("state") == "completed", "TKT is prior completed block")

    state = load(STATE)
    audit = state.get("audit")
    require(isinstance(audit, dict), "CURRENT_STATE.audit exists")
    require(audit.get("finding_inventory_count") == 192, "CURRENT_STATE inventory count remains 192")
    require(audit.get("finding_revalidation_completed_findings") == 155, "CURRENT_STATE pre-TS terminal count is 155")
    require(audit.get("finding_revalidation_pending_findings") == 37, "CURRENT_STATE pre-TS pending count is 37")
    require(audit.get("finding_revalidation_next_block") == "TS", "CURRENT_STATE pre-TS next block is TS")
    require(audit.get("finding_revalidation_latest_completed_block") == "TKT", "TKT is prior CURRENT_STATE completed block")

    source_registry = load(SOURCE_REGISTRY)
    sources = {x["source_id"]: x for x in source_registry.get("sources", [])}
    require(sources["TIME_V1.0"]["official_url"] == PDF_URL, "TimeService V1.0 source URL unchanged")

    for fid, terminal_state in TARGETS.items():
        by_id[fid]["revalidation_state"] = terminal_state
        by_id[fid]["terminal_state_source"] = str(REPORT)

    require(counts(entries) == (157, 35), f"post-TS counts are 157/35, got {counts(entries)}")
    next_finding = first_pending(entries)
    require(next_finding == "TSD-001", f"post-TS first pending is TSD-001, got {next_finding}")
    next_block = next_finding.split("-", 1)[0] if next_finding else None
    require(next_block == "TSD", f"post-TS next block is TSD, got {next_block}")

    blocks = registry.setdefault("revalidation_blocks", {})
    require("TS" not in blocks, "TS block is not already closed")
    registry["next_revalidation_block"] = next_block
    blocks["TS"] = {
        "date": "2026-09-14",
        "state": "completed",
        "authority_lane": "official byte-pinned VDV 301-2-10 TimeService V1.0 PDF plus exact VDV-301-1.0/2.0 release trees, shared ServiceNameEnumeration and executable RV-003 SNTP/DNS-SD profile",
        "evidence_id": "EV-159",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": PINNED_EV159_RUN,
        "pinned_successful_evidence_job": PINNED_EV159_JOB,
        "artifact_id": PINNED_EV159_ARTIFACT,
        "artifact_digest": PINNED_EV159_DIGEST,
        "evidence_head_sha": PINNED_EV159_HEAD,
        "source_pin": {
            "run_id": SOURCE_PIN_RUN,
            "job_id": SOURCE_PIN_JOB,
            "artifact_id": SOURCE_PIN_ARTIFACT,
            "artifact_digest": SOURCE_PIN_DIGEST,
            "head_sha": SOURCE_PIN_HEAD,
        },
        "pdf_authority": {
            "source_id": "TIME_V1.0",
            "official_url": PDF_URL,
            "sha256": PDF_SHA256,
            "size_bytes": PDF_SIZE,
            "pages": PDF_PAGES,
            "visual_pages": [4, 6],
            "semantic_evidence_mode": "byte-pinned rendered visual; Poppler text hashes fingerprint-only",
        },
        "upstream_authority": UPSTREAM,
        "runtime_authority": {
            "profile": str(RUNTIME_PROFILE),
            "profile_blob": EXPECTED_RUNTIME_PROFILE_BLOB,
            "validator": str(RUNTIME_VALIDATOR),
            "validator_blob": EXPECTED_RUNTIME_VALIDATOR_BLOB,
            "result": "PASS",
            "validation_kind": "protocol_discovery_profile",
            "xml_operations": [],
            "cyclic_time_broadcast_expected": False,
        },
        "xsd_authority": {
            "ServiceNameEnumeration_V1.0_blob": EXPECTED_ENUM_V10_BLOB,
            "dedicated_TimeService_XSD": False,
        },
        "findings": TARGETS,
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": next_block,
        "next_finding": next_finding,
    }

    audit["finding_revalidation_next_block"] = next_block
    audit["finding_revalidation_completed_findings"] = 157
    audit["finding_revalidation_pending_findings"] = 35
    audit["finding_revalidation_current_block"] = "TS"
    audit["finding_revalidation_latest_completed_block"] = "TS"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_revalidation_evidence_id"] = "EV-159"
    audit["latest_executable_evidence_id"] = "EV-159"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["ts_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-159",
        "run_id": run_id,
        "pinned_successful_evidence_run": PINNED_EV159_RUN,
        "pinned_successful_evidence_job": PINNED_EV159_JOB,
        "artifact_id": PINNED_EV159_ARTIFACT,
        "artifact_digest": PINNED_EV159_DIGEST,
        "source_pin_run": SOURCE_PIN_RUN,
        "source_pin_artifact": SOURCE_PIN_ARTIFACT,
        "terminal_states": TARGETS,
        "pdf_sha256": PDF_SHA256,
        "visual_pages": [4, 6],
        "runtime_validator": str(RUNTIME_VALIDATOR),
        "runtime_result": "PASS",
        "next_block": next_block,
        "next_finding": next_finding,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    rows = "\n".join(f"| `{fid}` | `{TARGETS[fid]}` | {RATIONALES[fid]} |" for fid in TARGETS)
    report = f"""# Finding revalidation — TimeService (TS)\n\nStatus: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen findings: `TS-001` and `TS-002`. Frozen inventory remains exactly **192 entries**.\n\n## Authority and evidence\n\n- Evidence: **EV-159**; successful closure run **{run_id}**.\n- Independently successful EV-159 run: **{PINNED_EV159_RUN}**, job **{PINNED_EV159_JOB}**, artifact **{PINNED_EV159_ARTIFACT}**, digest `{PINNED_EV159_DIGEST}`.\n- Source/render pin run: **{SOURCE_PIN_RUN}**, job **{SOURCE_PIN_JOB}**, artifact **{SOURCE_PIN_ARTIFACT}**, digest `{SOURCE_PIN_DIGEST}`.\n- Official VDV 301-2-10 TimeService V1.0 PDF: SHA-256 `{PDF_SHA256}`, {PDF_SIZE} bytes, {PDF_PAGES} pages.\n- Physical page **4** contains the bilingual document-number contradiction used for TS-002. Physical page **6** contains the SNTP/RFC-4330 and DNS-SD TimeService profile used for TS-001. Poppler text output is retained only as a byte-derived fingerprint; semantic page evidence is rendered visual evidence.\n- Exact official VDV-301-1.0 commit `{UPSTREAM['v1_0_commit']}` / tree `{UPSTREAM['v1_0_tree']}` and VDV-301-2.0 commit `{UPSTREAM['v2_0_commit']}` / tree `{UPSTREAM['v2_0_tree']}` contain no dedicated TimeService XSD.\n- `IBIS-IP_Enumerations_V1.0.xsd` blob `{EXPECTED_ENUM_V10_BLOB}` nevertheless contains `TimeService` in `ServiceNameEnumeration`.\n- RV-003 (`{EXPECTED_RUNTIME_VALIDATOR_BLOB}`) reran the deterministic SNTP/DNS-SD profile, including positive/negative cases, protocol routing, no invented XML operations and the non-cyclic delivery invariant.\n- The complete **50-file root XSD pool** was recompiled and byte-hashed before/after EV-159; no XSD changed.\n\n## Terminal states\n\n| Finding | Terminal state | Revalidation result |\n|---|---|---|\n{rows}\n\n## Mutation decision\n\n- XSD mutation: **none**.\n- Frozen inventory mutation: **none**.\n- Registry/status mutation: only `TS-001`, `TS-002` and the TS block/counter handoff.\n\n## State transition\n\n- Before: **155/192 terminal**, **37 pending**, first pending `TS-001`.\n- After: **157/192 terminal**, **35 pending**, first pending `{next_finding}`.\n- Next block: **{next_block}**.\n"""

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(report, encoding="utf-8")
    write_json(REGISTRY, registry)
    write_json(STATE, state)

    require(load(FROZEN).get("entry_count") == 192, "frozen inventory still 192 after writes")
    require(git_blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory bytes unchanged after writes")
    require(git_blob(SOURCE_REGISTRY) == EXPECTED_SOURCE_REGISTRY_BLOB, "PDF source registry unchanged after writes")
    require(git_blob(SOURCE_PINS) == EXPECTED_SOURCE_PINS_BLOB, "PDF source pin registry unchanged after writes")
    require(git_blob(ENUM_V10) == EXPECTED_ENUM_V10_BLOB, "ServiceNameEnumeration XSD unchanged after writes")

    post_registry = load(REGISTRY)
    post_entries = post_registry["inventory"]["entries"]
    require(counts(post_entries) == (157, 35), "written registry counts are 157/35")
    require(first_pending(post_entries) == "TSD-001", "written registry first pending is TSD-001")
    require(post_registry.get("next_revalidation_block") == "TSD", "written registry next block is TSD")
    require(post_registry["revalidation_blocks"]["TS"]["artifact_digest"] == PINNED_EV159_DIGEST, "written TS block pins EV-159 artifact digest")

    post_audit = load(STATE)["audit"]
    require(post_audit.get("finding_revalidation_completed_findings") == 157, "written CURRENT_STATE terminal count is 157")
    require(post_audit.get("finding_revalidation_pending_findings") == 35, "written CURRENT_STATE pending count is 35")
    require(post_audit.get("finding_revalidation_next_block") == "TSD", "written CURRENT_STATE next block is TSD")
    require(post_audit.get("finding_revalidation_latest_completed_block") == "TS", "written CURRENT_STATE latest block is TS")
    require(REPORT.is_file(), "TS revalidation report written")
    print("PASS TS closure writer")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
