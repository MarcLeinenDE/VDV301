#!/usr/bin/env python3
"""Validate the canonical VDV301 finding source-locator manifest."""
from __future__ import annotations
import json
import subprocess
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"audit_registry/finding_source_locators_v0.1.json"
SCHEMA=ROOT/"audit_registry/finding_source_locators_v0.1.schema.json"
SEMANTIC=ROOT/"audit_registry/finding_semantic_classification_v0.1.json"
PDF_REGISTRY=ROOT/"audit_registry/pdf_source_registry_v0.1.json"
PDF_PINS=ROOT/"audit_registry/pdf_source_pins_v0.1.json"

def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))

def git_blob(p: Path) -> str:
    return subprocess.check_output(["git","hash-object",str(p)],cwd=ROOT,text=True).strip()

def require(cond: bool,msg: str):
    if not cond:
        raise SystemExit("FAIL: "+msg)
    print("OK  "+msg)

def main() -> int:
    m=load(MANIFEST); s=load(SCHEMA); sem=load(SEMANTIC)
    pdf_registry=load(PDF_REGISTRY); pdf_pins=load(PDF_PINS)
    pdf_by_id={x["source_id"]:x for x in pdf_registry["sources"]}
    pin_by_id={x["source_id"]:x for x in pdf_pins["sources"]}
    errors=sorted(Draft202012Validator(s).iter_errors(m),key=lambda e:list(e.path))
    if errors:
        raise SystemExit("\n".join(f"{list(e.path)}: {e.message}" for e in errors))
    require(m["source_semantic_registry"]["git_blob"]==git_blob(SEMANTIC),"locator manifest pins current semantic-registry blob")
    require(len(sem["entries"])==192,"semantic registry has 192 findings")
    by={e["finding_id"]:e for e in sem["entries"]}
    order={e["finding_id"]:i for i,e in enumerate(sem["entries"])}
    ids=[e["finding_id"] for e in m["entries"]]
    require(len(ids)==len(set(ids)),"locator entries use unique finding IDs")
    require(all(i in by for i in ids),"all locator entries refer to semantic findings")
    require(ids==sorted(ids,key=lambda i:order[i]),"locator entries follow semantic finding order")
    for e in m["entries"]:
        src=by[e["finding_id"]]
        require(e["service"]==src["service"],f"{e['finding_id']} service matches semantic registry")
        require(e["scope_claims"]==src["version_scope"],f"{e['finding_id']} scope_claims exactly match semantic version_scope")
        versions=[c["version"] for c in e["coverage"]]
        require(len(versions)==len(set(versions)),f"{e['finding_id']} coverage versions are unique")
        if e["coverage_state"]=="complete":
            require(all(c["coverage_status"]=="complete" for c in e["coverage"]),f"{e['finding_id']} complete entry has no partial coverage lane")
        for c in e["coverage"]:
            require(c["pdf_locators"] or c["xsd_locators"],f"{e['finding_id']} {c['version']} has at least one direct locator")
            for p_loc in c["pdf_locators"]:
                sid=p_loc["source_id"]
                require(sid in pdf_by_id,f"{e['finding_id']} PDF source is registered: {sid}")
                require(sid in pin_by_id,f"{e['finding_id']} PDF source is byte-pinned: {sid}")
                require(pdf_by_id[sid]["official_url"]==p_loc["url"],f"{e['finding_id']} PDF official URL matches registry: {sid}")
                require(str(pdf_by_id[sid]["version"])==p_loc["document_version"],f"{e['finding_id']} PDF version matches registry: {sid}")
                require(pin_by_id[sid]["expected_sha256"]==p_loc["sha256"],f"{e['finding_id']} PDF SHA-256 matches pin registry: {sid}")
            for x in c["xsd_locators"]:
                p=ROOT/x["file"]
                require(p.is_file(),f"{e['finding_id']} XSD exists: {x['file']}")
                require(git_blob(p)==x["git_blob"],f"{e['finding_id']} XSD blob matches: {x['file']}")
    counts=m["counts"]
    require(counts["locator_entry_count"]==len(m["entries"]),"locator_entry_count matches entries")
    require(counts["coverage_complete_count"]==sum(e["coverage_state"]=="complete" for e in m["entries"]),"complete count matches")
    require(counts["coverage_partial_count"]==sum(e["coverage_state"]=="partial" for e in m["entries"]),"partial count matches")
    require(counts["remaining_finding_count"]==192-len(m["entries"]),"remaining count matches 192-finding target")
    if m["state"]=="complete":
        require(len(m["entries"])==192,"complete locator manifest covers all 192 findings")
    print(f"PASSED: source locators valid; entries={len(ids)} complete={counts['coverage_complete_count']} remaining={counts['remaining_finding_count']}")
    return 0

if __name__=="__main__":
    raise SystemExit(main())
