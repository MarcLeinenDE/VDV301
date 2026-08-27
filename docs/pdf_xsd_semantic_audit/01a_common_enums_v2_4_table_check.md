# Common structures / enumerations V2.4 - table-level PDF/XSD audit

Status: started, partial but table-level for the V2.4-changed areas.

Scope of this file:

```text
VDV-Schrift 301-2-1 V2.4, 01/2023
IBIS-IP_common_V2.4.xsd
IBIS-IP_Enumerations_V2.4.xsd
```

This file extends `01_common_enums_v2_1_to_v2_4.md` with a closer table-level check for the V2.4-changed structures and enumerations. It does not yet close the full Common/Enums audit.

## 1. Source anchors

PDF anchors used from VDV-Schrift 301-2-1 V2.4:

```text
2.31 LineInformation / Table 31
2.50 StopInformation / Table 50
2.51 StopInformationRequest / Table 51
2.57 TripInformation / Table 57
3.7 DoorCountingObjectClassEnumeration / Table 71
3.21 ServiceNameEnumeration / Table 85
4.6 Version 2.4 version history
```

XSD anchors used from `dev/schema-integration`:

```text
IBIS-IP_common_V2.4.xsd
IBIS-IP_Enumerations_V2.4.xsd
```

## 2. LineInformation V2.4

### PDF expectation

The V2.4 LineInformation table contains these V2.4-relevant rows:

| Element | PDF cardinality | PDF type |
|---|---:|---|
| `LinePublicCode` | `0:1` | `IBIS-IP.string` |
| `LineSymbolText` | `0:1` | `IBIS-IP.string` |
| `ExternalLineRef` | `0:1` | `IBIS-IP.string` |

The V2.4 version history also says that `LineSymbolCode` was renamed in the LineInformation structure.

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:element name="LinePublicCode" type="IBIS-IP.string" minOccurs="0">
<xs:element name="LineSymbolText" type="IBIS-IP.string" minOccurs="0">
<xs:element name="ExternalLineRef" type="IBIS-IP.string" minOccurs="0">
```

No separate `LineSymbolCode` element was observed in the checked V2.4 LineInformation snippet. The name occurs only in the documentation text for `LineSymbolText` as an alternative/reference concept.

### Result

| Check | Result | Notes |
|---|---|---|
| `LinePublicCode` type/cardinality | OK | PDF `0:1 IBIS-IP.string`; XSD optional string. |
| `LineSymbolText` type/cardinality | OK | PDF `0:1 IBIS-IP.string`; XSD optional string. |
| `ExternalLineRef` type/cardinality | OK | PDF `0:1 IBIS-IP.string`; XSD optional string. |
| `LineSymbolCode` rename | likely OK, needs previous-version diff | V2.4 XSD does not contain a dedicated `LineSymbolCode` element in the checked area. Need compare against V2.3/common history before closing. |

## 3. StopInformation V2.4

### PDF expectation

The V2.4 StopInformation table contains these V2.4-relevant rows:

| Element | PDF cardinality | PDF type |
|---|---:|---|
| `StopShortName` | `0:*` | `+InternationalTextType` |
| `StopLongNo` | `0:1` | `IBIS-IP.int` |
| `PointNumber` | `0:1` | `IBIS-IP.int` |
| `StopGlobalID` | `0:1` | `IBIS-IP.string` |
| `StopPointGlobalID` | `0:1` | `IBIS-IP.string` |

Note: the V2.4 version history says `StopPointNumber`, but the actual StopInformation table uses `PointNumber`.

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:element name="StopShortName" type="InternationalTextType" minOccurs="0" maxOccurs="unbounded">
<xs:element name="StopLongNo" type="IBIS-IP.int" minOccurs="0">
<xs:element name="PointNumber" type="IBIS-IP.int" minOccurs="0">
<xs:element name="StopGlobalID" type="IBIS-IP.string" minOccurs="0">
<xs:element name="StopPointGlobalID" type="IBIS-IP.string" minOccurs="0">
```

### Result

| Check | Result | Notes |
|---|---|---|
| `StopShortName` type/cardinality | OK | PDF `0:* +InternationalTextType`; XSD optional unbounded `InternationalTextType`. |
| `StopLongNo` type/cardinality | OK | PDF `0:1 IBIS-IP.int`; XSD optional `IBIS-IP.int`. |
| `PointNumber` type/cardinality | OK with note | PDF table and XSD align on `PointNumber`. Version history says `StopPointNumber`; do not rename from table/XSD evidence alone. |
| `StopGlobalID` type/cardinality | OK | PDF `0:1 IBIS-IP.string`; XSD optional string. |
| `StopPointGlobalID` type/cardinality | OK | PDF `0:1 IBIS-IP.string`; XSD optional string. |

