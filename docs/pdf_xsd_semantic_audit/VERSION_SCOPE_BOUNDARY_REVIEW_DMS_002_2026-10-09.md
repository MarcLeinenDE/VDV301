# DMS-002 — historical PDF cross-reference residue, verified boundary (2026-10-09)

**VERIFIED: affected VDV 301-2 Base Services V2.0 only; first unaffected/corrected successor V2.1.** Editorial PDF-only defect; no XML/XSD/provider runtime validation effect.

## Finding identity, visible evidence and context

The official bilingual **VDV 301-2 V2.0** (source `VDV301-2_BASE_V2.0`, SHA-256 `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`) visibly prints unresolved Word cross-reference residue `Fehler! Verweisquelle konnte nicht gefunden werden.` in **printed page 76**, **§5.3.2.1 Start weiterer Dienste / Start of further Services**, where a DMS StartService operation is described. This is already visually checked in byte-pinned render run `33758274931` / artifact `9894357560`, page PNG pin in `audit_registry/dms_visual_revalidation_evidence_2026-09-03.json`; source-locator body verification also documented in `SOURCE_LOCATOR_REVIEW_DMS_002_2026-10-06.md`. Other occurrences were independently confirmed in the V2.0 original PDF text on printed pp59, 69, 77, 92, 94, 97–100, so this is not a PDF-rendering artifact. The English parts of the bilingual V2.0 also carry the same embedded German Word error literal.

The official bilingual **VDV 301-2 V2.1** (source `VDV301-2_BASE_V2.1`, SHA-256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`) has its corresponding **§5.3.2.1** on printed page **77**, with a resolved chapter `7.1.23` reference. The visible body was independently reviewed in the historical source-locator record `SOURCE_LOCATOR_REVIEW_DMS_002_2026-10-06.md`. A full-document text search finds no remaining occurrence of that exact unresolved-Word error marker. The V2.1 rendering fallback was successfully established separately in `pdf-render-fallback.yml` run `37894085576` against the exact same V2.1 source hash; that particular run rendered printed pp88–102 for DMS-001, **not p77**, so it is not misrepresented as new p77 visual evidence.

## Independent predecessor/successor scope check

| Publication | Language-specific check | Conclusion |
| --- | --- | --- |
| VDV 301-2 V1.0 German (`VDV301-2_V1.0_DE`; pinned SHA `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`) | Whole-document original PDF text search for exact `Fehler! Verweisquelle`: no occurrence | Last available earlier German predecessor unaffected by this **specific marker**. This negative text check does not prove every historical reference correct. |
| VDV 301-2 V1.0 English (`VDV301-2_V1.0_EN`) | Independent English publication; search for English Word error markers `Error! Reference` / `Error! Bookmark`: no occurrence | No corresponding English marker established in this predecessor; do not infer language parity solely from German version. |
| VDV 301-2 V2.0 German/English in the same publication (`VDV301-2_BASE_V2.0`) | Visible page 76 and recurring errors in both language sections | First and last affected publication. |
| VDV 301-2 V2.1 German/English in the same publication (`VDV301-2_BASE_V2.1`) | §5.3.2.1 p77 prints the resolved §7.1.23 reference, previously visibly reviewed; whole-document exact-marker search negative | First corrected successor. |
| Separate DMS V2.2 (`DMS_V2.2`, SHA `72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e`) | Whole-document exact-marker search negative | No later persistence in this separately published official DMS document. |
| Separate DMS V2.4 (`DMS_V2.4`, SHA `347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd`) | Whole-document exact-marker search negative | No later persistence; independent publication/document scope, not a new XML constraint. |

No separate V2.3 DMS public PDF is in the canonical pinned source registry; the corresponding repository service XSD is integration comparison material and cannot prove anything about editorial PDF marker occurrence.

## Active disproof / scope and provider handling

Checked that the text is not an actual normative XML element, an intentional chapter reference or an extraction artifact: the original visually inspected printed page literally contains an unresolved Word field. The V2.1 corresponding chapter reference is resolved. This is a **documentation/editorial defect**, not a reason to mark a V2.0 implementation as nonconformant, change any XSD, create aliases, or introduce a runtime matcher.

Retain original finding ID `DMS-002`; retain existing semantic registry with V2.0 affected and V2.1 corrected-reference context. `defect_assessment=confirmed_pdf_defect`, `normative_authority=contextual_only`, `sdk_behavior=info`, `runtime_match=not_applicable`.

The full validation suite and terminal GitHub handoff gate must succeed before this evidence represents a closed canonical cycle. Next `DMS-003`.
