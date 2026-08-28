# VideoLiveService findings register addendum

Status: supplemental register; V1.0 byte-pinned Deep Read completed textually with targeted pinned-byte visual confirmation. V2.0 semantic/provenance first-pass closure exists; VLS-002 is executable-confirmed and V2.0 Deep Read is next.

Authority rule:

```text
V2.0 strict XML validation follows IBIS-IP_VideoLiveService_V2.0.xsd + Common V2.0 + Enums V2.0.
Public V1.0 has no confirmed official-release-tag VideoLiveService service XSD in the checked tag set and must not be silently mapped to V2.0.
V1.0 PDF semantics may explain history but cannot create a missing V1.0 schema authority.
Media transport/runtime is separate from XML/XSD validation.
```

Visual-review note:

```text
Interactive PDF screenshot requests for VLS V1.0 returned cache miss.
The exact pinned source was independently rendered with tools/render_vdv_pdf_pages.py.
Render runs: 33202961159 and 33203162588.
Source SHA-256: f535673427ff8f495102e1fc7723ca157408949b981572c4342b862f6d9c2a3c.
```

The fallback verified the source pin before rendering and successfully produced visible pages for material V1.0 findings. The cache miss is therefore a renderer/cache failure, not a VDV-source failure.

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

## VLS-002 - LiveStreamData xs:choice vs PDF multi-field structure

```text
state: executable-confirmed PDF/XSD semantic mismatch candidate
classification: xsd_structure_modelling_error_candidate
mismatch_kind: compositor_or_structure_modelling
confidence: very high
version_scope: V2.0 XSD; semantic evidence in V1.0 and V2.0 PDFs
validation_behavior: current V2.0 XSD permits one choice member per LiveStreamData
final_handling_bucket: executable_evidence_complete + post_audit_official_schema_candidate_review
```

Fresh V1.0 visual evidence independently shows `VideoLiveService.LiveStreamData` as one multi-field record containing together:

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

This strengthens the documented semantic history: the multi-field record concept already exists in V1.0. It does **not** make the V2.0 XSD normative for V1.0.

Executable V2.0 evidence remains:

```text
GitHub Actions run 33111119723
head d4ffe09067cb38bf7f78ba295e029902078ed18d
single StreamID sample: valid
StreamID + CameraName + rtspURI: rejected; CameraName not expected
complete PDF-shaped multi-field sample: rejected; CameraName not expected
EV-103 status: PASS
```

Evidence document:

```text
docs/pdf_xsd_semantic_audit/24c_executable_validation_video_compositors.md
```

## VLS-003 - V1.0 German foreword wrong part number

```text
state: visually_confirmed
classification: pdf_label_or_heading_error_candidate
confidence: very_high
version_scope: V1.0 PDF
validation_behavior: none; do not create document-number alias
```

Pinned-source page 4 visibly says in German that `VDV-Schrift 301-2-1` describes the live-video services, while the adjacent English foreword correctly uses `VDV 301-2-11`.

Visual evidence:

```text
render run: 33202961159
page: 4
```

## VLS-004 - VideoDisplayService in VideoLiveService start/stop prose

```text
state: visually_confirmed
classification: pdf_table_or_documentation_error_candidate
confidence: very_high
version_scope: V1.0 and first-pass evidence in V2.0 PDFs
validation_behavior: none; no service-name alias
```

Pinned-source page 38 is within the VideoLiveService start/stop procedure, then refers to stopping/restarting `VideoDisplayService`, and immediately returns to the statement that a dedicated VideoLive START/STOP operation is unnecessary because RTSP provides that functionality.

This is treated as a copy/paste/service-name documentation error.

Visual evidence:

```text
render run: 33203162588
page: 38
```

Persistence into V2.0 remains a V2.0 Deep Read check rather than a retroactive assumption.

## VLS-005 - invalid printed cardinality notation in V1.0 tables

```text
state: visually_confirmed
classification: pdf_table_cardinality_notation_error_candidate
confidence: very_high
version_scope: V1.0 PDF; textual persistence signal in V2.0 pending its own visual Deep Read
validation_behavior: none for V1.0 strict XML because no exact V1.0 VLS service XSD is confirmed
```

Visible V1.0 tables print:

```text
ListAllLiveStreamsData   -1:*
CameraCurrentState       -1:1
VideoCodec               -1:1
```

These leading-hyphen forms are not ordinary IBIS-IP cardinality notation. The audit does not guess whether the intended values were `1:*`, `0:1`, or something else.

Visual evidence:

```text
render run: 33202961159
pages: 39-40
```

No schema or validator rule is synthesized from the malformed printed notation.

## Deferred V1.0 cross-document version-label check

Visible page 45 includes references resembling:

```text
VideoRecordingService v1.1, 1.0, 05/2017
VideoDisplayService v1.1 1.0, 05/2017
```

The intended distinction between document revision/version notation has not yet been independently established. These strings are therefore carried only as follow-up evidence for `VRS_V1.0` and `VDS_V1.0`; no separate VLS defect is opened from them.

## V1.0 Deep Read report

```text
docs/pdf_xsd_semantic_audit/deep_read/VLS_V1.0.md
```

Completion:

```text
textual fresh read: complete
source pin: complete
historical official-tag XSD provenance check: complete
targeted visual confirmation of material findings: complete
all-page/all-figure visible review: not complete
state: needs_visual_review
```
