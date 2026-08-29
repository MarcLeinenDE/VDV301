#!/usr/bin/env python3
from pathlib import Path
import json

DATE='2026-08-29'
EV_RUN='33269006407'
EV_JOB='99144006184'
EV_CHECKER='tools/validate_sms_v22_ev116.py'
FREEZE='625bb9a4d19f1f1c47a529686defa9b1368c80ff'
NEXT='ARA_V2.4'


def append_once(path: Path, marker: str, text: str) -> None:
    current=path.read_text(encoding='utf-8')
    if marker not in current:
        path.write_text(current.rstrip()+'\n\n'+text.strip()+'\n', encoding='utf-8')

# 1) EV-116 document
Path('docs/pdf_xsd_semantic_audit/24o_executable_validation_sms_v22.md').write_text('''# EV-116 - SystemMonitoringService V2.2 official executable evidence

Status: PASS

Date: 2026-08-29

## Exact official authority

EV-116 executes the exact official `VDV-301-2.2` family. The integration branch is blob-identical for all three selected files.

```text
SystemMonitoringService V2.2  d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c
Common V2.2                   468fee6d177e7185dbcd5d3f90cfb114e29e01ae
Enumerations V2.2             2a23b512379b18e8f122ac1272cef8229fb86283
```

No later Common/Enumerations family is substituted.

## Run

```text
checker: tools/validate_sms_v22_ev116.py
checker introduction commit: e34e0f54f53b334ebd3652393aad1744cb287852
run: 33269006407
job: 99144006184
temporary run head: 5107f5465ce084543a026f0eace204e017315136
result: PASS
```

## Confirmed

- exact three official Git blobs matched;
- the service XSD includes exact Common V2.2 + Enumerations V2.2 and compiles;
- `SystemMonitoringServiceGroup` contains exactly `GetDeviceStatusResponse` and `GetServiceStatusResponse` service-local response elements;
- Common V2.2 contains the generic Subscribe/Unsubscribe request and response structures referenced by the PDF;
- exact `SystemMonitoringService.GetServiceStatusResponse` validates on its `OperationErrorMessage` branch;
- invented `SystemMonitoringService.GetSystemStatusResponse` has no global declaration and is invalid;
- exact `SystemMonitoringService.GetDeviceStatusResponse` validates;
- SMS response-data list wrappers are required 1:1;
- Common V2.2 list-item declarations are observed as 0:* only for authority/routing context.

## Evidence boundary

EV-116 strengthens the executable side of SMS-001 and SMS-002. It does **not** by itself revalidate Common findings CE-012, CE-018 or CE-019, nor does it make PDF prose executable authority.

No XSD changed.
''', encoding='utf-8')

