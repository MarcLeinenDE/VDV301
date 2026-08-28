# VideoLiveService findings register addendum

Status: supplemental register; V1.0 and V2.0 byte-pinned Deep Reads completed textually with targeted pinned-byte visual confirmation. VLS-002 is executable-confirmed against the exact official V2.0 schema family.

Authority rule:

```text
V2.0 strict XML validation follows IBIS-IP_VideoLiveService_V2.0.xsd + Common V2.0 + Enums V2.0.
Public V1.0 has no confirmed official-release-tag VideoLiveService service XSD in the checked tag set and must not be silently mapped to V2.0.
V1.0 PDF semantics may explain history but cannot create a missing V1.0 schema authority.
Media transport/runtime is separate from XML/XSD validation.
```

Visual-review rule:

```text
Interactive PDF screenshot cache misses are not source failures.
Material VLS pages were rendered from the exact byte-pinned PDF sources with tools/render_vdv_pdf_pages.py.
V1.0 render runs: 33202961159, 33203162588.
V2.0 render run: 33203850390.
```

## VLS-001 - public V1.0 without confirmed official release-tag XSD

```text
state: confirmed_provenance_gap_for_checked_official_release_tags
classification: schema_family_or_provenance_gap
confidence: very_high for checked official release tags
version_scope: public V1.0
validation_behavior: no strict VLS V1.0 XSD profile; no V2.0 substitution
final_handling_bucket: official_schema_family_clarification_candidate
```

Fresh Deep Read provenance evidence:

```text
official tag: VDV-301-1.0
tag commit: f5b53785f703e898632603eec3bfa3555a79fdba
tree: 729bbe3270e52fed3e0641466048a745d5a09b32
recursive tree inspection: complete
monolithic IBIS_IP_V1.0.xsd: checked
VideoLiveService V1.0 XSD/include/declaration: not found
```

Handling remains fail-closed: VLS V1.0 must not be routed through the V2.0 service XSD merely because V2.0 is available.

V2.0 contrast:

```text
VDV-301-2.0 contains exact official IBIS-IP_VideoLiveService_V2.0.xsd.
blob: d8c52f5de9ef3f5915524fef12da11eabf0ca041
route: VideoLiveService V2.0 -> Common V2.0 -> Enumerations V2.0
```

## VLS-002 - LiveStreamData xs:choice vs PDF multi-field structure

```text
state: executable-confirmed PDF/XSD semantic mismatch candidate
classification: xsd_structure_modelling_error_candidate
mismatch_kind: compositor_or_structure_modelling
confidence: very high
version_scope: official V2.0 XSD; semantic evidence in V1.0 and V2.0 PDFs
validation_behavior: current official V2.0 XSD permits one choice member per LiveStreamData
final_handling_bucket: executable_evidence_complete + post_audit_official_schema_candidate_review
```

Both fresh pinned PDF reads visibly present `VideoLiveService.LiveStreamData` as one multi-field stream record containing together:

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

The exact official V2.0 XSD uses:

```text
VideoLiveService.LiveStreamData -> xs:choice over the individual fields
```

Executable evidence:

```text
GitHub Actions run 33111119723
head d4ffe09067cb38bf7f78ba295e029902078ed18d
single StreamID sample: valid
StreamID + CameraName + rtspURI: rejected; CameraName not expected
complete PDF-shaped multi-field sample: rejected; CameraName not expected
EV-103 status: PASS
```

The V1.0 PDF strengthens semantic history only; it does not make V2.0 XSD authoritative for V1.0.

Evidence document:

```text
docs/pdf_xsd_semantic_audit/24c_executable_validation_video_compositors.md
```

## VLS-003 - V1.0 German foreword wrong part number

```text
state: visually_confirmed_in_V1.0_corrected_in_V2.0
classification: pdf_label_or_heading_error_candidate
confidence: very_high
version_scope: V1.0 PDF; corrected in V2.0
validation_behavior: none; do not create document-number alias
```

