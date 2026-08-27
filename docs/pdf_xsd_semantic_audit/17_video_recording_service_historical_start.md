# VideoRecordingService V1.0 / V2.0 / V2.4 historical audit start

Status: provenance and version-family first pass completed. Local XSD compilation/sample validation remains pending.

Working branch base:

```text
MarcLeinenDE/VDV301 dev/schema-integration
e2f701ed820d846e21da3fcdda6c21c05789524c
```

Scope:

```text
VDV 301-2-12 VideoRecordingService V1.0 (05/2017)
VDV 301-2-12 VideoRecordingService V2.0 (08/2019)
VDV 301-2-12 VideoRecordingService V2.4 (01/2023)
IBIS-IP_VideoRecordingService_V2.0.xsd
IBIS-IP_VideoRecordingService_V2.4.xsd
Common/Enumerations dependencies selected by those service XSDs
VDVde/VDV301 official release tags
VDVde/VDV301 open PR #27
```

## 1. V1.0 public document and provenance

The public V1.0 document describes VideoRecordingService as a proposal/enhancement for VDV301 V1.0 and defines the later operation family including:

```text
StartRecordingRRM
StartRecordingERM
PauseRecordingRRM
StopRecording
ForceStopRecording
GetVideoRecordingState
SubscribeVideoRecordingState
UnsubscribeVideoRecordingState
```

No `IBIS-IP_VideoRecordingService_V1.0.xsd` was found in the checked official release tags or repository code search.

Therefore:

```text
V1.0 document known
strict V1.0 XSD mapping unresolved
no historical backfill allowed
no substitution with V2.0
```

This becomes VRS-001.

## 2. V2.0 official XSD family

Official source:

```text
Repository: VDVde/VDV301
Tag: VDV-301-2.0
File: IBIS-IP_VideoRecordingService_V2.0.xsd
Blob: 6ef0dae64ce6f4d3aa4f652d6d166896e71aaac7
```

The branch file is the same official service family.

Exact dependencies selected by the XSD:

```text
VideoRecordingService V2.0
-> IBIS-IP_common_V2.0.xsd
-> IBIS-IP_Enumerations_V2.0.xsd
```

Do not substitute later Common/Enumerations pools.

## 3. V2.4 public document and candidate XSD

Public document:

```text
VDV 301-2-12 VideoRecordingService V2.4, 01/2023
```

No official VDVde/VDV301 V2.4 release tag exists in the checked repository release history.

Open upstream PR #27:

```text
PR: VDVde/VDV301 #27
Title: New AnalogRadioService and updated VideoRecordingService
State: open / unmerged
Head: 0aa728aab47a7f13b6f36da415581d51592c4ca7
File: IBIS-IP_VideoRecordingService_V2.4.xsd
Blob: 07ff2c41731e63fd85b203e4b8e0186136caaaaf
```

The branch V2.4 file has exactly the same blob SHA.

Classification:

```text
candidate/integration material
not official historical release material
```

Exact candidate dependencies remain deliberately old-versioned:

```text
VideoRecordingService V2.4 candidate
-> Common V2.0
-> Enumerations V2.0
```

Do not re-route to Common/Enums V2.4 just because the service document is V2.4.

## 4. Historical response-structure correction

V1.0 and V2.0 PDFs describe `VideoRecordingStateResponse` as carrying recording state information and related fill-level/start-stop information, with error information as the failure path.

Official V2.0 XSD instead defines:

```text
VideoRecordingStateResponseStructure
  xs:choice
    State
    AlarmArchiveFillLevel
    OperationErrorMessage
    StartStopMode
```

This permits exactly one of the four children.

The V2.4 candidate changes the model to:

```text
VideoRecordingStateResponseStructure
  xs:choice
    VideoRecordingState -> VideoRecordingStateStructure
    OperationErrorMessage

VideoRecordingStateStructure
  xs:sequence
    State required
    AlarmArchiveFillLevel optional
    StartStopMode optional
```

The V2.4 document version history explicitly records clarification/correction of the GetVideoRecordingState response.

This becomes VRS-003 and is a strong schema-modelling correction candidate, but no XSD is changed during this audit.

## 5. Subscribe heading history

V1.0/V2.0 operation tables identify:

```text
SubscribeVideoRecordingState
UnsubscribeVideoRecordingState
```

but the detailed section headings/TOC use:

```text
SubscribeDisplayState
UnsubscribeDisplayState
```

V2.4 corrects those headings to VideoRecordingState and explicitly records a fixed copy/paste error in the version history.

This becomes VRS-004 (`pdf_label_or_heading_error_candidate`).

## 6. Persistent XSD spelling candidate

Both official V2.0 and candidate V2.4 XSDs define:

```text
VideoRecordingService.PauseRecordingRRMRequestStruture
```

`Struture` is typo-like relative to the normal `Structure` naming convention. The PDFs propagate the same type spelling in the operation table, so strict validation/code generation must continue to use the exact XSD type name.

This becomes VRS-005 (`xsd_typo_candidate`).

## 7. Next file

```text
docs/pdf_xsd_semantic_audit/17a_video_recording_service_v1_0_v2_0_v2_4_pdf_xsd_first_pass.md
```
