# Audit handoff delta - Common V2.3 Deep Read

Date: 2026-08-28  
Branch: `dev/schema-integration`  
Base HEAD before this block: `f02d5e4d6789ec7c5ec0bfd632c5fd0e59b25ff0`

## Purpose

Complete the fresh Deep Read of byte-pinned `COMMON_V2.3`, reconcile it with the exact official XSD/dependency route and the explicit PR #30 variant, update Common findings, and correct stale historical audit metadata.

No XSD is changed by this block.

## Source authority

Official PDF:

```text
VDV 301-2-1 V2.3
SHA-256 d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b
size 793521 bytes
```

Exact official XSD route:

```text
IBIS-IP_common_V2.3.xsd
  blob 0d8926c4063c12de9a5e68b6f0addaab35a55dc1
  -> IBIS-IP_Enumerations_V2.2.xsd
     blob 2a23b512379b18e8f122ac1272cef8229fb86283
```

PR #30 remains separate:

```text
schema_variant_id: common-v2.3-upstream-pr30
blob: 456a7db179ce14bc3f04e2bc05e42e16545fb0c5
```

Post-split executable evidence remains EV-106 / run `33169314332`.

## Deep Read result

```text
textual fresh read complete: yes
old-audit comparison complete: yes
byte-pinned source: yes
visual closure: no - PDF screenshot backend returned cache-miss
state: needs_visual_review
```

CE-020 remains separately visually and executably confirmed from the preceding authority-split block.

## New Common findings

```text
CE-021 LogMessage MessageBody PDF vs XSD Message
CE-022 ServiceIdentification ServiceName PDF vs XSD Service
CE-023 V2.3 duplicate/corrupt second NetexMode table copied from Message
CE-024 UnsubscribeResponse Active PDF 0:1 vs XSD 1:1
CE-025 Reply-Path PDF vs XSD ReplyPath; documentation corrected by V2.4
CE-026 BeaconPoint Description PDF vs V2.3 XSD Desciption; XSD corrected by V2.4
```

Detailed evidence is in:

```text
docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.3.md
docs/pdf_xsd_semantic_audit/COMMON_FINDINGS_REGISTER_ADDENDUM.md
```

## Existing findings strengthened

The fresh native-text pass independently strengthens:

```text
CE-005
CE-011
CE-013
CE-014
CE-015
CE-016
CE-017
CE-018
CE-019
CE-020
plus inherited enumeration findings CE-004 and CE-006..CE-010
```

CE-015, CE-017 and CE-019 remain visually unclosed because the screenshot backend failed.

## Historical correction - CE-010 / canalBarge

A stale earlier history statement was found and corrected.

Exact official VDV-301-2.2 `IBIS-IP_Enumerations_V2.2.xsd` already contains:

```text
AirSubmodeEnumeration:
  canalBarge
```

Therefore:

```text
canalBarge is already part of the Common V2.3 dependency pool.
It was NOT introduced by Enumerations V2.4.
CE-010 remains a PDF-vs-XSD omission, but confirmed XSD scope starts at least with V2.2.
```

Corrected files:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_3_vs_v2_4_xsd_diff.csv
docs/pdf_xsd_semantic_audit/04e_common_enums_v2_3_v2_4_history_and_closure.md
```

## State/count updates

After this block:

```text
textual Deep Reads complete: 7
needs_visual_review: 7
exhaustive_read: 0
active Deep Read: none until next source is byte-pinned
next target: VDV301-2_GC_V2.4
```

The next target must be byte-pinned before reproducible Deep Read use.

## Authority guard

Unchanged:

```text
selected exact XSD family/variant = executable XML authority
PDF/XSD differences = audit knowledge, not silent schema rewrite
official Common V2.3 remains default
PR #30 Common V2.3 remains explicit candidate
no latest-wins
no official-facing action without explicit user approval
```
