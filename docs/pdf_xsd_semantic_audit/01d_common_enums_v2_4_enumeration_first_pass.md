# Common structures / enumerations V2.4 - enumeration first-pass audit

Status: started, partial.

This file starts the enumeration-by-enumeration PDF/XSD comparison for `IBIS-IP_Enumerations_V2.4.xsd` against `VDV-Schrift 301-2-1 V2.4`.

Scope of this pass:

```text
ConnectionStateEnumeration
ConnectionTypeEnumeration
DataIntervalEnumeration
DeviceClassEnumeration
DeviceStateEnumeration
DeviceTaskEnumeration
DoorCountingObjectClassEnumeration
DoorCountingQualityEnumeration
DoorOpenStateEnumeration
DoorOperationStateEnumeration
ErrorCodeEnumeration
ExitSideEnumeration
GNSSCoordinateSystemEnumeration
GNSSQualityEnumeration
GNSSTypeEnumeration
JourneyModeEnumeration
LocationStateEnumeration
MessageTypeEnumeration
RouteDeviationEnumeration
RouteDirectionEnumeration
ServiceNameEnumeration
ServiceStateEnumeration
SystemDocumentationInformationEnumeration
TicketRazziaInformationEnumeration
TicketValidationEnumeration
VehicleModeEnumeration
TripStateEnumeration
first pass over Netex/Submode enumerations
```

Important method note:

```text
Order differences in enumeration values are not treated as semantic mismatches.
XML enumeration value spelling/case differences are treated as semantic mismatches because XML values are case-sensitive.
```

## 1. Enumeration tables 3.1 to 3.20

### Mostly aligned enumerations

The following V2.4 PDF tables and XSD definitions are aligned in the first pass, allowing for ordering differences only:

| Enumeration | Status | Notes |
|---|---|---|
| `ConnectionStateEnumeration` | OK | Values: `ConnectionBroken`, `ConnectionOK`, `NoInformationAvailable`. |
| `ConnectionTypeEnumeration` | OK | Values: `Interchange`, `ProtectedConnection`. |
| `DataIntervalEnumeration` | OK | Values: `DistanceData`, `GNSSData`, `Heartbeat`, `NetworkLocationData`. |
| `DeviceClassEnumeration` | OK | Includes `MultiFunctionalDisplay` and `CombiDevice`. |
| `DeviceTaskEnumeration` | OK | Values: `restart`, `start_standby`, `stop_standby`. |
| `DoorCountingObjectClassEnumeration` | OK | Includes corrected `Wheelchair`. |
| `DoorCountingQualityEnumeration` | OK | Same values; order differs only. |
| `DoorOpenStateEnumeration` | OK | Values match. |
| `DoorOperationStateEnumeration` | OK | Values match. |
| `ErrorCodeEnumeration` | OK | Includes `OperationNotSupported`. |
| `ExitSideEnumeration` | OK | Values match. |
| `GNSSCoordinateSystemEnumeration` | OK with naming note | PDF heading uses `GNSSCoordinateSystemsEnumeration` plural in table text, section name and XSD use singular. Values match. |
| `GNSSQualityEnumeration` | OK | Values match. |
| `JourneyModeEnumeration` | OK | Values match. |
| `LocationStateEnumeration` | OK | Values match; order differs only. |
| `MessageTypeEnumeration` | OK | Values match. |
| `RouteDeviationEnumeration` | OK | Values match. |
| `RouteDirectionEnumeration` | OK | Values match. |

### CE-006: DeviceStateEnumeration contains extra XSD value `warning`

PDF V2.4 table 69 lists:

```text
defective
notavailable
running
readyForShutdown
```

XSD V2.4 contains:

```xml
<xs:enumeration value="defective"/>
<xs:enumeration value="warning"/>
<xs:enumeration value="notavailable"/>
<xs:enumeration value="running"/>
<xs:enumeration value="readyForShutdown"/>
```

Finding:

| Item | Status | Notes |
|---|---|---|
| `warning` | discrepancy | Present in XSD, absent from V2.4 PDF table. |

Interpretation:

```text
This is an XSD-extra-vs-PDF-table mismatch.
Do not remove `warning` automatically; it may be intentionally retained from earlier schema/service semantics.
Needs historical PDF/XSD check before any schema decision.
```

## 2. GNSSTypeEnumeration case mismatch

PDF V2.4 table 79 lists:

```text
GPS
Glonass
Galileo
Beidou
IRNSS
Other
DeadReckoning
MixedGNSSTypes
```

