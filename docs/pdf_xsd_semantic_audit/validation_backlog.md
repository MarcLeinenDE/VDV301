# PDF/XSD semantic audit validation backlog

Status: started.

## Local technical validation backlog

These checks require a local checkout or downloaded XSD pool.

### VB-001 - compile common/enums pool

Scope:

```text
IBIS-IP_common_V1.0.xsd + IBIS-IP_Enumerations_V1.0.xsd
IBIS-IP_common_V2.0.xsd + IBIS-IP_Enumerations_V2.0.xsd
IBIS-IP_common_V2.1.xsd + IBIS-IP_Enumerations_V2.1.xsd
IBIS-IP_common_V2.2.xsd + IBIS-IP_Enumerations_V2.2.xsd
IBIS-IP_common_V2.3.xsd + IBIS-IP_Enumerations_V2.2.xsd
IBIS-IP_common_V2.4.xsd + IBIS-IP_Enumerations_V2.4.xsd
```

Goal:

```text
All includes resolve per selected version pool.
No duplicate type definition conflicts within a selected version pool.
XSD parser accepts every selected schema.
Do not mix pools unless the selected service version explicitly does so.
```

### VB-002 - targeted XML samples for Common/Enums V2.4

Initial sample structures:

```text
LineInformation with LinePublicCode / LineSymbolText / ExternalLineRef
StopInformation with StopShortName / StopLongNo / PointNumber / StopGlobalID / StopPointGlobalID
TripInformation with BlockNumber
DoorCountingObjectClassEnumeration with Wheelchair
```

### VB-003 - version-family include verification

Goal:

```text
Confirm whether common V2.3 intentionally uses Enumerations V2.2.
Confirm V2.4 service candidates consistently use common V2.4 / Enumerations V2.4 when semantically required.
Record every mixed dependency family as a version-specific fact, not as a global defect.
```

### VB-004 - end-of-audit local validation for official PR candidates

Source:

```text
docs/pdf_xsd_semantic_audit/OFFICIAL_PR_CANDIDATES_AFTER_AUDIT.md
```

Goal:

```text
Before any official correction PR is prepared, run local XSD compilation and targeted positive/negative XML validation for the exact proposed change.
```

### VB-005 - DMS V2.4 schema compile and targeted samples

Source:

```text
docs/pdf_xsd_semantic_audit/02_dms_v2_4_pdf_xsd_audit.md
docs/pdf_xsd_semantic_audit/02a_dms_v2_2_v2_3_v2_4_history_compare.md
```

Scope:

```text
IBIS-IP_DeviceManagementService_V2.4.xsd
IBIS-IP_common_V2.4.xsd
IBIS-IP_Enumerations_V2.4.xsd
```

Initial sample ideas:

```text
Positive: GetDeviceErrorMessagesResponseData with no ErrorMessage.
Positive: SubdeviceErrorMessages with no ErrorMessage.
Positive: InstallUpdateRequest without UpdateURL.
Positive: DeviceStatus with only DeviceStatusName and DeviceStatusFlag.
Negative: UpdateStateData missing required UpdateTimestamp.
Negative: UpdateHistoryEntry missing required UpdateURL.
```

### VB-006 - TVS V2.4 schema compile, samples and operation inventory

Source:

```text
docs/pdf_xsd_semantic_audit/03_tvs_v2_2_v2_3_v2_4_include_semantic_audit.md
```

Scope:

```text
IBIS-IP_TicketValidationService_V2.4.xsd
IBIS-IP_common_V2.4.xsd
IBIS-IP_Enumerations_V2.4.xsd
```

Goal:

```text
Confirm TVS V2.4 compiles with the selected V2.4 dependency pool.
Validate targeted positive/negative samples for the V2.4 GetCurrentShortHaulStops operation.
Cross-check top-level TicketValidationService.* elements against TicketValidationServiceOperations group.
Validate that VehicleData.RouteDeviation follows RouteDeviationEnumeration as required by XSD.
```

### VB-007 - mixed-version validation matrix

Source:

```text
docs/pdf_xsd_semantic_audit/MIXED_VERSION_VALIDATION_PREMISE.md
docs/pdf_xsd_semantic_audit/AUDIT_SCOPE_MATRIX.md
```

Goal:

```text
Create a later executable validation matrix that maps each service/version to its exact XSD dependency pool.
```

Required properties:

```text
No latest-wins validation.
No global Common/Enums substitution.
Each service payload is validated against the selected service version and dependency pool.
Special/no-XSD services are marked explicitly instead of failing as missing files.
```

### VB-008 - Common/Enums V1.0 and V2.0 schema compile

Source:

```text
docs/pdf_xsd_semantic_audit/04a_common_enums_v1_0_v2_0_history.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v1_0_v2_0_xsd_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v1_0_vs_v2_0_xsd_diff.csv
```

Scope:

