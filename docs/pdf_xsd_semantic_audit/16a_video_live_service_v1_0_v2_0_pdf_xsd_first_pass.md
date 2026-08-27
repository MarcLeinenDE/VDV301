# VideoLiveService V1.0 / V2.0 PDF-XSD first pass

Status: semantic/provenance first pass completed. Local XSD compilation, XML sample validation and RTSP/media runtime checks remain pending.

Source starter:

```text
docs/pdf_xsd_semantic_audit/16_video_live_service_historical_start.md
```

## 1. Public-version mapping

### Public V1.0-era writing

```text
VDV 301-2-11
05/2017
VideoLiveService
```

It explicitly proposes video services as an extension of VDV301 Version 1.0.

No official release-tag `IBIS-IP_VideoLiveService_V1.0.xsd` was found in the checked tags. Therefore strict XSD validation for this public version remains unresolved.

### Public V2.0 writing

```text
VDV 301-2-11
08/2019
VideoLiveService V2.0
```

The foreword says this service is compatible with VDV301 Version 1.0 as well as 2.x. This compatibility statement is documentation evidence; it does not authorize the validator to map V1.0 traffic automatically to the V2.0 XSD.

Official V2.0 schema family:

```text
IBIS-IP_VideoLiveService_V2.0.xsd
-> IBIS-IP_common_V2.0.xsd
-> IBIS-IP_Enumerations_V2.0.xsd
```

## 2. Operation inventory

Both documents describe one IBIS-IP operation:

```text
ListAllLiveStreams
```

Request:

```text
no request payload data
```

Response concept:

```text
VideoLiveService.ListAllLiveStreamsResponseStructure
```

The V2.0 XSD exposes:

```text
VideoLiveService.ListAllLiveStreamsResponse
VideoLiveServiceGroup
```

with the same response structure.

No separate operation-name mismatch is opened.

## 3. Response wrapper

PDF response description presents:

```text
ListAllLiveStreamsData  1:*  VideoLiveService.LiveStreamData
OperationErrorMessage         IBIS-IP.string
```

The V2.0 XSD models a choice between repeated data and repeated error-message entries:

```text
xs:choice
  ListAllLiveStreamsData maxOccurs="unbounded"
  OperationErrorMessage maxOccurs="unbounded"
```

This is compatible with a success-data vs error-response interpretation and is not opened as a separate finding in this pass.

## 4. VLS-002 - LiveStreamData compositor mismatch

PDF V1.0 and V2.0 both describe the `LiveStreamData` structure as a stream-information record. The tables list the stream attributes together, with the main scalar attributes shown as required entries.

V2.0 XSD:

```xml
<xs:complexType name="VideoLiveService.LiveStreamData">
  <xs:choice>
    <xs:element name="StreamID" .../>
    <xs:element name="CameraName" .../>
    <xs:element name="CameraType" .../>
    <xs:element name="CameraCurrentState" .../>
    <xs:element name="rtspURI" .../>
    <xs:element name="VideoWidth" .../>
    <xs:element name="VideoHeight" .../>
    <xs:element name="VideoCodec" .../>
    <xs:element name="FramesPerSecond" .../>
    <xs:element name="Bitrate" .../>
    <xs:element name="Mirrored" .../>
    <xs:element name="Flipped" .../>
    <xs:element name="Rotation" .../>
    <xs:element name="Quality" .../>
  </xs:choice>
</xs:complexType>
```

Executable consequence:

```text
one LiveStreamData instance accepts exactly one choice alternative by default,
not the complete multi-field record described in the PDF.
```

Classification:

```text
mismatch_kind: compositor_or_structure_modelling
likely_source_issue: xsd_structure_modelling_error_candidate
classification_confidence: high
final_handling_bucket: local_validation_required + post_audit_official_schema_candidate_review
```

Why this is stronger than a cosmetic PDF mismatch:

```text
- both public document versions describe the same multi-field record semantics;
- stream identification and RTSP access logically require multiple fields together;
- the current official upstream master still contains the same xs:choice;
- no existing PR covering this issue was found in the repository PR search performed during this pass.
```

Validation authority remains the XSD until an official correction exists.

## 5. Enumerations

V2.0 XSD `VideoSourceCurrentStateEnumeration`:

```text
Connected
NoSync
NoETHConnection
```

Both checked PDF versions list the same values.

V2.0 XSD `VideoCodecEnumeration`:

```text
MJPEG
MPEG4
H264
H265
unknown
```

Both checked PDF versions list the same values.

No enumeration finding opened.

## 6. VLS-003 - V1.0 German foreword reference

V1.0 German foreword:

```text
VDV 301-2-1 describes the live video services.
```

V1.0 English foreword and V2.0 foreword identify:

```text
VDV 301-2-11
```

Classification:

```text
mismatch_kind: document_reference_number
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: high
version_scope: V1.0 PDF
```

The later document effectively provides historical correction evidence.

## 7. VLS-004 - VideoDisplayService in VideoLiveService start/stop section

Both documents contain a paragraph in the VideoLiveService start/stop procedure saying:

```text
To stop and/or restart the VideoDisplayService ...
```

The surrounding context is VideoLiveService and the immediately following note refers to START/STOP behavior for VideoLiveService and RTSP.

Classification:

```text
mismatch_kind: service_name_in_prose
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
version_scope: V1.0 and V2.0 PDFs
```

No executable alias or service-routing rule is derived from this prose typo.

## 8. Media/control boundary

The XSD describes discovery of live stream metadata, including `rtspURI`.

The actual live-video stream is not carried inside the IBIS-IP XML response. RTSP/RTP media behavior must be tested separately.

Future diagnostic layers:

```text
1. DNS-SD / VDV service discovery
2. HTTP/XML operation invocation and XSD validation
3. extracted rtspURI sanity/reachability
4. RTSP session/control behavior
5. media/RTP reception and stream characteristics
```

Success at one layer must not imply success at later layers.

## 9. Technical validation backlog

```text
VLS-VB-001: compile official VideoLiveService V2.0 + Common V2.0 + Enums V2.0.
VLS-VB-002: positive XSD sample with one LiveStreamData containing only StreamID, demonstrating current xs:choice behavior if accepted.
VLS-VB-003: negative/current-XSD sample containing StreamID + CameraName + rtspURI, demonstrating compositor conflict.
VLS-VB-004: build a PDF-intended complete LiveStreamData sample and record strict XSD result.
VLS-VB-005: positive/negative VideoCodecEnumeration samples.
VLS-VB-006: positive/negative VideoSourceCurrentStateEnumeration samples.
VLS-VB-007: runtime ListAllLiveStreams request/response test against a real implementation.
VLS-VB-008: separate RTSP URI reachability/session test.
VLS-VB-009: provenance assertion: public V1.0 remains no-strict-XSD-profile unless official release-tag material is found.
```

No task above has been executed during this audit block.