XSD V2.4 contains the same list except the generic value is lowercase:

```xml
<xs:enumeration value="other"/>
```

Finding:

| Item | Status | Notes |
|---|---|---|
| `Other` vs `other` | discrepancy | XML enumeration values are case-sensitive. |

This is tracked as part of `CE-007`.

## 3. ServiceNameEnumeration follow-up

PDF V2.4 table 85 lists both the older services and the replacement service:

```text
SystemDocumentationService
SystemManagementService
SystemMonitoringService
```

XSD V2.4 contains `SystemMonitoringService` but not the two older service names in the checked snippet.

This continues finding `CE-004`.

Additional observation:

```text
The V2.4 version history explicitly says SystemDocumentationService and SystemManagementService were deleted and SystemMonitoringService inserted.
Therefore the XSD appears to follow the version history, while the PDF enumeration table still appears to carry older values.
```

No schema change should be made from this alone.

## 4. TicketValidationEnumeration case mismatch

PDF V2.4 table 89 lists:

```text
Valid
notvalid
NoCard
```

XSD V2.4 contains:

```xml
<xs:enumeration value="valid"/>
<xs:enumeration value="notvalid"/>
<xs:enumeration value="NoCard"/>
```

Finding:

| Item | Status | Notes |
|---|---|---|
| `Valid` vs `valid` | discrepancy | Case-sensitive value mismatch between PDF and XSD. |

This is tracked as part of `CE-007`.

## 5. VehicleModeEnumeration case mismatch

PDF V2.4 table 90 lists:

```text
Air
bus
coach
ferry
metro
rail
tram
underground
```

XSD V2.4 contains:

```xml
<xs:enumeration value="air"/>
<xs:enumeration value="bus"/>
<xs:enumeration value="coach"/>
<xs:enumeration value="ferry"/>
<xs:enumeration value="metro"/>
<xs:enumeration value="rail"/>
<xs:enumeration value="tram"/>
<xs:enumeration value="underground"/>
```

Finding:

| Item | Status | Notes |
|---|---|---|
| `Air` vs `air` | discrepancy | Case-sensitive value mismatch between PDF and XSD. |

This is tracked as part of `CE-007`.

## 6. TripStateEnumeration

PDF V2.4 table 91 lists:

```text
EmptyRun
OnTrip
OffTrip
TripBreak
OffDuty
unknown
```

First-pass status:

```text
Pending XSD value extraction.
```

No finding opened yet.

## 7. Netex / Submode enumerations first pass

The V2.4 PDF defines `PtSubModesEnumeration`, `PrivateSubModesEnumeration` and submode enumerations from Rail through SelfDrive.

First-pass checks confirm that the XSD contains the Netex/Submode family and the broad submode lists.

### Noted case/text mismatches to verify

Potential case-sensitive mismatches seen in the PDF-vs-XSD first pass:

| Enumeration | PDF spelling | XSD spelling | Status |
|---|---|---|---|
| `FunicularSubmodeEnumeration` | `Unknown` | `unknown` | discrepancy candidate |
| `TaxiSubmodeEnumeration` | `Unknown` | `unknown` | discrepancy candidate |
| `TaxiSubmodeEnumeration` | `Undefined` | likely `undefined` | needs full snippet confirmation |
| `TaxiSubmodeEnumeration` | `minicab` | `miniCab` | discrepancy candidate |

These are treated as part of `CE-007` until the full Netex/Submode enumeration extraction is completed.

## 8. New findings from this pass

### CE-006 - DeviceStateEnumeration PDF table missing XSD value `warning`

State: open.

```text
XSD has `warning`; PDF V2.4 table does not list it.
```

### CE-007 - Enumeration case/spelling mismatches between PDF and XSD

State: open.

Confirmed first-pass items:

```text
GNSSTypeEnumeration: Other vs other
TicketValidationEnumeration: Valid vs valid
VehicleModeEnumeration: Air vs air
```

Candidate items needing full Netex/Submode extraction:

```text
FunicularSubmodeEnumeration: Unknown vs unknown
TaxiSubmodeEnumeration: Unknown/Undefined/minicab vs unknown/undefined/miniCab
```

## 9. Recommendation

Do not patch the XSD based on these findings yet.

Next audit step:

```text
Run or perform full enumeration extraction for all V2.4 XSD simpleTypes and compare against PDF tables 65-104.
Then classify each mismatch as:
- clear PDF typo/table inconsistency,
- clear XSD defect,
- historical compatibility carry-over,
- unresolved until VDV confirmation.
```
