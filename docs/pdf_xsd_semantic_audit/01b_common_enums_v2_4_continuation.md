# Common structures / enumerations V2.4 - continuation checks

Status: started, partial.

This file continues the V2.4 table-level audit after `01a_common_enums_v2_4_table_check.md`.

Scope in this continuation:

```text
InternationalTextType
IBIS-IP primitive wrapper datatypes
NetexMode
TripInformation AdditionalTextMessage / AdditionalTextMessage(n)
ServiceNameEnumeration follow-up
```

## 1. InternationalTextType

### PDF expectation

`VDV-Schrift 301-2-1 V2.4` table 17 describes `InternationalTextType` as:

```text
Value    1:1 IBIS-IP.string
Language 1:1 IBIS-IP.language
ErrorCode 0:1 ErrorCodeEnumeration
```

The same section also defines inline-formatting behaviour for the content of `Value`.

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:complexType name="InternationalTextType">
  <xs:sequence>
    <xs:element name="Value" type="IBIS-IP.string"/>
    <xs:element name="Language" type="IBIS-IP.language"/>
    <xs:element name="ErrorCode" type="ErrorCodeEnumeration" minOccurs="0"/>
  </xs:sequence>
</xs:complexType>
```

### Finding

| Item | Status | Notes |
|---|---|---|
| `Value` type/cardinality | OK | 1:1 by default, type `IBIS-IP.string`. |
| `Language` type/cardinality | OK | 1:1 by default, type `IBIS-IP.language`. |
| `ErrorCode` cardinality | OK | optional `0:1`. |
| inline formatting | documentation-level | XSD cannot enforce the permitted inline tags because `Value` is wrapped as `IBIS-IP.string`; tool documentation should keep the PDF behaviour separately. |

## 2. Primitive IBIS-IP wrapper datatypes

### PDF expectation

The V2.4 PDF describes the primitive wrapper datatypes from `IBIS-IP.anyURI` through `IBIS-IP.unsignedLong` with a common pattern:

```text
Value     1:1 underlying xs:* type
ErrorCode 0:1 ErrorCodeEnumeration
```

### XSD audit status

| Datatype | Status | Notes |
|---|---|---|
| `IBIS-IP.anyURI` | OK, sampled | `Value` uses `xs:anyURI`, `ErrorCode` optional. |
| `IBIS-IP.boolean` | OK, sampled | `Value` uses `xs:boolean`, `ErrorCode` optional. |
| `IBIS-IP.int` | OK, sampled | `Value` uses `xs:int`, `ErrorCode` optional. |
| `IBIS-IP.language` | OK, sampled | `Value` uses `xs:language`, `ErrorCode` optional. |
| `IBIS-IP.NMTOKEN` | OK, sampled | `Value` uses `xs:NMTOKEN`, `ErrorCode` optional. |
| remaining wrapper datatypes | pending | Need automated extraction or full manual sweep before closing. |

### Finding

No semantic issue found in the sampled wrapper datatypes. A full automated extraction from XSD is still recommended before closing the datatype section.

## 3. NetexMode

### PDF expectation

The V2.4 PDF describes `NetexMode` as a combined mode/submode structure with:

```text
PtMainMode / PrivateMainMode choice
PtSubModeChoiceGroup
PrivateSubModeChoiceGroup
```

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:choice minOccurs="0">
  <xs:element name="PtMainMode" type="PtSubModesEnumeration" minOccurs="0"/>
  <xs:element name="PrivateMainMode" type="PrivateSubModesEnumeration" minOccurs="0"/>
</xs:choice>
<xs:choice minOccurs="0">
  <xs:group ref="PtSubmodeChoiceGroup" minOccurs="0"/>
  <xs:group ref="PrivateSubmodeChoiceGroup" minOccurs="0"/>
</xs:choice>
```

### Finding

