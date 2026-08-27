# Common structures / enumerations V2.4 - datatype and core-structure audit

Status: datatype/core structure block advanced; wrapper datatypes closed for first PDF/XSD pass.

Scope of this block:

```text
VDV 301-2-1 V2.4 chapter 1:
- IBIS-IP wrapper datatypes 1.1-1.16
- InternationalTextType 1.17
- NetexMode 1.18

This file continues after the completed first exact enumeration diff in 01f.
```

Important authority rule:

```text
Validation authority is XSD.
PDF is recorded as documentation evidence and for provider-facing explanation.
If PDF and XSD disagree, validation follows XSD and the discrepancy is tracked.
```

See also:

```text
docs/pdf_xsd_semantic_audit/VALIDATION_AUTHORITY.md
```

## 1. IBIS-IP wrapper datatype pattern

### PDF expectation

The V2.4 Common Structures / Enumerations PDF describes primitive IBIS-IP wrapper datatypes with the common pattern:

```text
Value     1:1 underlying XML Schema primitive type
ErrorCode 0:1 ErrorCodeEnumeration
```

The wrapper datatype set in the V2.4 XSD contains 16 primitive wrappers.

### XSD observation

Observed in `IBIS-IP_common_V2.4.xsd`:

```text
IBIS-IP.anyURI             -> xs:anyURI
IBIS-IP.boolean            -> xs:boolean
IBIS-IP.byte               -> xs:byte
IBIS-IP.date               -> xs:date
IBIS-IP.dateTime           -> xs:dateTime
IBIS-IP.double             -> xs:double
IBIS-IP.duration           -> xs:duration
IBIS-IP.int                -> xs:int
IBIS-IP.language           -> xs:language
IBIS-IP.NMTOKEN            -> xs:NMTOKEN
IBIS-IP.nonNegativeInteger -> xs:nonNegativeInteger
IBIS-IP.normalizedString   -> xs:normalizedString
IBIS-IP.string             -> xs:string
IBIS-IP.time               -> xs:time
IBIS-IP.unsignedInt        -> xs:unsignedInt
IBIS-IP.unsignedLong       -> xs:unsignedLong
```

Each observed wrapper has this structure:

```xml
<xs:element name="Value" type="xs:*"/>
<xs:element name="ErrorCode" type="ErrorCodeEnumeration" minOccurs="0"/>
```

Machine-readable inventory:

```text
docs/pdf_xsd_semantic_audit/generated/common_v2_4_datatypes_xsd_inventory.csv
```

Human-readable inventory:

```text
docs/pdf_xsd_semantic_audit/generated/common_v2_4_datatypes_xsd_inventory.md
```

### Finding

| Item | Status | Notes |
|---|---|---|
| Wrapper datatype structure | OK | All 16 observed V2.4 wrapper types follow the PDF-described pattern. |
| `Value` cardinality | OK | Required by XSD default `1:1`. |
| `ErrorCode` cardinality | OK | Optional `0:1` through `minOccurs="0"`. |
| Validation authority | XSD | Primitive-type constraints are technically enforced by XSD. |

No new CE finding opened in this subsection.

## 2. InternationalTextType

### PDF expectation

The V2.4 PDF describes `InternationalTextType` with:

```text
Value     1:1 IBIS-IP.string
Language  1:1 IBIS-IP.language
ErrorCode 0:1 ErrorCodeEnumeration
```

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
| `Value` | OK | Required by XSD default occurrence, type `IBIS-IP.string`. |
| `Language` | OK | Required by XSD default occurrence, type `IBIS-IP.language`. |
| `ErrorCode` | OK | Optional. |
| inline formatting | documentation-level | PDF describes inline formatting behaviour, but XSD cannot fully enforce allowed markup while `Value` is represented through `IBIS-IP.string`. |

No new CE finding opened in this subsection.

Tool interpretation:

```text
InternationalTextType validates according to the XSD sequence.
Provider-facing notes may additionally explain PDF inline-formatting expectations, but those are not fully XSD-enforced.
```

