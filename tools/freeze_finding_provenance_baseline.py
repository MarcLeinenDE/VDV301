#!/usr/bin/env python3
"""Fail-closed writer for the final finding/provenance baseline freeze."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "audit_registry/finding_revalidation_registry_v0.1.json"
STATE = ROOT / "00_START_HERE/CURRENT_STATE.json"
FROZEN = ROOT / "audit_registry/finding_inventory_frozen_2026-09-03.json"
SOURCE_REGISTRY = ROOT / "audit_registry/pdf_source_registry_v0.1.json"
SOURCE_PINS = ROOT / "audit_registry/pdf_source_pins_v0.1.json"
EVIDENCE_GATE = ROOT / "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md"
PLAN = ROOT / "docs/pdf_xsd_semantic_audit/LEGACY_FINDING_REVALIDATION_PLAN.md"
READINESS_REPORT = ROOT / "docs/pdf_xsd_semantic_audit/FINDING_READINESS_RECONCILIATION_2026-09-14.md"
PIN_CORRECTION = ROOT / "docs/pdf_xsd_semantic_audit/PDF_SOURCE_PIN_CORRECTION_CIS_2026-09-14.md"
VALIDATOR = ROOT / "tools/validate_finding_baseline_ev168.py"
XSD_POOL = ROOT / "tools/validate_xsd_pool.py"
BASELINE = ROOT / "audit_registry/finding_provenance_baseline_2026-09-14.json"
REPORT = ROOT / "docs/pdf_xsd_semantic_audit/FINDING_PROVENANCE_BASELINE_FREEZE_2026-09-14.md"

EXPECTED = {
    FROZEN: "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
    REGISTRY: "d5a645bb9c1498cbca55796d16d2ee71c80ebb37",
    STATE: "ccc7efa9d1a12578295dcab7b19a18e3ef3e8e94",
    SOURCE_REGISTRY: "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
    SOURCE_PINS: "bc60527ddc158d967470a63d38ffd035e5ec1400",
    EVIDENCE_GATE: "969cce8b14b50ded2ca5eb745674b894428ecf1a",
    PLAN: "b8a38bd09ca6239b96981548b7cfcbd49aa4c9d5",
    READINESS_REPORT: "edb9490a0dcdba5c9dbab0cb69a382d7c5e7226d",
    PIN_CORRECTION: "ed10d5fd6f900372231891b72069f43eba0ddd87",
    VALIDATOR: "dddc6d0ef605b7725a85b8b54bd7b1d8995325a8",
    XSD_POOL: "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd",
}

EV168_RUN = "34844500027"
EV168_JOB = "103977033739"
EV168_ARTIFACT = "10347158213"
EV168_DIGEST = "sha256:cf92dcd1e0ca3ca24efc7d8327e3a9ce10d6fc1fc1e2342c0a56ac6ecf36a608"
EV168_HEAD = "f0eab8251939ef69c921e721fa5d8db1c049055e"
FINDING_ENTRIES_SHA256 = "411519c4aaaeb370dfa336d729988d37007a78dfaf5bc6d5fcfb1dfa3f49f792"
AUTHORITY_SNAPSHOT_SHA256 = "1f4d5b9468668c7b1839585b710fc63ad6a5ef6196f14afbe58c36377c809e95"
XSD_MANIFEST_SHA256 = "081cff20627157441c6fb6da11f4026906080e7dd44479e45c8bbcc1ef3dcb26"

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


def write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


def canonical_sha(value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def file_sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    closure_run_id = os.environ.get("CLOSURE_RUN_ID", "").strip()
    closure_run_url = os.environ.get("CLOSURE_RUN_URL", "").strip()
    require(closure_run_id.isdigit(), "CLOSURE_RUN_ID is numeric")
    require(
        closure_run_url == f"https://github.com/MarcLeinenDE/VDV301/actions/runs/{closure_run_id}",
        "CLOSURE_RUN_URL matches run id",
    )

    for path, expected in EXPECTED.items():
        require(path.is_file() and blob(path) == expected, f"exact freeze input blob {path.relative_to(ROOT)} = {expected}")
    require(not BASELINE.exists(), "finding/provenance baseline does not pre-exist")
    require(not REPORT.exists(), "finding/provenance freeze report does not pre-exist")

    frozen = load(FROZEN)
    registry = load(REGISTRY)
    state = load(STATE)
    entries = registry["inventory"]["entries"]
    ids = [entry["finding_id"] for entry in entries]

    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "original inventory remains frozen at 192")
    require(ids == frozen.get("finding_ids"), "final registry IDs exactly match frozen inventory IDs")
    require(len(entries) == 192 and all(entry.get("revalidation_state") in TERMINAL for entry in entries), "all 192 final findings are terminal")
    require(not any(entry.get("revalidation_state") in {"pending", "unresolved"} for entry in entries), "zero pending and unresolved findings")
    require(registry.get("state") == "inventory_frozen_revalidation_complete_finding_knowledge_ready", "registry is ready for baseline freeze")
    require(registry.get("next_revalidation_block") is None, "no revalidation block remains")
    require(registry["sdk_readiness"].get("finding_knowledge_ready") is True, "finding knowledge is ready")
    require(registry["remediation_readiness"].get("ready") is False, "remediation is not implicitly authorized")
    require(state.get("project_phase") == "finding_baseline_freeze_ready", "CURRENT_STATE is exactly baseline-freeze ready")
    require(state["audit"].get("finding_baseline_freeze_ready") is True, "CURRENT_STATE baseline-freeze flag is true")

    final_entries = [
        {
            "finding_id": entry["finding_id"],
            "revalidation_state": entry["revalidation_state"],
            "terminal_state_source": entry["terminal_state_source"],
        }
        for entry in entries
    ]
    require(canonical_sha(final_entries) == FINDING_ENTRIES_SHA256, "final finding-state digest matches EV-168")

    authority_payload = {
        "strict_profile_exclusions": registry["sdk_readiness"].get("strict_profile_exclusions", {}),
        "pdf_source_registry_blob": EXPECTED[SOURCE_REGISTRY],
        "pdf_source_pins_blob": EXPECTED[SOURCE_PINS],
        "evidence_gate_blob": EXPECTED[EVIDENCE_GATE],
        "revalidation_plan_blob": EXPECTED[PLAN],
        "readiness_report_blob": EXPECTED[READINESS_REPORT],
    }
    require(canonical_sha(authority_payload) == AUTHORITY_SNAPSHOT_SHA256, "authority snapshot digest matches EV-168")

    xsd_files = sorted(ROOT.glob("*.xsd"), key=lambda p: p.name)
    require(len(xsd_files) == 50, "root XSD pool still contains 50 files")
    xsd_manifest = [{"path": path.name, "sha256": file_sha(path)} for path in xsd_files]
    require(canonical_sha(xsd_manifest) == XSD_MANIFEST_SHA256, "XSD manifest digest matches EV-168")

    immutable_inputs = {str(path.relative_to(ROOT)): sha for path, sha in EXPECTED.items()}
    baseline_payload = {
        "baseline_version": "1.0",
        "date": "2026-09-14",
        "state": "frozen",
        "baseline_type": "finding_and_provenance",
        "canonical_branch": "dev/schema-integration",
        "evidence_head": EV168_HEAD,
        "evidence_id": "EV-168",
        "evidence_run_id": EV168_RUN,
        "evidence_job_id": EV168_JOB,
        "evidence_artifact_id": EV168_ARTIFACT,
        "evidence_artifact_digest": EV168_DIGEST,
        "freeze_closure_run_id": closure_run_id,
        "freeze_closure_run_url": closure_run_url,
        "inventory": {
            "count": 192,
            "terminal": 192,
            "pending": 0,
            "unresolved": 0,
            "source_snapshot": "audit_registry/finding_inventory_frozen_2026-09-03.json",
            "source_snapshot_blob": EXPECTED[FROZEN],
            "finding_entries_sha256": FINDING_ENTRIES_SHA256,
            "entries": final_entries,
        },
        "authority": {
            "snapshot_sha256": AUTHORITY_SNAPSHOT_SHA256,
            "immutable_input_blobs": immutable_inputs,
            "pdf_source_registry_blob": EXPECTED[SOURCE_REGISTRY],
            "pdf_source_pins_blob": EXPECTED[SOURCE_PINS],
            "strict_profile_exclusions": registry["sdk_readiness"].get("strict_profile_exclusions", {}),
            "latest_wins": False,
            "candidate_or_integration_authority_promoted": False,
            "cis_v1_1_release_xsd_identity": "unresolved",
            "cis_v1_1_strict_profile": "unavailable_fail_closed",
        },
        "xsd_pool": {
            "root_count": 50,
            "manifest_sha256": XSD_MANIFEST_SHA256,
            "files": xsd_manifest,
            "regression_result": "PASS",
        },
        "readiness": {
            "finding_knowledge_ready": True,
            "readiness_evidence_id": "EV-167",
            "readiness_evidence_run_id": "34843562886",
            "readiness_report": str(READINESS_REPORT.relative_to(ROOT)),
        },
        "policy": {
            "xsd_mutation_authorized": False,
            "frozen_inventory_mutation_authorized": False,
            "official_facing_remediation_authorized": False,
            "remediation_requires_separate_explicit_decision": True,
            "sdk_may_use_finding_knowledge": True,
            "selected_xsd_remains_normative_authority": True,
        },
    }
    payload_sha = canonical_sha(baseline_payload)
    baseline = dict(baseline_payload)
    baseline["baseline_payload_sha256"] = payload_sha
    write_json(BASELINE, baseline)

    baseline_record = {
        "state": "frozen",
        "date": "2026-09-14",
        "path": str(BASELINE.relative_to(ROOT)),
        "report": str(REPORT.relative_to(ROOT)),
        "baseline_payload_sha256": payload_sha,
        "finding_entries_sha256": FINDING_ENTRIES_SHA256,
        "authority_snapshot_sha256": AUTHORITY_SNAPSHOT_SHA256,
        "xsd_manifest_sha256": XSD_MANIFEST_SHA256,
        "evidence_id": "EV-168",
        "evidence_run_id": EV168_RUN,
        "evidence_job_id": EV168_JOB,
        "evidence_artifact_id": EV168_ARTIFACT,
        "evidence_artifact_digest": EV168_DIGEST,
        "evidence_head": EV168_HEAD,
        "closure_run_id": closure_run_id,
        "closure_run_url": closure_run_url,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "remediation_authorized": False,
    }

    registry["state"] = "finding_provenance_baseline_frozen"
    registry["finding_provenance_baseline"] = baseline_record
    registry["sdk_readiness"]["finding_baseline_frozen"] = True
    registry["sdk_readiness"]["finding_baseline_path"] = str(BASELINE.relative_to(ROOT))
    registry["sdk_readiness"]["finding_baseline_payload_sha256"] = payload_sha
    registry["remediation_readiness"]["baseline_freeze_complete"] = True
    registry["remediation_readiness"]["decision_phase_eligible"] = True
    registry["remediation_readiness"]["ready"] = False
    registry["remediation_readiness"]["note"] = "Finding/provenance baseline is frozen. Any official-facing remediation remains a separate explicit decision."

    state["project_phase"] = "finding_baseline_frozen"
    audit = state["audit"]
    audit["finding_baseline_freeze_ready"] = False
    audit["finding_baseline_frozen"] = True
    audit["finding_baseline_path"] = str(BASELINE.relative_to(ROOT))
    audit["finding_baseline_report"] = str(REPORT.relative_to(ROOT))
    audit["finding_baseline_payload_sha256"] = payload_sha
    audit["finding_baseline_evidence_id"] = "EV-168"
    audit["finding_baseline_evidence_run_id"] = EV168_RUN
    audit["finding_baseline_evidence_artifact_id"] = EV168_ARTIFACT
    audit["finding_baseline_evidence_artifact_digest"] = EV168_DIGEST
    audit["finding_entries_sha256"] = FINDING_ENTRIES_SHA256
    audit["finding_authority_snapshot_sha256"] = AUTHORITY_SNAPSHOT_SHA256
    audit["finding_baseline_xsd_manifest_sha256"] = XSD_MANIFEST_SHA256
    audit["audit_knowledge_phase_complete"] = True
    audit["remediation_authorized"] = False

    report = f"""# Finding / provenance baseline freeze — 2026-09-14

