# SOURCE LOCATOR REVIEW — DRCOM21-001 — 2026-11-12

**Status:** Original official PDF/XSD evidence and six-version boundaries verified; terminal gate status and continuation authority remain exclusively `00_START_HERE/CURRENT_STATE.json` and GitHub Actions.

## Finding identity and conclusion

Keep **one existing `DRCOM21-001`**. Original official Common PDFs **V2.0–V2.4** each visibly specify **`StopInformationRequest.StopName 0:1`**, whereas the corresponding exact selected Common XSD declares **`minOccurs="0" maxOccurs="unbounded"`** (0:*). Earlier historical V2.1-only scope was incomplete. The field in the distinct `StopInformationStructure` is 1:* and must not be conflated. `DRCOM23-001` concerns separate V2.3 `ArrivalExpected`/`DepartureExpected` request placement and remains an independent finding.

**Disproof/source attribution:** `0:1` is present as an actual member-row maximum in five original visible tables; it is not a choice-notation marker, generic text label, derived TOC number, or V2.1-specific editorial variant. Exact selected XSD member declarations are repeatedly `0:*`. Whether the PDF is too restrictive or the XSD intentionally/accidentally over-permissive is **not independently established** by the publisher. Consequently retain the proven difference as `cross_artifact_mismatch` instead of the historical source-attribution label `confirmed_pdf_defect`. Preserve the earlier assessment in Git history.

## Exact-byte official original body sources

