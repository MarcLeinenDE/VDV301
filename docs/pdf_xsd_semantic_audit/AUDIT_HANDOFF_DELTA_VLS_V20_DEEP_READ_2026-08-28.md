# Audit handoff delta - VLS V2.0 Deep Read

Date: 2026-08-28

## 1. Source

```text
source_id: VLS_V2.0
publication: VDV-Schrift 301-2-11, VideoLiveService V2.0, 08/2019
official URL: https://www.vdv.de/301-2-11-sdes-v2-0-video-live-service.pdfx
SHA-256: d75a543c138f21c4ad370925ca7f306bcde7d692ce793ddc1d51bdcf6032787b
size: 1,218,788 bytes
pin run: 33203673347
```

## 2. Exact XSD authority

```text
official tag: VDV-301-2.0
service XSD: IBIS-IP_VideoLiveService_V2.0.xsd
blob: d8c52f5de9ef3f5915524fef12da11eabf0ca041
dependencies: Common V2.0 + Enumerations V2.0
```

No nearby schema substitution is used.

## 3. Visual fallback

Interactive screenshots again returned `cache miss` for requested V2.0 pages. The exact pinned PDF was rendered with the permanent fallback.

```text
render run: 33203850390
engine: PyMuPDF 1.28.2
DPI: 180
pages: 4, 35, 36, 37, 41
result: success
```

The temporary render workflow was removed after evidence capture.

## 4. Finding history

```text
VLS-002: fresh V2.0 PDF/XSD read reconfirms the multi-field PDF vs xs:choice mismatch. EV-103 remains executable proof.
VLS-003: corrected in V2.0; both language forewords use 301-2-11.
VLS-004: persists visibly in V2.0 page 35.
VLS-005: persists visibly in V2.0 pages 36-37.
```

No new finding ID was required.

## 5. VLS-005 nuance

The visible PDF prints:

```text
ListAllLiveStreamsData  -1:*
CameraCurrentState      -1:1
VideoCodec              -1:1
```

The exact XSD has a repeated ListAllLiveStreamsData branch and one occurrence for the two enum fields within the selected choice. A stray leading hyphen is therefore a plausible editorial explanation, but the publication is not silently rewritten.

`VLS-005` remains a documentation-notation finding, distinct from the executable `VLS-002` compositor discrepancy.

## 6. EV-103

Existing executable evidence remains valid and directly matches the fresh selected authority:

```text
run: 33111119723
single StreamID LiveStreamData: valid
StreamID + CameraName + rtspURI: rejected
complete PDF-shaped multi-field LiveStreamData: rejected
```

No new executable test is necessary to preserve `VLS-002`.

## 7. RV-004

After the independent V2.0 read, RV-004 was compared and remains consistent:

```text
rtspURI metadata != RTSP endpoint availability
VDV XML metadata != RTSP control != RTP/RTCP media
no synthetic VideoLive XML START/STOP operation
no latest-RTSP-version-wins behavior
```

RV-004 run `33119694991` remains current for this boundary.

## 8. Cross-document follow-up

The VLS V1.0/V2.0 reference sections contain ambiguous VideoRecordingService/VideoDisplayService version strings around `v1.1, 1.0`. These remain unclassified until the independent `VRS_V1.0` and `VDS_V1.0` Deep Reads.

## 9. Completion

```text
VLS_V2.0 textual fresh read: complete
source pin: complete
exact XSD family: complete
targeted visible review: complete
EV-103 comparison: complete after fresh read
RV-004 comparison: complete after fresh read
all-page/all-figure visual review: not complete
state: needs_visual_review
```

## 10. Next

Proceed to `VRS_V1.0` with a new source pin and independent fresh read.

No XSD, master branch, PR, comment, merge or upstream branch is modified by this closeout.