```text
Common/Enums V1.0 pool:
  IBIS-IP_common_V1.0.xsd
  IBIS-IP_Enumerations_V1.0.xsd

Common/Enums V2.0 pool:
  IBIS-IP_common_V2.0.xsd
  IBIS-IP_Enumerations_V2.0.xsd
```

Goal:

```text
Compile V1.0 and V2.0 pools separately.
Do not mix V1.0 and V2.0 Common/Enums definitions.
Later add targeted samples for deltas such as DeviceStateEnumeration readyForShutdown and DataIntervall/DataInterval type naming if referenced by service schemas.
```

## Semantic audit backlog

### SB-001 - Common/Enums V2.4 affected table check

Status:

```text
Covered in first-pass Common/Enums V2.4 audit files; keep open for later history/validation closure.
```

### SB-002 - Common/Enums V2.3 affected table check

Tables/sections:

```text
DisplayContent
StopInformation
StopInformationRequest
TripInformation
```

### SB-003 - Common/Enums V2.2 affected table check

Tables/sections:

```text
DisplayContent / LineCode area
TripStateEnumeration
Connection / ConnectionMode / NetexMode
Mode/SubMode enumerations
DeviceClassEnumeration
ServiceNameEnumeration
```

### SB-004 - Common/Enums V2.1 affected table check

Tables/sections:

```text
DeviceClassEnumeration
ErrorCodeEnumeration
ServiceNameEnumeration
InternationalTextType
DestinationStructure
DisplayContent
```

### SB-005 - Common/Enums V2.4 deferred structure-name scope resolution

Status:

```text
Resolved for Common/Enums V2.4 first-pass closure.
No new CE finding opened.
```

### SB-006 - visual PDF confirmation for spelling/casing candidates

Status:

```text
Deferred by user request because visual checks require the user's personal/manual review.
Do not block other non-visual audit work on SB-006.
```

Pending visual checks:

```text
CE-015 FareZoneInformation Farezone* vs FareZone* casing.
CE-017 TSPPoint Desciption vs expected Description spelling.
ZoneType first-field casing/spelling if PDF differs from XSD FarezoneTypeID.
```

### SB-007 - post-audit official PR candidate review

Goal:

```text
At the end of the full PDF/XSD audit, review all CE/TVS/service findings and decide whether any minimal official-facing PRs should be prepared.
No official PR is opened from this register during the audit.
```

### SB-008 - DMS V2.4 semantic audit

Status:

```text
Started; first pass completed for the V2.4 documented technical correction scope.
No new DMS-specific CE finding opened in the first pass.
```

### SB-009 - DMS V2.2 / V2.3 / V2.4 history comparison

Status:

```text
Completed first pass.
No new DMS-specific CE finding opened.
DMS V2.4 candidate remains limited to the documented DMS V2.4 technical correction scope plus V2.4 dependency-family alignment.
DMS V2.3 remains labelled as integration/fork/candidate comparison material, not an official authority.
```

### SB-010 - TVS V2.2 / V2.3 / V2.4 include and semantic history

Status:

```text
Completed first pass.
TVS V2.2 -> V2.3: no schema delta observed; V2.3 treated as PDF/documentation correction.
TVS V2.4: new GetCurrentShortHaulStops response/data structure present and aligned with PDF table intent.
TVS-001 opened: new V2.4 operation absent from TicketValidationServiceOperations group.
TVS-002 opened: VehicleData.RouteDeviation PDF type name RouteDirectionEnumeration vs XSD RouteDeviationEnumeration.
No XSD changes made.
```

### SB-011 - Audit scope matrix

Status:

```text
Initial matrix created.
Use as master checklist for full VDV301 PDF/XSD audit coverage.
```

### SB-012 - Common/Enums historical audit V1.0 -> V2.4

Status:

```text
Started.
Plan file created.
V1.0 -> V2.0 XSD-side enumeration inventory and first diff completed.
PDF-side V1.0/V2.0 check pending.
```

Sources:

```text
docs/pdf_xsd_semantic_audit/04_common_enums_historical_v1_0_to_v2_4_plan.md
docs/pdf_xsd_semantic_audit/04a_common_enums_v1_0_v2_0_history.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v1_0_v2_0_xsd_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v1_0_vs_v2_0_xsd_diff.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v1_0_vs_v2_0_xsd_diff.md
```

Current result:

```text
No new CE finding opened yet.
Recorded XSD-side deltas include DataIntervall -> DataInterval naming, DeviceState readyForShutdown, RouteDirectionEnumeration, ServiceName video additions, PassengerCountingService and ServiceState starting.
These deltas require V1.0/V2.0 PDF-side confirmation before findings or version-range updates.
```

### SB-013 - mixed-version validation premise

Source:

```text
docs/pdf_xsd_semantic_audit/MIXED_VERSION_VALIDATION_PREMISE.md
```

Status:

```text
Added as audit premise.
Use it when classifying every PDF/XSD version pair and when designing later SDK validation behaviour.
```

Key rule:

```text
Every service version must remain independently auditable and validatable against its own selected XSD dependency pool.
Do not use latest-version schema rules globally.
```