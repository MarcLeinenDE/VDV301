#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path('.')
DATE = '2026-08-30'
EV = 'EV-118'
RUN = '33280224191'
JOB = '99174026383'
HEAD = 'f048cc6ac896c0eb9885999ee5c9e1d3c91d7e77'
CHECKER = 'tools/validate_common_v20_ev118.py'
FREEZE = '60d8e6a444473615771bcab52e22293d96a8aa04'
PDF_SHA = '23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088'
COMMON_BLOB = '8608e3dcd665c197c34da7f6ec6af5a3758da164'
ENUM_BLOB = '27e3c183b00381d959622d13c10543123af8eef6'

revalidated = {
    'CE-005': 'V2.0_scope_visible_table_and_version_history_plus_exact_0to1_XSD_declaration_EV-118',
    'CE-007': 'V2.0_scope_executable_enum_lexeme_boundaries_confirmed_EV-118',
    'CE-012': 'V2.0_scope_executable_empty_DeviceSpecificationWithStateList_confirmed_EV-118',
    'CE-013': 'V2.0_scope_executable_optional_choice_and_SpecificPoint_name_boundary_EV-118',
    'CE-014': 'V2.0_scope_executable_empty_DataVersionList_confirmed_EV-118',
    'CE-015': 'V2.0_scope_visible_pdf_and_exact_XSD_FareZone_case_boundary_confirmed_EV-118',
    'CE-016': 'V2.0_scope_visible_pdf_and_exact_XSD_GlobalCardStausID_boundary_confirmed_EV-118',
    'CE-017': 'V2.0_scope_executable_TSPPoint_Description_vs_Desciption_boundary_EV-118',
    'CE-018': 'V2.0_scope_visible_pdf_1star_plus_executable_empty_ServiceIdentificationWithStateList_EV-118',
    'CE-019': 'V2.0_scope_visible_pdf_type_reference_plus_exact_ServiceIdentificationWithStateStructure_EV-118',
    'CE-021': 'V2.0_scope_visible_MessageBody_vs_exact_XSD_Message_declaration_EV-118',
    'CE-022': 'V2.0_scope_executable_outer_Service_vs_ServiceName_boundary_EV-118',
    'CE-025': 'V2.0_scope_visible_Reply-Path_vs_exact_ReplyPath_declarations_EV-118',
    'CE-026': 'V2.0_scope_executable_BeaconPoint_Description_vs_Desciption_boundary_EV-118',
    'DRCOM10-002': 'V2.0_scope_executable_DataAcceptedResponse_choice_boundary_EV-118',
    'DRCOM10-003': 'V2.0_scope_executable_empty_ServiceSpecificationWithStateList_EV-118',
    'DRCOM10-004': 'V2.0_scope_exact_JourneyStop_Announcement_FareZone_0to1_declarations_EV-118',
    'DRCOM10-005': 'V2.0_scope_refined_child_name_facet_persists_type_facet_aligned_exact_XSD_EV-118',
    'DRCOM10-006': 'V2.0_scope_executable_DoorCountingObjectClass_lexemes_EV-118',
    'DRCOM10-007': 'V2.0_scope_context_verified_grouped_editorial_residue',
}

new_findings = {
    'DRCOM20-001': {
        'state': 'executable_confirmed_EV-118',
        'classification': 'pdf_type_reference_vs_xsd_primitive_instance_shape_mismatch',
        'summary': (
            'Common V2.0 PDF InternationalTextType prints Value as IBIS-IP.string and Language as '
            'IBIS-IP.language, while exact official V2.0 XSD uses xs:string and xs:language. EV-118 '
            'confirms the exact flat primitive-shaped instance validates and an IBIS-IP wrapper-shaped '
            'Value/Language instance fails. This is kept separate from CE-020 because CE-020 additionally '
            'tracks the V2.3 PR #30 same-path authority collision.'
        ),
        'executable_effect': True,
    }
}


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding='utf-8'))


