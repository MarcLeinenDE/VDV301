# COMMON V2.0 — VDV 301-2-1 — Deep Read Pass 2

Status: independent Fresh Read and exact-authority comparison frozen; historical Common findings intentionally unopened until after this freeze.

## Exact source

- Official publication URL: `https://www.vdv.de/301-2-1-sds-v-2-0.pdfx`
- Publication: VDV-Schrift 301-2-1, V2.0, `Common Data Structures and Enumerations`
- PDF SHA-256: `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088`
- Size: `946088` bytes
- Pin/render/read run: `33279811315`
- Job: `99172952524`
- Artifact: `9722644456` (`common-v20-pinned-read`)
- Artifact ZIP digest: `sha256:412a1714ce9c02b412262bb4d6103e686d85bf63709ad8a1bce2a3ac0d2361d9`
- Pages: `45`; all pages rendered at 120 dpi
- Extracted full-text SHA-256: `05e8a7e1788318bf5ac83ffdd61125622e28ce30f4fc5f388467a41ed46f5a3f`

Interactive PDF screenshot requests returned cache-miss. This was treated as a renderer/cache failure, not a source failure. The exact byte-pinned artifact was therefore used as the visual fallback. Material pages visibly inspected from that artifact include 13, 16, 17, 18, 21, 22, 24, 25, 26, 28, 29, 30, 31, 33, 35, 36, 37, 38 and 39.

## Exact V2.0 XSD authority established before historical findings

The official upstream tag `VDV-301-2.0` contains the exact family:

```text
IBIS-IP_common_V2.0.xsd        8608e3dcd665c197c34da7f6ec6af5a3758da164
IBIS-IP_Enumerations_V2.0.xsd  27e3c183b00381d959622d13c10543123af8eef6
```

`IBIS-IP_common_V2.0.xsd` directly includes `IBIS-IP_Enumerations_V2.0.xsd`. The same exact blobs are present on `dev/schema-integration`; there is no candidate/official split for this family.

## Independent Fresh Read observations

Historical Common finding registers were not consulted when deriving the observations below.

### FR-COM20-001 — InternationalTextType PDF type notation differs materially from exact V2.0 XSD

Pinned page 13 visibly documents `InternationalTextType` as:

```text
Value      1:1  IBIS-IP.string
Language   1:1  IBIS-IP.language
ErrorCode  0:1  ErrorCodeEnumeration
```

Exact V2.0 XSD defines:

```text
Value      xs:string
Language   xs:language
ErrorCode  ErrorCodeEnumeration, optional
```

Because `IBIS-IP.string` and `IBIS-IP.language` are wrapper complex types elsewhere in the schema family whereas the exact V2.0 declaration uses XSD primitives, this is potentially instance-shape relevant rather than a harmless display abbreviation.

### FR-COM20-002 — AdditionalAnnouncement choice differs in optionality and third element name

Pinned page 14 visibly marks the alternatives as a choice using VDV choice notation and names the third alternative `InformationAtSpecificPoint` of type `SpecificPoint`.

Exact V2.0 XSD uses `<xs:choice minOccurs="0">` with:

```text
ImmediateInformation
PeriodicalInformation
SpecificPoint
```

Thus the PDF presents a selected alternative while the XSD permits omitting the whole choice, and the third XML element name differs. The leading dash in the PDF notation is treated as the VDV choice marker, not negative cardinality.

### FR-COM20-003 — DataAcceptedResponse PDF table omits the exclusive XSD choice

Pinned page 16 visibly lists `DataAcceptedResponseData 1:1` and `OperationErrorMessage 1:1` as ordinary rows without the explicit choice grouping used by surrounding response tables.

Exact V2.0 XSD defines `DataAcceptedResponseStructure` as an `xs:choice` between exactly one `DataAcceptedResponseData` and `OperationErrorMessage`. A PDF-shaped instance containing both therefore conflicts with the executable compositor.

### FR-COM20-004 — several list/repetition cardinalities differ

Independent comparison found:

```text
DataVersionList.DataVersion:
  PDF 1:*
  XSD 0:*

DeviceSpecificationWithStateList.DeviceSpecificationWithState:
  PDF 1:*
  XSD 0:*

ServiceIdentificationWithStateList.ServiceIdentificationWithState:
  PDF 1:*
  XSD 0:*

ServiceSpecificationWithStateList.ServiceSpecificationWithState:
  PDF 1:*
  XSD 0:*

JourneyStopInformation.Announcement:
  PDF 0:*
  XSD 0:1

JourneyStopInformation.FareZone:
  PDF 0:*
  XSD 0:1
```

