# Visible-body source-locator revalidation — CE-015 / CE-016

Date: 2026-10-05  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`

## Visual evidence method

The live PDF screenshot renderer cache-missed COMMON V2.2, V2.3 and V2.4. Per the canonical fallback rule, a temporary read-only GitHub Actions render was used against the same official VDV URLs.

Fallback run: `37344880254`  
Artifact: `11360276214` (`ce1516-visible-body`)

The workflow downloaded and SHA-256-verified:

- COMMON V2.2: `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`
- COMMON V2.3: `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`
- COMMON V2.4: `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`

Rendered page hashes:

- V2.2 printed p.24: `10ee8e05d97c80bfae1c909fd6744cf8de4424cfc0d98c1c12c25d80ad281c4b`
- V2.3 printed p.24: `682a9b69e6b5904651c8bcba9667a9324656212cc1c7d2e5a7c76fbf8398c92f`
- V2.4 printed p.26: `97fb5a74b57cbfe48fe53f84cc2cbad6c9d1142b26001cd9235d0d3ba4ae522f`

COMMON V1.0/V2.0/V2.1 were visually checked from their existing exact-byte pinned artifacts:

- V1.0 run `33275626001`, artifact `9721397514`, printed p.14 hash `c241515dea4de9e459427b95dd877d35a84a3a77d1b276ca189d0c346b0cbdb8`
- V2.0 run `33279811315`, artifact `9722644456`, printed p.21 hash `d25a4dc3a8166ee364bd009d4ac259859e6152d4feeb9cb086312e44dee5c186`
- V2.1 run `33393002497`, artifact `9758203545`, printed p.23 hash `57d4ca913c243bf17167730b4523c52ab78e0a8e77ac4dc58b27e445308ab5d4`

The temporary render workflow was removed again after artifact capture.

## CE-015 — Farezone* versus FareZone*

Visible body anchors:

- V1.0 p.14: **1.26 FareZoneInformation**, Table 26
- V2.0 p.21: **2.26 FareZoneInformation**, Table 26
- V2.1 p.23: **2.26 FareZoneInformation**, Table 26
- V2.2 p.24: **2.26 FareZoneInformation**, Table 26
- V2.3 p.24: **2.26 FareZoneInformation**, Table 26
- V2.4 p.26: **2.26 FareZoneInformation**, Table 26

All visible PDF tables spell the four XML-facing member names with lower-case `z` after Fare:

- `FarezoneID`
- `FarezoneType`
- `FarezoneLongName`
- `FarezoneShortName`

The exact selected XSDs instead consistently require:

- `FareZoneID`
- `FareZoneType`
- `FareZoneLongName`
- `FareZoneShortName`

Selected blobs:

- V1.0 `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`
- V2.0 `8608e3dcd665c197c34da7f6ec6af5a3758da164`
- V2.1 `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e`
- V2.2 `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`
- V2.3 `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`
- V2.4 candidate/integration `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`

Active disproof attempt: could the PDF forms be presentation-only labels? For XML conformance this does not create aliases. Element names are case-sensitive and the selected XSDs expose only the `FareZone*` spellings.

Result: no semantic change.

- CE-015 remains a confirmed cross-artifact identifier-case mismatch.
- provider XML using `Farezone*` where the selected XSD requires `FareZone*` must **FAIL**.
- the diagnostic may explain the PDF spelling but must not normalize or repair the payload.
- SDK behavior remains `error_with_advisory`.
- V2.4 remains candidate/integration authority only.

## CE-016 — GlobalCardStatusID versus GlobalCardStausID

The same visible pages also contain the GlobalCardStatus table:

- V1.0 p.14: **1.27 GlobalCardStatus**, Table 27
- V2.0 p.21: **2.27 GlobalCardStatus**, Table 27
- V2.1 p.23: **2.27 GlobalCardStatus**, Table 27
- V2.2 p.24: **2.27 GlobalCardStatus**, Table 27
- V2.3 p.24: **2.27 GlobalCardStatus**, Table 27
- V2.4 p.26: **2.27 GlobalCardStatus**, Table 27

Every checked PDF visibly names the required member:

`GlobalCardStatusID`

The exact selected XSDs instead require the typo-like spelling:

`GlobalCardStausID`

Exact lines:

- V1.0 line 320
- V2.0 line 326
- V2.1 line 325
- V2.2 line 329
- V2.3 line 379
- V2.4 candidate/integration line 379

The strongest disproof attempt is that `GlobalCardStausID` is obviously typo-like and the PDF form is linguistically plausible. That does not alter executable authority. Under the project contract, the exact selected XSD remains normative even when the schema itself likely contains the defect.

Result: no semantic change.

- CE-016 remains `likely_xsd_defect` with high confidence.
- historical conformance must nevertheless use the exact typo-like XSD name.
- provider XML using `GlobalCardStatusID` against an affected selected XSD must **FAIL**.
- the SDK diagnostic must attribute the likely specification/XSD defect clearly so the provider is not misleadingly blamed.
- no silent alias, normalization or repair is permitted.
- a future corrected XSD must be represented as a new exact schema revision/profile rather than retroactively changing historical results.

## Accounting

- CE-015: `verified_current_standard`
- CE-016: `verified_current_standard`
- structural locator count remains **40**
- current-standard verified becomes **33**
- pending becomes **7**
- next pending finding: **CE-017**

## Gate

- GitHub Actions run: **37345434046**
- result: **SUCCESS**
- validated manifest commit: `7140623cb53f1fb4d846d46e91e7ad469f0a46db`
- structural locators: **40**
- current-standard verified: **33**
- pending current-standard revalidation: **7**
- next pending finding: **CE-017**

The gate validated CURRENT_STATE/body-registry synchronization, the CE-015/CE-016 locator assertions, and the existing audit regression suite.
