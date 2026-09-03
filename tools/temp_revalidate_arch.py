#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'audit_registry/finding_revalidation_registry_v0.1.json'
STATE=ROOT/'00_START_HERE/CURRENT_STATE.json'
PINS=ROOT/'audit_registry/pdf_source_pins_v0.1.json'
DR=ROOT/'docs/pdf_xsd_semantic_audit/deep_read/VDV301-1_V1.0_DE.md'
DOC=ROOT/'docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_ARCH_V10_2026-09-03.md'
SOURCE='docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_ARCH_V10_2026-09-03.md'
RUN='33725750019'
JOB='100554215021'
ART='9881897572'
PDF_SHA='5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2'
TEXT_SHA='bcf21432e5cec543317d029b882eef1a62706d2a5fb35a9e0b0bf3ec07afd964'
ART_SHA='b1805ba4137d541867a9bb20fcd6ff0654331acc0356d8e1b838c9cec83d4510'
ARCH=[f'ARCH-{i:03d}' for i in range(1,9)]

reg=json.loads(REG.read_text(encoding='utf-8'))
assert reg['state']=='inventory_frozen_revalidation_in_progress'
assert reg['inventory']['entry_count']==192
entries={e['finding_id']:e for e in reg['inventory']['entries']}
for fid in ARCH:
    assert entries[fid]['revalidation_state']=='pending'
    entries[fid]['revalidation_state']='contextual_not_defect'
    entries[fid]['terminal_state_source']=SOURCE