## 3. NetexMode

### PDF expectation

The PDF describes `NetexMode` as a combined main-mode/submode structure using:

```text
PtMainMode or PrivateMainMode
PtSubmodeChoiceGroup or PrivateSubmodeChoiceGroup
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

The related submode enumeration values were handled in the V2.4 enumeration inventory and exact PDF/XSD diff.

### Finding

| Item | Status | Notes |
|---|---|---|
| Main-mode choice structure | OK, partial | XSD has PT/private main-mode choice. |
| Submode choice structure | OK, partial | XSD has PT/private submode group choice. |
| Submode value parity | completed first pass in 01f | Differences are tracked as CE-008, CE-009 and CE-010. |
| Validation authority | XSD | If a PDF-listed submode value differs from the XSD value, validation follows XSD and the PDF discrepancy is reported. |

No new CE finding opened in this subsection; existing Netex/submode findings remain open for historical classification.

## 4. Subscribe / response core structures observed in the same XSD block

The same XSD slice also confirms these core response/request structures:

| Structure | XSD observation | Audit note |
|---|---|---|
| `SubscribeRequestStructure` | `Client-IP-Address` required, `ReplyPort` optional, `ReplyPath` optional | Needs PDF table confirmation before closure. |
| `SubscribeResponseStructure` | `Active`, `Heartbeat`, `OperationErrorMessage` all optional | XSD documentation notes compatibility reasons and that meaningful data should include at least one member; this is not enforced by XSD. |
| `UnsubscribeRequestStructure` | same addressing pattern as subscribe request | Needs PDF table confirmation before closure. |
| `UnsubscribeResponseStructure` | `Active` required, `OperationErrorMessage` optional | Needs PDF table confirmation before closure. |
| `DataAcceptedResponseStructure` | choice between response data and operation error message | Needs PDF table confirmation before closure. |
| `DataAcceptedResponseDataStructure` | `TimeStamp`, `DataAccepted` required; `ErrorCode`, `ErrorInformation` optional | Needs PDF table confirmation before closure. |

No CE finding is opened here yet because this subsection records XSD observations first. The PDF table-level closure for these structures belongs to the common data structures follow-up block.

## 5. Tool message examples for this section

Case-sensitive enum mismatch example:

```text
FAIL: `Air` is not allowed by the XSD for VehicleModeEnumeration.
Allowed according to XSD: `air`.
PDF note: The V2.4 PDF table lists `Air`; this audit tracks the difference as CE-007. According to VDV 301-2 V2.4 General Conventions, the XSD definition has precedence in case of inconsistency.
```

PDF-only service-name example:

```text
FAIL: `SystemManagementService` is not allowed by the XSD ServiceNameEnumeration.
PDF note: The V2.4 PDF table still lists `SystemManagementService`, but the V2.4 version history says this older service name was removed and the XSD omits it. Validation follows XSD. Finding: CE-004.
```

Wrapper datatype example:

```text
FAIL: `abc` is not valid for `IBIS-IP.int/Value` because the XSD maps that wrapper to `xs:int`.
PDF note: The PDF documents the wrapper concept, but actual type validation follows the XSD primitive type.
```

## 6. Result of this block

```text
- Validation-authority rule is explicitly applied to Common/Enums V2.4 datatype/core-structure checks.
- All 16 observed IBIS-IP wrapper datatypes in V2.4 follow the expected Value + optional ErrorCode pattern.
- InternationalTextType remains OK.
- NetexMode structure remains OK partial; value-level differences are already captured in the enumeration diff.
- Subscribe/DataAccepted core structures have first XSD observation notes and await PDF table-level closure.
```

Next audit block:

```text
Common data structures 2.1-2.64, starting with the structures most affected by V2.4 and already touched by previous findings:
LineInformation
StopInformation
TripInformation
DisplayContent
Connection
DeviceInformation / DeviceSpecification family
```
