# Deep Read - VideoLiveService V1.0

Document id: `VLS_V1.0`

Status: `needs_visual_review`

Fresh-read date: 2026-08-28

## 1. Source and provenance

Official public writing:

```text
VDV-Schrift 301-2-11
VideoLiveService
05/2017
https://www.vdv.de/301-2-11-sds.pdfx
```

Byte pin:

```text
SHA-256: f535673427ff8f495102e1fc7723ca157408949b981572c4342b862f6d9c2a3c
size:    1,166,329 bytes
pin run: 33197955036
```

The source is an official public VDV writing. No VDV PDF bytes or rendered page images are committed to the repository.

## 2. Visual-review method and cache-miss resolution

The interactive PDF screenshot backend returned `cache miss` for the requested VLS pages even though the PDF was reachable and byte-pinned.

The audit therefore used the pinned-byte fallback defined in:

```text
tools/render_vdv_pdf_pages.py
docs/pdf_xsd_semantic_audit/PDF_VISUAL_RENDER_FALLBACK.md
```

GitHub Actions rendered the exact pinned PDF bytes with PyMuPDF 1.28.2 at 180 dpi.

Visual evidence runs:

```text
33202961159  pages 4, 39, 40, 41, 44
33203162588  pages 38, 45
```

The render manifests verified the source SHA-256 and byte size before rendering and recorded per-PNG SHA-256 values.

Important result:

```text
interactive screenshot cache miss != source failure
```

The fallback produced readable visible pages from the exact source bytes. This removes the external screenshot cache from the critical path of the audit.

## 3. Historical XSD/provenance result

The official upstream tag `VDV-301-1.0` resolves to commit:

```text
f5b53785f703e898632603eec3bfa3555a79fdba
```

Its complete tree was inspected. It contains the historical V1.0 Common/Enums and multiple service XSDs plus `IBIS_IP_V1.0.xsd`, but no `IBIS-IP_VideoLiveService_V1.0.xsd` or equivalent VideoLive service XSD.

The monolithic `IBIS_IP_V1.0.xsd` includes the available V1.0 service files but does not include or declare VideoLiveService.

Therefore:

```text
VLS V1.0 public PDF authority: official public VDV writing
strict VLS V1.0 XSD authority: unresolved / no official release-tag service XSD confirmed
VLS V2.0 XSD must NOT be substituted for V1.0
```

This confirms existing finding `VLS-001` for the checked official release-tag provenance.

## 4. Service role and protocol boundary

The writing describes VideoLiveService as the source of information about available live picture/video sources and their parameters.

It identifies RTSP/RTP as the media/control protocol lane and states that the RTSP URI is carried in the live-stream data. It explicitly says a dedicated VideoLive `START` or `STOP` operation is not required because those actions belong to RTSP communication.

The VDV XML/service operation lane is therefore separate from the external RTSP/RTP media lane.

No later RTSP version is silently made normative for this historical writing.

## 5. Operation inventory

The writing exposes one VideoLiveService operation:

```text
ListAllLiveStreams
request: no payload
response: VideoLiveService.ListAllLiveStreamsResponseStructure
```

The operation is intended to return information for all available live sources/streams.

This is consistent with the architectural rule already used by RV-004: VideoLive XML metadata and RTSP/RTP media operation are separate layers.

## 6. Response and LiveStreamData semantics

The visible page 39 response table contains:

```text
ListAllLiveStreamsData   printed cardinality: -1:*
OperationErrorMessage    IBIS-IP.string
```

The visible page 40 `VideoLiveService.LiveStreamData` table presents one stream as a multi-field record containing together, among other fields:

```text
StreamID
CameraName
CameraType
CameraCurrentState
rtspURI
VideoWidth
VideoHeight
VideoCodec
FramesPerSecond
Bitrate
Mirrored
Flipped
Rotation
Quality
```

This is strong historical PDF evidence for the multi-field semantics already involved in `VLS-002` when the official V2.0 XSD is evaluated.

Authority guard:

```text
The V1.0 PDF strengthens the documented semantic history.
It does not create a missing V1.0 XSD and it does not make the V2.0 XSD normative for V1.0.
```

## 7. VLS-002 historical strengthening

The later official V2.0 XSD models `VideoLiveService.LiveStreamData` as one `xs:choice` over the individual fields. EV-103 executable evidence already proves that one selected field validates while a PDF-shaped multi-field record fails.

The fresh V1.0 read independently establishes that the multi-field record concept predates V2.0.

Result:

```text
VLS-002 remains scoped to executable V2.0 XSD behavior.
V1.0 is historical semantic evidence only because no exact official V1.0 service XSD is confirmed.
```

## 8. Confirmed documentation findings

### VLS-003 - wrong part number in German foreword

Visible page 4 states:

```text
Die VDV-Schrift 301-2-1 beschreibt die live Video-Dienste.
```

The adjacent English foreword correctly states `VDV 301-2-11`.

This is visually confirmed from the byte-pinned source.

### VLS-004 - VideoDisplayService in VideoLive start/stop prose

Visible page 38 contains the VideoLive start/stop sequence and then says:

```text
To stop and/or restart the VideoDisplayService ...
```

The following note immediately returns to VideoLiveService and explains that a dedicated VideoLive START/STOP operation is unnecessary because RTSP supplies this function.

The service-name substitution is therefore a high-confidence copy/paste/documentation error. No VideoDisplay alias or routing rule is created from this sentence.

### VLS-005 - invalid printed cardinality notation

Visible pages 39 and 40 print cardinality-like strings that are not valid ordinary IBIS-IP cardinality notation:

```text
ListAllLiveStreamsData  -1:*
CameraCurrentState      -1:1
VideoCodec              -1:1
```

The fresh read does not guess whether the intended values were `1:*`, `0:1`, or another form. The finding is limited to the visible fact that the publication prints the leading-hyphen forms.

Native text of the later V2.0 writing shows the same strings, so persistence into V2.0 is queued for its own pinned visual Deep Read rather than assumed here.

## 9. Reference/version-label follow-up

Visible page 45 references the neighboring video writings with strings including:

```text
VideoRecordingService v1.1, 1.0, 05/2017
VideoDisplayService v1.1 1.0, 05/2017
```

These labels are ambiguous. They are retained as a cross-document follow-up for the dedicated VRS V1.0 and VDS V1.0 Deep Reads. No new defect is opened here because the intended relation between document revision and service version has not yet been independently established.

## 10. Version history

Page 44 contains the heading `Versionshistorie / Version History` but no visible entries.

For a baseline V1.0 publication this is not classified as a defect by itself.

## 11. Fresh-read outcome

Existing findings:

```text
VLS-001 confirmed/strengthened
VLS-002 historically strengthened; executable authority remains V2.0 only
VLS-003 visually confirmed
VLS-004 visually confirmed
```

New finding:

```text
VLS-005 invalid printed cardinality notation (-1:* / -1:1)
```

No XSD change is made.

## 12. Completion status

```text
textual fresh read: complete
exact source pin: complete
historical official-tag XSD provenance check: complete
targeted visual checks: complete for material findings
all-page/all-figure visual pass: not complete
state: needs_visual_review
```

The next planned document is `VLS_V2.0`, using its own byte pin and exact official V2.0 XSD family. Only there will the V2.0 PDF/XSD compositor relationship be re-read as the selected version's own evidence.
