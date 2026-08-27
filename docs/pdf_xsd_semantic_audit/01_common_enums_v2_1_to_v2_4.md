# Common structures / enumerations V2.1 to V2.4 - PDF/XSD semantic audit

Status: started, partial.

Scope of this first block:

```text
IBIS-IP_common_V2.1.xsd
IBIS-IP_common_V2.2.xsd
IBIS-IP_common_V2.3.xsd
IBIS-IP_common_V2.4.xsd
IBIS-IP_Enumerations_V2.1.xsd
IBIS-IP_Enumerations_V2.2.xsd
IBIS-IP_Enumerations_V2.4.xsd
```

Open structural question:

```text
No IBIS-IP_Enumerations_V2.3.xsd is present in the branch.
IBIS-IP_common_V2.3.xsd includes IBIS-IP_Enumerations_V2.2.xsd.
This may be intentional, but remains an explicit audit point.
```

## Sources used in this block

PDF sources:

```text
VDV-Schrift 301-2-1 V2.1, 07/2018
VDV-Schrift 301-2-1 V2.2, 08/2019
VDV-Schrift 301-2-1 V2.3, 02/2021
VDV-Schrift 301-2-1 V2.4, 01/2023
```

XSD sources:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

This file currently focuses on version-history deltas. Full table-by-table structure checks remain pending.

## 1. V2.1 delta check

### PDF delta basis

VDV 301-2-1 V2.2 contains the V2.1 history section. Relevant V2.1 changes listed there:

```text
DeviceClassEnumeration: MultiFunctionalDisplay added
ErrorCodeEnumeration: OperationNotSupported added
ServiceNameEnumeration: DoorStateService, TrainSetDataService, TrainSetInformationService,
TrainSetManagementService, TicketValidationService, HTMLDisplayService added
InternationalTextType extended with inline formatting
DestinationStructure multiline texts defined
DisplayContent supply of separate contents to different displays defined
```

### XSD audit status

| Item | Status | Notes |
|---|---|---|
| MultiFunctionalDisplay in DeviceClassEnumeration | not checked yet | To be verified in IBIS-IP_Enumerations_V2.1.xsd. |
| OperationNotSupported in ErrorCodeEnumeration | not checked yet | To be verified in IBIS-IP_Enumerations_V2.1.xsd. |
| ServiceNameEnumeration additions | not checked yet | To be verified in IBIS-IP_Enumerations_V2.1.xsd. |
| InternationalTextType inline formatting | not checked yet | Needs table-level PDF/XSD comparison. |
| DestinationStructure multiline text handling | not checked yet | Needs table-level PDF/XSD comparison. |
| DisplayContent separate display content support | not checked yet | Needs table-level PDF/XSD comparison. |

## 2. V2.2 delta check

### PDF delta basis

VDV 301-2-1 V2.2 lists the following V2.2 functional additions/corrections:

```text
LineCode added to DisplayContent / LineInformation area
TripStateEnumeration added
ConnectionMode added to Connection, including NetexMode and Mode/SubMode enumerations
NetexMode added as new datatype
CombiDevice added as DeviceClass
SystemDocumentationService and SystemManagementService removed; SystemMonitoringService added in ServiceNameEnumeration
TransportMode note points to ConnectionMode instead
Heartbeat notes added
```

### XSD audit status

| Item | Status | Notes |
|---|---|---|
| LineCode | not checked yet | To be verified in common V2.2. |
| TripStateEnumeration | not checked yet | To be verified in enumerations V2.2. |
| ConnectionMode / NetexMode | not checked yet | To be verified in common V2.2 and enumerations V2.2. |
| CombiDevice | not checked yet | To be verified in enumerations V2.2. |
| ServiceNameEnumeration switch to SystemMonitoringService | not checked yet | To be verified in enumerations V2.2. |
| Heartbeat notes | not checked yet | Needs table-level check. |

## 3. V2.3 delta check

### PDF delta basis

