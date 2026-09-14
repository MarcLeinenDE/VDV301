#!/usr/bin/env python3
"""Fail-closed evidence gate for the final finding/provenance baseline freeze.

EV-168 verifies that the complete legacy-finding revalidation and readiness reconciliation
are finished and stable before a machine-readable baseline is frozen. It does not mutate
findings, source registries, the frozen inventory, or XSDs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FROZEN = ROOT / "audit_registry/finding_inventory_frozen_2026-09-03.json"
REGISTRY = ROOT / "audit_registry/finding_revalidation_registry_v0.1.json"
STATE = ROOT / "00_START_HERE/CURRENT_STATE.json"
SOURCE_REGISTRY = ROOT / "audit_registry/pdf_source_registry_v0.1.json"
SOURCE_PINS = ROOT / "audit_registry/pdf_source_pins_v0.1.json"
EVIDENCE_GATE = ROOT / "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md"
PLAN = ROOT / "docs/pdf_xsd_semantic_audit/LEGACY_FINDING_REVALIDATION_PLAN.md"
READINESS_REPORT = ROOT / "docs/pdf_xsd_semantic_audit/FINDING_READINESS_RECONCILIATION_2026-09-14.md"
PIN_CORRECTION = ROOT / "docs/pdf_xsd_semantic_audit/PDF_SOURCE_PIN_CORRECTION_CIS_2026-09-14.md"
XSD_POOL = ROOT / "tools/validate_xsd_pool.py"

EXPECTED_BLOBS = {
    FROZEN: "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
    REGISTRY: "d5a645bb9c1498cbca55796d16d2ee71c80ebb37",
    STATE: "ccc7efa9d1a12578295dcab7b19a18e3ef3e8e94",
    SOURCE_REGISTRY: "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
    SOURCE_PINS: "bc60527ddc158d967470a63d38ffd035e5ec1400",
    EVIDENCE_GATE: "969cce8b14b50ded2ca5eb745674b894428ecf1a",
    PLAN: "b8a38bd09ca6239b96981548b7cfcbd49aa4c9d5",
    READINESS_REPORT: "edb9490a0dcdba5c9dbab0cb69a382d7c5e7226d",
    PIN_CORRECTION: "ed10d5fd6f900372231891b72069f43eba0ddd87",
    XSD_POOL: "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd",
}

TERMINAL = {
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
    print(f"OK  {message}")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


def canonical_json_sha256(value: object) -> str:
    encoded = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    for path, expected in EXPECTED_BLOBS.items():
        require(path.is_file(), f"required baseline input exists: {path.relative_to(ROOT)}")
        require(blob(path) == expected, f"exact baseline input blob {path.relative_to(ROOT)} = {expected}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen", "original finding inventory remains frozen")
    require(frozen.get("entry_count") == 192, "original frozen inventory contains 192 findings")
    frozen_ids = frozen.get("finding_ids", [])
    require(len(frozen_ids) == len(set(frozen_ids)) == 192, "frozen inventory contains 192 unique finding IDs")

    registry = load(REGISTRY)
    entries = registry["inventory"]["entries"]
    ids = [entry["finding_id"] for entry in entries]
    require(len(entries) == len(set(ids)) == 192, "final revalidation registry contains 192 unique findings")
    require(ids == frozen_ids, "final registry finding order/identity exactly matches frozen inventory")
    require(all(entry.get("revalidation_state") in TERMINAL for entry in entries), "all 192 findings have terminal states")
    require(not any(entry.get("revalidation_state") == "pending" for entry in entries), "zero pending findings")
    require(not any(entry.get("revalidation_state") == "unresolved" for entry in entries), "zero unresolved findings after readiness reconciliation")
    require(all(entry.get("terminal_state_source") for entry in entries), "every terminal finding has a terminal-state source")
    require(registry.get("next_revalidation_block") is None, "no remaining revalidation block")
    require(
        registry.get("state") == "inventory_frozen_revalidation_complete_finding_knowledge_ready",
        "registry records complete finding-knowledge readiness",
    )

    sdk = registry.get("sdk_readiness", {})
    require(sdk.get("finding_knowledge_ready") is True, "finding knowledge readiness is true")
    require(sdk.get("readiness_reconciliation_pending") == [], "no readiness reconciliation remains pending")
    require(sdk.get("unresolved_sdk_affecting_findings") == [], "no unresolved SDK-affecting finding remains")
    exclusions = sdk.get("strict_profile_exclusions", {})
    require(
        "CIS_V1.1" in exclusions and "fail closed" in exclusions["CIS_V1.1"],
        "CIS V1.1 strict-profile exclusion is preserved fail-closed",
    )
    require(sdk.get("readiness_evidence_id") == "EV-167", "EV-167 is final readiness evidence")
    require(str(sdk.get("readiness_evidence_run_id")) == "34843562886", "EV-167 successful run is pinned")

    remediation = registry.get("remediation_readiness", {})
    require(remediation.get("ready") is False, "official-facing remediation is not implicitly authorized")
    require(remediation.get("official_facing_action_requires_separate_explicit_decision") is True, "remediation remains a separate explicit decision")

    state = load(STATE)
    audit = state["audit"]
    require(state.get("canonical_branch") == "dev/schema-integration", "CURRENT_STATE canonical branch is dev/schema-integration")
    require(state.get("project_phase") == "finding_baseline_freeze_ready", "project is exactly baseline-freeze ready")
    require(audit.get("finding_revalidation_completed_findings") == 192, "CURRENT_STATE terminal count is 192")
    require(audit.get("finding_revalidation_pending_findings") == 0, "CURRENT_STATE pending count is 0")
    require(audit.get("finding_knowledge_ready") is True, "CURRENT_STATE finding knowledge ready is true")
    require(audit.get("finding_baseline_freeze_ready") is True, "CURRENT_STATE explicitly allows baseline freeze")
    require(audit.get("finding_readiness_reconciliation_pending") == [], "CURRENT_STATE has no remaining readiness reconciliation")
    require(audit.get("latest_revalidation_evidence_id") == "EV-167", "CURRENT_STATE latest revalidation evidence is EV-167")

    source_registry = load(SOURCE_REGISTRY)
    source_pins = load(SOURCE_PINS)
    require(source_registry.get("physical_source_count") == 50, "PDF source registry retains 50 physical sources")
    require(source_registry.get("semantic_document_count") == 48, "PDF source registry retains 48 semantic document units")
    require(source_pins.get("hash_algorithm") == "sha256", "PDF pin registry remains SHA-256 based")
    require(len(source_pins.get("sources", [])) >= 48, "PDF pin registry retains complete audit source set")

    # Deterministic finding-state digest: this is the key semantic anchor of the frozen baseline.
    canonical_entries = [
        {
            "finding_id": entry["finding_id"],
            "revalidation_state": entry["revalidation_state"],
            "terminal_state_source": entry["terminal_state_source"],
        }
        for entry in entries
    ]
    entries_digest = canonical_json_sha256(canonical_entries)
    authority_digest = canonical_json_sha256(
        {
            "strict_profile_exclusions": sdk.get("strict_profile_exclusions", {}),
            "pdf_source_registry_blob": EXPECTED_BLOBS[SOURCE_REGISTRY],
            "pdf_source_pins_blob": EXPECTED_BLOBS[SOURCE_PINS],
            "evidence_gate_blob": EXPECTED_BLOBS[EVIDENCE_GATE],
            "revalidation_plan_blob": EXPECTED_BLOBS[PLAN],
            "readiness_report_blob": EXPECTED_BLOBS[READINESS_REPORT],
        }
    )

    xsd_files = sorted(ROOT.glob("*.xsd"), key=lambda p: p.name)
    require(len(xsd_files) == 50, "canonical root XSD pool contains exactly 50 files")
    xsd_manifest = [{"path": path.name, "sha256": file_sha256(path)} for path in xsd_files]
    xsd_manifest_digest = canonical_json_sha256(xsd_manifest)

    evidence = {
        "evidence_id": "EV-168",
        "purpose": "final finding/provenance baseline freeze precondition",
        "source_branch": "dev/schema-integration",
        "prestate": {
            "project_phase": "finding_baseline_freeze_ready",
            "frozen_inventory_count": 192,
            "terminal_findings": 192,
            "pending_findings": 0,
            "unresolved_findings": 0,
            "finding_knowledge_ready": True,
            "next_revalidation_block": None,
        },
        "immutable_input_blobs": {str(path.relative_to(ROOT)): sha for path, sha in EXPECTED_BLOBS.items()},
        "finding_entries_sha256": entries_digest,
        "authority_snapshot_sha256": authority_digest,
        "xsd_pool": {
            "root_xsd_count": 50,
            "manifest_sha256": xsd_manifest_digest,
            "files": xsd_manifest,
        },
        "readiness_evidence": {
            "id": "EV-167",
            "run": "34843562886",
            "job": "103973944657",
            "artifact": "10347047619",
            "artifact_digest": "sha256:d978765cfbd90b5f0ab345d9f6626b3ead6c051ac3477cf6a542d6db74a36bf2",
            "head": "171ff38a4b9df401429749ad9c8b5133de4d2e9a",
        },
        "authority_guards": {
            "latest_wins": False,
            "candidate_authority_promoted": False,
            "cis_v1_1_strict_profile": "excluded_fail_closed",
            "remediation_authorized": False,
        },
        "projected_freeze": {
            "project_phase": "finding_baseline_frozen",
            "finding_knowledge_ready": True,
            "finding_baseline_frozen": True,
            "remediation_authorized": False,
        },
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"FINDING_ENTRIES_SHA256={entries_digest}")
    print(f"AUTHORITY_SNAPSHOT_SHA256={authority_digest}")
    print(f"XSD_MANIFEST_SHA256={xsd_manifest_digest}")
    print(f"PASSED: EV-168 finding/provenance baseline pre-freeze gate; wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
