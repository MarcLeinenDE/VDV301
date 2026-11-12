# Source locator review — DRCOM22-001 — 2026-11-12

**Scope:** Revalidate one existing `DRCOM22-001` against all official Common PDF versions V1.0–V2.4 and each exact selected XSD, including the separate V2.4 candidate/integration authority. This is audit evidence, **not** XSD or runtime remediation. Current continuation and gate status remain solely canonical in `00_START_HERE/CURRENT_STATE.json`.

## Finding and disproof

Published original official Common PDFs V2.2, V2.3 and V2.4 show two `NetexMode` choice blocks — a general `PtMainMode`/`PrivateMainMode` one-of and a public/private submode one-of — each with `–1:1` under **VDV choice notation**. The leading dash signals an XML one-of choice, not negative minOccurs. The actual printed choice-group maximum `1:1` denotes a required one-of. By contrast each **exact selected** Common XSD `NetexMode` type has a sequence containing **two** outer `xs:choice` compositors, **each `minOccurs="0"`**. Therefore an empty instance of that **type** can be valid in the exact schema; the PDF one-of requirement is not an enforceable additional selected-XSD validity condition.

Strongest counter-explanations examined: (1) the PDF dash could be a numeric negative — rejected by project-wide VDV choice notation evidence and the document's aligned `PointType` choice; (2) the PDF may intentionally express a semantic requirement beyond permissive XSD template shape — possible, but it does **not** alter executable XSD acceptance; (3) different predecessor/tag/candidate schema — ruled out by exact selected XSD blobs and historical dependency lanes. Attribution to a PDF error **versus** a permissive XSD remains unproven; correct classification is **`cross_artifact_mismatch`**, replacing the historically narrower `confirmed_pdf_defect` attribution while preserving historical evidence.

## Original byte-pinned PDF body evidence

Original render artifacts were obtained from the same byte-pinned official sources recorded in `audit_registry/pdf_source_registry_v0.1.json` and `audit_registry/pdf_source_pins_v0.1.json`. Original body page PNG hashes were recomputed and compared to original archived manifests; V2.3 and V2.4 ZIP-embedded PDFs were independently SHA-256 checked. The live PDF screenshot renderer returned a **cache miss for V2.2**; the existing exact-byte GitHub **EV-138** fallback render sufficed and was visually inspected instead of claiming a visual limitation.

