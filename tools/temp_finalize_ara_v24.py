#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

def load_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def write_json(rel, obj):
    (ROOT / rel).write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def append_once(rel, marker, text):
    p = ROOT / rel
    cur = p.read_text(encoding="utf-8")
    if marker in cur:
        return
    if not cur.endswith("\n"):
        cur += "\n"
    p.write_text(cur + "\n" + text.strip() + "\n", encoding="utf-8")

reg_rel = "audit_registry/deep_read_registry_delta_ara_v24_2026-08-29.json"
reg = load_json(reg_rel)
ara = reg["document_updates"]["ARA_V2.4"]
ara["state"] = "historical_reconciliation_complete"
ara["historical_reconciliation_status"] = "complete_after_independent_fresh_read_freeze"
ara["historical_findings_opened_after_freeze"] = True
ara["historical_reconciliation"] = {
    "ARA-001": "context_verified_provenance_gap_under_current_evidence_gate",
    "ARA-002": "context_verified_pinned_pdf_internal_name_contradiction",
    "ARA-003": "executable_confirmed_EV-105_current_route_rerun_33228250613",
    "ARA-004": "context_verified_pinned_pdf_operation_name_inconsistency_with_candidate_xsd_support",
    "DRARA24-001": "context_verified_pdf_uri_scheme_omission",
    "DRARA24-002": "context_verified_grouped_editorial_typos"
}
ara["ev105_current_route_revalidation"] = {
    "original_run": "33111831627",
    "original_head": "86e3592968f24cfa59e05ace625f64886ca3ae89",
    "current_route_rerun": "33228250613",
    "current_route_head": "97a117a2b03fa2bc78f7fedb7eb2d31bd81ec419",
    "service_blob": "48fb303b80936d2d762f0889ce0c359e04c16e5b",
    "common_v2_3_blob": "0d8926c4063c12de9a5e68b6f0addaab35a55dc1",
    "enumerations_v2_2_blob": "2a23b512379b18e8f122ac1272cef8229fb86283",
    "result": "PASS",
    "authority": "candidate_integration_service_plus_official_common_v2.3_dependency",
    "official_release_conformance": False
}
write_json(reg_rel, reg)

findings = {
    "delta_version": "0.1", "date": "2026-08-29", "document_id": "ARA_V2.4",
    "evidence_gate": "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md",
    "fresh_read_freeze": "fe77b60b96e8d8aef138b71c00f44d4e409ba1f1",
    "executable_evidence": {
        "evidence_id": "EV-105", "checker": "tools/validate_analog_radio_ev105.py",
        "original_run": "33111831627", "current_route_rerun": "33228250613",
        "current_route_head": "97a117a2b03fa2bc78f7fedb7eb2d31bd81ec419", "result": "PASS",
        "authority": "candidate_AnalogRadio_V2.4_service_blob_48fb303b_plus_official_Common_V2.3_0d8926c_plus_Enums_V2.2_2a23b5"
    },
    "revalidated_findings": {
        "ARA-001": {"state": "context_verified", "classification": "schema_family_or_provenance_gap", "handling": "official_schema_family_clarification_candidate"},
        "ARA-002": {"state": "context_verified", "classification": "pdf_table_element_name_error", "handling": "official_pdf_documentation_clarification_candidate"},
        "ARA-003": {"state": "executable_confirmed_EV-105_current_route_rerun_33228250613", "classification": "cardinality_mismatch_candidate_xsd_more_permissive_than_pdf", "handling": "candidate_schema_review_plus_documentation_clarification"},
        "ARA-004": {"state": "context_verified_with_candidate_xsd_support", "classification": "pdf_operation_name_error_in_uri_example", "handling": "official_pdf_documentation_clarification_candidate"}
    },
    "new_unique_findings": {
        "DRARA24-001": {"state": "context_verified", "classification": "pdf_uri_example_scheme_omission", "summary": "Concrete SendTelegram URI example omits http:// although the immediately preceding URI form includes it.", "executable_effect": False},
        "DRARA24-002": {"state": "context_verified", "classification": "pdf_editorial_spelling_errors_grouped", "summary": "Grouped visible/editorial residue includes AnlogRadioService, pre-emtion, contians, pre-amption and BitrateEnumerationis.", "executable_effect": False}
    },
    "rejected_suspicions": [
        "cover-page isolated Fehler from extraction is not visible in rendered page 1",
        "missing SendTelegram response is not independently a defect because the PDF explicitly states response not provided",
        "official PDF reference to GitHub releases does not establish an official VDV-301-2.4 XSD release",
        "page-11 plain 1:1 is ordinary cardinality notation and not leading-minus XML-choice notation"
    ],
    "deduplication": "FR-ARA24-OBS-001 reconciles to historical ARA-002 + ARA-003; FR-ARA24-OBS-002 reconciles to ARA-004; the authority analysis revalidates ARA-001; FR-ARA24-OBS-003 becomes DRARA24-001; editorial observations FR-ARA24-OBS-004/005 are grouped as DRARA24-002."
}
write_json("audit_registry/deep_read_findings_delta_ara_v24_2026-08-29.json", findings)

