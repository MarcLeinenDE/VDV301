# Audit handoff delta - VideoRecordingService V1.0 Deep Read

Date: 2026-08-28

Branch: `dev/schema-integration`

## Scope completed

Completed the byte-pinned independent Deep Read for:

```text
VRS_V1.0
VDV-Schrift 301-2-12
VideoRecordingService
05/2017
```

No XSD was changed.

## Source pin

```text
source_id: VRS_V1.0
official URL: https://www.vdv.de/301-2-12-sds.pdfx
SHA-256: 29d0bcb270fdab2119c4653296d4bca01e0f8b127eb9aaf393f66b2b34dcd390
size: 1,227,302 bytes
pin run: 33204215397
```

## Visual evidence

Pinned-byte render fallback run:

```text
33204547867
pages: 4, 42-46, 50-51
PyMuPDF 1.28.2
180 dpi
```

The temporary workflow used to produce the render artifact was removed again. The permanent renderer and fallback policy remain unchanged.

Targeted material visual evidence is complete. An all-page/all-figure visual pass is not complete, so the registry state remains `needs_visual_review`.

## Historical V1.0 XSD provenance

Checked official repository evidence:

```text
complete VDV-301-1.0 tag tree
IBIS_IP_V1.0.xsd
commit history for IBIS-IP_VideoRecordingService_V1.0.xsd
```

Result:

```text
no exact official VRS V1.0 service XSD confirmed
expected V1.0 service-XSD path has no commits
monolithic V1.0 root contains no VideoRecordingService
```

Therefore VRS V1.0 remains fail-closed for strict XSD routing. Do not substitute V2.0 or candidate V2.4.

## Existing finding updates

### VRS-001

Strongly confirmed exact-schema provenance gap for V1.0.

### VRS-003

Fresh V1.0 PDF independently shows `VideoRecordingStateResponse` as one grouped multi-field structure containing:

```text
State
AlarmArchiveFillLevel
OperationErrorMessage
StartStopMode
```

This strengthens semantic history only. Executable authority for VRS-003 remains official V2.0 and EV-103.

### VRS-004

Visually confirmed in V1.0:

```text
operation inventory:
SubscribeVideoRecordingState
UnsubscribeVideoRecordingState

section headings:
SubscribeDisplayState
UnsubscribeDisplayState
```

No DisplayState alias is created.

## New V1.0 findings

### VRS-006

Both subscription detail paragraphs visibly contain:

```text
Fehler! Verweisquelle konnte nicht gefunden werden..
```

Classification: generated/editorial PDF cross-reference failure. No validation impact.

### VRS-007

The state-response table visibly prints:

```text
State          -1:1
StartStopMode  -1:1
```

Classification: invalid printed cardinality notation. The intended value is not guessed.

### VRS-008

The `StopRecording` request subsection says no data is required for `StopRecordingERM`, while the operation inventory contains `StopRecording` and no `StopRecordingERM`.

Classification: operation-name copy/paste documentation error. No alias is created.

### VRS-009

The references page labels VDV 301-2-11 in English as `VideoLiveService v1.1`, while the German line says `v1.0` and the dedicated pinned VLS V1.0 Deep Read establishes VDV 301-2-11 as VideoLiveService V1.0, 05/2017.

Classification: reference/version-label documentation error.

The adjacent `VideoDisplayService v1.1` label remains deferred to the dedicated VDS V1.0 Deep Read.

## V1.0 version history

The visible page 50 contains only the heading `Versionshistorie / Version History` and no entries. This is not classified as a defect by itself for a baseline publication.

## Files to be updated in the closure commit

```text
00_START_HERE/CURRENT_STATE.json
audit_registry/deep_read_findings_delta_vrs_v10_2026-08-28.json
audit_registry/deep_read_registry_delta_vrs_v10_2026-08-28.json
docs/pdf_xsd_semantic_audit/VIDEO_RECORDING_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/deep_read/VRS_V1.0.md
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_VRS_V10_DEEP_READ_2026-08-28.md
```

## Next planned block

```text
VRS_V2.0
```

Required order:

1. byte-pin the official VRS V2.0 PDF;
2. fresh-read V2.0 independently;
3. establish the exact official V2.0 schema family from its own provenance;
4. visually check the shared state-response structure and persistence/correction of VRS-004/VRS-006/VRS-007/VRS-008;
5. only then reintroduce EV-103 / VRS-003 executable evidence and the V2.4 candidate correction history;
6. do not change XSD merely because PDF and XSD disagree.

No PR, merge, upstream branch, official PR branch or fork `master` action is authorized by this delta.
