# VideoLiveService validation backlog addendum

Status: technical validation pending.

## VLS-VB-001 - compile official V2.0 family

```text
IBIS-IP_VideoLiveService_V2.0.xsd
IBIS-IP_common_V2.0.xsd
IBIS-IP_Enumerations_V2.0.xsd
```

## VLS-VB-002 - demonstrate current LiveStreamData choice semantics

Positive candidate against current XSD:

```text
one LiveStreamData containing only StreamID
```

Goal: confirm the current `xs:choice` behavior rather than assuming it from inspection alone.

## VLS-VB-003 - multi-field negative sample

Build a `LiveStreamData` containing at least:

```text
StreamID
CameraName
rtspURI
```

and record strict V2.0 XSD result.

## VLS-VB-004 - PDF-intended full record sample

Build a representative record with all documented fields and record strict XSD result. This is the main technical gate for VLS-002.

## VLS-VB-005 - enumeration tests

Positive values:

```text
VideoCodecEnumeration: MJPEG MPEG4 H264 H265 unknown
VideoSourceCurrentStateEnumeration: Connected NoSync NoETHConnection
```

Add unsupported-value negative samples.

## VLS-VB-006 - ListAllLiveStreams runtime operation

Invoke a real implementation and capture:

```text
HTTP status/content type
XML payload
XSD result
number of returned stream entries
```

## VLS-VB-007 - RTSP/media layer

For each returned `rtspURI`, test separately:

```text
URI parsing
endpoint reachability
RTSP session establishment
media reception where permitted
```

Do not conflate XML validity with media availability.

## VLS-VB-008 - public V1.0 provenance guard

Ensure the SDK reports `strict_xsd_profile_unresolved` rather than routing V1.0 to V2.0 when no official release-tag V1.0 schema pool is installed.

No task in this addendum has been executed yet.
