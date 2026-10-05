# Visible-body source-locator revalidation — CE-017 / CE-018

Date: 2026-10-05  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`

## Visual evidence method

COMMON V1.0, V2.0 and V2.1 were visually checked from the existing exact-byte pinned render artifacts:

- V1.0 run `33275626001`, artifact `9721397514`
- V2.0 run `33279811315`, artifact `9722644456`
- V2.1 run `33393002497`, artifact `9758203545`

Relevant rendered-page hashes:

- V1.0 p.17: `56f8f8263259c5794afe662012238a4a0b226bac9bb871ea400a3a5b11f7d7b2`
- V1.0 p.21: `6a6780ee47aea02bff11ad19eff8df618efbd6fffb36a32f5ca76b1f3603ab1b`
- V2.0 p.24: `e202d1d4ae06d943311774bb50fa3224b48dcc0a0af36f2a8286678124a37665`
- V2.0 p.29: `053630a4d098c7a130c2645d1e7611668cd06a267a9118f9af1326e6436b2b2d`
- V2.1 p.26: `682a45f9203dd7f62cfa2f258cc466560daa046a6791bed0eb4c8ec28680db40`
- V2.1 p.31: `7f7846616346d770eedc1f1332764722e861deb5c20854e3ccebb1c9c72a25e3`

The live PDF screenshot renderer successfully rendered COMMON V2.2 printed p.33 and visibly confirmed the TSPPoint table. Other requested V2.2-V2.4 screenshots cache-missed or timed out, so the canonical exact-byte fallback was used.

Fallback run: `37349355241`  
Artifact: `11361797577` (`ce1718-visible-body`)

The workflow downloaded and SHA-256-verified the exact official PDFs:

- COMMON V2.2: `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`
- COMMON V2.3: `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`
- COMMON V2.4: `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`

Rendered-page hashes:

- V2.2 p.27: `595803e54433c2fac972660cdb548f1d8121d640bef1162cf6e4395a98d9da6b`
- V2.2 p.33: `f71eba03793ef98b92c177a5456e443e7b82dd27bc8d297249156cac6875c1f4`
- V2.3 p.28: `ed849499804ca7d9b96843d7149842727eb3892b5c435223dc23d87cf86309ce`
- V2.3 p.35: `39728f9dab274a668f94aa98ee3f600e3e3db58ccc91d0bf08c055fb1c83f3ed`
- V2.4 p.30: `54c7fe1358108326670368e46d426c0382fa25f8670f7ef7757efb94238121de`
- V2.4 p.37: `84f88309b21b876db9c7171a1b1db8f4c3e93c69e6586f5a17849f7945cabfaf`

The temporary render workflow was removed again after artifact capture.

## CE-017 — TSPPoint Description versus Desciption

Visible body anchors:

- V1.0 p.21: **1.56 TSPPoint**, Table 56
- V2.0 p.29: **2.59 TSPPoint**, Table 59
- V2.1 p.31: **2.59 TSPPoint**, Table 59
- V2.2 p.33: **2.60 TSPPoint**, Table 60
- V2.3 p.35: **2.60 TSPPoint**, Table 60
- V2.4 p.37: **2.59 TSPPoint**, Table 59

Every checked PDF visibly names the optional repeatable member:

`Description`

The exact selected XSDs instead require the typo-like XML name:

`Desciption`

Exact selected blobs and lines:

- V1.0 `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`, line 662
- V2.0 `8608e3dcd665c197c34da7f6ec6af5a3758da164`, line 673
- V2.1 `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e`, line 672
- V2.2 `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`, line 681
- V2.3 `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`, line 761
- V2.4 candidate/integration `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`, line 813

The strongest disproof attempt is that `Desciption` is obviously typo-like and `Description` is the linguistically plausible form. That does not alter executable authority. The selected XSD is the exact conformance source for the chosen historical/profile lane.

Result: no semantic change.

- CE-017 remains `likely_xsd_defect` with high confidence.
- provider XML using `Description` against an affected selected XSD must **FAIL**.
- no alias, normalization or silent repair is permitted.
- the provider-facing diagnostic must make clear that the rejection is driven by a likely schema typo.
- a future corrected XSD must be represented as a distinct exact schema revision/profile rather than rewriting historical results.
- V2.4 remains candidate/integration authority only.

## CE-018 — ServiceIdentificationWithStateList minimum cardinality

Visible body anchors:

- V1.0 p.17: **1.39 ServiceIdentificationWithStateList**, Table 39 -> `ServiceIdentificationWithState 1:*`
- V2.0 p.24: **2.39 ServiceIdentificationWithStateList**, Table 39 -> `1:*`
- V2.1 p.26: **2.39 ServiceIdentificationWithStateList**, Table 39 -> `1:*`
- V2.2 p.27: **2.40 ServiceIdentificationWithStateList**, Table 40 -> `1:*`
- V2.3 p.28: **2.40 ServiceIdentificationWithStateList**, Table 40 -> `1:*`
- V2.4 p.30: **2.39 ServiceIdentificationWithStateList**, Table 39 -> `1:*`

The exact selected XSD family instead consistently declares:

`minOccurs="0" maxOccurs="unbounded"`

for the `ServiceIdentificationWithState` list member.

Exact lines:

- V1.0 line 484
- V2.0 line 490
- V2.1 line 489
- V2.2 line 498
- V2.3 line 548
- V2.4 candidate/integration line 563

The strongest disproof attempt is whether the PDF minimum should be treated as an additional semantic rule. Under the project authority contract it cannot override an exact selected XSD that accepts the empty list.

Result: no semantic change.

- CE-018 remains a confirmed cross-artifact minimum-cardinality mismatch.
- an empty `ServiceIdentificationWithStateList` that validates against the exact selected XSD must **PASS**.
- the stricter PDF minimum is advisory/documentation context only.
- SDK behavior remains `valid_with_advisory`.
- V2.4 remains candidate/integration authority only.

## Accounting

- CE-017: `verified_current_standard`
- CE-018: `verified_current_standard`
- structural locator count remains **40**
- current-standard verified becomes **35**
- pending becomes **5**
- next pending finding: **CE-019**

## Gate

Pending.
