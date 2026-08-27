# Location Services findings and V1.0 closure

Status: first-pass closure completed for BeaconLocationService, DistanceLocationService, GNSSLocationService and NetworkLocationService V1.0; local schema compilation still pending.

Scope:

```text
docs/pdf_xsd_semantic_audit/07_location_services_historical_start.md
docs/pdf_xsd_semantic_audit/07a_location_services_v1_0_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/LOCATION_SERVICES_FINDINGS_REGISTER_ADDENDUM.md
```

## Selected validation authority

Validation remains XSD-driven.

```text
BeaconLocationService V1.0     -> IBIS-IP_BeaconLocationService_V1.0.xsd     + Common V1.0 + Enumerations V1.0
DistanceLocationService V1.0   -> IBIS-IP_DistanceLocationService_V1.0.xsd   + Common V1.0 + Enumerations V1.0
GNSSLocationService V1.0       -> IBIS-IP_GNSSLocationService_V1.0.xsd       + Common V1.0 + Enumerations V1.0
NetworkLocationService V1.0    -> IBIS-IP_NetworkLocationService_V1.0.xsd    + Common V1.0 + Enumerations V1.0
```

No latest-wins substitution is allowed. These four services stay on the historical V1.0 Common/Enumerations pool unless a selected service schema explicitly requires something else.

## Closure result by service

### BeaconLocationService V1.0

First-pass result: OK.

Key XSD modelling:

```text
BeaconLocationService.GetDataResponse
  choice:
    Data
    OperationErrorMessage
Data:
  TimeStamp
  BeaconCode
  BeaconTime 0:1
  BeaconDistance
```

No Location-Services finding is opened for BeaconLocationService.

### DistanceLocationService V1.0

First-pass result: OK with exact-name note.

Key XSD modelling:

```text
DistanceLocationService.Data
  Distance
  Odometer-Pulses 0:1
```

`Odometer-Pulses` contains a hyphen and must be preserved exactly. Do not normalize this element name in a future validator, SDK, or generated model. This remains LS-002 as OK-with-note, not a defect.

### GNSSLocationService V1.0

First-pass result: one confirmed PDF/XSD spelling discrepancy candidate.

Key XSD modelling:

```text
GNSSLocationService.Data
  latitude
  longitude
  altitude 0:1
  time 0:1
  date 0:1
  SpeedOverGround 0:1
  SignalQuality 0:1
  NumberOfSatellites 0:1
  HoriziontalDilutionOfPrecision 0:1
  VerticalDilutionOfPrecision 0:1
  TrackDegreeTrue 0:1
  TrackDegreeMagnetic 0:1
  GNSSType
  GNSSCoordinateSystem 0:1
```

LS-001 remains open as a documented candidate: the PDF-side spelling is `HorizontalDilutionOfPrecision`, while the XSD-side executable spelling is `HoriziontalDilutionOfPrecision`.

Validation impact:

```text
<HorizontalDilutionOfPrecision> follows the checked PDF spelling but does not validate against the checked V1.0 XSD.
<HoriziontalDilutionOfPrecision> validates against the checked V1.0 XSD but looks typo-like in provider discussions.
```

No schema correction is made in this audit step.

### NetworkLocationService V1.0

First-pass result: OK.

Key XSD modelling:

```text
NetworkLocationService.Data
  CurrentTripRef
  NextPointRef
  DistanceToNextPoint
  NextStopPointRef
  DistanceToNextStopPoint
  RouteDeviation 0:1
  LocationState 0:1
```

No Location-Services finding is opened for NetworkLocationService.

## Cross-service modelling note

The four location services intentionally do not share one top-level wrapper pattern in the checked XSD set:

```text
BeaconLocationService: BeaconLocationService.GetDataResponse wrapper with Data / OperationErrorMessage choice.
DistanceLocationService: raw DistanceLocationService.Data top-level element.
GNSSLocationService: raw GNSSLocationService.Data top-level element.
NetworkLocationService: raw NetworkLocationService.Data top-level element.
```

This is documented as LS-003 OK-with-note. Future tooling must preserve each service's actual top-level XSD element instead of forcing one uniform pattern.

## Findings status after closure

```text
LS-001: open candidate / confirmed PDF-XSD spelling discrepancy candidate.
LS-002: OK with note, exact XML element name contains hyphen.
LS-003: OK with note, service-specific wrapper style differs by service.
```

## Validation backlog impact

Add local samples later:

```text
Beacon positive: BeaconLocationService.GetDataResponse/Data with required TimeStamp, BeaconCode, BeaconDistance.
Distance positive: DistanceLocationService.Data with Distance and Odometer-Pulses.
GNSS positive: GNSSLocationService.Data using XSD-valid HoriziontalDilutionOfPrecision.
GNSS negative/provider-note: GNSSLocationService.Data using PDF spelling HorizontalDilutionOfPrecision.
Network positive: NetworkLocationService.Data with required refs/distances and optional RouteDeviation/LocationState.
```

## Official PR impact

No official-facing PR is opened from this closure.

LS-001 should be included in the later post-audit review. A correction proposal, if ever prepared, must be minimal and must be backed by local XSD/sample validation and official-source evidence.

## Next block

```text
08_door_state_service_historical_start.md
```
