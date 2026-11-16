# DRDOOR21-001 — pinned original source locator and cross-version boundary — 2026-11-16

**Finding identity:** Existing frozen `DRDOOR21-001`, one documentation-only operation-reference defect in the **official VDV-Schrift 301-2-15, DoorStateService V2.1, 07/2018**. This pass adds a previously omitted fourth incorrect table-description cell in **Table 11** to the same ID. The correct executable operation family continues to be `RetrieveSpecificDoorOpenState` and `RetrieveSpecificDoorOperationState`. No new finding, XSD alias, schema modification, runtime matcher, or XML-result override.

## Actual visible byte-pinned original PDF body

Original official source: `DOOR_V2.1`, https://www.vdv.de/301-2-15-sd-v2-1-doorstateservice.pdfx, **SHA-256 `7413c99f2910f125947213561658ae9c808952d5b57700d155b939c899de26e8`**, **851513 bytes**, **16 PDF pages**. Fresh deterministic renderer [GitHub Actions run 43888781452](https://github.com/MarcLeinenDE/VDV301/actions/runs/43888781452), artifact `14234584210`, source hash and byte-size matched the canonical `pdf_source_pins_v0.1.json`; each original PNG independently inspected and SHA256 rechecked against `render_manifest.json`:

| Printed page | Actually visible body | Exact mismatched prose or reference | PNG SHA256 |
| --- | --- | --- | --- |
| **1** | Official cover `VDV-Schrift 301-2-15 / DoorStateService V2.1 / 07/2018` | Establishes exact publication identity | `bc059e744a0d8fbab47e94b2c20595bc66f1099f5bfeed4e308542563267f8a3` |
| **9** | §2 `Operations of the DoorStateService`, **Table 1** | Both correct `RetrieveSpecificDoorOpenState` and `RetrieveSpecificDoorOperationState` listed separately as normative operation names in surrounding official documentation | `0aa5447c81474719a89816d6128f0e371e708f58d4c0be82fef327a3df58c9f6` |
| **11** | §2.7 `Data Structures of Operation RetrieveSpecificDoorOpenState`, §2.7.1 **Request**, **Table 8** `Description of DoorStateService.RetrieveSpecificDoorOpenStateRequest` | Request-description cell incorrectly says **`RetrieveDoorOpenState`**, omitting `Specific` | `6655c4c27c55acf2dfd35f8a3f2ceb8aafb1f764a4e1e96a30f17a39f669fdb6` |
| **12** | §2.7.2 **Response**, **Table 9** `Description of DoorStateService.RetrieveSpecificDoorOpenStateResponse` | Response-description cell also incorrectly says **`RetrieveDoorOpenState`** | `4e9ab26220257e6d191fc3aa104b67b1cd2c5c3b062622955118ed2c1416f14b` |
| **12** | §2.8 `Data Structures of Operation RetrieveSpecificDoorOperationState`, §2.8.1 **Request**, **Table 10** `Description of DoorStateService.RetrieveSpecificDoorOperationStateRequest` | Request-description cell incorrectly says **`RetrieveDoorOpereationState`**, omitting `Specific` and misspelling `Operation` | same page-12 PNG above |
| **12** | §2.8.2 **Response**, **Table 11** `Description of DoorStateService.RetrieveSpecificDoorOperationStateResponse` | **Newly recovered omitted cell:** response-description cell incorrectly says **`RetrieveDoorOperationState`** (omits `Specific`, no `Opereation` spelling mistake in this row) | same page-12 PNG above |

**Locator correction:** Older frozen classification and EV-143 chiefly noted `RetrieveDoorOpenState` and `RetrieveDoorOpereationState`; Table 11's third distinct wrong form `RetrieveDoorOperationState` was overlooked. Historical original reports are preserved. One unique finding is expanded to cover all four directly observed cells and three distinct wrong tokens. Table 8 is **printed p11**, NOT p12; Tables 9, 10 and 11 are printed p12. Do not infer table positions from a TOC or from sequential numbering.

