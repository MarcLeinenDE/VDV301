# Common/Enums V2.3 -> V2.4 history and closure

Status: XSD-side dependency/value/structure diff and PDF-side first-pass closure completed.

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
No IBIS-IP_Enumerations_V2.3.xsd is observed in dev/schema-integration.
```

### Common/Enums V2.4

Observed:

```text
IBIS-IP_common_V2.4.xsd includes IBIS-IP_Enumerations_V2.4.xsd.
```

First-pass result:

```text
V2.4 returns to a matching common/enumeration version family.
This does not make V2.3 defective; it only defines a different dependency pool.
```

## 2. Generated XSD-side closure files

Created generated audit files:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_3_vs_v2_4_xsd_diff.csv
docs/pdf_xsd_semantic_audit/generated/common_v2_3_vs_v2_4_structure_delta.csv
```

Enumeration result:

```text
V2.3 uses the V2.2 enumeration pool.
V2.4 uses a separate V2.4 enumeration file.
Observed V2.4 enum deltas include Wheelchair spelling, AnalogRadioService and canalBarge.
```

Structure result:

```text
V2.4 contains targeted common-structure additions in LineInformation, StopInformation and TripInformation.
V2.4 also corrects BeaconPoint Desciption -> Description, while TSPPoint still uses Desciption.
```

## 3. V2.4 PDF-side first pass

The opened V2.4 PDF identifies itself as:

```text
VDV-Schrift 301-2-1
01/2023
Common Data Structures and Enumerations
V2.4
```

The V2.4 PDF/version-history side has already been checked in the preceding V2.4 audit files for the affected tables. For closure, the relevant V2.4 direction is:

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

Enumeration/service additions or corrections:
  DoorCountingObjectClass Wheelchair spelling
  AnalogRadioService in ServiceNameEnumeration
```

First-pass interpretation:

```text
The V2.4 common-structure additions are represented in the V2.4 XSD candidate/integration files.
The V2.4 enum-family change from inherited V2.2 enumerations to Enumerations V2.4 is meaningful and must be preserved by the later validator.
```

## 4. XSD observations for V2.4

Observed V2.4 XSD facts:

```text
IBIS-IP_common_V2.4.xsd includes IBIS-IP_Enumerations_V2.4.xsd.
IBIS-IP_Enumerations_V2.4.xsd contains AnalogRadioService.
IBIS-IP_Enumerations_V2.4.xsd contains DoorCountingObjectClassEnumeration value Wheelchair.
IBIS-IP_Enumerations_V2.4.xsd contains AirSubmodeEnumeration value canalBarge with an XSD note that it is not in TPEG.
```

Observed V2.4 structure facts:

```text
BeaconPointStructure uses Description.
TSPPointStructure still uses Desciption.
ZoneType still uses FarezoneTypeID and FareZoneTypeName mixed casing.
GlobalCardStatus still uses GlobalCardStausID.
TripInformation AdditionalTextMessage remains non-repeatable at the base field, with AdditionalTextMessage1..9 as named optional fields.
```

## 5. Finding range consolidation

This closure pass does not open new CE findings. It consolidates historical support for existing findings:

| Finding | Consolidated historical interpretation |
|---|---|
| CE-001 | Close as OK with note: V2.3 intentionally uses Common V2.3 + Enumerations V2.2 in the observed branch. Do not create a dummy Enumerations V2.3 file. |
| CE-002 | Remains OK with note: V2.4 history wording says StopPointNumber, but table/XSD use PointNumber. |
| CE-004 | Starts with V2.2: old SystemDocumentationService/SystemManagementService removed in history/XSD, but PDF tables still carry them through later docs. |
| CE-005 | Supported from V2.0 through V2.4: PDF/history expects AdditionalTextMessage repeatability, XSD models base AdditionalTextMessage as 0:1 and later adds named AdditionalTextMessage1..9. |
| CE-006 | Supported from V2.2 through V2.4: warning exists in XSD enumeration pool but is absent from the PDF table. |
| CE-007 | Supported historically at least from V1.x/V2.0 through V2.4 for checked values Valid/valid, Air/air and Other/other. |
| CE-008 | Supported from the V2.2 NetexMode/submode introduction through V2.4 for checked submode case mismatches. |
| CE-009 | Supported from the V2.2 NetexMode/submode introduction through V2.4: PDF specialRail vs XSD specialTrain. |
| CE-010 | Introduced/observed in V2.4 XSD: AirSubmode canalBarge is XSD-only in this audit chain. |
| CE-011 | Supported from V2.2 through V2.4: Connection TransportMode/ConnectionMode PDF 0:* vs XSD 0:1. |
| CE-012 | Supported through checked Common/Enums structure versions; final service-impact validation remains later. |
| CE-013 | Present through checked structure history: PDF uses InformationAtSpecificPoint wording, XSD uses SpecificPoint in an optional choice. |
| CE-014 | Present through checked structure history: DataVersionList PDF 1:* vs XSD 0:*. |
| CE-015 | Still deferred: visual confirmation required for FareZone/Farezone casing and ZoneType casing. |
| CE-016 | Observed at least in V2.3 and V2.4 XSD: GlobalCardStausID typo-like spelling remains XSD authority. |
| CE-017 | Observed through V2.3 and V2.4 for TSPPoint: Desciption remains XSD authority; visual V2.4 PDF confirmation remains deferred. |

## 6. CE-001 closure decision

Previous CE-001 state:

```text
Unclear whether the absence of IBIS-IP_Enumerations_V2.3.xsd is a defect.
```

Closure decision:

```text
CE-001 is OK with note.
The selected V2.3 pool is IBIS-IP_common_V2.3.xsd + IBIS-IP_Enumerations_V2.2.xsd.
This is a version-specific fact and must be represented in the later validation matrix.
```

Tool implication:

```text
When validating a V2.3 service using Common V2.3, load Enumerations V2.2 unless the audited service version explicitly points elsewhere.
Do not automatically substitute Enumerations V2.4 because it exists.
```

## 7. Validation backlog impact

Later technical validation should include these exact pools:

```text
Common/Enums V2.3 pool:
  IBIS-IP_common_V2.3.xsd
  IBIS-IP_Enumerations_V2.2.xsd

