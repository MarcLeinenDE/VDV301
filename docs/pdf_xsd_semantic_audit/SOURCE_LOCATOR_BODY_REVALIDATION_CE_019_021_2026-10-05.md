# Visible-body source-locator revalidation — CE-019 / CE-021

Date: 2026-10-05  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`

## Visual evidence method

COMMON V1.0, V2.0 and V2.1 were visually checked from the existing exact-byte pinned render artifacts:

- V1.0 run `33275626001`, artifact `9721397514`
- V2.0 run `33279811315`, artifact `9722644456`
- V2.1 run `33393002497`, artifact `9758203545`

Relevant rendered-page hashes:

- V1.0 p.15: `ee04c205a5ea2631b56dab16e1e429ccfe046da7353e69bad50af087320f5f13`
- V1.0 p.17: `56f8f8263259c5794afe662012238a4a0b226bac9bb871ea400a3a5b11f7d7b2`
- V2.0 p.22: `591644194d2f5edbf085bd589ee2c7ef9e2199a2c500696ee75046d183fa5a08`
- V2.0 p.24: `e202d1d4ae06d943311774bb50fa3224b48dcc0a0af36f2a8286678124a37665`
- V2.1 p.24: `709c501675f7393b8ff2d0dd25326a954da823a4906bc9f44443d1018d63d121`
- V2.1 p.26: `682a45f9203dd7f62cfa2f258cc466560daa046a6791bed0eb4c8ec28680db40`

The live PDF screenshot renderer was attempted for COMMON V2.2, V2.3 and V2.4 but cache-missed/timed out on the required pages. The canonical exact-byte fallback was therefore used.

Fallback run: `37362814695`  
Artifact: `11367581828` (`ce019021-visible-body`)

The fallback downloaded and SHA-256-verified the exact official PDFs:

- COMMON V2.2: `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`
- COMMON V2.3: `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`
- COMMON V2.4: `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`

Rendered-page hashes:

- V2.2 p.25: `c3c970fd3f977a6381a29d68633fdd4756e046fef44d3dab64989e0259295229`
- V2.2 p.27: `595803e54433c2fac972660cdb548f1d8121d640bef1162cf6e4395a98d9da6b`
- V2.3 p.26: `b541889bb83952a6f9e7aef044bc70834ea1acbe23e80d34c7d4f3d8ed9fa7ea`
- V2.3 p.28: `ed849499804ca7d9b96843d7149842727eb3892b5c435223dc23d87cf86309ce`
- V2.4 p.29: `cc99590d938de3c564c1abe9789da841c6ccc320e6bc5a1172cb3f8f55fb9cd5`
- V2.4 p.30: `54c7fe1358108326670368e46d426c0382fa25f8670f7ef7757efb94238121de`

The temporary render workflow was removed again after artifact capture.

## CE-019 — wrong structure reference in ServiceIdentificationWithStateList

Visible body anchors:

- V1.0 p.17: **1.39 ServiceIdentificationWithStateList**, Table 39
- V2.0 p.24: **2.39 ServiceIdentificationWithStateList**, Table 39
- V2.1 p.26: **2.39 ServiceIdentificationWithStateList**, Table 39
- V2.2 p.27: **2.40 ServiceIdentificationWithStateList**, Table 40
- V2.3 p.28: **2.40 ServiceIdentificationWithStateList**, Table 40
- V2.4 p.30: **2.39 ServiceIdentificationWithStateList**, Table 39

In every checked PDF, the row is named `ServiceIdentificationWithState` but the structure/type reference shown in the adjacent column is `ServiceSpecificationWithState`.

The exact selected XSDs instead type that list member as:

`ServiceIdentificationWithStateStructure`

Exact selected XSD lines:

- V1.0 line 484
- V2.0 line 490
- V2.1 line 489
- V2.2 line 498
- V2.3 line 548
- V2.4 candidate/integration line 563

The active disproof attempt was whether `ServiceSpecificationWithState` could be treated as an interchangeable or equivalent type. It cannot: the XSD explicitly binds the list element to `ServiceIdentificationWithStateStructure`, and the surrounding service-identification model contains device context that the specification structure alone does not provide.

Result: no semantic change.

- CE-019 remains a high-confidence likely PDF defect / wrong-structure-reference mismatch.
- `ServiceSpecificationWithState` is not an alternative XSD type for this list item.
- provider XML shaped according to the PDF reference but invalid against the selected XSD must **FAIL**.
- the diagnostic must explain that the PDF structure reference is the likely source of the implementation mistake.
- this issue remains separate from CE-018's cardinality mismatch on the same list.
- V2.4 remains candidate/integration authority only.

## CE-021 — LogMessage MessageBody versus Message

Visible body anchors:

- V1.0 p.15: **1.32 LogMessage**, Table 32
- V2.0 p.22: **2.32 LogMessage**, Table 32
- V2.1 p.24: **2.32 LogMessage**, Table 32
- V2.2 p.25: **2.32 LogMessage**, Table 32
- V2.3 p.26: **2.32 LogMessage**, Table 32
- V2.4 p.29: **2.32 LogMessage**, Table 32

Every checked PDF visibly names the required child:

`MessageBody`

and shows its type as `Message`.

The exact selected XSDs instead require the child element:

`Message`

of type `MessageStructure`.

Exact selected XSD lines:

- V1.0 line 395
- V2.0 line 401
- V2.1 line 400
- V2.2 line 409
- V2.3 line 459
- V2.4 candidate/integration line 474

The strongest disproof attempt was whether `MessageBody` is merely a presentation label while `Message` is the true XML name. The tables are explicitly documenting structure member names and therefore can directly mislead implementers, but they do not create an XSD alias.

Result: no semantic change.

- CE-021 remains a high-confidence likely PDF defect / stale identifier.
- `MessageBody` is not an XSD alias for `Message`.
- provider XML using `MessageBody` where the selected XSD requires `Message` must **FAIL**.
- the diagnostic should point out the PDF/XSD naming discrepancy rather than silently repairing the payload.
- V2.4 remains candidate/integration authority only.

## Accounting

- CE-019: `verified_current_standard`
- CE-021: `verified_current_standard`
- structural locator count remains **40**
- current-standard verified becomes **37**
- pending becomes **3**
- next pending finding: **CE-022**

## Gate

- GitHub Actions run: **37363179378**
- result: **SUCCESS**
- validated manifest commit: `f93274bb6d6d8d7bf9b51ff8ccb7053fd1565c56`
- structural locators: **40**
- current-standard verified: **37**
- pending current-standard revalidation: **3**
- next pending finding: **CE-022**

The gate validated CURRENT_STATE/body-registry synchronization, the CE-019/CE-021 locator assertions, and the existing audit regression suite.
