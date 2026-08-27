# Common/Enums V2.1 -> V2.2 history audit

Status: XSD-side enumeration diff and PDF-side first pass completed.

Scope:

```text
IBIS-IP_common_V2.1.xsd
IBIS-IP_Enumerations_V2.1.xsd
IBIS-IP_common_V2.2.xsd
IBIS-IP_Enumerations_V2.2.xsd
VDV 301-2-1 Common Data Structures and Enumerations V2.2 PDF source
```

Authority rule:

```text
Validation follows the selected version's XSD family.
PDF differences are retained as provider-facing explanation notes.
No schema change is made during this audit pass.
```

Mixed-version rule:

```text
Do not apply V2.2 Common/Enums definitions to a V2.1 service payload unless the selected service/dependency pool actually uses V2.2.
V2.1 and V2.2 must stay separately validatable.
```

## 1. XSD dependency family observation

### Common/Enums V2.1

Observed:

```text
IBIS-IP_common_V2.1.xsd includes IBIS-IP_Enumerations_V2.1.xsd.
```

### Common/Enums V2.2

Observed:

```text
IBIS-IP_common_V2.2.xsd includes IBIS-IP_Enumerations_V2.2.xsd.
```

Initial result:

```text
V2.1 and V2.2 each have their own common/enumeration dependency family in the branch.
No V2.1/V2.2 include-family mismatch is opened in this observation.
```

## 2. XSD enumeration diff

Created diff files:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_1_vs_v2_2_xsd_diff.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_1_vs_v2_2_xsd_diff.md
```

Observed XSD-side deltas:

| Change | V2.1 | V2.2 | Status | Notes |
|---|---|---|---|---|
| DeviceClass value added | - | `CombiDevice` | confirmed XSD delta | V2.2 PDF history/table confirms. |
| DeviceState value added | - | `warning` | confirmed XSD delta, PDF-table gap | V2.2 PDF table does not list `warning`; supports CE-006 historical origin. |
| ServiceName value removed | `SystemDocumentationService` | - | confirmed XSD delta | V2.2 version history says removed; PDF table still prints it. Supports CE-004. |
| ServiceName value removed | `SystemManagementService` | - | confirmed XSD delta | V2.2 version history says removed; PDF table still prints it. Supports CE-004. |
| ServiceName value added | - | `SystemMonitoringService` | confirmed XSD delta | V2.2 history/table and XSD confirm. |
| Type added | - | `TripStateEnumeration` | confirmed XSD delta | V2.2 history/table and XSD confirm. |
| NetexMode-related enumerations added | - | sections/types 3.28-3.40 | confirmed XSD delta | V2.2 history/table and XSD confirm mode/submode introduction. |

## 3. V2.2 PDF-side first pass

The opened V2.2 PDF identifies itself as:

```text
VDV-Schrift 301-2-1
08/2019
Common Data Structures and Enumerations
V2.2
```

The V2.2 version history confirms these functional changes:

```text
LineCode newly integrated into DisplayContent.
TripStateEnumeration newly added.
ConnectionMode newly integrated, including NetexMode and corresponding enumerations.
NetexMode added as new datatype.
NetexMode added as new element in Connection; TransportMode is deprecated for modal information.
Sections 3.28 to 3.40 added for modes and submodes.
CombiDevice added as a new DeviceClass.
SystemDocumentationService and SystemManagementService deleted.
SystemMonitoringService added in ServiceNameEnumeration.
```

The V2.2 version history also documents technical corrections:

```text
Info at TransportMode to use ConnectionMode instead.
Heartbeat.
```

## 4. PDF tables checked in this pass

The V2.2 PDF tables confirm:

```text
DeviceClassEnumeration includes CombiDevice.
TripStateEnumeration is present with EmptyRun, OnTrip, OffTrip, TripBreak, OffDuty, unknown.
NetexMode and mode/submode enumerations are present.
ServiceNameEnumeration includes SystemMonitoringService.
```

The V2.2 PDF tables also expose or keep visible already-known PDF/XSD gaps:

```text
DeviceStateEnumeration table lists defective, notavailable, running, readyForShutdown, but V2.2 XSD also contains warning.
ServiceNameEnumeration table still prints SystemDocumentationService and SystemManagementService although V2.2 history and XSD remove them.
TicketValidationEnumeration is printed as Valid while XSD uses valid.
VehicleModeEnumeration is printed as Air while XSD uses air.
GNSSTypeEnumeration is printed as Other while XSD uses other.
RailSubmodeEnumeration table prints specialRail while XSD contains specialTrain.
FunicularSubmodeEnumeration table prints Unknown while XSD uses unknown.
TaxiSubmodeEnumeration table prints Unknown / Undefined / minicab while XSD uses lower-case/camel-case forms in the checked XSD inventories.
AirSubmodeEnumeration table does not show canalBarge; exact XSD-history origin is carried to closure.
```

## 5. Classification

| Topic | First-pass classification | Finding impact |
|---|---|---|
| V2.2 include family | V2.2 common includes V2.2 enumerations. | No CE. |
| `CombiDevice` | V2.2 PDF and V2.2 XSD align. | No CE. |
| `TripStateEnumeration` | V2.2 PDF and V2.2 XSD align. | No CE. |
| `NetexMode` / mode-submode enumerations | V2.2 PDF and XSD align at introduction level. | No new CE for existence. Existing value-level CE-008/CE-009/CE-010 receive historical context. |
| `SystemMonitoringService` | V2.2 PDF table and XSD align for addition. | No CE for addition. |
| `SystemDocumentationService` / `SystemManagementService` | V2.2 history and XSD say removed, but V2.2 PDF table still prints them. | Supports CE-004 from V2.2 onward. |
| `warning` in DeviceStateEnumeration | V2.2 XSD contains `warning`, V2.2 PDF table does not list it. | Supports CE-006 from V2.2 onward. |
| `Valid` / `Air` / `Other` case | Still visible in V2.2 PDF/XSD pair. | Supports CE-007 historical range. |
| Submode casing and spelling | V2.2 introduces the affected tables. | Supports CE-008 and CE-009 historical origin; CE-010 origin remains to close exactly. |

## 6. Finding state decision

Status after this pass:

```text
No new CE finding opened.
No XSD change proposed.
No existing finding state changed in findings.md during this pass.
```

Reason:

```text
Several already-known CE findings are now historically anchored in V2.2, especially CE-004, CE-006, CE-008 and CE-009.
Affected-version ranges should still be consolidated in the dedicated Common/Enums historical closure step after V2.3 and V2.4 have been checked in sequence.
```

## 7. Validation backlog impact

Later technical validation should include version-specific pools:

```text
Common/Enums V2.1 pool:
  IBIS-IP_common_V2.1.xsd
  IBIS-IP_Enumerations_V2.1.xsd

