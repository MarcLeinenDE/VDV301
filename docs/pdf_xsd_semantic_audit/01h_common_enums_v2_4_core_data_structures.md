# Common structures / enumerations V2.4 - core data structure audit

Status: started, first core-structure block completed.

Scope of this block:

```text
VDV 301-2-1 V2.4 common data structures, selected core structures:
- Connection
- DeviceInformation / DeviceSpecification family
- DisplayContent
- LineInformation
- StopInformation
- StopInformationRequest
- TripInformation
```

This file continues after:

```text
01f_common_enums_v2_4_pdf_vs_xsd_enum_diff.md
01g_common_enums_v2_4_datatypes_core_structures.md
```

Authority rule:

```text
Executable validation follows XSD.
PDF tables are recorded as documentation evidence and provider-facing explanation.
If PDF and XSD disagree, validation follows XSD and the discrepancy is tracked.
```

See also:

```text
docs/pdf_xsd_semantic_audit/VALIDATION_AUTHORITY.md
```

## 1. Connection

### PDF expectation

VDV 301-2-1 V2.4 table 8 describes `Connection` with:

```text
StopRef                 1:1 IBIS-IP.NMTOKEN
ConnectionRef           1:1 IBIS-IP.NMTOKEN
ConnectionType          1:1 ConnectionTypeEnumeration
DisplayContent          0:1 +DisplayContent
Platform                0:1 IBIS-IP.string
ConnectionState         0:1 ConnectionStateEnumeration
TransportMode           0:* +Vehicle, deprecated
ConnectionMode          0:* NetexMode
ExpectedDepartureTime   0:1 IBIS-IP.dateTime
ScheduledDepartureTime  0:1 IBIS-IP.dateTime
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:complexType name="ConnectionStructure">
  <xs:sequence>
    <xs:element name="StopRef" type="IBIS-IP.NMTOKEN"/>
    <xs:element name="ConnectionRef" type="IBIS-IP.NMTOKEN"/>
    <xs:element name="ConnectionType" type="ConnectionTypeEnumeration"/>
    <xs:element name="DisplayContent" type="DisplayContentStructure" minOccurs="0"/>
    <xs:element name="Platform" type="IBIS-IP.string" minOccurs="0"/>
    <xs:element name="ConnectionState" type="ConnectionStateEnumeration" minOccurs="0"/>
    <xs:element name="TransportMode" type="VehicleStructure" minOccurs="0"/>
    <xs:element name="ConnectionMode" type="NetexMode" minOccurs="0"/>
    <xs:element name="ExpectedDepartureTime" type="IBIS-IP.dateTime" minOccurs="0"/>
    <xs:element name="ScheduledDepartureTime" type="IBIS-IP.dateTime" minOccurs="0"/>
  </xs:sequence>
</xs:complexType>
```

### Finding

| Item | Status | Notes |
|---|---|---|
| Required base fields | OK | StopRef, ConnectionRef and ConnectionType are required in both PDF and XSD. |
| DisplayContent / Platform / ConnectionState / times | OK | Optional in both PDF and XSD. |
| TransportMode cardinality | discrepancy candidate | PDF says `0:*`; XSD has `minOccurs="0"` only, therefore XSD permits at most one. |
| ConnectionMode cardinality | discrepancy candidate | PDF says `0:*`; XSD has `minOccurs="0"` only, therefore XSD permits at most one. |
| Validation authority | XSD | Repeated `TransportMode` or `ConnectionMode` entries should fail XSD validation even though the PDF table suggests `0:*`. |

Opened as `CE-011` in `findings.md`.

Provider-facing implication:

```text
FAIL: repeated ConnectionMode/TransportMode is not accepted by the XSD.
PDF note: VDV 301-2-1 V2.4 table 8 lists 0:* for these fields, but the XSD allows only 0:1. Since XSD has precedence, validation follows the XSD.
```

## 2. DeviceInformation / DeviceSpecification family

### PDF expectation

Tables 14 to 18 describe:

```text
DeviceInformation:
  DeviceInformationGroup: DeviceName, Manufacturer, SerialNumber, DeviceClass all 1:1
  DataVersionList 0:1
  WebInterfaceAddress 0:1

DeviceSpecification:
  DeviceClass 1:1
  DeviceID 1:1

DeviceSpecificationList:
  DeviceSpecification 1:*

DeviceSpecificationWithState:
  DeviceSpecification 1:1
  DeviceState 1:1

DeviceSpecificationWithStateList:
  DeviceSpecificationWithState 1:*
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:complexType name="DeviceInformationStructure">
  <xs:sequence>
    <xs:group ref="DeviceInformationGroup"/>
    <xs:element name="DataVersionList" type="DataVersionListStructure" minOccurs="0"/>
    <xs:element name="WebInterfaceAddress" type="IBIS-IP.anyURI" minOccurs="0"/>
  </xs:sequence>
</xs:complexType>

<xs:complexType name="DeviceSpecificationListStructure">
  <xs:sequence>
    <xs:element name="DeviceSpecification" type="DeviceSpecificationStructure" maxOccurs="unbounded"/>
  </xs:sequence>
</xs:complexType>

<xs:complexType name="DeviceSpecificationWithStateListStructure">
  <xs:sequence>
    <xs:element name="DeviceSpecificationWithState" type="DeviceSpecificationWithStateStructure" minOccurs="0" maxOccurs="unbounded"/>
  </xs:sequence>
</xs:complexType>
```

