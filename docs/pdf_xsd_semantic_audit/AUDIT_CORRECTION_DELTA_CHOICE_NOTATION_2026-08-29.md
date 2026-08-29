# Audit correction delta - VDV choice notation (`-1:1`, `-0:1`, `-1:*`)

Date: 2026-08-29

Status: corrective overlay; supersedes earlier interpretations that treated the leading minus sign itself as a malformed cardinality.

## Trigger

During user review, the meaning of leading-hyphen Min:Max values was questioned. The VDV's own table-notation rules in VDV 301-2 V2.0, section 6.1.3.3 `Multiplizität & Choice (Min:Max)`, were re-read.

The VDV rule is explicit:

```text
0:1  optional single element
1:1  mandatory single element
0:*  optional repeated element

A prefixed minus sign denotes XML choice.
Example: -1:1
Optional choice example: -0:1
A lower-case letter before the element name identifies the listed choice alternatives.
```

Therefore the minus sign is a choice marker, not a negative cardinality bound.

## Correction scope

Earlier Deep Read material incorrectly described `-1:1` / `-1:*` as malformed or invalid cardinality notation in:

```text
VLS-005
VRS-007
VDS-006
```

Those interpretations are corrected as follows.

### VLS-005 - refined, not withdrawn

`-1:*` and `-1:1` are not invalid cardinalities by themselves.

The remaining documentation issue is the *application* of the choice notation in the VideoLive tables:

```text
ListAllLiveStreamsData  -1:*
CameraCurrentState      -1:1
VideoCodec              -1:1
```

On the checked visible V1.0/V2.0 tables, the lower-case `a`, `b`, ... alternative labels required by the VDV notation rule are not visibly present for these rows. In `LiveStreamData`, most peer fields are ordinary `1:1` fields while only the enum-valued `CameraCurrentState` and `VideoCodec` carry the minus marker.

Thus VLS-005 is reclassified from `invalid cardinality notation` to:

```text
pdf_choice_notation_application_anomaly_candidate
state: finding_refined
```

This does not remove VLS-002. The V2.0 PDF still presents multiple ordinary required fields (`StreamID`, `CameraName`, `CameraType`, `rtspURI`, etc.) in one LiveStreamData structure, while the exact official V2.0 XSD places all individual fields in one `xs:choice`. EV-103 remains applicable; its `StreamID + CameraName + rtspURI` rejection does not depend on interpreting a leading-minus row.

### VRS-007 - withdrawn after correction

VRS-007 was opened only because `-1:1` was misread as an invalid negative minimum. That premise is wrong.

Visible VRS V2.0 page 18 actually uses the VDV choice notation explicitly:

```text
a  State          -1:1
   AlarmArchiveFillLevel  1:1
   OperationErrorMessage  1:1
b  StartStopMode  -1:1
```

The choice marker itself is valid VDV notation. VRS-007 is therefore:

```text
state: withdrawn_after_deep_read_correction
classification: rejected_after_deep_read
```

The underlying VRS-003 structure finding remains and is refined: the PDF depicts ordinary required `AlarmArchiveFillLevel` and `OperationErrorMessage` fields plus an `a/b` choice between `State` and `StartStopMode`, whereas the official V2.0 XSD makes all four members alternatives of a single `xs:choice`.

Visible VRS V2.4 page 20 confirms the intended notation even more clearly:

```text
a  VideoRecordingState   -1:1
b  OperationErrorMessage
```

This matches the candidate V2.4 outer `xs:choice`. The former statement that VRS-007 'moved' to the outer V2.4 row is superseded.

### VDS-006 - refined, not a cardinality error

The visible VDS V1.0/V2.0 tables use `a` plus `-1:1` on enum-valued rows such as `ViewType` and `State`. The minus sign itself is valid VDV choice notation.

However, the checked tables show an `a` marker without a visible peer `b` alternative in the same structure, while surrounding elements are ordinary `1:1` / `0:1` rows. This is not an invalid cardinality, but it is an incomplete or degenerate application of the documented choice notation.

VDS-006 is therefore reclassified to:

```text
pdf_choice_notation_application_anomaly_candidate
state: finding_refined
```

VDS-002 / VDS-004 remain valid and are strengthened by the corrected reading:

```text
VDS-002 PDF:
  ViewID   1:1
  ViewName 1:1
  a ViewType -1:1

VDS-002 XSD:
  xs:choice(ViewID | ViewName | ViewType)

VDS-004 PDF response examples:
  a State -1:1
  CurrentViewID 1:1
  OperationErrorMessage 0:1

VDS-004 XSD:
  xs:choice across all listed members
```

The PDF's ordinary non-choice rows are sufficient to establish the mismatch; the finding does not depend on treating `-1:1` as malformed.

## EV-103 impact

EV-103 remains valid executable evidence for the exact official V2.0 XSD families.

The correction changes the *PDF interpretation wording*, not the executed XSD outcomes:

```text
VLS-002: remains executable-confirmed
VRS-003: remains executable-confirmed, description refined
VDS-002: remains executable-confirmed
VDS-003: remains executable-confirmed
VDS-004: remains executable-confirmed
```

No XSD is changed.

## Audit precedence

This correction delta and the updated current service registers supersede older report sections that call the leading-minus forms themselves invalid/malformed. Historical Deep Read reports remain as audit snapshots; when they conflict with this correction, this correction is authoritative.

Affected historical report sections include:

```text
deep_read/VLS_V1.0.md  VLS-005 section
deep_read/VLS_V2.0.md  VLS-005 section
deep_read/VRS_V1.0.md  VRS-007 section
deep_read/VRS_V2.0.md  VRS-007 section
deep_read/VRS_V2.4.md  VRS-007 section
deep_read/VDS_V1.0.md  VDS-006 section
deep_read/VDS_V2.0.md  VDS-006 section
```

## Method guard added

Future Deep Reads must distinguish:

```text
plain Min:Max multiplicity
vs
VDV leading-minus XML-choice notation
```

A leading minus sign must never again be classified as a negative minimum by itself. Choice grouping must be evaluated from the minus marker, lower-case alternative labels, surrounding rows and the selected XSD compositor together.
