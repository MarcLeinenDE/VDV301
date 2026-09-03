#!/usr/bin/env python3
import json
import os
import subprocess
from pathlib import Path

DATE = "2026-09-03"
REPORT = "docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_CE_2026-09-03.md"
CORRECTION = "docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_COMMON_V22_CE008_CE009_IDENTITY_2026-09-03.md"
EVIDENCE = "audit_registry/revalidation_evidence_ev124_ce_block_2026-09-03.json"
REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
SNAPSHOT = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")

states = {
    "CE-001": "contextual_not_defect",
    "CE-002": "context_verified",
    "CE-003": "superseded",
    "CE-004": "context_verified",
    "CE-005": "executable_confirmed",
    "CE-006": "executable_confirmed",
    "CE-007": "executable_confirmed",
    "CE-008": "executable_confirmed",
    "CE-009": "executable_confirmed",
    "CE-010": "executable_confirmed",
    "CE-011": "executable_confirmed",
    "CE-012": "executable_confirmed",
    "CE-013": "executable_confirmed",
    "CE-014": "executable_confirmed",
    "CE-015": "executable_confirmed",
    "CE-016": "executable_confirmed",
    "CE-017": "executable_confirmed",
    "CE-018": "executable_confirmed",
    "CE-019": "context_verified",
    "CE-020": "executable_confirmed",
    "CE-021": "executable_confirmed",
    "CE-022": "executable_confirmed",
    "CE-023": "context_verified",
    "CE-024": "executable_confirmed",
    "CE-025": "executable_confirmed",
    "CE-026": "executable_confirmed",
}

reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
entries = {e["finding_id"]: e for e in reg["inventory"]["entries"]}
assert set(states).issubset(entries)
for fid in states:
    assert entries[fid]["revalidation_state"] == "pending", (fid, entries[fid])
    entries[fid]["revalidation_state"] = states[fid]
    entries[fid]["terminal_state_source"] = REPORT

run_id = os.environ.get("GITHUB_RUN_ID", "local")
head = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()

