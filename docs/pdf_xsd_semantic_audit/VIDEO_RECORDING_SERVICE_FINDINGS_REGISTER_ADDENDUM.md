# VideoRecordingService findings register addendum

Status: Deep Read Pass 2 completed for VRS V1.0, VRS V2.0 and VRS V2.4. Choice-notation interpretation corrected 2026-08-29. VRS-003 remains executable-confirmed for official V2.0; VRS-007 is withdrawn.

Authority rule:

```text
VRS V1.0 PDF: official public VDV writing; no exact official V1.0 service XSD confirmed in checked repository history.
Do not substitute V2.0 or V2.4 for V1.0.
VRS V2.0 strict validation: official VDV-301-2.0 service XSD + Common V2.0 + Enums V2.0.
Official V2.0 service-XSD blob: 6ef0dae64ce6f4d3aa4f652d6d166896e71aaac7.
VRS V2.4 public PDF is official documentation; checked V2.4 XSD is candidate/integration from open upstream PR #27.
```

Choice-notation correction:

```text
VDV 301-2 V2.0 section 6.1.3.3 defines leading '-' as XML-choice notation.
-1:1 is not an invalid cardinality.
VRS-007 is therefore withdrawn.
See AUDIT_CORRECTION_DELTA_CHOICE_NOTATION_2026-08-29.md.
```

## VRS-001 - V1.0 public PDF without confirmed exact official XSD

```text
state: strongly confirmed provenance gap
classification: schema_family_or_provenance_gap
confidence: very high for checked source set
validation_behavior: fail closed; no nearby-version substitution
```

## VRS-002 - V2.4 public document / candidate-XSD authority gap

```text
classification: schema_family_or_provenance_gap
state: confirmed
source: open VDVde/VDV301 PR #27
candidate service-XSD blob: 07ff2c41731e63fd85b203e4b8e0186136caaaaf
validation: candidate/integration profile only
```

## VRS-003 - V2.0 state-response compositor mismatch, refined after choice-notation correction

```text
classification: xsd_structure_modelling_error_candidate
state: fresh PDF/XSD + executable-confirmed
confidence: very high
scope: official V2.0
```

Corrected visible V2.0 PDF reading:

```text
a  State                  -1:1
   AlarmArchiveFillLevel   1:1
   OperationErrorMessage   1:1
b  StartStopMode           -1:1
```

The `-1:1` forms are valid VDV choice notation. The table therefore expresses ordinary required `AlarmArchiveFillLevel` and `OperationErrorMessage` fields plus an `a/b` choice between `State` and `StartStopMode`.

The exact official V2.0 XSD instead models:

```text
xs:choice(
  State,
  AlarmArchiveFillLevel,
  OperationErrorMessage,
  StartStopMode
)
```

EV-103 confirms the executable consequence:

```text
State only: valid
State + AlarmArchiveFillLevel: rejected
State + StartStopMode: rejected
run: 33111119723
```

Thus VRS-003 remains valid; only the former shorthand description "PDF grouped all four" is superseded by the more precise choice-aware reading above.

V2.4 correction history:

Visible V2.4 outer response uses:

```text
a  VideoRecordingState   -1:1
b  OperationErrorMessage
```

and nested `VideoRecordingStateStructure` contains required `State` plus optional `AlarmArchiveFillLevel` and `StartStopMode`. This matches the candidate V2.4 XSD structure, but candidate authority remains candidate only.

## VRS-004 - SubscribeDisplayState headings

```text
V1.0: wrong SubscribeDisplayState/UnsubscribeDisplayState headings
V2.0: wrong headings persist
V2.4: corrected to SubscribeVideoRecordingState/UnsubscribeVideoRecordingState
classification: pdf_label_or_heading_error_candidate
```

## VRS-005 - `PauseRecordingRRMRequestStruture`

```text
state: PDF/XSD spelling aligned
classification: shared_pdf_xsd_identifier_typo_candidate
mismatch_status: not a PDF/XSD mismatch
```

The typo-like `Struture` spelling is used by the official V2.0 PDF and XSD and retained by the checked V2.4 candidate. Do not silently normalize the executable identifier.

## VRS-006 - broken generated subscription cross references

```text
V1.0: visually present
V2.0: corrected/absent
V2.4: remains corrected
classification: pdf_editorial_cross_reference_error_candidate
```

## VRS-007 - withdrawn: `-1:1` is valid VDV choice notation

```text
old classification: invalid printed cardinality notation
new state: withdrawn_after_deep_read_correction
new classification: rejected_after_deep_read
```

Reason:

The finding was opened solely because the leading minus sign was interpreted as a negative minimum. The VDV's own notation rule defines it as an XML-choice marker.

Visible evidence now read correctly:

```text
V2.0:
a State -1:1
b StartStopMode -1:1

V2.4:
a VideoRecordingState -1:1
b OperationErrorMessage
```

There is no standalone cardinality defect here. Any V2.0 PDF/XSD structural difference is carried by VRS-003.

Historical report statements saying VRS-007 "persists" or "moves" in V2.4 are superseded by the 2026-08-29 correction delta.

## VRS-008 - StopRecording prose says StopRecordingERM

```text
state: visually confirmed persistent through V2.4
classification: pdf_operation_name_copy_paste_error_candidate
validation_behavior: no StopRecordingERM alias
```

## VRS-009 - neighboring video-service `v1.1` reference labels

```text
state: cross-document confirmed documentation/version-label errors
classification: pdf_reference_version_label_error_candidate
```

The VideoLiveService `v1.1` line is disproved by the dedicated VLS V1.0 audit. The adjacent VideoDisplayService `v1.1` question was later resolved by the VDS V1.0 audit and official VDV catalog: VDV 301-2-13 05/2017 is VideoDisplayService V1.0. No V1.1 resolver profiles are created from these reference lines.

## VRS-010 - Pause request table caption describes wrong role/name

```text
scope: V1.0/V2.0/V2.4
classification: pdf_table_caption_structure_name_error_candidate
state: visually confirmed cross-version
```

The PauseRecordingRRM request table caption calls it a response structure and shortens the name to `PauseRecordingRequest`. No such alias is created.

## VRS-011 - V2.4 VideoRecordingStateStructure table describes itself as Pause request data

```text
scope: V2.4
classification: pdf_table_role_copy_paste_error_candidate
state: visually confirmed
```

The table is the nested state structure in `VideoRecordingStateResponse`, but its descriptive cell says it is request data for `PauseRecordingRRM`.

## Visual evidence summary

```text
VRS V1.0
pin run: 33204215397
render run: 33204547867

VRS V2.0
pin run: 33206120045
render run: 33206290291

VRS V2.4
pin run: 33206809886
render run: 33207026201
```

## Current finding state

```text
VRS-001 confirmed provenance gap
VRS-002 candidate/official authority gap
VRS-003 executable-confirmed; PDF semantics refined using correct choice notation
VRS-004 corrected in V2.4
VRS-005 persists as exact typo-like identifier
VRS-006 corrected since V2.0
VRS-007 WITHDRAWN
VRS-008 persists through V2.4
VRS-009 cross-document version-label error confirmed
VRS-010 persists across checked versions
VRS-011 V2.4-only copy/paste role error
```

No XSD is changed and candidate authority is not promoted.
