# Common/Enums historical audit V1.0 -> V2.4 plan

Status: started, plan established.

Scope:

```text
VDV 301-2-1 Common Data Structures and Enumerations
PDF versions: V1.0, V2.0, V2.1, V2.2, V2.3, V2.4
XSD family in dev/schema-integration:
  IBIS-IP_common_V1.0.xsd
  IBIS-IP_common_V2.0.xsd
  IBIS-IP_common_V2.1.xsd
  IBIS-IP_common_V2.2.xsd
  IBIS-IP_common_V2.3.xsd
  IBIS-IP_common_V2.4.xsd
  IBIS-IP_Enumerations_V1.0.xsd
  IBIS-IP_Enumerations_V2.0.xsd
  IBIS-IP_Enumerations_V2.1.xsd
  IBIS-IP_Enumerations_V2.2.xsd
  IBIS-IP_Enumerations_V2.4.xsd
```

Known structural gap to classify:

```text
No IBIS-IP_Enumerations_V2.3.xsd is observed in dev/schema-integration.
IBIS-IP_common_V2.3.xsd currently uses the V2.2 enumeration dependency family.
This is already tracked as CE-001 and must be resolved historically, not guessed.
```

## Why this block comes before most service audits

Common/Enums structures and values are reused by many services.

Examples already encountered:

```text
TripInformationStructure
StopInformationStructure
LineInformationStructure
DeviceStateEnumeration
VehicleModeEnumeration
RouteDeviationEnumeration
ServiceNameEnumeration
```

If a mismatch originates in Common/Enums, it should be recorded once as a Common/Enums finding and referenced by dependent service audits instead of duplicated as a service defect.

## Mixed-version validation impact

This historical block implements the mixed-version validation premise:

```text
Older service payloads must be validated against the Common/Enums version family actually used by that service version.
The newest V2.4 definitions must not be applied globally to older services.
```

See:

```text
docs/pdf_xsd_semantic_audit/MIXED_VERSION_VALIDATION_PREMISE.md
```

## Work phases

### Phase 1 - XSD-side version inventory

Create or extend reproducible inventories for each observed Common/Enums version:

```text
common structures by version
common wrapper datatypes by version
enumeration values by version
include/dependency family by version
```

Existing V2.4 inventories remain valid but should be expanded backwards.

### Phase 2 - PDF-side version inventory

For each PDF version, extract/check:

```text
version history
common datatype tables
common data-structure tables
common enumeration tables
explicit corrections and deprecations
```

When PDF extraction may distort spelling/casing, mark as visual confirmation required instead of opening a final finding.

### Phase 3 - pairwise PDF/XSD checks

For each version:

```text
V1.0 PDF -> V1.0 XSD family
V2.0 PDF -> V2.0 XSD family
V2.1 PDF -> V2.1 XSD family
V2.2 PDF -> V2.2 XSD family
V2.3 PDF -> V2.3 available XSD family / V2.2 enum dependency, to be classified
V2.4 PDF -> V2.4 XSD family
```

### Phase 4 - historical delta chain

Compare each transition:

```text
V1.0 -> V2.0
V2.0 -> V2.1
V2.1 -> V2.2
V2.2 -> V2.3
V2.3 -> V2.4
```

The goal is to determine whether each current finding is:

```text
new in V2.4
inherited from older XSDs
introduced by a PDF table update
introduced by a dependency-family change
candidate/fork/integration-only
```

### Phase 5 - finding range update

Every CE finding must receive a clear version range where possible:

```text
affected version(s)
first observed version
last observed version
status in later versions
validation consequence by version
```

## Initial target findings for historical closure

Prioritise known Common/Enums findings first:

```text
CE-001 Enumerations V2.3 file absent / common V2.3 uses Enumerations V2.2.
CE-004 ServiceNameEnumeration V2.4 table vs XSD/history discrepancy.
CE-005 TripInformation.AdditionalTextMessage cardinality across V2.0-V2.4.
CE-006 DeviceStateEnumeration XSD-only warning value.
CE-007 / CE-008 enum case mismatches.
CE-009 RailSubmodeEnumeration specialRail vs specialTrain.
CE-010 AirSubmodeEnumeration canalBarge XSD-only.
CE-011 Connection TransportMode/ConnectionMode cardinality.
CE-012 DeviceSpecificationWithStateList cardinality.
CE-013 AdditionalAnnouncement choice naming/cardinality.
CE-014 DataVersionList cardinality.
CE-015 / CE-017 visual checks remain deferred until manual review is possible.
```

## File sequence

Recommended detailed files:

```text
04a_common_enums_v1_0_v2_0_history.md
04b_common_enums_v2_0_v2_1_history.md
04c_common_enums_v2_1_v2_2_history.md
04d_common_enums_v2_2_v2_3_history.md
04e_common_enums_v2_3_v2_4_history.md
04f_common_enums_historical_findings_closure.md
```

## First concrete next file

```text
docs/pdf_xsd_semantic_audit/04a_common_enums_v1_0_v2_0_history.md
```

Goal:

```text
Establish the V1.0 and V2.0 XSD-side baseline and start the PDF/XSD historical comparison without opening findings prematurely.
```