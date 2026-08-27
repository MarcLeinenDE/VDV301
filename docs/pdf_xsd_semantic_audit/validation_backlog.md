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
TripInformation with BlockNumber / ExternalVehicleJourneyRef
DoorCountingObjectClassEnumeration with Wheelchair
```

### VB-003 - version-family include verification

Goal:

```text
Confirm and preserve version-specific dependency facts.
Current important result: Common V2.3 intentionally uses Enumerations V2.2 in this audit branch.
V2.4 uses Common V2.4 + Enumerations V2.4.
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
No latest-wins validation.
No global Common/Enums substitution.
```

### VB-008 - Common/Enums V1.0 and V2.0 schema compile

Source:

```text
docs/pdf_xsd_semantic_audit/04a_common_enums_v1_0_v2_0_history.md
```

Goal:

```text
Compile V1.0 and V2.0 pools separately.
Add targeted samples for DeviceState readyForShutdown and DataIntervall/DataInterval naming if referenced by service schemas.
```

### VB-009 - Common/Enums V2.1 and V2.2 targeted validation

Source:

```text
docs/pdf_xsd_semantic_audit/04b_common_enums_v2_0_v2_1_history.md
docs/pdf_xsd_semantic_audit/04c_common_enums_v2_1_v2_2_history.md
```

Initial samples:

```text
V2.0 negative / V2.1 positive: MultiFunctionalDisplay.
V2.0 negative / V2.1 positive: OperationNotSupported.
V2.1 negative / V2.2 positive: CombiDevice.
V2.1 negative / V2.2 positive: SystemMonitoringService.
V2.1 positive / V2.2 negative: SystemDocumentationService.
V2.2 positive but PDF-note: DeviceStateEnumeration warning.
V2.2 specialRail negative / specialTrain positive.
```

### VB-010 - Common/Enums V2.3 and V2.4 closure validation

Source:

```text
docs/pdf_xsd_semantic_audit/04d_common_enums_v2_2_v2_3_history.md
docs/pdf_xsd_semantic_audit/04e_common_enums_v2_3_v2_4_history_and_closure.md
```

Scope:

```text
Common/Enums V2.3 pool:
  IBIS-IP_common_V2.3.xsd
  IBIS-IP_Enumerations_V2.2.xsd

Common/Enums V2.4 pool:
  IBIS-IP_common_V2.4.xsd
  IBIS-IP_Enumerations_V2.4.xsd
```

Initial samples:

```text
V2.2 negative / V2.3 positive: DisplayContent.AdditionalInformation1.
V2.2 negative / V2.3 positive: StopInformation.ArrivalExpected.
V2.3 negative / V2.4 positive: LineInformation.LinePublicCode.
V2.3 negative / V2.4 positive: StopInformation.StopGlobalID.
V2.3 negative / V2.4 positive: TripInformation.BlockNumber.
V2.3 negative / V2.4 positive: ServiceNameEnumeration AnalogRadioService.
V2.3 positive / V2.4 negative: DoorCountingObjectClassEnumeration WheelChair.
V2.3 negative / V2.4 positive: DoorCountingObjectClassEnumeration Wheelchair.
V2.4 positive with PDF note: AirSubmodeEnumeration canalBarge.
```

## Semantic audit backlog

### SB-001 - Common/Enums V2.4 affected table check

Status:

```text
Covered in first-pass Common/Enums V2.4 audit files; keep open for later local validation closure.
```

### SB-002 - Common/Enums V2.3 affected table check

Status:

```text
Covered by 04d first pass; local validation remains.
```

### SB-003 - Common/Enums V2.2 affected table check

Status:

```text
Covered by 04c first pass; local validation remains.
```

### SB-004 - Common/Enums V2.1 affected table check

Status:

```text
Covered by 04b first pass; local validation remains.
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
```

### SB-010 - TVS V2.2 / V2.3 / V2.4 include and semantic history

Status:

```text
Completed first pass.
TVS-001 and TVS-002 opened.
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
First-pass chain completed in 04a through 04e.
CE-001 closed as OK with note.
No XSD correction proposed by the historical closure.
Local compile/sample validation remains in VB-001/VB-008/VB-009/VB-010.
```

Sources:

```text
docs/pdf_xsd_semantic_audit/04_common_enums_historical_v1_0_to_v2_4_plan.md
docs/pdf_xsd_semantic_audit/04a_common_enums_v1_0_v2_0_history.md
docs/pdf_xsd_semantic_audit/04b_common_enums_v2_0_v2_1_history.md
docs/pdf_xsd_semantic_audit/04c_common_enums_v2_1_v2_2_history.md
docs/pdf_xsd_semantic_audit/04d_common_enums_v2_2_v2_3_history.md
docs/pdf_xsd_semantic_audit/04e_common_enums_v2_3_v2_4_history_and_closure.md
```

### SB-013 - mixed-version validation premise

Status:

```text
Added as audit premise.
Use it when classifying every PDF/XSD version pair and when designing later SDK validation behaviour.
```

### SB-014 - CustomerInformationService historical audit

Status:

```text
Next recommended service-level block after Common/Enums foundation closure.
```

Initial goal:

```text
Map public CIS PDF versions against observed CIS XSD files.
Identify dependency pool per CIS version.
Compare PDF/XSD facts per version without latest-wins assumptions.
```
