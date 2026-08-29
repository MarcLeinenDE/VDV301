#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(".")
DATE = "2026-08-30"
EV_ID = "EV-117"
EV_RUN = "33279461529"
EV_JOB = "99172025835"
EV_HEAD = "104ff8d49af248258fcf174d62610c43179fdcf5"
CHECKER = "tools/validate_common_v10_ev117.py"
COMMON_BLOB = "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c"
ENUM_BLOB = "a9bea5bc73003ed91ded8519db06c32c4067831d"
PDF_SHA = "a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf"
FREEZE = "f21aa84b0aae5222cbfdcc4757b599f8133e2d36"

revalidated = {
    "CE-005": "V1x_scope_context_verified_with_EV-117_exact_V1.0_type_and_cardinality_support",
    "CE-007": "V1x_scope_executable_enum_lexeme_boundaries_confirmed_EV-117",
    "CE-012": "V1x_scope_executable_empty_list_confirmed_EV-117",
    "CE-013": "V1x_scope_executable_choice_and_name_boundary_confirmed_EV-117",
    "CE-014": "V1x_scope_exact_V1.0_anonymous_DataVersion_0star_declaration_confirmed_EV-117",
    "CE-015": "V1x_scope_visible_pdf_and_exact_XSD_case_boundary_confirmed_EV-117",
    "CE-016": "V1x_scope_visible_pdf_and_exact_XSD_spelling_boundary_confirmed_EV-117",
    "CE-017": "V1x_scope_executable_Description_vs_Desciption_boundary_confirmed_EV-117",
    "CE-018": "V1x_scope_executable_empty_list_confirmed_EV-117",
    "CE-019": "V1x_scope_visible_pdf_type_reference_and_exact_XSD_type_confirmed_EV-117",
    "CE-021": "V1x_scope_visible_pdf_and_exact_XSD_Message_declaration_confirmed_EV-117",
    "CE-022": "V1x_scope_executable_outer_Service_vs_ServiceName_boundary_confirmed_EV-117",
    "CE-025": "V1x_scope_visible_pdf_and_exact_XSD_ReplyPath_declaration_confirmed_EV-117",
    "CE-026": "V1x_scope_executable_Description_vs_Desciption_boundary_confirmed_EV-117",
}

