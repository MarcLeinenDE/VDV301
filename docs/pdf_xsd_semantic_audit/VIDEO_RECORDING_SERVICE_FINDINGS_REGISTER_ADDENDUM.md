# VideoRecordingService findings register addendum

Status: first-pass closure completed.

## VRS-001 - V1.0 public PDF without official release-tag XSD

```text
classification: schema_family_or_provenance_gap
confidence: high for checked source set
validation: strict XSD profile unresolved
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
confidence: high
scope: official V2.0 XSD
behavior: xs:choice permits only one of State/AlarmArchiveFillLevel/OperationErrorMessage/StartStopMode
historical evidence: V2.4 candidate restructures response and V2.4 history records clarification of GetVideoRecordingState
```

## VRS-004 - SubscribeDisplayState headings

```text
classification: pdf_label_or_heading_error_candidate
confidence: high
scope: V1.0/V2.0 PDF headings/TOC
correct semantic operation: SubscribeVideoRecordingState / UnsubscribeVideoRecordingState
V2.4: corrected
```

## VRS-005 - PauseRecordingRRMRequestStruture

```text
classification: xsd_typo_candidate
confidence: high that spelling is typo-like
scope: V2.0 official + V2.4 candidate
validation/codegen: exact XSD spelling remains authoritative
```