def save(path: str, data):
    (ROOT / path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def append_once(path: str, marker: str, text: str):
    p = ROOT / path
    old = p.read_text(encoding='utf-8')
    if marker not in old:
        p.write_text(old.rstrip() + '\n\n' + text.strip() + '\n', encoding='utf-8')


# Findings delta.
delta = {
    'delta_version': '0.1',
    'date': DATE,
    'document_id': 'COMMON_V2.0',
    'fresh_read_freeze': FREEZE,
    'source_evidence': {
        'pdf_sha256': PDF_SHA,
        'size_bytes': 946088,
        'pin_render_read_run': '33279811315',
        'job': '99172952524',
        'artifact_id': '9722644456',
        'artifact_zip_sha256': '412a1714ce9c02b412262bb4d6103e686d85bf63709ad8a1bce2a3ac0d2361d9',
        'page_count': 45,
        'fulltext_sha256': '05e8a7e1788318bf5ac83ffdd61125622e28ce30f4fc5f388467a41ed46f5a3f',
    },
    'exact_xsd_authority': {
        'official_tag': 'VDV-301-2.0',
        'common_blob': COMMON_BLOB,
        'enumerations_blob': ENUM_BLOB,
        'branch_bytes_match_official_tag': True,
    },
    'executable_evidence': {
        'evidence_id': EV,
        'checker': CHECKER,
        'run': RUN,
        'job': JOB,
        'head_tested': HEAD,
        'result': 'PASS',
        'authority': 'exact_official_VDV-301-2.0_Common_Enumerations_family',
    },
    'revalidated_or_scope_extended_findings': revalidated,
    'new_unique_findings': new_findings,
    'explicit_non_extension': {
        'CE-020': 'not scope-extended: CE-020 remains V2.3-specific because its identity includes the PR #30 same-path authority collision; DRCOM20-001 tracks the V2.0 primitive-vs-wrapper PDF/XSD mismatch'
    },
    'active_falsification': [
        'Connection DisplayContent optionality and ExpectedDepartureTime/ScheduledDepartureTime are corrected and aligned in V2.0',
        'TripInformation RouteDirection and RouteDirectionEnumeration are aligned in V2.0',
        'readyForShutdown, PassengerCountingService, video service names and ServiceState starting align in V2.0',
        'ShortTripStop V1.x type facet is not carried forward: V2.0 PDF type aligns semantically with ShortTripStopStructure; only the child-label facet persists',
        'Message-ID is identical in PDF and XSD and is not a finding',
    ],
    'next_natural_document_id': 'COMMON_V2.1',
}
save('audit_registry/deep_read_findings_delta_common_v20_2026-08-30.json', delta)

# Registry closure.
reg_path = 'audit_registry/deep_read_registry_delta_common_v20_2026-08-30.json'
reg = load(reg_path)
doc = reg['document_updates']['COMMON_V2.0']
if doc.get('state') != 'independent_fresh_read_frozen_pending_historical_reconciliation':
    raise SystemExit(f"unexpected registry state: {doc.get('state')}")
doc['state'] = 'deep_read_closed_after_historical_reconciliation_EV-118'
doc['historical_reconciliation_status'] = 'complete'
doc['executable_evidence'] = {
    'evidence_id': EV, 'checker': CHECKER, 'run': RUN, 'job': JOB,
    'head_tested': HEAD, 'result': 'PASS', 'common_blob': COMMON_BLOB,
    'enumerations_blob': ENUM_BLOB,
}
doc['revalidated_or_scope_extended_findings'] = revalidated
doc['new_unique_findings'] = list(new_findings)
doc['findings_delta'] = 'audit_registry/deep_read_findings_delta_common_v20_2026-08-30.json'
doc['next_natural_document_id'] = 'COMMON_V2.1'
save(reg_path, reg)

# Revalidation registry.
fr_path = 'audit_registry/finding_revalidation_registry_v0.1.json'
fr = load(fr_path)
fr['date'] = DATE
fr['explicit_revalidations_during_deep_read_pass_2']['COMMON_V2.0'] = revalidated
save(fr_path, fr)

# Current state.
state_path = '00_START_HERE/CURRENT_STATE.json'
state = load(state_path)
a = state['audit']
if a.get('deep_read_current_document_id') != 'COMMON_V2.0' or a.get('deep_read_in_progress') != 1:
    raise SystemExit('CURRENT_STATE is not at expected COMMON_V2.0 in-progress boundary')
state['date'] = DATE
a['deep_read_in_progress'] = 0
a['deep_read_previous_document_id'] = 'COMMON_V2.0'
a['next_natural_deep_read_document_id'] = 'COMMON_V2.1'
a['latest_deep_read_finding'] = 'DRCOM20-001'
a['latest_deep_read_revalidation'] = 'CE-026_V2.0_scope_executable_BeaconPoint_Description_vs_Desciption_boundary_EV-118'
a['latest_common_finding'] = 'DRCOM20-001'
a['latest_deep_read_findings_delta'] = 'audit_registry/deep_read_findings_delta_common_v20_2026-08-30.json'
a['latest_deep_read_registry_delta'] = reg_path
a['common_v2_0_deep_read_report'] = 'docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.0.md'
a['common_v2_0_handoff'] = 'docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_COMMON_V20_DEEP_READ_2026-08-30.md'
a['common_v2_0_executable_evidence'] = {
    'evidence_id': EV, 'run': RUN, 'job': JOB, 'checker': CHECKER, 'result': 'PASS',
    'Common_V2.0_blob': COMMON_BLOB, 'Enumerations_V2.0_blob': ENUM_BLOB,
}
a['common_v2_0_findings'] = {**revalidated, **{k: v['state'] for k, v in new_findings.items()}}
state['evidence']['latest_targeted_xsd_evidence'] = EV
state['next_actions'] = [
    'Start COMMON V2.1 Deep Read from the official byte-pinned source; establish exact VDV-301-2.1 Common/Enumerations authority before historical reconciliation.',
    'Complete independent COMMON V2.1 Fresh Read and targeted visible review before reopening historical Common findings for that document.',
    'After Deep Read Pass 2 freeze the complete finding inventory and run mandatory legacy finding revalidation before SDK/remediation baseline freeze.'
]
save(state_path, state)

# EV evidence doc.
ev_doc = f'''# 24p — Executable validation COMMON V2.0 — EV-118

Status: PASS.

## Authority

```text
official tag:                  VDV-301-2.0
IBIS-IP_common_V2.0.xsd        {COMMON_BLOB}
IBIS-IP_Enumerations_V2.0.xsd  {ENUM_BLOB}
route:                         Common V2.0 -> Enumerations V2.0
branch bytes:                  exact match to official tag
```

## Execution

```text
Evidence ID: {EV}
checker:     {CHECKER}
run:         {RUN}
job:         {JOB}
head tested: {HEAD}
result:      PASS
```

## Confirmed boundaries

EV-118 confirms the exact V2.0 family compiles and, among its targeted checks:

- `InternationalTextType.Value` is `xs:string` and `Language` is `xs:language`;
  flat primitive-shaped content validates while the PDF-implied IBIS-IP wrapper-shaped
  Value/Language content fails.
- `AdditionalAnnouncement` is an optional XSD choice; `SpecificPoint` validates and
  PDF-only `InformationAtSpecificPoint` fails.
- `DataAcceptedResponse` is an exclusive choice: either branch alone validates; both fail.
- empty `DataVersionList` and the three checked WithState lists validate.
- `TripInformation.AdditionalTextMessage` has effective maxOccurs=1 in exact XSD;
  this check is declaration evidence, not a separately constructed full TripInformation repeat probe.
- BeaconPoint/TSPPoint `Desciption` is accepted while `Description` is rejected.
- ServiceIdentification outer `Service` validates while PDF outer `ServiceName` fails.
- exact enum lexemes `WheelChair`, `Other`, `other`, `valid`, `air` validate while the
  corresponding checked PDF-side variants fail.
- V2.0 corrections/additions such as `ExpectedDepartureTime`, `ScheduledDepartureTime`,
  `RouteDirectionEnumeration`, `readyForShutdown`, PassengerCounting/video service names
  and `starting` are positively present and are not carried forward as defects.

EV-118 does not modify the official XSD and does not turn PDF notation into executable authority.
'''
(ROOT / 'docs/pdf_xsd_semantic_audit/24p_executable_validation_common_v20.md').write_text(ev_doc, encoding='utf-8')

# Deep-read report closure.
report_append = f'''## Historical reconciliation and closure — 2026-08-30

Historical Common material was reopened only after independent freeze `{FREEZE}`.

### Deduplification / scope extension

```text
{chr(10).join(f'{k}: {v}' for k, v in revalidated.items())}
```

Only one new V2.0-specific ID is required:

```text
DRCOM20-001: {new_findings['DRCOM20-001']['classification']}
```

`CE-020` is deliberately not broadened because its finding identity includes the V2.3
PR #30 authority collision. `DRCOM20-001` isolates the V2.0 PDF-vs-official-XSD
primitive/wrapper type difference without importing later candidate history.

`DRCOM10-005` is refined for V2.0: the child-label mismatch persists, but the V1.x
StopPointTariffInformation type/model facet is not carried forward because the V2.0 PDF
type is aligned with the ShortTripStop model.

### Executable evidence

EV-118 run `{RUN}` / job `{JOB}` PASS against exact official V2.0 blobs
`{COMMON_BLOB}` + `{ENUM_BLOB}`.

### Closure

COMMON V2.0 remains `needs_visual_review`, not `exhaustive_read`: all 45 pinned pages
were rendered and material finding pages were visibly reviewed, but the visual pass was
targeted rather than pixel-by-pixel exhaustive.

No XSD was changed. Next natural Deep Read unit: `COMMON_V2.1`.
'''
append_once('docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.0.md', '## Historical reconciliation and closure — 2026-08-30', report_append)

# Common addendum.
common_append = f'''## COMMON V2.0 Deep Read scope extension — 2026-08-30

Source: byte-pinned official V2.0 VDV 301-2-1 publication, SHA-256 `{PDF_SHA}`.
Exact executable authority: official tag `VDV-301-2.0`, Common `{COMMON_BLOB}` plus
Enumerations `{ENUM_BLOB}`. EV-118 run `{RUN}` PASS.

Existing IDs revalidated/refined:

```text
{chr(10).join(f'{k}: {v}' for k, v in revalidated.items())}
```

New unique finding:

```text
DRCOM20-001 InternationalTextType PDF IBIS-IP.string/IBIS-IP.language vs exact
             V2.0 XSD xs:string/xs:language; executable instance-shape difference EV-118
```

`CE-020` remains V2.3-specific because it additionally tracks PR #30 and the explicit
same-path authority collision. No V2.0 candidate overlay is inferred.

Validation follows the exact selected V2.0 XSD family; no PDF alias or multiplicity is synthesized.
'''
append_once('docs/pdf_xsd_semantic_audit/COMMON_FINDINGS_REGISTER_ADDENDUM.md', '## COMMON V2.0 Deep Read scope extension — 2026-08-30', common_append)

# Evidence policy.
ep_path = 'docs/pdf_xsd_semantic_audit/EVIDENCE_ID_POLICY.md'
ep = (ROOT / ep_path).read_text(encoding='utf-8')
anchor = 'EV-117  Common V1.0 exact historical authority + Deep Read choice/cardinality/naming/enum boundary evidence'
if anchor not in ep:
    raise SystemExit('EV-117 anchor missing')
if 'EV-118  Common V2.0' not in ep:
    ep = ep.replace(anchor, anchor + '\nEV-118  Common V2.0 exact official authority + Deep Read type/choice/cardinality/naming/enum boundary evidence')
ep = ep.replace('EV-001, EV-002 and EV-101 through EV-117', 'EV-001, EV-002 and EV-101 through EV-118')
if '\nEV-118:\n' not in ep:
    ep = ep.rstrip() + f'''\n\nEV-118:\nThe checked Common V2.0 family is exact official `VDV-301-2.0` authority:\n  Common V2.0       {COMMON_BLOB}\n  Enumerations V2.0 {ENUM_BLOB}\nEV-118 run {RUN} confirms the primitive InternationalTextType instance shape and the\ntargeted V2.0 compositor/cardinality/name/enum boundaries. It is official-release V2.0\nXSD evidence and does not inherit the later V2.3 PR #30 candidate authority collision.\n'''
(ROOT / ep_path).write_text(ep, encoding='utf-8')

# Validation backlog.
vb_path = 'docs/pdf_xsd_semantic_audit/validation_backlog.md'
vb = (ROOT / vb_path).read_text(encoding='utf-8')
if 'EV-118           run 33280224191' not in vb:
    # Insert immediately after EV-117 if present; otherwise append safely.
    anchor_line = 'EV-117           run 33279461529  PASS  exact historical Common V1.0 Deep Read authority/behaviour evidence'
    line = 'EV-118           run 33280224191  PASS  exact official Common V2.0 Deep Read authority/behaviour evidence'
    if anchor_line in vb:
        vb = vb.replace(anchor_line, anchor_line + '\n' + line)
    else:
        vb = vb.rstrip() + '\n\n' + line + '\n'
vb = vb.replace('EV-110 through EV-117 are targeted additive tests', 'EV-110 through EV-118 are targeted additive tests')
backlog_append = f'''## COMMON V2.0 EV-118 closure

EV-118 run `{RUN}` / job `{JOB}` PASS on exact official Common V2.0 `{COMMON_BLOB}` +
Enumerations V2.0 `{ENUM_BLOB}`.

The V2.0 deterministic XSD lane is closed for the frozen observations. Existing CE/DRCOM10
IDs are scope-extended only where the exact pinned source rediscovered the same issue.
`DRCOM20-001` is the sole new V2.0-specific finding. No further deterministic V2.0 XSD
run is currently required before moving to `COMMON_V2.1`.
'''
if '## COMMON V2.0 EV-118 closure' not in vb:
    vb = vb.rstrip() + '\n\n' + backlog_append.strip() + '\n'
(ROOT / vb_path).write_text(vb, encoding='utf-8')

# Central findings index.
find_path = 'docs/pdf_xsd_semantic_audit/findings.md'
find = (ROOT / find_path).read_text(encoding='utf-8')
find_append = f'''## COMMON V2.0 Deep Read closure

```text
source: exact byte-pinned official VDV 301-2-1 V2.0
XSD authority: official VDV-301-2.0
Common blob: {COMMON_BLOB}
Enumerations blob: {ENUM_BLOB}
EV-118: run {RUN} PASS
```

The V2.0 Fresh Read mainly revalidates/extends existing Common finding identities.
The sole new ID is `DRCOM20-001`: InternationalTextType is documented with
`IBIS-IP.string` / `IBIS-IP.language`, while exact official V2.0 XSD uses `xs:string` /
`xs:language`; EV-118 confirms the observable instance-shape boundary.

`CE-020` remains V2.3-specific because its identity also includes the PR #30 candidate
same-path authority collision. No XSD was modified.
'''
if '## COMMON V2.0 Deep Read closure' not in find:
    find = find.rstrip() + '\n\n' + find_append.strip() + '\n'
(ROOT / find_path).write_text(find, encoding='utf-8')

# Handoff.
handoff = f'''# Audit handoff delta — COMMON V2.0 Deep Read closure — 2026-08-30

## Closed unit

`COMMON_V2.0` / official VDV 301-2-1 V2.0.

```text
PDF SHA-256: {PDF_SHA}
Fresh Read freeze: {FREEZE}
official XSD tag: VDV-301-2.0
Common blob: {COMMON_BLOB}
Enumerations blob: {ENUM_BLOB}
```

## EV-118

```text
checker: {CHECKER}
run:     {RUN}
job:     {JOB}
result:  PASS
```

## Reconciliation

Existing CE/DRCOM10 IDs were reused wherever the independent Fresh Read rediscovered the
same semantic discrepancy. Only `DRCOM20-001` is new. `CE-020` remains V2.3-specific.

V1.x corrections that genuinely align in V2.0 were actively falsified and are not carried
forward as defects: Connection optionality/time names, RouteDirection, readyForShutdown,
PassengerCounting/video service names and ServiceState starting.

No XSD changed. No candidate authority was introduced.

## Resume

Next natural Deep Read unit: `COMMON_V2.1`.
'''
(ROOT / 'docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_COMMON_V20_DEEP_READ_2026-08-30.md').write_text(handoff, encoding='utf-8')

# Validate JSON written by this finalizer.
for path in [
    state_path, reg_path, fr_path,
    'audit_registry/deep_read_findings_delta_common_v20_2026-08-30.json',
]:
    json.loads((ROOT / path).read_text(encoding='utf-8'))

print('Prepared COMMON V2.0 closure files successfully')
