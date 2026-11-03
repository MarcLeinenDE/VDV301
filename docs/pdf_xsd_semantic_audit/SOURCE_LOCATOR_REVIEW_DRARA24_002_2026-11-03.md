# DRARA24-002 — AnalogRadioService V2.4 grouped editorial source-locator and boundary review (2026-11-03)

## Identity, pin and authority

- Reused the frozen existing finding `DRARA24-002` (84th semantic-inventory item; zero duplicate findings).
- Official **VDV-Schrift 301-2-19**, `AnalogRadioService` **V2.4**, 01/2023, source id `ARA_V2.4`, official original URL `https://www.vdv.de/301-2-19-sde-v2.4-analogradioservice.pdfx`.
- Original PDF **SHA256 `d0c8d8a3b8719c13b09f43ec98349d2e9b22d07fec0c9267bceff0812cbbc34c`, size 1,009,640 bytes, 16 pages**. GitHub Actions renderer `tools/render_vdv_pdf_pages.py` re-fetched the official URL and independently checked the original's hash and size against `audit_registry/pdf_source_pins_v0.1.json` before 160-dpi render.
- Fresh [GitHub original-byte render run 41622197308](https://github.com/MarcLeinenDE/VDV301/actions/runs/41622197308), exact-source artifact **13223594443**, ZIP SHA256 `4489db1d1573170e3d62b00e2ad97f97b7ce81c01f67413428773e308e43d770`; successful independent handoff run `41622197246` for the render-request commit.
- All three actual rendered images visually inspected, including printed footer page numbers, headings, prose, table and diagrams. PNG fingerprints:
  - Printed **p. 8** `ARA_V2.4_page_0008_160dpi.png`: SHA256 `d8a0b01c6c1f78d99c1f98d7cd69d7ac0bb967eef9379f0afe1e0dd22ef6c7e6`.
  - Printed **p. 10** `ARA_V2.4_page_0010_160dpi.png`: SHA256 `c72f87ce54809ab66d53e59b2d001ae842a785713cc60d09927fdcf88310f075`.
  - Printed **p. 12** `ARA_V2.4_page_0012_160dpi.png`: SHA256 `508a09395c92d0d286663b60ce5cc5b91aa938ba4d9d1d070b62733ea5aff6dd`.
- No original PDF bytes or rendered images are committed to the repository. Renderer artifact provides independent image hashes, source pin, navigation metadata and all target original pages.

## Five visible editorial defects — grouped as **one** finding

| Original printed body | Visible text | Confirmed specific editorial defect and contextual control |
|---|---|---|
| **p. 8 §1 `Initial Situation and Overview`**, first paragraph | `traffic light pre-emtion` | Missing `p` in `pre-emption`. In a later paragraph the same printed page correctly line-wraps `pre-` followed by `emption` and is **not** a second error. |
| **p. 10 §2 `Functional service description` → §2.1 `Operations of the AnalogRadioService`**, introductory sentence immediately above the operation-inventory table | `The AnlogRadioService has only one operation.` | `AnlogRadioService` omits `a`; adjacent printed §2 heading, prior correctly spelled `AnalogRadioService` prose, operation tables and source identifier use the correct service spelling. Prose typo, not a distinct operation or a new service name. |
| **p. 12 §2.3 `DataStructure TransmitterStructure`**, opening prose | `TransmitterStructure is a structure that contians ...` | `contians` instead of `contains`; no structural-definition issue follows. |
| **p. 12 §2.3 `DataStructure TransmitterStructure`**, closing prose | `traffic light pre-amption.` | `pre-amption` instead of `pre-emption`; correct spelling independently appears in p. 10 functional prose. |
| **p. 12 §2.4 `Enumeration BitrateEnumeration`**, introduction immediately above enumeration-value table | `BitrateEnumerationis an enumeration ...` | Missing separating whitespace between correct type name `BitrateEnumeration` and ordinary word `is`. Visible original has continuous text, not merely a PDF text-extraction artifact. The §2.4 heading and table label show the separately spelled correct type `BitrateEnumeration`. |

The headings are **actual original page-body headings and visible table context**, not reconstructed from contents, historical report or extracted searchable text.

## Active falsification and non-inflation

1. **PDF extraction or ordinary line wrap?** Independently compared all exact original 160-dpi PNG pages with extracted text. The five target strings are visibly present. The correct `pre-\nemption` wrap on p. 8 is a false-positive candidate and explicitly excluded.
2. **Real service or XSD identifier typo?** `AnlogRadioService` is introductory English prose; the heading, service introduction and operation table show the correctly named `AnalogRadioService`. The odd `BitrateEnumerationis` is a concatenated *sentence*, not a standalone XML type; `BitrateEnumeration` is separately and correctly identified in the same section's heading and table.
3. **Semantic or executable conflict?** None is demonstrated by these isolated spelling defects. Prior separate `ARA-002`/`ARA-003` concern a genuinely contradictory Transmitter name/cardinality and retain their own IDs/evidence. `ARA-004` and `DRARA24-001` concern the URI example and stay separate. The five English editorial strings stay **one finding**.
4. **Absent visible cover-text error?** The historic PDF extraction's bare `Fehler` on the cover was not visually present, as documented in independent deep-read; it is not included or counted.

## Independently checked publication/version boundary

- The official current [VDV IP-KOM-ÖV publication index](https://www.vdv.de/ip-kom-oev.aspx) and [VDV publication detail 301-2-19](https://www.vdv.de/schriften---mitteilungen.aspx?coriander=v3_2dafd3a4-6936-a003-8ce1-cf1c01aca7fc&id=26a243a0-300f-43d5-98bb-b4adac08d8b6&mode=detail) list the dedicated AnalogRadioService **V2.4**, issued **01/2023**, without a separately listed earlier AnalogRadioService edition or corrected successor. This is **the first and last independently available official dedicated service-document edition** in this verified publication set. It does **not** establish hypothetical V2.3/V2.5 textual content, nor assert that all possible historical unpublished drafts were checked.
- Official publication catalog lists languages D/E; the verified five actual printed defects occur in the **English body** of the byte-pinned 2.4 original. No independent German-language typo or separate version history is inferred without an exact original.
- Historic `IBIS-IP_AnalogRadioService_V2.4.xsd` candidate/integration XSD provenance (`48fb303b80936d2d762f0889ce0c359e04c16e5b`), PR #27, is independent of this editorial issue; do not promote the candidate to an officially tagged 2.4 schema. No XSD or dependency route needed for document-only typo validation.

## Classification and handling

- `confirmed_pdf_defect`, `documentation_spelling`, secondary `editorial_residue` + `grouped_spelling_typos`; `normative_authority=contextual_only`.
- `validation_effect=[documentation_only,no_runtime_effect]`, `sdk_behavior=no_runtime_diagnostic`, `runtime_match=not_applicable`. Retain existing DE/EN diagnostic wording for explanation/reporting; no actual provider result, XML instance FAIL, extension, alias, runtime matcher or schema rewrite.
- Only one source/body/history locator group is credited; move registry counts from **83/192 to 84/192**, with **108 remaining**, only after the full gate and final HEAD verification both pass.
- After full gates, next canonical semantic ID is **`DRCOM10-001`**.

## Evidence and scope control

Canonical existing original fresh-read `docs/pdf_xsd_semantic_audit/deep_read/ARA_V2.4.md` (observations `FR-ARA24-OBS-004` and `005`), `docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_ARA_V24_2026-09-03.md`, byte pin `audit_registry/pdf_source_pins_v0.1.json`, original render run `41622197308` artifact `13223594443` and independent newly inspected printed p8/p10/p12 evidence.
