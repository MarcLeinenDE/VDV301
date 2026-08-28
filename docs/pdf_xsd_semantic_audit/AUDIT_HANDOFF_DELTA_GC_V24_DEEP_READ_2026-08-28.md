# Audit handoff delta - General Conventions V2.4 Deep Read

Date: 2026-08-28  
Branch: `dev/schema-integration`  
Base permanent HEAD before Deep Read closure: `d127ccf21d8362a4771506e1d071a695662f40dd`

## Purpose

Complete the byte-pinned fresh Deep Read of `VDV301-2_GC_V2.4`, distinguish intentional V2.4 corrections from inherited/regressed documentation defects, and preserve the exact XSD-authority rule now explicitly stated by V2.4 itself.

No XSD is changed by this block.

## Source pin

```text
source_id: VDV301-2_GC_V2.4
SHA-256: 048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d
size: 1767094 bytes
pin evidence run: 33179106915
```

The same run revalidated the complete deterministic repository baseline successfully.

## Deep Read state

```text
textual fresh read: complete
existing-audit comparison: complete
byte-pinned source: yes
visual page review: attempted, screenshot backend cache-miss
state: needs_visual_review
```

## Positive V2.4 changes confirmed

```text
German DNS-SD TXT Table 3 now includes missing coachnumber/deviceclass/deviceID entries.
Chapter 6 explicitly says XSD definitions take precedence over documentation when inconsistent.
V2.3 history numbering is corrected to 7.2.1 / 7.2.2.
```

The new XSD-precedence sentence independently validates the repository's established authority model.

## New Deep Read findings

```text
DR3012GC24-001  German OnBordUnit vs English/XSD OnBoardUnit
DR3012GC24-002  German addressing headings duplicate 2.1.1 for IP and subnet/gateway
DR3012GC24-003  English allowed version-character list duplicates digit 2
DR3012GC24-004  typo-like technical service identifiers in DNS-SD/system-start examples and glossary
DR3012GC24-005  no common IBIS-IP version in 1.5 vs stale 'version 1.0 of IBIS-IP' wording in 2.5
```

Detailed evidence:

```text
docs/pdf_xsd_semantic_audit/deep_read/VDV301-2_GC_V2.4.md
audit_registry/deep_read_findings_delta_gc_v24_2026-08-28.json
```

## Reintroduced finding

`DR3012GC22-001` has a non-monotonic history:

```text
V2.2: unresolved Word cross-reference placeholders present
V2.3: literal placeholders absent in fresh read
V2.4: placeholders reintroduced at multiple locations
```

Do not duplicate the finding; retain this regression history on the original ID.

## Existing findings strengthened

```text
DISC-001
DR3012-001
DR3012-002
DR3012GC22-002
SUB-001
DR3012V21-001
```

`DR3012GC23-001` is resolved in the V2.4 publication because the V2.3 history subsection numbers are printed correctly there.

## Registry strategy

To avoid destructively rewriting the accumulated large Deep Read registries during this atomic block, V2.4 completion is represented by additive machine-readable deltas:

```text
audit_registry/deep_read_registry_delta_gc_v24_2026-08-28.json
audit_registry/deep_read_findings_delta_gc_v24_2026-08-28.json
```

`CURRENT_STATE.json` points to the base registries plus the latest deltas. `document_registry_v0.1.json` directly marks `VDV301-2_GC_V2.4` as `needs_visual_review`.

A later registry-consolidation phase may fold deltas into a new canonical registry version without loss of history.

## Counts after closure

```text
semantic document units: 48
textual Deep Reads complete: 8
needs_visual_review: 8
exhaustive_read: 0
active Deep Read: none
byte-pinned PDF sources: 3
```

## Next natural target

Following document-registry order:

```text
DMS_V2.2
```

Before starting it:

```text
1. byte-pin official DMS V2.2 PDF
2. verify source hash/size
3. perform fresh read before comparing with existing DMS findings
4. keep exact DMS V2.2 -> Common/Enumerations dependency authority
```