V1.0 pinned page 4 visibly says in German that `VDV-Schrift 301-2-1` describes the live-video services, while the adjacent English foreword correctly uses `VDV 301-2-11`.

V2.0 pinned page 4 consistently uses `VDV 301-2-11` in both language sections. The later correction does not rewrite the V1.0 publication.

Visual evidence:

```text
V1.0: run 33202961159, page 4
V2.0: run 33203850390, page 4
```

## VLS-004 - VideoDisplayService in VideoLiveService start/stop prose

```text
state: visually_confirmed_persists_through_V2.0
classification: pdf_table_or_documentation_error_candidate
confidence: very_high
version_scope: V1.0 and V2.0 PDFs
validation_behavior: none; no service-name alias
```

V1.0 page 38 and V2.0 page 35 both contain `VideoDisplayService` inside the VideoLive start/stop procedure. In both cases the nearby note returns to VideoLiveService and states that a dedicated VideoLive START/STOP operation is unnecessary because RTSP provides the function.

This is treated as a copy/paste/service-name documentation error.

Visual evidence:

```text
V1.0: run 33203162588, page 38
V2.0: run 33203850390, page 35
```

## VLS-005 - invalid printed cardinality notation

```text
state: visually_confirmed_persists_through_V2.0
classification: pdf_table_cardinality_notation_error_candidate
confidence: very_high
version_scope: V1.0 and V2.0 PDFs
validation_behavior: documentation notation issue; exact V2.0 XSD remains executable authority
```

Visible V1.0 and V2.0 tables print leading-hyphen cardinality-like values:

```text
ListAllLiveStreamsData   -1:*
CameraCurrentState       -1:1
VideoCodec               -1:1
```

V2.0 exact XSD comparison:

```text
ListAllLiveStreamsData: default minOccurs=1, maxOccurs=unbounded
CameraCurrentState: one occurrence inside the selected xs:choice branch
VideoCodec: one occurrence inside the selected xs:choice branch
```

This makes a stray leading hyphen a plausible editorial explanation, but the audit does not silently rewrite the publication. `VLS-005` remains distinct from `VLS-002`: the malformed printed notation is a documentation issue; the `xs:choice` structure has independently proven executable instance impact.

Visual evidence:

```text
V1.0: run 33202961159, pages 39-40
V2.0: run 33203850390, pages 36-37
```

## RTSP/RTP boundary after V2.0 fresh read

The fresh V2.0 writing independently confirms:

```text
rtspURI is carried in live-stream metadata;
RTP/RTSP are used for real-time video;
a dedicated VideoLive START/STOP operation is not required because RTSP supplies the function.
```

After the fresh PDF/XSD comparison, RV-004 was consulted and remains consistent. No runtime correction is required.

```text
RV-004 run: 33119694991 PASS
```

The SDK/runtime model must continue to separate:

```text
VDV discovery / HTTP / XML metadata
RTSP control
RTP/RTCP media
```

## Deferred V1.0/V2.0 cross-document version-label check

The VLS reference sections contain neighboring video-document version strings resembling:

```text
VideoRecordingService v1.1, 1.0, 05/2017
VideoDisplayService v1.1 1.0, 05/2017
```

Their intended document-revision/service-version relationship remains a follow-up for the independent `VRS_V1.0` and `VDS_V1.0` Deep Reads. No separate VLS defect is opened from them.

## Deep Read reports

```text
docs/pdf_xsd_semantic_audit/deep_read/VLS_V1.0.md
docs/pdf_xsd_semantic_audit/deep_read/VLS_V2.0.md
```

Completion:

```text
VLS V1.0 textual fresh read: complete
VLS V2.0 textual fresh read: complete
source pins: complete
V1.0 historical XSD provenance: complete
V2.0 exact official XSD route: complete
targeted visual confirmation of material findings: complete
EV-103 comparison after fresh V2.0 read: complete
RV-004 comparison after fresh V2.0 read: complete
all-page/all-figure visible review: not complete
state: needs_visual_review for both documents
```
