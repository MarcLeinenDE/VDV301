# Audit handoff delta – post-authority-split execution and V2.3 source pins

Date: 2026-08-28  
Canonical branch: `dev/schema-integration`  
Canonical base before this evidence block: `9b5a07331efee7dbc1633e43eb0085b06786850d`

## Purpose

Close the executable and source-provenance tasks left open after the Common V2.3 official/PR-30 authority split and the PDF source-cache infrastructure block.

This delta supersedes earlier statements that the current 50-root pool, the Common V2.3 candidate overlay, or the two active V2.3 PDF sources were still unexecuted/unpinned.

No XSD bytes were edited by this block.

## Controlled evidence run

GitHub Actions run:

```text
33169314332
```

Temporary evidence branch/head used for execution:

```text
audit/tmp-validation-run
392d89ada207e9821c72592eab50e839f9a3758a
```

The temporary branch was created from canonical `dev/schema-integration` at `9b5a0733...` and added only the executable EV-106 checker plus a temporary push-triggered evidence workflow. Repository XSD bytes were unchanged relative to the canonical base.

The temporary push workflow was removed immediately after the evidence run:

```text
6fd0bd819e545f70c71ae6b031c4126a4d80dda1
```

The permanent canonical audit workflow remains `workflow_dispatch` / manual-only.

## 50-root executable baseline

Result:

```text
root_compile_plus_dms_v24 exit_code = 0
Schema compile check: 50 XSD files
PASSED
```

All 50 current root XSDs compiled successfully, including the restored exact official `IBIS-IP_common_V2.3.xsd`.

The DMS V2.4 control samples also passed with their expected valid/invalid outcomes.

Current generated inventory from the same run:

```text
root_xsds = 50
xsd_service_profiles = 39
direct include edges = 84
non_xsd_profiles = 4
official root XSDs = 41
candidate root XSDs = 7
integration root XSDs = 2
```

The earlier `49 roots / 38 service profiles / 82 direct include edges` execution baseline is therefore superseded for the current stored state.

## EV-106 – Common V2.3 official vs PR #30 candidate

Permanent checker:

```text
tools/validate_common_v23_schema_variant.py
```

Evidence ID:

```text
EV-106
finding: CE-020
variant_id: common-v2.3-upstream-pr30
```

Verified Git blob identities:

```text
official Common V2.3:
0d8926c4063c12de9a5e68b6f0addaab35a55dc1

PR #30 candidate:
456a7db179ce14bc3f04e2bc05e42e16545fb0c5
```

Both isolated pools compile:

```text
Common V2.3 official   OK
Common V2.3 candidate  OK
CIS V2.3 official      OK
CIS V2.3 candidate     OK
```

Observable `InternationalTextType` difference:

```text
official flat instance      VALID
official wrapped instance   INVALID
candidate flat instance     INVALID
candidate wrapped instance  VALID
```

The semantic difference is therefore executable, not merely textual/provenance metadata.

Reason:

```text
official:
  InternationalTextType.Value    -> xs:string
  InternationalTextType.Language -> xs:language

candidate PR #30:
  InternationalTextType.Value    -> IBIS-IP.string
  InternationalTextType.Language -> IBIS-IP.language
```

The `IBIS-IP.*` types are wrapper complex types, so PR #30 changes the accepted XML instance shape.

Authority handling is unchanged:

```text
official release bytes remain default
candidate requires explicit schema_variant_id opt-in
candidate is assembled in an isolated pool
no latest-wins
no silent root replacement
```

## CE-020 original-PDF visual confirmation

The original official VDV 301-2-1 V2.3 PDF was visually inspected at printed page 12 / PDF page index 11, Table 17 `InternationalTextType`.

Visible table rows confirm:

```text
Value      1:1  IBIS-IP.string
Language   1:1  IBIS-IP.language
ErrorCode  0:1  ErrorCodeEnumeration
```

Thus the PDF agrees with the PR #30 candidate type names while the exact official VDV-301-2.3 XSD release blob remains different.

This confirms the PDF/XSD mismatch itself. It does not authorize changing the official schema authority.

## Byte-pinned official V2.3 PDF sources

The two active Deep Read sources were downloaded from their registered official VDV URLs and pinned by exact SHA-256 plus byte size.

### General Conventions V2.3

```text
source_id: VDV301-2_GC_V2.3
sha256: 4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603
size: 1057483 bytes
pinned_at_utc: 2026-08-28T12:00:27Z
deep_read_source_ready: true
```

### Common Structures / Enumerations V2.3

```text
source_id: COMMON_V2.3
sha256: d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b
size: 793521 bytes
pinned_at_utc: 2026-08-28T12:00:30Z
deep_read_source_ready: true
```

The stable URL/source catalog remains in `audit_registry/pdf_source_registry_v0.1.json`; exact byte pins are stored separately in `audit_registry/pdf_source_pins_v0.1.json` so later pin additions do not rewrite the source catalog. `tools/verify_vdv_pdf_source_pins.py` performs strict re-fetch/cache verification against the committed pins.

Only metadata/checksums are committed. PDF bytes remain outside Git under the ignored local source cache policy.

Any later mismatch remains a hard:

```text
SOURCE_CHANGED_SINCE_AUDIT
```

and must not be silently re-pinned.

## Permanent regression integration

EV-106 is added to the permanent manual audit workflow so future controlled runs re-check:

- exact official/candidate blob identities;
- isolated compilation of both Common V2.3 variants;
- CIS V2.3 compilation against each isolated variant;
- the flat-vs-wrapped `InternationalTextType` behaviour.

## Current continuation point

Infrastructure/executable work from the authority split is now closed.

Resume Deep Read Pass 2 with:

```text
VDV301-2_GC_V2.3
```

using the byte-pinned official source and render-first page review.

Then continue the dedicated `COMMON_V2.3` Deep Read. CE-020 already has original-PDF table visual confirmation plus EV-106 executable evidence, but the rest of Common V2.3 still requires the normal exhaustive document pass.

No PR, official upstream branch, fork `master`, or official release content was modified.
