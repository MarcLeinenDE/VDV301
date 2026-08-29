# Deep Read - VideoDisplayService V2.0

Document id: `VDS_V2.0`

Status: `needs_visual_review`

Fresh-read date: 2026-08-29

## 1. Source and byte pin

Official public writing:

```text
VDV-Schrift 301-2-13
VideoDisplayService V2.0
08/2019
https://www.vdv.de/301-2-13-sdes-v2-0-video-display-service.pdfx
```

Byte pin:

```text
SHA-256: c287df20d8225af2afcd37dfdb487eb4922b89ce78c287da91745d12b410c8a2
size:    903,444 bytes
pin run: 33226181059
```

No PDF or rendered page bytes are committed to the repository.

## 2. Fresh-read order and authority

The V2.0 PDF was read independently before consulting the existing VDS compositor findings or EV-103.

Only after the PDF read was the exact official `VDV-301-2.0` service XSD selected.

Exact XSD family:

```text
IBIS-IP_VideoDisplayService_V2.0.xsd
-> IBIS-IP_common_V2.0.xsd
-> IBIS-IP_Enumerations_V2.0.xsd
```

Official release-tag service-XSD Git blob:

```text
fcfdadd3b62a584370cae326004050b4dc832e23
```

The file on `dev/schema-integration` is byte-identical at Git-blob level to the official release-tag file.

No alternate, newer, or candidate schema is substituted.

## 3. Visual-review method

Pinned-byte rendering was used for the material pages.

```text
render run: 33226294383
engine: PyMuPDF 1.28.2
dpi: 180
rendered pages: 4, 6, 11, 12, 13, 14, 15, 16
artifact digest: sha256:a8f9a098f7bbf534d41c1586230a45518ada62c67482494d8ba9b0debb617fb1
```

The render source matched the permanent VDS V2.0 pin before rendering.

Targeted material findings are visually confirmed; an all-page/all-figure pass is not complete, so status remains `needs_visual_review`.

## 4. Document role and compatibility statement

The writing describes VideoDisplayService V2.0 as the IBIS-IP service controlling live-video/image views on displays.

The foreword states compatibility/compliance with VDV301 version 1.0 and 2.x.

Authority guard:

```text
This is a service/document compatibility statement.
It is not permission to validate missing V1.0 schema instances with the V2.0 XSD.
VDS V1.0 remains fail-closed because no exact V1.0 service XSD has been confirmed.
```

## 5. Operation inventory

The V2.0 writing retains the V1.0 operation set:

```text
ListViewCapabilities
SetVideoView
SetNextViewIndex
GetDisplayState
SubscribeDisplayState
UnsubscribeDisplayState
```

Subscription prose uses the Common Subscribe/Unsubscribe structures.

## 6. VDS-002 - ListViewCapabilitiesResponse

Visible page 13 describes one response record containing together:

```text
ViewID    1:1
ViewName  1:1
ViewType  -1:1
```

The exact official V2.0 XSD instead defines:

```text
VideoDisplayService.ListViewCapabilitiesResponseStructure
= xs:choice(ViewID | ViewName | ViewType)
```

Executable evidence EV-103 / run `33111119723` confirms:

```text
single ViewID: valid
ViewID + ViewName + ViewType: rejected
first rejected additional field: ViewName
```

Result:

```text
VDS-002 remains executable-confirmed for the exact official V2.0 family.
```

## 7. VDS-003 - SetVideoViewRequest

Visible page 14 requires both:

```text
ViewID   1:1
Timeout  1:1
```

The exact official V2.0 XSD models:

```text
SetVideoViewRequestStructure
= xs:choice(ViewID | Timeout)
```

EV-103 confirms:

```text
ViewID only: valid
ViewID + Timeout: rejected
first rejected additional field: Timeout
```

Result:

```text
VDS-003 remains executable-confirmed for official V2.0.
```

## 8. VDS-004 - response compositor family

Visible pages 14-15 describe grouped response records.

### SetVideoViewResponse

```text
State                  -1:1
CurrentViewID           1:1
OperationErrorMessage   0:1
```

### SetNextViewIndexResponse

```text
State                  -1:1
OperationErrorMessage   0:1
```

### GetDisplayStateResponse

```text
State                  -1:1
CurrentViewID           1:1
OperationErrorMessage   0:1
```

The exact official V2.0 XSD uses `xs:choice` in all three structures.

EV-103 confirms:

```text
SetVideoViewResponse State only: valid
State + CurrentViewID: rejected

GetDisplayStateResponse State only: valid
State + CurrentViewID: rejected

SetNextViewIndexResponse State only: valid
State + OperationErrorMessage: rejected
```

Result:

