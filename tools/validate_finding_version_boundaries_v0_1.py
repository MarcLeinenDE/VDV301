#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from jsonschema import Draft202012Validator
ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/"audit_registry/finding_version_scope_boundary_verification_v0.1.json"
SCHEMA=ROOT/"audit_registry/finding_version_scope_boundary_verification_v0.1.schema.json"
LOC=ROOT/"audit_registry/finding_source_locators_v0.1.json"
STATE=ROOT/"00_START_HERE/CURRENT_STATE.json"
def load(p): return json.loads(p.read_text(encoding="utf-8"))
def req(c,m):
    if not c: raise SystemExit("FAIL: "+m)
    print("OK  "+m)
def main():
    r,s,loc,state=load(REG),load(SCHEMA),load(LOC),load(STATE)
    errs=sorted(Draft202012Validator(s).iter_errors(r),key=lambda e:list(e.path))
    if errs: raise SystemExit("\n".join(f"{list(e.path)}: {e.message}" for e in errs))
    loc_ids=[e["finding_id"] for e in loc["entries"]]; entries=r["entries"]; ids=[e["finding_id"] for e in entries]
    req(ids==loc_ids,"boundary registry tracks locator findings in canonical order")
    req(len(ids)==len(set(ids)),"boundary registry IDs are unique")
    verified=sum(e["state"]=="verified" for e in entries); pending=sum(e["state"]=="pending_revalidation" for e in entries)
    req(r["counts"]["tracked_findings"]==len(entries),"tracked count matches")
    req(r["counts"]["verified"]==verified,"verified count matches")
    req(r["counts"]["pending_revalidation"]==pending,"pending count matches")
    pending_ids=[e["finding_id"] for e in entries if e["state"]=="pending_revalidation"]; nxt=pending_ids[0] if pending_ids else None
    req(r["next_pending_finding"]==nxt,"next pending finding matches canonical order")
    if r["state"]=="in_progress":
        req(pending>0,"in-progress registry has pending work")
        req(r["freeze"]["locator_expansion_frozen_until_pending_zero"] is True,"locator expansion frozen during retroactive pass")
        req(len(loc_ids)==r["freeze"]["baseline_locator_count"],"locator count remains at adoption baseline")
    else:
        req(pending==0,"complete registry has zero pending")
        req(r["freeze"]["locator_expansion_frozen_until_pending_zero"] is False,"complete registry releases locator expansion")
    for e in entries:
        if e["state"]=="verified":
            req(bool(e["evidence"]),f"{e['finding_id']} has boundary evidence")
            req(bool(e.get("scope_conclusion")),f"{e['finding_id']} has scope conclusion")
            req(bool(e.get("boundary_checks")),f"{e['finding_id']} has direct boundary checks")
    p=state["scope_boundary_progress"]
    req(p["tracked_findings"]==len(entries),"CURRENT_STATE tracked boundary count matches")
    req(p["verified"]==verified,"CURRENT_STATE verified boundary count matches")
    req(p["pending_revalidation"]==pending,"CURRENT_STATE pending boundary count matches")
    req(p["next_pending_finding"]==nxt,"CURRENT_STATE next boundary finding matches")
    req(p["locator_expansion_frozen"]==r["freeze"]["locator_expansion_frozen_until_pending_zero"],"CURRENT_STATE boundary freeze matches")
    if pending: req(state["project_phase"]=="version_scope_boundary_revalidation","project phase prioritizes boundary revalidation")
    print(f"PASSED: version-scope boundaries tracked={len(entries)} verified={verified} pending={pending}")
    return 0
if __name__=="__main__": raise SystemExit(main())