new_findings = {
    "DRCOM10-001": {
        "state": "executable_xsd_boundary_confirmed_EV-117_with_visible_pdf_context",
        "classification": "pdf_revision_vs_exact_historical_xsd_drift",
        "summary": (
            "The official 05/2017 Common publication records internal Version 1.1 changes, "
            "including Connection/RouteDirection changes, while the exact official Common/"
            "Enumerations V1.0 authority remains the unchanged 2014 import. EV-117 confirms "
            "required DisplayContent, ExpectedDepatureTime, no ScheduledDepartureTime, no "
            "TripInformation.RouteDirection and no RouteDirectionEnumeration in the selected V1.0 XSD family. "
            "AdditionalTextMessage overlap remains tracked as CE-005 rather than duplicated here."
        ),
        "executable_effect": True,
    },
    "DRCOM10-002": {
        "state": "executable_confirmed_EV-117",
        "classification": "pdf_compositor_omission_or_table_modelling_error",
        "summary": (
            "The DataAcceptedResponse PDF table visibly presents DataAcceptedResponseData and "
            "OperationErrorMessage as ordinary 1:1 rows, while exact V1.0 XSD uses xs:choice. "
            "EV-117 confirms each branch alone is valid and both together are invalid."
        ),
        "executable_effect": True,
    },
    "DRCOM10-003": {
        "state": "executable_confirmed_EV-117",
        "classification": "cardinality_xsd_more_permissive_than_pdf",
        "summary": (
            "ServiceSpecificationWithStateList is documented as 1:* but exact V1.0 XSD permits "
            "0:*; EV-117 confirms an empty list validates."
        ),
        "executable_effect": True,
    },
    "DRCOM10-004": {
        "state": "context_verified_with_exact_xsd_declarations_EV-117",
        "classification": "cardinality_xsd_stricter_than_pdf",
        "summary": (
            "JourneyStopInformation documents Announcement and FareZone as 0:* while exact V1.0 "
            "XSD declares each 0:1. EV-117 confirms the exact declarations; no separate repeated-instance "
            "probe is claimed."
        ),
        "executable_effect": True,
    },
    "DRCOM10-005": {
        "state": "context_verified_with_exact_xsd_declarations_EV-117",
        "classification": "pdf_element_name_and_type_reference_model_error",
        "summary": (
            "ShortTripStopList is shown with a repeating child labelled ShortTripStopList and "
            "type StopPointTariffInformation, while exact XSD uses ShortTripStop of type "
            "ShortTripStopStructure; StopPointTariffInformationStructure exists separately."
        ),
        "executable_effect": True,
    },
    "DRCOM10-006": {
        "state": "executable_confirmed_EV-117",
        "classification": "enumeration_lexeme_mismatch",
        "summary": (
            "DoorCountingObjectClassEnumeration prints Wheelchair/Others while exact V1.0 XSD "
            "uses WheelChair/Other; EV-117 confirms the XSD lexemes validate and PDF-side forms fail."
        ),
        "executable_effect": True,
    },
    "DRCOM10-007": {
        "state": "context_verified",
        "classification": "pdf_editorial_errors_grouped",
        "summary": (
            "Grouped low-severity non-executable editorial residue includes GNSSCoordinateSystem(s) "
            "heading/caption inconsistency, broken cross-references and spelling/language residue."
        ),
        "executable_effect": False,
    },
}