The V2.0 XSD now has a named `DataVersionListStructure`, unlike V1.0, but its `DataVersion` child remains `minOccurs="0" maxOccurs="unbounded"`.

### FR-COM20-005 — TripInformation AdditionalTextMessage is internally contradicted by the V2.0 document history and exact XSD

Pinned page 29 documents `AdditionalTextMessage 0:* +InternationalTextType` and includes the new `RouteDirection` field.

Pinned version-history page 39 explicitly states for Version 2.0 that `TripInformation` was updated so `AdditionalTextMessage` has `maxOccurs="unbounded"`.

Exact V2.0 XSD instead declares `AdditionalTextMessage` as optional `InternationalTextType` with no `maxOccurs`, therefore effective `0:1`. `RouteDirection` itself is present and correctly typed to `RouteDirectionEnumeration`.

The PDF table and its own V2.0 history therefore agree with each other on repeatability and disagree with the exact release XSD.

### FR-COM20-006 — multiple case-/spelling-sensitive XML identifiers differ

Visible PDF identifiers checked against exact V2.0 XSD include:

```text
PDF BeaconPoint.Description           XSD BeaconPoint.Desciption
PDF TSPPoint.Description              XSD TSPPoint.Desciption
PDF SubscribeRequest.Reply-Path       XSD ReplyPath
PDF UnsubscribeRequest.Reply-Path     XSD ReplyPath
PDF FarezoneID                        XSD FareZoneID
PDF FarezoneType                      XSD FareZoneType
PDF FarezoneLongName                  XSD FareZoneLongName
PDF FarezoneShortName                 XSD FareZoneShortName
PDF GlobalCardStatusID                XSD GlobalCardStausID
PDF ZoneType.FarezoneTypeName         XSD FareZoneTypeName
PDF LogMessage.MessageBody            XSD LogMessage.Message
PDF ShortTripStopList child label     XSD ShortTripStop
```

`Message-ID` is not included as a mismatch: both the V2.0 PDF and exact V2.0 XSD use `Message-ID`.

### FR-COM20-007 — ServiceIdentification family contains name/type substitutions

Pinned page 24 documents `ServiceIdentification` with outer row `ServiceName` of type `ServiceSpecification`, followed by `Device`.

Exact V2.0 XSD instead defines outer element `Service` of type `ServiceSpecificationStructure`, followed by `Device`.

The PDF also describes the `ServiceIdentificationWithStateList` member as `ServiceIdentificationWithState` but references `ServiceSpecificationWithState`; exact XSD uses `ServiceIdentificationWithStateStructure` and cardinality `0:*`.

The type/reference difference is therefore not merely omission of the conventional `Structure` suffix.

### FR-COM20-008 — case-sensitive enumeration lexemes differ while major V2.0 additions align

Exact pinned PDF versus Enumerations V2.0 confirms:

```text
DoorCountingObjectClassEnumeration:
  PDF Wheelchair / Others
  XSD WheelChair / Other

GNSSTypeEnumeration:
  PDF Other
  XSD other

TicketValidationEnumeration:
  PDF Valid
  XSD valid

VehicleModeEnumeration:
  PDF Air
  XSD air
```

In contrast, important V2.0 additions align between PDF and XSD: `readyForShutdown`, `RouteDirectionEnumeration`, `PassengerCountingService`, the three video service names, and `ServiceStateEnumeration.starting`.

### FR-COM20-009 — minor internal-document/editorial inconsistencies are grouped

Examples retained at low severity rather than inflated into many findings include:

- section heading/type uses singular `GNSSCoordinateSystemEnumeration` while a table row/caption uses plural `GNSSCoordinateSystemsEnumeration`; exact XSD is singular;
- spelling/English residue such as `dorr` and `Infromation` and similar non-executable editorial defects.

## Confirmed V1.1-to-V2.0 corrections / rejected overclaims

The Fresh Read also actively checked whether V1.x discrepancies had actually been corrected in V2.0. The following are aligned and must not be carried forward as defects merely because they existed in the public V1.x source:

- `Connection.DisplayContent` is optional in both V2.0 PDF and XSD.
- `ExpectedDepartureTime` is corrected in both V2.0 PDF and XSD.
- `ScheduledDepartureTime` exists in both.
- `TripInformation.RouteDirection` exists in both.
- `RouteDirectionEnumeration` exists in both.
- `DeviceStateEnumeration.readyForShutdown` exists in both.
- `PassengerCountingService`, video service names and `ServiceState.starting` exist in both.
- `IBIS-IP-VersionEnumeration` is not treated as a V2.0 requirement merely because it existed in V1.0.

