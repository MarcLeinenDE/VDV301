# SOURCE LOCATOR REVIEW — DRCOM20-001 — 2026-11-12

**Evidence status:** five exact original official Common PDF tables V2.0–V2.4, one V1.0 predecessor lacking comparable type table, exact selected Common XSD blobs, historical executable tests and version/language boundaries checked. Actual terminal state and gate success remain **only** in `00_START_HERE/CURRENT_STATE.json` and GitHub Actions.

## Identity, material discrepancy and disproof

Existing unique **DRCOM20-001**, not an added finding: each original published Common V2.0–V2.4 PDF in **§1.17 InternationalTextType / Table 17** says `Value 1:1 IBIS-IP.string`, `Language 1:1 IBIS-IP.language`. Each **exact selected** Common XSD instead declares children `Value xs:string`, `Language xs:language` directly. The IBIS-IP named structures also exist in each schema as distinct **complex wrapper types**, with their own required nested `Value` and optional `ErrorCode`. Literal PDF-derived wrapper XML introduces an unallowed nested element; strict XSD INVALID is normative. This is a material `wrong_type_reference` / `primitive_vs_wrapper_type_mismatch`, not harmless abbreviation or an alias. No silent XML repair, mutation, runtime matcher or newly promoted XSD authority.

## Visible original body locators and source hashes

The following original PDF pages were **actually opened** from the official pinned GitHub Actions render sources; each page PNG SHA256 was independently matched to its artifact page-hash manifest; the original PDF source SHA256 and byte size were matched to frozen official source pins. V2.2 page12 was freshly fetched/rendered from exact official PDF on request commit `7f0e918b085f37220629a72ce92a9be6e467ad7e`, run `43160761440`, artifact `13918320243`. No inferred table index or OCR-only locator was used.

