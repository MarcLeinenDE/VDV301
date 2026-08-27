# EV-103 - executable validation of video-service compositor findings

Status: completed; VLS-002, VRS-003 and VDS-002/VDS-003/VDS-004 are executable-confirmed against the exact selected V2.0 XSD families.

## Evidence run

```text
GitHub Actions run: 33111119723
head tested: d4ffe09067cb38bf7f78ba295e029902078ed18d
job: 98653897734
environment: Ubuntu 24.04 / Python 3.12.14 / lxml 6.1.2
EV-103 status: 0 / PASS
```

Harness:

```text
tools/validate_video_v20_compositors.py
```

Authority rules:

```text
V2.0 validation uses each official service XSD with Common V2.0 + Enums V2.0.
The VideoRecordingService V2.4 schema is candidate/integration material only and is used below solely as an explanatory control.
No V2.0 XSD was changed.
No candidate schema was promoted to official authority.
```

## VLS-002 - VideoLiveService.LiveStreamData

Official family:

```text
IBIS-IP_VideoLiveService_V2.0.xsd
-> IBIS-IP_common_V2.0.xsd
-> IBIS-IP_Enumerations_V2.0.xsd
```

Executable results:

```text
PASS: service XSD compiles
PASS: one LiveStreamData containing only StreamID validates
PASS: StreamID + CameraName + rtspURI is rejected as expected
PASS: a complete PDF-shaped multi-field LiveStreamData is rejected as expected
```

The first rejected additional field is `CameraName` after `StreamID`, with the validator reporting that `CameraName` is not expected. This is direct executable evidence of the `xs:choice` behavior rather than a scalar-wrapper or datatype failure.

Conclusion:

```text
VLS-002 = executable-confirmed compositor/structure modelling discrepancy.
The official V2.0 XSD permits one selected LiveStreamData field per instance, while the PDF describes one multi-field stream-information record.
```

## VRS-003 - VideoRecordingStateResponseStructure

Official V2.0 family:

```text
IBIS-IP_VideoRecordingService_V2.0.xsd
-> IBIS-IP_common_V2.0.xsd
-> IBIS-IP_Enumerations_V2.0.xsd
```

Executable V2.0 results:

```text
PASS: service XSD compiles
PASS: response containing only State validates
PASS: State + AlarmArchiveFillLevel is rejected as expected
PASS: State + StartStopMode is rejected as expected
```

The validator rejects the second response field because the first field has already selected the `xs:choice` alternative.

Candidate explanatory control:

```text
IBIS-IP_VideoRecordingService_V2.4.xsd
candidate/integration authority only
```

Result:

```text
PASS: candidate XSD compiles
PASS: VideoRecordingState containing State + AlarmArchiveFillLevel + StartStopMode validates
```

This control corroborates that the later candidate structure models the related state fields together, but it does not change the validation authority of V2.0.

Conclusion:

```text
VRS-003 = executable-confirmed compositor/structure modelling discrepancy for official V2.0.
```

## VDS-002 - ListViewCapabilitiesResponse

Official family:

```text
IBIS-IP_VideoDisplayService_V2.0.xsd
-> IBIS-IP_common_V2.0.xsd
-> IBIS-IP_Enumerations_V2.0.xsd
```

Results:

```text
PASS: service XSD compiles
PASS: single ViewID validates
PASS: PDF-shaped ViewID + ViewName + ViewType is rejected as expected
```

The first rejected additional field is `ViewName`.

Conclusion:

```text
VDS-002 = executable-confirmed.
```

## VDS-003 - SetVideoViewRequest

Results:

```text
PASS: ViewID-only request validates
PASS: PDF-required ViewID + Timeout request is rejected as expected
```

The first rejected additional field is `Timeout`.

Conclusion:

```text
VDS-003 = executable-confirmed.
```

## VDS-004 - response compositor family

Results:

```text
PASS: SetVideoViewResponse with State only validates
PASS: State + CurrentViewID is rejected as expected
PASS: GetDisplayStateResponse with State only validates
PASS: State + CurrentViewID is rejected as expected
PASS: SetNextViewIndexResponse with State only validates
PASS: State + OperationErrorMessage is rejected as expected
```

Conclusion:

```text
VDS-004 = executable-confirmed across all three checked response structures.
```

## Block result

```text
VLS-002: executable-confirmed
VRS-003: executable-confirmed
VDS-002: executable-confirmed
VDS-003: executable-confirmed
VDS-004: executable-confirmed
```

No schema correction is made in the integration branch. These results provide reproducible evidence for post-audit official candidate review and for SDK/provider-note behavior.

## Next

```text
EV-104
TrainSet services
- TSM-002
- TSD-003
root/modelling and operation-manifest behavior
```