| Item | Status | Notes |
|---|---|---|
| Main-mode choice structure | OK, partial | Present in XSD. |
| Submode choice structure | OK, partial | Present in XSD. |
| Full submode enumeration value parity | pending | Needs enumeration-by-enumeration comparison for PtSubModes, PrivateSubModes and all submode enumerations. |

## 4. TripInformation AdditionalTextMessage / AdditionalTextMessage(n)

### PDF expectation

The V2.4 table for `TripInformation` states:

```text
AdditionalTextMessage     0:* +InternationalTextType
AdditionalTextMessage(n)  0:* +InternationalTextType, n = 1 to 9
```

The version history also records that `AdditionalTextMessage` was changed to `maxOccurs="unbounded"` in an earlier version.

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:element name="AdditionalTextMessage" type="InternationalTextType" minOccurs="0"/>
<xs:element name="AdditionalTextMessage1" type="InternationalTextType" minOccurs="0"/>
<xs:element name="AdditionalTextMessage2" type="InternationalTextType" minOccurs="0"/>
<xs:element name="AdditionalTextMessage3" type="InternationalTextType" minOccurs="0"/>
<xs:element name="AdditionalTextMessage4" type="InternationalTextType" minOccurs="0"/>
<xs:element name="AdditionalTextMessage5" type="InternationalTextType" minOccurs="0"/>
<xs:element name="AdditionalTextMessage6" type="InternationalTextType" minOccurs="0"/>
<xs:element name="AdditionalTextMessage7" type="InternationalTextType" minOccurs="0"/>
<xs:element name="AdditionalTextMessage8" type="InternationalTextType" minOccurs="0"/>
<xs:element name="AdditionalTextMessage9" type="InternationalTextType" minOccurs="0"/>
```

There is no `maxOccurs` on these elements, so XML Schema default is `1`.

### Finding

| Item | Status | Notes |
|---|---|---|
| Element names | OK | Base plus `1..9` variants are present. |
| Element types | OK | All use `InternationalTextType`. |
| Cardinality | discrepancy | PDF says `0:*`; XSD currently allows at most one of each named element. |

This is tracked as finding `CE-005`.

Practical interpretation:

```text
The XSD permits at most one `AdditionalTextMessage`, one `AdditionalTextMessage1`, ..., one `AdditionalTextMessage9`.
The PDF table appears to allow multiple values for each of those fields.
Because `InternationalTextType` already carries one `Language`, the difference may matter for multilingual or repeated passenger text messages.
```

Do not change the XSD automatically. This needs confirmation against earlier XSD versions, examples and VDV intent.

## 5. ServiceNameEnumeration follow-up

`CE-004` remains open. The current XSD ServiceNameEnumeration contains `SystemMonitoringService` and current service names such as `AnalogRadioService`, `HTMLDisplayService`, `TicketValidationService`, `TimeService`, TrainSet services and Video services.

The discrepancy is not about whether `SystemMonitoringService` is present; it is about whether the removed older `SystemDocumentationService` and `SystemManagementService` should still appear because the PDF table still shows them while the version history says they were removed.

## 6. Status after this continuation

| Area | Status |
|---|---|
| V2.4 changed Line/Stop/Trip fields | mostly OK, with notes |
| InternationalTextType | OK |
| Primitive wrappers | OK sampled, full sweep pending |
| NetexMode | OK partial, full enumeration sweep pending |
| AdditionalTextMessage cardinality | discrepancy `CE-005` |
| ServiceNameEnumeration | discrepancy/note `CE-004` |

Next audit step:

```text
Complete enumeration-by-enumeration V2.4 value parity for:
DeviceClassEnumeration
ErrorCodeEnumeration
ServiceNameEnumeration
TripStateEnumeration
PtSubModesEnumeration
PrivateSubModesEnumeration
Rail/Coach/Metro/Bus/Tram/Water/Air/Telecabin/Funicular/Taxi/SelfDrive submode enumerations
```
