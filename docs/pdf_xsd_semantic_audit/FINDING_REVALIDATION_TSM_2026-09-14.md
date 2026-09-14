# Finding revalidation — TrainSetManagementService (TSM)

Status: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen findings: `TSM-001` through `TSM-003`. Frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Aggregate evidence: **EV-162**; successful closure run **34823587675**.
- Successful EV-162 validation run: **34823353897**, job **103909732702**, artifact **10339282538**, digest `sha256:8083d5badea1af9922302b202f06c33f4961d53878dfbc5d84324a4e4d65a4a0`.
- Exact TrainSet V2.1/V2.2 PDFs reused from the EV-160 source lane and re-acquired during validation.
- V2.1 physical page 30 and exact V2.1 XSD show `TrainSetManagementService.GetTrainSetComposition`; EV-109 executable-confirms that the later corrected `...Response` root is not valid in V2.1.
- V2.2 physical page 51 explicitly records the correction to `TrainSetManagementService.GetTrainSetCompositionResponse`. The exact V2.2 global root is corrected, but the `TrainSetManagementServiceOperations` group still contains the stale old name; EV-104 executable-confirms this mismatch.
- V2.2 physical page 31 uses the corrected global name but its embedded XSD diagram visibly expands the old flat coach fields. The exact V2.2 reused response structure instead has repeatable `SingleCoach -> SingleCoachInATrainSet`; this is documentation-only and does not change XSD authority.
- Complete **50-root-XSD pool** passed again; no schema mutation.

## Terminal states

| Finding | Terminal state | Result |
|---|---|---|
| `TSM-001` | `executable_confirmed` | Historical V2.1 response-root naming discrepancy confirmed by exact XSD behaviour and V2.2 correction history. |
| `TSM-002` | `executable_confirmed` | V2.2 corrected global root conflicts with stale operation-group member; EV-104 confirms validation behaviour. |
| `TSM-003` | `context_verified` | V2.2 page-31 embedded diagram remains stale relative to the exact repeated `SingleCoach` structure. |

## Mutation decision

- XSD mutation: **none**.
- Frozen inventory mutation: **none**.
- PDF source registry/pin mutation: **none**.
- Registry/status mutation: only `TSM-001`…`TSM-003` and the TSM block/counter handoff.

## State transition

- Before: **162/192 terminal**, **30 pending**, first pending `TSM-001`.
- After: **165/192 terminal**, **27 pending**, first pending `TVS-001`.
- Next block: **TVS**.
