# Block 25e / RV-004 - VideoLive RTSP/RTP boundary

Status: deterministic RTSP/RTP boundary classifier implemented and executable-tested. No live camera, RTSP endpoint or media stream was contacted.

## Evidence run

```text
GitHub Actions run: 33119694991
run number: 14
head tested: 7c3cbe9f56cce37432f73c83699ba35eabc64465
job: 98683189500
environment: Ubuntu 24.04.4 / Python 3.12.14 / lxml 6.1.2
video_runtime_status: 0 / PASS
```

The run also re-confirmed all previous EV and RV-001..RV-003 checks with status 0.

## Reusable implementation

```text
tools/runtime_video_profile.py
tools/validate_video_runtime_rv004.py
```

The implementation is intentionally network-independent and separates:

```text
VDV service discovery / HTTP / XML metadata
rtspURI and RTSP control plane
RTP/RTCP media plane
```

A successful result in one layer does not imply success in the next.

## VDV VideoLive boundary

The checked VideoLive profile exposes stream metadata including `rtspURI`. Stream control is delegated to RTSP rather than a synthetic VideoLive XML START/STOP operation.

Executable architecture guards confirm:

```text
valid XML stream metadata does not imply media availability
VideoLive START/STOP XML operations are not synthesized
validation layers remain separately addressable:
  vdv_discovery_and_http_xml
  rtsp_uri_and_control
  rtp_rtcp_media
```

## rtspURI deterministic checks

Cases:

```text
rtsp://camera.example/live/1 -> PASS
missing rtspURI              -> detected
http://... in rtspURI        -> detected
rtsp URI without host        -> detected
```

Authority is deliberately split:

```text
VDV: stream metadata supplies rtspURI / RTSP access boundary
external RTSP URI semantics: URI parsing and absolute-resource form
```

The deterministic profile uses the ordinary `rtsp` scheme. It does not infer support for other RTSP URI schemes merely because later external RTSP standards define them.

## RTSP version handling

The checked VDV writing names RTSP but does not, in the current audit evidence, pin a specific RTSP RFC/version.

Therefore the SDK rule is:

```text
record observed RTSP version
never report RTSP/2.0 as a VDV requirement solely because RFC 7826 is newer
never assume RTSP/2.0 is a drop-in replacement for RTSP/1.0
```

External standards tracked:

```text
RFC 2326 -> RTSP 1.0
RFC 7826 -> RTSP 2.0, obsoletes RTSP 1.0 but is not backwards compatible except basic version negotiation
```

Executable request/status-line cases:

```text
RTSP/1.0 absolute request line -> PASS
RTSP/2.0 absolute request line -> PASS
RTSP/2.0 OPTIONS *             -> PASS
relative Request-URI           -> detected
RTSP/1.0 response line         -> PASS
RTSP/2.0 response line         -> PASS
505 Version Not Supported      -> parseable negotiation evidence
```

Compatibility cases:

```text
RTSP/1.0 request -> RTSP/1.0 response -> PASS
RTSP/1.0 request -> RTSP/2.0 response -> detected as invalid version upgrade
RTSP/2.0 request -> RTSP/2.0 response -> PASS
RTSP/2.0 request -> RTSP/1.0 505      -> retained as negotiation evidence, not latest-wins success
```

## RTP RFC 3550 boundary

External authority:

```text
RFC 3550
```

Deterministic parser checks the fixed RTP header fields:

```text
version
padding flag
extension flag
CSRC count
marker
payload type
sequence number
timestamp
SSRC
```

Executable results:

```text
minimal 12-byte RTP header parses                  PASS
sequence/timestamp/SSRC extraction                 PASS
RTP version 2                                      PASS
RTP version other than 2                           detected
packet shorter than 12-byte fixed header           detected
CC=2 with two CSRCs -> 20-byte header              PASS
CC declares CSRCs but bytes are missing             detected
```

This confirms only packet-header classification. It does not prove codec correctness, jitter quality or stream continuity.

## Authority / latest-wins guard

The runtime validator must preserve three separate facts:

```text
VDV says where RTSP enters the VideoLive workflow.
RTSP standards define control protocol behavior.
RTP standards define media transport packet behavior.
```

A newer external RFC does not silently rewrite the historical VDV profile.

## What RV-004 does NOT claim

Not executed:

```text
real ListAllLiveStreams operation against a provider device
real rtspURI reachability
TCP connection to RTSP endpoint
OPTIONS/DESCRIBE/SETUP/PLAY/PAUSE/TEARDOWN sequence
SDP validation
authentication
RTP socket/media reception
RTCP reception
packet-loss/jitter/sequence continuity
codec decoding
resolution/frame-rate/bitrate verification
multicast vs unicast media-path behavior
```

Those remain live integration tasks.

## Result

```text
RV-004 deterministic Video RTSP/RTP boundary: PASS
```

## Phase boundary

With RV-004, the planned deterministic runtime/protocol evidence sequence is complete:

```text
RV-001 HTTP/XML + Content-Type
RV-002 DNS-SD/service discovery
RV-003 TimeService/SNTP
RV-004 Video RTSP/RTP boundary
```

Next phase:

```text
live/integration validation backlog consolidation
then central audit handoff/findings/backlog/index consolidation
then SDK implementation baseline
```
