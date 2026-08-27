# Common structures / enumerations V2.4 - PDF vs XSD enumeration diff

Status: completed first exact pass for VDV 301-2-1 V2.4 tables 65-104.

Scope:

```text
PDF side: VDV-Schrift 301-2-1 V2.4, chapter 3, tables 65-104
XSD side: IBIS-IP_Enumerations_V2.4.xsd in dev/schema-integration
```

Input inventories:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv
```

Machine-readable diff:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_vs_xsd_diff.csv
```

Important rule:

```text
Enumeration values are compared exactly and case-sensitively.
Value order differences are not classified as semantic mismatches because XML Schema enumeration order does not change validation behaviour.
```

## Summary

| Classification | Count | Meaning |
|---|---:|---|
| `only_in_pdf` | 2 | PDF table lists value not present in XSD inventory. |
| `only_in_xsd` | 2 | XSD permits value not listed in PDF table. |
| `case_difference` | 7 | Same spelling except case; not equivalent for XML validation. |
| `case_or_spelling_difference` | 1 | Non-identical value names that appear to represent the same conceptual entry. |

No mismatch was observed in the remaining enumeration values of tables 65-104 after normalising only for ordering.

## Exact differences

| Simple type | Classification | PDF value | XSD value | Finding |
|---|---|---|---|---|
| `DeviceStateEnumeration` | `only_in_xsd` | | `warning` | CE-006 |
| `GNSSTypeEnumeration` | `case_difference` | `Other` | `other` | CE-007 |
| `ServiceNameEnumeration` | `only_in_pdf` | `SystemDocumentationService` | | CE-004 |
| `ServiceNameEnumeration` | `only_in_pdf` | `SystemManagementService` | | CE-004 |
| `TicketValidationEnumeration` | `case_difference` | `Valid` | `valid` | CE-007 |
| `VehicleModeEnumeration` | `case_difference` | `Air` | `air` | CE-007 |
| `RailSubmodeEnumeration` | `case_or_spelling_difference` | `specialRail` | `specialTrain` | CE-009 |
| `AirSubmodeEnumeration` | `only_in_xsd` | | `canalBarge` | CE-010 |
| `FunicularSubmodeEnumeration` | `case_difference` | `Unknown` | `unknown` | CE-008 |
| `TaxiSubmodeEnumeration` | `case_difference` | `Unknown` | `unknown` | CE-008 |
| `TaxiSubmodeEnumeration` | `case_difference` | `Undefined` | `undefined` | CE-008 |
| `TaxiSubmodeEnumeration` | `case_difference` | `minicab` | `miniCab` | CE-008 |

## Notes by finding

### CE-004 - ServiceNameEnumeration older service names

The V2.4 PDF table still lists `SystemDocumentationService` and `SystemManagementService`, but the V2.4 XSD inventory does not. This matches the earlier version-history note that these service names were removed and `SystemMonitoringService` was added.

Interpretation remains unchanged: likely documentation/table inconsistency, not an immediate XSD defect.

### CE-006 - DeviceState warning

`warning` is XSD-only in the V2.4 enumeration table comparison.

Do not remove it automatically. Historical usage and previous schema versions need checking first.

### CE-007 - Common case differences

The following PDF values do not validate against the XSD values if used exactly as printed:

```text
PDF Other vs XSD other
PDF Valid vs XSD valid
PDF Air vs XSD air
```

For actual validation, the tool must follow the XSD.

### CE-008 - Submode case/spelling differences

The following values are case-sensitive PDF/XSD differences:

```text
PDF Unknown vs XSD unknown
PDF Undefined vs XSD undefined
PDF minicab vs XSD miniCab
```

These affect FunicularSubmodeEnumeration and TaxiSubmodeEnumeration.

### CE-009 - RailSubmode specialRail vs specialTrain

`RailSubmodeEnumeration` has one non-case-only naming mismatch:

```text
PDF: specialRail
XSD: specialTrain
```

This needs historical checking before any correction is proposed. It may be a PDF typo, an XSD typo, or a renamed value from an external TPEG/NeTEx source.

### CE-010 - AirSubmode canalBarge XSD-only value

`AirSubmodeEnumeration` contains one XSD-only value:

```text
canalBarge
```

The XSD itself annotates this value as not in TPEG. It is not listed in the V2.4 PDF AirSubmodeEnumeration table. Treat as an explicit schema/documentation divergence until checked historically.

## Result of this block

The V2.4 enumeration value comparison is now reproducible at inventory/diff level.

Next recommended audit step:

```text
Start the full Common Structures V2.4 table-level structure comparison:
IBIS-IP datatypes, InternationalTextType, NetexMode and common structures 2.1-2.64.
```

Alternative if we want to close findings first:

```text
Check CE-006, CE-009 and CE-010 against older Common/Enums PDFs/XSDs and external TPEG/NeTEx references.
```

Do not modify `IBIS-IP_Enumerations_V2.4.xsd` during this audit step.
