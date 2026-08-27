# Common structures / enumerations V2.4 - remaining data structures part 2

Status: started, partial.

Scope of this block:

```text
VDV 301-2-1 V2.4 common data structures from GNSSCoordinate onward.

Covered in this file:
GNSSCoordinate
JourneyStopInformation
Point / PointType / TSPPoint
SpecificPoint
StopSequence
TimingPoint
ViaPoint
ZoneType
```

Important scope note:

```text
The handoff list also mentioned NetworkLocationPoint, OperationalInformation,
PassengerCounting / PassengerCountingData, PathDestination and Route.
These names were not confirmed as standalone complexType definitions in
IBIS-IP_common_V2.4.xsd during this pass.
Some related concepts occur as fields, for example PathDestinationNumber and
RouteDirection inside TripInformation.
This must be resolved in the follow-up coverage pass before declaring the
Common/Enums V2.4 structure audit fully closed.
```

Authority rule:

```text
Validation follows the XSD.
PDF differences are retained as provider-facing explanation notes.
No schema change is made during this audit pass.
```

## 1. GNSSCoordinate

### PDF expectation

The PDF table for `GNSSCoordinate` describes a coordinate component with:

```text
Degree     1:1 IBIS-IP.double
Direction  1:1 IBIS-IP.string
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```text
GNSSCoordinateStructure:
  Degree    required IBIS-IP.double
  Direction required IBIS-IP.string
```

### Finding

Status: OK.

No CE finding opened.

## 2. JourneyStopInformation

### PDF expectation

The PDF table for `JourneyStopInformation` describes stop information used inside route/point contexts. The checked core fields are:

```text
StopRef   1:1 IBIS-IP.NMTOKEN
StopName  1:* +InternationalTextType
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```text
JourneyStopInformationStructure:
  StopRef  required IBIS-IP.NMTOKEN
  StopName required and repeatable InternationalTextType
```

### Finding

Status: OK for the checked fields.

No CE finding opened.

## 3. Point and PointType

### PDF expectation

The PDF table group around `Point` describes a route/path point with an index, a point type and distance to the previous point. The point type is a choice between stop, beacon, GNSS, timing and traffic-signal-prioritisation related point forms.

Expected shape:

```text
Point:
  PointIndex              1:1 IBIS-IP.int
  PointType               1:1 +PointType
  DistanceToPreviousPoint 1:1 IBIS-IP.int

PointType:
  one of StopPoint / BeaconPoint / GNSSLocationPoint / TimingPoint / TSPPoint
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```text
PointStructure:
  PointIndex required IBIS-IP.int
  PointType required PointTypeStructure
  DistanceToPreviousPoint required IBIS-IP.int

PointTypeStructure:
  xs:choice containing StopPoint, BeaconPoint, GNSSLocationPoint, TimingPoint and TSPPoint forms
```

### Finding

Status: OK, partial.

The choice structure is present. TSPPoint spelling is handled below as a separate finding candidate.

## 4. TSPPoint

### PDF expectation

The PDF-side spelling for the description field still needs visual confirmation in the table. Semantically, this field is expected to be a description text for the TSP point.

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```text
TSPPointStructure:
  TSPPointRef  optional IBIS-IP.NMTOKEN
  TSPCode      required IBIS-IP.NMTOKEN
  ShortName    optional repeatable InternationalTextType
  Desciption   optional repeatable InternationalTextType
```

The XSD element name is `Desciption`, not `Description`.

### Finding

This opens `CE-017` as a spelling-discrepancy candidate.

Tool implication:

```text
If a provider sends <Description>, validation fails against the current XSD.
The XSD-valid element name is <Desciption>.
Provider-facing note should say that the XSD spelling looks typo-like but is the executable validation authority unless an official schema correction exists.
```

PDF visual confirmation is required before final classification.

## 5. SpecificPoint

### PDF expectation

```text
PointRef                 1:1 IBIS-IP.NMTOKEN
DistanceToPreviousPoint  1:1 IBIS-IP.double
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```text
SpecificPointStructure:
  PointRef required IBIS-IP.NMTOKEN
  DistanceToPreviousPoint required IBIS-IP.double
```

