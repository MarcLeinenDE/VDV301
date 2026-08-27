# Common structures / enumerations V2.4 - datatype and core-structure audit

Status: started, partial.

Scope of this block:

```text
VDV 301-2-1 V2.4 chapter 1:
- IBIS-IP wrapper datatypes
- InternationalTextType
- NetexMode

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

Examples in this datatype family include string-like, numeric, date/time and URI wrapper types.

### XSD observation

Previously sampled and observed in `IBIS-IP_common_V2.4.xsd`:

```text
IBIS-IP.anyURI
IBIS-IP.boolean
IBIS-IP.int
IBIS-IP.language
IBIS-IP.NMTOKEN
```

These sampled types follow the expected wrapper structure:

```text
Value element with the respective xs:* primitive type
optional ErrorCode element of type ErrorCodeEnumeration
```

### Finding

| Item | Status | Notes |
|---|---|---|
| Wrapper datatype structure | OK, sampled | Sampled XSD structures follow the PDF pattern. |
| Full wrapper sweep | pending | Should be completed with automated extraction or local parser before closing the entire datatype section. |
| Validation authority | XSD | If a payload passes/fails because of XSD wrapper type constraints, the XSD result is authoritative. |

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

Observed earlier in `IBIS-IP_common_V2.4.xsd`:

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

## 3. NetexMode

### PDF expectation

The PDF describes `NetexMode` as a combined main-mode/submode structure using:

```text
PtMainMode or PrivateMainMode
PtSubmodeChoiceGroup or PrivateSubmodeChoiceGroup
```

### XSD observation

Observed earlier in `IBIS-IP_common_V2.4.xsd`:

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

## 4. Tool message examples for this section

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

## 5. Result of this block

```text
- Validation-authority rule is now explicitly applied to Common/Enums V2.4 datatype/core-structure checks.
- Wrapper datatype sampling remains OK but needs a full automated/local sweep before final closure.
- InternationalTextType remains OK.
- NetexMode structure remains OK partial; value-level differences are already captured in the enumeration diff.
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
