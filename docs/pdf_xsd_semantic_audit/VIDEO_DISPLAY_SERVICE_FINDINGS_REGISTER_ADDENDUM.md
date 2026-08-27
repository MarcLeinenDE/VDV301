# VideoDisplayService findings register addendum

Status: V1.0/V2.0 first-pass closure completed. VDS-002/VDS-003/VDS-004 are now executable-confirmed for official V2.0.

## VDS-001

```text
classification: schema_family_or_provenance_gap
scope: V1.0
validation: strict XSD profile unresolved
```

## VDS-002

```text
classification: xsd_structure_modelling_error_candidate
scope: V2.0 official
state: executable-confirmed
observation: ListViewCapabilitiesResponse PDF combines ViewID/ViewName/ViewType; XSD uses xs:choice
```

Executable evidence:

```text
single ViewID: valid
ViewID + ViewName + ViewType: rejected; ViewName not expected
```

## VDS-003

```text
classification: xsd_structure_modelling_error_candidate
scope: V2.0 official
state: executable-confirmed
observation: SetVideoViewRequest PDF requires ViewID + Timeout; XSD allows one via xs:choice
```

Executable evidence:

```text
ViewID only: valid
ViewID + Timeout: rejected; Timeout not expected
```

## VDS-004

```text
classification: xsd_structure_modelling_error_candidate
scope: V2.0 official
state: executable-confirmed
observation: response family PDFs combine state/current-view/error fields; XSD uses xs:choice
```

Executable evidence:

```text
SetVideoViewResponse State only: valid
SetVideoViewResponse State + CurrentViewID: rejected
GetDisplayStateResponse State only: valid
GetDisplayStateResponse State + CurrentViewID: rejected
SetNextViewIndexResponse State only: valid
SetNextViewIndexResponse State + OperationErrorMessage: rejected
```

Evidence source for VDS-002/003/004:

```text
GitHub Actions run 33111119723
head d4ffe09067cb38bf7f78ba295e029902078ed18d
docs/pdf_xsd_semantic_audit/24c_executable_validation_video_compositors.md
EV-103 status: PASS
```

## VDS-005

```text
classification: pdf_table_or_documentation_error_candidate
scope: V1.0 PDF
observation: unresolved Word cross-reference text
validation impact: none
```
