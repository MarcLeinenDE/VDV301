# Source locator review — DRCOM24-001 — 2026-11-12

**Scope and provenance:** One historical `DRCOM24-001` finding, not a new identity. This describes a **published official Common V2.4 PDF** compared with an **explicitly selected Common V2.4 candidate/integration XSD**; **no official Common V2.4 strict XSD profile** has been independently established. The previous historical terminal finding remains `manually_reviewed` / `no_strict_xsd_profile` / `unsupported_profile`; no runtime matcher is implemented or implied. This is the **second independent terminal audit cycle** requested after fully closing `DRCOM23-001`.

## Actual contradiction and disproof

The official original Common V2.4 PDF **printed page 28, §2.31 LineInformation**, visibly documents `LineName 0:1 IBIS-IP.string` and `LineShortName 0:1 IBIS-IP.string`. The full member table actually begins and ends on **printed p28**; its visible **Table 31 — Description of LineInformation caption is printed at the top of p29**, verified independently. A prior p28-only page citation is therefore insufficient for an exact table-caption locator; p28+p29 must be pinned together.

The exact selected candidate/integration `IBIS-IP_common_V2.4.xsd` blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` instead declares `LineInformationStructure.LineName` (line442) and `LineShortName` (line443) as **`InternationalTextType`, `minOccurs=0`, `maxOccurs=unbounded`**. This differs in both XML type/member shape and cardinality. The historical candidate `EV-122` validates InternationalTextType-shaped single/repeated values for **each member** and rejects the PDF-derived `IBIS-IP.string`-shaped single-member form. The test uses a synthetic `LI` harness root; that test root is not a claim about a published global application root.

Strongest disproof hypotheses:
1. The PDF's `IBIS-IP.string` might just be shorthand for `InternationalTextType`: **not supported**, because the two are separately modelled structures; EV-122 confirms distinct accepted XML shapes.
2. `0:1` might be a choice/compositor marker: **not supported**; these are ordinary `LineName` and `LineShortName` member rows and predecessor tables use `0:*` explicitly.
3. The discrepancy might already have existed in an older official release: **rejected** by independently checking every published Common V1.0–V2.3 original body and exact selected historical XSD.
4. The V2.4 candidate XSD may be the *official* schema: **rejected** by provenance. Upstream [VDVde/VDV301 PR #31](https://github.com/VDVde/VDV301/pull/31) remains open and unmerged at this verification. An official `VDV-301-2.4` release tag did not resolve. The publication's official PDF status does **not** grant official release authority to the candidate XSD.

Thus classify **`cross_artifact_mismatch`** with **candidate-only executable behavior**; do not attribute a confirmed defect to an unreleased candidate or treat the PDF alone as an executable released XSD. Preserve source uncertainty; no latest-wins or compatibility alias.

## Independent original published PDF bodies

Each original official PDF is byte- and size-pinned in the canonical source registry. Actual visible body table heading, rows, cardinality, types and captions were inspected on **each version**; page hashes are from corresponding original archived render manifests.

| Official published Common PDF | Actual printed body locator | LineName / LineShortName in PDF | Original PDF SHA-256 (bytes) | Original page PNG SHA-256 / render evidence |
| --- | --- | --- | --- | --- |
| **V1.0** (DE) | **p15 §1.31 Table 31 — Description of LineInformation** | **`0:*` `+InternationalTextType`** for both | `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf` (892769) | `ee04c205a5ea2631b56dab16e1e429ccfe046da7353e69bad50af087320f5f13`; run 33275626001/artifact 9721397514 |
| **V2.0** (DE/EN) | **p22 §2.31 Table 31 — Description of LineInformation** | `0:*` `+InternationalTextType` for both | `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088` (946088) | `591644194d2f5edbf085bd589ee2c7ef9e2199a2c500696ee75046d183fa5a08`; run 33279811315/artifact 9722644456 |
| **V2.1** (DE/EN) | **p24 §2.31 Table 31 — Description of LineInformation** | `0:*` `+InternationalTextType` for both | `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32` (1274051) | `709c501675f7393b8ff2d0dd25326a954da823a4906bc9f44443d1018d63d121`; run 33393002497/artifact 9758203545 |
| **V2.2** (DE/EN) | **p25 §2.31 Table 31 — Description of LineInformation** | `0:*` `+InternationalTextType` for both | `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203` (1411558) | `2ebf0c6f83c5c86acb9ce7875d36967d61d006476b7bb044479972f30ef9cf03`; fresh SHA-pinned deterministic fallback [run 43267750888](https://github.com/MarcLeinenDE/VDV301/actions/runs/43267750888), artifact 13966458352 |
| **V2.3** (DE/EN) | **p26 §2.31 Table 31 — Description of LineInformation** | `0:*` `+InternationalTextType` for both | `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b` (793521) | `d177fad7b44a43305467991ce985551f38fffa28ad3b880410ac9104551d7ca2`; run 33656579631/artifact 9856965744 |
| **V2.4** (DE/EN, disputed) | **p28 §2.31 LineInformation actual field table; p29 actual Table 31 caption** | **`0:1` `IBIS-IP.string`** for both | `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a` (1689647) | p28 `034a35e383793d622dec45d6a3d71d965e6cf5f6ec343d0711f298da8ad2c814`, p29 `697bda69bc5aedc769583b116b24a01761ba87d812c2ea6655cd7b64dafdf8d6`; run 33658306978/artifact 9857652638 |

The V2.2 original complete artifact was unavailable for direct reuse, so `tools/render_vdv_pdf_pages.py` with **the exact original official pin** was invoked after an atomic `gate_pending` render request on work-branch commit `9bebbbe11c631244cf20a4ab9cffc114dfc1d22f`. [Run 43267750888](https://github.com/MarcLeinenDE/VDV301/actions/runs/43267750888) SUCCESS rendered p23–26 at 160dpi from verified original **SHA-256 `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203` and exact **1411558 bytes**. Actual target is **printed page25**, not guessed from an adjacent edition; its original PNG hash `2ebf0c6f83c5c86acb9ce7875d36967d61d006476b7bb044479972f30ef9cf03` was independently recomputed and visibly verified.

No earlier official publication displays this V2.4 PDF string/0:1 pair; the **last matching predecessor** is V2.3. No later released successor is independently established. No independent German/English version track correcting this discrepancy was found: common published V2.0–V2.4 source documents are bilingual.

## Exact selected XSD blobs and line positions

| Selected Common XSD | Exact Git blob | `LineInformationStructure.LineName` / `LineShortName` lines | Exact selected schema declaration | Authority |
| --- | --- | --- | --- | --- |
| `IBIS-IP_common_V1.0.xsd` | `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c` | 383 / 384 | both `InternationalTextType` `0:*` | official historical |
| `IBIS-IP_common_V2.0.xsd` | `8608e3dcd665c197c34da7f6ec6af5a3758da164` | 389 / 390 | both `InternationalTextType` `0:*` | official historical |
| `IBIS-IP_common_V2.1.xsd` | `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e` | 388 / 389 | both `InternationalTextType` `0:*` | official historical |
| `IBIS-IP_common_V2.2.xsd` | `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` | 392 / 393 | both `InternationalTextType` `0:*` | exact historical upstream file lineage, no invented `VDV-301-2.2` tag |
| `IBIS-IP_common_V2.3.xsd` | `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` | 442 / 443 | both `InternationalTextType` `0:*` | `VDV-301-2.3` official; historical Enumerations V2.2 dependency |
| `IBIS-IP_common_V2.4.xsd` | `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` | 442 / 443 | both `InternationalTextType` `0:*` | **candidate/integration**, exact Enumerations `2afed8cf23afa91db92b0f043cc5b4ad428b0f25` |

Member XPath: `/xs:schema/xs:complexType[@name='LineInformationStructure']/xs:sequence/xs:element[@name='LineName' or @name='LineShortName']`. The V2.4 candidate retained earlier XSD member definitions despite the official V2.4 PDF editorial/type/cardinality change. **No official strict V2.4 XSD profile** is thereby established. The PDF must not silently become a fabricated executable schema or production runtime rule.

## Preserved tests, SDK limits, and terminal workflow

Historical **EV-122**, `tools/validate_common_v24_ev122.py`, run **33716645876** (EV-140 closure **33973935324**), verifies under the selected explicit **V2.4 candidate** profile: correctly formed `InternationalTextType` values for both fields accepted, repeated `LineName` and repeated `LineShortName` accepted, and PDF-derived simple `IBIS-IP.string`-shaped values rejected. It uses a synthetic `LI` root to isolate `LineInformationStructure`; not a claim about an official production `LineInformation` document root. No new cross-version XML test matrix executed in this source-locator cycle.

**SDK semantics:** retain `normative_authority=no_strict_xsd_profile`, `sdk_behavior=unsupported_profile`, `runtime_match=not_applicable` and `review_state=manually_reviewed`. The selected candidate profile may be explicitly compiled/validated in an analysis context, but must never be claimed as an official Common V2.4 strict SDK profile. An official-strict request must remain **fail-closed**, not accept the candidate XML shape as released, and no compatibility alias/auto-normalization or code generation rule from the PDF is authorized. Historical official V1.0–V2.3 results remain unchanged. `CE-020` and unrelated V2.4 nomenclature issues are separate.

At the substantive atomic `gate_pending` commit: keep the existing single semantic finding `DRCOM24-001`, append one six-lane source-locator, one visible-body verified record and one independently verified version boundary record; synchronize semantic source blob pins, the SDK manifest and `CURRENT_STATE.json`. Expected **96/192** locators, **96/96** body/scope, **96 remaining**; next unique **`DRDMS22-001`**. Require full schema-audit-validation and handoff-integrity SUCCESS, then separately `terminal_clean` and final-head Handoff Integrity before Memory PR. **No XSDs, runtime matcher or official-facing PR modified.**
