#!/usr/bin/env python3
"""Fail-closed writer for final frozen VideoRecordingService block VRS-001..011."""
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
PLAN = Path("docs/pdf_xsd_semantic_audit/LEGACY_FINDING_REVALIDATION_PLAN.md")
ADDENDUM = Path("docs/pdf_xsd_semantic_audit/VIDEO_RECORDING_SERVICE_FINDINGS_REGISTER_ADDENDUM.md")
CORRECTION = Path("docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_CHOICE_NOTATION_2026-08-29.md")
DEEP_V10 = Path("docs/pdf_xsd_semantic_audit/deep_read/VRS_V1.0.md")
DEEP_V20 = Path("docs/pdf_xsd_semantic_audit/deep_read/VRS_V2.0.md")
DEEP_V24 = Path("docs/pdf_xsd_semantic_audit/deep_read/VRS_V2.4.md")
EV103_DOC = Path("docs/pdf_xsd_semantic_audit/24c_executable_validation_video_compositors.md")
VALIDATOR = Path("tools/validate_vrs_revalidation_ev166.py")
EV103 = Path("tools/validate_video_v20_compositors.py")
XSD_POOL = Path("tools/validate_xsd_pool.py")
VRS20 = Path("IBIS-IP_VideoRecordingService_V2.0.xsd")
VRS24 = Path("IBIS-IP_VideoRecordingService_V2.4.xsd")
COMMON20 = Path("IBIS-IP_common_V2.0.xsd")
ENUM20 = Path("IBIS-IP_Enumerations_V2.0.xsd")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_VRS_2026-09-14.md")

EXPECTED = {
    FROZEN: "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
    REGISTRY: "9fa016a223052e84610d9a47e08a81a5015bcb4d",
    STATE: "5f7e232d7f8b75ea2ff85e88c108dd4646aa0ba4",
    SOURCE_REGISTRY: "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
    SOURCE_PINS: "88349638b423689799af700e8a1c8ec99bbfb67b",
    PLAN: "b8a38bd09ca6239b96981548b7cfcbd49aa4c9d5",
    ADDENDUM: "d9392d85a855717ac8041f9d34b127160244f946",
    CORRECTION: "fe024798ba1b9803ec70ee3b97def63ee03d298f",
    DEEP_V10: "f3ae1d90bfdb2f7bb65042e152b0b29a43bf0987",
    DEEP_V20: "9d0efc0fcf230955fcacab206b1d9de08d699dfd",
    DEEP_V24: "cdcec9be131ea6aa91ed32196b0f1cc32f13442a",
    EV103_DOC: "77bceaea8c3a6d4f113d9b38ba6ef4062859c6d7",
    VALIDATOR: "22ef7a87e5ae6395b7a15a96750a9eb116472bbb",
    EV103: "9c85d362a597b357a69577477bacc8dc8fcbe177",
    XSD_POOL: "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd",
    VRS20: "6ef0dae64ce6f4d3aa4f652d6d166896e71aaac7",
    VRS24: "07ff2c41731e63fd85b203e4b8e0186136caaaaf",
    COMMON20: "8608e3dcd665c197c34da7f6ec6af5a3758da164",
    ENUM20: "27e3c183b00381d959622d13c10543123af8eef6",
}
PINNED_RUN = "34840970136"
PINNED_JOB = "103965628772"
PINNED_ARTIFACT = "10346331279"
PINNED_DIGEST = "sha256:da205bc769db11a5406a11de1c2febeb6c38745924d51835fe7a22b6fd978309"
PINNED_HEAD = "8bcfbbc3e93fcc1bfc41e422cd5a83790ed99e9f"
TARGETS = {
    "VRS-001":"context_verified", "VRS-002":"context_verified", "VRS-003":"executable_confirmed",
    "VRS-004":"context_verified", "VRS-005":"context_verified", "VRS-006":"context_verified",
    "VRS-007":"withdrawn", "VRS-008":"context_verified", "VRS-009":"context_verified",
    "VRS-010":"context_verified", "VRS-011":"context_verified",
}
TERMINAL = {"context_verified","executable_confirmed","contextual_not_defect","withdrawn","unresolved","superseded"}

def req(c,m):
    if not c: raise SystemExit(f"FAIL {m}")
    print(f"OK  {m}")
def blob(p): return subprocess.check_output(["git","hash-object",str(p)], text=True).strip()
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def dump(p,d): p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
def counts(e): return (sum(x.get("revalidation_state") in TERMINAL for x in e),sum(x.get("revalidation_state")=="pending" for x in e))
def first_pending(e): return next((x["finding_id"] for x in e if x.get("revalidation_state")=="pending"),None)

