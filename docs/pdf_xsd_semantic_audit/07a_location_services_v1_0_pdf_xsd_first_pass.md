# Location Services V1.0 PDF/XSD first pass

Status: first pass completed for BeaconLocationService, DistanceLocationService, GNSSLocationService and NetworkLocationService V1.0; local schema compilation still pending.

Scope:

```text
VDV 301-2-2 BeaconLocationService V1.0 PDF
VDV 301-2-4 DistanceLocationService V1.0 PDF
VDV 301-2-5 GNSSLocationService V1.0 PDF
VDV 301-2-7 NetworkLocationService V1.0 PDF

IBIS-IP_BeaconLocationService_V1.0.xsd
IBIS-IP_DistanceLocationService_V1.0.xsd
IBIS-IP_GNSSLocationService_V1.0.xsd
IBIS-IP_NetworkLocationService_V1.0.xsd
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

Authority rule:

```text
Where a version-exact XSD exists, executable validation follows that selected version's XSD family.
PDF differences are recorded as documentation/provider-facing notes, not as executable validation authority.
No schema correction is made in this pass.
```

Dependency pool:

```text
All checked location-service V1.0 XSD files include:
- IBIS-IP_common_V1.0.xsd
- IBIS-IP_Enumerations_V1.0.xsd
```

## 1. BeaconLocationService V1.0

PDF-side first-pass facts:

```text
BeaconLocationService.GetDataResponse choice:
- Data 1:1 BeaconLocationService.DataContent
- OperationErrorMessage IBIS-IP.string

BeaconLocationService.DataContent:
- TimeStamp 1:1 IBIS-IP.dateTime
- BeaconCode 1:1 IBIS-IP.NMTOKEN
- BeaconTime 0:1 IBIS-IP.time
- BeaconDistance 1:1 IBIS-IP.double
```

XSD-side facts:

```text
IBIS-IP_BeaconLocationService_V1.0.xsd defines:
- BeaconLocationService.GetDataResponse
- BeaconLocationService.GetDataResponseStructure
- BeaconLocationService.DataContent
- TimeStamp
- BeaconCode
- BeaconTime minOccurs="0"
- BeaconDistance
```

First-pass decision:

```text
No BeaconLocationService-specific PDF/XSD discrepancy opened.
SubscribeData/UnsubscribeData are documented by the PDF as using generic VDV 301-2-1 data structures; no service-local Subscribe/Unsubscribe XSD elements are expected from this first pass.
```

## 2. DistanceLocationService V1.0

PDF-side first-pass facts:

```text
DistanceLocationService.Data:
- Distance 1:1 IBIS-IP.double
- Odometer-Pulses 0:1 IBIS-IP.int
```

XSD-side facts:

```text
IBIS-IP_DistanceLocationService_V1.0.xsd defines:
- DistanceLocationService.Data
- DistanceLocationService.DataStructure
- Distance
- Odometer-Pulses minOccurs="0"
```

First-pass decision:

```text
No DistanceLocationService-specific PDF/XSD discrepancy opened.
The hyphenated element name Odometer-Pulses is present in both the checked PDF extraction and the XSD.
```

## 3. GNSSLocationService V1.0

PDF-side first-pass facts:

```text
GNSSLocationService.Data:
- latitude 1:1 GNSSCoordinate
- longitude 1:1 GNSSCoordinate
- altitude 0:1 IBIS-IP.double
- time 0:1 IBIS-IP.time
- date 0:1 IBIS-IP.date
- SpeedOverGround 0:1 IBIS-IP.double
- SignalQuality 0:1 GNSSQualityEnumeration
- NumberOfSatellites 0:1 IBIS-IP.int
- HorizontalDilutionOfPrecision 0:1 IBIS-IP.double
- VerticalDilutionOfPrecision 0:1 IBIS-IP.double
- TrackDegreeTrue 0:1 IBIS-IP.double
- TrackDegreeMagnetic 0:1 IBIS-IP.double
- GNSSType 1:1 GNSSTypeEnumeration
- GNSSCoordinateSystem 0:1 GNSSCoordinateSystemEnumeration
```

XSD-side facts:

```text
IBIS-IP_GNSSLocationService_V1.0.xsd defines the same structure overall, but uses:
- HoriziontalDilutionOfPrecision

