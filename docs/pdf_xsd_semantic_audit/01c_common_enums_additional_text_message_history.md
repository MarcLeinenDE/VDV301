# Common structures - AdditionalTextMessage historical PDF/XSD trace

Status: focused finding trace for `CE-005`.

Scope:

```text
IBIS-IP_common_V1.0.xsd
IBIS-IP_common_V2.0.xsd
IBIS-IP_common_V2.1.xsd
IBIS-IP_common_V2.2.xsd
IBIS-IP_common_V2.3.xsd
IBIS-IP_common_V2.4.xsd
```

Purpose:

Track whether the `TripInformation/AdditionalTextMessage` cardinality discrepancy is a V2.4-only issue or inherited from earlier schema versions.

## 1. PDF baseline from V2.4 consolidated history

The V2.4 Common Structures / Enumerations PDF contains two relevant references:

```text
Version 1.1:
TripInformation: Type of AdditionalTextMessage changed from IBIS-IP.string to +InternationalTextType.

Version 2.0:
TripInformation structure: AdditionalTextMessage: maxOccurs="unbounded" updated.
```

The current V2.4 `TripInformation` table states:

```text
AdditionalTextMessage     0:* +InternationalTextType
AdditionalTextMessage(n)  0:* +InternationalTextType, n = 1 to 9
```

Interpretation used for this audit:

```text
The PDF lineage expects AdditionalTextMessage to be repeatable from V2.0 onward.
V2.3 additionally introduces numbered AdditionalTextMessage(n) variants.
```

## 2. XSD historical observations

### V1.0

Observed in `IBIS-IP_common_V1.0.xsd`:

```xml
<xs:element name="AdditionalTextMessage" type="IBIS-IP.string" minOccurs="0"/>
```

Assessment:

```text
Matches the pre-V1.1 type before the PDF-history change to InternationalTextType.
No maxOccurs is present, therefore cardinality is 0:1 in XSD.
```

### V2.0

Observed in `IBIS-IP_common_V2.0.xsd`:

```xml
<xs:element name="AdditionalTextMessage" type="InternationalTextType" minOccurs="0"/>
```

Assessment:

```text
Type is updated to InternationalTextType, but maxOccurs="unbounded" is not present.
This conflicts with the V2.0 PDF-history note saying maxOccurs="unbounded" was updated.
```

### V2.1

Observed in `IBIS-IP_common_V2.1.xsd`:

```xml
<xs:element name="AdditionalTextMessage" type="InternationalTextType" minOccurs="0"/>
```

Assessment:

```text
The V2.0 cardinality issue persists.
```

### V2.2

Observed in `IBIS-IP_common_V2.2.xsd`:

```xml
<xs:element name="AdditionalTextMessage" type="InternationalTextType" minOccurs="0"/>
```

Assessment:

```text
The V2.0 cardinality issue persists.
```

### V2.3

Observed in `IBIS-IP_common_V2.3.xsd`:

```xml
<xs:element name="AdditionalTextMessage" type="InternationalTextType" minOccurs="0"/>
<xs:element name="AdditionalTextMessage1" type="InternationalTextType" minOccurs="0"/>
...
<xs:element name="AdditionalTextMessage9" type="InternationalTextType" minOccurs="0"/>
```

Assessment:

```text
V2.3 adds the numbered AdditionalTextMessage(n) variants, but none of the base or numbered elements has maxOccurs="unbounded".
```

### V2.4

Observed in `IBIS-IP_common_V2.4.xsd`:

```xml
<xs:element name="AdditionalTextMessage" type="InternationalTextType" minOccurs="0"/>
<xs:element name="AdditionalTextMessage1" type="InternationalTextType" minOccurs="0"/>
...
<xs:element name="AdditionalTextMessage9" type="InternationalTextType" minOccurs="0"/>
```

Assessment:

```text
Same as V2.3. The PDF table says 0:* for base and numbered elements, while the XSD allows 0:1 for each named element.
```

## 3. Matrix

| Version | XSD type | Numbered variants | XSD maxOccurs | PDF/history expectation | Result |
|---|---|---:|---|---|---|
| V1.0 | `IBIS-IP.string` | no | implicit 1 | pre-V1.1 state | OK for type history; repeatability not expected from this source |
| V2.0 | `InternationalTextType` | no | implicit 1 | `maxOccurs="unbounded"` updated | mismatch |
| V2.1 | `InternationalTextType` | no | implicit 1 | inherited repeatability | mismatch |
| V2.2 | `InternationalTextType` | no | implicit 1 | inherited repeatability | mismatch |
| V2.3 | `InternationalTextType` | yes, 1..9 | implicit 1 each | AdditionalTextMessage(n) inserted; table lineage expects 0:* | mismatch |
| V2.4 | `InternationalTextType` | yes, 1..9 | implicit 1 each | table explicitly says 0:* for base and numbered variants | mismatch |

## 4. Finding update

`CE-005` is no longer a V2.4-only finding.

Updated interpretation:

```text
The XSD type change from IBIS-IP.string to InternationalTextType is reflected from V2.0 onward.
The PDF-documented maxOccurs="unbounded" change is not reflected in the XSD files V2.0 to V2.4.
The V2.3 numbered AdditionalTextMessage(n) extension is present, but also only as 0:1 per field in the XSD.
```

## 5. Recommended handling

Do not silently modify schemas in the integration branch yet.

Before changing any XSD:

```text
1. Check whether official examples rely on multiple repeated AdditionalTextMessage elements.
2. Check whether consumers historically interpreted the numbered fields as an alternative to repeated XML elements.
3. Check upstream/fork history for any PR or comment about this cardinality.
4. If corrected later, scope it as a separate schema-correction candidate, not mixed into the DMS V2.4 PR.
```

Tool impact until resolved:

```text
When validating against the current XSD pool, repeated AdditionalTextMessage elements will fail although the PDF table appears to allow them.
The VDV301 Tool should surface this as a known PDF/XSD discrepancy, not as a clear device/vendor error.
```
