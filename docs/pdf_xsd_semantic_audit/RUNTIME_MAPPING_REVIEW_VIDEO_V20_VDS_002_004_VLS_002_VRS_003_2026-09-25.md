# Runtime-mapping review — Video V2.0 final candidate block — 2026-09-25

Status: **reviewed / persisted / closure gate pending**.

## Scope

Final five runtime-mapping candidates:

```text
VDS-002
VDS-003
VDS-004
VLS-002
VRS-003
```

All five are confirmed PDF/XSD or cross-artifact compositor mismatches with executable evidence. All five remain advisory-only: the exact selected XSD result continues to determine PASS/FAIL.

## Choice-notation guard

The 2026-08-29 corrective overlay remains binding:

```text
-1:1 / -0:1 / -1:* = VDV XML-choice notation
```

The leading minus sign is not a negative cardinality. None of the five runtime mappings may trigger merely because the PDF uses leading-minus notation.

The surviving findings are based on the actual mismatch between ordinary PDF members / documented multi-field records and the exact XSD compositor.

## VDS-002 — ListViewCapabilitiesResponse

Official V2.0 PDF: ViewID and ViewName are ordinary required members; ViewType carries VDV choice notation.

Exact V2.0 XSD:

```text
xs:choice(ViewID | ViewName | ViewType)
```

EV-103 confirms a single ViewID validates while a PDF-shaped multi-field record is rejected.

Decision: `candidate -> reviewed`.

## VDS-003 — SetVideoViewRequest

Official V2.0 PDF requires ViewID and Timeout together.

Exact V2.0 XSD:

```text
xs:choice(ViewID | Timeout)
```

EV-103 confirms ViewID alone is valid while ViewID + Timeout is rejected.

Decision: `candidate -> reviewed`.

## VDS-004 — response compositor family

Affected exact response families:

```text
SetVideoViewResponse
SetNextViewIndexResponse
GetDisplayStateResponse
```

The PDF combines ordinary response members with choice-marked State. The exact V2.0 XSD makes all listed members of each response mutually exclusive in one xs:choice.

EV-103 confirms representative PDF-shaped combinations are rejected.

Decision: `candidate -> reviewed`.

## VLS-002 — LiveStreamData

Official V2.0 PDF describes a multi-field stream record. The exact V2.0 XSD places every stream field inside one xs:choice.

EV-103 confirms StreamID alone validates while StreamID + CameraName + rtspURI and a full PDF-shaped record are rejected.

Decision: `candidate -> reviewed`.

## VRS-003 — GetVideoRecordingStateResponse

Corrected V2.0 PDF reading:

```text
ordinary required fields:
  AlarmArchiveFillLevel
  OperationErrorMessage

a/b choice:
  State
  StartStopMode
```

Exact official V2.0 XSD instead places State, AlarmArchiveFillLevel, OperationErrorMessage and StartStopMode into a single xs:choice.

EV-103 confirms State alone validates and State + AlarmArchiveFillLevel is rejected.

The V2.4 candidate/integration model is correction-history evidence only and is never back-applied to V2.0.

Decision: `candidate -> reviewed`.

## Expected Phase-A inventory after persistence

```text
reviewed        77
candidate        0
not_designed     0
not_applicable 115
implemented      0
total           192
```

No executable matcher, compatibility alias, payload rewrite, schema substitution or XSD mutation is introduced.

## Primary gate

Primary runtime-mapping gate **36098151397**: **SUCCESS**.

The gate verified the exact official VDS/VLS/VRS V2.0 authority blobs, the five compositor boundaries, the binding choice-notation correction, re-ran EV-103, and passed semantic-registry schema, deterministic Known-Issues mapping, SDK-manifest consistency and the complete root-XSD regression suite.
