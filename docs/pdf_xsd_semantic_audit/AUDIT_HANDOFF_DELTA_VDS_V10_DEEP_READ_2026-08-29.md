# AUDIT HANDOFF DELTA - VideoDisplayService V1.0 Deep Read

Date: 2026-08-29
Branch: `dev/schema-integration`
Clean head before this closure: `8f3cb223ef968e7c6a545ade2a286c1420785cd8`

## Completed document

`VDS_V1.0` - VDV-Schrift 301-2-13 VideoDisplayService, 05/2017.

Official PDF pin:

```text
SHA-256: 9280cc239cf71bb158ab5941b522a2c4c822420e07ed44f4d4111d9689418480
size: 1,202,943 bytes
pin run: 33225713193
```

Pinned visual evidence:

```text
render run: 33225843645
engine: PyMuPDF 1.28.2
pages: 4,37,38,39,40,41,42,43,44,45
artifact digest: sha256:ff288301329a8fc3ea7e5e1fa568f06b0b6b5c4e76270f9c720a3a60eb29c9cd
```

Status after closure: `needs_visual_review` because targeted material pages are visually confirmed but an all-page/all-figure pass is not complete.

## Historical XSD provenance

The official `VDV-301-1.0` tag tree at `f5b53785f703e898632603eec3bfa3555a79fdba` contains no VideoDisplayService V1.0 service XSD.

`IBIS_IP_V1.0.xsd` blob `41289eaed2674a169fdf77a10a2eff293c76d5c4` has no VDS include/declaration.

Direct commit history for `IBIS-IP_VideoDisplayService_V1.0.xsd` is empty.

Therefore strict VDS V1.0 XSD authority remains unresolved and V2.0 must not be substituted.

## Fresh-read results

Visible V1.0 PDF semantics already show:

```text
ListViewCapabilitiesResponse = ViewID + ViewName + ViewType
SetVideoViewRequest = ViewID + Timeout
SetVideoViewResponse = State + CurrentViewID + OperationErrorMessage
SetNextViewIndexResponse = State + OperationErrorMessage
GetDisplayStateResponse = State + CurrentViewID + OperationErrorMessage
```

These historically strengthen later VDS-002/VDS-003/VDS-004 but do not create V1.0 executable behavior.

## Findings

Existing findings:

```text
VDS-001 strongly confirmed provenance gap
VDS-002 historical V1.0 semantics added; executable scope stays V2.0
VDS-003 historical V1.0 semantics added; executable scope stays V2.0
VDS-004 historical V1.0 semantics added; executable scope stays V2.0
VDS-005 visually confirmed Word-generated cross-reference failures
```

New findings:

```text
VDS-006 malformed printed -1:1 cardinality notation on ViewType/State rows
VDS-007 neighboring VLS/VRS references incorrectly label 05/2017 VideoDisplayService as v1.1
```

The official current VDV IP-KOM-ÖV catalog explicitly labels the 05/2017 VDV 301-2-13 publication `VideoDisplayService V1.0`. Therefore no VDS V1.1 profile or alias may be created from neighboring reference lines.

## Cross-document reference result

This resolves the question intentionally deferred from VLS/VRS Deep Reads. The same family of English-reference `v1.1` label errors exists for VideoLive and VideoRecording; the dedicated VDS source/catalog confirms VideoDisplay is likewise V1.0 for the 05/2017 publication.

## No schema change

No XSD was modified, no candidate was promoted, and no `master`/PR/upstream action was taken.

## Next document

`VDS_V2.0`.

Required order:

1. Byte-pin official VDS V2.0 PDF.
2. Fresh-read V2.0 independently.
3. Select exact official V2.0 service XSD + Common V2.0 + Enums V2.0.
4. Only after the PDF read, map VDS-002/VDS-003/VDS-004 and EV-103 to that exact authority context.
5. Check persistence/correction of VDS-005/VDS-006 and reference-label issues.
6. Use pinned-byte rendering for material pages or any screenshot cache miss.

Standing rules remain unchanged: no latest-wins routing, no XSD changes because PDF differs, no fork `master` modification, and no PR/comment/merge/upstream action without explicit user approval.
