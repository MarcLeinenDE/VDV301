#!/usr/bin/env python3
from __future__ import annotations
import json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def load(p): return json.loads((ROOT/p).read_text(encoding='utf-8'))
def dump(p,obj):
    path=ROOT/p; path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n",encoding='utf-8')
def need(v,m):
    if not v: raise RuntimeError(m)
    print('OK ',m)

STATE=Path('00_START_HERE/CURRENT_STATE.json')
REG=Path('audit_registry/deep_read_registry_delta_common_v23_2026-09-02.json')
FIND=Path('audit_registry/deep_read_findings_delta_common_v23_2026-09-02.json')
V22=Path('audit_registry/deep_read_findings_delta_common_v22_2026-09-02.json')
REGISTER=Path('docs/pdf_xsd_semantic_audit/COMMON_FINDINGS_REGISTER_ADDENDUM.md')
OLDREP=Path('docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.3.md')
FRESH=Path('docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.3_FRESH_2026-09-02.md')
HAND=Path('docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_COMMON_V23_DEEP_READ_2026-09-02.md')
CORR=Path('docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_COMMON_V23_CE023_SCOPE_2026-09-02.md')

# Guard starting state.
s=load(STATE); a=s['audit']
need(a['deep_read_needs_visual_review']==35,'start visual counter 35')
need(a['deep_read_textual_fresh_read_completed']==35,'start fresh counter 35')
need(a['deep_read_in_progress']==0,'no unit marked in progress before closure')
need(a['next_natural_deep_read_document_id']=='COMMON_V2.3','next unit is COMMON_V2.3')
need(a['latest_deep_read_finding']=='DRCOM22-001','starting latest Common finding is DRCOM22-001')
need((ROOT/FRESH).exists(),'fresh V2.3 freeze report exists')
need(not (ROOT/FIND).exists(),'V2.3 findings delta not already present')
need(not (ROOT/HAND).exists(),'V2.3 handoff not already present')
need(not (ROOT/CORR).exists(),'V2.3 CE-023 correction not already present')

