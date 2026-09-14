#!/usr/bin/env python3
"""EV-163: fail-closed aggregate revalidation gate for TVS-001..TVS-003.

EV-112..EV-114 are official release routes. EV-115 is V2.4
candidate/integration executable evidence and MUST NOT be reported as official
VDV-301-2.4 release conformance because no such release tag exists.

This validator mutates neither schemas nor audit state. It emits evidence only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

EXPECTED_BLOBS = {
    "audit_registry/finding_inventory_frozen_2026-09-03.json": "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
    "audit_registry/finding_revalidation_registry_v0.1.json": "d874cbe211d2335bb02fa9ed317244b31803e3dc",
    "audit_registry/pdf_source_registry_v0.1.json": "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
    "audit_registry/pdf_source_pins_v0.1.json": "88349638b423689799af700e8a1c8ec99bbfb67b",
    "00_START_HERE/CURRENT_STATE.json": "6406675512fdcca7ef75fcfd788631660932fb1c",
    "docs/pdf_xsd_semantic_audit/TICKET_VALIDATION_SERVICE_FINDINGS_REGISTER_ADDENDUM.md": "adea51d2dc812cedaf6f8957651c7ea6ac0dfaff",
    "tools/validate_tvs_v21_ev112.py": "ac95c53ac1ca1900f51df0b06fe3f0ed623700f5",
    "tools/validate_tvs_v22_ev113.py": "097bc0fc87f80da1d1161eb49345a2603e3304d3",
    "tools/validate_tvs_v23_ev114.py": "9411dd8123d0b7019b05b495eb493208c0f0ce81",
    "tools/validate_tvs_v24_ev115.py": "2f2fc8ad2a6d3180a3dc961b8de55ecae2c5c6d7",
    "tools/validate_drtvs21_revalidation_ev150.py": "cef846d7c18ed84b087e10e91e8df0d2637f304b",
}

TARGET_STATES = {
    "TVS-001": "executable_confirmed",
    "TVS-002": "executable_confirmed",
    "TVS-003": "executable_confirmed",
}

TERMINAL = {
    "source_verified",
    "context_verified",
    "executable_confirmed",
    "contextual_not_defect",
    "withdrawn",
    "unresolved",
    "superseded",
}

LANES = [
    ("EV-112", "tools/validate_tvs_v21_ev112.py", "official_release_V2.1"),
    ("EV-113", "tools/validate_tvs_v22_ev113.py", "official_release_V2.2"),
    ("EV-114", "tools/validate_tvs_v23_ev114.py", "official_release_V2.3"),
    ("EV-115", "tools/validate_tvs_v24_ev115.py", "candidate_integration_V2.4_not_official_release_conformance"),
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"OK  {message}")


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def assert_tokens(text: str, tokens: list[str], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    require(not missing, f"{label} contains required tokens" + (f"; missing={missing}" if missing else ""))


def counts(entries: list[dict]) -> tuple[int, int]:
    return (
        sum(x.get("revalidation_state") in TERMINAL for x in entries),
        sum(x.get("revalidation_state") == "pending" for x in entries),
    )


def first_pending(entries: list[dict]) -> str | None:
    return next((x.get("finding_id") for x in entries if x.get("revalidation_state") == "pending"), None)


def run_lane(root: Path, output: Path, evidence_id: str, rel: str, authority: str) -> dict:
    tool = root / rel
    proc = subprocess.run(
        [sys.executable, str(tool)], cwd=str(root), text=True, capture_output=True
    )
    log = output / f"{evidence_id.lower().replace('-', '_')}.log"
    log.write_text(proc.stdout + ("\nSTDERR:\n" + proc.stderr if proc.stderr else ""), encoding="utf-8")
    require(proc.returncode == 0, f"{evidence_id} executable lane passes ({authority})")
    require("PASSED:" in proc.stdout, f"{evidence_id} emits explicit PASSED marker")
    return {
        "evidence_id": evidence_id,
        "validator": rel,
        "validator_blob": git_blob_sha(tool),
        "authority": authority,
        "log": log.name,
        "log_sha256": sha256(log),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()

    root = args.repo_root.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)

    for rel, expected in EXPECTED_BLOBS.items():
        path = root / rel
        require(path.is_file(), f"pinned prestate file exists: {rel}")
        require(git_blob_sha(path) == expected, f"pinned prestate blob {rel} = {expected}")

    state = json.loads((root / "00_START_HERE/CURRENT_STATE.json").read_text(encoding="utf-8"))
    registry = json.loads((root / "audit_registry/finding_revalidation_registry_v0.1.json").read_text(encoding="utf-8"))
    audit = state["audit"]
    entries = registry["inventory"]["entries"]

    require(state["canonical_branch"] == "dev/schema-integration", "canonical branch is dev/schema-integration")
    require(audit["finding_inventory_count"] == 192, "frozen finding inventory count is 192")
    require(audit["finding_revalidation_completed_findings"] == 165, "prestate terminal count is 165")
    require(audit["finding_revalidation_pending_findings"] == 27, "prestate pending count is 27")
    require(audit["finding_revalidation_next_block"] == "TVS", "prestate next block is TVS")
    require(audit["finding_revalidation_latest_completed_block"] == "TSM", "latest completed block is TSM")
    require(audit["latest_executable_evidence_id"] == "EV-162", "latest executable evidence before TVS is EV-162")
    require(registry.get("next_revalidation_block") == "TVS", "registry next block is TVS")

    ids = [x["finding_id"] for x in entries]
    require(len(ids) == len(set(ids)) == 192, "registry inventory contains exactly 192 unique findings")
    require(counts(entries) == (165, 27), f"registry prestate counts are 165/27, got {counts(entries)}")
    require(first_pending(entries) == "TVS-001", "registry prestate first pending is TVS-001")
    by_id = {x["finding_id"]: x for x in entries}
    pending = [x["finding_id"] for x in entries if x.get("revalidation_state") == "pending"]
    require(pending[:3] == ["TVS-001", "TVS-002", "TVS-003"], "TVS findings are the contiguous leading pending block")
    for fid in TARGET_STATES:
        require(by_id[fid].get("revalidation_state") == "pending", f"{fid} is pending before EV-163")
        require(by_id[fid].get("terminal_state_source") is None, f"{fid} has no premature terminal-state source")

    projected = [dict(x) for x in entries]
    projected_by_id = {x["finding_id"]: x for x in projected}
    for fid, terminal_state in TARGET_STATES.items():
        projected_by_id[fid]["revalidation_state"] = terminal_state
    require(counts(projected) == (168, 24), f"projected post-TVS counts are 168/24, got {counts(projected)}")
    require(first_pending(projected) == "VDS-001", f"projected next finding is VDS-001, got {first_pending(projected)}")

    addendum = (root / "docs/pdf_xsd_semantic_audit/TICKET_VALIDATION_SERVICE_FINDINGS_REGISTER_ADDENDUM.md").read_text(encoding="utf-8")
    assert_tokens(addendum, [
        "TVS-001 - GetCurrentShortHaulStopsResponse omitted from TicketValidationServiceOperations",
        "upstream_master_structurally_confirmed_and_candidate_integration_executable_confirmed_EV-115",
        "No V2.4 release tag exists; executable evidence is candidate/integration authority.",
        "TVS-002 - VehicleData.RouteDeviation PDF type vs XSD type",
        "TVS-003 - stale CurrentStopPoint names after CurrentTariffStop rename",
        "EV-115: candidate/integration evidence only; not official-release conformance",
    ], "TVS finding register authority boundary")

    ev115_source = (root / "tools/validate_tvs_v24_ev115.py").read_text(encoding="utf-8")
    assert_tokens(ev115_source, [
        "candidate/integration", "NOT official-release V2.4 XSD conformance", "VDV-301-2.4",
        "GetCurrentShortHaulStopsResponse", "TicketValidationServiceOperations",
    ], "EV-115 provenance and TVS-001 structural guard")

    lane_results = [run_lane(root, output, *lane) for lane in LANES]

    manifest = {
        "evidence_id": "EV-163",
        "scope": ["TVS-001", "TVS-002", "TVS-003"],
        "purpose": "aggregate fail-closed revalidation of the frozen TVS block",
        "prestate": {"terminal": 165, "pending": 27, "first_pending": "TVS-001", "next_block": "TVS", "latest_evidence": "EV-162"},
        "target_states": TARGET_STATES,
        "projected_poststate": {"terminal": 168, "pending": 24, "first_pending": "VDS-001", "next_block": "VDS"},
        "lanes": lane_results,
        "authority_boundary": {
            "TVS-001": "upstream-master structural confirmation plus EV-115 candidate/integration executable evidence",
            "TVS-002": "official executable evidence EV-112/EV-113/EV-114; EV-115 adds candidate/integration V2.4 continuity only",
            "TVS-003": "official executable evidence EV-113/EV-114; EV-115 adds candidate/integration V2.4 continuity with official-PDF context",
            "v2_4_release_tag": "absent",
            "ev115_must_not_be_reported_as": "official V2.4 release XSD conformance",
        },
        "immutable_prestate_blobs": EXPECTED_BLOBS,
        "closure_authorized_only_after_ci_success": True,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }
    manifest_path = output / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"OK  wrote {manifest_path}")
    print("PASSED: EV-163 TVS aggregate revalidation gate; projected poststate 168/24, next VDS-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
