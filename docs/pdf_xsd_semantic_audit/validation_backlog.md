# PDF/XSD semantic audit validation backlog

Status: started.

## Local technical validation backlog

These checks require a local checkout or downloaded XSD pool.

### VB-001 - compile common/enums pool

Scope:

```text
IBIS-IP_common_V2.1.xsd + IBIS-IP_Enumerations_V2.1.xsd
IBIS-IP_common_V2.2.xsd + IBIS-IP_Enumerations_V2.2.xsd
IBIS-IP_common_V2.3.xsd + IBIS-IP_Enumerations_V2.2.xsd
IBIS-IP_common_V2.4.xsd + IBIS-IP_Enumerations_V2.4.xsd
```

Goal:

```text
All includes resolve.
No duplicate type definition conflicts within a selected version pool.
XSD parser accepts every selected schema.
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
Confirm TVS V2.4 compiles with the V2.4 dependency pool.
Validate targeted positive/negative samples for the V2.4 GetCurrentShortHaulStops operation.
Cross-check top-level TicketValidationService.* elements against TicketValidationServiceOperations group.
Validate that VehicleData.RouteDeviation follows RouteDeviationEnumeration as required by XSD.
```

Initial sample ideas:

```text
Positive: GetCurrentShortHaulStopsResponse with no CurrentTariffStop entries.
Positive: GetCurrentShortHaulStopsResponse with multiple CurrentTariffStop entries.
Operation inventory check: top-level GetCurrentShortHaulStopsResponse is absent from TicketValidationServiceOperations group.
VehicleData sample: RouteDeviationEnumeration value accepted where XSD expects RouteDeviationEnumeration.
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

Resolution:

| Name | Classification | Follow-up |
|---|---|---|
| NetworkLocationPoint | service-specific / older V1.0 NetworkLocation scope | NetworkLocationService V1.0 audit |
| PassengerCounting | service-specific PCS scope | PassengerCountingService V2.1 audit |
| PassengerCountingData | service-specific PCS scope | PassengerCountingService V2.1 audit |
| PathDestination | field-level TripInformation usage | already covered as PathDestinationNumber |
| Route | service-specific JourneyInformation element using TripInformationStructure | JourneyInformationService V1.0 audit |
| OperationalInformation | not confirmed / routing note only | revisit only with concrete PDF/XSD evidence |

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

Source:

```text
docs/pdf_xsd_semantic_audit/03_tvs_v2_2_v2_3_v2_4_include_semantic_audit.md
```

Status:

```text
Completed first pass.
TVS V2.2 -> V2.3: no schema delta observed; V2.3 treated as PDF/documentation correction.
TVS V2.4: new GetCurrentShortHaulStops response/data structure present and aligned with PDF table intent.
TVS-001 opened: new V2.4 operation absent from TicketValidationServiceOperations group.
TVS-002 opened: VehicleData.RouteDeviation PDF type name RouteDirectionEnumeration vs XSD RouteDeviationEnumeration.
No XSD changes made.
```

Follow-up:

```text
Run VB-006 later.
Consider TVS-001 as possible narrow official correction PR candidate only after full audit and validation.
Continue with next non-visual service block, recommended: CustomerInformationService V2.3/V2.4.
```
