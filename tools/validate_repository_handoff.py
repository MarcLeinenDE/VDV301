#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MARKER="<!-- NON_CANONICAL_CONTINUATION_DOCUMENT -->"
LEGACY=["docs/pdf_xsd_semantic_audit/00_index.md","docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF.md","docs/pdf_xsd_semantic_audit/AUDIT_SCOPE_MATRIX.md","docs/pdf_xsd_semantic_audit/findings.md","docs/pdf_xsd_semantic_audit/validation_backlog.md","docs/superbranch_status.md"]
CANON=["00_START_HERE/README.md","00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md","00_START_HERE/CURRENT_STATE.json","00_START_HERE/HANDOFF_INTEGRITY_POLICY.md"]
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def req(c,m):
    if not c: raise SystemExit("FAIL: "+m)
    print("OK  "+m)
def blob(p): return subprocess.check_output(["git","hash-object",str(p)],cwd=ROOT,text=True).strip()
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--handoff-only",action="store_true")
    parser.parse_args()
    for p in CANON: req((ROOT/p).is_file(),f"canonical restart document exists: {p}")
    state=load(ROOT/"00_START_HERE/CURRENT_STATE.json"); loc=load(ROOT/"audit_registry/finding_source_locators_v0.1.json"); sem=ROOT/"audit_registry/finding_semantic_classification_v0.1.json"; body=load(ROOT/"audit_registry/pdf_locator_body_verification_v0.1.json"); runtime=load(ROOT/"sdk_manifest/known_issues_runtime_mapping_v0.1.json"); manifest=load(ROOT/"sdk_manifest/manifest_v0.1.json"); boundary=load(ROOT/"audit_registry/finding_version_scope_boundary_verification_v0.1.json")
    req(state["canonical_branch"]=="dev/schema-integration","canonical branch is dev/schema-integration")
    h=state["handoff_integrity"]; req(h["policy"]=="00_START_HERE/HANDOFF_INTEGRITY_POLICY.md","handoff policy pointer is canonical"); req(h["post_prompt_check_required"] is True,"post-prompt check is mandatory"); req(h["canonical_restart_documents"]==CANON,"canonical restart list is exact"); req(h["legacy_control_documents_noncanonical"]==LEGACY,"legacy-control list is exact")
    req(h["work_cycle_state"] in ("gate_pending","terminal_clean"),"work-cycle state recognized")
    parent_ready=subprocess.run(["git","rev-parse","--verify","HEAD^"],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0
    changed=subprocess.check_output(["git","diff-tree","--root","--no-commit-id","--name-only","-r","HEAD"],cwd=ROOT,text=True).splitlines() if parent_ready else []
    if not parent_ready: req(True,"shallow full-checkout: commit-level guard delegated to depth-2 every-push handoff workflow")
    external=[p for p in changed if p!="00_START_HERE/CURRENT_STATE.json"]
    if external:
        req("00_START_HERE/CURRENT_STATE.json" in changed,"every substantive commit updates CURRENT_STATE in same commit")
        if any(p!="sdk_manifest/manifest_v0.1.json" for p in external):
            req(h["work_cycle_state"]=="gate_pending","substantive commit uses recoverable gate_pending")
    if h["work_cycle_state"]=="gate_pending":
        for field in ("pending_block","active_finding","active_step","next_step","recovery_instruction","resume_instruction"):
            minimum=1 if field=="active_finding" else 12
            req(isinstance(h.get(field),str) and len(h[field].strip())>=minimum,f"gate_pending {field} actionable")
        req(isinstance(h.get("evidence_refs"),list) and len(h["evidence_refs"])>0,"gate_pending evidence references present")
    if h["work_cycle_state"]=="terminal_clean":
        req(h["pending_gate"] is False,"terminal-clean has no pending gate")
        req(state["workflow_mode"]=="full_gate_on_canonical_changes_plus_handoff_check_on_every_push","terminal-clean workflow mode is final")
    else:
        req(h["pending_gate"] is True,"gate-pending explicitly marks pending gate")
        req(bool(h["pending_block"]) and bool(h["recovery_instruction"]),"gate-pending state is recoverable")
        req(state["workflow_mode"] in ("handoff_bootstrap_pending","full_gate_on_canonical_changes_plus_handoff_check_on_every_push"),"pending bootstrap workflow mode recognized")
    for p in LEGACY: req((ROOT/p).read_text(encoding="utf-8").startswith(MARKER),f"legacy control doc marked non-canonical: {p}")
    req((ROOT/"README.md").read_text(encoding="utf-8").startswith("<!-- VDV301_AUDIT_BRANCH_NOTICE -->"),"root README redirects audit branch to START_HERE")
    start=(ROOT/"00_START_HERE/README.md").read_text(encoding="utf-8"); req("HANDOFF_INTEGRITY_POLICY.md" in start,"START_HERE includes handoff policy"); req("VERSION_SCOPE_BOUNDARY_POLICY.md" in start,"START_HERE includes boundary policy")
    contract=(ROOT/"00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md").read_text(encoding="utf-8"); req("Prompt-cycle durability and repository hygiene" in contract,"contract has prompt-cycle rule"); req("Version-scope boundary hard gate" in contract,"contract has boundary hard gate")
    semblob=blob(sem); req(loc["source_semantic_registry"]["git_blob"]==semblob,"locator pins current semantic registry"); req(runtime["source_semantic_registry"]["git_blob"]==semblob,"runtime mapping pins current semantic registry")
    count=len(loc["entries"]); complete=sum(e["coverage_state"]=="complete" for e in loc["entries"]); partial=sum(e["coverage_state"]=="partial" for e in loc["entries"]); remaining=192-count
    req(body["counts"]["tracked_findings"]==count,"body registry tracks locator entries")
    for name in ("audit","sdk"):
        sec=state[name]; req(sec["source_locator_entry_count"]==count,f"{name} locator count matches"); req(sec["source_locator_complete_count"]==complete,f"{name} complete count matches"); req(sec["source_locator_partial_count"]==partial,f"{name} partial count matches"); req(sec["source_locator_remaining_count"]==remaining,f"{name} remaining count matches")
    k=manifest["known_issues_knowledge"]; req(k["source_locator_entry_count"]==count,"SDK manifest locator count matches"); req(k["source_locator_latest_review_block"]==state["audit"]["source_locator_latest_review_block"],"SDK manifest latest locator review matches"); req(k["source_locator_latest_review_report"]==state["audit"]["source_locator_latest_review_report"],"SDK manifest latest locator report matches"); req(k["source_locator_latest_gate_run_id"]==state["audit"]["source_locator_latest_gate_run_id"],"SDK manifest latest locator gate matches")
    bp=state["scope_boundary_progress"]; req(boundary["counts"]["tracked_findings"]==bp["tracked_findings"],"boundary tracked count sync"); req(boundary["counts"]["verified"]==bp["verified"],"boundary verified count sync"); req(boundary["counts"]["pending_revalidation"]==bp["pending_revalidation"],"boundary pending count sync"); req(boundary["next_pending_finding"]==bp["next_pending_finding"],"boundary next sync")
    req(k["version_scope_boundary_tracked_count"]==bp["tracked_findings"],"SDK manifest boundary tracked count matches"); req(k["version_scope_boundary_verified_count"]==bp["verified"],"SDK manifest boundary verified count matches"); req(k["version_scope_boundary_pending_count"]==bp["pending_revalidation"],"SDK manifest boundary pending count matches")
    for section in ("audit","sdk"):
        for key,bp_key in (("version_scope_boundary_tracked_count","tracked_findings"),("version_scope_boundary_verified_count","verified"),("version_scope_boundary_pending_count","pending_revalidation")):
            req(state[section][key]==bp[bp_key],f"{section} {key} matches canonical boundary count")
    if bp["pending_revalidation"]>0:
        req(bp["locator_expansion_frozen"] is True,"locator expansion frozen for boundary backlog"); req(state["project_phase"]=="version_scope_boundary_revalidation","boundary phase active")
    full=(ROOT/".github/workflows/schema-audit-validation.yml").read_text(encoding="utf-8"); hw=ROOT/".github/workflows/handoff-integrity.yml"
    req("validate_repository_handoff.py" in full,"full workflow runs handoff validator"); req("validate_finding_version_boundaries_v0_1.py" in full,"full workflow runs boundary validator"); req(hw.is_file(),"handoff-integrity workflow exists")
    hand=hw.read_text(encoding="utf-8"); req("push:" in hand and "dev/schema-integration" in hand and "validate_repository_handoff.py --handoff-only" in hand,"handoff workflow covers every canonical push")
    req(state["audit"].get("next_project_phase")!="legacy_finding_revalidation","stale next-project-phase pointer removed"); req("40 existing locator findings" not in state["audit"].get("latest_source_locator_rule",""),"stale visible-body freeze pointer removed")
    print("PASSED: repository handoff state is self-contained and internally consistent")
    return 0
if __name__=="__main__": raise SystemExit(main())
