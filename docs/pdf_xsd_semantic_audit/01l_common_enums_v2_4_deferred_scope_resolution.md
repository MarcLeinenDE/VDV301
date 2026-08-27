# Common structures / enumerations V2.4 - deferred scope resolution

Status: completed for SB-005 first-pass routing.

Scope:

```text
Resolve deferred names from the Common/Enums V2.4 structure closure pass.
```

Deferred names from SB-005:

```text
NetworkLocationPoint
OperationalInformation
PassengerCounting
PassengerCountingData
PathDestination
Route
```

Authority rule:

```text
Validation follows XSD.
PDF differences are retained as provider-facing explanation notes.
No schema changes are made in this audit pass.
```

## 1. Method

Each deferred name was classified as one of:

```text
common V2.4 standalone structure
common V2.4 field-level usage
service-specific structure
older-version service structure
PDF-only / documentation-only structure
extraction or planning artefact
unresolved
```

A missing standalone `IBIS-IP_common_V2.4.xsd` complexType is not by itself a CE finding. A CE finding should only be opened if the PDF table and XSD evidence show a real schema/documentation mismatch in the intended scope.

## 2. NetworkLocationPoint

### Resolution

```text
Not a confirmed standalone Common/Enums V2.4 complexType.
Route to NetworkLocationService V1.0 audit.
```

### Evidence / rationale

The branch contains:

```text
IBIS-IP_NetworkLocationService_V1.0.xsd
```

This service schema defines `NetworkLocationService.DataStructure` with fields such as:

```text
CurrentTripRef
NextPointRef
DistanceToNextPoint
NextStopPointRef
DistanceToNextStopPoint
RouteDeviation
LocationState
```

This is service-specific NetworkLocation data, not a Common V2.4 standalone structure named `NetworkLocationPoint`.

### Closure action

```text
Remove from Common/Enums V2.4 closure blockers.
Carry into NetworkLocationService V1.0 service audit.
No CE finding opened here.
```

## 3. PassengerCounting / PassengerCountingData

### Resolution

```text
Service-specific.
Route to PassengerCountingService V2.1 audit.
```

### Evidence / rationale

The branch contains:

```text
IBIS-IP_PassengerCountingService_V2.1.xsd
```

That schema defines PassengerCounting-specific operation and data structures, including:

```text
PassengerCountingService.AllDataStructure
PassengerCountingService.SpecificDoorDataStructure
PassengerCountingService.SetCounterDataRequestStructure
PassengerCountingService.CountingStatesStructure
```

The actual counting data uses common door/counting structures such as:

```text
DoorInformationStructure
DoorCountingListStructure
```

Those common structures were already checked in the Common/Enums V2.4 pass.

### Closure action

```text
Remove from Common/Enums V2.4 closure blockers.
Carry into PassengerCountingService V2.1 service audit.
No CE finding opened here.
```

## 4. Route

### Resolution

```text
Service-specific element usage in JourneyInformationService V1.0.
No standalone Common V2.4 `RouteStructure` confirmed.
```

### Evidence / rationale

The branch contains:

```text
IBIS-IP_JourneyInformationService_V1.0.xsd
```

Within JourneyInformationService, `ListAllRoutesResponse` uses:

```text
AllRouteData
Route type="TripInformationStructure" maxOccurs="unbounded"
```

Therefore `Route` is an element name that reuses the common `TripInformationStructure`, not a separate common structure needing a standalone `RouteStructure` in `IBIS-IP_common_V2.4.xsd`.

### Closure action

```text
Remove from Common/Enums V2.4 closure blockers.
Carry the service-level route operation into JourneyInformationService V1.0 audit.
No CE finding opened here.
```

## 5. PathDestination

### Resolution

```text
Common V2.4 field-level usage, not a standalone common structure.
```

### Evidence / rationale

`IBIS-IP_common_V2.4.xsd` and the Common/Enums V2.4 table-level audit include the field:

```text
TripInformation / PathDestinationNumber
```

No standalone `PathDestinationStructure` was confirmed in `IBIS-IP_common_V2.4.xsd`.

### Closure action

```text
Treat as covered by TripInformation field-level audit.
No CE finding opened here.
```

## 6. OperationalInformation

### Resolution

```text
Not confirmed as standalone Common/Enums V2.4 complexType in this branch.
Leave as documentation / extraction / planning artefact until a concrete PDF table or service XSD target is identified.
```

### Evidence / rationale

No standalone Common V2.4 complexType named `OperationalInformationStructure` was confirmed during this pass. No concrete service schema target was confirmed in the SB-005 evidence set.

### Closure action

```text
Remove from Common/Enums V2.4 closure blockers.
Keep a low-priority routing note for later service/version audits if the name appears in a concrete PDF table.
No CE finding opened here.
```

## 7. SB-005 closure result

```text
SB-005 is resolved for Common/Enums V2.4 first-pass closure.
```

Classification:

| Name | Classification | Follow-up |
|---|---|---|
| NetworkLocationPoint | service-specific / older V1.0 NetworkLocation scope | NetworkLocationService V1.0 audit |
| PassengerCounting | service-specific PCS scope | PassengerCountingService V2.1 audit |
| PassengerCountingData | service-specific PCS scope | PassengerCountingService V2.1 audit |
| PathDestination | field-level TripInformation usage | already covered as PathDestinationNumber |
| Route | service-specific JourneyInformation element using TripInformationStructure | JourneyInformationService V1.0 audit |
| OperationalInformation | not confirmed / routing note only | revisit only with concrete PDF/XSD evidence |

No new CE finding is opened by SB-005.

## 8. Next closure blockers

Remaining blockers before Common/Enums V2.4 first-pass closure:

```text
1. Visual PDF confirmation for CE-015 FareZoneInformation casing.
2. Visual PDF confirmation for CE-017 TSPPoint Desciption/Description spelling.
3. ZoneType first-field casing/spelling decision.
```

After those checks, Common/Enums V2.4 can be marked first-pass closed with explicitly carried historical/provider-note findings.
