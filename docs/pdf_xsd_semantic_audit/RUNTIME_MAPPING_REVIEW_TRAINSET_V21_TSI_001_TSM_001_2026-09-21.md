# Runtime-mapping review — TrainSet V2.1 TSI-001 / TSM-001 — 2026-09-21

Status: **reviewed / persisted / closure gate pending**.

## Authority boundary

This block is strictly limited to the official VDV-301-2.1 TrainSet service family.

```text
TrainSetInformationService V2.1 blob:
897f373e31b76aa23d8bc206854b042524e4c102

TrainSetManagementService V2.1 blob:
add9d1cb37e5759ff7a77855b239108d38373206
```

The official V2.2 correction history is evidence about the historical defects, **not executable authority for V2.1**.

## TSI-001 — documented multiple coaches cannot be represented in V2.1

Finding assessment remains `cross_artifact_mismatch`, confidence `confirmed`.

- V2.1 PDF physical pages 24-25 describe a sequence of coach data sets, one per coach.
- Exact V2.1 XSD contains one flat non-repeatable coach-field sequence.
- EV-109 / EV-161 prove one flat coach record validates and a second documented coach record is rejected.
- V2.2 later introduces repeatable `SingleCoach` with `maxOccurs=unbounded`.

Decision: `candidate -> reviewed`.

Runtime advisory is allowed only for an exact V2.1 XSD rejection where a complete first coach record is followed by an attempted second coach data set. Unrelated coach-field errors must not be classified as TSI-001. V2.2 modelling must not be back-applied.

## TSM-001 — historical V2.1 response root without Response suffix

Finding assessment remains `confirmed_xsd_defect`, confidence `confirmed`.

- exact V2.1 XSD declares `TrainSetManagementService.GetTrainSetComposition`;
- `TrainSetManagementService.GetTrainSetCompositionResponse` is absent in V2.1;
- EV-109 confirms old-name VALID / corrected-name INVALID;
- official V2.2 history explicitly records the corrected `...Response` name.

Decision: `candidate -> reviewed`.

For V2.1, PASS/FAIL continues to follow the historical XSD. A provider using the later corrected V2.2 root under a V2.1 profile **fails V2.1 validation**; the SDK may only explain that the historical identifier was later corrected.

## Expected mapping inventory after persistence

```text
reviewed        66
candidate       12
not_designed     0
not_applicable 114
implemented      0
```

No compatibility aliases, schema substitution or XSD mutation are introduced.

## Primary gate

Primary runtime-mapping gate **35645781280**: **SUCCESS**.

The gate re-ran EV-109 against the exact official TrainSet V2.1 XSDs, verified the V2.1 blob identities, semantic-registry schema, deterministic Known-Issues mapping, SDK-manifest consistency and the complete root-XSD regression suite before persistence.