Common/Enums V2.2 pool:
  IBIS-IP_common_V2.2.xsd
  IBIS-IP_Enumerations_V2.2.xsd
```

Suggested targeted samples after schema compile:

```text
V2.1 negative / V2.2 positive: DeviceClassEnumeration CombiDevice.
V2.1 negative / V2.2 positive: ServiceNameEnumeration SystemMonitoringService.
V2.1 positive / V2.2 negative: ServiceNameEnumeration SystemDocumentationService.
V2.1 positive / V2.2 negative: ServiceNameEnumeration SystemManagementService.
V2.2 positive but PDF-note: DeviceStateEnumeration warning.
V2.2 negative for PDF spelling: RailSubmodeEnumeration specialRail.
V2.2 positive for XSD spelling: RailSubmodeEnumeration specialTrain.
```

## 8. Next work inside the historical block

Next detailed audit file:

```text
docs/pdf_xsd_semantic_audit/04d_common_enums_v2_2_v2_3_history.md
```

Required next steps:

```text
1. Compare Common/Enums V2.2 and V2.3 XSD include families and enumeration/structure deltas.
2. Check VDV 301-2-1 V2.3 PDF version history and affected tables.
3. Track whether V2.3 intentionally keeps Enumerations V2.2.
4. Track DisplayContent, StopInformation, StopInformationRequest and TripInformation additions.
5. Decide whether CE-001 can be closed as intentional or remains unclear.
```

## 9. Result

```text
Common/Enums V2.1 -> V2.2 historical audit now has XSD-side diff plus PDF-side first pass.
The V2.2 PDF confirms the main V2.2 XSD-side additions/removals, but also exposes already-known table/history/XSD discrepancies.
No new finding opened in this pass.
Next: V2.2 -> V2.3 historical audit.
```
