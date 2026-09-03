# Legacy finding revalidation — Common/Enumerations CE block

Date: 2026-09-03
State: completed under the current Finding Evidence Gate.

## Scope

This block revalidates the frozen legacy identities `CE-001` through `CE-026`. Validation always follows the exact selected XSD authority route; PDF discrepancies never create executable aliases. Candidate/integration schema material remains explicitly labelled and is never promoted to official release authority by this closure.

## Evidence

Current-head aggregate executable evidence: `EV-124`, GitHub Actions run `33735601969`.

EV-124 reruns the existing per-version Common checkers EV-117 through EV-122 plus the V2.3 official/candidate variant checker used for CE-020. Original pinned-PDF Deep Reads remain the source/layout evidence. The executable rerun is additive and does not replace their authority boundaries.

## Terminal states

| Finding | Terminal state |
|---|---|
| `CE-001` | `contextual_not_defect` |
| `CE-002` | `context_verified` |
| `CE-003` | `superseded` |
| `CE-004` | `context_verified` |
| `CE-005` | `executable_confirmed` |
| `CE-006` | `executable_confirmed` |
| `CE-007` | `executable_confirmed` |
| `CE-008` | `executable_confirmed` |
| `CE-009` | `executable_confirmed` |
| `CE-010` | `executable_confirmed` |
| `CE-011` | `executable_confirmed` |
| `CE-012` | `executable_confirmed` |
| `CE-013` | `executable_confirmed` |
| `CE-014` | `executable_confirmed` |
| `CE-015` | `executable_confirmed` |
| `CE-016` | `executable_confirmed` |
| `CE-017` | `executable_confirmed` |
| `CE-018` | `executable_confirmed` |
| `CE-019` | `context_verified` |
| `CE-020` | `executable_confirmed` |
| `CE-021` | `executable_confirmed` |
| `CE-022` | `executable_confirmed` |
| `CE-023` | `context_verified` |
| `CE-024` | `executable_confirmed` |
| `CE-025` | `executable_confirmed` |
| `CE-026` | `executable_confirmed` |

## Important identity and scope decisions

### CE-001

`contextual_not_defect`. Official Common V2.3 explicitly includes `IBIS-IP_Enumerations_V2.2.xsd`; there is no requirement for a synthetic Enumerations V2.3 file. The exact dependency route is the authority.

### CE-002

`context_verified`. V2.4 version history says `StopPointNumber`, while the actual StopInformation table and selected XSD use `PointNumber`. The table/XSD identity wins for XML validation; no XSD rename is inferred.

### CE-003

`superseded`. This ID recorded a historical audit-progress state (V2.4 delta not yet fully closed), not a persistent semantic defect. Common V2.4 Deep Read and EV-122 completed the work it said was pending.

### CE-004 / CE-006

The identities remain distinct: `CE-004` is the stale ServiceNameEnumeration table content (`SystemDocumentationService` / `SystemManagementService`), while `CE-006` is the PDF omission of XSD value `DeviceStateEnumeration.warning`.

### CE-008 / CE-009

The original identities are preserved: `CE-008` is the Funicular/Taxi case-sensitive submode lexeme family; `CE-009` is RailSubmode `specialRail` vs `specialTrain`. The description-level swap in the V2.2 findings delta is corrected by `docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_COMMON_V22_CE008_CE009_IDENTITY_2026-09-03.md` without rewriting history.

### CE-020

`executable_confirmed`. The Common V2.3 official release blob and upstream PR #30 candidate remain two explicit semantic variants with different accepted `InternationalTextType` instance shapes. Official remains default for official authority; the PR30 overlay requires explicit candidate selection.

### CE-023

`context_verified`, documentation-only. The duplicate/corrupt second NetexMode table is confirmed for Common V2.2. Fresh exact visible V2.3 evidence withdrew the earlier V2.3 affected-scope claim; V2.4 is not affected. No XSD defect follows.

### CE-025 / CE-026

Historical mismatches remain confirmed for affected older scopes, while V2.4 is explicitly corrected and is not scope-extended.

## Gate result

All 26 frozen CE identities now have terminal states. `CE-003` is not allowed to survive as a false defect, and the CE-008/CE-009 identity swap is quarantined by an explicit correction overlay. No XSD was modified.
