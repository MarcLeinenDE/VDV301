# Audit handoff delta - VLS V1.0 Deep Read and pinned visual-render fallback

Date: 2026-08-28

Base clean HEAD before closeout:

```text
4daa21591c1d0c2b8c61944a8980bdaf131c7f23
```

## 1. Purpose

This delta closes the independent byte-pinned `VLS_V1.0` fresh read and records the new reproducible visual-render fallback introduced after repeated interactive PDF screenshot `cache miss` failures.

No XSD is changed by this delta.

## 2. Cache-miss diagnosis

Observed behavior:

```text
official VDV PDF reachable: yes
byte pin valid: yes
embedded/native PDF text readable: yes
interactive requested page screenshot: cache miss
```

Therefore the `cache miss` is treated as a screenshot/render-service cache failure, not a source-PDF failure and not a VDV documentation defect.

We cannot guarantee that the external interactive renderer will never return a cache miss. The audit no longer depends on it as the only visual path.

## 3. Permanent visual fallback

Permanent files introduced before this closeout:

```text
tools/render_vdv_pdf_pages.py
docs/pdf_xsd_semantic_audit/PDF_VISUAL_RENDER_FALLBACK.md
```

Permanent implementation commit:

```text
98987ab96d8a069e542bc11a7952996597a9e0e9
```

The renderer:

```text
- accepts only a registered source_id;
- resolves official URL + byte pin;
- verifies %PDF- signature;
- verifies SHA-256 + byte size before rendering;
- exits SOURCE_CHANGED_SINCE_AUDIT on mismatch;
- renders requested 1-based pages with PyMuPDF;
- records source metadata and per-PNG SHA-256 in render_manifest.json;
- keeps PDF/page-image bytes outside the public repository.
```

## 4. VLS V1.0 source pin

```text
source_id: VLS_V1.0
official URL: https://www.vdv.de/301-2-11-sds.pdfx
SHA-256: f535673427ff8f495102e1fc7723ca157408949b981572c4342b862f6d9c2a3c
size: 1,166,329 bytes
pin run: 33197955036
```

## 5. Visual fallback evidence

Render run 1:

```text
run: 33202961159
pages: 4, 39, 40, 41, 44
DPI: 180
engine: PyMuPDF 1.28.2
result: success
```

Render run 2:

```text
run: 33203162588
pages: 38, 45
DPI: 180
engine: PyMuPDF 1.28.2
result: success
```

Temporary render workflows were removed after evidence capture. The permanent renderer remains.

## 6. VLS V1.0 historical XSD provenance

The official upstream tag `VDV-301-1.0` was independently checked.

```text
tag commit: f5b53785f703e898632603eec3bfa3555a79fdba
tree: 729bbe3270e52fed3e0641466048a745d5a09b32
recursive tree: checked
IBIS_IP_V1.0.xsd: checked
VideoLiveService V1.0 service XSD: not found
VideoLiveService include/declaration in monolithic root: not found
```

Result:

```text
VLS V1.0 PDF authority = official public VDV writing
strict VLS V1.0 XSD authority = unresolved / no official release-tag service XSD confirmed
VLS V2.0 XSD substitution = forbidden
```

This confirms/strengthens `VLS-001`.

## 7. VLS V1.0 semantic findings

### VLS-002 historical strengthening

Visible V1.0 `LiveStreamData` is a multi-field stream record containing StreamID, camera metadata, rtspURI, dimensions, codec, frame rate, bitrate, transforms and quality together.

This strengthens the documented history behind `VLS-002`, but executable mismatch authority remains the official V2.0 XSD checked by EV-103.

### VLS-003 visually confirmed

Pinned page 4:

```text
German foreword -> VDV-Schrift 301-2-1 for live-video services
English foreword -> VDV 301-2-11
```

Classification remains documentation/document-number error; no resolver alias.

### VLS-004 visually confirmed

Pinned page 38 contains `VideoDisplayService` in the VideoLive start/stop procedure and immediately returns to VideoLive/RTSP semantics.

Classification: high-confidence copy/paste/service-name documentation error.

### VLS-005 new

Pinned pages 39-40 visibly print malformed cardinality-like strings:

```text
ListAllLiveStreamsData  -1:*
CameraCurrentState      -1:1
VideoCodec              -1:1
```

The intended values are deliberately not guessed. No V1.0 schema rule is synthesized.

## 8. Deferred cross-document item

Page 45 contains ambiguous VRS/VDS version-label strings. They are retained for the independent `VRS_V1.0` and `VDS_V1.0` Deep Reads and are not classified from VLS alone.

## 9. Completion status

```text
VLS_V1.0 textual fresh read: complete
byte pin: complete
historical XSD provenance: complete
targeted visual material findings: complete
all-page/all-figure visual pass: not complete
state: needs_visual_review
```

## 10. Next step

Proceed to `VLS_V2.0`:

```text
1. byte-pin official VLS V2.0 PDF;
2. fresh-read it as its own document;
3. use pinned-byte rendering where interactive screenshots miss;
4. compare against exact official V2.0 XSD -> Common V2.0 -> Enumerations V2.0;
5. re-check VLS-002 and persistence/correction of VLS-004/VLS-005;
6. compare to RV-004 only after the independent V2.0 read.
```

No PR/mail/upstream disposition is decided during this Deep Read.