rv_rel = "audit_registry/finding_revalidation_registry_v0.1.json"
rv = load_json(rv_rel)
rv["explicit_revalidations_during_deep_read_pass_2"]["ARA_V2.4"] = {
    "ARA-001": "context_verified_provenance_gap_under_current_evidence_gate",
    "ARA-002": "context_verified_pinned_pdf_internal_name_contradiction",
    "ARA-003": "executable_confirmed_EV-105_current_route_rerun_33228250613",
    "ARA-004": "context_verified_pinned_pdf_operation_name_inconsistency_with_candidate_xsd_support"
}
write_json(rv_rel, rv)

state_rel = "00_START_HERE/CURRENT_STATE.json"
state = load_json(state_rel)
a = state["audit"]
a["deep_read_needs_visual_review"] = 30
a["deep_read_textual_fresh_read_completed"] = 30
a["deep_read_in_progress"] = 0
a["deep_read_current_document_id"] = None
a["deep_read_previous_document_id"] = "ARA_V2.4"
a["next_natural_deep_read_document_id"] = "VDV301-3_02-2020"
a["latest_deep_read_finding"] = "DRARA24-002"
a["latest_deep_read_revalidation"] = "ARA-003_executable_confirmed_EV-105_current_route_rerun_33228250613"
a["latest_deep_read_registry_delta"] = reg_rel
a["latest_deep_read_findings_delta"] = "audit_registry/deep_read_findings_delta_ara_v24_2026-08-29.json"
a["ara_v2_4_deep_read_report"] = "docs/pdf_xsd_semantic_audit/deep_read/ARA_V2.4.md"
a["ara_v2_4_visual_evidence"] = {"pinned_byte_render_run": "33269472968", "render_job": "99145237184", "artifact": "9719652068", "artifact_digest": "sha256:06c2ce302b1b98d5bbe22265806ea605bbc2abe62327b8d809a0e27da19592a3", "pdf_page_count": 16, "pages_reviewed": [1,9,10,11,12,13,14], "status": "targeted_visible_review_complete_for_fresh_observations_not_exhaustive"}
a["ara_v2_4_fresh_read_status"] = "historical_reconciliation_complete"
a["ara_v2_4_findings"] = {"ARA-001": "context_verified_provenance_gap_under_current_evidence_gate", "ARA-002": "context_verified_pinned_pdf_internal_name_contradiction", "ARA-003": "executable_confirmed_EV-105_current_route_rerun_33228250613", "ARA-004": "context_verified_pinned_pdf_operation_name_inconsistency_with_candidate_xsd_support", "DRARA24-001": "context_verified", "DRARA24-002": "context_verified"}
a["ara_v2_4_executable_evidence"] = {"evidence_id": "EV-105", "checker": "tools/validate_analog_radio_ev105.py", "original_run": "33111831627", "current_route_rerun": "33228250613", "status": "PASS", "authority": "candidate_service_plus_official_Common_V2.3_current_route_not_official_release_conformance"}
ev = state["evidence"]
if "EV-116" not in ev["xsd_ev_completed"]: ev["xsd_ev_completed"].append("EV-116")
ev["latest_targeted_xsd_evidence_run"] = "33269006407"
ev["latest_pdf_source_pin_run"] = "33269415752"
ev["latest_pdf_visual_render_run"] = "33269472968"
ev["sms_v2_2_executable_evidence"] = "EV-116 / 33269006407"
ev["ara_v2_4_candidate_executable_evidence"] = "EV-105 / current-route rerun 33228250613 (original 33111831627)"
state["next_actions"] = [
    "Start VDV301-3_02-2020 Network Infrastructure with its own verified source pin.",
    "Fresh-read Network Infrastructure document-first and keep physical/network protocol evidence separate from XML/XSD authority.",
    "Reconcile historical network/discovery findings only after the independent fresh-read freeze.",
    "Continue remaining Deep Reads.",
    "After Deep Read Pass 2 freeze the complete finding inventory and run mandatory legacy finding revalidation before SDK/remediation baseline freeze.",
    "Do not decide PR/mail/remediation disposition during Deep Read unless explicitly requested."
]
write_json(state_rel, state)

