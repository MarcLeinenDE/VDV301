# Common/Enums V2.3 -> V2.4 history and closure

Status: XSD-side dependency/value/structure diff and PDF-side first-pass closure completed; CE-010 historical range corrected during Common V2.3 Deep Read on 2026-08-28.

Scope:

```text
IBIS-IP_common_V2.3.xsd
IBIS-IP_Enumerations_V2.2.xsd as V2.3 dependency pool
IBIS-IP_common_V2.4.xsd
IBIS-IP_Enumerations_V2.4.xsd
VDV 301-2-1 Common Data Structures and Enumerations V2.4 PDF source
```

Authority rule:

```text
Validation follows the selected version's XSD family.
PDF differences are retained as provider-facing explanation notes.
No schema change is made during this audit pass.
```

Mixed-version rule:

```text
Do not apply V2.4 Common/Enums definitions to a V2.3 service payload unless the selected service/dependency pool actually uses V2.4.
V2.3 and V2.4 must stay separately validatable.
```

## 1. XSD dependency family observation

### Common/Enums V2.3

Observed:

```text
IBIS-IP_common_V2.3.xsd includes IBIS-IP_Enumerations_V2.2.xsd.
No IBIS-IP_Enumerations_V2.3.xsd is observed.
```

The exact official Enumerations V2.2 blob used for the V2.3 pool is:

```text
2a23b512379b18e8f122ac1272cef8229fb86283
```

### Common/Enums V2.4

Observed:

```text
IBIS-IP_common_V2.4.xsd includes IBIS-IP_Enumerations_V2.4.xsd.
```

Result:

```text
V2.4 returns to a matching Common/Enumerations version family.
This does not make V2.3 defective; it defines a distinct exact dependency pool.
```

## 2. Generated XSD-side closure files

Generated audit files:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_3_vs_v2_4_xsd_diff.csv
docs/pdf_xsd_semantic_audit/generated/common_v2_3_vs_v2_4_structure_delta.csv
```

Corrected enumeration result:

```text
V2.3 uses the V2.2 enumeration pool.
V2.4 uses Enumerations V2.4.

Confirmed V2.3 -> V2.4 enumeration deltas include:
  DoorCountingObjectClass WheelChair -> Wheelchair
  ServiceNameEnumeration adds AnalogRadioService

canalBarge is NOT a V2.4 addition.
It is already present in the exact official VDV-301-2.2 Enumerations V2.2 blob
and therefore is already part of the Common V2.3 dependency pool.
```

The prior generated diff row that called `canalBarge` a V2.4 addition was stale and is corrected together with this file.

Structure result:

```text
V2.4 contains targeted common-structure additions in LineInformation, StopInformation and TripInformation.
V2.4 corrects BeaconPoint Desciption -> Description.
TSPPoint still uses Desciption.
```

## 3. V2.4 PDF-side first pass

The V2.4 PDF identifies itself as:

```text
VDV-Schrift 301-2-1
01/2023
Common Data Structures and Enumerations
V2.4
```

Relevant V2.4 structure direction:

```text
LineInformation additions:
  LinePublicCode
  LineSymbolText
  ExternalLineRef

StopInformation additions:
  StopShortName
  StopLongNo
  PointNumber
  StopGlobalID
  StopPointGlobalID

TripInformation additions:
  BlockNumber
  ExternalVehicleJourneyRef

Enumeration/service changes:
  DoorCountingObjectClass Wheelchair spelling
  AnalogRadioService in ServiceNameEnumeration