| Official Common PDF | Printed visible target | Original PDF SHA-256 | PDF bytes | Target PNG SHA-256 | Run / artifact |
| --- | --- | --- | ---: | --- | --- |
| V2.0 | p13 §1.17 **Table 17** | `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088` | 946088 | `1151012f58615b9bba2f93639e5b642ffa0ffb10f9967953a2d845d9e73b4e2c` | [33279811315](https://github.com/MarcLeinenDE/VDV301/actions/runs/33279811315) / `9722644456` |
| V2.1 | p12 §1.17 **Table 17** | `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32` | 1274051 | `a9bfcc2456e4f8be6833c30bfba6ab0e252c7f19d2ec605ca05c828dea67f561` | [33393002497](https://github.com/MarcLeinenDE/VDV301/actions/runs/33393002497) / `9758203545` |
| V2.2 | p12 §1.17 **Table 17** | `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203` | 1411558 | `975b0c2c7d0ea38d05329a49cb7dd8469545190887598c760f230683d531e26b` | [43160761440](https://github.com/MarcLeinenDE/VDV301/actions/runs/43160761440) / `13918320243` |
| V2.3 | p12 §1.17 **Table 17** | `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b` | 793521 | `c39c28106931c5a6af5acf7879e190c99a6c7f2bd7cd2867bc586bfb132204f4` | [33656579631](https://github.com/MarcLeinenDE/VDV301/actions/runs/33656579631) / `9856965744` |
| V2.4 | p14 §1.17 **Table 17** | `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a` | 1689647 | `f647f3af34ee57c5ad31cc52f2513f1efacbf380182e2bee7a1bd2fa43ccaae7` | [33658306978](https://github.com/MarcLeinenDE/VDV301/actions/runs/33658306978) / `9857652638` |

V2.0 original caption is German `Tabelle 17 — Beschreibung von InternationalTextType`; V2.1–V2.4 show English `Table 17 — Description of InternationalTextType`. The exact printed table rows, not the language of the caption, show the same conflicting **English XML** type references in all five editions.

## V1.0 predecessor is not a fabricated corrected release

The 36-page original Common V1.0 PDF (SHA256 `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf`, 892769 bytes) was searched in full and actual visible body pages checked: p7 **§1.1 Table1** references `+InternationalTextType` for `AnnouncementText`, PNG `28ff536a697d9e49a0e3a02deb92e6823ffa8b99aad8f056a3ef1d819edc5e32`, while p11 **§1.17 Table17** is **DeviceSpecificationWithState**, PNG `8d14a022ee3f3669661d5ed2eb2a6cb79a7479178b3732c57bccf5323a7f34df`. The original V1.0 document contains no **standalone InternationalTextType member type table** comparable to later §1.17 Table17. Its exactly selected official **V1.0 Common XSD** already declares direct primitive `Value` and `Language` (blob `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`, lines 708/709). V1.0 is therefore a **noncomparable predecessor**, not proof that the later PDF error was previously corrected and not a V1.0 runtime trigger.

## XSD exact selection and independent wrappers

| Common | Exact selected Common XSD Git blob | InternationalTextType line | Value xs:string | Language xs:language | Separate wrapper complexType lines | XSD authority |
| --- | --- | ---: | ---: | ---: | --- | --- |
| V1.0 (predecessor) | `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c` | 706 | 708 | 709 | 831 / 807 | official_release |
| V2.0 | `8608e3dcd665c197c34da7f6ec6af5a3758da164` | 717 | 719 | 720 | 842 / 818 | official_release |
| V2.1 | `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e` | 716 | 718 | 719 | 841 / 817 | official_release |
| V2.2 | `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` | 725 | 727 | 728 | 850 / 826 | official_release |
| V2.3 | `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` | 805 | 807 | 808 | 930 / 906 | official_release |
| V2.4 | `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` | 857 | 859 | 860 | 982 / 958 | candidate_integration |

The XSD member XPath hints are `/xs:schema/xs:complexType[@name='InternationalTextType']/xs:sequence/xs:element[@name='Value']` and `.../xs:element[@name='Language']`. Independently defined `IBIS-IP.string` and `IBIS-IP.language` wrappers do not change these child declarations.

**Authority and collision guards:** the official Common V2.4 PDF is published, while selected Common V2.4 XSD `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` remains `candidate_integration` (upstream PR #31 still open at this review, no official release promotion). V2.3 official Common XSD is its exact selected released blob, with exact historical Enumerations V2.2 dependency. The separately frozen **CE-020** finding covers the V2.3 official-XSD versus upstream PR #30 candidate authority collision and is **not** merged into `DRCOM20-001`.

## Historical executable evidence, falsification and version bounds

The strongest disproof was that IBIS-IP wrapper type names might only be semantic aliases for direct primitive members. That is rejected by real schema complexType declarations and existing **EV-118** positive primitive/negative wrapper-shaped XML tests on V2.0. Preserved **EV-119**, **EV-120**, **EV-121** and **EV-122** evidence supports successive exact profiles. This particular source-locator cycle **did not run a new five-version XML instance test matrix**. Source and page evidence, exact selected XSD declarations and prior executable validation are differentiated rather than conflated.

Version boundary: first verified affected official PDF/XSD profile **V2.0**, intermediate official **V2.1–V2.2**, last affected official Common XSD **V2.3**, and last checked affected official Common PDF with selected **candidate/integration** XSD **V2.4**. No independently verified later corrected publication or official V2.4 XSD release. V1.0 PDF predates the table and is not evidence for a repaired value. No unsupported separate German/English release-track inferred from table-caption language.

**Classification:** `confirmed_pdf_defect`, `wrong_type_reference`, `xsd_rejects_pdf_documented_form`, `error_with_advisory` only for pre-existing XSD INVALID, `reviewed_not_implemented` candidate trigger descriptions (not executable matcher).

## Registry and final-gate instructions

Revise the same semantic `DRCOM20-001` and its reviewed runtime mapping scopes, add **one** new source locator (five affected + one predecessor coverage lanes with required `supporting_evidence`), **one** standardized visible-body record and **one** verified scope boundary; sync SDK summary and `CURRENT_STATE.json`. Progress after final full GitHub gates and separate terminal handoff: **92/192**, 92/92 body and boundaries, **100 open**. Next unique finding **DRCOM21-001**. The former V2.0-only analysis remains historically preserved; no XSD/runtime edits.
