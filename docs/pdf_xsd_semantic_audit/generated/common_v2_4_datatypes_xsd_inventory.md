# XSD datatype inventory - IBIS-IP_common_V2.4

Status: generated audit inventory, manual extraction from `IBIS-IP_common_V2.4.xsd` lines covering the IBIS-IP wrapper datatype block.

Source XSD:

```text
IBIS-IP_common_V2.4.xsd
```

Machine-readable inventory:

```text
docs/pdf_xsd_semantic_audit/generated/common_v2_4_datatypes_xsd_inventory.csv
```

## Inventory

| XSD type | Value type | ErrorCode | Status |
|---|---|---|---|
| `IBIS-IP.anyURI` | `xs:anyURI` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.boolean` | `xs:boolean` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.byte` | `xs:byte` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.date` | `xs:date` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.dateTime` | `xs:dateTime` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.double` | `xs:double` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.duration` | `xs:duration` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.int` | `xs:int` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.language` | `xs:language` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.NMTOKEN` | `xs:NMTOKEN` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.nonNegativeInteger` | `xs:nonNegativeInteger` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.normalizedString` | `xs:normalizedString` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.string` | `xs:string` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.time` | `xs:time` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.unsignedInt` | `xs:unsignedInt` | `0:1 ErrorCodeEnumeration` | OK |
| `IBIS-IP.unsignedLong` | `xs:unsignedLong` | `0:1 ErrorCodeEnumeration` | OK |

## Result

All 16 V2.4 IBIS-IP primitive wrapper datatypes observed in the XSD follow the expected pattern:

```text
Value     1:1 corresponding xs:* primitive type
ErrorCode 0:1 ErrorCodeEnumeration
```

No new CE finding is opened for the wrapper datatype block.

## Tool interpretation

Validation follows the XSD primitive type and the optional ErrorCode structure. If a payload uses a value that violates the underlying XML Schema primitive type, the technical result is a validation fail regardless of any broader PDF wording.
