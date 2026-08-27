# VideoRecordingService technical validation backlog addendum

No task below is marked complete by the semantic audit.

```text
VRS-VB-001 compile official V2.0 + Common V2.0 + Enums V2.0.
VRS-VB-002 validate V2.0 response containing only State.
VRS-VB-003 verify V2.0 rejection of State + AlarmArchiveFillLevel due to xs:choice.
VRS-VB-004 verify V2.0 rejection of State + StartStopMode due to xs:choice.
VRS-VB-005 compile PR-#27 V2.4 candidate with exact Common V2.0 + Enums V2.0 pool.
VRS-VB-006 validate V2.4 candidate VideoRecordingState with required State and both optional fields.
VRS-VB-007 validate V2.4 candidate OperationErrorMessage alternative.
VRS-VB-008 inspect generated type names for PauseRecordingRRMRequestStruture.
VRS-VB-009 if an authoritative V1.0 XSD source is later found, establish provenance before any validation routing.
```
