#!/usr/bin/env python3
"""Atomically close LS-001..LS-003 after EV-153 has passed."""
from __future__ import annotations

import json
import os
from pathlib import Path

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
EVIDENCE = Path("audit_registry/location_services_revalidation_evidence_2026-09-08.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_LOCATION_SERVICES_2026-09-08.md")

EXPECTED_STATES = {
    "LS-001": "executable_confirmed",
    "LS-002": "contextual_not_defect",
    "LS-003": "contextual_not_defect",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    d = load(REGISTRY)
    s = load(STATE)
    e = load(EVIDENCE)
    run_id = os.environ["CLOSURE_RUN_ID"]
    run_url = os.environ["CLOSURE_RUN_URL"]

    assert e["evidence_id"] == "EV-153" and e["result"] == "PASS"
    assert e["scope"] == list(EXPECTED_STATES)
    assert e["successful_run_id"] == "34229647400"
    assert e["successful_job_id"] == "102072276013"
    assert e["head_sha"] == "45eeed958b3f7f1081f19d6858e54a27824c682f"
    assert e["artifact_id"] == "10057222866"
    assert e["artifact_digest"] == "sha256:914a1b126e8c06145fe0ccc896f4e2a85db5204a7562ad7dada21ad660fecff7"
    assert e["full_xsd_pool"] == {"count": 50, "result": "PASS"}
    assert e["fresh_visual_evidence"]["manual_visual_review_completed"] is True
    assert e["fresh_visual_evidence"]["manual_visual_review_result"] == "PASS"
    assert e["prestate"]["terminal"] == 132 and e["prestate"]["pending"] == 60
    assert e["prestate"]["first_pending"] == "LS-001"
    assert e["prestate"]["expected_poststate_if_closed"] == {
        "terminal": 135, "pending": 57, "first_pending": "NET-001"
    }
    assert e["immutable_guards"]["frozen_inventory_blob"] == "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
    assert e["immutable_guards"]["frozen_inventory_mutated"] is False
    assert e["immutable_guards"]["xsd_mutated"] is False
    assert e["failed_closed_attempt"]["substantive_finding_contradiction"] is False
    assert e["failed_closed_attempt"]["behavior_changed"] is False
    for fid, state in EXPECTED_STATES.items():
        assert e["finding_results"][fid]["recommended_terminal_state"] == state
    assert e["finding_results"]["LS-001"]["positive_xsd_sample_valid"] is True
    assert e["finding_results"]["LS-001"]["negative_pdf_spelling_rejected"] is True
    assert e["finding_results"]["LS-002"]["positive_exact_name_valid"] is True
    assert e["finding_results"]["LS-002"]["normalized_alias_rejected"] is True
    assert e["finding_results"]["LS-003"]["routing_confirmed"] is True

    inv = d["inventory"]
    entries = inv["entries"]
    assert inv["state"] == "frozen" and inv["entry_count"] == 192 and len(entries) == 192
    assert d["next_revalidation_block"] == "LS"
    pre_terminal = sum(x["revalidation_state"] != "pending" for x in entries)
    pre_pending = sum(x["revalidation_state"] == "pending" for x in entries)
    assert (pre_terminal, pre_pending) == (132, 60), (pre_terminal, pre_pending)
    by = {x["finding_id"]: x for x in entries}
    assert next(x["finding_id"] for x in entries if x["revalidation_state"] == "pending") == "LS-001"
    for fid, state in EXPECTED_STATES.items():
        assert by[fid]["revalidation_state"] == "pending"
        assert by[fid]["terminal_state_source"] is None
        by[fid]["revalidation_state"] = state
        by[fid]["terminal_state_source"] = str(REPORT)

    post_terminal = sum(x["revalidation_state"] != "pending" for x in entries)
    post_pending = sum(x["revalidation_state"] == "pending" for x in entries)
    assert (post_terminal, post_pending) == (135, 57), (post_terminal, post_pending)
    first_pending = next(x["finding_id"] for x in entries if x["revalidation_state"] == "pending")
    assert first_pending == "NET-001", first_pending

    next_block = "NET"
    key = "LS_V1.0"
    d["next_revalidation_block"] = next_block
    blocks = d["revalidation_blocks"]
    assert key not in blocks
    blocks[key] = {
        "date": "2026-09-08",
        "state": "completed",
        "parent_block": "LS",
        "scope_kind": "frozen_Location_Services_V1.0_pdf_xsd_findings",
        "source_ids": ["BLS_V1.0", "DLS_V1.0", "GNSS_V1.0", "NLS_V1.0"],
        "publication": "VDV 301-2-2/-4/-5/-7 Location Services V1.0, 07/2016",
        "authority_lane": "four byte-pinned official Location Services V1.0 PDFs plus four exact historical service schemas and Common V1.0 + Enumerations V1.0",
        "pdfs": e["authority"]["pdfs"],
        "service_xsd_blobs": e["authority"]["service_blobs"],
        "common_xsd_blob": e["authority"]["common_blob"],
        "enumerations_xsd_blob": e["authority"]["enumerations_blob"],
        "evidence_id": "EV-153",
        "evidence_run_id": e["successful_run_id"],
        "evidence_job_id": e["successful_job_id"],
        "evidence_head_sha": e["head_sha"],
        "artifact_id": e["artifact_id"],
        "artifact_digest": e["artifact_digest"],
        "evidence_record": str(EVIDENCE),
        "closure_run_id": run_id,
        "closure_run_url": run_url,
        "fresh_visual_physical_pages": e["fresh_visual_evidence"]["physical_pages"],
        "visual_status": "closed_by_fresh_byte_pinned_render_and_manual_inspection",
        "findings": EXPECTED_STATES,
        "full_xsd_pool": "50 roots PASS",
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": next_block,
        "next_subblock": next_block,
        "terminal_state_source": str(REPORT),
    }

    a = s["audit"]
    assert a["finding_inventory_count"] == 192
    assert (a["finding_revalidation_completed_findings"], a["finding_revalidation_pending_findings"]) == (132, 60)
    assert a["finding_revalidation_next_block"] == "LS"
    assert a["finding_revalidation_current_block"] == "JIS_V1.0"
    assert a["finding_revalidation_latest_completed_block"] == "JIS_V1.0"
    assert a["latest_revalidation_evidence_id"] == "EV-152"
    assert "location_services_revalidation" not in a

    a["finding_revalidation_completed_findings"] = 135
    a["finding_revalidation_pending_findings"] = 57
    a["finding_revalidation_current_block"] = key
    a["finding_revalidation_latest_completed_block"] = key
    a["finding_revalidation_next_block"] = next_block
    a["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    a["latest_revalidation_evidence_id"] = "EV-153"
    a["location_services_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-153",
        "evidence_run_id": e["successful_run_id"],
        "evidence_job_id": e["successful_job_id"],
        "evidence_head_sha": e["head_sha"],
        "artifact_id": e["artifact_id"],
        "artifact_digest": e["artifact_digest"],
        "terminal_states": EXPECTED_STATES,
        "exact_xsd_route": e["authority"]["xsd_route"],
        "pdf_pin_run_id": "34228583786",
        "fresh_visual_physical_pages": e["fresh_visual_evidence"]["physical_pages"],
        "visual_status": "closed",
        "report": str(REPORT),
        "next_block": next_block,
        "next_subblock": next_block,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report_text = f'''# Finding Revalidation — LS / Location Services V1.0

Date: 2026-09-08  
Scope: `LS-001` … `LS-003`  
Evidence: `EV-153`, successful run `{e["successful_run_id"]}`, job `{e["successful_job_id"]}`  
Evidence commit: `{e["head_sha"]}`  
Artifact: `{e["artifact_id"]}`, `{e["artifact_digest"]}`  
Closure run: `{run_id}`

## Authority route

The official VDV 301-2-2 BeaconLocationService, 301-2-4 DistanceLocationService, 301-2-5 GNSSLocationService and 301-2-7 NetworkLocationService V1.0 PDFs were freshly fetched and byte-pinned by run `34228583786`. Executable validation remains service/version exact: four separate V1.0 service schemas, each with Common V1.0 and Enumerations V1.0. No latest-wins substitution is permitted. All 50 root XSDs passed unchanged.

Fresh 180-DPI renders of BLS pages 7/8 and DLS/GNSS/NLS page 7 were manually inspected before closure.

## LS-001 — executable_confirmed

GNSS V1.0 PDF page 7 visibly prints `HorizontalDilutionOfPrecision`. Exact `IBIS-IP_GNSSLocationService_V1.0.xsd` instead defines `HoriziontalDilutionOfPrecision`. EV-153 accepts the XSD spelling and rejects the PDF spelling. This is a real PDF/XSD spelling discrepancy; selected XSD behavior remains normative. No schema correction is made by this audit closure.

## LS-002 — contextual_not_defect

Distance V1.0 PDF page 7 and exact XSD both use `Odometer-Pulses`. EV-153 accepts the exact hyphenated XML element and rejects the normalized alias `OdometerPulses`. The finding survives only as an implementation note: tooling must preserve the exact XML name.

## LS-003 — contextual_not_defect

The Location Services intentionally use service-specific root modelling. Beacon uses `BeaconLocationService.GetDataResponse` with a Data/OperationErrorMessage choice, while Distance, GNSS and Network expose raw `*.Data` roots. EV-153 confirms positive samples on their own service schemas and cross-schema rejection. A validator must route by the exact service/version schema and must not normalize these services to one generic root pattern.

## Fail-closed history and closure

The first EV-153 run (`34229230088`) failed only because `pdftotext -layout` split the long GNSS identifier during a textual evidence assertion. Authority guards and PDF pin checks had already passed. Commit `45eeed958b3f7f1081f19d6858e54a27824c682f` added robust raw-text extraction; the successful rerun changed no finding classification, XSD, or frozen inventory.

EV-153 PASS; fresh visual evidence manually inspected; complete 50-root XSD regression PASS; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **135/192 terminal, 57 pending**. The first remaining pending finding is `NET-001`; next block is `NET`.
'''

    dump(REGISTRY, d)
    dump(STATE, s)
    REPORT.write_text(report_text, encoding="utf-8")
    print("LS_CLOSURE_READY", post_terminal, post_pending, first_pending)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