append_once("docs/pdf_xsd_semantic_audit/deep_read/ARA_V2.4.md", "## Historical reconciliation — completed after freeze", """
## Historical reconciliation — completed after freeze

The post-freeze historical register maps cleanly to the independent observations:

- `ARA-001` is revalidated as the V2.4 public-document / official-release-schema provenance gap.
- `ARA-002` is revalidated from the pinned PDF's own contradiction: table `TransmitterType` vs embedded schema/diagram/example `Transmitter`.
- `ARA-003` is revalidated as the 1:1 vs 0:1 cardinality mismatch. EV-105 was rerun in canonical full-suite run `33228250613` on service blob `48fb303b...` with official Common V2.3 blob `0d8926c...` and Enumerations V2.2 blob `2a23b5...`; omission and presence of `Transmitter` both validate. This remains candidate/integration evidence, not official V2.4 release conformance.
- `ARA-004` is revalidated from the pinned PDF: operation inventory/XML example use `SendTelegram`, while the URI example uses `SendFFSKTelegram`.
- `DRARA24-001` records the concrete URI example's omitted `http://` scheme.
- `DRARA24-002` groups the remaining non-executable editorial spelling residue.

No XSD was changed. Historical IDs were not used to generate the fresh observation list; they were opened only after freeze for deduplication and revalidation.
""")

append_once("docs/pdf_xsd_semantic_audit/ANALOG_RADIO_SERVICE_FINDINGS_REGISTER_ADDENDUM.md", "## Deep Read Pass 2 current-gate reconciliation", """
## Deep Read Pass 2 current-gate reconciliation

Pinned official PDF evidence and the independent fresh-read freeze `fe77b60b96e8d8aef138b71c00f44d4e409ba1f1` revalidate `ARA-001` through `ARA-004`.

Current states:

```text
ARA-001  context_verified_provenance_gap_under_current_evidence_gate
ARA-002  context_verified_pinned_pdf_internal_name_contradiction
ARA-003  executable_confirmed_EV-105_current_route_rerun_33228250613
ARA-004  context_verified_pinned_pdf_operation_name_inconsistency_with_candidate_xsd_support
DRARA24-001 context_verified_pdf_uri_scheme_omission
DRARA24-002 context_verified_grouped_editorial_typos
```

EV-105 authority refinement:

```text
original run 33111831627:
  service blob 48fb303b...
  Common V2.3 at that historical head was PR-30 candidate 456a7db...

canonical full-suite rerun 33228250613:
  service blob 48fb303b...
  official Common V2.3 root 0d8926c...
  Enumerations V2.2 2a23b5...
  EV-105 PASS
  50/50 root XSD compile PASS
```

The current-route rerun closes the executable dependency-route concern without creating a new evidence ID. Candidate/integration status remains unchanged; there is still no official VDV-301-2.4 release XSD authority for AnalogRadioService.
""")

append_once("docs/pdf_xsd_semantic_audit/24e_executable_validation_analog_radio.md", "## Current-route revalidation under the Deep Read Evidence Gate", """
## Current-route revalidation under the Deep Read Evidence Gate

The original EV-105 run remains provenance evidence, but its historical head still had the PR-30 candidate blob at the root path `IBIS-IP_common_V2.3.xsd`.

A later canonical full-suite run reran the same checker after the Common V2.3 authority split:

```text
run: 33228250613
job: 99036090357
head: 97a117a2b03fa2bc78f7fedb7eb2d31bd81ec419
AnalogRadioService V2.4: 48fb303b80936d2d762f0889ce0c359e04c16e5b
Common V2.3 official:     0d8926c4063c12de9a5e68b6f0addaab35a55dc1
Enumerations V2.2:       2a23b512379b18e8f122ac1272cef8229fb86283
result: PASS
```

The run explicitly compiled `IBIS-IP_AnalogRadioService_V2.4.xsd`, confirmed `Transmitter` 0:1, accepted SendTelegram both without and with Transmitter, and the same full suite compiled 50/50 repository root XSDs.

Therefore ARA-003 is executable-confirmed under the current Evidence Gate without allocating a new EV ID. The result is still candidate/integration behavior only and must not be described as official V2.4 release conformance.
""")