# Final findings mapping.
mapping={
 'FR-COM23-001':['CE-020'],
 'FR-COM23-002':['DRCOM22-001'],
 'FR-COM23-003':['CE-013'],
 'FR-COM23-004':['CE-011'],
 'FR-COM23-005':['DRCOM10-002'],
 'FR-COM23-006':['CE-014','CE-012','CE-018','DRCOM10-003'],
 'FR-COM23-007':['CE-026','CE-015','CE-016','CE-021','CE-025','CE-017'],
 'FR-COM23-008':['DRCOM10-004'],
 'FR-COM23-009':['CE-022','CE-019'],
 'FR-COM23-010':['DRCOM10-005'],
 'FR-COM23-011':['DRCOM21-001','DRCOM23-001'],
 'FR-COM23-012':['CE-005'],
 'FR-COM23-013':['CE-024'],
 'FR-COM23-014':['CE-006','CE-004','DRCOM10-006','CE-007','CE-008','CE-009','CE-010'],
 'FR-COM23-015':['DRCOM10-007'],
 'FR-COM23-016':['DRCOM10-007'],
}
reval={
 'CE-004':'V2.3_scope_exact_EnumsV2.2_excludes_stale_SystemDocumentationService_SystemManagementService_and_keeps_SystemMonitoringService_EV-121',
 'CE-005':'V2.3_scope_executable_base_and_numbered_AdditionalTextMessage_each_0to1_EV-121',
 'CE-006':'V2.3_scope_exact_EnumsV2.2_contains_DeviceState_warning_while_pdf_omits_it_EV-121',
 'CE-007':'V2.3_scope_executable_GNSS_TicketValidation_VehicleMode_case_boundaries_EV-121',
 'CE-008':'V2.3_scope_executable_checked_NeTEx_submode_case_boundaries_including_Funicular_Taxi_EV-121',
 'CE-009':'V2.3_scope_executable_RailSubmode_specialRail_vs_specialTrain_EV-121',
 'CE-010':'V2.3_scope_executable_AirSubmode_canalBarge_present_in_exact_EnumsV2.2_EV-121',
 'CE-011':'V2.3_scope_executable_Connection_TransportMode_ConnectionMode_0to1_vs_pdf_0star_EV-121',
 'CE-012':'V2.3_scope_executable_empty_DeviceSpecificationWithStateList_EV-121',
 'CE-013':'V2.3_scope_executable_optional_AdditionalAnnouncement_choice_and_SpecificPoint_name_EV-121',
 'CE-014':'V2.3_scope_executable_empty_DataVersionList_EV-121',
 'CE-015':'V2.3_scope_visible_FareZone_case_boundaries_plus_exact_XSD_EV-121',
 'CE-016':'V2.3_scope_executable_GlobalCardStausID_boundary_EV-121',
 'CE-017':'V2.3_scope_executable_TSPPoint_Description_vs_Desciption_EV-121',
 'CE-018':'V2.3_scope_visible_1star_plus_executable_empty_ServiceIdentificationWithStateList_EV-121',
 'CE-019':'V2.3_scope_visible_type_reference_plus_exact_ServiceIdentificationWithStateStructure_EV-121',
 'CE-020':'V2.3_official_primitive_InternationalText_shape_confirmed_EV-121_PR30_collision_identity_remains_separate',
 'CE-021':'V2.3_scope_executable_MessageBody_vs_Message_boundary_EV-121',
 'CE-022':'V2.3_scope_executable_outer_ServiceName_vs_Service_boundary_EV-121',
 'CE-024':'V2.3_scope_executable_UnsubscribeResponse_Active_required_EV-121',
 'CE-025':'V2.3_scope_executable_Reply-Path_vs_ReplyPath_EV-121',
 'CE-026':'V2.3_scope_executable_BeaconPoint_Description_vs_Desciption_EV-121',
 'DRCOM10-002':'V2.3_scope_executable_DataAcceptedResponse_choice_boundary_EV-121',
 'DRCOM10-003':'V2.3_scope_executable_empty_ServiceSpecificationWithStateList_EV-121',
 'DRCOM10-004':'V2.3_scope_executable_JourneyStop_Announcement_FareZone_0to1_EV-121',
 'DRCOM10-005':'V2.3_scope_child_name_facet_persists_exact_XSD_EV-121',
 'DRCOM10-006':'V2.3_scope_executable_DoorCountingObjectClass_lexemes_EV-121',
 'DRCOM10-007':'V2.3_scope_context_verified_GNSS_identifier_and_grouped_editorial_residue',
 'DRCOM21-001':'V2.3_scope_executable_StopInformationRequest_StopName_0star_EV-121',
 'DRCOM22-001':'V2.3_scope_executable_NetexMode_optional_choices_empty_valid_EV-121',
}
findings={
 'delta_version':'0.1','date':'2026-09-02','document_id':'COMMON_V2.3',
 'fresh_read_freeze':'885905349b9812b64a92b9f6d27d211fe9f2aa14',
 'source_evidence':{'pdf_sha256':'d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b','size_bytes':793521,'pin_render_read_run':'33656579631','job':'100336514663','artifact_id':'9856965744','artifact_digest':'sha256:a3c0a59cf1a5e6ca8a98c7419c5f02e1445efa503b6986c62daa2f53171eb746','page_count':58,'fulltext_sha256':'c0ac2f22f0d4cf155d601d26c9c550214d7db221c0ce185eaeba26df27149c16'},
 'exact_xsd_authority':{'official_tag':'VDV-301-2.3','common_blob':'0d8926c4063c12de9a5e68b6f0addaab35a55dc1','enumerations_file':'IBIS-IP_Enumerations_V2.2.xsd','enumerations_blob':'2a23b512379b18e8f122ac1272cef8229fb86283','branch_bytes_match_official_tag':True},
 'executable_evidence':{'evidence_id':'EV-121','checker':'tools/validate_common_v23_ev121.py','run':'33657653888','job':'100340112497','head_tested':'3ca203156e2a6791c7757470e2cf4549f604ad0d','result':'PASS','authority':'exact_official_VDV-301-2.3_Common_plus_declared_Enumerations_V2.2'},
 'observation_to_finding_mapping':mapping,
 'revalidated_or_scope_extended_findings':reval,
 'new_unique_findings':{'DRCOM23-001':{'state':'executable_confirmed_EV-121','classification':'pdf_documents_elements_absent_from_xsd','summary':'COMMON V2.3 PDF documents ArrivalExpected and DepartureExpected as optional members of StopInformationRequest and the V2.3 history references section 2.52, while exact official StopInformationRequestStructure contains neither. EV-121 rejects either field in StopInformationRequest and accepts both in StopInformationStructure.','executable_effect':True}},
 'historical_corrections':{'CE-023':{'decision':'remove_COMMON_V2.3_from_affected_scope','reason':'fresh exact pinned V2.3 page 26 shows NetexMode heading and descriptive prose only; no duplicate Message table. Earlier native-text interpretation is rejected for V2.3. V2.2 remains confirmed affected.','correction_doc':str(CORR)},'V2.2_CE004_CE006_labels':{'decision':'correct_swapped_revalidation_descriptions','CE-004':'stale removed ServiceName values','CE-006':'DeviceState warning omitted from PDF'}},
 'explicit_non_extension':{'CE-023':'not mapped to any FR-COM23 observation; V2.3 scope is actively removed after visible-source falsification'},
 'active_falsification':['-1:1 is XML choice notation, not negative cardinality','PointType required choice aligns','AdditionalInformation(n) shorthand aligns with explicit AdditionalInformation1..9','StopInformation expected fields align; absence is specifically StopInformationRequest','exact pinned V2.3 page 26 falsifies prior duplicate NetexMode/Message-table interpretation','enumeration ordering ignored','no XSD change proposed or performed'],
 'next_natural_document_id':'COMMON_V2.4'
}
dump(FIND,findings)

