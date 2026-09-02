# COMMON V2.2 — VDV 301-2-1 — Deep Read Pass 2

Status: source-rederived Fresh Read observation freeze prepared from exact pinned V2.2 PDF and exact historical-upstream V2.2 XSD family. Historical independence is **not claimed as pristine** because a file-library search accidentally exposed historical Common finding material after the source-only comparison had begun but before the formal freeze commit. No historical finding ID or prior disposition is used to construct or expand the observation list below.

## Exact source

- Official publication: VDV-Schrift 301-2-1, V2.2, 08/2019, `Common Data Structures and Enumerations`.
- Official URL: `https://www.vdv.de/301-2-1-sdes-v2-2-commonstructure-enums.pdfx`
- PDF SHA-256: `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`
- Size: `1411558` bytes
- Pin/render/read run: `33614504943`
- Artifact: `9840345496` (`common-v22-pinned-read`)
- Artifact digest: `sha256:72bcf873ea86daf543acef1bf3050773f74ee31c57aed314be684a6e52f9a253`
- Pages: `55`; all pages rendered at 120 dpi
- Extracted full-text SHA-256: `4153a25b69cd9262fd6e2900f8275d13ffbdc76d0ca50b05196a7e5a7b2fb99e`
- Local artifact verification: full-text hash and all 55 page-PNG hashes match the manifest.

The interactive official-PDF path timed out. This was treated as an access/rendering failure, not as a source failure; the exact byte-pinned artifact is the visual fallback.

## Exact V2.2 XSD authority

No upstream tag named `VDV-301-2.2` resolves. Authority is therefore routed through the actual historical upstream file lineage rather than an invented tag or a later schema.

Exact historical-upstream V2.2 family:

```text
IBIS-IP_common_V2.2.xsd
  blob: 468fee6d177e7185dbcd5d3f90cfb114e29e01ae
  last V2.2 file modification before V2.3 lineage:
  775def7b24901bfd515c80fa5fe57f12562873fd

IBIS-IP_Enumerations_V2.2.xsd
  blob: 2a23b512379b18e8f122ac1272cef8229fb86283
  last V2.2 file modification:
  591ca66d8b94bb5c2a7f9440b3e31e28f8261a88
```

Common V2.2 directly includes Enumerations V2.2. The integration branch contains the same exact blobs. `latest wins` is forbidden.

## Method and disclosure

The full extracted text of all 55 pages was read. All 65 Common structure sections and all 40 enumeration sections were systematically compared against the exact V2.2 XSD family. Material candidates were then checked against the exact pinned page renders. Targeted visible pages included 12, 15–19, 21, 24–27, 29, 31–35, 37, 39–41, 43, 45–46 and 48–49.

A later file-library search unintentionally surfaced historical Common finding material before this freeze was committed. The observation set below was therefore re-derived from the complete V2.2 source/XSD matrix and is frozen with that process defect disclosed. It must not be described later as a pristine clean-room read.

## Source-rederived Fresh Read observations

### FR-COM22-001 — InternationalTextType PDF wrapper types differ from exact XSD primitives

Pinned page 12 visibly documents:

```text
Value     1:1 IBIS-IP.string
Language  1:1 IBIS-IP.language
ErrorCode 0:1 ErrorCodeEnumeration
```

Exact Common V2.2 XSD defines:

```text
Value     xs:string
Language  xs:language
ErrorCode ErrorCodeEnumeration, optional
```

The PDF type names refer to wrapper complex types while the XSD uses primitive lexical content directly. This is instance-shape relevant.

### FR-COM22-002 — NetexMode choice groups are mandatory in the PDF but optional in XSD

Pinned page 15 visibly uses VDV choice notation `–1:1` for both:
- the `PtMainMode` / `PrivateMainMode` choice, and
- the public/private submode choice.

Exact V2.2 XSD instead uses two separate `<xs:choice minOccurs="0">` compositors. It therefore allows a `NetexMode` with neither main mode nor submode.

This observation treats the leading dash as the VDV choice marker, not as a negative cardinality.

### FR-COM22-003 — AdditionalAnnouncement differs in choice optionality and third element name

Pinned page 16 visibly presents a one-of choice and names its third branch:

```text
InformationAtSpecificPoint
```

