# VideoRecordingService findings register addendum

Status: Deep Read Pass 2 has completed VRS V1.0; VRS V2.0 remains the next planned VideoRecording document. VRS-003 remains executable-confirmed for official V2.0.

Authority rule:

```text
Public VRS V1.0 writing is official PDF authority.
No exact official VRS V1.0 service XSD has been confirmed in the checked official repository history.
Do not substitute V2.0 or candidate/integration V2.4 for V1.0.
Official V2.0 strict validation follows IBIS-IP_VideoRecordingService_V2.0.xsd + Common V2.0 + Enums V2.0.
V2.4 VideoRecording XSD material remains candidate/integration unless separately promoted by official provenance evidence.
```

## VRS-001 - V1.0 public PDF without confirmed exact official XSD

```text
state: strongly confirmed provenance gap for checked official repository history
classification: schema_family_or_provenance_gap
confidence: very high for checked source set
version_scope: public V1.0
validation_behavior: no strict V1.0 XSD profile; no nearby-version substitution
final_handling_bucket: official_schema_family_clarification_candidate
```

Fresh V1.0 provenance checks:

```text
complete official VDV-301-1.0 tag tree: no VideoRecordingService V1.0 XSD
IBIS_IP_V1.0.xsd: no VideoRecordingService include/declaration
commit history for IBIS-IP_VideoRecordingService_V1.0.xsd: empty
```

The V1.0 PDF therefore remains documentation authority only for this service/version. It is not validated with V2.0 merely because V2.0 is available.

## VRS-002 - V2.4 public document / candidate-XSD authority gap

```text
classification: schema_family_or_provenance_gap
confidence: high
source: open VDVde/VDV301 PR #27
candidate blob: 07ff2c41731e63fd85b203e4b8e0186136caaaaf
validation: candidate/integration profile only
```

## VRS-003 - V2.0 VideoRecordingStateResponse compositor

```text
classification: xsd_structure_modelling_error_candidate
confidence: high
scope: official V2.0 XSD
state: executable-confirmed
behavior: xs:choice permits only one of State/AlarmArchiveFillLevel/OperationErrorMessage/StartStopMode
historical evidence: V1.0 PDF already describes these values as one grouped response structure; V2.4 candidate restructures the response and V2.4 history records clarification of GetVideoRecordingState
```

Executable evidence:

```text
GitHub Actions run 33111119723
head d4ffe09067cb38bf7f78ba295e029902078ed18d
V2.0 State-only response: valid
V2.0 State + AlarmArchiveFillLevel: rejected; AlarmArchiveFillLevel not expected
V2.0 State + StartStopMode: rejected; StartStopMode not expected
V2.4 candidate explanatory control with grouped State + FillLevel + StartStopMode: valid
EV-103 status: PASS
```

Fresh V1.0 visual evidence:

```text
page 43 visibly presents one VideoRecordingStateResponse containing:
State
AlarmArchiveFillLevel
OperationErrorMessage
StartStopMode
```

Authority guard: V1.0 strengthens semantic history only. No V1.0 XSD behavior is inferred.

Evidence document:

```text
docs/pdf_xsd_semantic_audit/24c_executable_validation_video_compositors.md
```

## VRS-004 - SubscribeDisplayState headings

```text
state: visually confirmed for V1.0; previously tracked across V1.0/V2.0, corrected by checked V2.4 documentation
classification: pdf_label_or_heading_error_candidate
confidence: very high for V1.0
scope: V1.0/V2.0 PDF headings/TOC
correct semantic operation: SubscribeVideoRecordingState / UnsubscribeVideoRecordingState
validation_behavior: no DisplayState alias
```

Pinned V1.0 visual evidence:

```text
page 42 operation table:
  SubscribeVideoRecordingState
  UnsubscribeVideoRecordingState

page 46 detail headings:
  SubscribeDisplayState
  UnsubscribeDisplayState
```

## VRS-005 - PauseRecordingRRMRequestStruture

```text
classification: xsd_typo_candidate
confidence: high that spelling is typo-like
scope: V2.0 official + V2.4 candidate
validation/codegen: exact XSD spelling remains authoritative
```

## VRS-006 - broken generated cross references in subscription prose

```text
state: visually confirmed
classification: pdf_editorial_cross_reference_error_candidate
confidence: very high
scope: V1.0 PDF
validation_behavior: none
```

Visible page 46 contains the literal generated-document error in both subscription paragraphs:

```text
Fehler! Verweisquelle konnte nicht gefunden werden..
```

The broken reference does not alter Common subscription structure authority.

## VRS-007 - invalid printed `-1:1` cardinality notation

```text
state: visually confirmed
classification: pdf_cardinality_notation_error_candidate
confidence: very high
scope: V1.0 PDF
validation_behavior: none for V1.0 because no exact strict XSD profile is confirmed
```

Visible page 43 prints:

```text
State          -1:1
StartStopMode  -1:1
```

The audit does not guess the intended cardinality.

## VRS-008 - StopRecording request prose says StopRecordingERM

```text
state: visually confirmed
classification: pdf_operation_name_copy_paste_error_candidate
confidence: very high
scope: V1.0 PDF
validation_behavior: no StopRecordingERM alias
```

Visible page 45 is headed for operation `StopRecording`, but its request prose says no additional data is required for `StopRecordingERM`. The page-42 operation inventory contains `StopRecording` and no `StopRecordingERM`.

## VRS-009 - English reference labels VideoLiveService as v1.1

```text
state: visually confirmed cross-document
classification: pdf_reference_version_label_error_candidate
confidence: very high for VideoLiveService reference
scope: V1.0 reference page
validation_behavior: none; do not create a VLS V1.1 profile from this label
```

Visible page 51 references VDV 301-2-11. The German line says VideoLiveService `v1.0`, while the English line says `VideoLiveService v1.1` alongside `1.0, 05/2017`.

The dedicated pinned VLS V1.0 Deep Read establishes VDV 301-2-11 as VideoLiveService V1.0 from 05/2017. Therefore the English `v1.1` label is a documentation/version-label error.

The adjacent VideoDisplayService `v1.1` reference remains deferred until the dedicated VDS V1.0 Deep Read.

## VRS V1.0 visual evidence

```text
source SHA-256: 29d0bcb270fdab2119c4653296d4bca01e0f8b127eb9aaf393f66b2b34dcd390
source size: 1,227,302 bytes
pin run: 33204215397
render run: 33204547867
rendered pages: 4, 42-46, 50-51
```

Targeted material findings are visually confirmed from exact pinned bytes. An all-page/all-figure visual pass is not complete, so the Deep Read status remains `needs_visual_review`.
