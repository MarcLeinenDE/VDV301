# EV-103 - executable validation of video-service compositor findings

Status: completed; VLS-002, VRS-003 and VDS-002/VDS-003/VDS-004 are executable-confirmed against the exact selected V2.0 XSD families.

Choice-notation interpretation corrected 2026-08-29. The executable XSD outcomes remain valid; the PDF-side descriptions below use the VDV's actual leading-minus XML-choice notation.

## Evidence run

```text
GitHub Actions run: 33111119723
head tested: d4ffe09067cb38bf7f78ba295e029902078ed18d
job: 98653897734
environment: Ubuntu 24.04 / Python 3.12.14 / lxml 6.1.2
EV-103 status: PASS
```

Harness:

```text
tools/validate_video_v20_compositors.py
```

Authority rules:

```text
V2.0 validation uses each official service XSD with Common V2.0 + Enums V2.0.
VideoRecordingService V2.4 schema is candidate/integration material only and is used solely as an explanatory control.
No V2.0 XSD was changed.
No candidate schema was promoted to official authority.
```

## VDV table-notation correction

VDV 301-2 V2.0 section 6.1.3.3 defines a prefixed minus sign as an XML-choice marker. Therefore `-1:1` is not a malformed/negative cardinality.

This correction affects only how the PDF tables are described. EV-103's executed XSD results are unchanged.

Correction overlay:

```text
docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_CHOICE_NOTATION_2026-08-29.md
```

## VLS-002 - VideoLiveService.LiveStreamData

Official family:

```text
IBIS-IP_VideoLiveService_V2.0.xsd
-> IBIS-IP_common_V2.0.xsd
-> IBIS-IP_Enumerations_V2.0.xsd
```

Corrected PDF-side interpretation:

The visible V2.0 `LiveStreamData` table contains numerous ordinary `1:1` fields in one structure, including `StreamID`, `CameraName`, `CameraType`, `rtspURI`, width/height, frame rate, bitrate and transformation fields. `CameraCurrentState` and `VideoCodec` carry leading-minus choice notation.

The exact V2.0 XSD instead places **all** individual LiveStreamData fields in one `xs:choice`.

Executable results:

```text
PASS: service XSD compiles
PASS: one LiveStreamData containing only StreamID validates
PASS: StreamID + CameraName + rtspURI is rejected as expected
PASS: a complete PDF-shaped multi-field LiveStreamData is rejected as expected
```

The decisive three-field sample uses only ordinary PDF `1:1` rows and therefore does not depend on any interpretation of `-1:1`.

Conclusion:

```text
VLS-002 remains executable-confirmed.
```

## VRS-003 - VideoRecordingStateResponseStructure

Official V2.0 family:

```text
IBIS-IP_VideoRecordingService_V2.0.xsd
-> IBIS-IP_common_V2.0.xsd
-> IBIS-IP_Enumerations_V2.0.xsd
```

Corrected visible PDF reading:

```text
a  State                  -1:1
   AlarmArchiveFillLevel   1:1
   OperationErrorMessage   1:1
b  StartStopMode           -1:1
```

The leading-minus values are valid VDV choice notation. The PDF therefore presents ordinary required AlarmArchiveFillLevel and OperationErrorMessage fields plus an a/b choice between State and StartStopMode.

The official V2.0 XSD instead models all four members as alternatives of one `xs:choice`.

Executable V2.0 results:

```text
PASS: service XSD compiles
PASS: response containing only State validates
PASS: State + AlarmArchiveFillLevel is rejected as expected
PASS: State + StartStopMode is rejected as expected
```

Candidate explanatory control:

```text
IBIS-IP_VideoRecordingService_V2.4.xsd
candidate/integration authority only
```

Visible V2.4 PDF and candidate XSD both move to an outer choice between VideoRecordingState and OperationErrorMessage, with VideoRecordingState grouping State plus optional fill-level/start-stop-mode data.

Result:

```text
PASS: candidate XSD compiles
PASS: grouped V2.4 VideoRecordingState sample validates
```

Conclusion:

```text
VRS-003 remains executable-confirmed for official V2.0.
VRS-007 (formerly 'invalid -1:1') is withdrawn separately; that correction does not close VRS-003.
```

## VDS-002 - ListViewCapabilitiesResponse

Official family:

```text
IBIS-IP_VideoDisplayService_V2.0.xsd
-> IBIS-IP_common_V2.0.xsd
-> IBIS-IP_Enumerations_V2.0.xsd
```

Corrected visible PDF reading:

```text
ViewID       1:1
ViewName     1:1
a  ViewType  -1:1
```

The minus sign on ViewType is valid choice notation; ViewID and ViewName remain ordinary mandatory rows in the PDF.

The exact XSD models `xs:choice(ViewID | ViewName | ViewType)`.

Results:

```text
PASS: service XSD compiles
PASS: single ViewID validates
PASS: PDF-shaped ViewID + ViewName + ViewType is rejected as expected
```

Conclusion:

```text
VDS-002 remains executable-confirmed.
```

## VDS-003 - SetVideoViewRequest

Visible PDF:

```text
ViewID   1:1
Timeout  1:1
```

XSD:

```text
xs:choice(ViewID | Timeout)
```

Results:

```text
PASS: ViewID-only request validates
PASS: PDF-required ViewID + Timeout request is rejected as expected
```

Conclusion:

```text
VDS-003 remains executable-confirmed and is unaffected by the notation correction.
```

## VDS-004 - response compositor family

Corrected visible PDF examples:

```text
SetVideoViewResponse:
a State -1:1
CurrentViewID 1:1
OperationErrorMessage 0:1

SetNextViewIndexResponse:
a State -1:1
OperationErrorMessage 0:1

GetDisplayStateResponse:
a State -1:1
CurrentViewID 1:1
OperationErrorMessage 0:1
```

The minus marker is valid choice notation. The other rows remain ordinary non-choice fields in the visible PDF.

The exact V2.0 XSD models all listed members of each response as one `xs:choice`.

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
VDS-004 remains executable-confirmed.
```

## Corrected block result

```text
VLS-002: executable-confirmed
VRS-003: executable-confirmed; PDF interpretation refined
VDS-002: executable-confirmed; PDF interpretation refined
VDS-003: executable-confirmed
VDS-004: executable-confirmed; PDF interpretation refined
```

Related notation findings:

```text
VLS-005: refined to choice-notation application anomaly
VRS-007: withdrawn/rejected after correction
VDS-006: refined to choice-notation application anomaly
```

No schema correction is made in the integration branch.