# Registry closure.
r=load(REG); d=r['document_updates']['COMMON_V2.3']
need(d['fresh_read_freeze']['observation_count']==16,'V2.3 freeze has 16 observations')
d['state']='historical_reconciliation_complete_executable_evidence_pass'
d['historical_common_findings_quarantined_until_fresh_read_freeze']=True
d['fresh_read_freeze'].update({'status':'frozen','freeze_commit':'885905349b9812b64a92b9f6d27d211fe9f2aa14','historical_reconciliation_started':True,'historical_reconciliation_completed':True,'executable_evidence_status':'EV-121_PASS','xsd_modified':False})
d['executable_evidence']={'evidence_id':'EV-121','checker':'tools/validate_common_v23_ev121.py','run':'33657653888','job':'100340112497','head_tested':'3ca203156e2a6791c7757470e2cf4549f604ad0d','result':'PASS','authority':'exact_official_VDV-301-2.3_Common_plus_declared_Enumerations_V2.2'}
d['historical_reconciliation']={'status':'complete','findings_delta':str(FIND),'revalidated_or_scope_extended_count':len(reval),'new_unique_findings':['DRCOM23-001'],'corrections':['CE-023 V2.3 scope removed after visible-source falsification','V2.2 CE-004/CE-006 revalidation labels corrected'],'next_natural_document_id':'COMMON_V2.4'}
d['next_after_freeze']='complete'; dump(REG,r)

# Correct swapped labels in V2.2 machine-readable delta.
v=load(V22); rr=v['revalidated_or_scope_extended_findings']
need('CE-004' in rr and 'CE-006' in rr,'V2.2 delta has CE-004 and CE-006')
rr['CE-004']='V2.2_scope_exact_EnumsV2.2_excludes_stale_SystemDocumentationService_SystemManagementService_and_keeps_SystemMonitoringService_EV-120'
rr['CE-006']='V2.2_scope_exact_EnumsV2.2_contains_DeviceState_warning_while_pdf_omits_it_EV-120'
v.setdefault('corrections',{})['2026-09-02_COMMON_V2.3_reconciliation']='CE-004/CE-006 revalidation descriptions were swapped; identities corrected without changing observation mapping.'
dump(V22,v)

