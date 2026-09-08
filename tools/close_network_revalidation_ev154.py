#!/usr/bin/env python3
"""Atomically close NET-001..NET-003 after EV-154 has passed."""
from __future__ import annotations

import json
import os
from pathlib import Path

REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
STATE = Path("00_START_HERE/CURRENT_STATE.json")
EVIDENCE = Path("audit_registry/network_vdv301_3_revalidation_evidence_2026-09-08.json")
REPORT = Path("docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_NETWORK_2026-09-08.md")

EXPECTED_STATES = {
    "NET-001": "context_verified",
    "NET-002": "context_verified",
    "NET-003": "context_verified",
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

    assert e["evidence_id"] == "EV-154" and e["result"] == "PASS"
    assert e["scope"] == list(EXPECTED_STATES)
    assert e["successful_run_id"] == "34232483234"
    assert e["successful_job_id"] == "102081822927"
    assert e["head_sha"] == "3645ddfeb32effd0b17432672ab91476e1accdf8"
    assert e["artifact_id"] == "10058380451"
    assert e["artifact_digest"] == "sha256:dcb266cad68054375d65818fda20d7ec53c59843a48525d60b3ade62f5c38396"
    assert e["authority"]["source_id"] == "VDV301-3_02-2020"
    assert e["authority"]["pdf_sha256"] == "edfedf36eeb18075b45bf5224f0da6500cdd489438091f18bada42f9668c2a99"
    assert e["authority"]["pdf_size_bytes"] == 558005
    assert e["authority"]["fresh_bytes_match_historical_pin"] is True
    assert e["authority"]["validation_lane"] == "physical/network/protocol documentation; intentionally no XSD lane"
    assert e["fresh_visual_evidence"]["physical_pages"] == [6, 7, 8, 11, 14, 20, 29]
    assert e["fresh_visual_evidence"]["manual_visual_review_completed"] is True
    assert e["fresh_visual_evidence"]["manual_visual_review_result"] == "PASS"
    assert e["fresh_visual_evidence"]["pin_and_validator_render_hashes_identical"] is True
    assert e["executable_evidence"]["applicable"] is False
    assert e["full_xsd_pool"]["count"] == 50 and e["full_xsd_pool"]["result"] == "PASS"
    assert e["prestate"]["terminal"] == 135 and e["prestate"]["pending"] == 57
    assert e["prestate"]["first_pending"] == "NET-001"
    assert e["prestate"]["expected_poststate_if_closed"] == {
        "terminal": 138, "pending": 54, "first_pending": "PCS-001"
    }
    assert e["immutable_guards"]["frozen_inventory_blob"] == "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
    assert e["immutable_guards"]["frozen_inventory_mutated"] is False
    assert e["immutable_guards"]["xsd_mutated"] is False
    for fid, state in EXPECTED_STATES.items():
        assert e["finding_results"][fid]["recommended_terminal_state"] == state
    assert e["finding_results"]["NET-001"]["alternate_document_identity_rejected"] is True
    assert e["finding_results"]["NET-002"]["english_toc_skip_confirmed"] is True
    assert e["finding_results"]["NET-003"]["correct_spelling_elsewhere_same_writing"] is True

    inv = d["inventory"]
    entries = inv["entries"]
    assert inv["state"] == "frozen" and inv["entry_count"] == 192 and len(entries) == 192
    assert d["next_revalidation_block"] == "NET"
    pre_terminal = sum(x["revalidation_state"] != "pending" for x in entries)
    pre_pending = sum(x["revalidation_state"] == "pending" for x in entries)
    assert (pre_terminal, pre_pending) == (135, 57), (pre_terminal, pre_pending)
    by = {x["finding_id"]: x for x in entries}
    assert next(x["finding_id"] for x in entries if x["revalidation_state"] == "pending") == "NET-001"
    for fid, state in EXPECTED_STATES.items():
        assert by[fid]["revalidation_state"] == "pending"
        assert by[fid]["terminal_state_source"] is None
        by[fid]["revalidation_state"] = state
        by[fid]["terminal_state_source"] = str(REPORT)

    post_terminal = sum(x["revalidation_state"] != "pending" for x in entries)
    post_pending = sum(x["revalidation_state"] == "pending" for x in entries)
    assert (post_terminal, post_pending) == (138, 54), (post_terminal, post_pending)
    first_pending = next(x["finding_id"] for x in entries if x["revalidation_state"] == "pending")
    assert first_pending == "PCS-001", first_pending

    next_block = "PCS"
    key = "VDV301-3_02-2020"
    d["next_revalidation_block"] = next_block
    blocks = d["revalidation_blocks"]
    assert key not in blocks
    blocks[key] = {
        "date": "2026-09-08",
        "state": "completed",
        "parent_block": "NET",
        "scope_kind": "frozen_VDV301_3_network_documentation_findings",
        "source_ids": ["VDV301-3_02-2020"],
        "publication": "VDV-Schrift 301-3 Network Infrastructure, 02/2020",
        "authority_lane": "byte-pinned official VDV 301-3 PDF plus independent frozen-head Deep Read; intentionally no XSD lane",
        "pdf": e["authority"],
        "evidence_id": "EV-154",
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
        "full_xsd_pool": "50 roots PASS as regression/no-mutation guard only",
        "xsd_lane_applicable": False,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
        "next_block": next_block,
        "next_subblock": next_block,
        "terminal_state_source": str(REPORT),
    }

    a = s["audit"]
    assert a["finding_inventory_count"] == 192
    assert (a["finding_revalidation_completed_findings"], a["finding_revalidation_pending_findings"]) == (135, 57)
    assert a["finding_revalidation_next_block"] == "NET"
    assert a["finding_revalidation_current_block"] == "LS_V1.0"
    assert a["finding_revalidation_latest_completed_block"] == "LS_V1.0"
    assert a["latest_revalidation_evidence_id"] == "EV-153"
    assert "network_revalidation" not in a

    a["finding_revalidation_completed_findings"] = 138
    a["finding_revalidation_pending_findings"] = 54
    a["finding_revalidation_current_block"] = key
    a["finding_revalidation_latest_completed_block"] = key
    a["finding_revalidation_next_block"] = next_block
    a["finding_revalidation_latest_terminal_state_source"] = str(REPORT)
    a["latest_revalidation_evidence_id"] = "EV-154"
    a["network_revalidation"] = {
        "status": "complete",
        "completed_at_run": run_id,
        "evidence_id": "EV-154",
        "evidence_run_id": e["successful_run_id"],
        "evidence_job_id": e["successful_job_id"],
        "evidence_head_sha": e["head_sha"],
        "artifact_id": e["artifact_id"],
        "artifact_digest": e["artifact_digest"],
        "terminal_states": EXPECTED_STATES,
        "source_id": e["authority"]["source_id"],
        "pdf_sha256": e["authority"]["pdf_sha256"],
        "pdf_size_bytes": e["authority"]["pdf_size_bytes"],
        "pdf_pin_run_id": e["authority"]["fresh_pin_run_id"],
        "fresh_visual_physical_pages": e["fresh_visual_evidence"]["physical_pages"],
        "visual_status": "closed",
        "xsd_lane_applicable": False,
        "report": str(REPORT),
        "next_block": next_block,
        "next_subblock": next_block,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }

    report_text = f'''# Finding Revalidation — NET / VDV 301-3 Network Infrastructure 02/2020

Date: 2026-09-08  
Scope: `NET-001` … `NET-003`  
Evidence: `EV-154`, successful run `{e["successful_run_id"]}`, job `{e["successful_job_id"]}`  
Evidence commit: `{e["head_sha"]}`  
Artifact: `{e["artifact_id"]}`, `{e["artifact_digest"]}`  
Closure run: `{run_id}`

## Authority route

The official VDV-Schrift 301-3 Network Infrastructure 02/2020 PDF was freshly fetched and byte-pinned at SHA-256 `{e["authority"]["pdf_sha256"]}` ({e["authority"]["pdf_size_bytes"]} bytes). The fresh bytes match the independent historical pin. Definition provenance comes from the independent frozen-head Deep Read performed before historical reconciliation. VDV 301-3 intentionally has no XSD lane; therefore the complete 50-root XSD run is retained only as a regression/no-mutation guard and is not used as executable evidence for these findings.

Fresh 180-DPI renders of physical pages 6, 7, 8, 11, 14, 20 and 29 were manually inspected before closure.

## NET-001 — context_verified

English Scope page 8 visibly says `VDV 303-3`. German Scope page 7, the page footer and the publication identity all establish `VDV 301-3`. The alternate-document interpretation is therefore actively disproved. The finding is a local English documentation-number typo.

## NET-002 — context_verified

The German cabling subsection is visibly numbered `2.3.4` on page 14. The corresponding English subsection is visibly numbered `2.3.5` on page 20, and the English table of contents on page 6 skips directly from `2.3.3` to `2.3.5`. Intentional bilingual renumbering is unsupported; the finding is an editorial subsection-numbering error.

## NET-003 — context_verified

German page 11 visibly prints `IEE 802.3`. The same exact publication uses the correct `IEEE 802.3` spelling elsewhere, including the PoE reference `IEEE 802.3af/at/bt` on page 29. An intentional alternate abbreviation is therefore actively disproved; this is a local IEEE spelling typo.

## Closure

EV-154 PASS; fresh byte-pinned visual evidence manually inspected; complete 50-root XSD regression PASS as no-mutation guard; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **138/192 terminal, 54 pending**. The first remaining pending finding is `PCS-001`; next block is `PCS`.
'''

    dump(REGISTRY, d)
    dump(STATE, s)
    REPORT.write_text(report_text, encoding="utf-8")
    print("NET_CLOSURE_READY", post_terminal, post_pending, first_pending)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
