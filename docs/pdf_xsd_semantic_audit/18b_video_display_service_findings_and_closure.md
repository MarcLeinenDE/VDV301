# VideoDisplayService findings and first-pass closure

Status: semantic/provenance first-pass closure completed. Local XSD compilation/sample validation remains pending.

## Routing closure

### V1.0

```text
Public VDV 301-2-13 document exists.
No official release-tag VideoDisplayService V1.0 XSD found.
Strict XSD routing unresolved.
Do not map to V2.0.
```

### V2.0

```text
Official XSD: IBIS-IP_VideoDisplayService_V2.0.xsd
Blob: fcfdadd3b62a584370cae326004050b4dc832e23
Pool: Common V2.0 + Enumerations V2.0
Current upstream master remains identical.
```

## Findings

```text
VDS-001  schema_family_or_provenance_gap
         V1.0 public PDF without official-tag service XSD

VDS-002  xsd_structure_modelling_error_candidate
         ListViewCapabilitiesResponse: PDF combined ViewID/ViewName/ViewType vs XSD xs:choice

VDS-003  xsd_structure_modelling_error_candidate
         SetVideoViewRequest: PDF requires ViewID + Timeout vs XSD xs:choice

VDS-004  xsd_structure_modelling_error_candidate
         SetVideoViewResponse/GetDisplayStateResponse/SetNextViewIndexResponse PDF combined state fields vs XSD xs:choice family

VDS-005  pdf_table_or_documentation_error_candidate
         V1.0 unresolved Word cross-reference text
```

## SDK implications

```text
- V1.0 remains public-document-known but strict-XSD-unresolved.
- V2.0 exact pool is Common/Enums V2.0.
- Do not interpret V2.0 document compatibility with VDV301 V1.0 as permission to validate V1.0 traffic against V2.0 XSD.
- Explain compositor mismatches in diagnostics while still enforcing exact XSD semantics.
- Media/display runtime behavior remains a separate test layer from XML validation.
```

## Validation status

```text
Semantic/provenance first pass: closed.
Local XSD compilation: not performed.
Sample XML validation: not performed.
No XSD correction: yes.
No upstream PR/comment/merge action: yes.
```

## Next planned block

```text
19_train_set_services_historical_start.md
VDV 301-2-14 TrainSet services V2.1 / V2.2
```
