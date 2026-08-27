# VideoLiveService V1.0 / V2.0 historical audit start

Status: public-version provenance and V2.0 official schema family resolved. V1.0 has no eligible official-release-tag XSD backfill in the checked tags. Local XSD/sample/media validation remains pending.

Working branch base:

```text
MarcLeinenDE/VDV301 dev/schema-integration
fb6c7c8f2720d34d5b64c8981d96c40ce58dcfaf
```

Scope:

```text
VDV 301-2-11 VideoLiveService, 05/2017 (public V1.0-era writing)
VDV 301-2-11 VideoLiveService V2.0, 08/2019
VDVde/VDV301 official release tags VDV-301-1.0, VDV-301-2.0, VDV-301-2.1, VDV-301-2.3
IBIS-IP_VideoLiveService_V2.0.xsd
IBIS-IP_common_V2.0.xsd
IBIS-IP_Enumerations_V2.0.xsd
```

## 1. V1.0 public document / schema provenance

The public 05/2017 VideoLiveService writing describes an extension of VDV301 Version 1.0 with the video-service component and specifies the `ListAllLiveStreams` operation and `LiveStreamData` structure.

No file named:

```text
IBIS-IP_VideoLiveService_V1.0.xsd
```

was found in the checked official release tags:

```text
VDV-301-1.0
VDV-301-2.0
VDV-301-2.1
VDV-301-2.3
```

Therefore the historical-backfill policy does not permit creating/backfilling a V1.0 service XSD from a fork, PR, inferred schema or later V2.0 file.

### VLS-001 candidate

```text
state: public-document-known / strict-XSD-routing unresolved
mismatch_kind: schema_family_or_provenance_gap
classification_confidence: high for checked official release tags
validation_behavior: do not silently map public V1.0 to VideoLiveService V2.0 XSD
```

## 2. V2.0 official provenance

Official source:

```text
VDVde/VDV301 tag VDV-301-2.0
IBIS-IP_VideoLiveService_V2.0.xsd
blob d8c52f5de9ef3f5915524fef12da11eabf0ca041
```

The file in `dev/schema-integration` has the identical blob SHA.

Explicit dependencies:

```text
IBIS-IP_common_V2.0.xsd
IBIS-IP_Enumerations_V2.0.xsd
```

Strict V2.0 XML family:

```text
VideoLiveService V2.0
-> Common V2.0
-> Enumerations V2.0
```

Current upstream `master` still contains the same V2.0 blob.

## 3. Service/media split

The VDV writing separates control/information semantics from actual media streaming:

```text
IBIS-IP XML operation: ListAllLiveStreams
stream access information: rtspURI and stream metadata
actual stream control/transport context: RTSP/RTP
```

The writing explicitly notes that dedicated START/STOP operations are not required for the live stream because these operations are part of RTSP communication/protocol behavior.

SDK implication:

```text
XML/XSD validation and media-protocol validation must be separate lanes.
A valid ListAllLiveStreams XML response does not prove that the RTSP stream is reachable/usable.
```

## 4. Candidate structural mismatch

### VLS-002 - LiveStreamData PDF record vs XSD xs:choice

Both public writings describe one `LiveStreamData` entry with a set of stream attributes including:

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

The V2.0 XSD defines `VideoLiveService.LiveStreamData` with an `xs:choice` containing those elements.

With default XSD occurrence rules, one LiveStreamData instance can contain only one of those alternatives, not the complete record described by the PDF.

Initial classification:

```text
mismatch_kind: compositor_or_structure_modelling
likely_source_issue: xsd_structure_modelling_error_candidate
classification_confidence: high
validation_behavior: selected XSD remains authority until any official correction; full PDF-style record is expected to fail strict XSD validation
```

No XSD is changed during this audit.

## 5. Documentation candidates

### VLS-003 - V1.0 German foreword document number

The V1.0 German foreword says VDV 301-2-1 describes the live video services, while the English foreword correctly names VDV 301-2-11. The V2.0 writing uses 301-2-11 consistently.

```text
classification: pdf_label_or_heading_error_candidate
confidence: high
```

### VLS-004 - VideoDisplayService name in VideoLiveService start/stop paragraph

Both V1.0 and V2.0 writings state in the VideoLiveService system-start/stop section that `VideoDisplayService` should be stopped/restarted, immediately before a note explaining that dedicated START/STOP operations for `VideoLiveService` are not required.

```text
classification: pdf_table_or_documentation_error_candidate
confidence: high
```

This is treated as a copy/paste/service-name documentation candidate, not an XSD issue.

## 6. Next file

```text
docs/pdf_xsd_semantic_audit/16a_video_live_service_v1_0_v2_0_pdf_xsd_first_pass.md
```
