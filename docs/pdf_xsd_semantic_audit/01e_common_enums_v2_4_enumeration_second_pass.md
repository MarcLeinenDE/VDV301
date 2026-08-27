# Common structures / enumerations V2.4 - enumeration second pass

Status: started, partial.

This file continues `01d_common_enums_v2_4_enumeration_first_pass.md` and focuses on the remaining V2.4 enumeration tables.

Scope in this pass:

```text
GNSSTypeEnumeration
ServiceNameEnumeration
ServiceStateEnumeration
SystemDocumentationInformationEnumeration
TicketRazziaInformationEnumeration
TicketValidationEnumeration
VehicleModeEnumeration
TripStateEnumeration
PtSubModesEnumeration
PrivateSubModesEnumeration
RailSubmodeEnumeration
CoachSubmodeEnumeration
MetroSubmodeEnumeration
BusSubmodeEnumeration
TramSubmodeEnumeration
WaterSubmodeEnumeration
AirSubmodeEnumeration
TelecabinSubmodeEnumeration
FunicularSubmodeEnumeration
TaxiSubmodeEnumeration
SelfDriveSubmodeEnumeration
```

The comparison is intentionally conservative: this pass records observed parity and observed differences, but does not change XSD files.

## 1. Confirmed or likely OK in this second pass

### ServiceStateEnumeration

PDF V2.4 table 86 lists:

```text
defective
notrunning
running
starting
standby
```

XSD V2.4 contains the same value set. Ordering is not relevant for XML enumeration validity.

Status: OK.

### SystemDocumentationInformationEnumeration

PDF V2.4 table 87 lists:

```text
ErrorMessage
StatusMessage
WarningMessage
All
```

XSD V2.4 contains the same value set.

Status: OK.

### TicketRazziaInformationEnumeration

PDF V2.4 table 88 lists:

```text
razzia
norazzia
```

XSD V2.4 contains both as `xs:enumeration` values and also still contains matching `xs:pattern` facets.

Status: OK with note.

Note: the simultaneous use of `xs:pattern` and `xs:enumeration` is redundant but not inherently contradictory because both patterns match the same values.

### TripStateEnumeration

PDF V2.4 table 91 lists:

```text
EmptyRun
OnTrip
OffTrip
TripBreak
OffDuty
unknown
```

XSD V2.4 contains the same value set.

Status: OK.

### PtSubModesEnumeration and PrivateSubModesEnumeration

PDF V2.4 tables 92 and 93 list the top-level mode selector values:

```text
PtSubModesEnumeration:
unknown, undefined, AirSubmode, BusSubmode, CoachSubmode, FunicularSubmode,
MetroSubmode, TramSubmode, TelecabinSubmode, RailSubmode, WaterSubmode

PrivateSubModesEnumeration:
unknown, undefined, SelfDriveSubmode, TaxiSubmode
```

XSD V2.4 contains the same value sets and the `PtSubmodeChoiceGroup` / `PrivateSubmodeChoiceGroup` reference the corresponding submode elements.

Status: OK.

### Standard submode enumerations: rail, coach, metro, bus, tram, water, air, telecabin, self-drive

Initial value parity check against PDF tables 94, 95, 96, 97, 98, 99, 100, 101 and 104 did not reveal a semantic mismatch in the first sweep.

Status: OK, pending full automated extraction.

Reason for keeping it open:

```text
These tables contain many values. The manual sweep is enough to classify them as promising,
but a final audit should generate XSD value lists and compare them mechanically against
extracted PDF value lists.
```

## 2. Confirmed differences / findings

### GNSSTypeEnumeration

PDF V2.4 table 79 lists:

```text
GPS
Glonass
Galileo
Beidou
IRNSS
Other
DeadReckoning
MixedGNSSTypes
```

XSD V2.4 contains the same semantic values, but the value for Other is lower-case:

```xml
<xs:enumeration value="other"/>
```

Status: discrepancy, tracked under `CE-007`.

