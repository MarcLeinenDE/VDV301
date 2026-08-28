# Audit handoff delta - VideoRecordingService V2.0 Deep Read

Date: 2026-08-28

Branch: `dev/schema-integration`

## Scope completed

Completed the independent byte-pinned Deep Read for:

```text
VRS_V2.0
VDV-Schrift 301-2-12
VideoRecordingService - V2.0
08/2019
```

No XSD was changed.

## Exact PDF source

```text
source_id: VRS_V2.0
official URL: https://www.vdv.de/301-2-12-sdes-v2-0-video-recording-service.pdfx
SHA-256: fbe9e68e72de4e5450f562aa6a6117283a94f87a28bded0e05458670527b6c5f
size: 941,841 bytes
pin run: 33206120045
```

## Visual evidence

Pinned-byte fallback render:

```text
run: 33206290291
pages: 4, 17-21, 25
180 dpi
```

The temporary render workflow was removed again after the artifact was produced. The permanent renderer/policy remain.

Targeted material pages are visually confirmed; an all-page/all-figure pass is not complete, so status remains `needs_visual_review`.

## Exact V2.0 XSD authority

Official upstream release tag:

```text
VDVde/VDV301
ref: VDV-301-2.0
IBIS-IP_VideoRecordingService_V2.0.xsd
blob: 6ef0dae64ce6f4d3aa4f652d6d166896e71aaac7
```

Dependency family:

```text
IBIS-IP_common_V2.0.xsd
IBIS-IP_Enumerations_V2.0.xsd
```

The same service XSD on `dev/schema-integration` has the identical Git blob SHA. Therefore the V2.0 service-XSD authority used in the audit is byte-identical to the official release-tag file.

## Compatibility statement authority boundary

Visible page 4 says the service is compatible/compliant with VDV301 version `1.0` and `2.x`.

Audit rule:

```text
This is a service/document compatibility statement.
It does not authorize using the V2.0 XSD as the missing VRS V1.0 schema authority.
```

The VRS V1.0 fail-closed provenance result remains unchanged.

## Finding history

### VRS-003

Persists and is now freshly PDF/XSD reconfirmed from exact V2.0 sources.

PDF page 18 presents one state response with:

```text
State
AlarmArchiveFillLevel
OperationErrorMessage
StartStopMode
```

Official XSD models those members under `xs:choice`.

EV-103 run `33111119723` remains exact executable proof:

```text
State only: valid
State + AlarmArchiveFillLevel: rejected
State + StartStopMode: rejected
```

The later V2.4 candidate grouping is explanatory only.

### VRS-004

Persists visibly in V2.0:

```text
operation table:
SubscribeVideoRecordingState
UnsubscribeVideoRecordingState

detail headings:
SubscribeDisplayState
UnsubscribeDisplayState
```

### VRS-005

Refined:

```text
PauseRecordingRRMRequestStruture
```

is visible in the V2.0 PDF operation table and is also the exact official V2.0 XSD type spelling.

Therefore it is not a PDF/XSD mismatch. It is a shared typo-like identifier spelling and must remain exact for validation/codegen. Checked V2.4 candidate XSD still carries the same spelling.

### VRS-006

Corrected/absent in V2.0. The V1.0 Word-generated broken reference placeholders are replaced by normal subscription prose on visible V2.0 page 21.

### VRS-007

Persists visibly:

```text
State          -1:1
StartStopMode  -1:1
```

No intended replacement cardinality is guessed.

### VRS-008

Persists visibly. Section is `StopRecording`, request prose says `StopRecordingERM`; operation table and official XSD use `StopRecording`.

### VRS-009

VideoLive reference portion persists visibly on V2.0 page 25:

```text
German: VideoLiveService v1.0
English: VideoLiveService v1.1
```

The dedicated VLS V1.0 Deep Read keeps the English label classified as a documentation/version-label error.

The neighboring VideoDisplayService `v1.1` reference remains deferred to `VDS_V1.0`.

## No new finding ID

VRS V2.0 required no new finding ID. The value of the block is the exact version-history resolution and the fresh confirmation of existing findings.

## Closure files

```text
00_START_HERE/CURRENT_STATE.json
audit_registry/deep_read_findings_delta_vrs_v20_2026-08-28.json
audit_registry/deep_read_registry_delta_vrs_v20_2026-08-28.json
docs/pdf_xsd_semantic_audit/VIDEO_RECORDING_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/deep_read/VRS_V2.0.md
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_VRS_V20_DEEP_READ_2026-08-28.md
```

The PDF pin had already been committed at VRS V2.0 start in `audit_registry/pdf_source_pins_v0.1.json`.

## Next planned block

```text
VRS_V2.4
```

Required order:

1. byte-pin the official public V2.4 PDF;
2. fresh-read the V2.4 writing independently;
3. keep public PDF authority separate from candidate/integration XSD authority;
4. establish corrections/history of VRS-003 through VRS-009 from the V2.4 writing itself;
5. only then compare the existing candidate XSD (`07ff2c41731e63fd85b203e4b8e0186136caaaaf`);
6. do not promote candidate XSD to official authority merely because an official V2.4 PDF exists.

After VRS V2.4, continue with VDS V1.0 and resolve the deferred VideoDisplayService `v1.1` reference question.

No PR, merge, official branch, upstream branch or fork `master` action is authorized by this delta.
