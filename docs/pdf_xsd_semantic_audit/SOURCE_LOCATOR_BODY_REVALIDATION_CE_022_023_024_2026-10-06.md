# Visible-body source-locator revalidation — CE-022 / CE-023 / CE-024

Date: 2026-10-06  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`

This block closes the remaining current-standard source-locator/body backlog. CE-023 required a scope correction during active disproof; that correction is separately recorded in:

`docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_CE023_V23_SCOPE_2026-10-06.md`

## CE-022 — ServiceIdentification ServiceName versus Service

Visible body anchors:

- V1.0 p.17: **1.37 ServiceIdentification**, Table 37
- V2.0 p.24: **2.37 ServiceIdentification**, Table 37
- V2.1 p.26: **2.37 ServiceIdentification**, Table 37
- V2.2 p.27: **2.38 ServiceIdentification**, Table 38
- V2.3 p.28: **2.38 ServiceIdentification**, Table 38
- V2.4 p.30: **2.37 ServiceIdentification**, Table 37

Every checked PDF visibly exposes the outer row as:

`ServiceName 1:1 +ServiceSpecification`

followed by `Device`.

The exact selected XSDs instead define the outer member:

`Service` of type `ServiceSpecificationStructure`

while `ServiceName` exists legitimately one level deeper inside `ServiceSpecificationStructure`.

Exact selected XSD line pairs:

- V1.0: outer Service line 472; inner ServiceName line 455
- V2.0: lines 478 / 461
- V2.1: lines 477 / 460
- V2.2: lines 486 / 469
- V2.3: lines 536 / 519
- V2.4 candidate/integration: lines 551 / 534

The active disproof attempt was whether the PDF simply omitted the wrapper name while still documenting the same XML path. It does not: the table promotes the nested `ServiceName` identifier to the outer ServiceIdentification level. That identifier is not declared at that XSD level.

Result: no semantic change.

- CE-022 remains a high-confidence likely PDF defect / wrong outer element name.
- `ServiceIdentification.ServiceName` is not an XSD alias for outer `Service`.
- provider XML using outer `ServiceName` must **FAIL** against the affected selected XSD.
- the diagnostic should explain the nested-field/table-copy origin.
- V2.4 remains candidate/integration authority only.

Exact-byte evidence used for the older lanes:

- V1.0 p.17 PNG SHA-256 `56f8f8263259c5794afe662012238a4a0b226bac9bb871ea400a3a5b11f7d7b2`
- V2.0 p.24 PNG SHA-256 `e202d1d4ae06d943311774bb50fa3224b48dcc0a0af36f2a8286678124a37665`
- V2.1 p.26 PNG SHA-256 `682a45f9203dd7f62cfa2f258cc466560daa046a6791bed0eb4c8ec28680db40`
- V2.3 p.28 PNG SHA-256 `ed849499804ca7d9b96843d7149842727eb3892b5c435223dc23d87cf86309ce`
- V2.4 p.30 PNG SHA-256 `54c7fe1358108326670368e46d426c0382fa25f8670f7ef7757efb94238121de`

V2.2 was also visibly checked on the exact official PDF surface.

## CE-023 — corrupt duplicate NetexMode table

### Common V2.2

Official PDF SHA-256:
`85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`.

Visible printed p.26 shows section **2.34 NetexMode** followed by a table whose structure header is **Message** and whose rows are:

- `Message-ID`
- `TimeStamp`
- `MessageType`
- `MessageText`

The caption nevertheless reads **Table 34 — Description of NetexMode**.

The actual NetexMode structure is visibly present earlier on p.15 as **1.18 NetexMode**. The exact V2.2 XSD blob `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`, lines 956-970, contains the NetexMode main-mode/submode choice structure rather than Message fields.

V2.2 remains affected.

### Common V2.3 — corrected scope

The previous current registry said V2.3 had been disproved and removed from scope. Current-standard revalidation falsified that statement.

Official PDF SHA-256:
`d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`.

Exact-byte artifact:

- run `33656579631`
- artifact `9856965744`

Visible body:

- p.26 starts **2.34 NetexMode** and its prose.
- p.27 visibly contains a **Message** structure table with `Message-ID`, `TimeStamp`, `MessageType`, `MessageText`.
- the caption is **Table 34 — Description of NetexMode**.

Rendered-page SHA-256:

- p.26 `b541889bb83952a6f9e7aef044bc70834ea1acbe23e80d34c7d4f3d8ed9fa7ea`
- p.27 `da2ebb0aaa92ca1aac51a842d20b2dcda3c11d8abe1c150e6f5b783167763d89`

The exact V2.3 XSD blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`, lines 1036-1050, contains the proper NetexMode choice model.

Therefore **V2.3 is affected**.

### Common V2.4 negative control

Official PDF SHA-256:
`01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`.

Visible p.29 shows:

- 2.32 LogMessage
- 2.33 Message
- **2.34 Point**

The erroneous second NetexMode section/table is gone. V2.4 remains not affected.

### Corrected result

CE-023 remains a confirmed PDF copy/paste/table defect, but its current scope is now:

- **V2.2 affected**
- **V2.3 affected**
- **V2.4 not affected**

No XSD special handling follows. SDK behavior remains documentation-only informational guidance.

The older V2.3-scope-withdrawal statements are preserved as history but superseded by the 2026-10-06 correction delta.

## CE-024 — UnsubscribeResponse Active 0:1 versus XSD 1:1

Visible body anchors:

- V2.2 p.34: **2.62 UnsubscribeResponse**, Table 62 -> `Active 0:1`
- V2.3 p.35: **2.62 UnsubscribeResponse**, Table 62 -> `Active 0:1`
- V2.4 p.38: **2.61 UnsubscribeResponse**, Table 61 -> `Active 0:1`

Exact selected XSDs instead require `Active` exactly once because `minOccurs` and `maxOccurs` are omitted:

- V2.2 blob `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`, line 909
- V2.3 blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`, line 989
- V2.4 candidate/integration blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`, line 1041

Visible rendered-page SHA-256:

- V2.2 p.34 `4135adcc1e2b41196dd0fc7c4f09c23ddb0cacbd9170f244f5b3312c1692964e`
- V2.3 p.35 `39728f9dab274a668f94aa98ee3f600e3e3db58ccc91d0bf08c055fb1c83f3ed`
- V2.4 p.38 `ef42b65d0e8796ad6b286b947c7e69c161ce3969a8507432459db3ee611ad8e4`

The strongest disproof attempt was whether the PDF optionality could be an allowed semantic relaxation. Under exact selected-XSD conformance it cannot override the required XSD member.

Result: no semantic change.

- CE-024 remains a confirmed cross-artifact cardinality mismatch.
- a response omitting `Active` must **FAIL** against the affected selected XSD.
- the diagnostic should explain that the PDF misleadingly documents `0:1`.
- V2.4 remains candidate/integration authority only.

## Accounting before gate

After this review block:

- CE-022: `verified_current_standard`
- CE-023: `verified_current_standard` with corrected V2.2+V2.3 scope
- CE-024: `verified_current_standard`
- structural locator count remains **40**
- current-standard verified becomes **40**
- pending current-standard revalidation becomes **0**
- structural expansion remains frozen until the strengthened gate succeeds
- next structurally missing finding after gate closure: **CIS-001**

## Gate

Pending.
