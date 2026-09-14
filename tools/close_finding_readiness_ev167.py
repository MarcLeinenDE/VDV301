#!/usr/bin/env python3
"""Fail-closed final finding-knowledge readiness closure for EV-167."""
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
PLAN = Path("docs/pdf_xsd_semantic_audit/LEGACY_FINDING_REVALIDATION_PLAN.md")
CIS_REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_CIS_2026-09-03.md")
PIN_CORRECTION = Path("docs/pdf_xsd_semantic_audit/PDF_SOURCE_PIN_CORRECTION_CIS_2026-09-14.md")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_READINESS_RECONCILIATION_2026-09-14.md")
VALIDATOR = Path("tools/validate_finding_readiness_ev167.py")
XSD_POOL = Path("tools/validate_xsd_pool.py")

EXPECTED = {
    FROZEN: "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
    REGISTRY: "8635e6d6a5e3f6f9a358760d35e716a0b065b277",
    STATE: "c5b5d7f29203a23d42fe9feee54ab2c130850191",
    SOURCE_REGISTRY: "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
    SOURCE_PINS: "bc60527ddc158d967470a63d38ffd035e5ec1400",
    EVIDENCE_GATE: "969cce8b14b50ded2ca5eb745674b894428ecf1a",
    PLAN: "b8a38bd09ca6239b96981548b7cfcbd49aa4c9d5",
    CIS_REPORT: "4e871dae28db1d36c99ff0ebcb553e7178681c4f",
    PIN_CORRECTION: "ed10d5fd6f900372231891b72069f43eba0ddd87",
    VALIDATOR: "a4c13eab177a64b0f18140673c07e8ef5fdcbf63",
    XSD_POOL: "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd",
}

