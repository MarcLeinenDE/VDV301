# Deep Read - VideoDisplayService V1.0

Document id: `VDS_V1.0`

Status: `needs_visual_review`

Fresh-read date: 2026-08-29

## 1. Source and byte pin

Official public writing:

```text
VDV-Schrift 301-2-13
VideoDisplayService
05/2017
https://www.vdv.de/301-2-13-sds.pdfx
```

Byte pin:

```text
SHA-256: 9280cc239cf71bb158ab5941b522a2c4c822420e07ed44f4d4111d9689418480
size:    1,202,943 bytes
pin run: 33225713193
```

The current official VDV IP-KOM-ÖV catalog explicitly labels the 05/2017 publication as `VideoDisplayService V1.0`.

No PDF or rendered page bytes are committed to the repository.

## 2. Historical XSD provenance

The complete official upstream tag `VDV-301-1.0` at commit/tree `f5b53785f703e898632603eec3bfa3555a79fdba` was inspected.

It contains historical V1.0 Common/Enums, several service XSDs and `IBIS_IP_V1.0.xsd`, but no VideoDisplayService V1.0 service XSD.

The monolithic `IBIS_IP_V1.0.xsd` contains no VideoDisplayService include or declaration.

A direct repository-history query for:

```text
IBIS-IP_VideoDisplayService_V1.0.xsd
```

returned no commits.

Therefore:

```text
VDS V1.0 PDF authority: official public VDV writing
strict VDS V1.0 XSD authority: unresolved / no exact official service XSD confirmed
VDS V2.0 XSD must NOT be substituted for V1.0
```

This strongly confirms existing finding `VDS-001` for the checked official repository history.

## 3. Visual-review method

The audit used the pinned-byte renderer:

```text
tools/render_vdv_pdf_pages.py
```

Render evidence:

```text
run: 33225843645
engine: PyMuPDF 1.28.2
dpi: 180
PDF pages: 49
rendered pages: 4, 37, 38, 39, 40, 41, 42, 43, 44, 45
artifact digest: sha256:ff288301329a8fc3ea7e5e1fa568f06b0b6b5c4e76270f9c720a3a60eb29c9cd
```

The render manifest verifies the pinned source SHA-256/size and records an individual SHA-256 for every PNG.

Targeted material findings are visually confirmed. An all-page/all-figure pass is not complete, so status remains `needs_visual_review`.

## 4. Document identity and role

Visible page 4 states in German and English that VDV 301-2-13 describes the video display services.

The writing describes VideoDisplayService as the IBIS-IP service that controls display of live video/images and views on monitors/displays. It relies on VideoLiveService for available source/stream information and can add OSD information.

The writing is part of the 05/2017 video-service publication set and describes its proposal as an extension of IBIS-IP / VDV301 Version 1.0.

## 5. Common-service and startup prose

Visible pages 37-38 describe identification, DeviceManagementService integration and startup/stop behavior.

The prose contains multiple literal Word-generated cross-reference failures:

```text
Fehler! Verweisquelle konnte nicht gefunden werden.
```

Examples are visible in:

```text
3.5.2 Identification of VideoDisplayService
3.5.3 DeviceManagementService and Error Handling
3.5.4 System start/stop procedure
```

This strengthens existing `VDS-005` and confirms it is not merely a text-extraction artifact.

No routing or protocol behavior is inferred from the missing targets.

## 6. Operation inventory

Visible pages 38-39 list:

```text
ListViewCapabilities
SetVideoView
SetNextViewIndex
GetDisplayState
SubscribeDisplayState
UnsubscribeDisplayState
```

Subscription operations use the Common Subscribe/Unsubscribe request/response structures.

The V1.0 document is documentation authority only because no exact V1.0 VDS service XSD is confirmed.

## 7. ListViewCapabilitiesResponse semantics

Visible page 40 presents one response record containing together:

```text
ViewID    1:1
ViewName  1:1
ViewType  -1:1
```

The multi-field record is strong historical PDF evidence for the semantic model later involved in `VDS-002`.

Authority guard:

```text
VDS-002 executable behavior remains scoped to official V2.0 XSD.
V1.0 contributes historical semantic evidence only.
```

## 8. SetVideoView semantics

Visible page 41 presents the request with both fields required:

```text
ViewID   1:1
Timeout  1:1
```

The response is presented as one record containing:

```text
State                  -1:1
CurrentViewID           1:1
OperationErrorMessage   0:1
```

Thus the `ViewID + Timeout` request concept and grouped response concept both predate V2.0 in the publication history.