instead of the PDF table spelling:
- HorizontalDilutionOfPrecision
```

First-pass decision:

```text
LS-001 opened as a Location Services finding candidate.
Validation follows the XSD spelling HoriziontalDilutionOfPrecision unless an official schema correction exists.
A payload using HorizontalDilutionOfPrecision as printed in the PDF will fail against the checked V1.0 XSD.
```

Related Common/Enums note:

```text
GNSSTypeEnumeration has already been covered by CE-007 for case-sensitive PDF/XSD value differences.
This file does not reopen that Common/Enums finding as a service-local GNSS finding.
```

## 4. NetworkLocationService V1.0

PDF-side first-pass facts:

```text
NetworkLocationService.Data:
- CurrentTripRef 1:1 IBIS-IP.NMTOKEN
- NextPointRef 1:1 IBIS-IP.NMTOKEN
- DistanceToNextPoint 1:1 IBIS-IP.double
- NextStopPointRef 1:1 IBIS-IP.NMTOKEN
- DistanceToNextStopPoint 1:1 IBIS-IP.double
- RouteDeviation 0:1 RouteDeviationEnumeration
- LocationState 0:1 LocationStateEnumeration
```

XSD-side facts:

```text
IBIS-IP_NetworkLocationService_V1.0.xsd defines the same local element sequence and cardinalities.
```

First-pass decision:

```text
No NetworkLocationService-specific PDF/XSD discrepancy opened.
```

## 5. Cross-service structural observation

Observed:

```text
BeaconLocationService uses a GetDataResponse wrapper with Data / OperationErrorMessage choice.
DistanceLocationService, GNSSLocationService and NetworkLocationService define raw *.Data top-level elements.
```

First-pass classification:

```text
This is treated as an intentional service-specific modelling difference, not as a defect.
Do not normalize these four services to one wrapper style in a validator.
```

## 6. Finding decision

New Location Services finding candidate:

```text
LS-001 - GNSSLocationService HorizontalDilutionOfPrecision PDF spelling vs XSD HoriziontalDilutionOfPrecision
```

Closed/OK notes:

```text
LS-002 candidate from the start file is closed OK with note: Odometer-Pulses is present in both PDF and XSD.
LS-003 candidate from the start file is closed OK with note: Beacon wrapper vs raw *.Data modelling differs across location services but is not treated as a defect.
```

No XSD change:

```text
No schema correction is made in this pass.
No official PR candidate is opened.
```

## 7. Validation backlog impact

Later local validation should compile:

```text
IBIS-IP_BeaconLocationService_V1.0.xsd + Common V1.0 + Enumerations V1.0
IBIS-IP_DistanceLocationService_V1.0.xsd + Common V1.0 + Enumerations V1.0
IBIS-IP_GNSSLocationService_V1.0.xsd + Common V1.0 + Enumerations V1.0
IBIS-IP_NetworkLocationService_V1.0.xsd + Common V1.0 + Enumerations V1.0
```

Suggested targeted samples:

```text
Beacon positive: GetDataResponse with Data/TimeStamp/BeaconCode/BeaconDistance.
Beacon positive: GetDataResponse with OperationErrorMessage.
Distance positive: DistanceLocationService.Data with Distance only.
Distance positive: DistanceLocationService.Data with Odometer-Pulses.
GNSS positive: GNSSLocationService.Data using HoriziontalDilutionOfPrecision.
GNSS negative: GNSSLocationService.Data using HorizontalDilutionOfPrecision.
Network positive: NetworkLocationService.Data with required five mandatory fields.
Network positive: NetworkLocationService.Data with optional RouteDeviation and LocationState.
```

## 8. Next Location Services audit step

Next recommended step:

```text
07b_location_services_findings_and_closure.md
```
