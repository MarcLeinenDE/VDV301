# COMMON V1.0 — VDV 301-2-1 — Deep Read Pass 2

Status: independent Fresh Read and exact-authority comparison frozen; historical Common findings intentionally unopened until after this freeze.

## Exact source

- Official publication URL: `https://www.vdv.de/301-2-1-sds.pdfx`
- Publication: VDV-Schrift 301-2-1, 05/2017, `Gemeinsame Datenstrukturen und Aufzählungstypen / Common data structures and enumerations`
- PDF SHA-256: `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf`
- Size: `892769` bytes
- Pin/render/read run: `33275626001`
- Job: `99161707311`
- Artifact: `9721397514` (`common-v10-pinned-read`)
- Artifact ZIP digest: `sha256:89c464676008150dbcbb99a5def23c9276043eac39226025086a9e8ed36e1221`
- Pages: `36`; all pages rendered at 120 dpi
- Extracted full-text SHA-256: `fdfdf62a88f78dd7a59b341157662d3e5708b2f9c56d2cf1df13a7d4eb0cfa0a`

## Exact V1.0 XSD authority established before historical findings

The official upstream repository history was checked independently rather than inferring authority from a later release.

Both V1.0 XSD files have the same single introduction commit in `VDVde/VDV301`:

```text
604a5a5c7608977e483072f7e450d7381cc182e4
2014-05-16
Erste Version der VDV 301 XSD Dateien von http://www.vdv.de/ibis-ip-v1.zipx?forced=true
```

Exact blobs:

```text
IBIS-IP_common_V1.0.xsd        194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
IBIS-IP_Enumerations_V1.0.xsd  a9bea5bc73003ed91ded8519db06c32c4067831d
```

`IBIS-IP_common_V1.0.xsd` directly includes `IBIS-IP_Enumerations_V1.0.xsd`. The same exact blobs are present on `dev/schema-integration`; therefore there is no candidate/official split for this V1.0 family.

No `IBIS-IP_common_V1.1.xsd` exists in the official repository and repository search returned no such file. This fact does not mean the 05/2017 PDF is misidentified: page 27 still defines `IBIS-IP-VersionEnumeration = 1.0`, while page 30 separately records document/data-definition revision `Version 1.1`. The source is therefore retained under the audit unit `COMMON_V1.0`; the revision/XSD divergence is examined rather than silently renamed.

## Independent Fresh Read observations

Historical Common finding registers were not consulted when deriving the observations below.

### FR-COM10-001 — explicit Version-1.1 document changes are not present in the unchanged official V1.0 XSD family

Pinned page 30 visibly records `Version 1.1` and explicitly states:

- `Connection`: new `ScheduledDepartureTime`; Min:Max information corrected.
- `TripInformation`: `AdditionalTextMessage` changed from `IBIS-IP.string` to `InternationalTextType`; new `RouteDirection` added.
- new `RouteDirectionEnumeration` added.

The visible data tables implement those statements: page 9 has `ScheduledDepartureTime` and optional `DisplayContent`; page 21 has multilingual/repeating `AdditionalTextMessage` and `RouteDirection`; page 28 contains `RouteDirectionEnumeration`.

The exact official V1.0 XSD blobs remain the 2014 initial-import versions and instead contain:

- no `ScheduledDepartureTime`;
- `Connection.DisplayContent` required rather than PDF `0:1`;
- misspelled `ExpectedDepatureTime` rather than PDF `ExpectedDepartureTime`;
- `TripInformation.AdditionalTextMessage` as optional single `IBIS-IP.string`;
- no `TripInformation.RouteDirection`;
- no `RouteDirectionEnumeration` in Enumerations V1.0.

This is a release/document-to-XSD semantic drift, not a reason to modify the XSD. For executable validation the selected V1.0 XSD family remains authoritative.

### FR-COM10-002 — AdditionalAnnouncement choice differs in both cardinality and selected element name

Pinned page 7 visibly marks the three alternatives as a `choice` with the VDV choice notation `–1:1` and names the third alternative `InformationAtSpecificPoint` of type `SpecificPoint`.

The exact XSD has `<xs:choice minOccurs="0">` and names the third element `SpecificPoint`. Thus the PDF describes a mandatory one-of choice while the XSD permits omitting the whole choice, and the third XML element name also differs.

The leading dash is treated as the VDV XML-choice marker; it is not interpreted as a negative cardinality.

### FR-COM10-003 — DataAcceptedResponse table omits the XSD choice and makes both alternatives appear mandatory

Pinned page 9 visibly lists `DataAcceptedResponseData 1:1` and `OperationErrorMessage 1:1` as ordinary rows, with no choice marker/group.

The exact XSD defines `DataAcceptedResponseStructure` as an `xs:choice` between exactly one `DataAcceptedResponseData` and `OperationErrorMessage`. This difference is executable XML behavior, not merely table styling.

### FR-COM10-004 — multiple case-sensitive XML identifier spellings differ between PDF and exact XSD

Visible PDF identifiers were checked against the exact XSD. Confirmed examples include:

```text
PDF BeaconPoint.Description           XSD BeaconPoint.Desciption
PDF TSPPoint.Description              XSD TSPPoint.Desciption
PDF Connection.ExpectedDepartureTime  XSD ExpectedDepatureTime
PDF SubscribeRequest.Reply-Path       XSD ReplyPath
PDF UnsubscribeRequest.Reply-Path     XSD ReplyPath
PDF FarezoneID                        XSD FareZoneID
PDF FarezoneType                      XSD FareZoneType
PDF FarezoneLongName                  XSD FareZoneLongName
PDF FarezoneShortName                 XSD FareZoneShortName
PDF GlobalCardStatusID                XSD GlobalCardStausID
PDF ZoneType.FarezoneTypeName         XSD FareZoneTypeName
PDF LogMessage.MessageBody            XSD LogMessage.Message
```

