# Audit Correction Delta — DRTVS21-003 / TicketValidationService V2.1

Date: 2026-09-07  
Branch: `dev/schema-integration`  
Finding: `DRTVS21-003`  
Evidence: `EV-150`, successful run `34087850644`, job `101635233786`

## Purpose

This correction preserves the historical Deep Read while removing one unsupported XSD-support sentence discovered during mandatory legacy-finding revalidation under the current Evidence Gate.

The underlying PDF editorial finding survives. Only one supporting sentence is corrected.

## Historical imprecise supporting sentence

The V2.1 Deep Read states, in support of the `SubscribeCurrentStop` versus `SubscribeCurrentStopPoint` inconsistency:

`The exact XSD operation group also uses SubscribeCurrentStopPoint.`

That sentence is not supported by the exact selected V2.1 TicketValidationService XSD and is superseded by this correction. The historical Deep Read is intentionally not silently rewritten.

## Exact V2.1 XSD authority

Selected official mixed-version route:

- `IBIS-IP_TicketValidationService_V2.1.xsd` — blob `f6497e6469b82ee19b185c4de749d13a7ca60bed`
- `IBIS-IP_common_V1.0.xsd` — blob `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`
- `IBIS-IP_Enumerations_V1.0.xsd` — blob `a9bea5bc73003ed91ded8519db06c32c4067831d`

The service XSD includes exactly Common V1.0 and Enumerations V1.0.

Its `TicketValidationServiceOperations` group and global element inventory contain these local service entries:

- `TicketValidationService.GetCurrentStopPointResponse`
- `TicketValidationService.GetRazziaResponse`
- `TicketValidationService.GetCurrentLineResponse`
- `TicketValidationService.GetVehicleDataResponse`
- `TicketValidationService.RetrieveTripDataRequest`
- `TicketValidationService.RetrieveTripDataResponse`

Neither `TicketValidationService.SubscribeCurrentStopPoint` nor `TicketValidationService.SubscribeCurrentStop` appears as a local group member or global element in that exact V2.1 service XSD.

Therefore the exact XSD cannot be used as positive support for either Subscribe spelling in this finding.

## Corrected finding basis

`DRTVS21-003` remains valid on same-document PDF evidence:

- physical page 5 table of contents: formal section `3.2 SubscribeCurrentStopPoint`
- physical page 10 German formal operation overview: `SubscribeCurrentStopPoint`
- physical page 11 German flow text: `SubscribeCurrentStop`
- physical page 12 English formal operation overview: `SubscribeCurrentStopPoint`
- physical page 13 English flow text: `SubscribeCurrentStop`
- physical page 14 formal detailed operation section: `SubscribeCurrentStopPoint`

Fresh 180-DPI renders from the exact byte-pinned PDF were manually inspected after EV-150 passed.

The strongest alternative hypothesis — that `SubscribeCurrentStop` is a second or legacy formal operation name — is rejected by the same publication's repeated formal overview/detail naming. No XSD alias or formal service operation is invented.

## Result

`DRTVS21-003` remains `context_verified` with classification `pdf_operation_name_editorial_error_candidate`.

The finding's basis is refined to:

`same-document formal operation overview/detail versus bilingual flow text`

and no longer includes the incorrect historical XSD-support sentence.

## Audit invariants

- frozen 192-finding inventory: unchanged
- XSD files: unchanged
- exact V2.1 mixed-version authority retained
- no latest-wins substitution
- no Subscribe alias invented
- correction trail preserved explicitly
