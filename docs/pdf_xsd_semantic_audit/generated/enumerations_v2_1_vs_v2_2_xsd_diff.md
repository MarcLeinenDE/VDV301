# Common/Enums V2.1 vs V2.2 XSD enumeration diff

Status: first-pass audit diff.

Scope:

```text
IBIS-IP_Enumerations_V2.1.xsd
IBIS-IP_Enumerations_V2.2.xsd
```

Authority rule:

```text
Validation follows the selected XSD family.
PDF differences are explanatory audit findings, not executable validation authority.
```

## First-pass XSD deltas

| Change | Area | V2.1 | V2.2 | First-pass classification |
|---|---|---|---|---|
| Added value | DeviceClassEnumeration | - | CombiDevice | Confirmed XSD delta; V2.2 PDF confirms. |
| Added value | DeviceStateEnumeration | - | warning | XSD-only / PDF-table-gap candidate; supports CE-006 from V2.2 onward. |
| Removed value | ServiceNameEnumeration | SystemDocumentationService | - | Confirmed XSD delta; V2.2 history says deleted but V2.2 table still prints it; supports CE-004. |
| Removed value | ServiceNameEnumeration | SystemManagementService | - | Confirmed XSD delta; V2.2 history says deleted but V2.2 table still prints it; supports CE-004. |
| Added value | ServiceNameEnumeration | - | SystemMonitoringService | Confirmed XSD delta; V2.2 history/table and XSD align. |
| Added type | TripStateEnumeration | - | type present | Confirmed XSD delta; V2.2 PDF confirms. |
| Added type group | NetexMode-related mode/submode enumerations | - | Pt/Private submodes and detailed submode enumerations | Confirmed XSD delta; V2.2 PDF history says sections 3.28-3.40 added. |

## Important inherited/history-supported findings

```text
CE-004: ServiceNameEnumeration PDF table vs XSD/version-history discrepancy is already visible in V2.2.
CE-006: DeviceStateEnumeration warning is already an XSD-side V2.2 value while the V2.2 PDF table does not list it.
CE-007: Valid/Air/Other casing differences remain visible in V2.2 tables.
CE-008: Funicular/Taxi submode casing differences appear with the V2.2 submode introduction.
CE-009: RailSubmodeEnumeration specialRail vs specialTrain appears with the V2.2 submode introduction.
CE-010: AirSubmodeEnumeration canalBarge XSD-only origin still requires exact XSD-history closure.
```

## First-pass decision

```text
No new CE finding is opened by this generated diff alone.
Existing CE findings receive historical support, but affected-version ranges stay deferred to the Common/Enums historical closure step.
```