Status: **frozen**.

The mandatory legacy-finding revalidation and final readiness reconciliation are complete. This freeze creates the immutable audit-knowledge baseline that later SDK knowledge design or a separately authorized remediation phase must reference.

## Frozen scope

- Frozen finding inventory: **192** entries.
- Final terminal findings: **192**.
- Pending findings: **0**.
- Unresolved findings: **0** at the finding-claim level after `CIS-001` readiness reconciliation.
- Machine-readable baseline: `{BASELINE.relative_to(ROOT)}`.
- Finding-state digest: `{FINDING_ENTRIES_SHA256}`.
- Authority/provenance digest: `{AUTHORITY_SNAPSHOT_SHA256}`.
- 50-root-XSD manifest digest: `{XSD_MANIFEST_SHA256}`.
- Baseline payload digest: `{payload_sha}`.

## EV-168 freeze evidence

- Run: **{EV168_RUN}**.
- Job: **{EV168_JOB}**.
- Artifact: **{EV168_ARTIFACT}**.
- Artifact digest: `{EV168_DIGEST}`.
- Evidence head: `{EV168_HEAD}`.
- Freeze closure run: **{closure_run_id}**.
- Full 50-root-XSD regression: **PASS**.

## Authority guards retained

- `latest-wins` remains forbidden.
- Candidate/integration XSD authority is not promoted to official authority.
- CIS V1.1 has no strict release-XSD profile; its release-XSD identity remains unresolved and routing remains fail-closed.
- The selected XSD remains normative validation authority wherever a strict selected profile exists.

