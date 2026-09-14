#!/usr/bin/env python3
"""Fail-closed closure writer for frozen TicketValidationService findings TVS-001..003."""
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
ADDENDUM = Path("docs/pdf_xsd_semantic_audit/TICKET_VALIDATION_SERVICE_FINDINGS_REGISTER_ADDENDUM.md")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_TVS_2026-09-14.md")
VALIDATOR = Path("tools/validate_tvs_revalidation_ev163.py")
EV112 = Path("tools/validate_tvs_v21_ev112.py")
EV113 = Path("tools/validate_tvs_v22_ev113.py")
EV114 = Path("tools/validate_tvs_v23_ev114.py")
EV115 = Path("tools/validate_tvs_v24_ev115.py")
XSD_POOL = Path("tools/validate_xsd_pool.py")
TVS21 = Path("IBIS-IP_TicketValidationService_V2.1.xsd")
COMMON10 = Path("IBIS-IP_common_V1.0.xsd")
ENUM10 = Path("IBIS-IP_Enumerations_V1.0.xsd")
TVS22 = Path("IBIS-IP_TicketValidationService_V2.2.xsd")
COMMON22 = Path("IBIS-IP_common_V2.2.xsd")
ENUM22 = Path("IBIS-IP_Enumerations_V2.2.xsd")
TVS23 = Path("IBIS-IP_TicketValidationService_V2.3.xsd")
TVS24 = Path("IBIS-IP_TicketValidationService_V2.4.xsd")
COMMON24 = Path("IBIS-IP_common_V2.4.xsd")
ENUM24 = Path("IBIS-IP_Enumerations_V2.4.xsd")

EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_REGISTRY_PRE_BLOB = "d874cbe211d2335bb02fa9ed317244b31803e3dc"
EXPECTED_STATE_PRE_BLOB = "6406675512fdcca7ef75fcfd788631660932fb1c"
EXPECTED_SOURCE_REGISTRY_BLOB = "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8"
EXPECTED_SOURCE_PINS_BLOB = "88349638b423689799af700e8a1c8ec99bbfb67b"
EXPECTED_EVIDENCE_GATE_BLOB = "969cce8b14b50ded2ca5eb745674b894428ecf1a"
EXPECTED_ADDENDUM_BLOB = "adea51d2dc812cedaf6f8957651c7ea6ac0dfaff"
EXPECTED_VALIDATOR_BLOB = "094d16f26be4a00740a23d7014c968e9641f5485"
EXPECTED_EV112_BLOB = "ac95c53ac1ca1900f51df0b06fe3f0ed623700f5"
EXPECTED_EV113_BLOB = "097bc0fc87f80da1d1161eb49345a2603e3304d3"
EXPECTED_EV114_BLOB = "9411dd8123d0b7019b05b495eb493208c0f0ce81"
EXPECTED_EV115_BLOB = "2f2fc8ad2a6d3180a3dc961b8de55ecae2c5c6d7"
EXPECTED_XSD_POOL_BLOB = "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd"
EXPECTED_TVS21_BLOB = "f6497e6469b82ee19b185c4de749d13a7ca60bed"
EXPECTED_COMMON10_BLOB = "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c"
EXPECTED_ENUM10_BLOB = "a9bea5bc73003ed91ded8519db06c32c4067831d"
EXPECTED_TVS22_BLOB = "5a4be2b2ba66860f035777ec0458dba0790880e1"
EXPECTED_COMMON22_BLOB = "468fee6d177e7185dbcd5d3f90cfb114e29e01ae"
EXPECTED_ENUM22_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"
EXPECTED_TVS23_BLOB = "b17591c5b067254dd3e2260f3ef2acd2e18394a9"
EXPECTED_TVS24_BLOB = "34b18b8c874e325dd923b366a72bb0ebee32e59e"
EXPECTED_COMMON24_BLOB = "1946fd37e29ced605654f49ea3d98cd2fbbdc8e4"
EXPECTED_ENUM24_BLOB = "2afed8cf23afa91db92b0f043cc5b4ad428b0f25"

PINNED_EV163_RUN = "34835469790"
PINNED_EV163_JOB = "103948172257"
PINNED_EV163_ARTIFACT = "10343689439"
PINNED_EV163_DIGEST = "sha256:dbba3bbd71adf72f0d44ba540d214291190749f5f8cbe5d0a6341461ad68f140"
PINNED_EV163_HEAD = "b2dc3c28bce9dc21591a3e232e12cace90637616"

