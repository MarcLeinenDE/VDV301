# Finding Revalidation — DRTVS21 / TicketValidationService V2.1

Date: 2026-09-07  
Scope: `DRTVS21-001`, `DRTVS21-002`, `DRTVS21-003`, `DRTVS21-004`  
Evidence: `EV-150`, successful run `34087850644`, job `101635233786`  
Evidence commit: `9e99931b27645f4a45850b6c7a45486f04369825`  
Closure run: `34088402374`

## Authority route

Official byte-pinned VDV 301-2-16 TicketValidationService V2.1 PDF (`676c05d7615f2f2ce95ec4eb085428cb0c970a4226809566e8968200df69988d`, 752652 bytes) plus the exact official mixed-version XSD route `TicketValidationService V2.1 -> Common V1.0 -> Enumerations V1.0`. No latest-wins substitution is permitted.

EV-150 reran EV-112 and the complete 50-root-XSD repository regression pool. No XSD changed. Fresh 180-DPI renders of physical pages 5, 10, 11, 12, 13, 14 and 15 were manually inspected.

## DRTVS21-001 — executable_confirmed

Physical page 14 visibly prints `IBIS-IP.NMToken` for `CurrentTripRef`. The exact V2.1 XSD declares `IBIS-IP.NMTOKEN`; Common V1.0 contains the exact uppercase type and no `IBIS-IP.NMToken` alias. EV-112 rerun confirms the negative compile boundary for the PDF spelling.

## DRTVS21-002 — context_verified

Physical page 15 visibly concatenates the GetCurrentLine response display as `TicketValidationServiceCurrentLineData`, while the adjacent structure display preserves a separator and the exact XSD type is `TicketValidationService.CurrentLineDataStructure`. The common PDF convention of omitting `Structure` is retained as context and is not itself classified as the defect; the material anomaly is the missing service-name separator.

## DRTVS21-003 — context_verified with audit correction

Formal PDF material uses `SubscribeCurrentStopPoint` (pages 5, 10, 12 and 14), while German and English flow text use `SubscribeCurrentStop` (pages 11 and 13). The finding survives as a PDF editorial operation-name inconsistency.

One historical Deep Read support sentence is superseded: the exact V2.1 service XSD operation group does **not** contain `SubscribeCurrentStopPoint`; in fact its local operation/global inventory contains neither Subscribe spelling. Therefore XSD positive support is removed from this finding. The dedicated correction trail is `docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_DRTVS21_003_V21_XSD_SUPPORT_2026-09-07.md`.

## DRTVS21-004 — context_verified

Visible documentation residue is confirmed: page 10 contains `Unscubscribe` and `Unscubscibe` in operation-description prose; page 15 contains `GetrazziaResponsetData` and `Error Respone`. These are non-executable editorial strings and create no XML aliases or validation rules.

## Closure

EV-150 PASS; EV-112 rerun PASS; all 50 root XSDs PASS; exact TVS V2.1 authority retained; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **126/192 terminal, 66 pending**. The first remaining pending finding is `HDS-001`; next block is `HDS` (`HDS_V21_V22_V22A_HDS001`).
