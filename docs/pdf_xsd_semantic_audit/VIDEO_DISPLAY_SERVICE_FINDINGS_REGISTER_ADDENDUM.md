# VideoDisplayService findings register addendum

Status: Deep Read Pass 2 completed for VDS V1.0 and VDS V2.0. VDS-002/VDS-003/VDS-004 are fresh-read and executable-confirmed for the exact official V2.0 schema family.

Authority rule:

```text
VDS V1.0 PDF: official public VDV writing; exact strict V1.0 service XSD unresolved.
Do not substitute V2.0 for V1.0.
VDS V2.0 strict validation: official VDV-301-2.0 service XSD + Common V2.0 + Enums V2.0.
Official and integration VDS V2.0 service XSD Git blob: fcfdadd3b62a584370cae326004050b4dc832e23.
```

The V2.0 writing's compatibility/compliance statement covering VDV301 1.0 and 2.x is not schema-version substitution authority.

## VDS-001 - V1.0 public PDF without confirmed exact official service XSD

```text
classification: schema_family_or_provenance_gap
scope: V1.0
state: strongly confirmed for checked official repository history
confidence: very high
validation: strict V1.0 XSD profile unresolved
```

Evidence:

```text
complete VDV-301-1.0 tag tree: no VideoDisplayService V1.0 XSD
IBIS_IP_V1.0.xsd: no VideoDisplayService include/declaration
commit history for IBIS-IP_VideoDisplayService_V1.0.xsd: empty
```

## VDS-002 - ListViewCapabilitiesResponse compositor

```text
classification: xsd_structure_modelling_error_candidate
scope: official V2.0
state: fresh PDF/XSD + executable-confirmed
confidence: very high
```

Fresh V2.0 PDF page 13 presents one record containing `ViewID`, `ViewName`, and `ViewType` together.

Exact official V2.0 XSD blob `fcfdadd3b62a584370cae326004050b4dc832e23` models the three members as `xs:choice`.

EV-103 / run `33111119723`:

```text
single ViewID: valid
ViewID + ViewName + ViewType: rejected; ViewName not expected
```

V1.0 page 40 already contains the same multi-field semantic concept, but that is historical PDF evidence only because no exact V1.0 VDS service XSD is confirmed.

## VDS-003 - SetVideoViewRequest compositor

```text
classification: xsd_structure_modelling_error_candidate
scope: official V2.0
state: fresh PDF/XSD + executable-confirmed
confidence: very high
```

Fresh V2.0 page 14 requires:

```text
ViewID   1:1
Timeout  1:1
```

Exact official V2.0 XSD uses `xs:choice(ViewID | Timeout)`.

EV-103:

```text
ViewID only: valid
ViewID + Timeout: rejected; Timeout not expected
```

V1.0 contains the same two-field documented request semantics as historical evidence only.

## VDS-004 - response compositor family

```text
classification: xsd_structure_modelling_error_candidate
scope: official V2.0
state: fresh PDF/XSD + executable-confirmed
confidence: very high
```

Fresh V2.0 pages 14-15 present grouped multi-field responses:

```text
SetVideoViewResponse: State + CurrentViewID + OperationErrorMessage
SetNextViewIndexResponse: State + OperationErrorMessage
GetDisplayStateResponse: State + CurrentViewID + OperationErrorMessage
```

The exact official V2.0 XSD models each response as `xs:choice`.

EV-103 confirms representative multi-field combinations are rejected after the first selected choice member.

## VDS-005 - broken generated Word cross references

```text
classification: pdf_table_or_documentation_error_candidate
scope: V1.0 PDF
state: visually confirmed in V1.0; corrected/absent in V2.0
confidence: very high
validation impact: none
```

V1.0 contains literal generated Word reference failures in identification, DeviceManagement/error-handling, startup and subscription prose.

The corresponding V2.0 passages were fresh-read and visually checked; the generated errors are absent.

## VDS-006 - invalid printed `-1:1` cardinality notation

```text
classification: pdf_cardinality_notation_error_candidate
scope: V1.0/V2.0 PDF
state: visually confirmed persistent through V2.0
confidence: very high
```

Visible V2.0 pages 13-15 continue the V1.0 malformed notation, including:

```text
ListViewCapabilitiesResponse.ViewType  -1:1
SetVideoViewResponse.State              -1:1
SetNextViewIndexResponse.State           -1:1
GetDisplayStateResponse.State            -1:1
```

The intended cardinality is not guessed. V2.0 validation follows the exact selected XSD.

## VDS-007 - neighboring documents label VideoDisplayService as v1.1

```text
classification: pdf_reference_version_label_error_candidate
state: cross_document_confirmed
confidence: very high
validation impact: none
```

The official VDV catalog identifies the 05/2017 VDV 301-2-13 publication as `VideoDisplayService V1.0`. Neighboring VLS/VRS reference sections nevertheless label that same publication `VideoDisplayService v1.1`.

Resolver rule:

```text
Do not create VDS V1.1 as a schema/profile/version alias from those reference lines.
```

VDS V2.0 itself does not establish a VDS V1.1 profile. Its reference page continues already-known English v1.1 errors for VideoLiveService and VideoRecordingService.

## VDS-008 - incorrect RTP and SOA abbreviation expansions

```text
classification: pdf_protocol_or_architecture_abbreviation_error_candidate
scope: V1.0/V2.0 PDF
state: visually confirmed in V2.0; textually confirmed in V1.0
confidence: very high
validation impact: none on XML/XSD
```

The VDS abbreviation table says:

```text
RTP  Real Time Protocol
SOA  Server Oriented Architecture
```

External standard terminology says:

```text
RFC 3550: RTP is the real-time transport protocol / A Transport Protocol for Real-Time Applications
OASIS SOA Reference Model: SOA = Service Oriented Architecture
```

SDK/protocol handling must not derive these definitions from the erroneous VDS abbreviation expansion.

## Visual evidence

```text
VDS V1.0
source SHA-256: 9280cc239cf71bb158ab5941b522a2c4c822420e07ed44f4d4111d9689418480
source size: 1,202,943 bytes
pin run: 33225713193
render run: 33225843645
pages: 4,37-45
artifact digest: sha256:ff288301329a8fc3ea7e5e1fa568f06b0b6b5c4e76270f9c720a3a60eb29c9cd

VDS V2.0
source SHA-256: c287df20d8225af2afcd37dfdb487eb4922b89ce78c287da91745d12b410c8a2
source size: 903,444 bytes
pin run: 33226181059
render run: 33226294383
pages: 4,6,11-16
artifact digest: sha256:a8f9a098f7bbf534d41c1586230a45518ada62c67482494d8ba9b0debb617fb1
```

Targeted material findings are visually confirmed; all-page/all-figure passes remain incomplete, so both Deep Read states remain `needs_visual_review`.

## Executable evidence

```text
EV-103
GitHub Actions run: 33111119723
head tested: d4ffe09067cb38bf7f78ba295e029902078ed18d
status: PASS
```

No XSD correction is made in the integration branch.
