# COMMON V2.3 — VDV 301-2-1 — source-only Fresh Read freeze

Status: independent source/XSD observation freeze for Deep Read Pass 2. Historical COMMON V2.3 reports, Common finding registers and prior finding dispositions were intentionally not opened before this freeze.

## Exact source

- Official publication: VDV-Schrift 301-2-1, V2.3, Common Data Structures and Enumerations, 02/2021.
- Official URL: `https://www.vdv.de/301-2-1-sdes-v2-3-commonstructure-enums.pdfx`
- PDF SHA-256: `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`
- Size: `793521` bytes.
- Fresh pin/render/read run: `33656579631`, job `100336514663`, result PASS.
- Artifact: `9856965744` (`common-v23-pinned-read`).
- Artifact digest: `sha256:a3c0a59cf1a5e6ca8a98c7419c5f02e1445efa503b6986c62daa2f53171eb746`.
- Pages: `58`; all pages rendered at 120 dpi.
- Extracted full-text SHA-256: `c0ac2f22f0d4cf155d601d26c9c550214d7db221c0ce185eaeba26df27149c16`.
- The fresh official retrieval is byte-identical to the pre-existing 2026-08-28 pin.
- All 58 page PNG hashes were rechecked against the artifact manifest.

## Exact V2.3 XSD authority

Official upstream tag: `VDV-301-2.3`.

```text
IBIS-IP_common_V2.3.xsd
  blob: 0d8926c4063c12de9a5e68b6f0addaab35a55dc1

IBIS-IP_Enumerations_V2.2.xsd
  blob: 2a23b512379b18e8f122ac1272cef8229fb86283
```

The official V2.3 Common XSD explicitly includes `IBIS-IP_Enumerations_V2.2.xsd`; there is no V2.3 enumeration substitution in this authority route. The integration branch contains the exact same two blobs. `latest wins` is forbidden.

## Method

The complete extracted text of all 58 pages was read and the Common structures/enumerations were compared against the exact V2.3 Common / V2.2 Enumerations XSD family. Material candidates were checked against the rendered pinned pages. The comparison deliberately distinguishes XML choice notation from ordinary cardinality and treats exact XML spelling, case, compositor and multiplicity as executable boundaries.

Historical Common findings remain quarantined until this observation list is frozen. The list below is therefore the immutable input to later historical reconciliation.

## Frozen source-only observations

### FR-COM23-001 — InternationalTextType PDF wrapper types differ from exact XSD primitives

Visible PDF table documents:

```text
Value     1:1 IBIS-IP.string
Language  1:1 IBIS-IP.language
ErrorCode 0:1 ErrorCodeEnumeration
```

Exact Common V2.3 XSD defines `Value` as `xs:string` and `Language` as `xs:language`. The PDF type names refer to wrapper complex types while the executable XSD uses primitive lexical content directly. This is instance-shape relevant.

### FR-COM23-002 — NetexMode mandatory PDF choices are optional in exact XSD

The PDF marks both NetexMode one-of groups with VDV choice notation `–1:1`: one main-mode branch and one public/private submode branch.

Exact XSD defines two separate `<xs:choice minOccurs="0">` compositors. Consequently an empty `NetexMode` is XSD-permitted although the PDF presents both choices as mandatory.

The leading dash is the VDV choice marker; it is not interpreted as a negative cardinality.

### FR-COM23-003 — AdditionalAnnouncement differs in choice optionality and third branch name

The PDF presents a one-of choice and names the third branch `InformationAtSpecificPoint`.

Exact XSD uses an optional `<xs:choice minOccurs="0">` with the branches:

```text
ImmediateInformation
PeriodicalInformation
SpecificPoint
```

Thus the XSD allows the choice to be absent and uses a different XML element name for the third branch.

### FR-COM23-004 — Connection TransportMode and ConnectionMode repeatability differs

The PDF documents both `TransportMode` and `ConnectionMode` as `0:*`.

Exact Common V2.3 XSD declares both with `minOccurs="0"` and no `maxOccurs`, therefore effective `0:1`.

### FR-COM23-005 — DataAcceptedResponse PDF rows hide the exclusive XSD choice