### Finding

Status: OK.

No CE finding opened.

Note: `SpecificPoint` is also relevant to `CE-013`, where the PDF names the AdditionalAnnouncement choice `InformationAtSpecificPoint` while the XSD element name is `SpecificPoint`.

## 6. StopSequence

### PDF expectation

```text
StopPoint 2:* +StopInformation
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:element name="StopPoint" type="StopInformationStructure" minOccurs="2" maxOccurs="unbounded"/>
```

### Finding

Status: OK.

No CE finding opened.

## 7. TimingPoint

### PDF expectation

```text
TimingPointRef 0:1 IBIS-IP.NMTOKEN
ScheduleTime   1:1 IBIS-IP.dateTime
GNSSPoint      1:1 +GNSSPoint
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```text
TimingPointStructure:
  TimingPointRef optional IBIS-IP.NMTOKEN
  ScheduleTime required IBIS-IP.dateTime
  GNSSPoint required GNSSPointStructure
```

### Finding

Status: OK.

No CE finding opened.

## 8. ViaPoint

### PDF expectation

Expected checked fields:

```text
ViaPointRef              1:1 IBIS-IP.NMTOKEN
PlaceRef                 0:1 IBIS-IP.NMTOKEN
PlaceName                0:* +InternationalTextType
PlaceShortName           0:* +InternationalTextType
ViaPointDisplayPriority  0:1 IBIS-IP.int
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```text
ViaPointStructure:
  ViaPointRef required IBIS-IP.NMTOKEN
  PlaceRef optional IBIS-IP.NMTOKEN
  PlaceName optional repeatable InternationalTextType
  PlaceShortName optional repeatable InternationalTextType
  ViaPointDisplayPriority optional IBIS-IP.int
```

### Finding

Status: OK.

No CE finding opened.

## 9. ZoneType

### PDF expectation

The PDF-side exact spelling for the first field still needs visual confirmation because earlier FareZone tables already showed potentially fragile `Farezone`/`FareZone` casing in extraction.

Expected semantic shape:

```text
FarezoneTypeID / FareZoneTypeID 1:1 IBIS-IP.NMTOKEN
FareZoneTypeName                0:* +InternationalTextType
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```text
ZoneType:
  FarezoneTypeID required IBIS-IP.NMTOKEN
  FareZoneTypeName optional repeatable InternationalTextType
```

### Finding

Status: OK with casing/spelling note pending visual PDF confirmation.

No new CE finding opened yet. If the visual PDF table uses `FareZoneTypeID` while XSD uses `FarezoneTypeID`, this should be linked to `CE-015` or opened as a separate ZoneType casing finding.

## 10. Not closed in this pass

The following names from the continuation plan were not confirmed as standalone `IBIS-IP_common_V2.4.xsd` complexType definitions during this pass:

```text
NetworkLocationPoint
OperationalInformation
PassengerCounting
PassengerCountingData
PathDestination
Route
```

Observed related fields/concepts:

```text
TripInformation contains RouteDirection.
TripInformation contains PathDestinationNumber.
```

Handling:

```text
Do not classify these as missing yet.
First check whether they are:
1. PDF-only common structures,
2. service-specific structures in another XSD,
3. older-version leftovers,
4. differently named XSD structures,
5. or extraction/planning artefacts.
```

This is carried into the validation/semantic backlog instead of opening a CE finding immediately.

## Result of this block

```text
OK in this pass:
GNSSCoordinate
JourneyStopInformation checked core fields
Point / PointType checked core shape
SpecificPoint
StopSequence
TimingPoint
ViaPoint
ZoneType with casing note

Opened finding:
CE-017 TSPPoint Desciption spelling candidate.

Deferred scope resolution:
NetworkLocationPoint / OperationalInformation / PassengerCounting / PassengerCountingData / PathDestination / Route.
```

Next audit block:

```text
Create a Common/Enums V2.4 structure closure pass:
- resolve the deferred names above,
- update the backlog with service-specific routing if needed,
- then mark which V2.4 common structure tables are closed, partial or pending visual PDF confirmation.
```
