# VideoDisplayService findings register addendum

Status: V1.0/V2.0 first-pass closure completed.

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
observation: ListViewCapabilitiesResponse PDF combines ViewID/ViewName/ViewType; XSD uses xs:choice
```

## VDS-003

```text
classification: xsd_structure_modelling_error_candidate
scope: V2.0 official
observation: SetVideoViewRequest PDF requires ViewID + Timeout; XSD allows one via xs:choice
```

## VDS-004

```text
classification: xsd_structure_modelling_error_candidate
scope: V2.0 official
observation: response family PDFs combine state/current-view/error fields; XSD uses xs:choice
```

## VDS-005

```text
classification: pdf_table_or_documentation_error_candidate
scope: V1.0 PDF
observation: unresolved Word cross-reference text
validation impact: none
```