```

## 4. XSD observations for V2.4

Observed:

```text
IBIS-IP_common_V2.4.xsd includes IBIS-IP_Enumerations_V2.4.xsd.
IBIS-IP_Enumerations_V2.4.xsd contains AnalogRadioService.
IBIS-IP_Enumerations_V2.4.xsd contains DoorCountingObjectClassEnumeration value Wheelchair.
IBIS-IP_Enumerations_V2.4.xsd contains AirSubmodeEnumeration value canalBarge.
```

Historical correction:

```text
The presence of canalBarge in V2.4 is not a version delta.
The same value already exists in official Enumerations V2.2.
CE-010 is therefore a PDF-vs-XSD omission whose confirmed XSD history begins at least with V2.2.
```

Observed V2.4 structure facts:

```text
BeaconPointStructure uses Description.
TSPPointStructure still uses Desciption.
ZoneType uses FarezoneTypeID and FareZoneTypeName mixed casing.
GlobalCardStatus uses GlobalCardStausID.
TripInformation AdditionalTextMessage remains non-repeatable at the base field, with AdditionalTextMessage1..9 as named optional fields.
```

## 5. Finding range consolidation

| Finding | Consolidated historical interpretation |
|---|---|
| CE-001 | OK with note: V2.3 intentionally uses Common V2.3 + Enumerations V2.2. Do not create a dummy Enumerations V2.3 file. |
| CE-002 | V2.4 history wording says StopPointNumber, but table/XSD use PointNumber. |
| CE-004 | Starts with V2.2: old SystemDocumentationService/SystemManagementService removed in history/XSD, but PDF tables still carry them through later docs. |
| CE-005 | Supported from V2.0 through V2.4: PDF/history expects AdditionalTextMessage repeatability; XSD bounds each named field. |
| CE-006 | Supported from V2.2 through V2.4: warning exists in XSD enumeration pool but is absent from the PDF table. |
| CE-007 | Case-sensitive differences such as Valid/valid, Air/air and Other/other. |
| CE-008 | Supported from the V2.2 NetexMode/submode introduction through V2.4 for checked submode case mismatches. |
| CE-009 | Supported from the V2.2 NetexMode/submode introduction through V2.4: PDF specialRail vs XSD specialTrain. |
| CE-010 | **Corrected range:** XSD-only `canalBarge` is already present in official Enumerations V2.2, hence affects the V2.3 dependency pool and V2.4; it was not introduced in V2.4. |
| CE-011 | Supported from V2.2 through V2.4: Connection TransportMode/ConnectionMode PDF 0:* vs XSD 0:1. |
| CE-012 | Supported through checked Common/Enums structure versions. |
| CE-013 | PDF uses InformationAtSpecificPoint wording; XSD uses SpecificPoint in an optional choice. |
| CE-014 | DataVersionList PDF 1:* vs XSD 0:*. |
| CE-015 | Native-text evidence now strengthens FareZone/Farezone and ZoneType casing differences; visual closure remains pending. |
| CE-016 | V2.3/V2.4 GlobalCardStausID typo-like XSD spelling remains authority. |
| CE-017 | V2.3/V2.4 TSPPoint Desciption remains XSD authority; native-text PDF says Description; visual closure pending. |

The subsequent fresh Common V2.3 Deep Read additionally opened CE-021..CE-026; see `COMMON_FINDINGS_REGISTER_ADDENDUM.md` and `deep_read/COMMON_V2.3.md`.

## 6. CE-001 closure decision

```text
CE-001 is OK with note.
Selected V2.3 pool:
  IBIS-IP_common_V2.3.xsd
  IBIS-IP_Enumerations_V2.2.xsd
```

Tool implication:

```text
When validating a V2.3 service using Common V2.3, load Enumerations V2.2 unless the audited service version explicitly points elsewhere.
Do not automatically substitute Enumerations V2.4.
```

## 7. Validation backlog impact

Exact pools:

```text
Common/Enums V2.3:
  IBIS-IP_common_V2.3.xsd
  IBIS-IP_Enumerations_V2.2.xsd

Common/Enums V2.4:
  IBIS-IP_common_V2.4.xsd
  IBIS-IP_Enumerations_V2.4.xsd
```

Targeted version-delta samples remain:

```text
V2.3 negative / V2.4 positive: LineInformation.LinePublicCode.
V2.3 negative / V2.4 positive: StopInformation.StopGlobalID.
V2.3 negative / V2.4 positive: TripInformation.BlockNumber.
V2.3 negative / V2.4 positive: ServiceNameEnumeration AnalogRadioService.
V2.3 positive / V2.4 negative: DoorCountingObjectClassEnumeration WheelChair.
V2.3 negative / V2.4 positive: DoorCountingObjectClassEnumeration Wheelchair.
V2.4 negative for PDF value: RailSubmodeEnumeration specialRail.
V2.4 positive for XSD value: RailSubmodeEnumeration specialTrain.
```

`canalBarge` must no longer be used as a V2.3-negative/V2.4-positive sample. It is valid in the exact V2.3 dependency pool because that pool uses official Enumerations V2.2, which already contains the value.

## 8. Result

```text
Common/Enums historical first-pass chain V1.0/V1.x -> V2.4 remains complete.
V2.3 and V2.4 dependency pools are explicitly distinct.
CE-001 remains closed as OK with note.
CE-010 historical range is corrected.
No XSD correction is proposed by this closure pass.
```

The Common V2.3 Deep Read supersedes the earlier assumption that `canalBarge` was introduced only with V2.4.
