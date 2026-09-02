# Audit handoff delta — COMMON V2.2 Deep Read — 2026-09-02

## Completed block

`COMMON_V2.2` is closed for Deep Read Pass 2 as `needs_visual_review` with historical reconciliation complete.

- Fresh-read freeze: `13409ec0d79f74ed493abc196abb8a69186adeaa`.
- Official PDF SHA-256: `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`; 1,411,558 bytes; 55 pages.
- Pin/render/read run: `33614504943`; artifact `9840345496`.
- Exact authority route: historical upstream V2.2 file lineage; no `VDV-301-2.2` tag was invented.
- Common blob: `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`.
- Enumerations blob: `2a23b512379b18e8f122ac1272cef8229fb86283`.
- EV-120: PASS, run `33620003188`, job `100214595629`, checker `tools/validate_common_v22_ev120.py`.
- New unique finding: `DRCOM22-001` — PDF requires NetexMode main/submode choices while exact XSD makes both compositors optional; an empty NetexMode validates.
- Existing findings revalidated/scope-extended: 30; exact mapping is in `audit_registry/deep_read_findings_delta_common_v22_2026-09-02.json`.
- Historical scope correction: `CE-023` is present in V2.2 and V2.3; checked V2.4 is corrected.

## Independence/provenance note

The V2.2 observation list is source-rederived and frozen, but not claimed as pristine clean-room evidence. A file-library search exposed historical Common material after source-only comparison began and before formal freeze. The complete fourteen-group list was re-derived from the pinned PDF plus exact V2.2 XSD family and frozen with this process defect disclosed.

## Guardrails

- No XSD was changed.
- Exact selected XSD remains executable authority.
- `-1:1` is VDV choice notation, not a negative cardinality.
- Do not latest-wins substitute a later Common/Enumerations family.
- `DRCOM22-001` (choice optionality) and `CE-023` (corrupt duplicate table) are separate identities.
- `FR-COM22-014` stays documentation-only; LineCode/Heartbeat cross-reference residue creates no XML aliases.
- Historical findings require Evidence-Gate revalidation; EV-120 is the V2.2 executable evidence.

## Next natural unit

`COMMON_V2.3`.

Start from its already pinned source/authority evidence, re-establish the exact current evidence state, then perform the independent/source-first Deep Read before reopening historical Common findings for that unit.