# Correct CE-023 register block.
p=ROOT/REGISTER; txt=p.read_text(encoding='utf-8')
pat=r'## CE-023 - .*?(?=\n## CE-024 -)'
m=re.search(pat,txt,flags=re.S); need(m is not None,'CE-023 block found exactly for replacement')
new='''## CE-023 - Common V2.2 duplicate/corrupt second NetexMode table\n\nState: V2.2 PDF copy/paste table error confirmed; prior V2.3 scope withdrawn after fresh exact visible-source falsification.\n\nClassification:\n\n```text\nmismatch_kind: duplicate_or_copy_paste_table\nlikely_source_issue: pdf_table_error_candidate\nclassification_confidence: high for V2.2\nversion_scope: Common V2.2 confirmed affected; Common V2.3 removed from affected scope; Common V2.4 not affected\nvalidation_behavior: no XSD defect implied\nfinal_handling_bucket: documentation_correction_candidate\n```\n\nV2.2 evidence:\n\n```text\nThe independently frozen Common V2.2 read confirms section 2.34 is a corrupt duplicate NetexMode table carrying Message structure content.\nValidation continues to follow the exact V2.2 XSD NetexMode model.\n```\n\nV2.3 correction evidence:\n\n```text\nFresh exact official Common V2.3 PDF SHA-256:\nd59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b\nrender/read run: 33656579631\nartifact: 9856965744\nvisible page 26: section 2.34 NetexMode contains the NetexMode heading and descriptive prose only; it does NOT contain a duplicate Message table.\n```\n\nDecision:\n\n```text\nThe earlier V2.3 native-text interpretation is rejected for V2.3.\nDo not carry CE-023 into Common V2.3.\nV2.2 remains the confirmed affected version.\nNo XSD change is implied.\n```\n'''
txt=txt[:m.start()]+new+txt[m.end():]; p.write_text(txt.rstrip()+"\n",encoding='utf-8')

# Mark old reconnaissance report as superseded for V2.3 scope decisions.
op=ROOT/OLDREP; old=op.read_text(encoding='utf-8')
marker='> **Superseded for COMMON V2.3 scope decisions on 2026-09-02.**'
if marker not in old:
    old=marker+' The independent source-only freeze `COMMON_V2.3_FRESH_2026-09-02.md` plus EV-121 supersedes this earlier reconnaissance. In particular, its old duplicate-NetexMode-table interpretation is rejected by the exact pinned visible V2.3 page 26.\n\n'+old
op.write_text(old.rstrip()+"\n",encoding='utf-8')

# Correction document.
corr='''# Audit correction delta — COMMON V2.3 CE-023 scope — 2026-09-02\n\n## Correction\n\n`CE-023` previously carried Common V2.3 in the affected range for a supposed duplicate/corrupt second NetexMode table. The independent Fresh Read of the exact official V2.3 publication falsifies that V2.3 claim.\n\n- Exact V2.3 PDF SHA-256: `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`.\n- Fresh render/read run: `33656579631`.\n- Artifact: `9856965744`.\n- Visible page 26, section 2.34: NetexMode heading and descriptive prose only; no duplicate Message table.\n- Fresh freeze: `885905349b9812b64a92b9f6d27d211fe9f2aa14`.\n\n## Result\n\n`CE-023` is now scoped to **Common V2.2 only** in the checked V2.2–V2.4 chain. V2.3 is explicitly removed from the affected scope; V2.4 is not affected. The prior V2.3 native-text interpretation is rejected.\n\nThis correction changes audit metadata/documentation only. No XSD is modified.\n'''
(ROOT/CORR).write_text(corr,encoding='utf-8')