PINNED_EV167_RUN = "34843562886"
PINNED_EV167_JOB = "103973944657"
PINNED_EV167_ARTIFACT = "10347047619"
PINNED_EV167_DIGEST = "sha256:d978765cfbd90b5f0ab345d9f6626b3ead6c051ac3477cf6a542d6db74a36bf2"
PINNED_EV167_HEAD = "171ff38a4b9df401429749ad9c8b5133de4d2e9a"

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
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def main() -> int:
    closure_run_id = os.environ.get("CLOSURE_RUN_ID", "").strip()
    closure_run_url = os.environ.get("CLOSURE_RUN_URL", "").strip()
    require(closure_run_id.isdigit(), "CLOSURE_RUN_ID is numeric")
    require(
        closure_run_url == f"https://github.com/MarcLeinenDE/VDV301/actions/runs/{closure_run_id}",
        "CLOSURE_RUN_URL matches run id",
    )

    for path, expected in EXPECTED.items():
        require(path.is_file() and blob(path) == expected, f"exact prestate/evidence blob {path} = {expected}")
    require(not REPORT.exists(), "final readiness reconciliation report does not pre-exist")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory remains exactly 192")

    registry = load(REGISTRY)
    entries = registry["inventory"]["entries"]
    by_id = {entry["finding_id"]: entry for entry in entries}
    require(len(entries) == len(by_id) == 192, "registry contains exactly 192 unique findings")
    require(all(entry.get("revalidation_state") in TERMINAL for entry in entries), "all findings are terminal before readiness reconciliation")
    require(not any(entry.get("revalidation_state") == "pending" for entry in entries), "zero pending findings before readiness reconciliation")
    require(registry.get("next_revalidation_block") is None, "no remaining revalidation block")
    require(
        registry.get("state") == "inventory_frozen_revalidation_terminalized_readiness_pending",
        "registry is in terminalized/readiness-pending prestate",
    )
    require(by_id["CIS-001"].get("revalidation_state") == "unresolved", "CIS-001 prior terminal state is unresolved")
    require(
        by_id["CIS-001"].get("terminal_state_source") == str(CIS_REPORT),
        "CIS-001 prior terminal source is canonical CIS closure report",
    )
    unresolved_before = [entry["finding_id"] for entry in entries if entry.get("revalidation_state") == "unresolved"]
    require(unresolved_before == ["CIS-001"], f"CIS-001 is sole unresolved prestate finding, got {unresolved_before}")

    sdk = registry["sdk_readiness"]
    require(sdk.get("finding_knowledge_ready") is False, "finding knowledge is not prematurely ready")
    require(sdk.get("readiness_reconciliation_pending") == ["CIS-001"], "only CIS-001 is pending readiness reconciliation")

    state = load(STATE)
    audit = state["audit"]
    require(
        audit.get("finding_revalidation_completed_findings") == 192
        and audit.get("finding_revalidation_pending_findings") == 0,
        "CURRENT_STATE prestate is 192/0",
    )
    require(audit.get("finding_readiness_reconciliation_pending") == ["CIS-001"], "CURRENT_STATE prestate names CIS-001 readiness item")
    require(audit.get("legacy_finding_revalidation_state") == "inventory_frozen_revalidation_terminalized_readiness_pending", "CURRENT_STATE prestate awaits readiness reconciliation")

    # Reconcile the finding claim, not the unknown release-XSD identity.
    by_id["CIS-001"]["revalidation_state"] = "context_verified"
    by_id["CIS-001"]["terminal_state_source"] = str(REPORT)

    require(all(entry.get("revalidation_state") in TERMINAL for entry in entries), "all 192 findings remain terminal after reconciliation")
    require(not any(entry.get("revalidation_state") == "pending" for entry in entries), "zero pending findings after reconciliation")
    unresolved_after = [entry["finding_id"] for entry in entries if entry.get("revalidation_state") == "unresolved"]
    require(unresolved_after == [], "zero unresolved findings after claim-level reconciliation")

    authority_boundary = {
        "CIS_V1.1_publication": "official public VDV PDF, corrected permanent byte pin f9d63dd1f2e417691913e57a9c7121c90b4e781cbcd1328be681695975f59739 / 809729 bytes",
        "release_tag": "VDV-301-1.1 absent",
        "untagged_working_family": "commit 0a5228a768c7d710c40f5f99fbdce2e544d19883, CIS blob 5957e27f128a191c794b0c8081b531a07126784a; not release authority and materially behind published PDF",
        "release_xsd_identity": "still unresolved; no matching strict release profile is invented",
        "sdk_rule": "CIS V1.1 strict validation profile unavailable/fail-closed; do not substitute untagged working or neighbouring-version XSD",
    }

    registry["state"] = "inventory_frozen_revalidation_complete_finding_knowledge_ready"
    registry["sdk_readiness"]["finding_knowledge_ready"] = True
    registry["sdk_readiness"]["readiness_reconciliation_pending"] = []
    registry["sdk_readiness"]["unresolved_sdk_affecting_findings"] = []
    registry["sdk_readiness"]["strict_profile_exclusions"] = {
        "CIS_V1.1": "no confirmed matching release-tag XSD authority; fail closed / unsupported strict profile"
    }
    registry["sdk_readiness"]["readiness_evidence_id"] = "EV-167"
    registry["sdk_readiness"]["readiness_evidence_run_id"] = PINNED_EV167_RUN
    registry["sdk_readiness"]["readiness_report"] = str(REPORT)
    registry["readiness_reconciliation"] = {
        "date": "2026-09-14",
        "state": "completed",
        "evidence_id": "EV-167",
        "pinned_successful_evidence_run": PINNED_EV167_RUN,
        "pinned_successful_evidence_job": PINNED_EV167_JOB,
        "artifact_id": PINNED_EV167_ARTIFACT,
        "artifact_digest": PINNED_EV167_DIGEST,
        "evidence_head_sha": PINNED_EV167_HEAD,
        "closure_run_id": closure_run_id,
        "closure_run_url": closure_run_url,
        "finding_reconciled": "CIS-001",
        "prior_state": "unresolved",
        "final_state": "context_verified",
        "authority_boundary": authority_boundary,
        "xsd_pool_result": "PASS_50_root_XSDs",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }
    registry["remediation_readiness"]["ready"] = False
    registry["remediation_readiness"]["revalidation_complete"] = True
    registry["remediation_readiness"]["note"] = "Finding revalidation/readiness is complete; official-facing remediation still requires a separate explicit decision."

    state["project_phase"] = "finding_baseline_freeze_ready"
    audit["legacy_finding_revalidation_state"] = "complete_finding_knowledge_ready"
    audit["finding_readiness_reconciliation_pending"] = []
    audit["finding_knowledge_ready"] = True
    audit["finding_readiness_evidence_id"] = "EV-167"
    audit["finding_readiness_evidence_run_id"] = PINNED_EV167_RUN
    audit["finding_readiness_report"] = str(REPORT)
    audit["finding_baseline_freeze_ready"] = True
    audit["latest_revalidation_evidence_id"] = "EV-167"
    audit["latest_revalidation_evidence_run_id"] = closure_run_id
    audit["cis_revalidation"]["terminal_states"]["CIS-001"] = "context_verified"
    audit["cis_revalidation"]["readiness_reconciliation"] = {
        "evidence_id": "EV-167",
        "prior_state": "unresolved",
        "final_state": "context_verified",
        "release_xsd_identity": "unresolved",
        "sdk_rule": authority_boundary["sdk_rule"],
        "report": str(REPORT),
    }

    report = f"""# Finding knowledge readiness reconciliation — 2026-09-14

Status: **complete / finding knowledge ready** under the current `FINDING_EVIDENCE_GATE.md` and `LEGACY_FINDING_REVALIDATION_PLAN.md`.

## Final inventory state

- Frozen inventory: **192 findings**.
- Terminal findings: **192**.
- Pending findings: **0**.
- Remaining revalidation block: **none**.
- Final readiness evidence: **EV-167**.
- Successful EV-167 run: **{PINNED_EV167_RUN}**, job **{PINNED_EV167_JOB}**, artifact **{PINNED_EV167_ARTIFACT}**, digest `{PINNED_EV167_DIGEST}`, head `{PINNED_EV167_HEAD}`.
- Closure run: **{closure_run_id}**.
- Full XSD regression pool: **PASS (50 root XSDs)**.

## CIS-001 reconciliation

The earlier CIS closure correctly refused to promote the untagged V1.1 working schema to release authority and therefore stored `CIS-001` as `unresolved`. Final readiness reconciliation separates two questions that had been conflated:

1. **Is the exact matching official CIS V1.1 release-XSD identity known?** — **No; it remains unresolved.**
2. **Is the finding claim that the published V1.1 PDF lacks a confirmed matching release-tag XSD authority established?** — **Yes; context-verified.**

Direct EV-167 controls:

- official CIS V1.1 PDF URL: `https://www.vdv.de/301-2-3-sds-v1-1.pdfx`;
- corrected permanent PDF pin: `f9d63dd1f2e417691913e57a9c7121c90b4e781cbcd1328be681695975f59739`, **809729 bytes**;
- original source-evidence run `33736316368`, job `100587592810`, artifact `9885887536`;
- the PDF contains `SpeakerActive` and `StopInformationActive`;
- no `VDV-301-1.1` release tag is present in the checked official repository;
- untagged working commit `0a5228a768c7d710c40f5f99fbdce2e544d19883`, CIS blob `5957e27f128a191c794b0c8081b531a07126784a`, omits both published fields;
- the CIS pin registry inconsistency discovered during EV-167 was corrected separately and transparently in `PDF_SOURCE_PIN_CORRECTION_CIS_2026-09-14.md`.

Therefore `CIS-001` is reconciled from `unresolved` to **`context_verified` as a provenance-gap finding**. This does **not** claim that an official matching V1.1 XSD exists.

## SDK authority rule

```text
CIS V1.1 strict XSD profile: unavailable / fail closed.
Do not substitute the untagged V1.1 working family.
Do not substitute V1.0, V2.0 or any later CIS XSD.
Report the strict profile as unsupported because release authority is unresolved.
```

This removes the unresolved SDK routing branch without inventing schema authority. The selected XSD remains normative wherever a selected strict profile actually exists.

## Readiness result

`finding_knowledge_ready = true`.

This permits the later finding/provenance baseline freeze and SDK knowledge design. It does **not** authorize any XSD mutation or official-facing remediation. Those remain separate explicit phases.

No XSD or frozen-inventory mutation occurred.
"""

    write_json(REGISTRY, registry)
    write_json(STATE, state)
    REPORT.write_text(report, encoding="utf-8")

    # Post-write internal checks.
    registry2 = load(REGISTRY)
    state2 = load(STATE)
    entries2 = registry2["inventory"]["entries"]
    by2 = {entry["finding_id"]: entry for entry in entries2}
    require(len(entries2) == 192 and all(entry.get("revalidation_state") in TERMINAL for entry in entries2), "poststate keeps all 192 findings terminal")
    require(not any(entry.get("revalidation_state") in {"pending", "unresolved"} for entry in entries2), "poststate has zero pending and zero unresolved findings")
    require(by2["CIS-001"].get("revalidation_state") == "context_verified", "poststate reconciles CIS-001 to context_verified")
    require(registry2["sdk_readiness"].get("finding_knowledge_ready") is True, "poststate finding knowledge ready")
    require(registry2.get("next_revalidation_block") is None, "poststate has no next revalidation block")
    require(state2.get("project_phase") == "finding_baseline_freeze_ready", "poststate advances project phase to baseline-freeze ready")
    require(state2["audit"].get("finding_knowledge_ready") is True, "CURRENT_STATE records finding knowledge ready")
    require(REPORT.is_file(), "readiness reconciliation report written")

    print("PASSED: final EV-167 finding readiness closure prepared")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