TARGETS = {
    "TVS-001": "executable_confirmed",
    "TVS-002": "executable_confirmed",
    "TVS-003": "executable_confirmed",
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
        VALIDATOR: EXPECTED_VALIDATOR_BLOB,
        EV112: EXPECTED_EV112_BLOB,
        EV113: EXPECTED_EV113_BLOB,
        EV114: EXPECTED_EV114_BLOB,
        EV115: EXPECTED_EV115_BLOB,
        XSD_POOL: EXPECTED_XSD_POOL_BLOB,
        TVS21: EXPECTED_TVS21_BLOB,
        COMMON10: EXPECTED_COMMON10_BLOB,
        ENUM10: EXPECTED_ENUM10_BLOB,
        TVS22: EXPECTED_TVS22_BLOB,
        COMMON22: EXPECTED_COMMON22_BLOB,
        ENUM22: EXPECTED_ENUM22_BLOB,
        TVS23: EXPECTED_TVS23_BLOB,
        TVS24: EXPECTED_TVS24_BLOB,
        COMMON24: EXPECTED_COMMON24_BLOB,
        ENUM24: EXPECTED_ENUM24_BLOB,
    }
    for path, expected in immutable.items():
        require(path.is_file() and blob(path) == expected, f"exact prestate/authority blob {path} = {expected}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory remains exactly 192")
    require(all(fid in frozen.get("finding_ids", []) for fid in TARGETS), "all TVS targets are frozen inventory members")

    registry = load(REGISTRY)
    entries = registry["inventory"]["entries"]
    ids = [x["finding_id"] for x in entries]
    require(len(ids) == len(set(ids)) == 192, "registry contains exactly 192 unique findings")
    require(registry.get("next_revalidation_block") == "TVS", "prestate next block is TVS")
    require(counts(entries) == (165, 27), f"pre-TVS counts are 165/27, got {counts(entries)}")
    require(first_pending(entries) == "TVS-001", "pre-TVS first pending is TVS-001")
    by_id = {x["finding_id"]: x for x in entries}
    for fid in TARGETS:
        require(by_id[fid].get("revalidation_state") == "pending" and by_id[fid].get("terminal_state_source") is None, f"{fid} is pending without premature source")
    require(by_id["VDS-001"].get("revalidation_state") == "pending", "VDS-001 remains pending before TVS closure")
    require(registry.get("revalidation_blocks", {}).get("TSM", {}).get("state") == "completed", "TSM is prior completed block")
    require("TVS" not in registry.get("revalidation_blocks", {}), "TVS block is not already closed")

    audit = load(STATE)["audit"]
    require(audit.get("finding_revalidation_completed_findings") == 165, "CURRENT_STATE pre-TVS terminal count is 165")
    require(audit.get("finding_revalidation_pending_findings") == 27, "CURRENT_STATE pre-TVS pending count is 27")
    require(audit.get("finding_revalidation_next_block") == "TVS", "CURRENT_STATE pre-TVS next block is TVS")
    require(audit.get("finding_revalidation_latest_completed_block") == "TSM", "TSM is prior CURRENT_STATE completed block")
    require(audit.get("latest_revalidation_evidence_id") == "EV-162", "EV-162 is prior revalidation evidence")
    require(audit.get("latest_executable_evidence_id") == "EV-162", "EV-162 is prior executable evidence")

    for fid, terminal_state in TARGETS.items():
        by_id[fid]["revalidation_state"] = terminal_state
        by_id[fid]["terminal_state_source"] = str(REPORT)

    require(counts(entries) == (168, 24), f"post-TVS counts are 168/24, got {counts(entries)}")
    next_finding = first_pending(entries)
    require(next_finding == "VDS-001", f"post-TVS first pending is VDS-001, got {next_finding}")

    authority_boundary = {
        "EV-112": "official VDV-301-2.1 executable route",
        "EV-113": "official VDV-301-2.2 executable route",
        "EV-114": "official VDV-301-2.3 route; release routes through the V2.2-named TVS service XSD",
        "EV-115": "candidate/integration V2.4 executable evidence only; NOT official-release V2.4 XSD conformance",
        "v2_4_release_tag": "absent",
    }

    registry["next_revalidation_block"] = "VDS"
    registry.setdefault("revalidation_blocks", {})["TVS"] = {
        "date": "2026-09-14",
        "state": "completed",
        "authority_lane": "EV-112/EV-113/EV-114 official release lanes plus EV-115 candidate/integration V2.4 continuity under an explicit non-official-release boundary",
        "authority_boundary": authority_boundary,
        "evidence_id": "EV-163",
        "evidence_run_id": run_id,
        "evidence_run_url": run_url,
        "pinned_successful_evidence_run": PINNED_EV163_RUN,
        "pinned_successful_evidence_job": PINNED_EV163_JOB,
        "artifact_id": PINNED_EV163_ARTIFACT,
        "artifact_digest": PINNED_EV163_DIGEST,
        "evidence_head_sha": PINNED_EV163_HEAD,
        "underlying_executable_evidence": ["EV-112", "EV-113", "EV-114", "EV-115"],
        "full_xsd_regression_pool": {"root_xsd_count": 50, "result": "PASS"},
        "findings": TARGETS,
        "terminal_state_source": str(REPORT),
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": "VDS",
        "next_finding": next_finding,
    }

    audit["finding_revalidation_next_block"] = "VDS"
    audit["finding_revalidation_completed_findings"] = 168
    audit["finding_revalidation_pending_findings"] = 24
    audit["finding_revalidation_current_block"] = "TVS"
    audit["finding_revalidation_latest_completed_block"] = "TVS"
    audit["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    audit["latest_revalidation_evidence_id"] = "EV-163"
    audit["latest_executable_evidence_id"] = "EV-163"
    audit["latest_executable_evidence_run_id"] = run_id
    audit["latest_executable_evidence_run"] = run_id
    audit["tvs_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-163",
        "run_id": run_id,
        "pinned_successful_evidence_run": PINNED_EV163_RUN,
        "pinned_successful_evidence_job": PINNED_EV163_JOB,
        "artifact_id": PINNED_EV163_ARTIFACT,
        "artifact_digest": PINNED_EV163_DIGEST,
        "evidence_head_sha": PINNED_EV163_HEAD,
        "terminal_states": TARGETS,
        "authority_boundary": authority_boundary,
        "xsd_pool_result": "PASS_50_root_XSDs",
        "next_block": "VDS",
        "next_finding": next_finding,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report = f"""# Finding revalidation — TicketValidationService (TVS)\n\nStatus: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.\n\n## Scope\n\nFrozen findings: `TVS-001` through `TVS-003`. Frozen inventory remains exactly **192 entries**.\n\n## Evidence and authority\n\n- Aggregate evidence: **EV-163**; closure run **{run_id}**.\n- Successful EV-163 validation run: **{PINNED_EV163_RUN}**, job **{PINNED_EV163_JOB}**, artifact **{PINNED_EV163_ARTIFACT}**, digest `{PINNED_EV163_DIGEST}`, head `{PINNED_EV163_HEAD}`.\n- EV-112: official VDV-301-2.1 executable route.\n- EV-113: official VDV-301-2.2 executable route.\n- EV-114: official VDV-301-2.3 route; the release routes TicketValidationService through the V2.2-named service XSD.\n- EV-115: V2.4 **candidate/integration** executable evidence only. No VDV-301-2.4 release tag exists; EV-115 is **not official-release V2.4 XSD conformance**.\n- Complete **50-root-XSD pool** passed again. No XSD or frozen-inventory mutation occurred.\n\n## Terminal states\n\n| Finding | Terminal state | Result |\n|---|---|---|\n| `TVS-001` | `executable_confirmed` | Upstream-master structural confirmation plus EV-115 candidate/integration executable evidence confirms the omitted `GetCurrentShortHaulStopsResponse` operation-group boundary. This does **not** elevate the V2.4 candidate lane to official release authority. |\n| `TVS-002` | `executable_confirmed` | Official executable evidence EV-112/EV-113/EV-114 confirms the `VehicleData.RouteDeviation` type behavior across official release routes; EV-115 adds candidate/integration continuity only. |\n| `TVS-003` | `executable_confirmed` | Official executable evidence EV-113/EV-114 confirms the `CurrentStopPoint` → `CurrentTariffStop` rename boundary; EV-115 adds candidate/integration continuity only. |\n\n## Post-state\n\n- Terminal: **168 / 192**\n- Pending: **24 / 192**\n- Next block: **VDS**\n- First pending finding: **VDS-001**\n- XSD mutation: **none**\n- Frozen inventory mutation: **none**\n"""

    write_json(REGISTRY, registry)
    state = load(STATE)
    state["audit"] = audit
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")

    require(counts(load(REGISTRY)["inventory"]["entries"]) == (168, 24), "written registry is 168/24")
    require(first_pending(load(REGISTRY)["inventory"]["entries"]) == "VDS-001", "written registry first pending is VDS-001")
    require(load(STATE)["audit"].get("finding_revalidation_next_block") == "VDS", "written CURRENT_STATE next block is VDS")
    require(REPORT.is_file(), "TVS terminal report written")
    print("PASSED: TVS closure writer produced atomic 168/24 -> VDS-001 state")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
