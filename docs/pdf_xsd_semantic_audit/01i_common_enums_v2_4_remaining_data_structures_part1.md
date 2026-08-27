# Common structures / enumerations V2.4 - remaining data structures part 1

Status: started, partial.

Scope of this block:

```text
VDV 301-2-1 V2.4 common data structures after the first core block.
Tables covered here:
1  AdditionalAnnouncement
2  Announcement
3  BayArea
4  BeaconPoint
5  CardApplInformation
6  CardTicketData
9  DataAcceptedResponse
10 DataAcceptedResponseData
11 DataVersion
12 DataVersionList
13 Destination
20 DoorCounting
21 DoorCountingList
22 DoorInformation
23 DoorOpenState
24 DoorOperationState
25 DoorState
26 FareZoneInformation
27 GlobalCardStatus
28 GNSSPoint
```

Tables 7-8 and 14-19 were already covered or referenced in `01h_common_enums_v2_4_core_data_structures.md`.

Authority rule:

```text
Validation follows the XSD. PDF differences are retained as provider-facing explanation notes.
```

## 1. AdditionalAnnouncement

### PDF expectation

The PDF table for `AdditionalAnnouncement` defines:

```text
AnnouncementRef        1:1 IBIS-IP.NMTOKEN
AnnouncementText       0:* +InternationalTextType
AnnouncementTTSText    0:* +InternationalTextType
choice:
  ImmediateInformation      1:1 IBIS-IP.boolean
  PeriodicalInformation     1:1 IBIS-IP.duration
  InformationAtSpecificPoint 1:1 +SpecificPoint
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```text
AnnouncementRef required
AnnouncementText minOccurs="0" maxOccurs="unbounded"
AnnouncementTTSText minOccurs="0" maxOccurs="unbounded"
choice minOccurs="0":
  ImmediateInformation
  PeriodicalInformation
  SpecificPoint