VDV 301-2-1 V2.3 lists these V2.3 functional additions:

```text
AdditionalInformation(s) inserted in DisplayContent
RunNumber inserted in DisplayContent
ArrivalExpected inserted in StopInformation / StopInformationRequest
DepartureExpected inserted in StopInformation / StopInformationRequest
RunNumber inserted in TripInformation
PatternNumber inserted in TripInformation
PathDestinationNumber inserted in TripInformation
AdditionalTextMessage(s) inserted in TripInformation
```

### XSD evidence observed so far

Observed in `IBIS-IP_common_V2.3.xsd`:

```xml
<xs:include schemaLocation="IBIS-IP_Enumerations_V2.2.xsd"/>
```

Observed in the V2.3 common XSD:

```xml
<xs:element name="AdditionalInformation" type="InternationalTextType" minOccurs="0" maxOccurs="unbounded">
...
<xs:element name="AdditionalInformation1" type="InternationalTextType" minOccurs="0" maxOccurs="unbounded">
...
<xs:element name="RunNumber" type="IBIS-IP.int" minOccurs="0">
```

Observed in StopInformation:

```xml
<xs:element name="ArrivalExpected" type="IBIS-IP.dateTime" minOccurs="0">
...
<xs:element name="DepartureExpected" type="IBIS-IP.dateTime" minOccurs="0"/>
```

Observed in TripInformation:

```xml
<xs:element name="RunNumber" type="IBIS-IP.int" minOccurs="0">
<xs:element name="PatternNumber" type="IBIS-IP.int" minOccurs="0">
<xs:element name="PathDestinationNumber" type="IBIS-IP.int" minOccurs="0">
```

### V2.3 findings

| Item | Status | Notes |
|---|---|---|
| AdditionalInformation(s) in DisplayContent | OK, partial | Present in common V2.3; exact PDF cardinalities still need table check. |
| RunNumber in DisplayContent | OK, partial | Present after AdditionalInformation group; exact location/cardinality to be checked. |
| ArrivalExpected in StopInformation | OK, partial | Present as optional IBIS-IP.dateTime. |
| DepartureExpected in StopInformation | OK, partial | Present as optional IBIS-IP.dateTime. |
| RunNumber in TripInformation | OK, partial | Present as optional IBIS-IP.int. |
| PatternNumber in TripInformation | OK, partial | Present as optional IBIS-IP.int. |
| PathDestinationNumber in TripInformation | OK, partial | Present as optional IBIS-IP.int. |
| AdditionalTextMessage(s) in TripInformation | not checked yet | Need targeted XSD/table check. |
| Enumerations V2.3 | Unclear | No separate `IBIS-IP_Enumerations_V2.3.xsd`; common V2.3 includes V2.2 enumerations. Need confirm against PDF/index and intended schema-family practice. |

## 4. V2.4 delta check

### PDF delta basis

VDV 301-2-1 V2.4 lists these V2.4 functional additions/corrections:

```text
LinePublicCode inserted in LineInformation
LineSymbolText inserted in LineInformation
ExternalLineRef inserted in LineInformation
StopShortName inserted in StopInformation
StopLongNo inserted in StopInformation
StopPointNumber inserted in StopInformation, but the actual table uses PointNumber
StopGlobalID inserted in StopInformation
StopPointGlobalID inserted in StopInformation
BlockNumber inserted in TripInformation
LineSymbolCode renamed in LineInformation
Attribute descriptions extended in LineInformation, StopInformation and TripInformation
DoorCountingObjectClassEnumeration corrected
```