## Phase boundary

`finding_knowledge_ready = true` and the finding/provenance baseline is now frozen.

This **does not authorize XSD changes or official-facing remediation**. Remediation remains a separate explicit decision. SDK finding-knowledge design may reference this frozen baseline without reopening historical findings silently; any later evidence change requires an explicit new baseline/version rather than mutation of this snapshot.

No XSD, PDF source bytes, source-pin registry or original frozen finding inventory was modified by this freeze.
"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")

    # Post-write checks.
    baseline2 = load(BASELINE)
    payload2 = dict(baseline2)
    embedded = payload2.pop("baseline_payload_sha256")
    require(embedded == payload_sha == canonical_sha(payload2), "baseline payload self-digest verifies")
    registry2 = load(REGISTRY)
    state2 = load(STATE)
    require(registry2.get("state") == "finding_provenance_baseline_frozen", "registry poststate is baseline frozen")
    require(registry2["finding_provenance_baseline"].get("baseline_payload_sha256") == payload_sha, "registry points to exact baseline payload digest")
    require(registry2["sdk_readiness"].get("finding_knowledge_ready") is True, "finding knowledge remains ready")
    require(registry2["sdk_readiness"].get("finding_baseline_frozen") is True, "SDK readiness records frozen baseline")
    require(registry2["remediation_readiness"].get("ready") is False, "remediation remains unauthorized")
    require(state2.get("project_phase") == "finding_baseline_frozen", "CURRENT_STATE project phase is finding_baseline_frozen")
    require(state2["audit"].get("finding_baseline_frozen") is True, "CURRENT_STATE records frozen finding baseline")
    require(state2["audit"].get("audit_knowledge_phase_complete") is True, "audit knowledge phase is complete")
    require(state2["audit"].get("remediation_authorized") is False, "CURRENT_STATE does not authorize remediation")
    require(REPORT.is_file(), "baseline freeze report written")

    print(f"BASELINE_PAYLOAD_SHA256={payload_sha}")
    print("PASSED: finding/provenance baseline freeze prepared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