Exact V2.2 XSD uses an optional `<xs:choice minOccurs="0">` with:

```text
ImmediateInformation
PeriodicalInformation
SpecificPoint
```

Thus the whole choice may be absent in XSD, and the third XML element name differs.

### FR-COM22-004 — Connection TransportMode and ConnectionMode repeatability differs

Pinned page 18 visibly documents both:

```text
TransportMode  0:*
ConnectionMode 0:*
```

Exact V2.2 XSD declares both with `minOccurs="0"` and no `maxOccurs`, therefore effective `0:1`.

### FR-COM22-005 — DataAcceptedResponse table omits the exclusive XSD choice

Pinned page 18 visibly lists:

```text
DataAcceptedResponseData 1:1
OperationErrorMessage    1:1
```

as ordinary rows. Exact XSD defines an `xs:choice` between exactly one of the two. A PDF-shaped instance containing both conflicts with the executable compositor.

### FR-COM22-006 — several list structures document 1:* while exact XSD permits empty lists

Visible PDF / exact XSD:

```text
DataVersionList.DataVersion:
  PDF 1:*   XSD 0:*

DeviceSpecificationWithStateList.DeviceSpecificationWithState:
  PDF 1:*   XSD 0:*

ServiceIdentificationWithStateList.ServiceIdentificationWithState:
  PDF 1:*   XSD 0:*

ServiceSpecificationWithStateList.ServiceSpecificationWithState:
  PDF 1:*   XSD 0:*
```

Other checked list structures such as DeviceSpecificationList, ServiceInformationList, ServiceStartList, PointSequence and StopSequence retain aligned non-empty minima.

### FR-COM22-007 — field-level cardinality differences occur in both directions

Visible PDF / exact XSD:

```text
JourneyStopInformation.Announcement:
  PDF 0:*   XSD 0:1

JourneyStopInformation.FareZone:
  PDF 0:*   XSD 0:1

StopInformationRequest.StopName:
  PDF 0:1   XSD 0:*

TripInformation.AdditionalTextMessage:
  PDF 0:*   XSD 0:1

UnsubscribeResponse.Active:
  PDF 0:1   XSD 1:1
```

The TripInformation mismatch is additionally contradicted by the document's own page-48 Version-2.0 history, which explicitly says `AdditionalTextMessage: maxOccurs="unbounded"` was updated.

### FR-COM22-008 — multiple case-/spelling-sensitive XML identifiers differ

Visible V2.2 PDF vs exact Common V2.2 XSD:

```text
PDF BeaconPoint.Description            XSD BeaconPoint.Desciption
PDF TSPPoint.Description               XSD TSPPoint.Desciption

PDF FareZoneInformation.FarezoneID        XSD FareZoneID
PDF FareZoneInformation.FarezoneType      XSD FareZoneType
PDF FareZoneInformation.FarezoneLongName  XSD FareZoneLongName
PDF FareZoneInformation.FarezoneShortName XSD FareZoneShortName

PDF GlobalCardStatus.GlobalCardStatusID XSD GlobalCardStausID

PDF LogMessage.MessageBody              XSD LogMessage.Message

PDF SubscribeRequest.Reply-Path         XSD ReplyPath
PDF UnsubscribeRequest.Reply-Path       XSD ReplyPath

PDF ZoneType.FarezoneTypeName           XSD FareZoneTypeName
```

`Message-ID` is aligned and is not a finding. Layout line-wrap hyphens are not promoted automatically to XML-name characters.

### FR-COM22-009 — ServiceIdentification family contains element/type substitutions

Pinned page 27 documents outer `ServiceIdentification` as:

```text
ServiceName 1:1 +ServiceSpecification
Device      1:1 +DeviceSpecification
```

Exact XSD uses outer element `Service`, type `ServiceSpecificationStructure`, followed by `Device`.

The same page documents `ServiceIdentificationWithStateList` item `ServiceIdentificationWithState` but associates it with `ServiceSpecificationWithState`; exact XSD uses `ServiceIdentificationWithStateStructure`.

These are not merely omitted `Structure` suffixes; the referenced model identity differs.

### FR-COM22-010 — ShortTripStopList child name differs

Pinned page 29 visibly names the repeating child `ShortTripStopList` with type `ShortTripStop`.