Additional falsification rules retained:

1. choice notation is interpreted using the VDV notation rule, never as negative cardinality;
2. a leading `+` in PDF type notation is reference notation, not part of an XML QName;
3. line-wrap hyphens are not automatically promoted to XML-name characters;
4. enumeration order is ignored;
5. no XSD change is proposed from the PDF differences.

## Fresh-read freeze result

Nine independent observation groups are frozen against the byte-pinned official V2.0 publication and exact official `VDV-301-2.0` XSD family. Historical Common findings may now be opened only for deduplication and current-Evidence-Gate revalidation.

## Historical reconciliation and closure — 2026-08-30

Historical Common material was reopened only after independent freeze `60d8e6a444473615771bcab52e22293d96a8aa04`.

### Deduplification / scope extension

```text
CE-005: V2.0_scope_visible_table_and_version_history_plus_exact_0to1_XSD_declaration_EV-118
CE-007: V2.0_scope_executable_enum_lexeme_boundaries_confirmed_EV-118
CE-012: V2.0_scope_executable_empty_DeviceSpecificationWithStateList_confirmed_EV-118
CE-013: V2.0_scope_executable_optional_choice_and_SpecificPoint_name_boundary_EV-118
CE-014: V2.0_scope_executable_empty_DataVersionList_confirmed_EV-118
CE-015: V2.0_scope_visible_pdf_and_exact_XSD_FareZone_case_boundary_confirmed_EV-118
CE-016: V2.0_scope_visible_pdf_and_exact_XSD_GlobalCardStausID_boundary_confirmed_EV-118
CE-017: V2.0_scope_executable_TSPPoint_Description_vs_Desciption_boundary_EV-118
CE-018: V2.0_scope_visible_pdf_1star_plus_executable_empty_ServiceIdentificationWithStateList_EV-118
CE-019: V2.0_scope_visible_pdf_type_reference_plus_exact_ServiceIdentificationWithStateStructure_EV-118
CE-021: V2.0_scope_visible_MessageBody_vs_exact_XSD_Message_declaration_EV-118
CE-022: V2.0_scope_executable_outer_Service_vs_ServiceName_boundary_EV-118
CE-025: V2.0_scope_visible_Reply-Path_vs_exact_ReplyPath_declarations_EV-118
CE-026: V2.0_scope_executable_BeaconPoint_Description_vs_Desciption_boundary_EV-118
DRCOM10-002: V2.0_scope_executable_DataAcceptedResponse_choice_boundary_EV-118
DRCOM10-003: V2.0_scope_executable_empty_ServiceSpecificationWithStateList_EV-118
DRCOM10-004: V2.0_scope_exact_JourneyStop_Announcement_FareZone_0to1_declarations_EV-118
DRCOM10-005: V2.0_scope_refined_child_name_facet_persists_type_facet_aligned_exact_XSD_EV-118
DRCOM10-006: V2.0_scope_executable_DoorCountingObjectClass_lexemes_EV-118
DRCOM10-007: V2.0_scope_context_verified_grouped_editorial_residue
```

Only one new V2.0-specific ID is required:

```text
DRCOM20-001: pdf_type_reference_vs_xsd_primitive_instance_shape_mismatch
```

`CE-020` is deliberately not broadened because its finding identity includes the V2.3
PR #30 authority collision. `DRCOM20-001` isolates the V2.0 PDF-vs-official-XSD
primitive/wrapper type difference without importing later candidate history.

`DRCOM10-005` is refined for V2.0: the child-label mismatch persists, but the V1.x
StopPointTariffInformation type/model facet is not carried forward because the V2.0 PDF
type is aligned with the ShortTripStop model.

### Executable evidence

EV-118 run `33280224191` / job `99174026383` PASS against exact official V2.0 blobs
`8608e3dcd665c197c34da7f6ec6af5a3758da164` + `27e3c183b00381d959622d13c10543123af8eef6`.

### Closure

COMMON V2.0 remains `needs_visual_review`, not `exhaustive_read`: all 45 pinned pages
were rendered and material finding pages were visibly reviewed, but the visual pass was
targeted rather than pixel-by-pixel exhaustive.

No XSD was changed. Next natural Deep Read unit: `COMMON_V2.1`.