def main():
    run=os.environ.get("EVIDENCE_RUN_ID","").strip(); url=os.environ.get("EVIDENCE_RUN_URL","").strip()
    req(run.isdigit(),"EVIDENCE_RUN_ID is numeric")
    req(url==f"https://github.com/MarcLeinenDE/VDV301/actions/runs/{run}","EVIDENCE_RUN_URL matches run id")
    for p,h in EXPECTED.items(): req(p.is_file() and blob(p)==h,f"exact prestate/authority blob {p} = {h}")
    req(not REPORT.exists(),"VRS closure report does not pre-exist")
    frozen=load(FROZEN); req(frozen.get("state")=="frozen" and frozen.get("entry_count")==192,"frozen inventory remains exactly 192")
    reg=load(REGISTRY); entries=reg["inventory"]["entries"]; byid={x["finding_id"]:x for x in entries}
    req(len(entries)==len(byid)==192,"registry contains exactly 192 unique findings")
    req(reg.get("next_revalidation_block")=="VRS","prestate next block is VRS")
    req(counts(entries)==(181,11),f"pre-VRS counts are 181/11, got {counts(entries)}")
    req(first_pending(entries)=="VRS-001","pre-VRS first pending is VRS-001")
    for fid in TARGETS: req(byid[fid].get("revalidation_state")=="pending" and byid[fid].get("terminal_state_source") is None,f"{fid} pending without premature source")
    req(reg.get("revalidation_blocks",{}).get("VLS",{}).get("state")=="completed","VLS is prior completed block")
    req("VRS" not in reg.get("revalidation_blocks",{}),"VRS block is not already closed")
    state=load(STATE); audit=state["audit"]
    req(audit.get("finding_revalidation_completed_findings")==181,"CURRENT_STATE pre-VRS terminal count is 181")
    req(audit.get("finding_revalidation_pending_findings")==11,"CURRENT_STATE pre-VRS pending count is 11")
    req(audit.get("finding_revalidation_next_block")=="VRS","CURRENT_STATE pre-VRS next block is VRS")
    req(audit.get("latest_revalidation_evidence_id")=="EV-165","EV-165 is prior evidence")
    for fid,s in TARGETS.items(): byid[fid]["revalidation_state"]=s; byid[fid]["terminal_state_source"]=str(REPORT)
    req(counts(entries)==(192,0),f"post-VRS counts are 192/0, got {counts(entries)}")
    req(first_pending(entries) is None,"post-VRS has no pending finding")
    unresolved=[x["finding_id"] for x in entries if x.get("revalidation_state")=="unresolved"]
    req(unresolved==["CIS-001"],f"only unresolved terminal finding is CIS-001, got {unresolved}")
    boundary={
        "VRS_V1.0":"official PDF; no exact official V1.0 service XSD confirmed; no nearby-version substitution",
        "VRS_V2.0":"official VDV-301-2.0 service/Common/Enums family",
        "VRS_V2.4":"official PDF; XSD remains open unmerged PR #27 candidate/integration only",
        "VRS-007":"withdrawn by authoritative choice-notation correction overlay",
    }
    reg["state"]="inventory_frozen_revalidation_terminalized_readiness_pending"
    reg["next_revalidation_block"]=None
    reg.setdefault("sdk_readiness",{})["finding_knowledge_ready"]=False
    reg["sdk_readiness"]["readiness_reconciliation_pending"]=["CIS-001"]
    reg.setdefault("remediation_readiness",{})["ready"]=False
    reg.setdefault("revalidation_blocks",{})["VRS"]={
        "date":"2026-09-14","state":"completed","evidence_id":"EV-166","evidence_run_id":run,"evidence_run_url":url,
        "pinned_successful_evidence_run":PINNED_RUN,"pinned_successful_evidence_job":PINNED_JOB,"artifact_id":PINNED_ARTIFACT,
        "artifact_digest":PINNED_DIGEST,"evidence_head_sha":PINNED_HEAD,"underlying_executable_evidence":["EV-103"],
        "visual_evidence_runs":["33204547867","33206290291","33207026201"],"authority_boundary":boundary,
        "findings":TARGETS,"terminal_state_source":str(REPORT),"full_xsd_regression_pool":{"root_xsd_count":50,"result":"PASS"},
        "xsd_mutation":False,"frozen_inventory_mutation":False,"next_block":None,"remaining_pending":0,
        "readiness_reconciliation_pending":["CIS-001"],
    }
    audit["legacy_finding_revalidation_state"]="inventory_frozen_revalidation_terminalized_readiness_pending"
    audit["finding_revalidation_next_block"]=None
    audit["finding_revalidation_completed_findings"]=192
    audit["finding_revalidation_pending_findings"]=0
    audit["finding_revalidation_current_block"]="VRS"
    audit["finding_revalidation_latest_completed_block"]="VRS"
    audit["finding_revalidation_latest_terminal_state_source"]=str(REPORT)
    audit["latest_revalidation_evidence_id"]="EV-166"
    audit["latest_executable_evidence_id"]="EV-166"
    audit["latest_executable_evidence_run_id"]=run
    audit["latest_executable_evidence_run"]=run
    audit["finding_revalidation_terminalization_complete"]=True
    audit["finding_readiness_reconciliation_pending"]=["CIS-001"]
    audit["vrs_revalidation"]={"status":"complete","evidence_id":"EV-166","run_id":run,"artifact_id":PINNED_ARTIFACT,
        "artifact_digest":PINNED_DIGEST,"evidence_head_sha":PINNED_HEAD,"terminal_states":TARGETS,"authority_boundary":boundary,
        "xsd_pool_result":"PASS_50_root_XSDs","pending_after":0,"readiness_reconciliation_pending":["CIS-001"],"xsd_mutation":False}
    report=f"""# Finding revalidation — VideoRecordingService (VRS)\n\nStatus: **final finding block completed** on 2026-09-14 under the current Evidence Gate.\n\n## Scope and evidence\n\nFrozen findings: `VRS-001` through `VRS-011`. EV-166 successful validation run **{PINNED_RUN}**, job **{PINNED_JOB}**, artifact **{PINNED_ARTIFACT}**, digest `{PINNED_DIGEST}`, head `{PINNED_HEAD}`. Closure run: **{run}**. EV-103 is the executable V2.0 compositor evidence for `VRS-003`. All **50 root XSDs PASS**.\n\nV1.0/V2.0/V2.4 official PDFs were reacquired byte-identically. V2.0 uses the exact official `VDV-301-2.0` XSD family. V2.4 XSD remains open, unmerged PR #27 candidate/integration evidence only.\n\n## Terminal decisions\n\n| Finding | State | Decision |\n|---|---|---|\n| VRS-001 | `context_verified` | Official V1.0 PDF exists; no exact official V1.0 VRS service-XSD release route is confirmed. No nearby version is substituted. |\n| VRS-002 | `context_verified` | Official V2.4 PDF vs open/unmerged PR #27 candidate-XSD authority gap is confirmed. |\n| VRS-003 | `executable_confirmed` | Official V2.0 PDF/XSD compositor mismatch remains; EV-103 confirms accepted/rejected shapes. |\n| VRS-004 | `context_verified` | Wrong SubscribeDisplayState headings persist through V2.0 and are corrected in V2.4. |\n| VRS-005 | `context_verified` | `PauseRecordingRRMRequestStruture` is a shared exact PDF/XSD typo-like identifier, not a mismatch; executable spelling must not be normalized. |\n| VRS-006 | `context_verified` | Broken generated subscription references are present in V1.0 and corrected from V2.0 onward. |\n| VRS-007 | `withdrawn` | The premise was false: leading `-` is valid VDV XML-choice notation. The correction overlay supersedes older Deep-Read wording. |\n| VRS-008 | `context_verified` | StopRecording prose says StopRecordingERM through V2.4; no such alias is created. |\n| VRS-009 | `context_verified` | Neighboring VLS/VDS `v1.1` reference labels are cross-document documentation errors. |\n| VRS-010 | `context_verified` | Pause request table caption has wrong role/name across all checked VRS PDFs. |\n| VRS-011 | `context_verified` | V2.4 VideoRecordingStateStructure table has a copy/paste role description error. |\n\n## Final frozen-inventory state\n\nPrestate: **181 terminal / 11 pending**.\n\nPoststate: **192 terminal / 0 pending**. There is no next revalidation block.\n\nThe frozen inventory is fully terminalized, but SDK finding-knowledge readiness is **not promoted yet**: `CIS-001` remains the sole terminal `unresolved` finding and receives a separate readiness reconciliation because the plan requires zero unresolved finding that could alter SDK accept/reject/routing behavior.\n\nNo XSD mutation. No frozen-inventory mutation.\n"""
    dump(REGISTRY,reg); dump(STATE,state); REPORT.write_text(report,encoding="utf-8")
    req(blob(FROZEN)==EXPECTED[FROZEN],"frozen inventory unchanged after write")
    req(blob(SOURCE_REGISTRY)==EXPECTED[SOURCE_REGISTRY],"PDF source registry unchanged after write")
    req(blob(SOURCE_PINS)==EXPECTED[SOURCE_PINS],"PDF source pins unchanged after write")
    req(blob(VRS20)==EXPECTED[VRS20] and blob(VRS24)==EXPECTED[VRS24],"VRS XSD authority files unchanged after write")
    print("PASSED: VRS final-block closure files prepared; expected poststate 192/0; readiness reconciliation pending CIS-001")
    return 0
if __name__=="__main__": raise SystemExit(main())