This historically strengthens later `VDS-003` and `VDS-004`, but creates no inferred V1.0 XSD rule.

## 9. SetNextViewIndex and GetDisplayState semantics

Visible page 41 shows `SetNextViewIndexResponse` as:

```text
State                  -1:1
OperationErrorMessage   0:1
```

Visible page 42 shows `GetDisplayStateResponse` as:

```text
State                  -1:1
CurrentViewID           1:1
OperationErrorMessage   0:1
```

Again, these are multi-field response tables. They are historical semantic evidence for later `VDS-004` only.

## 10. VDS-006 - invalid printed `-1:1` cardinality notation

Visible pages 40-42 print malformed leading-hyphen cardinalities:

```text
ListViewCapabilitiesResponse.ViewType  -1:1
SetVideoViewResponse.State              -1:1
SetNextViewIndexResponse.State           -1:1
GetDisplayStateResponse.State            -1:1
```

Classification:

```text
pdf_cardinality_notation_error_candidate
```

The audit does not guess whether the intended value is `1:1`, `0:1`, or another cardinality.

Because no exact strict VDS V1.0 XSD is confirmed, this finding has no V1.0 executable-schema resolution.

## 11. Subscription cross-reference errors

Visible page 42 describes SubscribeDisplayState and UnsubscribeDisplayState using chapters 10.51/10.52 of VDV301-2 but replaces the referenced-document target with the literal Word error:

```text
Fehler! Verweisquelle konnte nicht gefunden werden.
```

This is part of existing `VDS-005`, not a new finding ID.

The missing cross-reference does not redefine the Common subscription structures.

## 12. Version history

Visible page 44 contains the heading:

```text
Versionshistorie / Version History
```

with no entries.

For the baseline V1.0 publication this is not classified as a defect by itself.

## 13. VDS-007 - external documents label VideoDisplayService as v1.1

The dedicated VDS publication and official VDV catalog establish the 05/2017 VDV 301-2-13 publication as `VideoDisplayService V1.0`.

Neighboring official 05/2017 video-service writings (VLS/VRS) contain reference lines that label VDV 301-2-13 / 05-2017 as `VideoDisplayService v1.1`.

This is now classified as a cross-document reference-version-label error:

```text
id: VDS-007
classification: pdf_reference_version_label_error_candidate
state: cross_document_confirmed
validation impact: none
```

No VDS V1.1 schema/profile is created from those reference labels.

This resolves the deferred VideoDisplay portion carried forward from the VLS/VRS Deep Reads.

## 14. Reference-page consistency inside VDS V1.0

Visible page 45 itself contains the same known English-reference `v1.1` errors for neighboring services:

```text
VDV 301-2-11:
German  VideoLiveService v1.0
English VideoLiveService v1.1

VDV 301-2-12:
German  VideoRecordingService v1.0
English VideoRecordingService v1.1
```

Those are already established in the dedicated VLS/VRS Deep Reads. They are not duplicated as new VDS findings.

## 15. Relation to later V2.0 findings

Only after completing the independent V1.0 read was the existing VDS finding register consulted.

The V1.0 PDF independently shows that the semantic concepts later involved in V2.0 findings already existed in 05/2017:

```text
VDS-002: ViewCapabilities is a multi-field record
VDS-003: SetVideoView request contains ViewID + Timeout
VDS-004: display-state responses contain multiple related fields together
```

However:

```text
No exact V1.0 VDS XSD is confirmed.
Therefore no V1.0 compositor behavior is inferred.
EV-103 remains V2.0-only executable evidence.
```

## 16. Fresh-read outcome

Existing findings:

```text
VDS-001 strongly confirmed for checked official V1.0 repository provenance
VDS-002 historically strengthened only; executable scope remains V2.0
VDS-003 historically strengthened only; executable scope remains V2.0
VDS-004 historically strengthened only; executable scope remains V2.0
VDS-005 visually confirmed and expanded to exact visible locations
```

New findings:

```text
VDS-006 invalid printed -1:1 cardinality notation
VDS-007 external VideoDisplayService v1.1 reference-version label error
```

No XSD is changed.

## 17. Completion status

```text
textual fresh read: complete
exact source pin: complete
historical official-tag XSD provenance check: complete
targeted visual checks: complete for material findings
cross-document VideoDisplay v1.1 question: resolved
all-page/all-figure visual pass: not complete
state: needs_visual_review
```

Next planned document: `VDS_V2.0`, using its own byte pin and exact official V2.0 XSD family before re-evaluating VDS-002/VDS-003/VDS-004 and EV-103 in that version's own authority context.