Historical independent [EV-143 run 33976777554](https://github.com/MarcLeinenDE/VDV301/actions/runs/33976777554), artifact `9972544125` was also independently reopened, `manifest.sha256` file hashes recomputed (all pass), and its p11/p12 original pages visually checked. The new run provides the cover and operations overview plus refreshed full-body proof. The historical EV-143 finding remains a valid but **incomplete subset** of the four-cell observation.

## Exact selected executable XSD authority

| Official upstream `VDVde/VDV301@VDV-301-2.1` | Exact Git blob | Verified content |
| --- | --- | --- |
| `IBIS-IP_DoorStateService_V2.1.xsd` | `abff0f3960e2ec7a9caaa9ddeb6efff8f4183805` | `DoorStateServiceGroup` at line 10 and member declarations around lines 24–27 use `DoorStateService.RetrieveSpecificDoorOpenStateRequest/Response` and `DoorStateService.RetrieveSpecificDoorOperationStateRequest/Response`; response/request complexTypes around lines 52–82, **no** `RetrieveDoorOpenState`, `RetrieveDoorOpereationState`, or `RetrieveDoorOperationState` operation aliases |
| `IBIS-IP_common_V1.0.xsd` | `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c` | Actual direct `xs:include` from DoorState V2.1 |
| `IBIS-IP_Enumerations_V1.0.xsd` | `a9bea5bc73003ed91ded8519db06c32c4067831d` | Actual direct `xs:include` from DoorState V2.1 |

All three exact selected working-branch file blobs were re-fetched and independently matched the named official upstream release tag. The **mixed-version Common V1.0 / Enumerations V1.0 dependencies are intentional and normative for this selected profile**; neither Common V2.1 nor an imagined newest schema may be substituted.

## Independently checked publication/version boundary

- **First/last verified affected standalone published DoorStateService document:** VDV 301-2-15 **V2.1**, official single publication in the canonical PDF source registry and on the VDV official current IP-KOM-ÖV publication index (checked 2026-11-16): https://www.vdv.de/ip-kom-oev.aspx. The original p1 identity and p9/11/12 body are all directly visible. A copied V2.2 or V2.4 DoorStateService PDF is **not** in the canonical registered publication inventory, and the VDV publication listing exposes V2.1 as the published 301-2-15 edition. Do not claim another official DoorStateService release or a later correction without an independently pinned source.
- **Earlier context:** V1.0 DE/EN and integrated V2.0/V2.1 Basic Services have their own separately pinned source editions, but none is an earlier dedicated 301-2-15 DoorStateService publication with these exact §2.7/2.8 tables. This document-local typo must not be retroactively attributed to their distinct service descriptions. Their version numbers do not establish a nonaffected preceding edition of **this same** DoorStateService document.
- **No verified affected successor** and **no verified corrected standalone successor**. The scope is exactly official DoorStateService V2.1, not a broad version range. If the upstream list changes, rerun the publication identity and byte-pin boundary independently.
- **Cross-finding boundaries:** The adjacent table 9 and 11 `OperationErrorMessage` choice-member discrepancy is already separately tracked as `DRS-002` and involves XML element naming; `DoorOpenState` semantics in table 9 are separately `DRDOOR21-002`. **Do not merge those into this operation-reference prose finding.** The `-1:1` choice marker is intentional VDV notation, not negative cardinality. `DRS-004` covers XSD annotation spelling residues, not this PDF-only reference defect.

## Active disproof, XML evidence, SDK and diagnostics

1. **Could the shortened tokens be intentional aliases?** No. The identical official PDF's p9 Table 1, p11 §2.7, p12 §2.8, all four table captions and the exact official release-tag DoorStateServiceGroup use the `RetrieveSpecific…` family. The three shortened/typoed cells are descriptive prose rather than separately declared XML elements.
2. **Could `Opereation` be the only problem?** No. All four cells omit `Specific`; Table 11 independently proves a shortened spelling with correctly written `Operation`. The original editor spelling error is supplemental only.
3. **Could schema include or version routing explain the difference?** No. The exact official V2.1 service XSD, with its deliberate V1.0 dependencies, contains no shortened operation identifiers. The selected-XSD outcome remains normative; the PDF is not an executable extension.
4. **Do we need a new positive/negative XML-instance test?** No for this documentation-only description defect. Historical EV-143 PASS and EV-111 specific XSD context remain evidence of declaration names, not full XML validation tests for the wrong PDF prose; **no new instance test is claimed**.
5. **SDK disposition:** Existing `info / informational / reviewed_not_implemented` mapping is expanded in *descriptive triggers only* for the newly observed `RetrieveDoorOperationState`; no productive matcher, operation discovery alias, repair, normalization, or XML PASS/FAIL change. Complete German and English `title`, `short`, `long`, `recommendation` remain canonical and now describe all three distinct wrong tokens and four cells.

## Terminal workflow

Keep existing finding identity `DRDOOR21-001`; update semantic source references and bilingual diagnostics, source locator with p1/p9/p11/p12 and exact printed table/caption context, all three official tag-pinned XSD dependencies, verified visual-body and independent scope registers, reviewed-only runtime metadata and consistent `CURRENT_STATE.json`/SDK manifest. New unique locator count **102/192**, body **102/102**, independent version boundaries **102/102**, remaining **90**. Next frozen-semantic unique ID **`DRDOOR21-002`**, not started. Complete full schema-audit-validation and handoff-integrity on substantive HEAD; separate `terminal_clean` commit and verify *both* workflows on final HEAD. Only after successful closure, publish stable facts to private `ai-mem` via reviewed PR (no raw PDFs, snapshots or XSD copied).