### XSD evidence observed so far

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:include schemaLocation="IBIS-IP_Enumerations_V2.4.xsd"/>
```

Observed in LineInformation-related XSD area:

```xml
<xs:element name="LinePublicCode" type="IBIS-IP.string" minOccurs="0">
<xs:element name="LineSymbolText" type="IBIS-IP.string" minOccurs="0">
<xs:element name="ExternalLineRef" type="IBIS-IP.string" minOccurs="0">
```

Observed in StopInformation:

```xml
<xs:element name="StopShortName" type="InternationalTextType" minOccurs="0" maxOccurs="unbounded">
<xs:element name="StopLongNo" type="IBIS-IP.int" minOccurs="0">
<xs:element name="PointNumber" type="IBIS-IP.int" minOccurs="0">
<xs:element name="StopGlobalID" type="IBIS-IP.string" minOccurs="0">
<xs:element name="StopPointGlobalID" type="IBIS-IP.string" minOccurs="0">
```

Observed in TripInformation:

```xml
<xs:element name="BlockNumber" type="IBIS-IP.int" minOccurs="0">
```

Observed in `IBIS-IP_Enumerations_V2.4.xsd`:

```xml
<xs:simpleType name="DoorCountingObjectClassEnumeration">
  ...
  <xs:enumeration value="Wheelchair"/>
  ...
</xs:simpleType>
```

### V2.4 findings

| Item | Status | Notes |
|---|---|---|
| common V2.4 includes enumerations V2.4 | OK | Present. |
| LinePublicCode | OK, partial | Present as optional IBIS-IP.string. |
| LineSymbolText | OK, partial | Present as optional IBIS-IP.string. |
| ExternalLineRef | OK, partial | Present as optional IBIS-IP.string. |
| StopShortName | OK, partial | Present as optional unbounded InternationalTextType. |
| StopLongNo | OK, partial | Present as optional IBIS-IP.int. |
| StopPointNumber / PointNumber | OK with note | PDF version history says StopPointNumber, but the actual PDF table uses PointNumber and the XSD uses PointNumber. Treat as OK-with-note unless VDV confirms the version-history wording is normative. |
| StopGlobalID | OK, partial | Present as optional IBIS-IP.string. |
| StopPointGlobalID | OK, partial | Present as optional IBIS-IP.string. |
| BlockNumber | OK, partial | Present as optional IBIS-IP.int. |
| DoorCountingObjectClassEnumeration correction | OK, partial | V2.4 PDF table lists Wheelchair; XSD V2.4 contains Wheelchair. |
| LineSymbolCode rename | not checked yet | Need targeted check against previous version and V2.4 table. |
| Attribute descriptions extended | not checked yet | Documentation-level comparison; no schema validity impact unless annotations are required. |

## 5. Immediate findings from this block

### CE-001: No separate Enumerations V2.3 file in branch

State: unclear.

`IBIS-IP_common_V2.3.xsd` includes `IBIS-IP_Enumerations_V2.2.xsd`, and the branch has no `IBIS-IP_Enumerations_V2.3.xsd`.

Interpretation:

- This may be intentional if V2.3 introduced only common structures and no enumeration-file delta.
- It still needs confirmation from PDF tables/version history and repository history.

### CE-002: V2.4 StopPointNumber wording differs from actual table/XSD name

State: OK with note.

The V2.4 version history says `StopPointNumber`, while the actual StopInformation table uses `PointNumber`, and the XSD uses `PointNumber`.

Interpretation:

- Do not rename the XSD field based on the version-history wording alone.
- Treat the table/XSD pairing as stronger evidence until proven otherwise.

### CE-003: V2.4 common/enums delta is promising but not fully closed

State: partial OK.

The main V2.4 additions observed in version history are present in the V2.4 XSD files. Still pending:

```text
LineSymbolCode rename check
full table cardinality comparison for affected structures
schema-pool compile
sample validation
```

## 6. Next steps

1. Finish V2.4 table-level checks for LineInformation, StopInformation and TripInformation.
2. Check V2.4 Enumerations table-level values, starting with DoorCountingObjectClassEnumeration.
3. Finish V2.3 TripInformation / DisplayContent exact cardinality checks.
4. Resolve the missing/intentional `Enumerations V2.3` question.
5. Then move backwards to V2.2 and V2.1 table-level checks.