Common/Enums V2.4 pool:
  IBIS-IP_common_V2.4.xsd
  IBIS-IP_Enumerations_V2.4.xsd
```

Suggested targeted samples after schema compile:

```text
V2.3 negative / V2.4 positive: LineInformation.LinePublicCode.
V2.3 negative / V2.4 positive: StopInformation.StopGlobalID.
V2.3 negative / V2.4 positive: TripInformation.BlockNumber.
V2.3 negative / V2.4 positive: ServiceNameEnumeration AnalogRadioService.
V2.3 positive / V2.4 negative: DoorCountingObjectClassEnumeration WheelChair.
V2.3 negative / V2.4 positive: DoorCountingObjectClassEnumeration Wheelchair.
V2.4 positive with PDF note: AirSubmodeEnumeration canalBarge.
V2.4 negative for PDF value: RailSubmodeEnumeration specialRail.
V2.4 positive for XSD value: RailSubmodeEnumeration specialTrain.
```

## 8. Finding register update target

The following register update is justified by this closure file:

```text
CE-001: change state from unclear to OK with note.
Add affected-version/dependency note: V2.3 Common uses Enumerations V2.2.
```

Other CE findings should receive affected-version range notes, but no finding needs to be newly opened here.

## 9. Result

```text
Common/Enums historical first-pass chain V1.0/V1.x -> V2.4 is now complete.
V2.3 and V2.4 dependency pools are explicitly distinct.
CE-001 can be closed as OK with note.
No XSD correction is proposed by this closure pass.
Manual visual checks for CE-015, CE-017 and ZoneType remain deferred.
```

## 10. Next recommended step

After updating the register/index/handoff/backlog, continue with service-level historical audit:

```text
CustomerInformationService historical block.
```

Reason:

```text
Common/Enums foundation is now sufficiently mapped for service-level work.
CIS has multiple public PDF versions and high practical relevance for mixed-version systems.
```
