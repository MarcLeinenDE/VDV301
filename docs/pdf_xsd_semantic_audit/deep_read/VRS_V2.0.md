# Deep Read - VideoRecordingService V2.0

Document id: `VRS_V2.0`

Status: `needs_visual_review`

Fresh-read date: 2026-08-28

## 1. Source and provenance

Official public writing:

```text
VDV-Schrift 301-2-12
VideoRecordingService - V2.0
08/2019
https://www.vdv.de/301-2-12-sdes-v2-0-video-recording-service.pdfx
```

Byte pin:

```text
SHA-256: fbe9e68e72de4e5450f562aa6a6117283a94f87a28bded0e05458670527b6c5f
size:    941,841 bytes
pin run: 33206120045
```

No VDV PDF bytes or rendered page images are committed to the repository.

## 2. Independent-read order

The V2.0 writing was fresh-read first from the official source. Only after the PDF semantics and material visual findings were established were the exact V2.0 XSD, EV-103 and later V2.4 candidate material reintroduced.

This prevents later corrections from being used as a template for interpreting the historical V2.0 source.

## 3. Visual evidence

Pinned-byte render fallback:

```text
run: 33206290291
pages: 4, 17, 18, 19, 20, 21, 25
resolution: 180 dpi
```

The renderer verified the pinned PDF hash and byte size before rendering.

Targeted material pages are visually confirmed. An all-page/all-figure visual pass is not complete, therefore the overall state remains `needs_visual_review`.

## 4. Foreword and compatibility statement

Visible page 4 identifies VDV 301-2-12 as the VideoRecordingService writing and states in both languages that the service is compatible/compliant with VDV301 version `1.0` as well as `2.x`.

Authority interpretation:

```text
This is a service/document compatibility statement.
It is NOT permission to validate VRS V1.0 with the V2.0 XSD.
Exact schema-family provenance remains version-specific.
```

The separately completed VRS V1.0 audit found no exact official V1.0 service XSD in the checked official repository history, so the V1.0 fail-closed routing rule remains unchanged.

## 5. Operation inventory

Visible page 17 lists:

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

The response operations use the shared type:

```text
VideoRecordingService.VideoRecordingStateResponseStructure
```

The Pause request row visibly names:

```text
VideoRecordingService.PauseRecordingRRMRequestStruture
```

The subscription rows use generic Common Subscribe/Unsubscribe structures.

## 6. Exact official V2.0 XSD authority

The exact upstream release-tag file was read from:

```text
VDVde/VDV301
ref: VDV-301-2.0
IBIS-IP_VideoRecordingService_V2.0.xsd
Git blob: 6ef0dae64ce6f4d3aa4f652d6d166896e71aaac7
```

It includes exactly:

```text
IBIS-IP_common_V2.0.xsd
IBIS-IP_Enumerations_V2.0.xsd
```

The copy on `dev/schema-integration` has the same Git blob SHA, so the audited service XSD is byte-identical to the official release-tag file.

## 7. VRS-003 - grouped PDF state vs `xs:choice`

Visible page 18 says the proposal uses only one response data structure and presents one `VideoRecordingStateResponse` table containing together:

```text
State
AlarmArchiveFillLevel
OperationErrorMessage
StartStopMode
```

The exact official V2.0 XSD instead declares:

```text
VideoRecordingService.VideoRecordingStateResponseStructure
  xs:choice
    State
    AlarmArchiveFillLevel
    OperationErrorMessage
    StartStopMode
```

This is a direct PDF/XSD structural mismatch for the exact V2.0 authority family.

EV-103 had already executed this exact family:

```text
run: 33111119723
service XSD compiles: PASS
State-only response: valid
State + AlarmArchiveFillLevel: rejected
State + StartStopMode: rejected
EV-103: PASS
```

Therefore `VRS-003` is freshly PDF/XSD reconfirmed and remains executable-confirmed.

The later V2.4 candidate groups related state fields under `VideoRecordingStateStructure`; that is explanatory correction evidence only and does not rewrite V2.0 validation.

## 8. VRS-004 - SubscribeDisplayState headings persist

Visible page 17 operation inventory correctly uses:

```text
SubscribeVideoRecordingState
UnsubscribeVideoRecordingState
```

Visible page 21 detail headings still say:

```text
SubscribeDisplayState
UnsubscribeDisplayState
```

Thus `VRS-004` visibly persists from V1.0 into V2.0.

