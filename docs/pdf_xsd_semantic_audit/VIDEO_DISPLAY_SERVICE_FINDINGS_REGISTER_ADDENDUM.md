# VideoDisplayService findings register addendum

Status: Deep Read Pass 2 completed for VDS V1.0 and VDS V2.0. Choice-notation interpretation corrected 2026-08-29. VDS-002/VDS-003/VDS-004 remain fresh-read and executable-confirmed for the exact official V2.0 schema family.

Authority rule:

```text
VDS V1.0 PDF: official public VDV writing; exact strict V1.0 service XSD unresolved.
Do not substitute V2.0 for V1.0.
VDS V2.0 strict validation: official VDV-301-2.0 service XSD + Common V2.0 + Enums V2.0.
Official and integration VDS V2.0 service-XSD Git blob: fcfdadd3b62a584370cae326004050b4dc832e23.
```

Choice-notation correction:

```text
VDV 301-2 V2.0 section 6.1.3.3 defines a prefixed minus sign as XML-choice notation.
-1:1 is not an invalid/negative cardinality.
Historical VDS-006 wording is superseded.
See AUDIT_CORRECTION_DELTA_CHOICE_NOTATION_2026-08-29.md.
```

## VDS-001 - V1.0 public PDF without confirmed exact official service XSD

```text
classification: schema_family_or_provenance_gap
scope: V1.0
state: strongly confirmed for checked official repository history
confidence: very high
validation: strict V1.0 XSD profile unresolved
```

## VDS-002 - ListViewCapabilitiesResponse compositor

```text
classification: xsd_structure_modelling_error_candidate
scope: official V2.0
state: fresh PDF/XSD + executable-confirmed
confidence: very high
```

Corrected visible V2.0 PDF reading:

```text
ViewID       1:1
ViewName     1:1
a  ViewType  -1:1
```

The leading minus on `ViewType` is valid VDV choice notation. It does **not** make `ViewID` or `ViewName` choice alternatives; those rows remain ordinary mandatory fields in the visible table.

The exact official V2.0 XSD instead declares:

```text
xs:choice(ViewID | ViewName | ViewType)
```

EV-103:

```text
single ViewID: valid
ViewID + ViewName + ViewType: rejected; ViewName not expected
run: 33111119723
```

Therefore VDS-002 remains executable-confirmed and does not depend on treating `-1:1` as malformed.

## VDS-003 - SetVideoViewRequest compositor

```text
classification: xsd_structure_modelling_error_candidate
scope: official V2.0
state: fresh PDF/XSD + executable-confirmed
confidence: very high
```

Visible V2.0 PDF:

```text
ViewID   1:1
Timeout  1:1
```

Official V2.0 XSD:

```text
xs:choice(ViewID | Timeout)
```

EV-103 confirms `ViewID + Timeout` is rejected. This finding is unaffected by the choice-notation correction.

## VDS-004 - response compositor family

```text
classification: xsd_structure_modelling_error_candidate
scope: official V2.0
state: fresh PDF/XSD + executable-confirmed
confidence: very high
```

Corrected visible PDF reading includes examples such as:

```text
SetVideoViewResponse:
a  State                  -1:1
   CurrentViewID           1:1
   OperationErrorMessage   0:1

SetNextViewIndexResponse:
a  State                  -1:1
   OperationErrorMessage   0:1

GetDisplayStateResponse:
a  State                  -1:1
   CurrentViewID           1:1
   OperationErrorMessage   0:1
```

The minus marker on `State` is valid choice notation. The surrounding `CurrentViewID` / `OperationErrorMessage` rows are ordinary non-choice multiplicities in the visible PDF.

The exact official V2.0 XSD instead places all listed members of each response inside one `xs:choice`.

EV-103 confirms representative combinations are rejected after the first choice member. VDS-004 therefore remains executable-confirmed.

## VDS-005 - broken generated Word cross references

```text
classification: pdf_table_or_documentation_error_candidate
scope: V1.0 PDF
state: visually confirmed in V1.0; corrected/absent in V2.0
```

## VDS-006 - choice-notation application anomaly (refined)

```text
old classification: invalid printed -1:1 cardinality notation
state: finding_refined
classification: pdf_choice_notation_application_anomaly_candidate
confidence: high
scope: V1.0/V2.0 PDF
```

The old premise is rejected: `-1:1` is a valid VDV XML-choice notation form.

The remaining issue is the *application/presentation* in the checked VideoDisplay tables. Visible examples show a single lower-case `a` choice label on an enum-valued row such as `ViewType` or `State`, but no visible peer `b` alternative in the same structure, while surrounding rows carry ordinary `1:1` or `0:1` multiplicities.

Example:

```text
ViewID       1:1
ViewName     1:1
a  ViewType  -1:1
```

and:

```text
a  State                  -1:1
   CurrentViewID           1:1
   OperationErrorMessage   0:1
```

Therefore:

```text
Do not call -1:1 invalid.
Do not infer a negative minimum.
Treat the visible single-alternative choice presentation as incomplete/degenerate choice-notation application.
Use the selected XSD for executable compositor semantics.
```

VDS-006 is documentation-only and remains separate from VDS-002/VDS-004.

## VDS-007 - neighboring documents label VideoDisplayService as v1.1

```text
classification: pdf_reference_version_label_error_candidate
state: cross-document confirmed
```

The official VDV catalog identifies the 05/2017 VDV 301-2-13 publication as VideoDisplayService V1.0. Neighboring VLS/VRS reference sections label it `v1.1`. No VDS V1.1 schema/profile alias is created.

## VDS-008 - incorrect RTP and SOA abbreviation expansions

```text
classification: pdf_protocol_or_architecture_abbreviation_error_candidate
scope: V1.0/V2.0 PDF
state: visually confirmed in V2.0; textually confirmed in V1.0
```

VDS prints:

```text
RTP  Real Time Protocol
SOA  Server Oriented Architecture
```

External standard terminology uses RTP as the real-time transport protocol and SOA as Service Oriented Architecture. This has no XML/XSD impact.

## Visual evidence

```text
VDS V1.0
source SHA-256: 9280cc239cf71bb158ab5941b522a2c4c822420e07ed44f4d4111d9689418480
render run: 33225843645

VDS V2.0
source SHA-256: c287df20d8225af2afcd37dfdb487eb4922b89ce78c287da91745d12b410c8a2
render run: 33226294383
```

## Executable evidence

```text
EV-103
run: 33111119723
status: PASS
```

## Current finding state

```text
VDS-001 strongly confirmed V1.0 provenance gap
VDS-002 executable-confirmed; PDF reading refined using correct choice notation
VDS-003 executable-confirmed; unaffected by correction
VDS-004 executable-confirmed; PDF reading refined using correct choice notation
VDS-005 V1.0-only, corrected in V2.0
VDS-006 refined: choice-notation application anomaly, NOT invalid cardinality
VDS-007 cross-document V1.1 label error confirmed
VDS-008 RTP/SOA abbreviation expansion error
```

No XSD correction is made.
