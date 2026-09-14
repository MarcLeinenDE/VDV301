# Finding revalidation — TicketingService (TKT)

Status: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen findings: `TKT-001` through `TKT-009`. Frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Evidence: **EV-158**; successful closure run **34813841015**.
- Independently successful EV-158 run: **34813527845**, job **103879396942**, artifact **10336185560**, digest `sha256:ba5ee246787f58d4cf690421fda683fb1dd072106d5c4e7eb6376c218b717870`.
- Source/render pin run: **34771722424**, job **103762406542**, artifact **10322336797**, digest `sha256:df661f9444ab7e26b563b0c748fee583314b19d789b316c6405e45e1fe99589c`.
- Official VDV 301-2-9 TicketingService V1.0 PDF: SHA-256 `96241226c7a25b0384527dd3de5fcd9448c8e75f38bfb4ffd7b607680bfc6b43`, 627099 bytes, 16 pages.
- Targeted physical pages 7-12 were rendered from the exact pinned PDF. Page 11 is visual-only evidence for the visible `CardApplicationInformation` label because Poppler interleaves that table's columns; the executable XSD spelling boundary is tested independently.
- Official upstream release contexts: VDV-301-1.0 commit `f5b53785f703e898632603eec3bfa3555a79fdba` carries TicketInformationService V1.0 blob `017ca64666e25d757fc0cde1f1be817f06a743fc`; VDV-301-2.0 commit `f2569a91f0a7c737a0ca7c0280b28ad223d7ee08` carries blob `3fda66d872ab0d1c511247f13e715cf3ad56afe7`.
- The complete 50-file root XSD pool was recompiled and byte-hashed before/after EV-158; no XSD changed.

## Terminal states

| Finding | Terminal state | Revalidation result |
|---|---|---|
| `TKT-001` | `context_verified` | The same TicketInformationService V1.0 path has distinct official blobs and executable surfaces in the VDV-301-1.0 and VDV-301-2.0 release contexts; resolution therefore requires release context/schema revision rather than the filename version alone. |
| `TKT-002` | `contextual_not_defect` | TicketInformationService is a filename token; executable schema identities are TicketingService.*. No TicketInformationService.* executable alias is declared. |
| `TKT-003` | `context_verified` | The PDF assigns SubscribeResponseStructure to UnsubscribeValidationResult, while Common V1.0 defines UnsubscribeResponseStructure. Both response structures have the same Active/OperationErrorMessage XML choice, so this is a documentation type-name discrepancy without XML-shape delta. |
| `TKT-004` | `executable_confirmed` | The exact TicketingService.ValidateTicketRequest root validates, while the PDF heading TicketInformationService.Validation.GetDataRequest is not an executable root and is rejected. |
| `TKT-005` | `context_verified` | The PDF overview names TicketingService.ValidationResultStructure, which is absent from the XSD; the executable GetValidationResult root maps to TicketingService.GetValidationResultResponseStructure. |
| `TKT-006` | `executable_confirmed` | The XSD sequence is DefaultLanguage before TimeStamp. Executable validation accepts progression in XSD order and rejects the PDF order at the first misplaced field. |
| `TKT-007` | `context_verified` | The PDF detailed table labels the outer GetValidationResultResponseStructure while the displayed TimeStamp/ValidationResult fields belong to TicketingService.ValidationResultDataStructure. |
| `TKT-008` | `executable_confirmed` | CardApplikationInformation is the schema-declared spelling and validates; the PDF spelling CardApplicationInformation is rejected by the exact XSD. PDF page 11 is preserved as rendered visual evidence because text extraction interleaves the table columns. |
| `TKT-009` | `context_verified` | The official PDF visibly uses TicketingSevice in labels, while the XSD exposes no such alias; executable service identity remains TicketingService. |

## Mutation decision

- XSD mutation: **none**.
- Frozen inventory mutation: **none**.
- Registry/status mutation: only the nine frozen TKT findings and block/counter handoff.

## State transition

- Before: **146/192 terminal**, **46 pending**, first pending `TKT-001`.
- After: **155/192 terminal**, **37 pending**, first pending `TS-001`.
- Next block: **TS**.
