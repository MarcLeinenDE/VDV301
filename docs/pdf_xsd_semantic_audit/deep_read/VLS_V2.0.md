# Deep Read - VideoLiveService V2.0

Document id: `VLS_V2.0`

Status: `needs_visual_review`

Fresh-read date: 2026-08-28

## 1. Source and authority

Official public writing:

```text
VDV-Schrift 301-2-11
VideoLiveService V2.0
08/2019
https://www.vdv.de/301-2-11-sdes-v2-0-video-live-service.pdfx
```

Byte pin:

```text
SHA-256: d75a543c138f21c4ad370925ca7f306bcde7d692ce793ddc1d51bdcf6032787b
size:    1,218,788 bytes
pin run: 33203673347
```

Exact XML authority:

```text
VDVde/VDV301 tag: VDV-301-2.0
IBIS-IP_VideoLiveService_V2.0.xsd
-> IBIS-IP_common_V2.0.xsd
-> IBIS-IP_Enumerations_V2.0.xsd
service XSD blob: d8c52f5de9ef3f5915524fef12da11eabf0ca041
```

The file in the integration branch matches the exact official-tag V2.0 service XSD. No nearby or later schema is substituted.

## 2. Visual review and cache-miss fallback

The interactive PDF screenshot backend again returned `cache miss` for requested V2.0 pages even though the PDF source was reachable and byte-pinned.

The permanent pinned-byte fallback was used:

```text
tools/render_vdv_pdf_pages.py
policy: docs/pdf_xsd_semantic_audit/PDF_VISUAL_RENDER_FALLBACK.md
render run: 33203850390
engine: PyMuPDF 1.28.2
DPI: 180
pages: 4, 35, 36, 37, 41
result: success
```

The render manifest verified the exact VLS V2.0 PDF SHA-256 and byte size before creating page images.

This independently confirms that the external screenshot `cache miss` is not a failure of the VDV source.

## 3. Foreword / document identity

V2.0 identifies itself consistently as VDV 301-2-11.

Visible page 4 says in both language sections that the VideoLiveService is VDV 301-2-11 and that the service is compatible with VDV301 version 1.0 and 2.x.

Historical result:

```text
VLS-003 (V1.0 German foreword says 301-2-1): corrected in V2.0.
```

The correction is documentation history only and does not alter V1.0's published text.

## 4. Service and protocol boundary

The V2.0 writing states that service advertisement follows VDV301 DNS-SD rules and mentions TCP, UDP and HTTP for data transmission. RTP and RTSP are used for real-time video data.

The live-stream information carries an `rtspURI`. The writing explicitly says a dedicated VideoLive START/STOP operation is not required because these operations belong to RTSP communication.

Therefore the fresh read independently confirms the architecture later encoded in RV-004:

```text
VDV discovery / HTTP / XML metadata
!= RTSP control plane
!= RTP/RTCP media plane
```

No particular newer RTSP RFC/version is made normative merely because it is newer.

## 5. Operation inventory

The writing documents one VideoLiveService operation:

```text
ListAllLiveStreams
request payload: none
response: VideoLiveService.ListAllLiveStreamsResponseStructure
```

The response is intended to provide information about the available video sources/live streams and error information.

## 6. VLS-004 persists in V2.0

Visible page 35, inside `3.4.2 System start/stop procedure`, states that the operation of `VideoLiveService` can be used and then says that to stop/restart the `VideoDisplayService`, DeviceManagementService operations shall be used.

Immediately afterwards the note returns to `VideoLiveService` and says a dedicated START/STOP operation is unnecessary because RTSP provides the function.

Result:

```text
VLS-004 persists visibly in V2.0.
classification remains documentation/copy-paste service-name error.
no VideoDisplayService alias or routing rule is created.
```

## 7. Response table and VLS-005 persistence

Visible page 36 prints:

```text
ListAllLiveStreamsData   -1:*   VideoLiveService.LiveStreamData
OperationErrorMessage            IBIS-IP.string
```

