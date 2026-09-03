#!/usr/bin/env python3
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'audit_registry/finding_revalidation_registry_v0.1.json'
STATE=ROOT/'00_START_HERE/CURRENT_STATE.json'
DOC=ROOT/'docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_ARA_V24_2026-09-03.md'
SOURCE='docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_ARA_V24_2026-09-03.md'

terminal={
 'ARA-001':'context_verified',
 'ARA-002':'context_verified',
 'ARA-003':'executable_confirmed',
 'ARA-004':'context_verified',
 'DRARA24-001':'context_verified',
 'DRARA24-002':'context_verified',
}

reg=json.loads(REG.read_text(encoding='utf-8'))
assert reg['state']=='inventory_frozen_revalidation_in_progress'
assert reg['inventory']['entry_count']==192
assert reg['inventory']['source_head']=='7fad145f528205ef5c40e58a3a23374379b08189'
entries={e['finding_id']:e for e in reg['inventory']['entries']}
for fid,st in terminal.items():
    assert fid in entries
    assert entries[fid]['revalidation_state']=='pending'
    entries[fid]['revalidation_state']=st
    entries[fid]['terminal_state_source']=SOURCE

reg.setdefault('revalidation_blocks',{})['ARA_V2.4']={
 'date':'2026-09-03',
 'state':'completed',
 'source_freeze':'docs/pdf_xsd_semantic_audit/deep_read/ARA_V2.4.md',
 'fresh_read_freeze_commit':'fe77b60b96e8d8aef138b71c00f44d4e409ba1f1',
 'pdf_sha256':'d0c8d8a3b8719c13b09f43ec98349d2e9b22d07fec0c9267bceff0812cbbc34c',
 'candidate_service_blob':'48fb303b80936d2d762f0889ce0c359e04c16e5b',
 'selected_common_blob':'0d8926c4063c12de9a5e68b6f0addaab35a55dc1',
 'selected_enumerations_blob':'2a23b512379b18e8f122ac1272cef8229fb86283',
 'ev105_current_route_run':'33228250613',
 'ev105_current_route_result':'PASS',
 'findings':terminal,
 'terminal_state_source':SOURCE,
 'xsd_mutation':False,
}
reg['next_revalidation_block']='ARCH'
REG.write_text(json.dumps(reg,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

state=json.loads(STATE.read_text(encoding='utf-8'))
a=state['audit']
a['legacy_finding_revalidation_state']='inventory_frozen_revalidation_in_progress'
a['finding_revalidation_current_block']='ARA_V2.4'
a['finding_revalidation_latest_completed_block']='ARA_V2.4'
a['finding_revalidation_next_block']='ARCH'
a['finding_revalidation_completed_findings']=6
a['finding_revalidation_pending_findings']=186
a['finding_revalidation_latest_terminal_state_source']=SOURCE
STATE.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

DOC.write_text('''# Legacy finding revalidation — ARA V2.4 — 2026-09-03

Status: completed under the current Finding Evidence Gate.

## Authority and evidence route

- Frozen inventory: `audit_registry/finding_inventory_frozen_2026-09-03.json` (192 findings; immutable source head `7fad145f528205ef5c40e58a3a23374379b08189`).
- Independent fresh read: `docs/pdf_xsd_semantic_audit/deep_read/ARA_V2.4.md`.
- Fresh-read freeze commit: `fe77b60b96e8d8aef138b71c00f44d4e409ba1f1`.
- Official PDF SHA-256: `d0c8d8a3b8719c13b09f43ec98349d2e9b22d07fec0c9267bceff0812cbbc34c`.
- AnalogRadio V2.4 service XSD remains candidate/integration material, blob `48fb303b80936d2d762f0889ce0c359e04c16e5b`; it is not promoted to official release authority.
- Selected dependency route for executable evidence: Common V2.3 `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`, Enumerations V2.2 `2a23b512379b18e8f122ac1272cef8229fb86283`.
- EV-105 current-route rerun `33228250613`: PASS.

## Terminal finding states

| Finding | Terminal state | Basis |
|---|---|---|
| ARA-001 | `context_verified` | Public V2.4 PDF vs absent official V2.4 release schema; candidate provenance explicitly bounded. |
| ARA-002 | `context_verified` | Pinned PDF internally contradicts `TransmitterType` with embedded schema/diagram/XML example `Transmitter`. |
| ARA-003 | `executable_confirmed` | PDF 1:1 vs candidate XSD 0:1; EV-105 proves omission and presence are both candidate-XSD-valid. |
| ARA-004 | `context_verified` | Pinned PDF operation inventory/XML example use `SendTelegram`; URI example uses `SendFFSKTelegram`. |
| DRARA24-001 | `context_verified` | Pinned PDF URI template includes `http://`; concrete example omits the scheme. Executable XML validation is not applicable. |
| DRARA24-002 | `context_verified` | Visible grouped editorial spelling residue in the pinned PDF. Executable XML validation is not applicable. |

## Gate reconciliation

`ARA-001` through `ARA-004` were explicitly re-evaluated during Deep Read Pass 2 after adoption of the current Evidence Gate. Their records reconstruct the original pinned source, exact authority route, full local context and active disproof attempts. `ARA-003` additionally has executable evidence. `DRARA24-001` and `DRARA24-002` were created from that same independent current-gate read and are documentation-only findings, so `context_verified` is terminal.

No XSD file is changed. The frozen 192-entry inventory snapshot is not mutated; only the live revalidation registry receives terminal states.

Next block: `ARCH`.
''',encoding='utf-8')

print('ARA_REVALIDATION_COMPLETED=6')
print('PENDING=186')
print('NEXT=ARCH')