Impact:

```text
XML enumeration values are case-sensitive. `Other` and `other` are not equivalent for validation.
```

### TicketValidationEnumeration

PDF V2.4 table 89 lists:

```text
Valid
notvalid
NoCard
```

XSD V2.4 contains:

```xml
<xs:enumeration value="valid"/>
<xs:enumeration value="notvalid"/>
<xs:enumeration value="NoCard"/>
```

Status: discrepancy, tracked under `CE-007`.

Impact:

```text
The PDF value `Valid` would not validate against an XSD that only permits `valid`.
```

### VehicleModeEnumeration

PDF V2.4 table 90 lists:

```text
Air
bus
coach
ferry
metro
rail
tram
underground
```

XSD V2.4 contains:

```xml
<xs:enumeration value="air"/>
<xs:enumeration value="bus"/>
<xs:enumeration value="coach"/>
<xs:enumeration value="ferry"/>
<xs:enumeration value="metro"/>
<xs:enumeration value="rail"/>
<xs:enumeration value="tram"/>
<xs:enumeration value="underground"/>
```

Status: discrepancy, tracked under `CE-007`.

Impact:

```text
The PDF value `Air` would not validate against an XSD that only permits `air`.
```

### FunicularSubmodeEnumeration

PDF V2.4 table 102 lists:

```text
Unknown
funicular
streetCableCar
allFunicularServices
undefinedFunicular
```

XSD V2.4 contains:

```xml
<xs:enumeration value="unknown"/>
<xs:enumeration value="funicular"/>
<xs:enumeration value="streetCableCar"/>
<xs:enumeration value="allFunicularServices"/>
<xs:enumeration value="undefinedFunicular"/>
```

Status: discrepancy candidate, tracked under `CE-008`.

Impact:

```text
The PDF value `Unknown` would not validate against an XSD that only permits `unknown`.
```

### TaxiSubmodeEnumeration

PDF V2.4 table 103 lists:

```text
Unknown
Undefined
communalTaxi
charterTaxi
waterTaxi
railTaxi
bikeTaxi
blackCab
minicab
allTaxiServices
```

XSD V2.4 contains:

```xml
<xs:enumeration value="unknown"/>
<xs:enumeration value="undefined"/>
...
<xs:enumeration value="miniCab"/>
<xs:enumeration value="allTaxiServices"/>
```

Status: discrepancy candidate, tracked under `CE-008`.

Observed differences:

```text
PDF Unknown    vs XSD unknown
PDF Undefined  vs XSD undefined
PDF minicab    vs XSD miniCab
```

Impact:

```text
All three are case-sensitive differences.
```

## 3. Interpretation rules for this pass

This audit does not assume that the PDF table is always correct or that the XSD is always correct.

Working interpretation:

```text
- If the XSD and version history agree but a table differs, mark as likely documentation/table inconsistency.
- If the PDF table and version history agree against the XSD, mark as stronger schema-mismatch candidate.
- If only capitalization differs, mark as case-sensitive discrepancy and defer correction until historical usage is checked.
```

## 4. New findings from this pass

### CE-008 - Submode enumeration case mismatches

State: discrepancy candidate.

Affected values observed so far:

```text
FunicularSubmodeEnumeration:
PDF Unknown vs XSD unknown

TaxiSubmodeEnumeration:
PDF Unknown / Undefined / minicab
vs XSD unknown / undefined / miniCab
```

This may be a PDF table capitalization issue because many other submode tables consistently use lower-case `unknown` and `undefined`. However, the mismatch is still relevant for tool documentation because XML validation follows the XSD values exactly.

## 5. Next step

Next audit step:

```text
Automated or scripted extraction of all V2.4 enumeration values from IBIS-IP_Enumerations_V2.4.xsd,
then manual PDF-list normalization check for tables 65-104.
```

Purpose:

```text
Close the enumeration sweep with a complete machine-generated XSD value inventory.
```
