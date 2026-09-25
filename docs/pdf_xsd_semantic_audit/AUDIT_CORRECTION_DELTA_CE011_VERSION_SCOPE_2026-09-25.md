# Audit correction delta — CE-011 version scope — 2026-09-25

Status: **post-Phase-A scope correction / evidence-backed / no finding reclassification**.

## Trigger

Phase-B source-locator hardening compared the semantic registry with the already completed Common/Enumerations historical closure and version-specific Deep Reads.

The semantic registry limited `CE-011` to Common V2.4 candidate/integration. That is too narrow.

## Corrected scope

```text
V2.1: NOT affected by CE-011
V2.2: affected
V2.3: affected
V2.4: affected in the explicitly selected candidate/integration XSD lane
```

The canonical semantic scope is therefore:

- Common V2.2–V2.3: official selected profiles;
- Common V2.4: explicit candidate/integration profile.

## Evidence

### V2.1 negative control

The V2.1 fresh read explicitly records the Connection multiplicities as aligned: `TransportMode 0:1` in the PDF matches the selected XSD, and ConnectionMode has not yet been introduced as the later modal-information field.

This prevents back-extending CE-011 to V2.1 or older versions.

### V2.2 origin

The V2.2 version history introduces `ConnectionMode` / `NetexMode` and states that ConnectionMode is newly integrated.

The pinned V2.2 PDF page 18 documents:

```text
TransportMode   0:*
ConnectionMode  0:*
```

The exact selected Common V2.2 XSD declares both fields with `minOccurs="0"` and no `maxOccurs`, hence effective `0:1`.

The V2.2 fresh-read reconciliation maps this observation directly to `CE-011`.

### V2.3

The V2.3 fresh read repeats the same boundary: the PDF documents both fields `0:*`, while exact Common V2.3 declares both as effective `0:1`.

### V2.4

The official V2.4 PDF retains `0:*` for both fields. The selected Common V2.4 XSD candidate/integration lane retains effective `0:1`.

The terminal historical closure already states: **CE-011 supported from V2.2 through V2.4**.

## Invariants

This correction does not change:

- finding identity;
- `cross_artifact_mismatch` assessment;
- confirmed confidence;
- `error_with_advisory` SDK behaviour;
- `runtime_match=reviewed`;
- the 77/115 Phase-A counts;
- any XSD byte;
- the selected-XSD PASS/FAIL rule.

The deterministic runtime mapping is regenerated only to carry the corrected `profile_scope`. The source-locator manifest is repinned to the updated semantic-registry blob; its already closed CE-005..CE-010 entries are unchanged.

## Follow-up

Phase A and the source-locator pilot must be revalidated before CE-011..CE-014 locator persistence continues.

## Primary revalidation gate

Run **36129458624**: **SUCCESS** on HEAD `346e21797405779ab9904db5903f6470cbe7b66f`.

The gate verified the corrected CE-011 scope, V2.1 as an aligned negative control, V2.2/V2.3/V2.4 affected XSD boundaries, unchanged 77/115 runtime counts, exact semantic-to-runtime profile projection, the existing locator pilot's semantic pin, all per-version Common validators, SDK consistency, root-XSD regression and a clean XSD tree.
