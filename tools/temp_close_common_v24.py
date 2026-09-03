#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def p(rel): return ROOT/rel
def load(rel): return json.loads(p(rel).read_text(encoding='utf-8'))
def dump(rel,obj): p(rel).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def need(v,msg):
    if not v: raise SystemExit('FAIL '+msg)
    print('OK ',msg)

def main():
    state=load('00_START_HERE/CURRENT_STATE.json')
    a=state['audit']
    need(a['deep_read_textual_fresh_read_completed']==36,'start textual counter 36')
    need(a['deep_read_needs_visual_review']==36,'start visual counter 36')
    need(a['deep_read_in_progress']==0,'no deep read in progress')
    need(a['next_natural_deep_read_document_id']=='COMMON_V2.4','next unit COMMON_V2.4')
    need(a['latest_deep_read_finding']=='DRCOM23-001','starting latest finding DRCOM23-001')
    freeze='docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.4_FRESH_2026-09-03.md'
    need(p(freeze).exists(),'V2.4 source-only freeze exists')
    regrel='audit_registry/deep_read_registry_delta_common_v24_2026-09-03.json'
    reg=load(regrel)
    doc=reg['document_updates']['COMMON_V2.4']
    need(doc['fresh_read_freeze']['observation_count']==15,'V2.4 freeze has 15 observations')
    need(doc['fresh_read_freeze']['freeze_commit']=='789f02f697809b1eef4d3b1a366a3599649a6d7d','freeze commit exact')
    newfiles=[
      'audit_registry/deep_read_findings_delta_common_v24_2026-09-03.json',
      'docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.4.md',
      'docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_COMMON_V24_DEEP_READ_2026-09-03.md',
      'docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_COMMON_V24_INTERNATIONALTEXT_AUTHORITY_2026-09-03.md']
    for x in newfiles: need(not p(x).exists(),f'new closure path absent: {x}')

    findings={
      'delta_version':'0.1','date':'2026-09-03','document_id':'COMMON_V2.4',
      'fresh_read_freeze':'789f02f697809b1eef4d3b1a366a3599649a6d7d',
      'source_evidence':{
        'pdf_sha256':'01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a','size_bytes':1689647,
        'pin_render_read_run':'33658306978','job':'100342316111','artifact_id':'9857652638',
        'artifact_digest':'sha256:be0ce46c03893d79b216c92e7af8cd2906b27524f9d24a954be5d7e1d57d934c','page_count':63,
        'fulltext_sha256':'02bfe01587937052f0d9b1c4a581a7a0546b6a3ca024de94310c6894646929b1'},
      'selected_xsd_authority':{
        'status':'candidate_integration_explicit_selection','release_tag':None,
        'common_blob':'1946fd37e29ced605654f49ea3d98cd2fbbdc8e4','enumerations_blob':'2afed8cf23afa91db92b0f043cc5b4ad428b0f25',
        'common_includes':'IBIS-IP_Enumerations_V2.4.xsd','candidate_branch':'candidate/dms-v2.4-xsd','upstream_draft_pr':'VDVde/VDV301#31',
        'official_release_authority':False,'latest_xsd_wins':False},
      'executable_evidence':{'evidence_id':'EV-122','checker':'tools/validate_common_v24_ev122.py','run':'33716645876','job':'100527119224','head_tested':'50811251d855e02aa7decc7a1c82fa2444d2ac39','result':'PASS','authority':'exact_selected_candidate_integration_Common_V2.4_plus_Enumerations_V2.4'},
      'observation_to_finding_mapping':{
        'FR-COM24-001':['DRCOM20-001'],'FR-COM24-002':['DRCOM22-001'],'FR-COM24-003':['CE-013'],'FR-COM24-004':['CE-011'],
        'FR-COM24-005':['DRCOM10-002'],'FR-COM24-006':['CE-014','CE-012','CE-018','DRCOM10-003'],
        'FR-COM24-007':['DRCOM10-004','DRCOM21-001','CE-005','CE-024'],'FR-COM24-008':['DRCOM24-001'],
        'FR-COM24-009':['CE-015','CE-016','CE-021','CE-017'],'FR-COM24-010':['CE-022','CE-019'],
        'FR-COM24-011':['DRCOM10-005'],'FR-COM24-012':['CE-006','CE-004'],'FR-COM24-013':['CE-007','CE-008','CE-009','CE-010'],
        'FR-COM24-014':['CE-002','DRCOM10-007'],'FR-COM24-015':['DRCOM10-007']},
      'revalidated_or_scope_extended_findings':{
        'DRCOM20-001':'V2.4_candidate_scope_executable_InternationalText_native_xs_string_language_vs_PDF_wrapper_references_EV-122',
        'DRCOM22-001':'V2.4_candidate_scope_executable_NetexMode_optional_choices_empty_valid_EV-122',
        'CE-013':'V2.4_candidate_scope_executable_AdditionalAnnouncement_optional_choice_and_SpecificPoint_name_EV-122',
        'CE-011':'V2.4_candidate_scope_executable_Connection_TransportMode_ConnectionMode_0to1_vs_pdf_0star_EV-122',
        'DRCOM10-002':'V2.4_candidate_scope_executable_DataAcceptedResponse_choice_boundary_EV-122',
        'CE-014':'V2.4_candidate_scope_executable_empty_DataVersionList_EV-122','CE-012':'V2.4_candidate_scope_executable_empty_DeviceSpecificationWithStateList_EV-122',
        'CE-018':'V2.4_candidate_scope_visible_1star_plus_executable_empty_ServiceIdentificationWithStateList_EV-122',
        'DRCOM10-003':'V2.4_candidate_scope_executable_empty_ServiceSpecificationWithStateList_EV-122',
        'DRCOM10-004':'V2.4_candidate_scope_executable_JourneyStop_Announcement_FareZone_0to1_EV-122',
        'DRCOM21-001':'V2.4_candidate_scope_executable_StopInformationRequest_StopName_0star_EV-122',
        'CE-005':'V2.4_candidate_scope_executable_base_AdditionalTextMessage_0to1_EV-122','CE-024':'V2.4_candidate_scope_executable_UnsubscribeResponse_Active_required_EV-122',
        'CE-015':'V2.4_candidate_scope_executable_FareZone_case_boundaries_EV-122','CE-016':'V2.4_candidate_scope_executable_GlobalCardStausID_boundary_EV-122',
        'CE-021':'V2.4_candidate_scope_executable_MessageBody_vs_Message_boundary_EV-122','CE-017':'V2.4_candidate_scope_executable_TSPPoint_Description_vs_Desciption_EV-122',
        'CE-022':'V2.4_candidate_scope_executable_outer_ServiceName_vs_Service_boundary_EV-122','CE-019':'V2.4_candidate_scope_exact_ServiceIdentificationWithStateStructure_EV-122',
        'DRCOM10-005':'V2.4_candidate_scope_executable_ShortTripStop_child_name_boundary_EV-122',
        'CE-006':'V2.4_candidate_scope_exact_Enums_contains_DeviceState_warning_while_PDF_omits_it_EV-122','CE-004':'V2.4_candidate_scope_exact_Enums_excludes_stale_SystemDocumentationService_SystemManagementService_EV-122',
        'CE-007':'V2.4_candidate_scope_executable_GNSS_TicketValidation_VehicleMode_case_boundaries_EV-122','CE-008':'V2.4_candidate_scope_executable_checked_NeTEx_submode_case_boundaries_EV-122',
        'CE-009':'V2.4_candidate_scope_executable_RailSubmode_specialRail_vs_specialTrain_EV-122','CE-010':'V2.4_candidate_scope_executable_AirSubmode_canalBarge_present_EV-122',
        'CE-002':'V2.4_source_context_revalidated_StopPointNumber_history_wording_vs_PointNumber_table_and_candidate_XSD',
        'DRCOM10-007':'V2.4_source_context_revalidated_grouped_cross_reference_and_editorial_residue'},
      'new_unique_findings':{
        'DRCOM24-001':{'state':'executable_confirmed_EV-122','classification':'pdf_xsd_type_shape_and_cardinality_mismatch','summary':'COMMON V2.4 PDF LineInformation documents LineName and LineShortName as IBIS-IP.string 0:1, while the exact selected candidate XSD models both as repeatable InternationalTextType. EV-122 confirms candidate InternationalText instances and repetition are valid while the PDF-shaped value-only form is invalid.','executable_effect':True,'authority_scope':'selected_candidate_integration_V2.4_only_until_official_release_exists'}},
      'historical_scope_corrections':{
        'DRCOM23-001':{'decision':'do_not_extend_to_V2.4','reason':'V2.4 PDF and selected candidate XSD both contain optional StopInformationRequest.ArrivalExpected and DepartureExpected; EV-122 positive.'},
        'CE-025':{'decision':'do_not_extend_to_V2.4','reason':'V2.4 PDF and candidate XSD use ReplyPath; EV-122 accepts ReplyPath and rejects old Reply-Path.'},
        'CE-026':{'decision':'do_not_extend_to_V2.4','reason':'V2.4 BeaconPoint uses Description in PDF and candidate XSD; EV-122 confirms correction.'},
        'DRCOM10-006':{'decision':'do_not_extend_DoorCounting_lexeme_mismatch_to_V2.4','reason':'V2.4 PDF and candidate Enumerations use Wheelchair and Other; EV-122 confirms correction.'},
        'CE-020':{'decision':'not_mapped_to_V2.4','reason':'CE-020 is the V2.3 official-vs-PR30 same-path authority collision identity; V2.4 is a separately selected candidate/integration family.'},
        'CE-023':{'decision':'not_mapped_to_V2.4','reason':'confirmed V2.2-only duplicate NetexMode/Message documentation issue.'},
        'historical_01g_InternationalTextType':{'decision':'superseded','reason':'old V2.4 first-pass note incorrectly stated XSD uses IBIS-IP.string/language; exact selected blobs use xs:string/xs:language. Fresh freeze plus EV-122 supersede it.','correction_doc':'docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_COMMON_V24_INTERNATIONALTEXT_AUTHORITY_2026-09-03.md'}},
      'active_falsification':['-1:1 is XML choice notation, not negative cardinality','PointType required choice aligns','V2.4 StopInformationRequest expected fields align','V2.4 BeaconPoint Description aligns','V2.4 ReplyPath aligns','V2.4 DoorCounting Wheelchair aligns','enumeration ordering ignored','no XSD change proposed or performed'],
      'next_project_phase':'legacy_finding_revalidation'
    }
    dump('audit_registry/deep_read_findings_delta_common_v24_2026-09-03.json',findings)

    doc['state']='closed_needs_visual_review_candidate_integration_authority'
    doc['historical_quarantine_released_after_freeze']=True
    doc['fresh_read_freeze']['historical_reconciliation_started']=True
    doc['fresh_read_freeze']['historical_reconciliation_completed']=True
    doc['fresh_read_freeze']['executable_evidence_status']='EV-122_PASS_run_33716645876_job_100527119224'
    doc['fresh_read_freeze']['xsd_modified']=False
    doc['historical_reconciliation']={'findings_delta':'audit_registry/deep_read_findings_delta_common_v24_2026-09-03.json','new_unique_findings':['DRCOM24-001'],'scope_corrections':['DRCOM23-001','CE-025','CE-026','DRCOM10-006','CE-020','CE-023'],'stale_note_correction':'docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_COMMON_V24_INTERNATIONALTEXT_AUTHORITY_2026-09-03.md'}
    doc['executable_evidence']={'evidence_id':'EV-122','checker':'tools/validate_common_v24_ev122.py','run':'33716645876','job':'100527119224','result':'PASS','authority':'exact_selected_candidate_integration_family'}
    doc['next_after_freeze']='closed_then_legacy_finding_revalidation'
    doc['next_natural_document_id_after_closure']=None
    dump(regrel,reg)

    pins=load('audit_registry/pdf_source_pins_v0.1.json')
    need(not any(x['source_id']=='COMMON_V2.4' for x in pins['sources']),'COMMON_V2.4 pin not already present')
    pins['sources'].append({'source_id':'COMMON_V2.4','expected_sha256':'01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a','expected_size_bytes':1689647,'pinned_at_utc':'2026-09-02T17:00:20Z','deep_read_source_ready':True,'evidence_run_id':'33658306978','evidence_job_id':'100342316111','artifact_id':'9857652638','note':'Fresh official VDV PDF retrieval for final Common V2.4 Deep Read; selected XSD authority is separately candidate/integration.'})
    dump('audit_registry/pdf_source_pins_v0.1.json',pins)

    a['deep_read_needs_visual_review']=37; a['deep_read_textual_fresh_read_completed']=37; a['deep_read_in_progress']=0
    a['deep_read_current_document_id']='COMMON_V2.4'; a['deep_read_previous_document_id']='COMMON_V2.4'; a['next_natural_deep_read_document_id']=None
    a['deep_read_pass_2_status']='frozen_complete'; a['next_project_phase']='legacy_finding_revalidation'
    a['latest_deep_read_finding']='DRCOM24-001'; a['latest_deep_read_revalidation']='DRCOM24-001_V2.4_candidate_scope_LineName_LineShortName_type_shape_repeatability_EV-122'; a['latest_common_finding']='DRCOM24-001'
    a['latest_audit_correction']='docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_COMMON_V24_INTERNATIONALTEXT_AUTHORITY_2026-09-03.md'
    a['pdf_sources_byte_pinned']=31
    if 'COMMON_V2.4' not in a['pinned_active_sources']: a['pinned_active_sources'].append('COMMON_V2.4')
    a['latest_deep_read_registry_delta']=regrel; a['latest_deep_read_findings_delta']='audit_registry/deep_read_findings_delta_common_v24_2026-09-03.json'
    a['common_v2_4_deep_read_report']='docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.4.md'
    a['common_v2_4_source_freeze']=freeze
    a['common_v2_4_authority']={'status':'candidate_integration_explicit_selection','common_blob':'1946fd37e29ced605654f49ea3d98cd2fbbdc8e4','enumerations_blob':'2afed8cf23afa91db92b0f043cc5b4ad428b0f25','upstream_draft_pr':'VDVde/VDV301#31','official_release_tag':None}
    a['legacy_finding_revalidation_state']='ready_after_deep_read_pass_2_freeze'
    state['date']='2026-09-03'; state['project_phase']='legacy_finding_revalidation'
    dump('00_START_HERE/CURRENT_STATE.json',state)

    report='''# COMMON V2.4 — Deep Read closure\n\nDate: 2026-09-03  \nState: **closed / needs_visual_review**  \nAuthority: **selected candidate/integration V2.4 family; not an official release tag**\n\n## Frozen source basis\n\nThe immutable source-only observation set is `COMMON_V2.4_FRESH_2026-09-03.md`, frozen by commit `789f02f697809b1eef4d3b1a366a3599649a6d7d` before historical reconciliation. The official PDF is SHA-256 `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`, 1,689,647 bytes, 63 pages. Run `33658306978` rendered all pages; all 63 page hashes were rechecked.\n\nSelected executable schema family:\n\n- Common blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`\n- Enumerations blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`\n- bytes match branch `candidate/dms-v2.4-xsd` / open draft `VDVde/VDV301#31`\n- no official `VDV-301-2.4` tag exists\n- therefore candidate/integration authority is explicit and must not be relabelled official\n\n## Historical reconciliation\n\n| Frozen group | Finding identity | Decision |\n|---|---|---|\n| FR-COM24-001 | DRCOM20-001 | persists in selected candidate family |\n| FR-COM24-002 | DRCOM22-001 | persists |\n| FR-COM24-003 | CE-013 | persists |\n| FR-COM24-004 | CE-011 | persists |\n| FR-COM24-005 | DRCOM10-002 | persists |\n| FR-COM24-006 | CE-014 / CE-012 / CE-018 / DRCOM10-003 | persists |\n| FR-COM24-007 | DRCOM10-004 / DRCOM21-001 / CE-005 / CE-024 | persists |\n| FR-COM24-008 | **DRCOM24-001** | **new unique finding** |\n| FR-COM24-009 | CE-015 / CE-016 / CE-021 / CE-017 | persists; Beacon/ReplyPath older findings explicitly excluded |\n| FR-COM24-010 | CE-022 / CE-019 | persists |\n| FR-COM24-011 | DRCOM10-005 | persists |\n| FR-COM24-012 | CE-006 / CE-004 | persists |\n| FR-COM24-013 | CE-007 / CE-008 / CE-009 / CE-010 | persists; old DoorCounting mismatch fixed |\n| FR-COM24-014 | CE-002 / DRCOM10-007 | history/cross-reference residue |\n| FR-COM24-015 | DRCOM10-007 | grouped editorial residue |\n\n## DRCOM24-001\n\nPDF `LineInformation` documents `LineName` and `LineShortName` as `IBIS-IP.string`, `0:1`. The selected candidate XSD models both as `InternationalTextType`, `0:*`. The difference changes XML shape/type and repeatability.\n\nEV-122 is executable confirmation: run `33716645876`, job `100527119224`, checker `tools/validate_common_v24_ev122.py`. Candidate InternationalText instances and repetition validate; the PDF-shaped value-only form does not.\n\n## Scope corrections at V2.4\n\nThe Fresh Read actively prevents incorrect historical extension:\n\n- `DRCOM23-001`: V2.4 adds `ArrivalExpected` and `DepartureExpected` to `StopInformationRequest`; PDF and candidate XSD align.\n- `CE-025`: `ReplyPath` aligns in V2.4.\n- `CE-026`: `BeaconPoint.Description` aligns in V2.4.\n- `DRCOM10-006`: V2.4 DoorCounting uses `Wheelchair` / `Other`; the older lexeme mismatch is fixed.\n- `CE-020`: remains a V2.3 official-vs-PR30 authority-collision identity, not a V2.4 finding.\n- `CE-023`: remains V2.2-only.\n\n## Historical note correction\n\n`01g_common_enums_v2_4_datatypes_core_structures.md` contained a stale first-pass statement that V2.4 `InternationalTextType` used `IBIS-IP.string` / `IBIS-IP.language` in XSD. The exact selected blobs use `xs:string` / `xs:language`. The old statement is preserved only as historical provenance and superseded by the fresh freeze, EV-122, and `AUDIT_CORRECTION_DELTA_COMMON_V24_INTERNATIONALTEXT_AUTHORITY_2026-09-03.md`.\n\n## Closure\n\n- 15 frozen source-only observation groups reconciled.\n- New unique finding: `DRCOM24-001`.\n- EV-122 PASS.\n- No XSD changed.\n- Deep Read Pass 2 is frozen complete after this final planned unit.\n- Next project phase: full legacy finding revalidation under the current Evidence Gate.\n'''
    p('docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.4.md').write_text(report,encoding='utf-8')

    correction='''# Audit correction — COMMON V2.4 InternationalTextType authority — 2026-09-03\n\n## Corrected historical statement\n\nThe earlier first-pass file `01g_common_enums_v2_4_datatypes_core_structures.md` stated that the V2.4 XSD model for `InternationalTextType` used `IBIS-IP.string` and `IBIS-IP.language` and therefore aligned with the PDF table. That statement is superseded.\n\nThe exact selected V2.4 candidate/integration blobs used by the final Deep Read are:\n\n- `IBIS-IP_common_V2.4.xsd` blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`\n- `IBIS-IP_Enumerations_V2.4.xsd` blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`\n\nIn that Common blob, `InternationalTextType.Value` is `xs:string` and `Language` is `xs:language`. The official V2.4 PDF table prints the wrapper-reference names `IBIS-IP.string` and `IBIS-IP.language`. EV-122 confirms the executable shape boundary.\n\n## Authority qualification\n\nThese XSD bytes are candidate/integration authority, byte-identical to `candidate/dms-v2.4-xsd` / open draft `VDVde/VDV301#31`. They are not promoted to official release authority. No `VDV-301-2.4` release tag resolves.\n\n## Effect\n\n- The historical first-pass conclusion is retained only for provenance, not as current audit truth.\n- The authoritative current audit identity for this V2.4 boundary is `DRCOM20-001` extended/revalidated to the selected candidate scope by EV-122.\n- No XSD is modified.\n'''
    p('docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_COMMON_V24_INTERNATIONALTEXT_AUTHORITY_2026-09-03.md').write_text(correction,encoding='utf-8')

    old='docs/pdf_xsd_semantic_audit/01g_common_enums_v2_4_datatypes_core_structures.md'
    txt=p(old).read_text(encoding='utf-8')
    mark='> **Superseded audit note (2026-09-03):**'
    need(mark not in txt,'01g correction marker not already present')
    pre='''> **Superseded audit note (2026-09-03):** The historical `InternationalTextType` conclusion below is not current authority. The exact selected V2.4 candidate/integration Common blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` uses native `xs:string` / `xs:language`, while the official PDF prints `IBIS-IP.string` / `IBIS-IP.language`. See `AUDIT_CORRECTION_DELTA_COMMON_V24_INTERNATIONALTEXT_AUTHORITY_2026-09-03.md` and EV-122. Historical text is retained for provenance only.\n\n'''
    p(old).write_text(pre+txt.rstrip()+'\n',encoding='utf-8')

    handoff='''# Audit handoff delta — COMMON V2.4 Deep Read — 2026-09-03\n\n## Completed block\n\n`COMMON_V2.4` is closed as the final planned Deep Read Pass 2 unit.\n\n- source-only freeze commit: `789f02f697809b1eef4d3b1a366a3599649a6d7d`\n- official PDF SHA-256: `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`, 1,689,647 bytes, 63 pages\n- render/read run `33658306978`, job `100342316111`, artifact `9857652638`; all 63 render hashes rechecked\n- selected XSD authority is candidate/integration, not official: Common blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` + Enumerations blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`, matching open draft `VDVde/VDV301#31`\n- EV-122 PASS: run `33716645876`, job `100527119224`\n- new unique finding `DRCOM24-001`: LineName/LineShortName PDF `IBIS-IP.string 0:1` vs candidate XSD `InternationalTextType 0:*`\n\n## Scope corrections\n\nDo not extend `DRCOM23-001`, `CE-025`, `CE-026` or DoorCounting portion of `DRCOM10-006` into V2.4; the fresh source and EV-122 show those boundaries corrected. `CE-020` remains V2.3 authority-collision specific; `CE-023` remains V2.2-only.\n\nThe stale V2.4 first-pass InternationalText statement in `01g...` is explicitly superseded by a correction delta; no history is silently deleted.\n\n## Guardrails\n\n- No XSD changed.\n- Candidate/integration is not relabelled official.\n- `latest wins` remains forbidden.\n- `-1:1` remains XML choice notation.\n\n## Next phase\n\nDeep Read Pass 2 is frozen complete. Proceed with `LEGACY_FINDING_REVALIDATION_PLAN.md`: freeze the full finding inventory and revalidate every finding not already explicitly revalidated under the current Evidence Gate, requiring zero pending SDK-relevant findings before baseline freeze.\n'''
    p('docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_COMMON_V24_DEEP_READ_2026-09-03.md').write_text(handoff,encoding='utf-8')

    register='docs/pdf_xsd_semantic_audit/COMMON_FINDINGS_REGISTER_ADDENDUM.md'
    rt=p(register).read_text(encoding='utf-8').rstrip()
    marker='## COMMON V2.4 Deep Read closure — 2026-09-03'
    need(marker not in rt,'V2.4 register closure not already appended')
    rt+='''\n\n## COMMON V2.4 Deep Read closure — 2026-09-03\n\nAuthority note: the selected Common/Enums V2.4 bytes are **candidate/integration** (matching open draft `VDVde/VDV301#31`), not an official release-tag family.\n\n### DRCOM24-001 — LineInformation LineName/LineShortName type + repeatability mismatch\n\nState: **executable-confirmed EV-122**.\n\nPDF V2.4 documents both fields as `IBIS-IP.string 0:1`; selected candidate XSD models both as `InternationalTextType 0:*`. EV-122 confirms both the shape/type and repetition effects. Validation follows the exact selected candidate XSD in candidate mode; the diagnostic layer may explain the PDF difference.\n\n### V2.4 scope corrections\n\n- `DRCOM23-001` ends at V2.3: V2.4 StopInformationRequest contains `ArrivalExpected` and `DepartureExpected` in both PDF and selected candidate XSD.\n- `CE-025` is not extended to V2.4: `ReplyPath` aligns.\n- `CE-026` is not extended to V2.4: `BeaconPoint.Description` aligns.\n- DoorCounting lexeme portion of `DRCOM10-006` is not extended to V2.4: `Wheelchair` / `Other` align.\n- `CE-020` remains V2.3 official-vs-PR30 collision specific.\n- `CE-023` remains V2.2-only.\n\nThe exact 15-group reconciliation is machine-readable in `audit_registry/deep_read_findings_delta_common_v24_2026-09-03.json`.\n'''
    p(register).write_text(rt+'\n',encoding='utf-8')

    for rel in ['.github/workflows/temp-common-v24-pin-read.yml','.github/workflows/temp-common-v24-ev122.yml','.github/workflows/temp-close-common-v24.yml','tools/temp_close_common_v24.py']:
        need(p(rel).exists(),f'temporary path exists: {rel}')
        p(rel).unlink(); print('REMOVED',rel)
    print('COMMON_V24_CLOSURE_STATE_OK')

if __name__=='__main__': main()