The PDF lists `DataAcceptedResponseData 1:1` and `OperationErrorMessage 1:1` as ordinary rows. Exact XSD defines an `xs:choice` between exactly one of the two branches. An instance containing both is therefore not valid against the executable schema.

### FR-COM23-006 — four list structures document 1:* while exact XSD permits empty lists

PDF / exact XSD:

```text
DataVersionList.DataVersion                         PDF 1:*  XSD 0:*
DeviceSpecificationWithStateList.DeviceSpecificationWithState
                                                    PDF 1:*  XSD 0:*
ServiceIdentificationWithStateList.ServiceIdentificationWithState
                                                    PDF 1:*  XSD 0:*
ServiceSpecificationWithStateList.ServiceSpecificationWithState
                                                    PDF 1:*  XSD 0:*
```

Other checked list structures with explicit non-empty minima remain aligned and are not included in this observation.

### FR-COM23-007 — case- and spelling-sensitive XML identifiers differ

Visible PDF versus exact XSD includes:

```text
BeaconPoint.Description                  -> Desciption
FareZoneInformation.FarezoneID           -> FareZoneID
FareZoneInformation.FarezoneType         -> FareZoneType
FareZoneInformation.FarezoneLongName     -> FareZoneLongName
FareZoneInformation.FarezoneShortName    -> FareZoneShortName
GlobalCardStatus.GlobalCardStatusID       -> GlobalCardStausID
LogMessage.MessageBody                    -> Message
SubscribeRequest.Reply-Path               -> ReplyPath
UnsubscribeRequest.Reply-Path             -> ReplyPath
TSPPoint.Description                      -> Desciption
ZoneType.FarezoneTypeName                 -> FareZoneTypeName
```

`FarezoneTypeID` itself aligns and is not promoted into this finding. Layout line-wrap hyphens are not automatically treated as XML-name characters.

### FR-COM23-008 — JourneyStopInformation Announcement and FareZone are less repeatable in XSD

The PDF documents both `Announcement` and `FareZone` as `0:*`.

Exact XSD declares each with `minOccurs="0"` and no `maxOccurs`, therefore effective `0:1`.

### FR-COM23-009 — ServiceIdentification family contains element/type substitutions

The PDF documents the outer `ServiceIdentification` element as `ServiceName` with referenced `ServiceSpecification`. Exact XSD uses outer element `Service` of type `ServiceSpecificationStructure`.

The PDF also associates the repeating `ServiceIdentificationWithStateList.ServiceIdentificationWithState` item with `ServiceSpecificationWithState`; exact XSD uses `ServiceIdentificationWithStateStructure`.

These are model-identity differences, not merely omitted `Structure` suffixes.

### FR-COM23-010 — ShortTripStopList repeating child name differs

The PDF names the repeating child `ShortTripStopList` and references `ShortTripStop` as its type. Exact XSD defines the repeating child as `ShortTripStop` of type `ShortTripStopStructure`.

### FR-COM23-011 — StopInformationRequest has cardinality drift plus two PDF fields absent from exact XSD

The PDF documents:

```text
StopName          0:1
ArrivalExpected   0:1
DepartureExpected 0:1
```

Exact `StopInformationRequestStructure` instead declares `StopName` as `0:*` and contains neither `ArrivalExpected` nor `DepartureExpected`.

The document's own V2.3 version history states that `ArrivalExpected` and `DepartureExpected` were added to StopInformation and references both sections 2.51 and 2.52. Exact XSD contains both fields in `StopInformationStructure`, where they align, but not in `StopInformationRequestStructure`. The discrepancy is therefore specifically observable at StopInformationRequest.

### FR-COM23-012 — TripInformation AdditionalTextMessage family is less repeatable in XSD

The PDF documents the base `AdditionalTextMessage` as `0:*` and the V2.3 `AdditionalTextMessage(n)` family (`n = 1..9`) as `0:*`.

Exact XSD declares the base element and each explicit `AdditionalTextMessage1` through `AdditionalTextMessage9` as `0:1`.

The `(n)` notation is treated as documentation shorthand for the numbered elements, not as a literal XML element name. The newly added `RunNumber`, `PatternNumber` and `PathDestinationNumber` fields align at `0:1` and are not findings.