# 2) findings delta
findings={
  'delta_version':'0.1','date':DATE,'document_id':'SMS_V2.2',
  'evidence_gate':'docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md',
  'fresh_read_freeze':FREEZE,
  'executable_evidence':{'evidence_id':'EV-116','checker':EV_CHECKER,'run':EV_RUN,'job':EV_JOB,'result':'PASS','authority':'official_VDV-301-2.2_exact_family'},
  'revalidated_findings':{
    'SMS-001':{'state':'contextual_not_defect_executable_context_confirmed_EV-116','classification':'service_modelling / intentional generic Common subscription modelling','handling':'no_action_note'},
    'SMS-002':{'state':'executable_confirmed_EV-116','classification':'pdf_operation_heading_error','handling':'official_pdf_documentation_clarification_candidate'},
    'SMS-003':{'state':'context_verified','classification':'pdf_wrong_service_copy_paste','handling':'official_pdf_documentation_clarification_candidate'},
    'SMS-004':{'state':'context_verified_pdf_reference_number_error','classification':'pdf_reference_number_error','handling':'official_pdf_documentation_clarification_candidate'}
  },
  'new_unique_findings':{
    'DRSMS22-001':{'state':'context_verified','classification':'documentation_generation_error_printed_broken_cross_reference','summary':'PDF visibly prints Fehler! Textmarke nicht definiert. in the list-of-figures area','executable_effect':False},
    'DRSMS22-002':{'state':'context_verified_with_exact_common_type_semantics','classification':'pdf_semantic_copy_paste_error','summary':'ServiceStatus prose describes device state although exact Common type semantics are ServiceIdentification + ServiceState','executable_effect':False},
    'DRSMS22-003':{'state':'context_verified','classification':'pdf_editorial_spelling_error','summary':'SystemManagementService is misspelled SystemManagmentService in version history','executable_effect':False},
    'DRSMS22-004':{'state':'context_verified','classification':'pdf_operation_table_label_omission','summary':'UnsubscribeServiceStatus request/response structures are present but Req./Resp. labels are omitted in the operation table','executable_effect':False}
  },
  'rejected_suspicions':[
    'cover-page isolated Fehler from extraction is not visible in rendered page 1',
    '-1:1 with a/b labels is VDV XML-choice notation and matches xs:choice',
    'generic subscription operations not appearing as service-local XSD elements is not a defect'
  ],
  'common_lane_not_revalidated':['CE-012','CE-018','CE-019'],
  'deduplication':'FR-SMS22-OBS-001/003/005 reconcile to historical SMS-003/SMS-002/SMS-004 respectively; four remaining fresh observations receive DRSMS22-001..004.'
}
Path('audit_registry/deep_read_findings_delta_sms_v22_2026-08-29.json').write_text(json.dumps(findings,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# 3) registry delta
p=Path('audit_registry/deep_read_registry_delta_sms_v22_2026-08-29.json')
d=json.loads(p.read_text(encoding='utf-8')); h=d['document_updates']['SMS_V2.2']
h['state']='targeted_visual_review_complete_historical_reconciliation_complete'
h['historical_reconciliation_status']='complete_for_V2.2'
h['fresh_read_freeze_commit']=FREEZE
h['existing_findings_revalidated']={
  'SMS-001':'contextual_not_defect_executable_context_confirmed_EV-116',
  'SMS-002':'executable_confirmed_EV-116',
  'SMS-003':'context_verified',
  'SMS-004':'context_verified_pdf_reference_number_error'
}
h['new_unique_findings']=['DRSMS22-001','DRSMS22-002','DRSMS22-003','DRSMS22-004']
h['executable_evidence']={'evidence_id':'EV-116','checker':EV_CHECKER,'run':EV_RUN,'job':EV_JOB,'status':'PASS','authority':'official_VDV-301-2.2_exact_family'}
h['common_lane_deferred_findings']=['CE-012','CE-018','CE-019']
h['common_lane_note']='SMS V2.2 observes exact Common declarations for routing context only; CE-012/018/019 are not revalidated by this service closure.'
h['next_document_id']=NEXT
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# 4) revalidation registry
p=Path('audit_registry/finding_revalidation_registry_v0.1.json')
r=json.loads(p.read_text(encoding='utf-8'))
r['explicit_revalidations_during_deep_read_pass_2']['SMS_V2.2']={
  'SMS-001':'contextual_not_defect_executable_context_confirmed_EV-116',
  'SMS-002':'executable_confirmed_EV-116',
  'SMS-003':'context_verified',
  'SMS-004':'context_verified_pdf_reference_number_error'
}
p.write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# 5) SMS finding register: refine historical labels and append current closure
p=Path('docs/pdf_xsd_semantic_audit/SYSTEM_MONITORING_SERVICE_FINDINGS_REGISTER_ADDENDUM.md')
t=p.read_text(encoding='utf-8')
repls={
 'Status: supplemental register; first-pass closure completed for SystemMonitoringService V2.2.':'Status: supplemental register; SystemMonitoringService V2.2 has now been independently re-read and the historical SMS finding set revalidated under the current Evidence Gate.',
 'likely_source_issue: service_modelling_or_generic_response_candidate':'likely_source_issue: contextual_not_defect',
 'classification_confidence: high for observation; medium-high for intentional-modelling interpretation':'classification_confidence: high',
 'likely_source_issue: pdf_label_or_heading_error_candidate':'likely_source_issue: pdf_operation_heading_error',
 'likely_source_issue: pdf_table_or_documentation_error_candidate':'likely_source_issue: pdf_wrong_service_copy_paste',
 'mismatch_kind: unresolved\nlikely_source_issue: pdf_label_or_heading_error_candidate\nclassification_confidence: medium':'mismatch_kind: documentation_reference_number\nlikely_source_issue: pdf_reference_number_error\nclassification_confidence: high',
 'final_handling_bucket: unresolved_keep_open':'final_handling_bucket: official_pdf_documentation_clarification_candidate',
 'No executable change follows from this candidate.':'No executable XSD change follows from this documentation reference-number error.'
}
for old,new in repls.items():
    if old not in t: raise SystemExit(f'expected SMS register text missing: {old}')
    t=t.replace(old,new,1)
p.write_text(t,encoding='utf-8')
append_once(p,'## Current Evidence-Gate closure — SMS V2.2', '''## Current Evidence-Gate closure — SMS V2.2

Fresh-read freeze: `625bb9a4d19f1f1c47a529686defa9b1368c80ff`.

Executable evidence: `EV-116`, run `33269006407`, job `99144006184`, PASS on the exact official VDV-301-2.2 family.

```text
SMS-001 -> contextual_not_defect_executable_context_confirmed_EV-116
SMS-002 -> executable_confirmed_EV-116
SMS-003 -> context_verified
SMS-004 -> context_verified_pdf_reference_number_error
```

`SMS-001` remains an intentional modelling note: generic Subscribe/Unsubscribe structures live in Common V2.2 and no service-specific subscription roots are invented. `SMS-002` is executable-constrained because the real `GetServiceStatusResponse` validates while invented `GetSystemStatusResponse` has no global declaration. `SMS-004` is no longer unresolved: the same official PDF identifies the old Base Services source as VDV 301-2-0, consistent with the official publication catalog.

### DRSMS22-001 — printed broken cross-reference

State: `context_verified`. Page 5 visibly contains `Fehler! Textmarke nicht definiert.` in the list-of-figures area. Documentation-generation defect; no executable effect.

### DRSMS22-002 — ServiceStatus prose describes device state

State: `context_verified_with_exact_common_type_semantics`. ServiceStatus tables use device-state wording even though exact Common V2.2 models `ServiceIdentificationWithState` as `ServiceIdentification` + `ServiceState`. PDF semantic/copy-paste defect; no XSD change.

### DRSMS22-003 — SystemManagementService spelling

State: `context_verified`. Version history spells the service `SystemManagmentService`; the reference section uses the correct name. Editorial PDF defect only.

### DRSMS22-004 — missing Req./Resp. labels

State: `context_verified`. The UnsubscribeServiceStatus row contains the request and response structures but omits the visible `Req.`/`Resp.` labels present for neighboring operations. Documentation-table omission only.

### Common-lane guard

CE-012, CE-018 and CE-019 remain outside this SMS closure. EV-116 observes the exact Common V2.2 declarations only as routing/executable context and does not revalidate those Common PDF findings.''')

# 6) deep-read report reconciliation appendix
p=Path('docs/pdf_xsd_semantic_audit/deep_read/SMS_V2.2.md')
append_once(p,'## Historical SMS reconciliation after fresh-read freeze', '''## Historical SMS reconciliation after fresh-read freeze

The independent SMS V2.2 source state was frozen in commit `625bb9a4d19f1f1c47a529686defa9b1368c80ff` before the historical SMS finding IDs were reopened for reconciliation.

Mapping:

```text
FR-SMS22-OBS-003 -> SMS-002, confirmed PDF heading/name error; executable boundary EV-116
FR-SMS22-OBS-001 -> SMS-003, confirmed wrong-service foreword copy/paste
FR-SMS22-OBS-005 -> SMS-004, confirmed PDF reference-number error
rejected generic-subscription defect hypothesis -> SMS-001, contextual_not_defect with EV-116 support
FR-SMS22-OBS-002 -> DRSMS22-001
FR-SMS22-OBS-004 -> DRSMS22-002
FR-SMS22-OBS-006 -> DRSMS22-003
FR-SMS22-OBS-007 -> DRSMS22-004
```

EV-116 (`tools/validate_sms_v22_ev116.py`, run `33269006407`, job `99144006184`) passed on the exact official VDV-301-2.2 family and proves the executable ServiceStatus/SystemStatus boundary plus the existence of generic Common subscription structures.

CE-012, CE-018 and CE-019 are deliberately not revalidated here. They remain Common-lane findings subject to their own Evidence-Gate treatment.

SMS V2.2 historical reconciliation is complete. No XSD was changed. Next Deep Read document: `ARA_V2.4`.''')

# 7) evidence ID policy
p=Path('docs/pdf_xsd_semantic_audit/EVIDENCE_ID_POLICY.md')
t=p.read_text(encoding='utf-8')
old='EV-115  TicketValidationService V2.4 candidate/integration ShortHaul inventory + recurring type/rename behavior evidence\n'
if old not in t: raise SystemExit('EV-115 list line missing')
t=t.replace(old,old+'EV-116  SystemMonitoringService V2.2 exact operation-name/generic-subscription modelling evidence\n',1)
t=t.replace('EV-001, EV-002 and EV-101 through EV-115','EV-001, EV-002 and EV-101 through EV-116')
anchor='EV-115 PASS is candidate/integration evidence and must never be described as official-release V2.4 XSD conformance.\n```'
if anchor not in t: raise SystemExit('EV-115 authority guard anchor missing')
ev116='''EV-115 PASS is candidate/integration evidence and must never be described as official-release V2.4 XSD conformance.\n\nEV-116:\nThe checked SystemMonitoringService V2.2 family is exact official VDV-301-2.2 authority:\n  SystemMonitoringService d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c\n  Common V2.2             468fee6d177e7185dbcd5d3f90cfb114e29e01ae\n  Enums V2.2              2a23b512379b18e8f122ac1272cef8229fb86283\nEV-116 proves the service-local Get response naming boundary, validates GetServiceStatusResponse, rejects invented GetSystemStatusResponse, and confirms the generic Common Subscribe/Unsubscribe structures used by the PDF.\nIts observation of Common list-item minOccurs=0 is routing context only and does not revalidate CE-012, CE-018, CE-019 or any Common PDF interpretation.\n```'''
t=t.replace(anchor,ev116,1)
p.write_text(t,encoding='utf-8')

# 8) validation backlog
p=Path('docs/pdf_xsd_semantic_audit/validation_backlog.md')
t=p.read_text(encoding='utf-8')
t=t.replace('includes EV-115 for TicketValidationService V2.4 candidate/integration structure and behavior, with an explicit non-release authority guard.','includes EV-116 for exact official SystemMonitoringService V2.2 operation-name/generic-subscription evidence, while EV-115 retains its explicit non-release authority guard.',1)
old='EV-115           run 33265239836  PASS  candidate/integration TVS V2.4 ShortHaul inventory + recurring type/rename behavior; NOT official-release conformance\n'
if old not in t: raise SystemExit('EV-115 backlog line missing')
t=t.replace(old,old+'EV-116           run 33269006407  PASS  official SMS V2.2 ServiceStatus naming + generic Common subscription modelling evidence\n',1)
t=t.replace('EV-110 through EV-115 are targeted additive tests','EV-110 through EV-116 are targeted additive tests',1)
p.write_text(t,encoding='utf-8')
append_once(p,'## SystemMonitoringService V2.2 Deep Read / EV-116 evidence status', '''## SystemMonitoringService V2.2 Deep Read / EV-116 evidence status

```text
PDF sha256: 996f639a81cb91ad20a8e78b6213e7c85d41ff0ec42caba4208d6c4652b140f4
PDF size: 847416
pin run: 33268541691
render/read run: 33268591224
fresh-read freeze: 625bb9a4d19f1f1c47a529686defa9b1368c80ff
EV-116 run: 33269006407 PASS
EV-116 job: 99144006184
```

Current SMS result:

```text
SMS-001 contextual_not_defect; generic Common subscription modelling; EV-116 support
SMS-002 executable_confirmed_EV-116; PDF SystemStatus headings conflict with executable ServiceStatus naming
SMS-003 context_verified; unrelated HTMLDisplayService foreword copy/paste
SMS-004 context_verified; VDV 302-2 reference-number error
DRSMS22-001 context_verified; printed broken cross-reference
DRSMS22-002 context_verified; ServiceStatus/device-state prose copy/paste
DRSMS22-003 context_verified; SystemManagmentService spelling
DRSMS22-004 context_verified; missing Req./Resp. table labels
```

CE-012, CE-018 and CE-019 remain in the Common lane and are not revalidated by EV-116 or this service closure.

SMS V2.2 Deep Read/reconciliation is complete. Next document: `ARA_V2.4`.''')

# 9) CURRENT_STATE
p=Path('00_START_HERE/CURRENT_STATE.json')
s=json.loads(p.read_text(encoding='utf-8')); a=s['audit']
a['deep_read_in_progress']=0
a['deep_read_current_document_id']=None
a['deep_read_previous_document_id']='SMS_V2.2'
a['next_natural_deep_read_document_id']=NEXT
a['latest_deep_read_finding']='DRSMS22-004'
a['latest_deep_read_revalidation']='SMS-002_executable_confirmed_EV-116_SMS-001_contextual_not_defect_EV-116'
a['latest_deep_read_findings_delta']='audit_registry/deep_read_findings_delta_sms_v22_2026-08-29.json'
a['sms_v2_2_fresh_read_status']='historical_reconciliation_complete'
a['sms_v2_2_findings']={
 'SMS-001':'contextual_not_defect_executable_context_confirmed_EV-116',
 'SMS-002':'executable_confirmed_EV-116',
 'SMS-003':'context_verified',
 'SMS-004':'context_verified_pdf_reference_number_error',
 'DRSMS22-001':'context_verified',
 'DRSMS22-002':'context_verified_with_exact_common_type_semantics',
 'DRSMS22-003':'context_verified',
 'DRSMS22-004':'context_verified'
}
a['sms_v2_2_executable_evidence']={'evidence_id':'EV-116','checker':EV_CHECKER,'run':EV_RUN,'job':EV_JOB,'status':'PASS','authority':'official_VDV-301-2.2_exact_family'}
a['sms_v2_2_common_lane_not_revalidated']=['CE-012','CE-018','CE-019']
p.write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

# 10) handoff delta
Path('docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_SMS_V22_DEEP_READ_2026-08-29.md').write_text('''# Audit handoff delta — SystemMonitoringService V2.2 Deep Read

Date: 2026-08-29

## Permanent result

- SMS V2.2 official PDF pinned: `996f639a81cb91ad20a8e78b6213e7c85d41ff0ec42caba4208d6c4652b140f4`, 847416 bytes, run `33268541691`.
- Exact official XSD family: SMS `d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c`, Common `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`, Enums `2a23b512379b18e8f122ac1272cef8229fb86283`.
- Full render/read: run `33268591224`, job `99142914429`; fresh-read freeze `625bb9a4d19f1f1c47a529686defa9b1368c80ff`.
- EV-116: checker `tools/validate_sms_v22_ev116.py`, run `33269006407`, job `99144006184`, PASS on exact official authority.
- SMS-001 revalidated as contextual non-defect/generic Common subscription modelling.
- SMS-002 executable-confirmed: PDF SystemStatus headings conflict with exact ServiceStatus operation/root naming.
- SMS-003 context-verified wrong-service foreword copy/paste.
- SMS-004 upgraded from unresolved to context-verified PDF reference-number error.
- New findings: DRSMS22-001 broken cross-reference, DRSMS22-002 ServiceStatus/device-state prose copy-paste, DRSMS22-003 spelling error, DRSMS22-004 Req./Resp. label omission.
- CE-012, CE-018 and CE-019 are not revalidated by this SMS closure and stay in the Common lane.
- No XSD changed.

## Next

Start `ARA_V2.4` (AnalogRadioService V2.4, VDV 301-2-19) document-first: own official PDF pin, exact authority classification/family, fresh read before historical AnalogRadio finding reconciliation.
''',encoding='utf-8')

# JSON sanity and critical assertions
for q in [
 Path('audit_registry/deep_read_findings_delta_sms_v22_2026-08-29.json'),
 Path('audit_registry/deep_read_registry_delta_sms_v22_2026-08-29.json'),
 Path('audit_registry/finding_revalidation_registry_v0.1.json'),
 Path('00_START_HERE/CURRENT_STATE.json')]:
    json.loads(q.read_text(encoding='utf-8'))
assert s['audit']['next_natural_deep_read_document_id']=='ARA_V2.4'
assert s['audit']['deep_read_in_progress']==0
assert 'SMS_V2.2' in r['explicit_revalidations_during_deep_read_pass_2']
print('SMS_V2.2_FINALIZER_OK')