Visible page 37 prints the multi-field `VideoLiveService.LiveStreamData` table and includes:

```text
StreamID            1:1
CameraName          1:1
CameraType          1:1
CameraCurrentState -1:1
rtspURI             1:1
VideoWidth          1:1
VideoHeight         1:1
VideoCodec         -1:1
FramesPerSecond     1:1
Bitrate             1:1
Mirrored            1:1
Flipped             1:1
Rotation            1:1
Quality             1:1
```

Thus `VLS-005` persists visibly from V1.0 into V2.0.

The exact V2.0 XSD gives `ListAllLiveStreamsData` `maxOccurs="unbounded"` with default `minOccurs=1`, and the two enum fields have default one occurrence within the selected choice alternative. This is compatible with interpreting the printed leading hyphen as an editorial notation defect, but the audit does not silently rewrite the PDF text.

Important distinction:

```text
VLS-005 = malformed printed cardinality notation.
VLS-002 = separate structural/compositor mismatch caused by xs:choice.
```

## 8. VLS-002 fresh PDF/XSD confirmation

The V2.0 PDF visibly presents `LiveStreamData` as one table/record containing the full set of stream fields together.

The exact official V2.0 XSD defines:

```text
VideoLiveService.LiveStreamData -> xs:choice over the individual fields
```

and also models the response as an `xs:choice` between repeated stream data and repeated error messages.

Existing EV-103 already executed the selected exact V2.0 family:

```text
run: 33111119723
one LiveStreamData containing only StreamID: valid
StreamID + CameraName + rtspURI: rejected
complete PDF-shaped multi-field LiveStreamData: rejected
```

Fresh-read result:

```text
VLS-002 remains executable-confirmed.
The V2.0 PDF and exact V2.0 XSD describe observably different structure semantics.
No XSD is changed automatically.
```

## 9. Enumeration values

The PDF lists:

```text
VideoSourceCurrentStateEnumeration:
Connected
NoSync
NoETHConnection

VideoCodecEnumeration:
MJPEG
MPEG4
H264
H265
unknown
```

The exact official V2.0 service XSD contains the same enum spellings. No fresh enum-value mismatch was identified in this pass.

## 10. References / cross-document follow-up

The V2.0 reference section still contains the neighboring video-document version strings resembling:

```text
VideoRecordingService v1.1, 1.0, 05/2017
VideoDisplayService v1.1 1.0, 05/2017
```

As with V1.0, these remain cross-document follow-up evidence for the independent `VRS_V1.0` and `VDS_V1.0` Deep Reads. Their meaning is not guessed from the VLS document alone.

## 11. Comparison to V1.0

```text
VLS-001: V1.0 provenance gap only; V2.0 has exact official service XSD.
VLS-002: V1.0 supplies historical multi-field semantics; V2.0 has executable PDF/XSD xs:choice mismatch.
VLS-003: corrected in V2.0 foreword.
VLS-004: persists visibly in V2.0.
VLS-005: persists visibly in V2.0.
```

## 12. Runtime comparison after fresh read

After the independent PDF/XSD read, RV-004 was consulted. It remains consistent with the selected V2.0 writing:

```text
rtspURI metadata does not prove media availability;
VDV XML metadata, RTSP control and RTP/RTCP media remain separate layers;
VideoLive START/STOP XML operations are not synthesized;
newer RTSP versions are not latest-wins replacements for the historical VDV profile.
```

No RV-004 correction is required from this V2.0 fresh read.

## 13. Completion

```text
textual fresh read: complete
source pin: complete
exact official V2.0 XSD family: confirmed
targeted visual material pages: complete
existing EV-103 comparison: complete after fresh read
RV-004 comparison: complete after fresh read
new finding IDs: none
finding history updates: VLS-002, VLS-003, VLS-004, VLS-005
all-page/all-figure visual pass: not complete
state: needs_visual_review
```

Next planned document: `VRS_V1.0`.