### Finding

| Item | Status | Notes |
|---|---|---|
| DeviceInformation | OK | Required group and optional DataVersionList/WebInterfaceAddress align with PDF. |
| DeviceSpecification | OK | DeviceClass and DeviceID required. |
| DeviceSpecificationList | OK | XSD default minOccurs=1 and maxOccurs=unbounded matches 1:*. |
| DeviceSpecificationWithState | OK | DeviceSpecification and DeviceState required. |
| DeviceSpecificationWithStateList | discrepancy candidate | PDF says 1:*; XSD has minOccurs=0, maxOccurs=unbounded. |
| Validation authority | XSD | An empty `DeviceSpecificationWithStateList` may validate against XSD even though the PDF table indicates at least one entry. |

Opened as `CE-012` in `findings.md`.

## 3. DisplayContent

### PDF expectation

VDV 301-2-1 V2.4 table 19 describes `DisplayContent` with:

```text
DisplayContentRef       0:1 IBIS-IP.NMTOKEN
LineInformation         1:1 +LineInformation
Destination             1:1 +Destination
ViaPoint                0:* +ViaPoint
AdditionalInformation   0:* +InternationalTextType
AdditionalInformation(n) 0:* +InternationalTextType, n = 1 to 9
RunNumber               0:1 +IBIS-IP.int
DisplayPolicy group: Priority, PeriodDuration, Duration each 0:1
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:element name="DisplayContentRef" type="IBIS-IP.NMTOKEN" minOccurs="0"/>
<xs:element name="LineInformation" type="LineInformationStructure"/>
<xs:element name="Destination" type="DestinationStructure"/>
<xs:element name="ViaPoint" type="ViaPointStructure" minOccurs="0" maxOccurs="unbounded"/>
<xs:element name="AdditionalInformation" type="InternationalTextType" minOccurs="0" maxOccurs="unbounded"/>
<xs:element name="AdditionalInformation1" type="InternationalTextType" minOccurs="0" maxOccurs="unbounded"/>
...
<xs:element name="AdditionalInformation9" type="InternationalTextType" minOccurs="0" maxOccurs="unbounded"/>
<xs:element name="RunNumber" type="IBIS-IP.int" minOccurs="0"/>
<xs:group ref="DisplayPolicyGroup" minOccurs="0"/>
```

### Finding

| Item | Status | Notes |
|---|---|---|
| Required LineInformation / Destination | OK | Required in both PDF and XSD. |
| DisplayContentRef / RunNumber / DisplayPolicy | OK | Optional in both PDF and XSD. |
| ViaPoint | OK | 0:* in both PDF and XSD. |
| AdditionalInformation base and numbered 1..9 | OK | 0:* in both PDF and XSD. |

No new CE finding opened.

## 4. LineInformation

### PDF expectation

VDV 301-2-1 V2.4 table 31 describes `LineInformation` with the established fields `LineRef`, `LineName`, `LineShortName`, `LineNumber`, `LineCode` and the V2.4 additions:

```text
LinePublicCode  0:1 IBIS-IP.string
LineSymbolText  0:1 IBIS-IP.string
ExternalLineRef 0:1 IBIS-IP.string
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:element name="LinePublicCode" type="IBIS-IP.string" minOccurs="0"/>
<xs:element name="LineSymbolText" type="IBIS-IP.string" minOccurs="0"/>
<xs:element name="ExternalLineRef" type="IBIS-IP.string" minOccurs="0"/>
```

### Finding

| Item | Status | Notes |
|---|---|---|
| V2.4 additions | OK | Names, type family and optional cardinality align. |
| LineSymbolCode naming note | OK with note | V2.4 version history mentions rename/wording around LineSymbolCode; table and XSD have LineSymbolText as the added XML element. |

No new CE finding opened.

## 5. StopInformation / StopInformationRequest

### PDF expectation

VDV 301-2-1 V2.4 table 50 describes `StopInformation` with core required fields and V2.4 additions:

```text
StopIndex          1:1 IBIS-IP.int
StopRef            1:1 IBIS-IP.NMTOKEN
StopName           1:* +InternationalTextType
StopAlternativeName 0:* +InternationalTextType
Platform           0:1 IBIS-IP.string
DisplayContent     1:* +DisplayContent
StopAnnouncement   0:* +Announcement
Arrival/Departure fields optional
Connection         0:* +Connection
FareZone           0:* IBIS-IP.NMTOKEN
StopShortName      0:* +InternationalTextType
StopLongNo         0:1 IBIS-IP.int
PointNumber        0:1 IBIS-IP.int
StopGlobalID       0:1 IBIS-IP.string
StopPointGlobalID  0:1 IBIS-IP.string
```

