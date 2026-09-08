#!/usr/bin/env python3
"""One-shot fail-closed JIS EV-152 registry closure. Removed by its workflow after success."""
from __future__ import annotations

import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REG = ROOT / "audit_registry/finding_revalidation_registry_v0.1.json"
STATE = ROOT / "00_START_HERE/CURRENT_STATE.json"
EVIDENCE = ROOT / "audit_registry/jis_revalidation_evidence_2026-09-08.json"
REPORT = ROOT / "docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_JIS_2026-09-08.md"
EXPECTED_STATES = {
    "JIS-001": "contextual_not_defect",
    "JIS-002": "contextual_not_defect",
    "JIS-003": "executable_confirmed",
    "JIS-004": "context_verified",
    "JIS-005": "executable_confirmed",
}


def main() -> int:
    d = json.loads(REG.read_text(encoding="utf-8"))
    s = json.loads(STATE.read_text(encoding="utf-8"))
    e = json.loads(EVIDENCE.read_text(encoding="utf-8"))
    run_id = os.environ["CLOSURE_RUN_ID"]
    run_url = os.environ["CLOSURE_RUN_URL"]

    assert e["evidence_id"] == "EV-152" and e["result"] == "PASS"
    assert e["scope"] == list(EXPECTED_STATES)
    assert e["successful_run_id"] == "34113437268"
    assert e["successful_job_id"] == "101714662141"
    assert e["head_sha"] == "4da900b4acf993b14bdfbe5f48e0fb386fbad3fe"
    assert e["artifact_id"] == "10015273758"
    assert e["artifact_digest"] == "sha256:338e3fb679a8375c98fba359a3478d4cf7ba0968f3e97c08209ce52c0d23dc65"
    assert e["authority"]["xsd_route"] == "JIS V1.0 -> Common V1.0 -> Enumerations V1.0"
    assert e["authority"]["pdf"]["sha256"] == "424181b4932e18b6ac059843fa3978fdcc07a9c6acb553f9fbe8b71ef583da73"
    assert e["authority"]["pdf"]["size_bytes"] == 772125
    assert e["full_xsd_pool"] == {"count": 50, "result": "PASS"}
    assert e["fresh_visual_evidence"]["manual_visual_review_completed"] is True
    assert e["fresh_visual_evidence"]["manual_visual_review_result"] == "PASS"
    assert e["fresh_visual_evidence"]["physical_pages"] == [9, 11, 12, 13, 17, 19, 22]
    assert e["prestate"]["terminal"] == 127 and e["prestate"]["pending"] == 65
    assert e["prestate"]["expected_poststate_if_closed"] == {
        "terminal": 132, "pending": 60, "first_pending": "LS-001"
    }
    assert e["immutable_guards"]["frozen_inventory_blob"] == "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
    assert e["immutable_guards"]["frozen_inventory_mutated"] is False
    assert e["immutable_guards"]["xsd_mutated"] is False
    assert e["failed_closed_attempt"]["substantive_finding_contradiction"] is False
    assert e["failed_closed_attempt"]["behavior_changed"] is False
    for fid, terminal_state in EXPECTED_STATES.items():
        assert e["finding_results"][fid]["recommended_terminal_state"] == terminal_state
    assert e["finding_results"]["JIS-003"]["positive_one_line"] is True
    assert e["finding_results"]["JIS-003"]["negative_two_lines"] is False
    assert e["finding_results"]["JIS-005"]["positive_xsd_element_name"] is True
    assert e["finding_results"]["JIS-005"]["negative_pdf_row_name"] is False

    inv = d["inventory"]
    entries = inv["entries"]
    assert inv["state"] == "frozen" and inv["entry_count"] == 192 and len(entries) == 192
    assert d["next_revalidation_block"] == "JIS"
    pre_terminal = sum(x["revalidation_state"] != "pending" for x in entries)
    pre_pending = sum(x["revalidation_state"] == "pending" for x in entries)
    assert (pre_terminal, pre_pending) == (127, 65), (pre_terminal, pre_pending)
    by_id = {x["finding_id"]: x for x in entries}
    for fid, terminal_state in EXPECTED_STATES.items():
        assert by_id[fid]["revalidation_state"] == "pending"
        assert by_id[fid]["terminal_state_source"] is None
        by_id[fid]["revalidation_state"] = terminal_state
        by_id[fid]["terminal_state_source"] = str(REPORT.relative_to(ROOT))

    post_terminal = sum(x["revalidation_state"] != "pending" for x in entries)
    post_pending = sum(x["revalidation_state"] == "pending" for x in entries)
    assert (post_terminal, post_pending) == (132, 60), (post_terminal, post_pending)
    first_pending = next(x["finding_id"] for x in entries if x["revalidation_state"] == "pending")
    assert first_pending == "LS-001", first_pending

    next_block = "LS"
    next_subblock = "LS"
    key = "JIS_V1.0"
    report_rel = str(REPORT.relative_to(ROOT))
    evidence_rel = str(EVIDENCE.relative_to(ROOT))
    d["next_revalidation_block"] = next_block
    blocks = d["revalidation_blocks"]
    assert key not in blocks
    blocks[key] = {
        "date": "2026-09-08",
        "state": "completed",
        "parent_block": "JIS",
        "scope_kind": "frozen_JIS_V1.0_pdf_xsd_findings",
        "source_id": "JIS_V1.0",
        "publication": "VDV 301-2-6 JourneyInformationService V1.0, 07/2016",
        "authority_lane": "byte-pinned official JIS V1.0 PDF plus exact historical route JIS V1.0 -> Common V1.0 -> Enumerations V1.0",
        "pdf_sha256": "424181b4932e18b6ac059843fa3978fdcc07a9c6acb553f9fbe8b71ef583da73",
        "pdf_size_bytes": 772125,
        "pdf_pin_run_id": "34103529949",
        "service_xsd_blob": "8c303db5a9c0548d66b90174d9c329d33092ad24",
        "common_xsd_blob": "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c",
        "enumerations_xsd_blob": "a9bea5bc73003ed91ded8519db06c32c4067831d",
        "evidence_id": "EV-152",
        "evidence_run_id": "34113437268",
        "evidence_job_id": "101714662141",
        "evidence_head_sha": "4da900b4acf993b14bdfbe5f48e0fb386fbad3fe",
        "artifact_id": "10015273758",
        "artifact_digest": "sha256:338e3fb679a8375c98fba359a3478d4cf7ba0968f3e97c08209ce52c0d23dc65",
        "evidence_record": evidence_rel,
        "closure_run_id": run_id,
        "closure_run_url": run_url,
        "fresh_visual_physical_pages": [9, 11, 12, 13, 17, 19, 22],
        "visual_status": "closed_by_fresh_byte_pinned_render_and_manual_inspection",
        "findings": EXPECTED_STATES,
        "full_xsd_pool": "50 roots PASS",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": next_block,
        "next_subblock": next_subblock,
        "terminal_state_source": report_rel,
    }

    a = s["audit"]
    assert a["finding_inventory_count"] == 192
    assert (a["finding_revalidation_completed_findings"], a["finding_revalidation_pending_findings"]) == (127, 65)
    assert a["finding_revalidation_next_block"] == "JIS"
    assert a["finding_revalidation_current_block"] == "HDS_V21_V22_V22A_HDS001"
    assert a["finding_revalidation_latest_completed_block"] == "HDS_V21_V22_V22A_HDS001"
    assert a["latest_revalidation_evidence_id"] == "EV-151"
    assert "jis_revalidation" not in a

    a["finding_revalidation_completed_findings"] = 132
    a["finding_revalidation_pending_findings"] = 60
    a["finding_revalidation_current_block"] = key
    a["finding_revalidation_latest_completed_block"] = key
    a["finding_revalidation_next_block"] = next_block
    a["finding_revalidation_latest_terminal_state_source"] = report_rel
    a["latest_revalidation_evidence_id"] = "EV-152"
    a["jis_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-152",
        "evidence_run_id": "34113437268",
        "evidence_job_id": "101714662141",
        "evidence_head_sha": "4da900b4acf993b14bdfbe5f48e0fb386fbad3fe",
        "artifact_id": "10015273758",
        "artifact_digest": "sha256:338e3fb679a8375c98fba359a3478d4cf7ba0968f3e97c08209ce52c0d23dc65",
        "terminal_states": EXPECTED_STATES,
        "exact_xsd_route": "JIS V1.0 -> Common V1.0 -> Enumerations V1.0",
        "fresh_visual_physical_pages": [9, 11, 12, 13, 17, 19, 22],
        "visual_status": "closed",
        "report": report_rel,
        "next_block": next_block,
        "next_subblock": next_subblock,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report_text = f"""# Finding Revalidation — JIS / JourneyInformationService V1.0

Date: 2026-09-08  
Scope: `JIS-001` … `JIS-005`  
Evidence: `EV-152`, successful run `34113437268`, job `101714662141`  
Evidence commit: `4da900b4acf993b14bdfbe5f48e0fb386fbad3fe`  
Artifact: `10015273758`, `sha256:338e3fb679a8375c98fba359a3478d4cf7ba0968f3e97c08209ce52c0d23dc65`  
Closure run: `{run_id}`

## Authority route

The official VDV 301-2-6 JourneyInformationService V1.0 PDF was re-fetched and byte-pinned at SHA-256 `424181b4932e18b6ac059843fa3978fdcc07a9c6acb553f9fbe8b71ef583da73` / 772125 bytes. The exact executable authority is the historical route `JIS V1.0 -> Common V1.0 -> Enumerations V1.0`. All 50 root XSDs passed unchanged.

Fresh 180-DPI renders of physical pages 9, 11, 12, 13, 17, 19 and 22 were manually inspected before closure.

## JIS-001 — contextual_not_defect

The apparent missing JIS-local Subscribe/Unsubscribe schema surface is intentional shared modelling. The PDF operation overview uses the generic Subscribe/Unsubscribe request and response structures; sections 1.4/1.5 and 1.7/1.8 explicitly delegate them to VDV 301-2-1. Exact Common V1.0 defines those structures. No JIS-local alias is inferred.

## JIS-002 — contextual_not_defect

The seven JIS `Set*` operations have local request structures, while their positive response uses the shared `DataAcceptedResponseStructure` shown by the PDF and defined in exact Common V1.0. The lack of JIS-local `Set*Response` roots is not a schema defect.

## JIS-003 — executable_confirmed

PDF table 29 visibly specifies `LineInformation` as `1:*`. Exact `JourneyInformationService.AllLineInformationData` declares `LineInformation` without `maxOccurs`, so XML Schema default `maxOccurs=1` applies. EV-152 accepts a one-entry instance and rejects an otherwise equivalent two-entry instance. This is a real PDF/XSD cardinality mismatch; selected XSD behavior remains normative.

## JIS-004 — context_verified

In section 1.22 `RetrieveAllRoutesPerLine`, table 38 visibly labels the request as `JourneyInformationService.SetBlockNumberRequest` even though the row contains `LineRef`. Section 1.23 separately defines the actual SetBlockNumber request with `BlockRef`. Exact XSD defines `JourneyInformationService.RetrieveAllRoutesPerLineRequest` with `LineRef`. This is a documentation copy/paste label defect only.

## JIS-005 — executable_confirmed

PDF table 21 visibly names the successful choice row `SpecificGNSSPointInformationData`; table 22 then defines the Data-suffixed structure. Exact XSD instead requires choice element `SpecificGNSSPointInformation` typed as `JourneyInformationService.SpecificGNSSPointInformationData`. EV-152 accepts the XSD element name and rejects the PDF Data-suffixed element name. Selected XSD behavior remains normative.

## Fail-closed history and closure

The first EV-152 run (`34113029896`) failed before completion; commit `4da900b4acf993b14bdfbe5f48e0fb386fbad3fe` hardened the global operation locator. The successful rerun changed no finding classification, XSD, or frozen inventory.

EV-152 PASS; all seven visual pages inspected; complete 50-root XSD regression PASS; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **132/192 terminal, 60 pending**. The first remaining pending finding is `LS-001`; next block is `LS`.
"""

    REG.write_text(json.dumps(d, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    STATE.write_text(json.dumps(s, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT.write_text(report_text, encoding="utf-8")
    print("JIS_CLOSURE_STATE_OK", post_terminal, post_pending, first_pending)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
