#!/usr/bin/env python3
import json, os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'audit_registry/finding_revalidation_registry_v0.1.json'
STATE=ROOT/'00_START_HERE/CURRENT_STATE.json'
DOC=ROOT/'docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_BG_2026-09-03.md'
SOURCE='docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_BG_2026-09-03.md'
run=os.environ.get('GITHUB_RUN_ID','local')
reg=json.loads(REG.read_text())
entries={e['finding_id']:e for e in reg['inventory']['entries']}
for fid,st in {'BG-001':'context_verified','BG-002':'contextual_not_defect'}.items():
    assert entries[fid]['revalidation_state']=='pending'
    entries[fid]['revalidation_state']=st
    entries[fid]['terminal_state_source']=SOURCE
reg.setdefault('revalidation_blocks',{})['BG']={
 'date':'2026-09-03','state':'completed','authority_lane':'official_git_tag_provenance_plus_operational_legacy_root_adapter',
 'upstream_repository':'VDVde/VDV301','compared_tags':['VDV-301-1.0','VDV-301-2.0'],
 'upstream_compare_base_commit':'f5b53785f703e898632603eec3bfa3555a79fdba',
 'same_path_v10_blob_transitions':{
  'IBIS-IP_JourneyInformationService_V1.0.xsd':['1ee4d7aeb15f3269c5335313be9e214bdb519d2e','8c303db5a9c0548d66b90174d9c329d33092ad24'],
  'IBIS-IP_PassengerCountingService_V1.0.xsd':['600a3ee6290c630a4435fb06ca9803dabaceb788','4161872be76740abfdd1cddf96f8a736333fc8be'],
  'IBIS-IP_SystemManagementService_V1.0.xsd':['85390f99d6c19c88923ed9a5fc8a5706137708af','2d32630a0f1981e980e6a466e3f6a69136410f24'],
  'IBIS-IP_TicketInformationService_V1.0.xsd':['017ca64666e25d757fc0cde1f1be817f06a743fc','3fda66d872ab0d1c511247f13e715cf3ad56afe7']},
 'aggregate_v1_blob':'41289eaed2674a169fdf77a10a2eff293c76d5c4','aggregate_removed_by_VDV_301_2_0':True,
 'executable_evidence_id':'EV-123','executable_run_id':run,'executable_checker':'tools/validate_legacy_v1_roots.py',
 'findings':{'BG-001':'context_verified','BG-002':'contextual_not_defect'},'terminal_state_source':SOURCE,'xsd_mutation':False}
reg['next_revalidation_block']='CE'
REG.write_text(json.dumps(reg,indent=2,ensure_ascii=False)+'\n')
state=json.loads(STATE.read_text())
a=state['audit']; a['finding_revalidation_current_block']='BG'; a['finding_revalidation_latest_completed_block']='BG'; a['finding_revalidation_next_block']='CE'; a['finding_revalidation_completed_findings']=16; a['finding_revalidation_pending_findings']=176; a['finding_revalidation_latest_terminal_state_source']=SOURCE; a['latest_executable_evidence_id']='EV-123'; a['latest_executable_evidence_run_id']=run
STATE.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n')
DOC.write_text(f'''# Legacy finding revalidation — Base / General — 2026-09-03\n\nStatus: completed under the current Finding Evidence Gate.\n\n## Exact provenance reconstruction\n\nFresh upstream comparison of `VDVde/VDV301` tags `VDV-301-1.0` and `VDV-301-2.0` reconfirms the four same-path V1.0 blob transitions and removal of the original aggregate `IBIS_IP_V1.0.xsd`. The exact transitions are:\n\n- JourneyInformationService V1.0: `1ee4d7ae...` → `8c303db5...`\n- PassengerCountingService V1.0: `600a3ee6...` → `4161872b...`\n- SystemManagementService V1.0: `85390f99...` → `2d32630a...`\n- TicketInformationService V1.0: `017ca646...` → `3fda66d8...`\n\nThe strongest disproof hypothesis was also retained: **different blob does not automatically mean a different payload-validity model**. The prior semantic diff remains controlling for that distinction: these four transitions are primarily packaging/self-containment changes. Therefore `BG-001` is not a rule to duplicate every release snapshot or require `release_context` merely because bytes differ. Exact release context is needed where semantic constraints differ or strict historical reproduction is requested.\n\n## BG-001\n\nTerminal state: `context_verified`.\n\nThe provenance/routing warning survives: service name + version token alone does not prove byte identity. The refined interpretation also survives: blob difference alone is insufficient to infer a semantic validation difference. Exact selected blob/pool remains authority; latest-wins is forbidden.\n\n## BG-002\n\nTerminal state: `contextual_not_defect`.\n\nUpstream tag comparison confirms that `IBIS_IP_V1.0.xsd` belongs to the original VDV-301-1.0 packaging and is removed in VDV-301-2.0. It remains historical packaging/root-declaration evidence, not an active dependency to mix with later self-contained V1.0 service files. No synthetic later aggregate is to be invented.\n\n## Executable support — EV-123\n\nRun `{run}` executes the existing `tools/validate_legacy_v1_roots.py` against the current deduplicated superbranch. The generated harnesses are adapters only; they compile the exact legacy root mappings without modifying or pretending to replace official VDV XSDs.\n\nFrozen inventory remains unchanged at 192 IDs. Live revalidation total after this block: **16 terminal / 176 pending**. Next block: `CE`. No XSD was changed.\n''')
print('BG_REVALIDATION_COMPLETED=2')
print('TOTAL_TERMINAL=16')
print('PENDING=176')
print('NEXT=CE')
