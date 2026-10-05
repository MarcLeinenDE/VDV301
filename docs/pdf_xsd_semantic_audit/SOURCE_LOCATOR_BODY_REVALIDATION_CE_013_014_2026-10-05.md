# Visible-body source-locator revalidation — CE-013 / CE-014

Date: 2026-10-05  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`

## CE-013 — AdditionalAnnouncement choice name and optionality

Visible body was rechecked across all affected publication lanes.

- V1.0 p.7: **1.1 AdditionalAnnouncement**, Table 1
- V2.0 p.14: **2.1 AdditionalAnnouncement**, Table 1
- V2.1 p.15: **2.1 AdditionalAnnouncement**, Table 1
- V2.2 p.16: **2.1 AdditionalAnnouncement**, Table 1
- V2.3 p.16: **2.1 AdditionalAnnouncement**, Table 1
- V2.4 p.18: **2.1 AdditionalAnnouncement**, Table 1

The visible PDF tables present a one-of choice and name the third branch `InformationAtSpecificPoint`.

Exact selected XSD authority in every lane instead has two independent boundaries:

1. the surrounding `xs:choice` has `minOccurs="0"`, so the choice may be absent;
2. the third XML branch is named `SpecificPoint`, not `InformationAtSpecificPoint`.

Selected blobs:

- V1.0 `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`
- V2.0 `8608e3dcd665c197c34da7f6ec6af5a3758da164`
- V2.1 `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e`
- V2.2 `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`
- V2.3 `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`
- V2.4 candidate/integration `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`

For V1.0/V2.0/V2.1 the live renderer was not relied upon; the exact-byte pinned render artifacts were inspected:
- V1.0 run `33275626001`, artifact `9721397514`
- V2.0 run `33279811315`, artifact `9722644456`
- V2.1 run `33393002497`, artifact `9758203545`

V2.2/V2.3/V2.4 were visibly rechecked from the official PDF surfaces.

Result: no semantic change.

- CE-013 remains a confirmed cross-artifact structure mismatch.
- `InformationAtSpecificPoint` is not an XSD alias for `SpecificPoint`.
- a payload using the PDF element name where the selected XSD requires `SpecificPoint` must **FAIL**.
- an AdditionalAnnouncement without any choice branch may still be XSD-valid and must not be rejected by an extra PDF-derived rule.
- SDK behavior remains `error_with_advisory`.

## CE-014 — DataVersionList minimum cardinality

Visible body anchors:

- V1.0 p.10: **1.12 DataVersionList**, Table 12 -> `DataVersion 1:*`
- V2.0 p.17: **2.12 DataVersionList**, Table 12 -> `1:*`
- V2.1 p.18: **2.12 DataVersionList**, Table 12 -> `1:*`
- V2.2 p.19: **2.12 DataVersionList**, Table 12 -> `1:*`
- V2.3 p.19: **2.12 DataVersionList**, Table 12 -> `1:*`
- V2.4 p.21: **2.12 DataVersionList**, Table 12 -> `1:*`

Exact selected XSDs all allow **0:***:

- V1.0 inline anonymous list member: line 239, `minOccurs="0" maxOccurs="unbounded"`
- V2.0 `DataVersionListStructure`: line 218
- V2.1: line 219
- V2.2: line 224
- V2.3: line 224
- V2.4 candidate/integration: line 224

The strongest disproof attempt is whether the PDF minimum should be treated as an additional semantic constraint. Under the project authority contract it cannot override the exact selected XSD for conformance.

Result: no semantic change.

- CE-014 remains a confirmed cross-artifact minimum-cardinality mismatch.
- an empty `DataVersionList` that validates against the selected XSD must **PASS**.
- the PDF 1:* statement is advisory/documentation context only.
- V2.4 remains candidate/integration authority only.
- SDK behavior remains `valid_with_advisory`.

## Accounting

- CE-013: `verified_current_standard`
- CE-014: `verified_current_standard`
- structural locator count remains **40**
- current-standard verified becomes **31**
- pending becomes **9**
- next pending finding: **CE-015**

## Gate

- GitHub Actions run: **37339952632**
- result: **SUCCESS**
- validated manifest commit: `d6550dd3f90f18d116e220fbbcb1d5c7dd72e9de`
- structural locators: **40**
- current-standard verified: **31**
- pending current-standard revalidation: **9**
- next pending finding: **CE-015**

The gate validated CURRENT_STATE/body-registry synchronization, the CE-013/CE-014 locator assertions, and the existing audit regression suite.
