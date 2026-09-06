# Finding Revalidation — DRS / DoorStateService V2.1

Date: 2026-09-06  
Scope: `DRS-001`, `DRS-002`, `DRS-003`, `DRS-004`  
Evidence: `EV-145`, successful evidence run `34026409256`, job `101468048441`  
Evidence commit: `9405a83c235d47cebcde6d0cb8f59e69485f5f93`  
Closure run: `34026674927`

## Authority route

Official byte-pinned VDV 301-2.1 DoorStateService PDF (`7413c99f2910f125947213561658ae9c808952d5b57700d155b939c899de26e8`, 851513 bytes) plus the exact official VDV-301-2.1 mixed-version schema family: `IBIS-IP_DoorStateService_V2.1.xsd` blob `abff0f3960e2ec7a9caaa9ddeb6efff8f4183805`, `IBIS-IP_common_V1.0.xsd` blob `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`, and `IBIS-IP_Enumerations_V1.0.xsd` blob `a9bea5bc73003ed91ded8519db06c32c4067831d`. The mixed-version dependency is authoritative; latest-XSD-wins is forbidden.

EV-145 freshly rendered PDF pages 9–12 at 180 DPI, retained both layout and raw text extraction for source-token checks, reran EV-111 for the executable DRS-002/DRS-003 boundary, and reran the complete 50-XSD pool.

## DRS-001 — context_verified

The page-9 operation overview repeats `SubscribeDoorOpenStates` / `UnsubscribeDoorOpenStates` after `GetDoorOperationStates`. The exact DoorStateService V2.1 XSD declares distinct OperationStates subscription operations. The shared/generic-name counter-hypothesis is therefore rejected. This is documentation-only and does not require executable XML evidence.

## DRS-002 — executable_confirmed

Page 12 names `OperationErrorMessage` in the RetrieveSpecific response context. The exact RetrieveSpecific response choices use `ErrorMessage`; `OperationErrorMessage` is rejected. EV-111 was rerun under EV-145 and passed the positive/negative boundary again.

## DRS-003 — executable_confirmed

`GetDoorOpenStatesRequest` and `GetDoorOperationStatesRequest` remain exact untyped local XSD declarations. EV-111 rerun reconfirms the resulting XML Schema `xs:anyType` default behaviour, including acceptance of arbitrary nested content. The counter-hypothesis that an omitted request structure implies an empty request is rejected.

## DRS-004 — context_verified

The known `GetDoorOpeationStates` / `RetrieveSpecificDoorOperationnState` misspellings are confined to `xs:documentation`. Executable `@name` / `@type` identifiers remain correctly spelled, so executable impact is disproved.

## Choice-notation guard

The page-12 `a/b -1:1` notation is treated as VDV XML-choice notation, not as a negative cardinality. No new cardinality finding is promoted.

## Closure

EV-145 PASS; closure rerun PASS; EV-111 rerun PASS; all 50 XSDs PASS; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **110/192 terminal, 82 pending**. The first remaining pending frozen finding is `DRSMS22-001`; next block is `DRSMS22` (`SMS_V2.2_DRSMS22`).
