# Common/Enums V2.0 -> V2.1 XSD enumeration diff

Status: first-pass diff recorded.

Scope:

```text
IBIS-IP_Enumerations_V2.0.xsd
IBIS-IP_Enumerations_V2.1.xsd
```

## Confirmed XSD-side deltas

| Change | Type | Value | Status | Notes |
|---|---|---|---|---|
| added value | `DeviceClassEnumeration` | `MultiFunctionalDisplay` | confirmed XSD delta | PDF V2.1 history/table confirms. |
| added value | `ErrorCodeEnumeration` | `OperationNotSupported` | confirmed XSD delta | PDF V2.1 history/table confirms. |
| added value | `ServiceNameEnumeration` | `DoorStateService` | confirmed XSD delta | PDF V2.1 history/table confirms. |
| added value | `ServiceNameEnumeration` | `TrainSetDataService` | confirmed XSD delta | PDF V2.1 history/table confirms. |
| added value | `ServiceNameEnumeration` | `TrainSetInformationService` | confirmed XSD delta | PDF V2.1 history/table confirms. |
| added value | `ServiceNameEnumeration` | `TrainSetManagementService` | confirmed XSD delta | PDF V2.1 history/table confirms. |
| added value | `ServiceNameEnumeration` | `TicketValidationService` | confirmed XSD delta | PDF V2.1 history/table confirms. |
| added value | `ServiceNameEnumeration` | `HTMLDisplayService` | confirmed XSD delta | PDF V2.1 history/table confirms. |

## Include-family observation

```text
IBIS-IP_common_V2.0.xsd includes IBIS-IP_Enumerations_V2.0.xsd.
IBIS-IP_common_V2.1.xsd includes IBIS-IP_Enumerations_V2.1.xsd.
```

## Classification

```text
No new CE finding opened from these XSD deltas.
The V2.1 PDF confirms the listed enumeration additions in the version history and tables.
```