```text
VDS-004 remains executable-confirmed across the checked V2.0 response family.
```

## 9. VDS-005 - Word cross-reference failures are corrected in V2.0

The V1.0 publication visibly contained multiple literal generated-document errors:

```text
Fehler! Verweisquelle konnte nicht gefunden werden.
```

The corresponding V2.0 common-service/startup/subscription prose was fresh-read and visually checked. Those generated errors are absent and normal reference/prose text is present.

Result:

```text
VDS-005 is V1.0-only in the checked publication history and is corrected/absent in V2.0.
```

## 10. VDS-006 - malformed printed cardinality persists

Visible V2.0 pages 13-15 continue to print leading-hyphen cardinalities:

```text
ListViewCapabilitiesResponse.ViewType  -1:1
SetVideoViewResponse.State              -1:1
SetNextViewIndexResponse.State           -1:1
GetDisplayStateResponse.State            -1:1
```

This reproduces the V1.0 notation defect.

The audit does not infer a corrected cardinality from the printed value. For V2.0, validation behavior comes solely from the exact selected XSD.

Result:

```text
VDS-006 persists through V2.0.
```

## 11. Reference-version labels

Visible page 16 continues the known English-reference errors for neighboring 05/2017 video services:

```text
VideoLiveService:      German v1.0 / English v1.1
VideoRecordingService: German v1.0 / English v1.1
```

These are already established by the dedicated VLS/VRS Deep Reads.

`VDS-007` specifically concerns neighboring documents incorrectly labeling VideoDisplayService itself as v1.1. The dedicated VDS V1.0 source plus official VDV catalog resolved that as a cross-document documentation error.

No new self-version finding is opened from VDS V2.0.

## 12. VDS-008 - incorrect RTP and SOA abbreviation expansions

The abbreviation table is visibly wrong in both VDS V1.0 and V2.0.

VDS text prints:

```text
RTP  Real Time Protocol
SOA  Server Oriented Architecture
```

External normative/standard reference terminology:

```text
RFC 3550: RTP = real-time transport protocol / RTP: A Transport Protocol for Real-Time Applications
OASIS Reference Model for SOA: SOA = Service Oriented Architecture
```

Classification:

```text
id: VDS-008
classification: pdf_protocol_or_architecture_abbreviation_error_candidate
scope: VDS V1.0 / VDS V2.0
state: visually confirmed for V2.0; textually confirmed in V1.0
confidence: very high
validation impact: none on XML/XSD
```

SDK/protocol rule:

```text
Do not derive RTP/SOA definitions from these erroneous expansions.
Use the referenced external protocol/architecture standards for terminology.
```

## 13. Minor editorial errors

The fresh read also contains several ordinary prose/typing defects such as variants resembling:

```text
Central Video Cotrol
IBI-IP
dvideo
citure
diosplay
```

These are bundled as minor editorial quality observations rather than creating separate technical finding IDs because they do not alter operation names, schema identifiers, cardinalities, protocol selection, or validation routing.

## 14. Version history

The V2.0 publication does not provide an explicit detailed change-history table comparable to some later VDV writings.

Therefore corrections/persistence were established by direct V1.0↔V2.0 comparison rather than inferred from a claimed change log.

## 15. Exact XSD identity and EV-103

The exact service XSD in the official `VDV-301-2.0` tag and on `dev/schema-integration` has the same Git blob:

```text
fcfdadd3b62a584370cae326004050b4dc832e23
```

Thus EV-103 is directly applicable to the same selected V2.0 service schema, not merely a similar file.

Evidence:

```text
EV-103 run: 33111119723
head tested: d4ffe09067cb38bf7f78ba295e029902078ed18d
status: PASS
```

## 16. Fresh-read outcome

```text
VDS-001: V1.0 provenance gap only; unchanged
VDS-002: fresh PDF/XSD + EV-103 executable-confirmed for V2.0
VDS-003: fresh PDF/XSD + EV-103 executable-confirmed for V2.0
VDS-004: fresh PDF/XSD + EV-103 executable-confirmed for V2.0
VDS-005: corrected/absent in V2.0
VDS-006: persists visibly into V2.0
VDS-007: already resolved cross-document V1.1 label issue; no new self-label defect in V2.0
VDS-008: new cross-version RTP/SOA abbreviation-expansion error
```

No XSD change is made.

## 17. Completion status

```text
textual fresh read: complete
exact source pin: complete
exact official V2.0 service-XSD identity: complete
targeted visual review: complete for material findings
EV-103 mapping to exact selected schema: complete
all-page/all-figure visual pass: not complete
state: needs_visual_review
```

Next planned document in catalog/registry order: `TRAINSET_V2.1`.
