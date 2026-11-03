# DRARA24-001 — AnalogRadioService V2.4 URI example lacks `http://` (2026-11-03)

## Finding identity, source and historical scope

Existing frozen finding **DRARA24-001**; no new finding ID. The official VDV-Schrift **301-2-19, AnalogRadioService V2.4 (01/2023)** is the sole separately listed AnalogRadioService service-document version in the checked official VDV [publication catalogue](https://www.vdv.de/ip-kom-oev.aspx) on 2026-11-03. No official predecessor AnalogRadioService service-document publication is independently established, and no corrected successor is independently established. This is not evidence of a V2.3 or V2.5 dedicated AnalogRadioService document.

Exact original: `ARA_V2.4`, official URL `https://www.vdv.de/301-2-19-sde-v2.4-analogradioservice.pdfx`, expected/observed SHA-256 `d0c8d8a3b8719c13b09f43ec98349d2e9b22d07fec0c9267bceff0812cbbc34c`, size **1,009,640 bytes**. The GitHub Actions [exact-pin render run 41620405346](https://github.com/MarcLeinenDE/VDV301/actions/runs/41620405346), artifact **13223143148**, independently downloaded the official PDF and verified both SHA-256 and byte size against `audit_registry/pdf_source_pins_v0.1.json` before rendering three original pages at 160 dpi (PyMuPDF). No PDF bytes or rendered original pages are committed to the public repository.

## Visible original body — direct comparison

- **Printed page 13; actual visible heading `2.5 Examples / 2.5.1 URI for the Operation SendTelegram`**. The adjacent underlined URI pattern is exactly `http://Host:Port/ServiceName/Operation`. The underlined concrete example is `192.168.1.2:8080/AnalogRadioService/SendFFSKTelegram`. **The concrete example omits the `http://` prefix shown in the immediately preceding template.** Original PNG `ARA_V2.4_page_0013_160dpi.png` SHA-256 `23c581ef866494a56b9777c444f41405874a8349e972147e7ae4aeb66a1a72e8`; inspected actual rendered body and printed page footer.
- **Printed page 10; `2.1 Operations of the AnalogRadioService`**. The operation tables identify `SendTelegram` as the only operation, and the service uses HTTP for XML control. This contextual cross-check separates the URI-scheme problem from the independent operation-name defect **ARA-004**. Original PNG SHA-256 `c72f87ce54809ab66d53e59b2d001ae842a785713cc60d09927fdcf88310f075`.
- **Printed page 13; `2.5 Examples / 2.5.2 XML of a complete telegram`**. The XML root `AnalogRadioService.SendTelegram` is distinct from the scheme-less URI illustration. No XSD inference follows from the missing URI prefix.
- **Printed page 14; `Regelwerke – Normen und Empfehlungen / References`**. The reference section cites General Conventions V2.3, but does not establish any separately issued AnalogRadio V2.3 predecessor. PNG SHA-256 `789b3d997149244c1a35a5225b576333c81ffcfa1e6a724de51bcc2a65fbe776`.

PNG fingerprints, source identities, retrieval method, page count (16), and source checks are contained in the pinned `render_manifest.json` in the GitHub artifact. Original page 13 was visually checked both through the live PDF viewer and the byte-pinned independent GitHub render. Canonical locator is the **actual visible page 13 body section 2.5.1**, not a table-of-contents extrapolation or generic prose.

## Active disproof and attribution

- **Hypothesis: the second form intentionally shows a shortened or relative address.** Rejected as an explanation of the documented URI example: the publication explicitly calls it a service URI, provides a full `http://` URI template directly above, and does not label the shortened form as abbreviated or relative. Record a *documentation/example inconsistency*, not a protocol-specific provider noncompliance claim.
- **Hypothesis: this is merely a SendFFSKTelegram typo.** This is a separate defect: the operation inventory and XML example say `SendTelegram`; that mismatched suffix belongs to **ARA-004**. DRARA24-001 covers **only the omitted URI scheme**. No duplicate identity or extra progress credit.
- **Hypothesis: candidate AnalogRadio V2.4 XSD decides the URI form.** Wrong authority layer. No XML payload acceptance/cardinality/enum claim is made here. The `IBIS-IP_AnalogRadioService_V2.4.xsd` candidate/integration schema (historical blob `48fb303b80936d2d762f0889ce0c359e04c16e5b`) is separately provenance-classified, and official PR #27 remained open/unmerged in the repository check. No 2.4 tagged official schema authority was claimed.

## Classification, SDK and provider consequence

- `confirmed_pdf_defect`; `stale_diagram_or_example`; `uri_example_missing_scheme`; `template_example_inconsistency`; original PDF document-only.
- `normative_authority=contextual_only`; `validation_effect=documentation_only/no_runtime_effect`; `sdk_behavior=info`; runtime match `not_applicable`. Keep existing DE/EN diagnostics. No XSD mutation, no executable matcher, no synthetic negative XML sample or provider FAIL.
- A provider's *actual* HTTP endpoint may be evaluated under the explicitly selected VDV/HTTP profile independently, but the documentation example's omission is **not itself** a basis to reject an XML instance or invent new URL validation rules.
- Existing finding `DRARA24-001` receives **one** complete source locator, body verification and independently checked publication boundary. Progress **82 → 83 / 192** (109 remaining) only after all synchronized canonical registries and complete substantive/final-HEAD gates pass.
- Next canonical finding in semantic order: `DRARA24-002`.

## Evidence and no-remediation boundary

Original source pin `audit_registry/pdf_source_registry_v0.1.json` + `audit_registry/pdf_source_pins_v0.1.json` (first original pin run33269415752), fresh pinned visual GitHub render **run41620405346 artifact13223143148**, existing independent deep-read `docs/pdf_xsd_semantic_audit/deep_read/ARA_V2.4.md` and finding revalidation `docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_ARA_V24_2026-09-03.md`. XSD source remains unchanged. No upstream PR or released schema modified.