Table 51 describes `StopInformationRequest` as a reduced request structure with optional identification fields and required repeated `DisplayContent`.

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:element name="StopName" type="InternationalTextType" maxOccurs="unbounded"/>
<xs:element name="StopAlternativeName" type="InternationalTextType" minOccurs="0" maxOccurs="unbounded"/>
<xs:element name="Platform" type="IBIS-IP.string" minOccurs="0"/>
<xs:element name="DisplayContent" type="DisplayContentStructure" maxOccurs="unbounded"/>
<xs:element name="StopAnnouncement" type="AnnouncementStructure" minOccurs="0" maxOccurs="unbounded"/>
<xs:element name="Connection" type="ConnectionStructure" minOccurs="0" maxOccurs="unbounded"/>
```

The earlier V2.4 delta audit also observed the V2.4 additions `StopShortName`, `StopLongNo`, `PointNumber`, `StopGlobalID` and `StopPointGlobalID` in the XSD.

### Finding

| Item | Status | Notes |
|---|---|---|
| StopInformation required/optional core | OK, partial | Observed XSD snippets align with PDF for the checked fields. |
| V2.4 additions | OK | Previously checked; names and cardinalities align, with CE-002 note for version-history wording `StopPointNumber` vs table/XSD `PointNumber`. |
| StopInformationRequest | OK, partial | DisplayContent is required 1:* in PDF and XSD; request identification fields are optional in XSD as in PDF. |

No new CE finding opened beyond existing `CE-002`.

## 6. TripInformation

### PDF expectation

VDV 301-2-1 V2.4 table 57 describes `TripInformation` with:

```text
TripRef                  1:1 IBIS-IP.NMTOKEN
StopSequence             1:1 +StopSequence
LocationState            0:1 LocationStateEnumeration
TimetableDelay           0:1 IBIS-IP.int
AdditionalTextMessage    0:* +InternationalTextType
AdditionalTextMessage(n) 0:* +InternationalTextType, n = 1 to 9
AdditionalAnnouncement   0:* +AdditionalAnnouncement
RouteDirection           0:1 RouteDirectionEnumeration
RunNumber                0:1 IBIS-IP.int
PatternNumber            0:1 IBIS-IP.int
PathDestinationNumber    0:1 IBIS-IP.int
BlockNumber              0:1 IBIS-IP.int
ExternalVehicleJourneyRef 0:1 IBIS-IP.string
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:element name="RouteDirection" type="RouteDirectionEnumeration" minOccurs="0"/>
<xs:element name="RunNumber" type="IBIS-IP.int" minOccurs="0"/>
<xs:element name="PatternNumber" type="IBIS-IP.int" minOccurs="0"/>
<xs:element name="PathDestinationNumber" type="IBIS-IP.int" minOccurs="0"/>
<xs:element name="BlockNumber" type="IBIS-IP.int" minOccurs="0"/>
<xs:element name="ExternalVehicleJourneyRef" type="IBIS-IP.string" minOccurs="0"/>
```

The known `AdditionalTextMessage` mismatch is tracked separately as `CE-005`.

### Finding

| Item | Status | Notes |
|---|---|---|
| Core fields | OK, partial | TripRef, StopSequence, LocationState and TimetableDelay remain to be shown in a tighter XSD snippet, but no mismatch has been observed. |
| RunNumber / PatternNumber / PathDestinationNumber / BlockNumber / ExternalVehicleJourneyRef | OK | Observed optional fields align with PDF. |
| AdditionalTextMessage cardinality | confirmed historical mismatch | PDF says 0:* for base and numbered fields; XSD permits only 0:1 per named field. Tracked as CE-005. |
| Validation authority | XSD | Repeated `AdditionalTextMessage` values fail XSD even if the PDF table suggests 0:*. Provider note must cite CE-005. |

No new CE finding opened in this subsection.

## 7. Result of this block

```text
New findings opened:
- CE-011 Connection TransportMode/ConnectionMode cardinality PDF 0:* vs XSD 0:1.
- CE-012 DeviceSpecificationWithStateList PDF 1:* vs XSD 0:*.

Confirmed no new mismatch in this pass for:
- DisplayContent
- LineInformation V2.4 additions
- StopInformation V2.4 additions
- TripInformation V2.4 additions except already-known CE-005
```

## 8. Next audit step

Continue Common/Enums V2.4 structures in table order, likely:

```text
01i_common_enums_v2_4_remaining_data_structures_part1.md

AdditionalAnnouncement
Announcement
BayArea
BeaconPoint
CardApplInformation
CardTicketData
CardType
DataAcceptedResponse
DataAcceptedResponseData
DataVersion
DataVersionList
Destination
DoorCounting / DoorInformation / DoorState family
```

Do not change any XSD during this audit step.