These are case-/spelling-sensitive XML names where applicable. Line-wrap hyphens introduced only by table layout are excluded from this observation.

### FR-COM10-005 — list/repetition cardinalities diverge in several structures

Independent comparison found the following material Min:Max differences:

```text
DeviceSpecificationWithStateList:
  PDF DeviceSpecificationWithState 1:*
  XSD minOccurs=0 maxOccurs=unbounded

ServiceIdentificationWithStateList:
  PDF ServiceIdentificationWithState 1:*
  XSD minOccurs=0 maxOccurs=unbounded

ServiceSpecificationWithStateList:
  PDF ServiceSpecificationWithState 1:*
  XSD minOccurs=0 maxOccurs=unbounded

JourneyStopInformation.Announcement:
  PDF 0:*
  XSD minOccurs=0, maxOccurs default 1

JourneyStopInformation.FareZone:
  PDF 0:*
  XSD minOccurs=0, maxOccurs default 1
```

The PDF also presents a named `DataVersionList` structure with `DataVersion 1:*`; the V1.0 XSD has no named `DataVersionListStructure`, and the anonymous `DataVersionList` inside `DeviceInformationStructure` permits `DataVersion 0:*`.

### FR-COM10-006 — ServiceIdentification family contains element/type substitutions in the PDF tables

Pinned page 17 visibly describes `ServiceIdentification` with a row named `ServiceName` of type `ServiceSpecification`; exact XSD instead defines element `Service` of type `ServiceSpecificationStructure`.

The same page describes the `ServiceIdentificationWithStateList` member as `ServiceIdentificationWithState` but types it as `ServiceSpecificationWithState` and points to section 1.43. Exact XSD types that member as `ServiceIdentificationWithStateStructure`. This is not a harmless shortened `Structure` suffix: it changes which data structure is referenced.

### FR-COM10-007 — ShortTripStop naming/type model differs between PDF and exact XSD

Pinned page 18 shows `ShortTripStopList` with a repeating child displayed as `ShortTripStopList` and type `StopPointTariffInformation` (cross-reference 1.49). Page 19 separately documents `StopPointTariffInformationStructure`.

Exact XSD defines `ShortTripStopListStructure` with repeating element `ShortTripStop` of type `ShortTripStopStructure`; that structure contains `JourneyStopInformation` and `FareZoneInformation`. The XSD also separately contains `StopPointTariffInformationStructure` with the same two members. Therefore the PDF and XSD disagree on both the list member name and its declared type/model identity.

Page 19 additionally captions Table 49 `Description of StopInformation` although the section/table itself is `StopPointTariffInformation`; this caption is editorial residue and is not used as the structural authority for the preceding finding.

### FR-COM10-008 — enumeration value sets/case and inventory diverge

Exact PDF render and Enumerations V1.0 comparison confirms:

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

ServiceNameEnumeration:
  PDF additionally lists PassengerCountingService
  XSD does not contain it

ServiceStateEnumeration:
  PDF additionally lists starting
  XSD does not contain it

RouteDirectionEnumeration:
  PDF contains the complete enumeration
  XSD V1.0 does not define the type at all
```

Enumeration order alone was ignored. The exact V1.0 XSD additionally defines `DataIntervallEnumeration` and `DeviceTaskEnumeration`, neither of which appears in the PDF chapter/table inventory; this is retained as an inventory asymmetry but is not yet promoted to an independent defect without service-context reconciliation.

### FR-COM10-009 — minor internal-document/editorial inconsistencies are grouped

Examples retained at low severity rather than inflated into many findings:

- page 26 section/type heading uses singular `GNSSCoordinateSystemEnumeration`, but the table's `Enumeration Name` and caption print `GNSSCoordinateSystemsEnumeration`;
- `Common enummerations`, `dorr operation`, `Infromation`, and several broken/incorrect `cf. 0` cross-references;
- page 30 English version-history bullets retain German words such as `ergänzt` and `Typ`.

These do not independently change executable validation behavior.

## Active falsification / rejected overclaims

1. `Version 1.1` on page 30 is not treated as proof that the IBIS-IP protocol version should be 1.1. Page 27 explicitly keeps `IBIS-IP-VersionEnumeration` at `1.0`; document/data-definition revision and protocol version are distinct concepts.
2. Leading `–1:1` is treated as choice notation, not negative cardinality.
3. Hyphens produced by visible line wrapping are not automatically treated as XML-name characters. Only identifiers visibly intended as names and independently contradicted by XSD are retained.
4. A leading `+` in PDF type notation is not part of an XML QName; it denotes referenced structure/type notation in the document.
5. Enumeration order differences are ignored because order is not an XSD lexical constraint on the enumerated value set.
6. XSD-only internal/helper structures and the two XSD-only enum types are not automatically labelled PDF defects until downstream service context establishes whether the Common document was expected to expose them.
7. No XSD change is proposed. All executable differences remain diagnostics/findings candidates relative to the selected exact authority.

## Fresh-read freeze result

Nine independent observation groups are frozen. They distinguish the explicit 1.1 document-revision drift from additional identifier, choice, cardinality, service-model, ShortTrip and enumeration differences. Historical Common findings may now be opened only for deduplication and current-Evidence-Gate revalidation.