The original GitHub Actions rendered pages were downloaded and their PNG SHA-256 checked against the archived per-page manifest. For V2.2, previous full-render artifact was no longer accessible; the required pinned fallback was requested on [commit faa30405](https://github.com/MarcLeinenDE/VDV301/commit/faa30405ba78a02ad7539e356cb54861a4ad5b73) and completed [run 43216104609](https://github.com/MarcLeinenDE/VDV301/actions/runs/43216104609) SUCCESS, artifact `13944345486`. Its manifest separately proves exact official source SHA256 and 1411558 bytes, 55 pages, PyMuPDF 160dpi; rendered original p31 SHA256 `a072381c3477de238461a0ca5a69882fbc0cc1da5b20ec417f01dbd51504aaba` verified locally. The body table was visually inspected, not only searched as text.

| Official Common PDF | Actual printed body locator | Original PDF SHA-256 | Bytes | Checked original PNG SHA-256 (page order) | Run / artifact |
| --- | --- | --- | ---: | --- | --- |
| V1.0 (predecessor) | p19 §1.48 Table48 StopInformation, p20 §1.50 Table50 StopSequence | `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf` | 892769 | `48c89183aeb69a335687da8321990e4dc79b4ab0062181ee1ea160edbf922346 / 74c8f525df2d2b14e63fdbb5b2eec2e51bd2bbb28c3110aa967fff6bdb661282` | 33275626001 / 9721397514 |
| V2.0 | p27 §2.51 Table51 | `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088` | 946088 | `71d3999b383690495891ee390ef3836fddc87503d2d92874e4ad2e5ecd5d536f` | 33279811315 / 9722644456 |
| V2.1 | p29 §2.51 Table51 | `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32` | 1274051 | `2493af2ea41abe8c72e1d351762acf54412b7f05cdd04f25cce7736843a1fde5` | 33393002497 / 9758203545 |
| V2.2 | p31 §2.52 Table52 | `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203` | 1411558 | `a072381c3477de238461a0ca5a69882fbc0cc1da5b20ec417f01dbd51504aaba` | 43216104609 / 13944345486 |
| V2.3 | p32 §2.52 Table52 | `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b` | 793521 | `b9f7576dd7654b3976fd7d05e7d2d653e07a2c912ab60c7fa2d8514dcdd1b904` | 33656579631 / 9856965744 |
| V2.4 | p34 §2.51 Table51 begins, caption on p35 | `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a` | 1689647 | `d3d1f03a989ae3f18349b747643307567ff3e873862014e7c642b46bedd54a16 / 9a333351c0ef89a63067595482fdff7f26b59808c40f693ba2d1e32bf6fb24bd` | 33658306978 / 9857652638 |

Specifically: V2.0 p27 §2.51 **Table 51**; V2.1 p29 §2.51 **Table 51**; V2.2 p31 §2.52 **Table 52**; V2.3 p32 §2.52 **Table 52**. V2.4 §2.51 starts on **p34**, where the StopName row visibly reads `0:1`, and its actual **Table 51 caption** is printed on p35; **both pages** were inspected. These are body-derived locators, never inferred from TOC/history.

### V1.0 predecessor boundary

The pinned official 36-page V1.0 original was searched for a request-specific heading and its visible printed body p19–20 inspected: **§1.48 Table 48 is `StopInformation` (StopName `1:*`), followed by §1.49 Table 49 `StopPointTariffInformation` and §1.50 Table 50 `StopSequence`**. No corresponding standalone `StopInformationRequest` member table appears in this PDF. Its exact official XSD already defines `StopInformationRequestStructure.StopName 0:*` (blob `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`, line 532). The predecessor is **noncomparable as a PDF/XSD claim**, not a previously corrected PDF version. The V1.0 schema member alone cannot extend the PDF/XSD-mismatch trigger backwards.

## Exact selected XSD members and authority classes

The child XPath for each exact XSD is `/xs:schema/xs:complexType[@name='StopInformationRequestStructure']/xs:sequence/xs:element[@name='StopName']`.

| Common XSD | Git blob | Line | XSD member rule | XSD authority |
| --- | --- | ---: | --- | --- |
| `IBIS-IP_common_V1.0 (predecessor).xsd` | `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c` | 532 | `minOccurs="0" maxOccurs="unbounded"` | `official_release` |
| `IBIS-IP_common_V2.0.xsd` | `8608e3dcd665c197c34da7f6ec6af5a3758da164` | 538 | `minOccurs="0" maxOccurs="unbounded"` | `official_release` |
| `IBIS-IP_common_V2.1.xsd` | `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e` | 537 | `minOccurs="0" maxOccurs="unbounded"` | `official_release` |
| `IBIS-IP_common_V2.2.xsd` | `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` | 546 | `minOccurs="0" maxOccurs="unbounded"` | `official_release` |
| `IBIS-IP_common_V2.3.xsd` | `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` | 596 | `minOccurs="0" maxOccurs="unbounded"` | `official_release` |
| `IBIS-IP_common_V2.4.xsd` | `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` | 611 | `minOccurs="0" maxOccurs="unbounded"` | `candidate_integration` |

V2.0–V2.3 use the exact selected **historical official** XSD/dependency routes. V2.4 has a **published official PDF** but the selected XSD blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` remains **candidate/integration**, not promoted to official; upstream PR #31 was still open. Common V2.3 retains its historical Enumerations V2.2 dependency. No `latest wins`, no schema replacement or alias.

## Executable evidence, deliberate limits and SDK result

Preserved **EV-119** establishes on exact Common V2.1 that a request with **two StopName elements is XSD VALID**; historical EV-137 closeout run `33857041308` documents that state. EV-118 and EV-120/121/122 are preserved related Common-profile evidence. **No fresh five-version XML instance positive/negative matrix was executed in this source-locator block**; five exact selected XSD declarations and original PDF layout were independently verified instead.

**Classification:** `cross_artifact_mismatch` / `cardinality_mismatch`, PDF maximum 0:1 vs selected XSD maximum `unbounded`, `valid_with_advisory`. SDK behavior: never impose the PDF limit on already XSD-valid XML, attach only optional explanation on existing `VALID`. Runtime mapping stays `reviewed_not_implemented`; no productive matcher. No XSD bytes, root adapters, selected routes, or production runtime were changed.

**Version-scope conclusion:** first independently confirmed conflicting selected pair **Common V2.0**; intermediate official V2.1–V2.2; last official selected XSD **V2.3**; last checked published Common PDF paired with explicit candidate/integration schema **V2.4**. V1.0 noncomparable PDF predecessor. No verified later corrected successor; no separate German/English publication track inferred from bilingual contents.

## Canonical synchronization and continuation

Update the **same** semantic finding and reviewed SDK mapping scopes, add exactly one six-lane source locator (`supporting_evidence` included), one visible body record and one verified boundary record. Mirror `93/192`, `93/93`, `99 remaining` in canonical `CURRENT_STATE.json` and SDK summary. A substantive `gate_pending` commit must pass full Schema-Audit-Validation and Handoff Integrity. Then a separately committed `terminal_clean` handoff and final HEAD Handoff Integrity must pass before ai-mem PR or proceeding to next unique **`DRCOM22-001`**. Never count a scope correction as a new finding identity or alter a historical PDF/XSD source.