# Handoff.
hand='''# Audit handoff delta — COMMON V2.3 Deep Read — 2026-09-02\n\n## Completed block\n\n`COMMON_V2.3` is closed for Deep Read Pass 2 as `needs_visual_review` with historical reconciliation complete.\n\n- Independent source-only freeze: `885905349b9812b64a92b9f6d27d211fe9f2aa14`.\n- Official PDF SHA-256: `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`; 793,521 bytes; 58 pages.\n- Fresh pin/render/read run: `33656579631`, job `100336514663`, artifact `9856965744`.\n- Exact authority: official `VDV-301-2.3` Common blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` plus its declared Enumerations V2.2 blob `2a23b512379b18e8f122ac1272cef8229fb86283`.\n- EV-121: PASS, run `33657653888`, job `100340112497`, checker `tools/validate_common_v23_ev121.py`.\n- New unique finding: `DRCOM23-001` — PDF documents `ArrivalExpected` and `DepartureExpected` in `StopInformationRequest`, while exact official `StopInformationRequestStructure` contains neither; EV-121 rejects both there and accepts both in `StopInformation`.\n- Remaining frozen observations map to existing Common identities; exact mapping is in `audit_registry/deep_read_findings_delta_common_v23_2026-09-02.json`.\n\n## Audit corrections discovered\n\n- `CE-023`: V2.3 removed from affected scope. Exact pinned page 26 has no duplicate Message table under NetexMode. V2.2 remains confirmed affected.\n- V2.2 machine-readable CE-004/CE-006 revalidation descriptions were swapped and are corrected: CE-004 = stale removed ServiceName values; CE-006 = DeviceState `warning` omitted from PDF.\n\n## Guardrails\n\n- No XSD changed.\n- Exact selected XSD family remains executable authority.\n- `-1:1` is VDV choice notation.\n- V2.3 officially reuses Enumerations V2.2; do not latest-wins substitute V2.4.\n- Historical reconnaissance does not override the independent fresh source freeze.\n\n## Next natural unit\n\n`COMMON_V2.4`.\n'''
(ROOT/HAND).write_text(hand,encoding='utf-8')

# Update current state.
a['deep_read_needs_visual_review']=36; a['deep_read_textual_fresh_read_completed']=36; a['deep_read_in_progress']=0
a['deep_read_current_document_id']='COMMON_V2.3'; a['deep_read_previous_document_id']='COMMON_V2.3'; a['next_natural_deep_read_document_id']='COMMON_V2.4'
a['latest_deep_read_finding']='DRCOM23-001'; a['latest_deep_read_revalidation']='DRCOM23-001_V2.3_scope_executable_StopInformationRequest_expected_fields_absent_EV-121'; a['latest_common_finding']='DRCOM23-001'
a['latest_deep_read_registry_delta']=str(REG); a['latest_deep_read_findings_delta']=str(FIND); a['latest_audit_correction']=str(CORR)
a['common_v2_3_deep_read_report']=str(FRESH); a['common_v2_3_handoff']=str(HAND); a['common_v2_3_fresh_read_status']='historical_reconciliation_complete'
a['common_v2_3_executable_evidence']='EV-121 / 33657653888'; a['common_v2_3_findings']={'DRCOM23-001':'executable_confirmed_EV-121','CE-023':'V2.3_scope_withdrawn_after_exact_visible_source_falsification'}
if 'evidence' in s:
    e=s['evidence']; e['latest_targeted_xsd_evidence_run']='33657653888'; e['latest_targeted_xsd_evidence']='EV-121'; e['latest_pdf_source_pin_run']='33656579631'; e['latest_pdf_visual_render_run']='33656579631'; e['common_v2_3_executable_evidence']='EV-121 / 33657653888'
dump(STATE,s)

# Remove temporary workflows and this closure helper. Closure workflow removes itself too.
for rel in ['.github/workflows/temp-common-v23-pin-read.yml','.github/workflows/temp-common-v23-ev121.yml','tools/temp_close_common_v23.py']:
    q=ROOT/rel; need(q.exists(),f'temporary path exists: {rel}'); q.unlink(); print('OK  removed',rel)

print('COMMON_V23_CLOSURE_STATE_OK')
