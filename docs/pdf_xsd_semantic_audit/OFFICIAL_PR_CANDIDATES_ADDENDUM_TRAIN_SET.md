# TrainSet services post-audit official-facing candidates

Tracking only. No upstream action without explicit user approval.

## TS-CAND-001 - TSM V2.2 stale operation-group name

Linked finding: `TSM-002`.

V2.2 version history explicitly says the root was corrected from `TrainSetManagementService.GetTrainSetComposition` to `...GetTrainSetCompositionResponse`; the global declaration is corrected but the operation group retains the old name.

Post-audit gate:

```text
- compile exact V2.2 pool,
- compare global roots and group members,
- confirm current upstream still contains the mismatch,
- assess codegen impact,
- prepare only a minimal candidate after user approval.
```

## TS-CAND-002 - historical V2.1 defects

`TSI-001`, `TSM-001` and `TSD-001` are already explicitly addressed by the V2.2 technical-correction history. They are primarily historical compatibility/diagnostic findings, not automatic requests to rewrite old released XSDs.