```

### Finding

| Item | Status | Notes |
|---|---|---|
| AnnouncementRef | OK | Required in XSD. |
| AnnouncementText | OK | Repeatable optional. |
| AnnouncementTTSText | OK | Repeatable optional. |
| Choice itself | PDF/XSD cardinality note | PDF table wording implies one of the choices; XSD makes the choice optional with `minOccurs="0"`. |
| Third choice element name | mismatch | PDF says `InformationAtSpecificPoint`; XSD says `SpecificPoint`. |

This opens finding `CE-013`.

Tool implication:

```text
If a payload uses <InformationAtSpecificPoint>, validation fails.
Provider-facing note: PDF table names the choice InformationAtSpecificPoint, but XSD defines SpecificPoint. XSD has precedence.
```

Do not change the XSD during this audit.

## 2. Announcement

### PDF expectation

```text
AnnouncementRef      1:1 IBIS-IP.NMTOKEN
AnnouncementText     0:* +InternationalTextType
AnnouncementTTSText  0:* +InternationalTextType
```

### XSD observation / finding

The XSD matches the PDF expectation:

```text
AnnouncementRef required
AnnouncementText minOccurs="0" maxOccurs="unbounded"
AnnouncementTTSText minOccurs="0" maxOccurs="unbounded"
```

Status: OK.

## 3. BayArea

### PDF expectation

```text
BeforeBay 0:1 IBIS-IP.double
BehindBay 0:1 IBIS-IP.double
```

### XSD observation / finding

The XSD contains `BeforeBay` and `BehindBay` as optional `IBIS-IP.double` elements.

Status: OK.

## 4. BeaconPoint

### PDF expectation

```text
PointRef   0:1 IBIS-IP.NMTOKEN
BeaconCode 1:1 IBIS-IP.NMTOKEN
ShortName  0:* +InternationalTextType
Description 0:* +InternationalTextType
```

### XSD observation / finding

The XSD contains:

```text
PointRef optional
BeaconCode required
ShortName optional repeatable
Description optional repeatable
```

Status: OK.

Note: this also confirms the current V2.4 XSD spelling `Description` in this branch.

## 5. CardApplInformation

### PDF expectation

```text
CardApplInformationLength 1:1 IBIS-IP.unsignedInt
CardApplInformationData   1:* IBIS-IP.byte
```

### XSD observation / finding

The XSD type name is `CardApplInformations`, as in the historical schema naming, and contains:

```text
CardApplInformationLength required
CardApplInformationData maxOccurs="unbounded", default minOccurs=1
```

Status: OK with naming note.

The table heading uses singular `CardApplInformation`, while the XSD complexType uses `CardApplInformations`. This is not opened as a CE finding yet because the PDF line itself also shows the plural structure name in the extracted table text and this may be inherited naming.

## 6. CardTicketData

### PDF expectation

```text
CardTicketDataID     1:1 IBIS-IP.unsignedLong
CardTicketDataLength 1:1 IBIS-IP.unsignedInt
CardTicketData       1:* IBIS-IP.byte
```

### XSD observation / finding

The XSD matches:

```text
CardTicketDataID required
CardTicketDataLength required
CardTicketData maxOccurs="unbounded", default minOccurs=1
```

Status: OK.

## 7. DataAcceptedResponse

### PDF expectation

The PDF table lists:

```text
DataAcceptedResponseData 1:1 +DataAcceptedResponseDataStructure
OperationErrorMessage    1:1 IBIS-IP.string
```

Semantically this is an either/or response shape.

### XSD observation / finding

The XSD models this as an `xs:choice`:

```text
DataAcceptedResponseData or OperationErrorMessage
```

Status: OK.

Tool implication:

```text
Both elements together are invalid because the XSD uses a choice.
```

## 8. DataAcceptedResponseData

### PDF expectation

```text
TimeStamp        1:1 IBIS-IP.dateTime
DataAccepted     1:1 IBIS-IP.boolean
ErrorCode        0:1 ErrorCodeEnumeration
ErrorInformation 0:1 IBIS-IP.string
```

### XSD observation / finding

The XSD matches the table expectation.

Status: OK.

## 9. DataVersion

### PDF expectation

```text
DataType   1:1 IBIS-IP.string
VersionRef 1:1 IBIS-IP.NMTOKEN
```

### XSD observation / finding

The XSD matches the PDF expectation.

Status: OK.

## 10. DataVersionList

### PDF expectation

```text
DataVersion 1:* +DataVersion
```

### XSD observation

Observed in XSD:

```xml
<xs:element name="DataVersion" type="DataVersionStructure" minOccurs="0" maxOccurs="unbounded"/>
```

### Finding

The XSD allows an empty `DataVersionList`, while the PDF table describes at least one `DataVersion`.

This opens finding `CE-014`.

Tool implication:

```text
An empty DataVersionList validates against XSD but appears stricter in the PDF table.
Validation follows XSD; provider-facing documentation should note the PDF says 1:*.
```

## 11. Destination

### PDF expectation

```text
DestinationRef       1:1 IBIS-IP.NMTOKEN
DestinationName      0:* +InternationalTextType
DestinationShortName 0:* +InternationalTextType
```

### XSD observation / finding

The XSD matches the PDF expectation.

Status: OK.

The PDF also describes multi-line `DestinationName` behaviour. This is documentation-level display behaviour and is not fully enforceable by XSD beyond allowing repeated `DestinationName` elements.

## 12. DoorCounting

### PDF expectation

```text
ObjectClass  1:1 DoorCountingObjectClassEnumeration
In           1:1 IBIS-IP.int
Out          1:1 IBIS-IP.int
CountQuality 0:1 DoorCountingQualityEnumeration
```

### XSD observation / finding

The XSD matches the PDF expectation.

Status: OK.

## 13. DoorCountingList

### PDF expectation

```text
DoorID   1:1 IBIS-IP.NMTOKEN
CountSet 1:* +DoorCounting
```

### XSD observation / finding

The XSD matches:

```text
DoorID required
CountSet maxOccurs="unbounded", default minOccurs=1
```

Status: OK.

## 14. DoorInformation

### PDF expectation

```text
DoorID 1:1 IBIS-IP.NMTOKEN
Count  1:* +DoorCounting
State  0:1 +DoorState
```

### XSD observation / finding

The XSD matches:

```text
DoorID required
Count maxOccurs="unbounded", default minOccurs=1
State optional
```

Status: OK.

## 15. DoorOpenState

### PDF expectation

```text
Value     1:1 DoorOpenStateEnumeration
ErrorCode 0:1 ErrorCodeEnumeration
```

### XSD observation / finding

The XSD matches.

Status: OK.

## 16. DoorOperationState

### PDF expectation

```text
Value     1:1 DoorOperationStateEnumeration
ErrorCode 0:1 ErrorCodeEnumeration
```

### XSD observation / finding

The XSD matches.

Status: OK.

## 17. DoorState

### PDF expectation

```text
OpenState      1:1 +DoorOpenState
OperationState 0:1 +DoorOperationState
```

### XSD observation / finding

The XSD matches.

Status: OK.

## 18. FareZoneInformation

### PDF expectation

The PDF table extraction shows the element names as:

```text
FarezoneID
FarezoneType
FarezoneLongName
FarezoneShortName
```

with cardinalities:

```text
FarezoneID        1:1 IBIS-IP.NMTOKEN
FarezoneType      0:1 +ZoneType
FarezoneLongName  0:* +InternationalTextType
FarezoneShortName 0:* +InternationalTextType
```

### XSD observation

The XSD uses camel-case names with capital `Z`:

```text
FareZoneID
FareZoneType
FareZoneLongName
FareZoneShortName
```

with matching cardinalities/types.

### Finding

This is a potential case-sensitive PDF/XSD element-name discrepancy. Because the PDF extraction may be affected by table formatting, this is opened conservatively as `CE-015` for manual visual/PDF confirmation.

Tool implication if confirmed:

```text
Payloads using FarezoneID / FarezoneType will fail against the XSD.
Allowed XSD names are FareZoneID / FareZoneType.
PDF note can explain the documentation casing difference, if confirmed visually.
```

## 19. GlobalCardStatus

### PDF expectation

```text
GlobalCardStatusID   1:1 IBIS-IP.unsignedInt
GlobalCardStatusText 0:* IBIS-IP.string
```

### XSD observation

The XSD complex type is named `GlobalCardStatus`, but its ID element is spelled:

```text
GlobalCardStausID
```

The text element is:

```text
GlobalCardStatusText minOccurs="0" maxOccurs="unbounded"
```

### Finding

This opens finding `CE-016`.

Tool implication:

```text
Payloads using GlobalCardStatusID, as printed in the PDF, will fail against the XSD.
The XSD-accepted element name is GlobalCardStausID.
Because XSD has precedence, validation follows the typo-like XSD spelling unless/until an official schema correction exists.
```

This is a high-value provider-facing note because it looks like a spelling error but is still technically authoritative for XSD validation.

## 20. GNSSPoint

### PDF expectation

```text
PointRef  0:1 IBIS-IP.NMTOKEN
Longitude 1:1 +GNSSCoordinate
Latitude  1:1 +GNSSCoordinate
Altitude  0:1 IBIS-IP.double
```

### XSD observation / finding

The XSD matches:

```text
PointRef optional
Longitude required GNSSCoordinateStructure
Latitude required GNSSCoordinateStructure
Altitude optional IBIS-IP.double
```

Status: OK.

## Result of this block

```text
OK:
Announcement, BayArea, BeaconPoint, CardApplInformation, CardTicketData,
DataAcceptedResponse, DataAcceptedResponseData, DataVersion, Destination,
DoorCounting, DoorCountingList, DoorInformation, DoorOpenState,
DoorOperationState, DoorState, GNSSPoint.

Opened/updated findings:
CE-013 AdditionalAnnouncement choice naming/cardinality difference.
CE-014 DataVersionList PDF 1:* vs XSD 0:*.
CE-015 FareZoneInformation casing difference, visual PDF confirmation needed.
CE-016 GlobalCardStatusID vs GlobalCardStausID spelling difference.
```

Next audit block:

```text
Continue with common data structures from GNSSCoordinate onward:
GNSSCoordinate
JourneyStopInformation
LineInformation follow-up if needed
LocationState
NetworkLocationPoint
OperationalInformation
PassengerCounting / PassengerCountingData family
PathDestination / Point / Route / SpecificPoint / StopSequence / TimingPoint / ViaPoint / ZoneType
```