| Published Common source | Original visible body target | Original PDF SHA-256 / bytes | PNG SHA-256 (verified) | Render run / artifact |
| --- | --- | --- | --- | --- |
| V2.2, 08/2019 | **printed p15 §1.18, Table 20 — Description of NetexMode**; both choice blocks `–1:1` | `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`, **1411558 B** | `bdf9073a1e82458c76e7c727aa5f093da9b36eaee20596332af42a669470081a` | [33857241506](https://github.com/MarcLeinenDE/VDV301/actions/runs/33857241506), `9930671790` (`common-v22-ev138`) |
| V2.3, 02/2021 | **printed p15 §1.18, Table 20 — Description of NetexMode**; both choice blocks `–1:1` | `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`, **793521 B** | `f5a33a1cc837192d4c999432fd4747134f2a53158e0f5cdf786773c502958af6` | [33656579631](https://github.com/MarcLeinenDE/VDV301/actions/runs/33656579631), `9856965744` (`common-v23-pinned-read`) |
| V2.4, 01/2023 | **printed p17 §1.18, Table 20 — Description of NetexMode**; both choice blocks `–1:1` | `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`, **1689647 B** | `f830bd02a7e707ab536e486fb476ce74f5905e66f39af3a82a588adf14228094` | [33658306978](https://github.com/MarcLeinenDE/VDV301/actions/runs/33658306978), `9857652638` (`common-v24-pinned-read`) |

All three pages were visually read including table caption, both grouping markers, child rows and adjacent prose. The `1.18` / `Table 20` identifiers are the actual visible **body**, not TOC, history or inferred sequential numbering. The different `2.34 NetexMode` table error in Common V2.2–V2.3 is recorded separately under `CE-023`; it must not be counted as this group's source.

## Independently verified predecessor and language/version boundaries

| Version | Original PDF SHA-256 | Exact selected Common XSD Git blob | Boundary result |
| --- | --- | --- | --- |
| V1.0 (German) | `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf` | `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c` | Entire pinned 36-page original text and XSD contain **no NetexMode**. Nonaffected predecessor. |
| V2.0 (DE/EN) | `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088` | `8608e3dcd665c197c34da7f6ec6af5a3758da164` | Entire pinned 45-page original text and XSD contain **no NetexMode**. Nonaffected predecessor. |
| V2.1 (DE/EN) | `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32` | `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e` | Entire pinned 48-page original text and XSD contain **no NetexMode**. **Last nonaffected predecessor**. |

The exact full-text snapshots were read and searched (not merely TOCs): SHA-256 V1.0 `fdfdf62a88f78dd7a59b341157662d3e5708b2f9c56d2cf1df13a7d4eb0cfa0a`, V2.0 `05e8a7e1788318bf5ac83ffdd61125622e28ce30f4fc5f388467a41ed46f5a3f`, V2.1 `5dce4c8ecc770574bdce8d5961fefbc01f88b1547e3957855013d9b077fc24b0`. V2.2's published version history §4.4.1 explicitly states **NetexMode added as a new data type (1.18)**, corroborating the first affected version. No fabricated PDF table locators for absence. V2.2–V2.4 PDFs are published bilingual source editions; no independently different language-specific schema correction is established. A later corrected **official successor after V2.4 was not verified**; do not invent one.

## Exact selected XSD/authority and executable behavior

Common XSD member XPath: `/xs:schema/xs:complexType[@name='NetexMode']/xs:sequence/xs:choice` (two sibling choice compositors).

| Exact selected XSD | Git blob | Choice lines | Authority and dependency |
| --- | --- | --- | --- |
| `IBIS-IP_common_V2.2.xsd` | `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` | 961 / 965 | Historical upstream V2.2 file lineage, with exact Enumerations V2.2; **no invented VDV-301-2.2 tag** |
| `IBIS-IP_common_V2.3.xsd` | `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` | 1041 / 1045 | **official_release** `VDV-301-2.3`, historically includes **Enumerations V2.2** |
| `IBIS-IP_common_V2.4.xsd` | `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` | 1093 / 1097 | Explicitly selected **candidate_integration** XSD; the V2.4 PDF is official but candidate schema is **not** an official release |

Historical exact-profile executable tests already in the repo:

- `tools/validate_common_v22_ev120.py`: exact pinned Common V2.2 / Enumerations V2.2, **`<TestNetexMode/>` VALID**, populated branch also VALID; existing EV-120 PASS run `33620003188`, EV-138 revalidation `33857443446`.
- `tools/validate_common_v23_ev121.py`: exact official V2.3 / Enumerations V2.2, synthetic harness **`<N/>` VALID**, populated branch VALID; file reviewed.
- `tools/validate_common_v24_ev122.py`: exact selected V2.4 candidate/integration, synthetic harness **`<N/>` VALID**, populated branch VALID; file reviewed.

These are **synthetic test roots for the `NetexMode` type**, not assertions that a global production XML document root literally named `NetexMode` is necessarily declared. No new multi-version XML fixture execution was performed during this locator cycle. The preserved historical harnesses plus static exact-XSD inspect establish the affected shape without replacing the selected XSD result.

## SDK and history-safe conclusion

**Unique finding:** `DRCOM22-001` retained; original V2.2-only semantic/runtime scope extended to **official Common V2.2 and V2.3**, plus **official V2.4 PDF / selected V2.4 candidate/integration XSD**. V1.0–V2.1 excluded. `cardinality_mismatch`, `choice_compositor_optionality`, `cross_artifact_mismatch`; cause unassigned. Selected schema still returns **VALID** for an empty NetexMode type. An optional `valid_with_advisory` may only decorate existing XSD-valid results and remains **`reviewed_not_implemented`**, never an added schema failure, compatibility alias or XSD mutation.

`CE-023` remains separately documented (corrupt duplicate NetexMode table V2.2–V2.3, corrected documentation V2.4); this finding is not a duplicate or remediation of `CE-023`. Historical older V2.2-only snapshots remain untouched.

At the substantive `gate_pending` milestone, synchronize affected semantic/runtime scope, source-locator six-version coverage, original-PDF body verification, independent version boundary registry, SDK mirror and `CURRENT_STATE.json` in **one atomic commit**. Expected **94/192 source locators**, **94/94 visible-body and version boundary**, **98 pending**. Require full `schema-audit-validation` and `handoff-integrity` SUCCESS for substantive HEAD, then separately commit `terminal_clean` handoff and verify the final HEAD; only then migrate durable memory through a reviewed PR. Next unique finding **`DRCOM23-001`**.
