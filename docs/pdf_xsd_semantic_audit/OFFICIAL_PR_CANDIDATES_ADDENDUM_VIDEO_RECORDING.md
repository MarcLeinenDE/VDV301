# VideoRecordingService post-audit official-facing candidates

Tracking only. Do not open or modify any upstream PR without explicit user approval.

## VRS-CAND-001 - V2.0 response compositor

Linked finding: VRS-003.

```text
Official V2.0 XSD models State/AlarmArchiveFillLevel/OperationErrorMessage/StartStopMode as sibling alternatives in xs:choice.
Public V1.0/V2.0 semantics describe combined state/fill-level information.
Open PR #27 V2.4 candidate restructures the response and the V2.4 document history explicitly records the GetVideoRecordingState clarification.
```

Post-audit requirements:

```text
- compile exact official V2.0 pool,
- demonstrate multi-field rejection,
- compile candidate V2.4 pool,
- demonstrate corrected multi-field state response,
- assess compatibility impact before deciding whether any separate V2.0 correction proposal is sensible.
```

## VRS-CAND-002 - PauseRecordingRRMRequestStruture spelling

Linked finding: VRS-005.

```text
Potential narrow XSD typo candidate, but changing an XSD type name can break generated APIs even when XML element names are unchanged.
```

Do not combine automatically with existing upstream PR #27.
