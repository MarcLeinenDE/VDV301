# Finding Revalidation — DOOR V2.1

Date: 2026-09-05  
Scope: `DRDOOR21-001`, `DRDOOR21-002`  
Evidence: `EV-143`, successful evidence run `33976777554`  
Closure run: `34025259521`

## Authority
Official public DOOR V2.1 PDF: `7413c99f2910f125947213561658ae9c808952d5b57700d155b939c899de26e8`. Exact release route: `VDV-301-2.1`, DoorStateServiceGroup blob `abff0f3960e2ec7a9caaa9ddeb6efff8f4183805`, Common V1.0 `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`, Enumerations V1.0 `a9bea5bc73003ed91ded8519db06c32c4067831d`. No latest-XSD substitution.

## DRDOOR21-001 — context_verified
Pages 11–12 visibly contain shortened/incorrect operation names around `RetrieveSpecificDoorOpenState` and `RetrieveSpecificDoorOperationState`. The exact official XSD contains the `RetrieveSpecific...` structures and no shortened/typo aliases. The alternate-name hypothesis is rejected. Documentation-only defect; no validation alias or XSD change.

## DRDOOR21-002 — context_verified
The `DoorOpenState` row is described as an operation state. Exact XSD structures separate `OpenState` from `OperationState`, rejecting deliberate-shared-semantics as an explanation. Documentation copy/paste defect only.

## Closure
EV-143 PASS; closure rerun PASS; full XSD pool PASS; frozen inventory unchanged; no XSD mutation. Revalidation count is now 103/192 terminal, 89 pending. Next block: Network (`DRNET20-001..003`).