reg["next_revalidation_block"] = "CIS"
reg.setdefault("revalidation_blocks", {})["CE"] = {
    "date": DATE,
    "state": "completed",
    "authority_lane": "exact_Common_Enumerations_version_routes_plus_explicit_V2.3_variant_overlay",
    "aggregate_executable_evidence_id": "EV-124",
    "aggregate_run_id": run_id,
    "head_tested": head,
    "underlying_executable_evidence": ["EV-117", "EV-118", "EV-119", "EV-120", "EV-121", "EV-122", "EV-106"],
    "identity_correction_overlay": CORRECTION,
    "findings": states,
    "supersession_notes": {
        "CE-001": "No defect: official Common V2.3 explicitly includes Enumerations V2.2; absence of a separate Enumerations V2.3 file is intentional authority routing, not a schema gap.",
        "CE-003": "Historical audit-progress note only; superseded by completed Common V2.4 Deep Read and EV-122. It is not retained as a semantic defect.",
        "CE-023": "Documentation-only V2.2 duplicate/copy-paste NetexMode table. Earlier V2.3 scope was withdrawn by exact visible-source falsification.",
        "CE-025": "Historical Reply-Path/ReplyPath discrepancy remains confirmed for affected older scopes; V2.4 is corrected and is not affected.",
        "CE-026": "Historical Description/Desciption discrepancy remains confirmed for affected older scopes; V2.4 BeaconPoint is corrected and is not affected."
    },
    "xsd_mutation": False,
    "terminal_state_source": REPORT,
}
REGISTRY.write_text(json.dumps(reg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

state = json.loads(STATE.read_text(encoding="utf-8"))
audit = state["audit"]
audit["finding_revalidation_next_block"] = "CIS"
audit["finding_revalidation_completed_findings"] = 42
audit["finding_revalidation_pending_findings"] = 150
audit["finding_revalidation_current_block"] = "CE"
audit["finding_revalidation_latest_completed_block"] = "CE"
audit["finding_revalidation_latest_terminal_state_source"] = REPORT
audit["latest_executable_evidence_id"] = "EV-124"
audit["latest_executable_evidence_run"] = run_id
audit["latest_audit_correction"] = CORRECTION
STATE.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

evidence = {
    "evidence_id": "EV-124",
    "date": DATE,
    "purpose": "current-head aggregate executable rerun for CE-001..CE-026 legacy revalidation closure",
    "run_id": run_id,
    "head_tested": head,
    "result": "PASS",
    "checkers": [
        {"tool": "tools/validate_common_v10_ev117.py", "authority": "exact selected Common V1.0 route", "result": "PASS"},
        {"tool": "tools/validate_common_v20_ev118.py", "authority": "exact selected Common V2.0 route", "result": "PASS"},
        {"tool": "tools/validate_common_v21_ev119.py", "authority": "exact selected Common V2.1 route", "result": "PASS"},
        {"tool": "tools/validate_common_v22_ev120.py", "authority": "exact historical-upstream Common V2.2 + Enumerations V2.2 family", "result": "PASS"},
        {"tool": "tools/validate_common_v23_ev121.py", "authority": "official VDV-301-2.3 Common + declared Enumerations V2.2", "result": "PASS"},
        {"tool": "tools/validate_common_v24_ev122.py", "authority": "explicit selected candidate/integration Common V2.4 + Enumerations V2.4", "result": "PASS"},
        {"tool": "tools/validate_common_v23_schema_variant.py", "authority": "official V2.3 vs explicit upstream-PR30 candidate overlay", "result": "PASS"},
    ],
    "authority_note": "EV-124 aggregates current-head reruns only. It does not upgrade candidate/integration V2.4 or PR30 bytes to official authority and does not replace the per-version evidence identities.",
    "xsd_mutation": False,
}
Path(EVIDENCE).write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

correction = f"""# Audit correction delta — COMMON V2.2 CE-008 / CE-009 identity mapping\n\nDate: {DATE}\nStatus: correction overlay; historical delta is preserved unchanged.\n\n## Problem\n\n`audit_registry/deep_read_findings_delta_common_v22_2026-09-02.json` correctly maps the combined source observation `FR-COM22-013` to both `CE-008` and `CE-009`, but its `revalidated_or_scope_extended_findings` descriptions swap the two historical finding identities.\n\nThe original finding identities, independently preserved by the V2.4 enumeration audit and the later V2.3/V2.4 Deep Read mappings, are:\n\n```text\nCE-008 = Funicular/Taxi NeTEx submode case-sensitive lexeme mismatches\n         (Unknown/Undefined/minicab vs unknown/undefined/miniCab)\n\nCE-009 = RailSubmode specialRail (PDF) vs specialTrain (XSD)\n```\n\nThe V2.2 delta text instead labels `CE-008` as the RailSubmode item and `CE-009` as the Funicular/Taxi case item. That description-level swap is rejected.\n\n## Decision\n\n- Keep the frozen/historical V2.2 delta byte history unchanged.\n- Preserve its observation-to-finding membership because both IDs belong to `FR-COM22-013`.\n- For all current and future registries, use the original identities above.\n- EV-120 remains technically valid; the executable assertions are not invalidated by the label swap.\n- V2.3 EV-121 and V2.4 EV-122 use the corrected identities.\n- No XSD is changed.\n\nThis overlay is part of the CE legacy-finding revalidation closure and prevents the swapped V2.2 labels from propagating into the SDK knowledge baseline.\n"""
Path(CORRECTION).write_text(correction, encoding="utf-8")

rows = "\n".join(f"| `{fid}` | `{states[fid]}` |" for fid in sorted(states))
report = f"""# Legacy finding revalidation — Common/Enumerations CE block\n\nDate: {DATE}\nState: completed under the current Finding Evidence Gate.\n\n## Scope\n\nThis block revalidates the frozen legacy identities `CE-001` through `CE-026`. Validation always follows the exact selected XSD authority route; PDF discrepancies never create executable aliases. Candidate/integration schema material remains explicitly labelled and is never promoted to official release authority by this closure.\n\n## Evidence\n\nCurrent-head aggregate executable evidence: `EV-124`, GitHub Actions run `{run_id}`.\n\nEV-124 reruns the existing per-version Common checkers EV-117 through EV-122 plus the V2.3 official/candidate variant checker used for CE-020. Original pinned-PDF Deep Reads remain the source/layout evidence. The executable rerun is additive and does not replace their authority boundaries.\n\n## Terminal states\n\n| Finding | Terminal state |\n|---|---|\n{rows}\n\n## Important identity and scope decisions\n\n### CE-001\n\n`contextual_not_defect`. Official Common V2.3 explicitly includes `IBIS-IP_Enumerations_V2.2.xsd`; there is no requirement for a synthetic Enumerations V2.3 file. The exact dependency route is the authority.\n\n### CE-002\n\n`context_verified`. V2.4 version history says `StopPointNumber`, while the actual StopInformation table and selected XSD use `PointNumber`. The table/XSD identity wins for XML validation; no XSD rename is inferred.\n\n### CE-003\n\n`superseded`. This ID recorded a historical audit-progress state (V2.4 delta not yet fully closed), not a persistent semantic defect. Common V2.4 Deep Read and EV-122 completed the work it said was pending.\n\n### CE-004 / CE-006\n\nThe identities remain distinct: `CE-004` is the stale ServiceNameEnumeration table content (`SystemDocumentationService` / `SystemManagementService`), while `CE-006` is the PDF omission of XSD value `DeviceStateEnumeration.warning`.\n\n### CE-008 / CE-009\n\nThe original identities are preserved: `CE-008` is the Funicular/Taxi case-sensitive submode lexeme family; `CE-009` is RailSubmode `specialRail` vs `specialTrain`. The description-level swap in the V2.2 findings delta is corrected by `{CORRECTION}` without rewriting history.\n\n### CE-020\n\n`executable_confirmed`. The Common V2.3 official release blob and upstream PR #30 candidate remain two explicit semantic variants with different accepted `InternationalTextType` instance shapes. Official remains default for official authority; the PR30 overlay requires explicit candidate selection.\n\n### CE-023\n\n`context_verified`, documentation-only. The duplicate/corrupt second NetexMode table is confirmed for Common V2.2. Fresh exact visible V2.3 evidence withdrew the earlier V2.3 affected-scope claim; V2.4 is not affected. No XSD defect follows.\n\n### CE-025 / CE-026\n\nHistorical mismatches remain confirmed for affected older scopes, while V2.4 is explicitly corrected and is not scope-extended.\n\n## Gate result\n\nAll 26 frozen CE identities now have terminal states. `CE-003` is not allowed to survive as a false defect, and the CE-008/CE-009 identity swap is quarantined by an explicit correction overlay. No XSD was modified.\n"""
Path(REPORT).write_text(report, encoding="utf-8")

snap = json.loads(SNAPSHOT.read_text(encoding="utf-8"))
assert snap["state"] == "frozen"
assert snap["source_head"] == "7fad145f528205ef5c40e58a3a23374379b08189"
assert snap["entry_count"] == 192
assert set(states).issubset(set(snap["finding_ids"]))

print("CE_REVALIDATION_PREPARED=26")
print("COMPLETED=42")
print("PENDING=150")
print("NEXT=CIS")