def load_json(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def save_json(path: str, data):
    (ROOT / path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_once(path: str, marker: str, text: str):
    p = ROOT / path
    current = p.read_text(encoding="utf-8")
    if marker not in current:
        p.write_text(current.rstrip() + "\n\n" + text.strip() + "\n", encoding="utf-8")


# 1) Machine-readable findings delta.
delta = {
    "delta_version": "0.1",
    "date": DATE,
    "document_id": "COMMON_V1.0",
    "evidence_gate": "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md",
    "fresh_read_freeze": FREEZE,
    "source_evidence": {
        "pdf_sha256": PDF_SHA,
        "pin_render_read_run": "33275626001",
        "job": "99161707311",
        "artifact": "9721397514",
        "page_count": 36,
        "fulltext_sha256": "fdfdf62a88f78dd7a59b341157662d3e5708b2f9c56d2cf1df13a7d4eb0cfa0a",
    },
    "exact_xsd_authority": {
        "official_import_commit": "604a5a5c7608977e483072f7e450d7381cc182e4",
        "common_blob": COMMON_BLOB,
        "enumerations_blob": ENUM_BLOB,
        "common_v1_1_xsd_found": False,
        "authority_note": (
            "The 05/2017 PDF has internal document/data-definition revision Version 1.1, "
            "but executable authority remains the exact official V1.0 XSD family."
        ),
    },
    "executable_evidence": {
        "evidence_id": EV_ID,
        "checker": CHECKER,
        "run": EV_RUN,
        "job": EV_JOB,
        "head_tested": EV_HEAD,
        "result": "PASS",
        "authority": "exact_official_historical_Common_V1.0_Enumerations_V1.0_family",
        "initial_probe_correction": {
            "run": "33279395750",
            "job": "99171853097",
            "classification": "test_fixture_error_not_authority_or_finding_failure",
            "detail": "InternationalTextType positive fixture initially omitted required Language; corrected fixture rerun passed.",
        },
    },
    "revalidated_or_scope_extended_findings": revalidated,
    "new_unique_findings": new_findings,
    "deduplication": (
        "Fresh observations overlapping CE-005/007/012-019/021/022/025/026 reuse those IDs. "
        "Only V1.x-specific revision/compositor/cardinality/model/lexeme/editorial observations "
        "without an existing finding identity receive DRCOM10-001..007."
    ),
    "next_natural_document_id": "COMMON_V2.0",
}
save_json("audit_registry/deep_read_findings_delta_common_v10_2026-08-30.json", delta)

# 2) Close the Common V1.0 registry delta.
reg_path = "audit_registry/deep_read_registry_delta_common_v10_2026-08-29.json"
reg = load_json(reg_path)
doc = reg["document_updates"]["COMMON_V1.0"]
if doc.get("state") != "independent_fresh_read_frozen_pending_historical_reconciliation":
    raise SystemExit(f"Unexpected COMMON_V1.0 registry state: {doc.get('state')}")
doc["state"] = "deep_read_closed_after_historical_reconciliation_EV-117"
doc["historical_reconciliation_status"] = "complete"
doc["executable_evidence"] = {
    "evidence_id": EV_ID,
    "checker": CHECKER,
    "run": EV_RUN,
    "job": EV_JOB,
    "head_tested": EV_HEAD,
    "result": "PASS",
    "common_blob": COMMON_BLOB,
    "enumerations_blob": ENUM_BLOB,
}
doc["revalidated_or_scope_extended_findings"] = revalidated
doc["new_unique_findings"] = list(new_findings.keys())
doc["findings_delta"] = "audit_registry/deep_read_findings_delta_common_v10_2026-08-30.json"
doc["next_natural_document_id"] = "COMMON_V2.0"
save_json(reg_path, reg)

# 3) Record current-gate revalidation status.
fr_path = "audit_registry/finding_revalidation_registry_v0.1.json"
fr = load_json(fr_path)
fr["date"] = DATE
fr["explicit_revalidations_during_deep_read_pass_2"]["COMMON_V1.0"] = revalidated
save_json(fr_path, fr)

# 4) Advance current state to the closed V1.0 boundary / next V2.0 unit.
cs_path = "00_START_HERE/CURRENT_STATE.json"
cs = load_json(cs_path)
cs["date"] = DATE
a = cs["audit"]
if a.get("deep_read_current_document_id") != "COMMON_V1.0":
    raise SystemExit(f"Unexpected current document: {a.get('deep_read_current_document_id')}")
a["deep_read_needs_visual_review"] = 32
a["deep_read_textual_fresh_read_completed"] = 32
a["deep_read_in_progress"] = 0
a["deep_read_previous_document_id"] = "COMMON_V1.0"
a["next_natural_deep_read_document_id"] = "COMMON_V2.0"
a["latest_deep_read_finding"] = "DRCOM10-007"
a["latest_deep_read_revalidation"] = "CE-026_V1x_scope_executable_Description_vs_Desciption_boundary_EV-117"
a["latest_common_finding"] = "DRCOM10-007"
a["latest_deep_read_findings_delta"] = "audit_registry/deep_read_findings_delta_common_v10_2026-08-30.json"
a["latest_deep_read_registry_delta"] = reg_path
a["common_v1_0_executable_evidence"] = {
    "evidence_id": EV_ID,
    "run": EV_RUN,
    "job": EV_JOB,
    "checker": CHECKER,
    "result": "PASS",
    "common_blob": COMMON_BLOB,
    "enumerations_blob": ENUM_BLOB,
}
a["common_v1_0_findings"] = {**revalidated, **{k: v["state"] for k, v in new_findings.items()}}
save_json(cs_path, cs)

# 5) EV-117 evidence document.
ev_doc = f"""# 24o — Executable validation COMMON V1.0 — EV-117

Status: PASS.

## Authority

Exact historical official V1.0 family:

```text
official import commit 604a5a5c7608977e483072f7e450d7381cc182e4
IBIS-IP_common_V1.0.xsd       {COMMON_BLOB}
IBIS-IP_Enumerations_V1.0.xsd {ENUM_BLOB}
route                          Common V1.0 -> Enumerations V1.0
```

The official 05/2017 Common PDF is byte-pinned as `{PDF_SHA}` and carries an internal
document/data-definition revision `Version 1.1`. No `IBIS-IP_common_V1.1.xsd` was found.
EV-117 therefore does not invent a V1.1 schema authority.

## Execution

```text
Evidence ID: {EV_ID}
checker:     {CHECKER}
run:         {EV_RUN}
job:         {EV_JOB}
head tested: {EV_HEAD}
result:      PASS
```

An earlier controlled run `33279395750` / job `99171853097` failed only because the
positive Beacon/TSP test fixture omitted the required `Language` child of
`InternationalTextType`. The fixture was corrected; no XSD, finding or authority
classification was changed to obtain the PASS.

## Confirmed executable boundaries

EV-117 pins the exact Git blobs and confirms, among other checks:

- Connection V1.0 has required `DisplayContent`, typo-like `ExpectedDepatureTime`, no
  `ExpectedDepartureTime` and no `ScheduledDepartureTime`.
- TripInformation V1.0 has single optional `AdditionalTextMessage` of type
  `IBIS-IP.string`, no `RouteDirection`; Enumerations V1.0 has no `RouteDirectionEnumeration`.
- AdditionalAnnouncement uses optional `xs:choice`; omitted choice and `SpecificPoint`
  validate, PDF-only `InformationAtSpecificPoint` does not.
- DataAcceptedResponse uses an exclusive XSD choice; either branch validates, both together fail.
- empty DeviceSpecificationWithStateList, ServiceIdentificationWithStateList and
  ServiceSpecificationWithStateList validate.
- exact typo/case element names are enforced for BeaconPoint/TSPPoint and ServiceIdentification.
- historical enum lexemes are case-sensitive: `WheelChair`, `Other`, `other`, `valid`
  and `air` validate in their respective types while the checked PDF-side alternatives fail.
- `PassengerCountingService` and `starting` are not members of the exact V1.0
  ServiceName/ServiceState enumerations.

## Evidence-Gate boundary

EV-117 proves only the executable declarations and instance behaviour it tests. The
finding conclusions also rely on the independently frozen, byte-pinned Fresh Read in
`deep_read/COMMON_V1.0.md`. No XSD change is implied.
"""
(ROOT / "docs/pdf_xsd_semantic_audit/24o_executable_validation_common_v10.md").write_text(ev_doc, encoding="utf-8")

# 6) Append closure to the frozen Fresh Read report.
closure = f"""## Historical reconciliation and closure — 2026-08-30

The historical Common registers were opened only after the independent Fresh Read
freeze `{FREEZE}`.

### Deduplication

Existing finding identities are reused and their V1.x scope is revalidated/refined
where the pinned 05/2017 source and exact V1.0 XSD support it:

```text
{chr(10).join(f'{k}: {v}' for k, v in revalidated.items())}
```

New unique findings are limited to:

```text
{chr(10).join(f'{k}: {v["classification"]}' for k, v in new_findings.items())}
```

`DRCOM10-001` deliberately does not duplicate the AdditionalTextMessage issue already
tracked by `CE-005`.

### Executable evidence

EV-117 run `{EV_RUN}` / job `{EV_JOB}` PASS on exact historical V1.0 blobs
`{COMMON_BLOB}` + `{ENUM_BLOB}`. See `24o_executable_validation_common_v10.md`.

The first controlled EV-117 run failed only due to an incomplete positive test fixture
for InternationalTextType and is retained as provenance, not as contradictory schema evidence.

### Closure

COMMON V1.0 remains `needs_visual_review`, not `exhaustive_read`: all 36 pinned pages
were rendered and the material pages for findings were visibly reviewed, but the
visual pass was targeted rather than a pixel-by-pixel exhaustive closure.

No XSD was changed. Next natural Deep Read unit: `COMMON_V2.0`.
"""
append_once("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V1.0.md", "## Historical reconciliation and closure — 2026-08-30", closure)

# 7) Append V1.x scope extension to Common findings register.
scope_text = f"""## COMMON V1.0 / public V1.x Deep Read scope extension — 2026-08-30

Source: byte-pinned official 05/2017 VDV 301-2-1 publication, SHA-256 `{PDF_SHA}`.
Exact executable authority remains official Common V1.0 `{COMMON_BLOB}` plus
Enumerations V1.0 `{ENUM_BLOB}`.

EV-117 run `{EV_RUN}` PASS.

Existing IDs revalidated/refined for V1.x where applicable:

```text
{chr(10).join(f'{k}: {v}' for k, v in revalidated.items())}
```

This does **not** visually close unresolved V2.x portions of CE-019/021/022/etc.;
it only establishes the V1.x scope from the independently pinned source.

New unique V1.x Deep Read findings are `DRCOM10-001..DRCOM10-007`; detailed machine-
readable evidence is in `audit_registry/deep_read_findings_delta_common_v10_2026-08-30.json`.

Validation continues to follow the exact selected XSD family. No alias is synthesized
from PDF spelling, casing, cardinality or type-reference wording.
"""
append_once("docs/pdf_xsd_semantic_audit/COMMON_FINDINGS_REGISTER_ADDENDUM.md", "## COMMON V1.0 / public V1.x Deep Read scope extension — 2026-08-30", scope_text)

# 8) Evidence ID policy.
ep_path = "docs/pdf_xsd_semantic_audit/EVIDENCE_ID_POLICY.md"
ep = (ROOT / ep_path).read_text(encoding="utf-8")
needle = "EV-116  SystemMonitoringService V2.2 exact operation-name/generic-subscription modelling evidence"
if needle not in ep:
    raise SystemExit("EV-116 policy anchor missing")
if "EV-117  Common V1.0" not in ep:
    ep = ep.replace(needle, needle + "\nEV-117  Common V1.0 exact historical authority + Deep Read choice/cardinality/naming/enum boundary evidence")
ep = ep.replace("EV-001, EV-002 and EV-101 through EV-116", "EV-001, EV-002 and EV-101 through EV-117")
if "EV-117:" not in ep:
    ep = ep.rstrip() + f"""

EV-117:
The checked Common V1.0 family is exact historical official authority from the
2014 VDV initial V1 import:
  Common V1.0       {COMMON_BLOB}
  Enumerations V1.0 {ENUM_BLOB}
The byte-pinned 05/2017 publication has internal document/data-definition revision
Version 1.1, but no Common V1.1 XSD exists. EV-117 therefore tests the exact V1.0
executable family and must not be described as invented V1.1 schema conformance.
Run {EV_RUN} PASS.
"""
(ROOT / ep_path).write_text(ep, encoding="utf-8")

# 9) Validation backlog.
vb_path = "docs/pdf_xsd_semantic_audit/validation_backlog.md"
vb = (ROOT / vb_path).read_text(encoding="utf-8")
line116 = "EV-116           run 33269006407  PASS  official SMS V2.2 ServiceStatus naming + generic Common subscription modelling evidence"
if line116 not in vb:
    raise SystemExit("EV-116 backlog anchor missing")
if "EV-117           run 33279461529" not in vb:
    vb = vb.replace(line116, line116 + "\nEV-117           run 33279461529  PASS  exact historical Common V1.0 Deep Read authority/behaviour evidence")
vb = vb.replace("EV-110 through EV-116 are targeted additive tests", "EV-110 through EV-117 are targeted additive tests")
append = f"""## COMMON V1.0 EV-117 closure

EV-117 run `{EV_RUN}` / job `{EV_JOB}` PASS on exact official historical Common V1.0
`{COMMON_BLOB}` + Enumerations V1.0 `{ENUM_BLOB}`.

The prior Common targeted backlog is narrowed for V1.x: EV-117 now supplies exact
V1.0 declaration/instance evidence for CE-005/007/012-019/021/022/025/026 to the
extent explicitly listed in the Common V1.0 findings delta. It does not automatically
close unresolved visual scope in later Common versions.

New V1.x-specific findings DRCOM10-001..007 are recorded in the Common V1.0 delta.
No further deterministic V1.0 XSD run is currently required before moving to `COMMON_V2.0`.
"""
if "## COMMON V1.0 EV-117 closure" not in vb:
    vb = vb.rstrip() + "\n\n" + append.strip() + "\n"
(ROOT / vb_path).write_text(vb, encoding="utf-8")

# 10) Central findings index.
find_path = "docs/pdf_xsd_semantic_audit/findings.md"
find = (ROOT / find_path).read_text(encoding="utf-8")
section = f"""## COMMON V1.0 / public V1.x Deep Read closure

```text
source: byte-pinned official 05/2017 VDV 301-2-1 publication
exact XSD authority: Common V1.0 {COMMON_BLOB}
                     Enumerations V1.0 {ENUM_BLOB}
EV-117: run {EV_RUN} PASS
```

The source has internal document/data-definition revision `Version 1.1` while the
official executable XSD family remains the unchanged V1.0 import. Existing Common
finding IDs are reused where the Fresh Read rediscovered the same discrepancy.
Unique additions are `DRCOM10-001..DRCOM10-007`, covering revision-vs-XSD drift,
DataAcceptedResponse choice modelling, additional list/cardinality/model differences,
DoorCountingObjectClass lexemes and grouped editorial residue.

No V1.1 XSD authority is invented and no XSD is changed.
"""
if "## COMMON V1.0 / public V1.x Deep Read closure" not in find:
    find = find.rstrip() + "\n\n" + section.strip() + "\n"
(ROOT / find_path).write_text(find, encoding="utf-8")

# 11) Handoff delta.
handoff = f"""# Audit handoff delta — COMMON V1.0 Deep Read closure — 2026-08-30

## Closed unit

`COMMON_V1.0` / official public VDV 301-2-1 Common publication.

Pinned PDF SHA-256: `{PDF_SHA}`.
Independent Fresh Read freeze: `{FREEZE}`.

## Exact XSD authority

```text
official import commit: 604a5a5c7608977e483072f7e450d7381cc182e4
Common V1.0:            {COMMON_BLOB}
Enumerations V1.0:      {ENUM_BLOB}
```

No Common V1.1 XSD was found. The PDF's internal Version 1.1 revision is retained as
documentation/data-definition history, not converted into a new executable authority.

## EV-117

```text
checker: {CHECKER}
run:     {EV_RUN}
job:     {EV_JOB}
result:  PASS
```

The initial controlled run `33279395750` failed solely because a positive
InternationalTextType fixture omitted required `Language`; the corrected fixture passed.
No finding/XSD was altered to force success.

## Reconciliation

Existing CE identities reused:
`CE-005`, `CE-007`, `CE-012..019`, `CE-021`, `CE-022`, `CE-025`, `CE-026`.

New unique findings:
`DRCOM10-001..DRCOM10-007`.

Detailed mapping:
`audit_registry/deep_read_findings_delta_common_v10_2026-08-30.json`.

## Guardrails

- exact selected XSD remains executable validation authority;
- no latest-XSD-wins;
- no invented Common V1.1 XSD;
- no XSD modification in this closure;
- unresolved later-version visual portions are not silently closed by V1.x evidence.

## Resume

Next natural Deep Read unit: `COMMON_V2.0`.
"""
(ROOT / "docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_COMMON_V10_DEEP_READ_2026-08-30.md").write_text(handoff, encoding="utf-8")

print("Prepared COMMON V1.0 closure files successfully")