### FR-COM23-013 — UnsubscribeResponse.Active is optional in PDF but required by XSD

The PDF documents `Active 0:1`. Exact `UnsubscribeResponseStructure` declares `Active` without `minOccurs`, therefore required `1:1`.

### FR-COM23-014 — enumeration inventories and lexical values differ

Visible PDF versus exact Enumerations V2.2 includes:

```text
DeviceStateEnumeration:
  PDF omits warning
  XSD contains warning

ServiceNameEnumeration:
  PDF still prints SystemDocumentationService and SystemManagementService
  XSD excludes both and contains SystemMonitoringService

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

RailSubmodeEnumeration:
  PDF specialRail
  XSD specialTrain

AirSubmodeEnumeration:
  PDF omits canalBarge
  XSD contains canalBarge

FunicularSubmodeEnumeration:
  PDF Unknown
  XSD unknown

TaxiSubmodeEnumeration:
  PDF Unknown / Undefined / minicab
  XSD unknown / undefined / miniCab
```

Enumeration order alone is ignored.

### FR-COM23-015 — GNSS coordinate-system enumeration identifier is internally singular/plural inconsistent

The section heading uses singular `GNSSCoordinateSystemEnumeration`, while the visible table body/caption print plural `GNSSCoordinateSystemsEnumeration`. Exact XSD simpleType is singular `GNSSCoordinateSystemEnumeration`.

### FR-COM23-016 — grouped internal documentation and cross-reference residue

Low-severity non-executable documentation residue is grouped rather than inflated into individual schema findings. Examples include:

- DeviceClass cross-reference points to the wrong enumeration section;
- DoorCounting ObjectClass cross-reference is offset from the actual DoorCountingObjectClass enumeration section;
- `ShortTripStop.FareZoneInformation` references section 2.53 although the FareZoneInformation structure is section 2.26;
- the StopPointTariffInformation table caption says `Description of StopInformation`;
- section heading `CardApplInformation` is singular while the displayed structure is `CardApplInformations`;
- V2.2 history residue says LineCode was integrated into `DisplayContent (2.31)` although section 2.31 is LineInformation and the exact XSD places LineCode in LineInformationStructure;
- Heartbeat history cross-references do not match the visible SubscribeResponse section;
- minor spelling/wording residue such as `DisplaContent` remains.

These do not change executable XML validation by themselves.

## Active falsification and aligned areas

1. VDV `–1:1` is choice notation, never a negative cardinality.
2. `PointType` uses the same choice notation and aligns with a required XSD choice, confirming the notation itself is not defective.
3. A leading `+` in a PDF type column is reference notation, not part of an XML QName.
4. `AdditionalInformation(n)` is treated as shorthand for the explicit `AdditionalInformation1..9` XSD elements; the checked cardinality aligns at `0:*`.
5. V2.3 `DisplayContent.RunNumber` aligns.
6. V2.3 `TripInformation.RunNumber`, `PatternNumber` and `PathDestinationNumber` align.
7. `StopInformation.ArrivalExpected` and `StopInformation.DepartureExpected` align; the absence is specifically in `StopInformationRequestStructure`.
8. DeviceSpecificationList, ServiceInformationList, ServiceStartList, PointSequence and StopSequence retain aligned non-empty minima.
9. SubscribeResponse prose that Active *should* be set in a meaningful response is not promoted into an XSD defect when the schema intentionally allows optional members.
10. Enumeration ordering differences are ignored.
11. Inline formatting tags shown inside text values are content syntax, not inferred XSD child declarations.
12. The exact pinned V2.3 page for section 2.34 NetexMode shows the NetexMode heading and description, not a duplicate Message table. No corrupt second NetexMode table is part of this Fresh Read freeze.
13. No XSD change is proposed or performed.

## Freeze result

Sixteen source-only observation groups are frozen against the freshly revalidated official V2.3 PDF and exact official `VDV-301-2.3` Common / Enumerations V2.2 authority family.

Historical reconciliation may map, deduplicate, refine or falsify prior finding identities, but it must not retrospectively add observations while describing them as part of this freeze. Where old historical material conflicts with the exact pinned V2.3 source, the fresh source evidence takes precedence for V2.3 scope determination.
