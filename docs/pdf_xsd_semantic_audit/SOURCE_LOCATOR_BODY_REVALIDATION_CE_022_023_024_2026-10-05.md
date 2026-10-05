# Visible-body source-locator revalidation — CE-022 / CE-023 / CE-024

Date: 2026-10-05  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`  
Scope: final current-standard revalidation block for the structurally complete 40-finding locator set.

## Evidence method

All PDF conclusions below are based on visible body tables/headings from the exact registered publications. The web screenshot renderer was attempted first. Where it cache-missed, exact-byte pinned/fallback render artifacts were used.

Reusable pinned artifacts:

- COMMON V1.0: run `33275626001`, artifact `9721397514`
- COMMON V2.0: run `33279811315`, artifact `9722644456`
- COMMON V2.1: run `33393002497`, artifact `9758203545`
- COMMON V2.3: run `33656579631`, artifact `9856965744`
- COMMON V2.4: run `33658306978`, artifact `9857652638`

Final V2.2 fallback:

- run `37364660362`
- artifact `11367729790`
- exact official PDF SHA-256 verified before render: `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`
- printed p.15 render SHA-256: `b17050642bc1c1a0dfefb9140405890e44225e6209ae953583aeff5962023692`
- printed p.34 render SHA-256: `4135adcc1e2b41196dd0fc7c4f09c23ddb0cacbd9170f244f5b3312c1692964e`

## CE-022 — ServiceIdentification outer ServiceName versus XSD Service

Visible PDF body:

- V1.0 p.17: **1.37 ServiceIdentification**, Table 37
- V2.0 p.24: **2.37 ServiceIdentification**, Table 37
- V2.1 p.26: **2.37 ServiceIdentification**, Table 37
- V2.2 p.27: **2.38 ServiceIdentification**, Table 38
- V2.3 p.28: **2.38 ServiceIdentification**, Table 38
- V2.4 p.30: **2.37 ServiceIdentification**, Table 37

All six visible tables place `ServiceName` at the outer `ServiceIdentification` level and reference `ServiceSpecification`.

Exact selected XSDs instead require:

- outer `ServiceIdentificationStructure.Service` of type `ServiceSpecificationStructure`
- nested `ServiceSpecificationStructure.ServiceName` of type `ServiceNameEnumeration`

Exact outer/nested line pairs:

- V1.0: lines 472 / 455
- V2.0: lines 478 / 461
- V2.1: lines 477 / 460
- V2.2: lines 486 / 469
- V2.3: lines 536 / 519
- V2.4 candidate/integration: lines 551 / 534

The active disproof attempt was whether the documented `ServiceName` could simply be a shorthand for the nested structure. It cannot define a valid outer XML element: `ServiceName` already has a distinct nested position in the exact XSD model.

Result: no semantic change.

- CE-022 remains a high-confidence likely PDF table-copy/naming defect.
- at the outer ServiceIdentification level the selected XSD requires `Service`.
- provider XML using outer `ServiceName` must **FAIL** if the selected XSD rejects it.
- no alias or silent reshaping is permitted.
- V2.4 remains candidate/integration authority only.

## CE-023 — corrupt duplicate NetexMode table

### V2.2

Printed p.15 visibly contains the actual **1.18 NetexMode / Table 20** choice model.

Printed p.26 visibly contains a second **2.34 NetexMode / Table 34** whose table body is actually the `Message` structure:

- `Message-ID`
- `TimeStamp`
- `MessageType`
- `MessageText`

Exact Common V2.2 XSD blob `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` contains the real `NetexMode` choice model at lines 956-970.

### V2.3 — correction of prior scope withdrawal

The exact byte-pinned V2.3 PDF SHA-256 is `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`.

Visible evidence:

- p.15: **1.18 NetexMode / Table 20** contains the actual main-mode/submode choice model.
- p.26: **2.34 NetexMode** heading and descriptive prose begin.
- p.27: the continued **Table 34 — Description of NetexMode** visibly contains the `Message` fields above.

Pinned page hashes:

- p.15: `f5a33a1cc837192d4c999432fd4747134f2a53158e0f5cdf786773c502958af6`
- p.26: `d177fad7b44a43305467991ce985551f38fffa28ad3b880410ac9104551d7ca2`
- p.27: `a71c6c8a01f3516223469873682c358c530b16f066f9b097ef28ec107b465cd8`

All match the artifact page-hash manifest.

The previous V2.3 scope withdrawal checked p.26 and correctly observed that the table body was not on that page, but failed to follow the section onto p.27. That disproof was therefore incomplete.

Exact official Common V2.3 XSD blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` contains the actual `NetexMode` choice model at lines 1036-1050.

### V2.4 negative control

Exact byte-pinned V2.4 printed p.29 visibly shows:

- 2.32 LogMessage
- 2.33 Message
- **2.34 Point**

There is no corrupt second NetexMode table. V2.4 remains outside CE-023 affected scope.

### Corrected result

CE-023 remains documentation-only, but its canonical scope is corrected to:

- **Common V2.2 affected**
- **Common V2.3 affected**
- **Common V2.4 not affected**

No XSD defect, XML alias or runtime validation exception follows.

Correction delta:
`docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_CE023_V23_SCOPE_2026-10-05.md`

Historical reports containing the prior V2.3 withdrawal are retained as historical records and are superseded by this correction for current canonical state.

## CE-024 — UnsubscribeResponse.Active PDF 0:1 versus XSD 1:1

Visible body:

- V2.2 p.34: **2.62 UnsubscribeResponse**, Table 62 -> `Active 0:1`
- V2.3 p.35: **2.62 UnsubscribeResponse**, Table 62 -> `Active 0:1`
- V2.4 p.38: **2.61 UnsubscribeResponse**, Table 61 -> `Active 0:1`

Exact selected XSDs instead declare `Active` without `minOccurs` or `maxOccurs`, therefore effective **1:1**:

- V2.2 official blob `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`, line 909
- V2.3 official blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`, line 989
- V2.4 candidate/integration blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`, line 1041

The active disproof attempt was whether the PDF's optionality could be treated as an additional accepted form. It cannot override the exact selected XSD.

Result: no semantic change.

- CE-024 remains a confirmed cross-artifact cardinality mismatch.
- an UnsubscribeResponse missing `Active` must **FAIL** against these selected XSDs.
- the PDF 0:1 statement is explanatory Known-Issue context only.
- V2.4 remains candidate/integration authority only.

## Final current-standard accounting

After this block:

- CE-022: `verified_current_standard`
- CE-023: `verified_current_standard` with corrected V2.2-V2.3 scope
- CE-024: `verified_current_standard`
- structural locator entries: **40**
- current-standard verified: **40**
- pending: **0**

The visible-body quality backlog is therefore complete. Structural source-locator expansion may resume only after the strengthened gate validates this exact final state.

## Gate

Pending.
