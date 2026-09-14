#!/usr/bin/env python3
"""Final fail-closed finding-knowledge readiness gate after all 192 frozen findings are terminal.

EV-167 does not alter CIS-001's terminal state. It determines whether the sole unresolved
finding still leaves SDK accept/reject/routing behaviour ambiguous. The required safe rule
is fail-closed: no strict CIS V1.1 validation profile is exposed unless a published release
authority can be established.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
FROZEN=ROOT/"audit_registry/finding_inventory_frozen_2026-09-03.json"
REGISTRY=ROOT/"audit_registry/finding_revalidation_registry_v0.1.json"
STATE=ROOT/"00_START_HERE/CURRENT_STATE.json"
SOURCE_REGISTRY=ROOT/"audit_registry/pdf_source_registry_v0.1.json"
SOURCE_PINS=ROOT/"audit_registry/pdf_source_pins_v0.1.json"
EVIDENCE_GATE=ROOT/"docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md"
PLAN=ROOT/"docs/pdf_xsd_semantic_audit/LEGACY_FINDING_REVALIDATION_PLAN.md"
CIS_REPORT=ROOT/"docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_CIS_2026-09-03.md"
XSD_POOL=ROOT/"tools/validate_xsd_pool.py"
EXPECTED={
 FROZEN:"02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
 REGISTRY:"8635e6d6a5e3f6f9a358760d35e716a0b065b277",
 STATE:"c5b5d7f29203a23d42fe9feee54ab2c130850191",
 SOURCE_REGISTRY:"d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
 SOURCE_PINS:"88349638b423689799af700e8a1c8ec99bbfb67b",
 EVIDENCE_GATE:"969cce8b14b50ded2ca5eb745674b894428ecf1a",
 PLAN:"b8a38bd09ca6239b96981548b7cfcbd49aa4c9d5",
 CIS_REPORT:"4e871dae28db1d36c99ff0ebcb553e7178681c4f",
 XSD_POOL:"7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd",
}
TERMINAL={"context_verified","executable_confirmed","contextual_not_defect","withdrawn","unresolved","superseded"}
CIS_PDF_SHA="89080a41da387270ecac5b228df6aa4903ccb123a0d37e9e73cd98396786931b"
CIS_PDF_SIZE=985025
CIS_PDF_URL="https://www.vdv.de/301-2-3-sds-v1-1.pdfx"
WORKING_COMMIT="0a5228a768c7d710c40f5f99fbdce2e544d19883"
WORKING_CIS_BLOB="5957e27f128a191c794b0c8081b531a07126784a"

def req(c,m):
 if not c: raise SystemExit(f"FAIL {m}")
 print(f"OK  {m}")
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def blob(p): return subprocess.check_output(["git","hash-object",str(p)],cwd=ROOT,text=True).strip()
def sha256(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for chunk in iter(lambda:f.read(1024*1024),b""): h.update(chunk)
 return h.hexdigest()
def tokens(p,vals,label):
 t=p.read_text(encoding="utf-8")
 for v in vals: req(v in t,f"{label} contains authoritative token: {v}")

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--cis-v11-pdf",required=True,type=Path); ap.add_argument("--output",required=True,type=Path); a=ap.parse_args()
 for p,h in EXPECTED.items(): req(p.is_file() and blob(p)==h,f"exact blob {p.relative_to(ROOT)} = {h}")
 frozen=load(FROZEN); req(frozen.get("state")=="frozen" and frozen.get("entry_count")==192,"frozen inventory remains 192")
 reg=load(REGISTRY); entries=reg["inventory"]["entries"]; by={x["finding_id"]:x for x in entries}
 req(len(entries)==len(by)==192,"registry has 192 unique findings")
 req(sum(x.get("revalidation_state") in TERMINAL for x in entries)==192,"all 192 findings are terminal")
 req(sum(x.get("revalidation_state")=="pending" for x in entries)==0,"zero pending findings")
 req(reg.get("next_revalidation_block") is None,"no next revalidation block")
 req(reg.get("state")=="inventory_frozen_revalidation_terminalized_readiness_pending","registry awaits readiness reconciliation")
 unresolved=[x["finding_id"] for x in entries if x.get("revalidation_state")=="unresolved"]
 req(unresolved==["CIS-001"],f"CIS-001 is sole unresolved terminal finding, got {unresolved}")
 req(by["CIS-001"].get("terminal_state_source")==str(CIS_REPORT.relative_to(ROOT)),"CIS-001 points to canonical CIS closure report")
 sdk=reg["sdk_readiness"]
 req(sdk.get("finding_knowledge_ready") is False,"finding knowledge is not prematurely ready")
 req(sdk.get("readiness_reconciliation_pending")==["CIS-001"],"only CIS-001 awaits readiness reconciliation")
 st=load(STATE)["audit"]
 req(st.get("finding_revalidation_completed_findings")==192 and st.get("finding_revalidation_pending_findings")==0,"CURRENT_STATE is 192/0")
 req(st.get("finding_readiness_reconciliation_pending")==["CIS-001"],"CURRENT_STATE names CIS-001 as readiness item")
 tokens(CIS_REPORT,[
  "Official Git history contains an untagged V1.1 working family at `0a5228a…`",
  "there is no `VDV-301-1.1` release tag",
  "lacks published-PDF fields `SpeakerActive` and `StopInformationActive`",
  "cannot be promoted to a strict published V1.1 release authority",
 ],"CIS closure report")
 tokens(PLAN,[
  "zero pending findings",
  "zero unresolved finding that could alter SDK accept/reject/routing behavior",
  "The selected XSD version remains the hard validation authority.",
 ],"revalidation plan")
 sources=load(SOURCE_REGISTRY); src=next(x for x in sources["sources"] if x["source_id"]=="CIS_V1.1")
 pins=load(SOURCE_PINS); pin=next(x for x in pins["sources"] if x["source_id"]=="CIS_V1.1")
 req(src.get("official_url")==CIS_PDF_URL,"CIS V1.1 official PDF URL pinned")
 req(pin.get("expected_sha256")==CIS_PDF_SHA and pin.get("expected_size_bytes")==CIS_PDF_SIZE,"CIS V1.1 PDF hash/size pinned")
 req(str(pin.get("evidence_run_id"))=="33736316368","CIS V1.1 source evidence run pinned")
 req(a.cis_v11_pdf.is_file() and a.cis_v11_pdf.stat().st_size==CIS_PDF_SIZE and sha256(a.cis_v11_pdf)==CIS_PDF_SHA,"fresh CIS V1.1 PDF bytes match permanent pin")
 resolution={
  "finding_id":"CIS-001",
  "terminal_state_preserved":"unresolved",
  "sdk_affecting_unresolved":False,
  "sdk_policy":"no_strict_cis_v1_1_profile_fail_closed",
  "routing_rule":"CIS V1.1 published PDF has no confirmed matching release-tag XSD; do not substitute untagged working or nearby-version XSD; report profile authority unresolved/unsupported",
  "working_commit":WORKING_COMMIT,
  "working_cis_blob":WORKING_CIS_BLOB,
  "reason":"The unresolved provenance question no longer creates an SDK branch choice because the only permitted rule is to expose no strict validation profile for CIS V1.1.",
 }
 out={"evidence_id":"EV-167","prestate":{"terminal":192,"pending":0,"finding_knowledge_ready":False},"cis_001_readiness_resolution":resolution,"projected_readiness":{"finding_knowledge_ready":True,"unresolved_sdk_affecting_findings":[],"non_sdk_affecting_unresolved_findings":["CIS-001"]},"xsd_mutation":False,"frozen_inventory_mutation":False}
 a.output.parent.mkdir(parents=True,exist_ok=True); a.output.write_text(json.dumps(out,indent=2)+"\n",encoding="utf-8")
 print(f"PASSED: EV-167 final finding-knowledge readiness gate; wrote {a.output}")
 return 0
if __name__=="__main__": raise SystemExit(main())