No DisplayState alias is created.

## 9. VRS-005 - `PauseRecordingRRMRequestStruture`

The typo-like identifier is visibly present in the V2.0 PDF operation table and is also the exact type name in the official V2.0 XSD:

```text
VideoRecordingService.PauseRecordingRRMRequestStruture
```

Result:

```text
This is not a PDF/XSD mismatch.
It is a shared PDF/XSD identifier spelling that looks typo-like.
Exact XSD spelling remains executable/codegen authority.
Do not auto-correct it to RequestStructure in XML/schema routing.
```

The checked V2.4 candidate XSD still carries the same `Struture` spelling.

## 10. VRS-006 - broken V1.0 cross references corrected in V2.0

V1.0 visibly contained generated Word placeholders in both subscription paragraphs.

Visible V2.0 page 21 instead contains ordinary prose saying SubscribeRequest/SubscribeResponse and UnsubscribeRequest/UnsubscribeResponse are used. The broken generated placeholder is absent.

History:

```text
V1.0: VRS-006 present
V2.0: corrected/absent
```

## 11. VRS-007 - invalid `-1:1` cardinality notation persists

Visible page 18 prints:

```text
State          -1:1
StartStopMode  -1:1
```

Thus `VRS-007` visibly persists into V2.0.

The audit does not infer an intended cardinality from the malformed notation. Executable V2.0 behavior comes from the selected XSD, not from repairing the printed table.

## 12. VRS-008 - StopRecording prose still says StopRecordingERM

Visible page 20 is headed:

```text
2.5.4 Data structure of operation StopRecording
```

The request subsection says:

```text
No additional data must be given by execution of operation StopRecordingERM.
```

The operation inventory uses `StopRecording` and the official XSD declares `VideoRecordingService.StopRecordingResponse`; there is no `StopRecordingERM` operation.

Therefore `VRS-008` visibly persists into V2.0. No alias is created.

## 13. VRS-009 - VideoLiveService v1.1 reference persists

Visible page 25 references VDV 301-2-11 as:

```text
German:  VideoLiveService v1.0, 1.0, 05/2017
English: VideoLiveService v1.1  1.0, 05/2017
```

The dedicated VLS V1.0 audit established VDV 301-2-11 as VideoLiveService V1.0 from 05/2017.

Therefore the VideoLive portion of `VRS-009` visibly persists into VRS V2.0.

The adjacent VideoDisplayService `v1.1` label remains deferred until the dedicated VDS V1.0 Deep Read establishes its own history.

## 14. Minor editorial observations not promoted to separate findings

The V2.0 writing also contains low-impact spelling/wording issues such as `VideoReordingService`, pluralized operation prose and similar editorial artifacts.

They are not opened as separate findings because they do not add meaningful resolver, validation or provenance behavior beyond the already recorded material findings.

## 15. Later V2.4 explanatory control

Only after the independent V2.0 read, the existing V2.4 candidate XSD was consulted.

It changes the state response model to a choice between:

```text
VideoRecordingState
OperationErrorMessage
```

with `VideoRecordingState` containing a sequence of:

```text
State
AlarmArchiveFillLevel  optional
StartStopMode          optional
```

EV-103 confirms a grouped candidate V2.4 state sample validates.

Authority guard:

```text
V2.4 XSD = candidate/integration evidence only.
It explains a later modelling direction but does not alter official V2.0 behavior.
```

## 16. Fresh-read outcome

No new finding ID was needed.

Existing finding history:

```text
VRS-003  persists; fresh PDF/XSD reconfirmed; EV-103 executable-confirmed
VRS-004  persists visibly
VRS-005  clarified as shared PDF/XSD typo-like exact identifier, not a mismatch
VRS-006  corrected/absent in V2.0
VRS-007  persists visibly
VRS-008  persists visibly
VRS-009  VideoLive reference portion persists visibly
```

No XSD change is made.

## 17. Completion status

```text
textual fresh read: complete
exact source pin: complete
targeted visual checks: complete
exact official V2.0 XSD provenance: complete
fork-vs-official service XSD byte identity: confirmed
EV-103 comparison: complete after fresh read
V2.4 candidate explanatory comparison: complete after fresh read
all-page/all-figure visual pass: not complete
state: needs_visual_review
```

Next planned VideoRecording document: `VRS_V2.4`, using its own byte pin and treating its public PDF and candidate/integration XSD as separate authority lanes.