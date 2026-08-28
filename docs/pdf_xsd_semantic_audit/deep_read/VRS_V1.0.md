# Deep Read - VideoRecordingService V1.0

Document id: `VRS_V1.0`

Status: `needs_visual_review`

Fresh-read date: 2026-08-28

## 1. Source and provenance

Official public writing:

```text
VDV-Schrift 301-2-12
VideoRecordingService
05/2017
https://www.vdv.de/301-2-12-sds.pdfx
```

Byte pin:

```text
SHA-256: 29d0bcb270fdab2119c4653296d4bca01e0f8b127eb9aaf393f66b2b34dcd390
size:    1,227,302 bytes
pin run: 33204215397
```

No VDV PDF bytes or rendered page images are committed to the repository.

## 2. Visual-review method

The document was reviewed textually first and then material layout-sensitive pages were rendered from the exact pinned source bytes with:

```text
tools/render_vdv_pdf_pages.py
docs/pdf_xsd_semantic_audit/PDF_VISUAL_RENDER_FALLBACK.md
```

Visual evidence run:

```text
33204547867
pages: 4, 42-46, 50-51
renderer: PyMuPDF 1.28.2
resolution: 180 dpi
```

The renderer verifies the pinned PDF SHA-256 and byte size before rendering. This is the audit fallback whenever the interactive screenshot backend is unavailable or returns `cache miss`.

## 3. Historical XSD/provenance result

The complete tree of the official upstream `VDV-301-1.0` tag was inspected.

It contains historical V1.0 Common/Enums, several V1.0 service XSDs and the monolithic `IBIS_IP_V1.0.xsd`, but no VideoRecordingService V1.0 service XSD.

The monolithic V1.0 root also contains no VideoRecordingService include or declaration.

In addition, the official repository commit history for the expected path:

```text
IBIS-IP_VideoRecordingService_V1.0.xsd
```

returns no commits.

Therefore:

```text
VRS V1.0 PDF authority: official public VDV writing
strict VRS V1.0 XSD authority: unresolved / no exact official V1.0 service XSD confirmed
VRS V2.0 or V2.4 XSD must not be substituted for V1.0
```

This strongly confirms `VRS-001` for the checked official repository history.

## 4. Service role and operation inventory

Visible page 42 lists the V1.0 operations as:

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

The table uses one common response type for the recording-control/state operations:

```text
VideoRecordingService.VideoRecordingStateResponseStructure
```

The subscription rows use the generic Common subscription request/response structures.

## 5. VideoRecordingStateResponse semantics

Visible page 43 says the proposal uses one response structure and shows `VideoRecordingService.VideoRecordingStateResponse` as a multi-field structure.

The table contains together:

```text
State
AlarmArchiveFillLevel
OperationErrorMessage
StartStopMode
```

This is independent historical PDF evidence for the grouped-state semantics later involved in `VRS-003` against the official V2.0 XSD.

Authority guard:

```text
VRS-003 executable scope remains official V2.0 XSD.
V1.0 provides semantic history only because no exact V1.0 service XSD is confirmed.
```

## 6. VRS-004 - SubscribeDisplayState / UnsubscribeDisplayState headings

Visible page 42 uses the operation names:

```text
SubscribeVideoRecordingState
UnsubscribeVideoRecordingState
```

Visible page 46 instead titles the detailed sections:

```text
Data structure of operation SubscribeDisplayState
Data structure of operation UnsubscribeDisplayState
```

This is a visually confirmed internal documentation naming inconsistency. No `SubscribeDisplayState` or `UnsubscribeDisplayState` operation alias is created.

Existing finding `VRS-004` is strengthened by pinned visual evidence.

## 7. VRS-006 - broken generated cross references

The same visible page 46 contains literal generated-document errors in both subscription paragraphs:

```text
Fehler! Verweisquelle konnte nicht gefunden werden..
```

The affected prose attempts to refer to Common subscription structure sections.

Classification:

```text
pdf_editorial_cross_reference_error_candidate
```

Validation impact: none. The generic Common subscription structures remain resolved from their actual selected authority, not from the broken page reference.

## 8. VRS-007 - invalid printed cardinality notation

Visible page 43 prints:

```text
State          -1:1
StartStopMode  -1:1
```

A leading negative minimum is not a meaningful ordinary IBIS-IP cardinality notation.

The audit does not guess the intended cardinality. The finding is limited to the visible invalid notation.

Because no exact VRS V1.0 XSD is confirmed, no PDF/XSD cardinality comparison is fabricated for V1.0.

## 9. VRS-008 - StopRecording section names StopRecordingERM

Visible page 45 is headed:

```text
3.5.4 Data structure of operation StopRecording
```

Its request subsection then states that no additional data must be supplied for operation:

```text
StopRecordingERM
```

The operation inventory on page 42 contains `StopRecording`, not `StopRecordingERM`.

Classification:

```text
pdf_operation_name_copy_paste_error_candidate
```

No `StopRecordingERM` routing alias is created.

## 10. VRS-009 - reference version label for VideoLiveService

Visible reference page 51 identifies VDV 301-2-11. The German line identifies VideoLiveService as `v1.0`, while the English line prints `VideoLiveService v1.1` alongside `1.0, 05/2017`.

The dedicated byte-pinned VLS V1.0 Deep Read independently established that VDV 301-2-11 is the official VideoLiveService V1.0 writing from 05/2017.

Therefore the English `v1.1` label is classified as a high-confidence reference/version-label documentation error.

The adjacent VideoDisplayService `v1.1` label remains only cross-document evidence until the dedicated VDS V1.0 read establishes its own document/version history.

## 11. Other visible document observations

Page 45 contains a correctly structured `PauseRecordingRRM` request table with `PauseInterval 1:1` and repeatedly points control operations back to the shared `VideoRecordingStateResponse`.

Page 50 contains the heading:

```text
Versionshistorie / Version History
```

but no visible entries. For a baseline publication this is not classified as a defect by itself.

The foreword on page 4 correctly identifies VDV 301-2-12 as the video recording service writing.

## 12. Relationship to later evidence

Only after completing the independent V1.0 read was the existing later evidence reintroduced:

```text
VRS-003 / EV-103:
official V2.0 XSD models the related response as xs:choice and rejects grouped PDF-shaped state responses.

V2.4 candidate control:
later candidate material groups the related state information differently and is explanatory only.
```

The V1.0 PDF shows that grouped state semantics were already present in the public writing before V2.0.

This does not retroactively create a V1.0 validation profile and does not promote V2.4 candidate material.

## 13. Fresh-read outcome

Existing findings strengthened:

```text
VRS-001  exact V1.0 XSD provenance gap strongly confirmed
VRS-003  V1.0 adds historical grouped-state semantic evidence; executable scope remains V2.0
VRS-004  SubscribeDisplayState / UnsubscribeDisplayState headings visually confirmed
```

New V1.0 findings:

```text
VRS-006  broken Word/generated cross-reference placeholders
VRS-007  invalid printed -1:1 cardinalities
VRS-008  StopRecording request prose says StopRecordingERM
VRS-009  English VDV 301-2-11 reference labels VideoLiveService v1.1 instead of v1.0
```

No XSD change is made.

## 14. Completion status

```text
textual fresh read: complete
exact source pin: complete
historical official repository XSD/provenance check: complete
targeted material visual checks: complete
all-page/all-figure visual pass: not complete
state: needs_visual_review
```

Next planned document: `VRS_V2.0`, using its own byte pin and the exact official V2.0 schema family. The V2.0 read must independently establish persistence/correction before reusing VRS-003 or later V2.4 candidate evidence.