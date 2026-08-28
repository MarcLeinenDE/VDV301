# VideoRecordingService findings register addendum

Status: Deep Read Pass 2 has completed VRS V1.0 and VRS V2.0. VRS V2.4 is the next planned VideoRecording document. VRS-003 is fresh-read and executable-confirmed for official V2.0.

Authority rule:

```text
Public VRS V1.0 writing is official PDF authority.
No exact official VRS V1.0 service XSD has been confirmed in the checked official repository history.
Do not substitute V2.0 or candidate/integration V2.4 for V1.0.
Official V2.0 strict validation follows IBIS-IP_VideoRecordingService_V2.0.xsd + Common V2.0 + Enums V2.0.
The V2.0 service XSD on dev/schema-integration is byte-identical to the official VDV-301-2.0 release-tag blob 6ef0dae64ce6f4d3aa4f652d6d166896e71aaac7.
V2.4 VideoRecording XSD material remains candidate/integration unless separately promoted by official provenance evidence.
```

The V2.0 PDF statement that the service is compatible/compliant with VDV301 version 1.0 and 2.x is treated as a service/document compatibility statement. It does not authorize schema-version substitution.

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
confidence: very high
scope: official V2.0 XSD
state: fresh PDF/XSD + executable-confirmed
behavior: xs:choice permits only one of State/AlarmArchiveFillLevel/OperationErrorMessage/StartStopMode
historical evidence: V1.0 PDF already describes the values as one grouped response; V2.4 candidate restructures related state data
```

Fresh V2.0 evidence:

```text
PDF page 18: one VideoRecordingStateResponse table contains together
  State
  AlarmArchiveFillLevel
  OperationErrorMessage
  StartStopMode

Official VDV-301-2.0 XSD blob 6ef0dae64ce6f4d3aa4f652d6d166896e71aaac7:
  VideoRecordingStateResponseStructure = xs:choice over the same four members
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

Authority guard: the V2.4 result is corroborative control evidence only and does not rewrite official V2.0 validation.

Evidence document:

```text
docs/pdf_xsd_semantic_audit/24c_executable_validation_video_compositors.md
```

## VRS-004 - SubscribeDisplayState headings

```text
state: visually confirmed persistent through V2.0
classification: pdf_label_or_heading_error_candidate
confidence: very high
scope: V1.0/V2.0 PDF headings/TOC
correct semantic operation: SubscribeVideoRecordingState / UnsubscribeVideoRecordingState
V2.4 documentation: previously observed as corrected
validation_behavior: no DisplayState alias
```

Pinned evidence:

```text
V1.0 page 42 operation table:
  SubscribeVideoRecordingState
  UnsubscribeVideoRecordingState
V1.0 page 46 detail headings:
  SubscribeDisplayState
  UnsubscribeDisplayState

V2.0 page 17 operation table:
  SubscribeVideoRecordingState
  UnsubscribeVideoRecordingState
V2.0 page 21 detail headings:
  SubscribeDisplayState
  UnsubscribeDisplayState
```

## VRS-005 - PauseRecordingRRMRequestStruture

```text
state: PDF/XSD spelling aligned and confirmed for official V2.0
classification: shared_pdf_xsd_identifier_typo_candidate
confidence: high that spelling is typo-like; very high that exact spelling is authoritative for V2.0
scope: official V2.0 PDF + official V2.0 XSD; checked V2.4 candidate XSD retains spelling
validation/codegen: exact `PauseRecordingRRMRequestStruture` spelling remains authoritative
mismatch_status: not a PDF/XSD mismatch
```

Visible V2.0 page 17 and the exact official XSD both use:

```text
VideoRecordingService.PauseRecordingRRMRequestStruture
```

Do not silently normalize this identifier to `RequestStructure` in XML/schema routing or code generation.

## VRS-006 - broken generated cross references in subscription prose

```text
state: visually confirmed in V1.0; historically corrected/absent in V2.0
classification: pdf_editorial_cross_reference_error_candidate
confidence: very high
scope: V1.0 PDF
validation_behavior: none
```

V1.0 visible page 46 contains in both subscription paragraphs:

```text
Fehler! Verweisquelle konnte nicht gefunden werden..
```

V2.0 visible page 21 instead contains normal subscription prose using SubscribeRequest/SubscribeResponse and UnsubscribeRequest/UnsubscribeResponse; the generated error is absent.

## VRS-007 - invalid printed `-1:1` cardinality notation

```text
state: visually confirmed persistent through V2.0
classification: pdf_cardinality_notation_error_candidate
confidence: very high
scope: V1.0/V2.0 PDF
validation_behavior: never repair the printed value into an assumed XSD rule
```

Visible evidence:

```text
V1.0 page 43:
  State          -1:1
  StartStopMode  -1:1

V2.0 page 18:
  State          -1:1
  StartStopMode  -1:1
```

The intended cardinality is not guessed. For V2.0, executable behavior is determined by the exact selected XSD.

## VRS-008 - StopRecording request prose says StopRecordingERM

```text
state: visually confirmed persistent through V2.0
classification: pdf_operation_name_copy_paste_error_candidate
confidence: very high
scope: V1.0/V2.0 PDF
validation_behavior: no StopRecordingERM alias
```

Visible V1.0 page 45 and V2.0 page 20 are both headed for `StopRecording`, but their request prose says no additional data is required for `StopRecordingERM`. The operation inventory and official V2.0 XSD use `StopRecording` and do not define `StopRecordingERM`.

## VRS-009 - English reference labels VideoLiveService as v1.1

```text
state: visually confirmed persistent through V2.0 for VideoLiveService reference
classification: pdf_reference_version_label_error_candidate
confidence: very high for VideoLiveService reference
scope: V1.0/V2.0 reference pages
validation_behavior: none; do not create a VLS V1.1 profile from this label
```

Pinned V1.0 and V2.0 reference pages both show the same conflict for VDV 301-2-11:

```text
German:  VideoLiveService v1.0, 1.0, 05/2017
English: VideoLiveService v1.1  1.0, 05/2017
```

The dedicated pinned VLS V1.0 Deep Read establishes VDV 301-2-11 as VideoLiveService V1.0 from 05/2017. Therefore the English `v1.1` label is a documentation/version-label error.

The adjacent VideoDisplayService `v1.1` reference remains deferred until the dedicated VDS V1.0 Deep Read.

## Visual evidence summary

```text
VRS V1.0
source SHA-256: 29d0bcb270fdab2119c4653296d4bca01e0f8b127eb9aaf393f66b2b34dcd390
source size: 1,227,302 bytes
pin run: 33204215397
render run: 33204547867
rendered pages: 4, 42-46, 50-51

VRS V2.0
source SHA-256: fbe9e68e72de4e5450f562aa6a6117283a94f87a28bded0e05458670527b6c5f
source size: 941,841 bytes
pin run: 33206120045
render run: 33206290291
rendered pages: 4, 17-21, 25
```

Targeted material findings are visually confirmed from exact pinned bytes. All-page/all-figure visual passes are not complete, so both Deep Read states remain `needs_visual_review`.
