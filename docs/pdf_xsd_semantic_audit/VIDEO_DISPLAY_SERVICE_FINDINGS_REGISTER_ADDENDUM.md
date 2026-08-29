# VideoDisplayService findings register addendum

Status: Deep Read Pass 2 completed for VDS V1.0. VDS-002/VDS-003/VDS-004 remain executable-confirmed for official V2.0; V1.0 contributes historical PDF semantics only because no exact V1.0 service XSD is confirmed.

Authority rule:

```text
VDS V1.0 public PDF authority: official VDV writing 301-2-13, 05/2017
VDS V1.0 strict XSD authority: unresolved / no exact service XSD confirmed in checked official repository history
Do not substitute VDS V2.0 for V1.0.
Official V2.0 findings and EV-103 remain scoped to the exact V2.0 XSD family.
```

## VDS-001 - V1.0 public PDF without confirmed exact official service XSD

```text
classification: schema_family_or_provenance_gap
scope: V1.0
state: strongly confirmed for checked official repository history
confidence: very high
validation: strict V1.0 XSD profile unresolved
```

Fresh provenance evidence:

```text
complete VDV-301-1.0 tag tree: no VideoDisplayService V1.0 XSD
IBIS_IP_V1.0.xsd: no VideoDisplayService include/declaration
commit history for IBIS-IP_VideoDisplayService_V1.0.xsd: empty
```

No nearby-version substitution is allowed.

## VDS-002 - ListViewCapabilitiesResponse compositor

```text
classification: xsd_structure_modelling_error_candidate
scope: official V2.0
state: executable-confirmed
```

Official V2.0 behavior remains:

```text
single ViewID: valid
ViewID + ViewName + ViewType: rejected; ViewName not expected
EV-103: PASS
```

Fresh V1.0 historical evidence:

Visible V1.0 page 40 already presents one response record containing together:

```text
ViewID
ViewName
ViewType
```

This strengthens semantic history only. No V1.0 XSD behavior is inferred.

## VDS-003 - SetVideoViewRequest compositor

```text
classification: xsd_structure_modelling_error_candidate
scope: official V2.0
state: executable-confirmed
```

Official V2.0 executable evidence remains:

```text
ViewID only: valid
ViewID + Timeout: rejected; Timeout not expected
EV-103: PASS
```

Fresh V1.0 page 41 shows both:

```text
ViewID   1:1
Timeout  1:1
```

as the request structure. Historical evidence only for V1.0.

## VDS-004 - response compositor family

```text
classification: xsd_structure_modelling_error_candidate
scope: official V2.0
state: executable-confirmed
```

Official V2.0 executable evidence remains:

```text
SetVideoViewResponse State only: valid
State + CurrentViewID: rejected
GetDisplayStateResponse State only: valid
State + CurrentViewID: rejected
SetNextViewIndexResponse State only: valid
State + OperationErrorMessage: rejected
EV-103: PASS
```

Fresh V1.0 pages 41-42 already describe those responses as grouped multi-field records. This is historical semantic evidence only; it does not create a missing V1.0 schema.

## VDS-005 - broken generated Word cross references

```text
classification: pdf_table_or_documentation_error_candidate
scope: V1.0 PDF
state: visually confirmed
confidence: very high
validation impact: none
```

Pinned visual evidence shows the literal text:

```text
Fehler! Verweisquelle konnte nicht gefunden werden.
```

in multiple locations, including:

```text
3.5.2 Identification of VideoDisplayService
3.5.3 DeviceManagementService and Error Handling
3.5.4 System start/stop procedure
3.6.5 SubscribeDisplayState
3.6.6 UnsubscribeDisplayState
```

No missing target is guessed and no resolver behavior is derived from the broken references.

## VDS-006 - invalid printed `-1:1` cardinality notation

```text
classification: pdf_cardinality_notation_error_candidate
scope: V1.0 PDF
state: visually confirmed
confidence: very high
validation impact: none for V1.0 because strict service-XSD authority is unresolved
```

Visible pages 40-42 print:

```text
ListViewCapabilitiesResponse.ViewType  -1:1
SetVideoViewResponse.State              -1:1
SetNextViewIndexResponse.State           -1:1
GetDisplayStateResponse.State            -1:1
```

The intended replacement cardinality is not guessed.

## VDS-007 - neighboring documents label VideoDisplayService as v1.1

```text
classification: pdf_reference_version_label_error_candidate
state: cross_document_confirmed
confidence: very high
validation impact: none
```

The current official VDV catalog explicitly labels the 05/2017 VDV 301-2-13 publication as:

```text
VideoDisplayService V1.0
```

The dedicated VDS source is that 05/2017 publication. Neighboring VLS/VRS reference sections nevertheless label VDV 301-2-13 / 05/2017 as `VideoDisplayService v1.1`.

Therefore the neighboring `v1.1` label is treated as a documentation/reference-version error.

Resolver rule:

```text
Do not create VDS V1.1 as a schema/profile/version alias from those reference lines.
```

This resolves the cross-document question intentionally deferred during the VLS/VRS Deep Reads.

## VDS V1.0 visual evidence

```text
source SHA-256: 9280cc239cf71bb158ab5941b522a2c4c822420e07ed44f4d4111d9689418480
source size: 1,202,943 bytes
pin run: 33225713193
render run: 33225843645
render engine: PyMuPDF 1.28.2
rendered pages: 4, 37-45
artifact digest: sha256:ff288301329a8fc3ea7e5e1fa568f06b0b6b5c4e76270f9c720a3a60eb29c9cd
```

Targeted material findings are visually confirmed. The all-page/all-figure visual pass is not complete, so VDS V1.0 remains `needs_visual_review`.

## Existing V2.0 executable evidence

```text
GitHub Actions run 33111119723
head d4ffe09067cb38bf7f78ba295e029902078ed18d
EV-103 status: PASS
```

This evidence remains V2.0-only until the dedicated VDS V2.0 Deep Read selects and rechecks that version's own PDF/XSD authority.