Exact XSD defines the repeating child as:

```text
ShortTripStop
```

of type `ShortTripStopStructure`.

### FR-COM22-011 — section 2.34 is a corrupt duplicate NetexMode table

Pinned page 26 contains section `2.34 NetexMode`, but its table header/body is visibly the `Message` structure:

```text
Message
Message-ID
TimeStamp
MessageType
MessageText
```

The correct NetexMode model is already given on page 15 and is represented in XSD by the main-mode/submode choices. This is an internal documentation copy/paste error, not an XSD-shape basis.

### FR-COM22-012 — DeviceState and ServiceName enumeration inventories disagree with XSD, and ServiceName contradicts V2.2 history

Pinned page 37 `DeviceStateEnumeration` lists:

```text
defective
notavailable
running
readyForShutdown
```

Exact Enumerations V2.2 additionally contains `warning`.

Pinned page 40 `ServiceNameEnumeration` still contains both:

```text
SystemDocumentationService
SystemManagementService
```

while exact Enumerations V2.2 contains neither and does contain `SystemMonitoringService`.

Pinned page 49's own Version-2.2 history explicitly says `SystemDocumentationService` and `SystemManagementService` were deleted and `SystemMonitoringService` added. The page-40 table is therefore internally stale relative to the same official PDF.

### FR-COM22-013 — case-sensitive and NeTEx enumeration lexemes/inventory differ

Visible PDF vs exact Enumerations V2.2 includes:

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
  PDF Unknown / Undefined
  XSD unknown / undefined
```

Enumeration order alone is ignored. The remaining checked NeTEx mode/submode values are not promoted merely for ordering or layout differences.

### FR-COM22-014 — grouped internal documentation/cross-reference errors

Low-severity documentation residue is grouped instead of inflated into separate executable findings:

- page 49 says `LineCode` was added to `DisplayContent (2.31)`, but section 2.31 is `LineInformation`, and the exact XSD also places `LineCode` in `LineInformationStructure`;
- page 49 references `Heartbeat (2.55; 2.61)`, while the visible Heartbeat member is in `SubscribeResponse` section 2.56 and section 2.61 is `UnsubscribeRequest`;
- page 31 Table 53 is `StopPointTariffInformation` but its caption says `Description of StopInformation`;
- section 2.5 is headed singular `CardApplInformation` while its displayed structure name is plural `CardApplInformations`;
- section 3.13 heading is singular `GNSSCoordinateSystemEnumeration`, while table body/caption print plural `GNSSCoordinateSystemsEnumeration`; exact XSD type is singular;
- wording residue includes `dorr`, `Infromation`, `WateSubmode`, `directiona`, and the Taxi/SelfDrive rows on page 15 describing private submodes as air transportation.

## Active falsification and aligned areas

The source-only comparison also deliberately rejected plausible overclaims:

1. `–1:1` is treated as choice notation. `PointType` page 27 and exact XSD both require one choice, showing the notation itself is not defective.
2. A leading `+` in a PDF type column is reference notation, not part of an XML QName.
3. IBIS-IP wrapper types 1.1–1.16 align with the exact XSD.
4. Announcement, BayArea, card structures, Destination, DeviceInformation, DeviceSpecification/List, the core DisplayContent structure, door structures, GNSS structures, LineInformation itself, Point/PointSequence/PointType, ServiceInformation/List, ServiceSpecification/WithState, ServiceStart/List, ShortTripStop itself, SpecificPoint, StopInformation, StopSequence, SubscribeResponse cardinalities, TimingPoint, TripSequence, Vehicle and ViaPoint are aligned in the checked facets.
5. `SubscribeResponse` prose says Active *should* be set when no error message exists. This recommendation is not promoted into an XSD defect merely because the XSD permits other optional combinations.
6. Enumeration ordering differences are ignored.
7. No XSD change is proposed from any observation.

## Freeze result

Fourteen source-rederived observation groups are frozen against the exact pinned V2.2 publication and exact historical-upstream V2.2 Common/Enumerations family.

The historical-independence boundary is explicitly qualified because of the accidental pre-freeze file-library exposure. Any later historical reconciliation must use this frozen list as immutable input and may only map/deduplicate/revalidate it; it must not retrospectively add observations while calling them part of this freeze.

No XSD was changed.