reg.setdefault('revalidation_blocks',{})['ARCH_V1.0']={
    'date':'2026-09-03','state':'completed','terminal_state':'contextual_not_defect',
    'authority_lane':'architecture_inventory_non_xsd','official_source_id':'VDV301-1_V1.0_DE',
    'official_pdf_sha256':PDF_SHA,'fulltext_sha256':TEXT_SHA,'page_count':36,
    'pin_render_run':RUN,'pin_render_job':JOB,'artifact_id':ART,'artifact_digest_sha256':ART_SHA,
    'visual_pages_checked':[6,7,10,14,16,26,27],
    'findings':{fid:'contextual_not_defect' for fid in ARCH},
    'terminal_state_source':SOURCE,'executable_evidence_reason_not_applicable':'Architecture context/authority constraints; no direct XSD validation behavior claim.',
    'xsd_mutation':False
}
reg['next_revalidation_block']='BG'
REG.write_text(json.dumps(reg,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

pins=json.loads(PINS.read_text(encoding='utf-8'))
assert not any(x['source_id']=='VDV301-1_V1.0_DE' for x in pins['sources'])
pins['sources'].append({
    'source_id':'VDV301-1_V1.0_DE','expected_sha256':PDF_SHA,'expected_size_bytes':1052021,
    'pinned_at_utc':'2026-09-03T06:58:30Z','deep_read_source_ready':True,
    'evidence_run_id':RUN,'evidence_job_id':JOB,'artifact_id':ART,
    'artifact_digest_sha256':ART_SHA,'page_count':36,'render_dpi':120,'fulltext_sha256':TEXT_SHA,
    'pin_note':'Fresh official-byte retrieval and targeted visual Evidence-Gate backfill for ARCH-001..ARCH-008.'
})
PINS.write_text(json.dumps(pins,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

state=json.loads(STATE.read_text(encoding='utf-8'))
a=state['audit']
a['pdf_sources_byte_pinned']=len(pins['sources'])
a['finding_revalidation_current_block']='ARCH'
a['finding_revalidation_latest_completed_block']='ARCH'
a['finding_revalidation_next_block']='BG'
a['finding_revalidation_completed_findings']=14
a['finding_revalidation_pending_findings']=178
a['finding_revalidation_latest_terminal_state_source']=SOURCE
STATE.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

old=DR.read_text(encoding='utf-8')
marker='## Evidence-Gate visual backfill — 2026-09-03'
assert marker not in old
DR.write_text(old.rstrip()+f'''\n\n{marker}\n\nThe original-source/visual gap relevant to `ARCH-001` through `ARCH-008` is closed without changing the broader document label to an exhaustive all-page visual audit.\n\n- fresh official PDF SHA-256: `{PDF_SHA}`\n- size: `1052021` bytes\n- pin/render run: `{RUN}`; job `{JOB}`\n- artifact: `{ART}` (`arch-v10-pinned-read`), digest `sha256:{ART_SHA}`\n- pages: `36`; all page PNG hashes verified against the artifact manifest\n- fulltext SHA-256: `{TEXT_SHA}`\n- targeted visual pages for the eight architecture claims: 6, 7, 10, 14, 16, 26, 27\n\nThese pages visibly confirm the service-oriented architecture and Part-2 boundary, provider/consumer hierarchy, vehicle/system boundary, safety boundary, UDP-multicast versus TCP/HTTP communication classes, historical SNTP/RTP wording, XML information format, and the distinction between functional components and implemented services. The eight `ARCH-*` records are therefore terminalized separately as `contextual_not_defect` architecture constraints. No XSD authority is inferred and no XSD is changed.\n''',encoding='utf-8')

DOC.write_text(f'''# Legacy finding revalidation — ARCH V1.0 — 2026-09-03\n\nStatus: completed under the current Finding Evidence Gate.\n\n## Original-source evidence\n\n- Authority: official German `VDV-Schrift 301-1`, 01/2014, Part 1 Systemarchitektur. This is an architecture authority lane, not an XSD lane.\n- Official source ID: `VDV301-1_V1.0_DE`.\n- Fresh PDF SHA-256: `{PDF_SHA}`; size `1052021` bytes.\n- Pin/render run `{RUN}`, job `{JOB}`, artifact `{ART}`, artifact digest `sha256:{ART_SHA}`.\n- 36 pages rendered at 120 dpi; all 36 page hashes verified locally against the artifact hash list.\n- Fulltext SHA-256: `{TEXT_SHA}`.\n- Relevant visual pages: 6, 7, 10, 14, 16, 26, 27.\n\n## Terminal states\n\n| Finding | State | Gate result / active disproof |\n|---|---|---|\n| ARCH-001 | `contextual_not_defect` | Pages 7/10 visibly establish replacement of Master/Slave by a service-oriented architecture and define service/operation independently of the device. This is architecture context, not a defect. |\n| ARCH-002 | `contextual_not_defect` | Page 14 visibly describes higher components as active consumers and lower ones as providers. The wording is a general hierarchy model; it does not override service-specific callback/subscription rules. |\n| ARCH-003 | `contextual_not_defect` | Page 16 visibly says every vehicle is a self-contained IBIS-IP system and a coupled vehicle is another IBIS-IP system connected through interfaces. It does not prohibit cross-vehicle communication. |\n| ARCH-004 | `contextual_not_defect` | Pages 7 and 26 establish the non-safety architecture boundary and general contemporary protection requirement. No concrete TLS/certificate/cipher profile is specified here. |\n| ARCH-005 | `contextual_not_defect` | Page 26 visibly distinguishes fast-changing data using UDP multicast from reliable longer-lived information using TCP/HTTP. These are architecture communication classes refined by Part 2, not a global per-packet SDK rule. |\n| ARCH-006 | `contextual_not_defect` | Pages 6 and 27 visibly place XML information exchange in Part 1 while Part 2 supplies technical XML structures. Exact elements/cardinalities therefore remain Part-2/XSD authority. |\n| ARCH-007 | `contextual_not_defect` | Page 26 explicitly calls SNTP/RTP conceivable but not yet specified **in this edition**. The strongest counter-hypothesis—treating that phrase as a permanent prohibition—is rejected by its publication-context wording. |\n| ARCH-008 | `contextual_not_defect` | Page 10 visibly states that only part of the functional components are specified/implemented as services or applications. A component name therefore cannot be promoted to an executable service identity. |\n\n## Executable-evidence boundary\n\nExecutable XSD evidence is not applicable to these eight records because they are architecture/authority constraints, not XML validity claims. Any downstream service-specific XML rule must still be proven against its exact selected Part-2 XSD family.\n\nFrozen inventory remains unchanged at 192 IDs. Live revalidation total after this block: **14 terminal / 178 pending**. Next block: `BG`. No XSD was changed.\n''',encoding='utf-8')

print('ARCH_REVALIDATION_COMPLETED=8')
print('TOTAL_TERMINAL=14')
print('PENDING=178')
print('NEXT=BG')