policy_rel = "docs/pdf_xsd_semantic_audit/EVIDENCE_ID_POLICY.md"
policy = (ROOT / policy_rel).read_text(encoding="utf-8")
if "EV-105 current-route revalidation:" not in policy:
    needle = "Authority guards:\n\n```text\n"
    insert = """Authority guards:\n\n```text\nEV-105 current-route revalidation:\nThe original EV-105 run 33111831627 tested AnalogRadioService blob 48fb303b80936d2d762f0889ce0c359e04c16e5b while the root Common V2.3 path still held PR-30 candidate blob 456a7db179ce14bc3f04e2bc05e42e16545fb0c5.\nCanonical full-suite run 33228250613 reran the same EV-105 checker with the same service blob but official Common V2.3 blob 0d8926c4063c12de9a5e68b6f0addaab35a55dc1 plus Enumerations V2.2 blob 2a23b512379b18e8f122ac1272cef8229fb86283; EV-105 and the 50-root compile both PASS.\nThis closes the current-route executable dependency concern without a new EV ID. AnalogRadioService V2.4 remains candidate/integration material and EV-105 is not official-release V2.4 conformance evidence.\n\n"""
    if needle not in policy: raise SystemExit("EVIDENCE_ID_POLICY authority guard anchor missing")
    policy = policy.replace(needle, insert, 1)
    (ROOT / policy_rel).write_text(policy, encoding="utf-8")

backlog_rel = "docs/pdf_xsd_semantic_audit/validation_backlog.md"
backlog = (ROOT / backlog_rel).read_text(encoding="utf-8")
old = "EV-105           run 33111831627  PASS  AnalogRadio candidate cardinality"
new = "EV-105           run 33111831627  PASS  AnalogRadio candidate cardinality; current-route rerun 33228250613 PASS"
if old in backlog: backlog = backlog.replace(old, new, 1)
elif new not in backlog: raise SystemExit("validation_backlog EV-105 anchor missing")
(ROOT / backlog_rel).write_text(backlog, encoding="utf-8")
append_once(backlog_rel, "## AnalogRadioService V2.4 Deep Read closure", """
## AnalogRadioService V2.4 Deep Read closure

The official V2.4 PDF is byte-pinned and independently fresh-read. The executable XSD comparison remains candidate/integration-only because no official VDV-301-2.4 release tag/service XSD exists.

Current-gate reconciliation:

```text
ARA-001 context_verified provenance gap
ARA-002 context_verified TransmitterType-vs-Transmitter PDF inconsistency
ARA-003 executable_confirmed EV-105 current-route rerun 33228250613
ARA-004 context_verified SendFFSKTelegram-vs-SendTelegram URI inconsistency
DRARA24-001 context_verified missing http:// in concrete URI example
DRARA24-002 context_verified grouped editorial spelling residue
```

No new EV ID is required: canonical full-suite run `33228250613` already reran EV-105 with the current official Common V2.3 root and passed.
""")

handoff = """# Audit handoff delta — AnalogRadioService V2.4 Deep Read

Date: 2026-08-29
Branch: `dev/schema-integration`

## Closure

`ARA_V2.4` completed the independent Fresh Read, pinned-byte visual review and post-freeze historical reconciliation.

Official PDF:

```text
VDV 301-2-19 AnalogRadioService V2.4, 01/2023
sha256 d0c8d8a3b8719c13b09f43ec98349d2e9b22d07fec0c9267bceff0812cbbc34c
size 1009640
pin run 33269415752
render/read run 33269472968
```

XSD authority remains candidate/integration:

```text
AnalogRadioService V2.4 48fb303b80936d2d762f0889ce0c359e04c16e5b
Common V2.3 official    0d8926c4063c12de9a5e68b6f0addaab35a55dc1
Enumerations V2.2      2a23b512379b18e8f122ac1272cef8229fb86283
no VDV-301-2.4 official release tag/service XSD
```

EV-105 needs no new run: canonical full-suite run `33228250613` already reran the checker on that current route and passed.

Revalidated historical findings: `ARA-001` through `ARA-004`.
New findings: `DRARA24-001`, `DRARA24-002`.

No XSD changed.

## Next natural document

`VDV301-3_02-2020` — Network Infrastructure / Netzwerkinfrastruktur.

Continue document-first: establish/pin the official source, fresh-read independently, and only after freeze reconcile historical network/discovery material.
"""
(ROOT / "docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_ARA_V24_DEEP_READ_2026-08-29.md").write_text(handoff, encoding="utf-8")

for rel in [reg_rel, "audit_registry/deep_read_findings_delta_ara_v24_2026-08-29.json", rv_rel, state_rel]: json.loads((ROOT / rel).read_text(encoding="utf-8"))
Path(__file__).unlink()
print("ARA_V24_FINALIZE_READY")
