# Location services historical audit start

Status: started; provenance/scope and first XSD mapping completed.

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
```

Authority rule:

```text
Where a version-exact service XSD exists, executable validation follows the selected service version's XSD family.
PDF differences are recorded as provider-facing notes unless and until a schema correction candidate is deliberately prepared.
No schema change is made in this start pass.
```

Mixed-version rule:

```text
Do not route location-service payloads through a generic/latest location schema.
The four checked location services are separate V1.0 service schemas with separate top-level element names and structures.
```

## 1. Public PDF mapping

The public VDV index lists these service PDFs in the location-service area:

| VDV part | Service | Public version observed | Audit classification |
|---|---|---|---|
| 301-2-2 | BeaconLocationService | V1.0 | public VDV PDF observed |
| 301-2-4 | DistanceLocationService | V1.0 | public VDV PDF observed |
| 301-2-5 | GNSSLocationService | V1.0 | public VDV PDF observed |
| 301-2-7 | NetworkLocationService | V1.0 | public VDV PDF observed |

First-pass interpretation:

```text
Only V1.0 public service-PDF versions have been observed for these four location services in the first pass.
No V2.x location-service-specific PDF version was observed on the public index in this pass.
```

## 2. Repository XSD mapping

Observed XSD files in dev/schema-integration:

| Service | Service XSD | Common dependency | Enumeration dependency | Classification |
|---|---|---|---|---|
| BeaconLocationService | `IBIS-IP_BeaconLocationService_V1.0.xsd` | `IBIS-IP_common_V1.0.xsd` | `IBIS-IP_Enumerations_V1.0.xsd` | version-exact V1.0 XSD present |
| DistanceLocationService | `IBIS-IP_DistanceLocationService_V1.0.xsd` | `IBIS-IP_common_V1.0.xsd` | `IBIS-IP_Enumerations_V1.0.xsd` | version-exact V1.0 XSD present |
| GNSSLocationService | `IBIS-IP_GNSSLocationService_V1.0.xsd` | `IBIS-IP_common_V1.0.xsd` | `IBIS-IP_Enumerations_V1.0.xsd` | version-exact V1.0 XSD present |
| NetworkLocationService | `IBIS-IP_NetworkLocationService_V1.0.xsd` | `IBIS-IP_common_V1.0.xsd` | `IBIS-IP_Enumerations_V1.0.xsd` | version-exact V1.0 XSD present |

First-pass interpretation:

```text
All four location services currently map to the same V1.0 dependency pool:
Common V1.0 + Enumerations V1.0.
```

## 3. First XSD observations by service

### BeaconLocationService V1.0

XSD form:

```text
Top-level element:
BeaconLocationService.GetDataResponse

Data structure:
Data / BeaconLocationService.DataContent
  TimeStamp 1:1
  BeaconCode 1:1
  BeaconTime 0:1
  BeaconDistance 1:1
```

First-pass interpretation:

```text
BeaconLocationService uses a GetDataResponse-style operation element, not a raw *.Data publish-style top-level element.
Detailed PDF/XSD table comparison remains the next pass.
```

### DistanceLocationService V1.0

XSD form:

```text
Top-level element:
DistanceLocationService.Data

Data structure:
  Distance 1:1
  Odometer-Pulses 0:1
```

First-pass interpretation:

```text
The element name Odometer-Pulses contains a hyphen.
This must be preserved in executable validation and sample generation.
Do not normalize it to OdometerPulses without an explicit official schema change.
```

### GNSSLocationService V1.0

XSD form:

```text
Top-level element:
GNSSLocationService.Data

Data structure:
  latitude 1:1
  longitude 1:1
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
  GNSSType 1:1
  GNSSCoordinateSystem 0:1
```

First-pass interpretation:

```text
The XSD spelling HoriziontalDilutionOfPrecision is typo-like but authoritative for validation in the current V1.0 schema.
Do not silently normalize it to HorizontalDilutionOfPrecision.
GNSSTypeEnumeration already overlaps with CE-007 case-sensitivity notes.
```

### NetworkLocationService V1.0

XSD form:

```text
Top-level element:
NetworkLocationService.Data

Data structure:
  CurrentTripRef 1:1
  NextPointRef 1:1
  DistanceToNextPoint 1:1
  NextStopPointRef 1:1
  DistanceToNextStopPoint 1:1
  RouteDeviation 0:1
  LocationState 0:1
```

First-pass interpretation:

```text
NetworkLocationService references journey/network progress information and depends on JourneyInformationService refs in documentation annotations.
RouteDeviation is already a Common/Enums enumeration area, so related value/case findings must remain in the shared CE register rather than being duplicated here.
```

## 4. Preliminary finding decision

No LS finding is opened in this start pass.

Candidate notes for the next detailed pass:

```text
LS-001 candidate: GNSS XSD spelling HoriziontalDilutionOfPrecision vs likely PDF/semantic HorizontalDilutionOfPrecision; check matching PDF table before classifying.
LS-002 candidate: DistanceLocationService Odometer-Pulses hyphenated XSD element; verify PDF exact spelling before any provider-facing note.
LS-003 candidate: BeaconLocationService GetDataResponse-style operation differs from the raw *.Data style used by Distance/GNSS/Network; likely intentional service-specific modelling but should be documented.
```

No XSD change is proposed.

## 5. Validation backlog impact

Later local technical validation should compile these pools separately even though they share dependencies:

```text
BeaconLocationService V1.0 + Common V1.0 + Enumerations V1.0
DistanceLocationService V1.0 + Common V1.0 + Enumerations V1.0
GNSSLocationService V1.0 + Common V1.0 + Enumerations V1.0
NetworkLocationService V1.0 + Common V1.0 + Enumerations V1.0
```

Suggested targeted samples:

```text
Beacon positive: GetDataResponse/Data with TimeStamp, BeaconCode, BeaconDistance and optional BeaconTime.
Distance positive: Data with Distance only.
Distance positive: Data with Odometer-Pulses.
Distance negative: OdometerPulses without hyphen if no alias exists.
GNSS positive: Data with latitude, longitude and GNSSType.
GNSS positive: Data with HoriziontalDilutionOfPrecision as spelled in XSD.
GNSS negative: HorizontalDilutionOfPrecision if no alias exists.
Network positive: Data with required trip/point/distance fields.
Network positive: optional RouteDeviation and LocationState.
```

## 6. Next location-services audit step

Next detailed step:

```text
07a_location_services_v1_0_pdf_xsd_first_pass.md
```