## 4. StopInformationRequest V2.4

### PDF expectation

The V2.4 StopInformationRequest table contains `ArrivalExpected` and `DepartureExpected` but does not show the V2.4 stop-name / stop-global-ID extension fields from StopInformation.

### Result

| Check | Result | Notes |
|---|---|---|
| New StopInformation-only V2.4 fields are absent from StopInformationRequest | OK by PDF table | Do not add `StopShortName`, `StopLongNo`, `PointNumber`, `StopGlobalID` or `StopPointGlobalID` to StopInformationRequest based only on the version-history wording. |
| `ArrivalExpected` / `DepartureExpected` in StopInformationRequest | inherited from V2.3; OK pending full row check | Already part of V2.3 delta; not a new V2.4 change. |

## 5. TripInformation V2.4

### PDF expectation

The V2.4 TripInformation table contains:

| Element | PDF cardinality | PDF type |
|---|---:|---|
| `BlockNumber` | `0:1` | `IBIS-IP.int` |

The same table also contains the V2.3 additions `RunNumber`, `PatternNumber`, `PathDestinationNumber` and `AdditionalTextMessage(n)`.

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:element name="BlockNumber" type="IBIS-IP.int" minOccurs="0">
```

### Result

| Check | Result | Notes |
|---|---|---|
| `BlockNumber` type/cardinality | OK | PDF `0:1 IBIS-IP.int`; XSD optional `IBIS-IP.int`. |
| V2.3 TripInformation additions carried into V2.4 | partially OK | `RunNumber`, `PatternNumber`, `PathDestinationNumber` were observed earlier. `AdditionalTextMessage(n)` still needs targeted check. |

## 6. DoorCountingObjectClassEnumeration V2.4

### PDF expectation

The V2.4 table lists:

```text
Adult
Bike
Child
Pram
Wheelchair
Unidentified
Other
```

### XSD observation

Observed in `IBIS-IP_Enumerations_V2.4.xsd`:

```xml
<xs:simpleType name="DoorCountingObjectClassEnumeration">
  ...
  <xs:enumeration value="Adult"/>
  <xs:enumeration value="Bike"/>
  <xs:enumeration value="Child"/>
  <xs:enumeration value="Pram"/>
  <xs:enumeration value="Wheelchair"/>
  <xs:enumeration value="Unidentified"/>
  <xs:enumeration value="Other"/>
  ...
</xs:simpleType>
```

### Result

| Check | Result | Notes |
|---|---|---|
| `DoorCountingObjectClassEnumeration` values | OK | Values match the V2.4 table; correction to `Wheelchair` is reflected. |

## 7. ServiceNameEnumeration inconsistency

### PDF observation

The V2.4 version history says V2.2 removed `SystemDocumentationService` and `SystemManagementService` and added `SystemMonitoringService`.

However, the V2.4 ServiceNameEnumeration table still lists:

```text
SystemDocumentationService
SystemManagementService
SystemMonitoringService
```

### XSD observation

Observed in `IBIS-IP_Enumerations_V2.4.xsd`:

```xml
<xs:enumeration value="SystemMonitoringService"/>
```

and no `SystemDocumentationService` / `SystemManagementService` entries were present in the checked ServiceNameEnumeration snippet.

### Result

| Check | Result | Notes |
|---|---|---|
| `SystemMonitoringService` present | OK | Present in XSD. |
| `SystemDocumentationService` / `SystemManagementService` absent from XSD | PDF/XSD discrepancy with version-history support | The XSD follows the version-history statement, but not the still-visible V2.4 enumeration table. Treat as documentation/table inconsistency, not as an immediate XSD defect. |

Finding ID: `CE-004`.

## 8. Current closure state for Common/Enums V2.4 changed areas

| Area | Status |
|---|---|
| LineInformation V2.4 additions | OK, except previous-version rename diff still pending |
| StopInformation V2.4 additions | OK with `PointNumber` note |
| StopInformationRequest | OK by table; no V2.4 stop-global-ID fields expected there |
| TripInformation `BlockNumber` | OK |
| DoorCountingObjectClassEnumeration | OK |
| ServiceNameEnumeration | Discrepancy noted, likely PDF table/history inconsistency |

## 9. Remaining work before closing Common/Enums V2.4

```text
- Compare LineSymbolCode/LineSymbolText against V2.3 source to close the rename item.
- Target-check AdditionalTextMessage(n) in V2.4 common XSD.
- Full enumeration table pass for all V2.4 enumerations, not only the V2.4-changed one.
- Full Common datatype pass for V2.4, including InternationalTextType and NetexMode.
- Decide how to mark the ServiceNameEnumeration discrepancy in tool output.
```