# VideoLiveService findings register addendum

Status: Deep Read Pass 2 completed for VLS V1.0 and VLS V2.0. Choice-notation interpretation corrected 2026-08-29. VLS-002 remains executable-confirmed against the exact official V2.0 schema family.

Authority rule:

```text
V2.0 strict XML validation follows IBIS-IP_VideoLiveService_V2.0.xsd + Common V2.0 + Enums V2.0.
Public V1.0 has no confirmed exact official-release-tag VideoLiveService service XSD in the checked source set and must not be silently mapped to V2.0.
Media transport/runtime remains separate from XML/XSD validation.
```

Choice-notation correction:

```text
VDV 301-2 V2.0 section 6.1.3.3 defines a prefixed minus sign as XML-choice notation.
-1:1 is not a negative or invalid cardinality.
Historical VLS-005 wording calling -1:* / -1:1 malformed cardinality is superseded.
See AUDIT_CORRECTION_DELTA_CHOICE_NOTATION_2026-08-29.md.
```

## VLS-001 - public V1.0 without confirmed exact release-tag XSD

```text
state: confirmed_provenance_gap_for_checked_official_release_tags
classification: schema_family_or_provenance_gap
confidence: very high for checked source set
version_scope: public V1.0
validation_behavior: no strict VLS V1.0 XSD profile; no V2.0 substitution
```

Evidence:

```text
official tag VDV-301-1.0 checked recursively
monolithic IBIS_IP_V1.0.xsd checked
VideoLiveService V1.0 XSD/include/declaration not found
```

## VLS-002 - LiveStreamData PDF structure vs V2.0 XSD compositor

```text
state: fresh-read + executable-confirmed
classification: xsd_structure_modelling_error_candidate
confidence: very high
scope: official V2.0 XSD; V1.0/V2.0 PDF semantic history
```

Corrected PDF reading:

Visible V2.0 `LiveStreamData` contains many ordinary mandatory rows in one structure, including:

```text
StreamID        1:1
CameraName      1:1
CameraType      1:1
rtspURI         1:1
VideoWidth      1:1
VideoHeight     1:1
FramesPerSecond 1:1
Bitrate         1:1
Mirrored        1:1
Flipped         1:1
Rotation        1:1
Quality         1:1
```

`CameraCurrentState` and `VideoCodec` additionally carry leading-minus choice notation. The leading minus is **not** used as evidence that the whole structure is malformed.

The exact official V2.0 XSD instead declares `VideoLiveService.LiveStreamData` as one `xs:choice` over all individual fields.

EV-103 remains decisive without relying on any leading-minus row:

```text
single StreamID: valid
StreamID + CameraName + rtspURI: rejected; CameraName not expected
complete PDF-shaped multi-field sample: rejected
run: 33111119723
```

Therefore VLS-002 remains executable-confirmed.

## VLS-003 - V1.0 German foreword wrong part number

```text
state: visually confirmed in V1.0; corrected in V2.0
classification: pdf_label_or_heading_error_candidate
```

V1.0 German foreword says `VDV-Schrift 301-2-1` describes live-video services; adjacent English text and V2.0 use `301-2-11`.

## VLS-004 - VideoDisplayService in VideoLive start/stop prose

```text
state: visually confirmed persistent through V2.0
classification: pdf_table_or_documentation_error_candidate
```

The VideoLive start/stop section says `VideoDisplayService` where surrounding context and the following note clearly concern VideoLiveService. No service-name alias is created.

## VLS-005 - choice-notation application anomaly (refined)

```text
old classification: invalid/malformed printed cardinality notation
state: finding_refined
classification: pdf_choice_notation_application_anomaly_candidate
confidence: high
scope: V1.0/V2.0 PDF
```

The old premise is rejected: `-1:1` is valid VDV XML-choice notation, and `-1:*` is a leading-minus Min:Max choice form rather than a negative minimum.

The remaining anomaly is how the notation is applied/presented in the checked VideoLive tables.

Visible V2.0 examples:

```text
ListAllLiveStreamsData  -1:*
CameraCurrentState      -1:1
VideoCodec              -1:1
```

The VDV table-notation rule says lower-case letters (`a`, `b`, ...) identify the listed XML-choice alternatives. In the checked VideoLive table renderings, such alternative labels are not visibly present on these rows. In `LiveStreamData`, the minus markers occur only on two enum-valued fields while numerous peer fields remain plain `1:1`.

Therefore:

```text
Do not call the cardinality invalid.
Do not infer a negative minimum.
Treat the presentation as incomplete/ambiguous choice-notation application.
Use the exact selected XSD for executable structure semantics.
```

VLS-005 remains distinct from VLS-002: VLS-002 is the executable whole-structure compositor mismatch; VLS-005 is only a documentation-notation application issue.

## RTSP/RTP boundary

Fresh V1.0/V2.0 reads confirm:

```text
rtspURI is metadata carried by the VDV service;
RTSP controls the video session;
RTP/RTCP carries media;
a dedicated VideoLive START/STOP XML operation is not synthesized.
```

RV-004 remains consistent and passed in run `33119694991`.

## Visual evidence

```text
VLS V1.0 pin: f535673427ff8f495102e1fc7723ca157408949b981572c4342b862f6d9c2a3c
render runs: 33202961159, 33203162588

VLS V2.0 pin: d75a543c138f21c4ad370925ca7f306bcde7d692ce793ddc1d51bdcf6032787b
render run: 33203850390
```

Targeted material findings are visually confirmed. All-page/all-figure review is still incomplete, so the documents remain `needs_visual_review`.

## Current finding state

```text
VLS-001 confirmed provenance gap for checked V1.0 sources
VLS-002 executable-confirmed V2.0 compositor mismatch
VLS-003 corrected in V2.0
VLS-004 persists through V2.0
VLS-005 refined: choice-notation application anomaly, NOT invalid cardinality
```

No XSD change is made.
