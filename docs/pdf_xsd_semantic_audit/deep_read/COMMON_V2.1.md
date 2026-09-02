# Common Data Structures and Enumerations V2.1 — Deep Read Pass 2

Status: independent COMMON V2.1 source read and targeted pinned-byte visual falsification complete; fresh observations frozen before historical reconciliation.

## Source and authority boundary

- Official publication: VDV-Schrift 301-2-1, Common Data Structures and Enumerations V2.1, 07/2018.
- Official URL: https://www.vdv.de/301-2-1-sds-v2-1-commonstructure-enums.pdfx
- PDF SHA-256: `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32`.
- PDF size: `1274051` bytes.
- Recovery pin run: `33608210402`; prior retained evidence run: `33393002497`.
- Recovery pin time: `2026-09-02T08:20:57Z`. The original 2026-08-31 pin timestamp could not be reconstructed from the retained artifact; the 2026-09-02 retrieval was byte-identical to the retained source evidence.
- Exact executable XSD authority: official tag `VDV-301-2.1`.
- `IBIS-IP_common_V2.1.xsd` blob: `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e`.
- `IBIS-IP_Enumerations_V2.1.xsd` blob: `311464690ad60749ed8d326217787e4b8ed0b718`.
- Integration-branch bytes match the exact official tag.
- No latest-XSD substitution is permitted and no XSD is modified by this audit.

## Render/read evidence

- Exact pinned-byte artifact: run `33608210402`, artifact `common-v21-recovery-read`, artifact id `9837875704`.
- Artifact digest: `sha256:f76b9cbc078edbe4646bf8d8754d486e6046bda460f885a7d52889c78a29ee34`.
- PDF pages: `48`; all pages rendered at 120 dpi.
- Extracted full-text SHA-256: `5dce4c8ecc770574bdce8d5961fefbc01f88b1547e3957855013d9b077fc24b0`.
- Local recheck confirmed all 48 PNG page hashes against the artifact manifest.
- Complete extracted text was read across all 48 pages.
- Targeted visible falsification covered pages 12, 15-18, 20, 23-24, 26-42 where material table, choice, cardinality, spelling/case, enumeration, or version-history observations occur.

## Independence boundary and procedural note

The observation set below was derived from the exact COMMON V2.1 PDF and exact official V2.1 XSD family without using historical COMMON finding IDs to construct it.

During preparation of the repository freeze, `CURRENT_STATE.json` exposed historical COMMON V2.0 finding metadata after the independent V2.1 observation list had already been completed, but before the formal freeze commit was written. No historical ID, description, or prior result was used to add, remove, merge, split, or rewrite the frozen V2.1 observations below. This late metadata exposure is recorded here rather than hidden. Historical reconciliation begins only after this freeze and must revalidate each mapping under the current Evidence Gate.

## Independent observations

### FR-COM21-OBS-001 — InternationalTextType table and XSD use different member types

Page 12 defines `InternationalTextType.Value` as `IBIS-IP.string` and `Language` as `IBIS-IP.language`. Those PDF types are wrapper structures defined elsewhere in the same document.

The exact V2.1 XSD instead declares `Value` directly as `xs:string` and `Language` directly as `xs:language`, with `ErrorCode` as the optional third child of `InternationalTextType`. A literal PDF-shaped instance would therefore have a different nesting model from the authoritative XSD.

### FR-COM21-OBS-002 — AdditionalAnnouncement choice differs in optionality and specific-point child name

Page 15 visibly presents a `choice` with `ImmediateInformation`, `PeriodicalInformation`, and `InformationAtSpecificPoint`; the choice notation shows the first branch as `-1:1`, i.e. XML-choice notation rather than a negative cardinality.

The exact V2.1 XSD uses `<xs:choice minOccurs="0">`, so the entire choice may be absent, and names the third branch `SpecificPoint`, not `InformationAtSpecificPoint`. Both facets are retained as one structure-level observation.

### FR-COM21-OBS-003 — BeaconPoint uses Description in the PDF but Desciption in the XSD

Page 16 visibly names the optional repeatable member `Description`. The exact V2.1 XSD spells the element `Desciption`. XML element names are case- and spelling-sensitive, so the forms are not interchangeable.

### FR-COM21-OBS-004 — DataAcceptedResponse required-pair table conflicts with XSD exclusive choice

Page 17 visibly lists both `DataAcceptedResponseData 1:1` and `OperationErrorMessage 1:1` as ordinary rows and does not present a choice heading.

The exact V2.1 XSD defines `DataAcceptedResponseStructure` as an `xs:choice` between those two elements. The PDF-shaped form requires both; the authoritative XSD accepts exactly one.

### FR-COM21-OBS-005 — Four list structures are 1:* in the PDF but 0:* in the XSD

The PDF visibly specifies at least one item for:
- page 18 `DataVersionList/DataVersion`;
- page 20 `DeviceSpecificationWithStateList/DeviceSpecificationWithState`;
- page 26 `ServiceIdentificationWithStateList/ServiceIdentificationWithState`;
- page 27 `ServiceSpecificationWithStateList/ServiceSpecificationWithState`.

The exact V2.1 XSD gives each corresponding list member `minOccurs="0" maxOccurs="unbounded"`. Therefore empty list containers validate in XSD although the PDF tables require one or more entries.

### FR-COM21-OBS-006 — FareZoneInformation element-name casing differs

Page 23 visibly uses `FarezoneID`, `FarezoneType`, `FarezoneLongName`, and `FarezoneShortName`.

The exact V2.1 XSD uses `FareZoneID`, `FareZoneType`, `FareZoneLongName`, and `FareZoneShortName`. All four are case-sensitive XML element-name differences.

### FR-COM21-OBS-007 — GlobalCardStatusID differs from XSD GlobalCardStausID

Page 23 visibly names the required element `GlobalCardStatusID`. The exact V2.1 XSD names it `GlobalCardStausID`. The XSD spelling is authoritative for XML validation even though the PDF spelling is linguistically plausible.

### FR-COM21-OBS-008 — JourneyStopInformation Announcement and FareZone multiplicities differ

Page 24 visibly specifies `Announcement 0:*` and `FareZone 0:*`.

The exact V2.1 XSD declares both with `minOccurs="0"` and no `maxOccurs`, hence `0:1`. Other nearby repeatable fields such as `Connection` do have `maxOccurs="unbounded"`, so this is not inferred from a general table convention.

### FR-COM21-OBS-009 — LogMessage child is MessageBody in the PDF but Message in the XSD

Page 24 visibly defines the second required `LogMessage` member as `MessageBody`, type `Message`.

The exact V2.1 XSD defines the child element itself as `Message`, type `MessageStructure`. The type concept aligns; the child element name does not.

### FR-COM21-OBS-010 — ServiceIdentification child is ServiceName in the PDF but Service in the XSD

Page 26 visibly defines `ServiceIdentification` with required children `ServiceName` and `Device`; `ServiceName` is typed as `ServiceSpecification`.

The exact V2.1 XSD instead defines the first child as `Service`, type `ServiceSpecificationStructure`. The type concept aligns, while the XML child name differs.

### FR-COM21-OBS-011 — ServiceIdentificationWithStateList shows the wrong referenced structure type

Page 26 visibly types the list member `ServiceIdentificationWithState` as `ServiceSpecificationWithState`.

The exact V2.1 XSD types it as `ServiceIdentificationWithStateStructure`. This is separate from the 1:* versus 0:* list-minimum mismatch captured in FR-COM21-OBS-005.

### FR-COM21-OBS-012 — ShortTripStopList repeats its container name as the child name

Page 28 visibly names the repeated child of `ShortTripStopList` as `ShortTripStopList`, while the displayed type is `ShortTripStop`.

The exact V2.1 XSD names the repeated child `ShortTripStop`. The PDF therefore has a child-name defect while its referenced structure concept is otherwise aligned.

### FR-COM21-OBS-013 — StopInformationRequest.StopName is 0:1 in the PDF but 0:* in the XSD

Page 29 visibly specifies `StopName 0:1` in `StopInformationRequest`.

The exact V2.1 XSD declares `StopName` with `minOccurs="0" maxOccurs="unbounded"`. This does not affect `StopInformation.StopName`, which is 1:* in both sources.

### FR-COM21-OBS-014 — SubscribeRequest and UnsubscribeRequest use Reply-Path versus XSD ReplyPath

Pages 30 and 32 visibly name the optional child `Reply-Path`.

The exact V2.1 XSD names the child `ReplyPath` in both request structures. `Client-IP-Address` remains hyphenated in both PDF and XSD, so the `Reply-Path` discrepancy cannot be dismissed as a global punctuation-normalization convention.

### FR-COM21-OBS-015 — TripInformation.AdditionalTextMessage contradicts both the XSD and the PDF's own version history

Page 31 visibly specifies `AdditionalTextMessage 0:*`.

Page 41 explicitly states in the Version 2.0 technical corrections that `TripInformation structure: AdditionalTextMessage: maxOccurs="unbounded" updated`.

Nevertheless the exact V2.1 XSD still declares `AdditionalTextMessage` only with `minOccurs="0"` and no `maxOccurs`, hence `0:1`. The mismatch is therefore supported by both the V2.1 structure table and the document's own historical correction statement.

### FR-COM21-OBS-016 — TSPPoint uses Description in the PDF but Desciption in the XSD

Page 31 visibly names the optional repeatable member `Description`. The exact V2.1 XSD spells the element `Desciption`.

### FR-COM21-OBS-017 — ZoneType uses FarezoneTypeName in the PDF but FareZoneTypeName in the XSD

Page 33 visibly names the optional repeatable element `FarezoneTypeName`. The exact V2.1 XSD uses `FareZoneTypeName`.

The neighboring `FarezoneTypeID` spelling is identical in PDF and XSD; only the `TypeName` element has this case-boundary difference.

### FR-COM21-OBS-018 — Enumeration lexical boundaries differ in four enumeration families

Visible PDF/XSD lexeme differences are:
- page 35 `DoorCountingObjectClassEnumeration`: PDF `Wheelchair` versus XSD `WheelChair`, and PDF `Others` versus XSD `Other`;
- page 37 `GNSSTypeEnumeration`: PDF `Other` versus XSD `other`;
- page 39 `TicketValidationEnumeration`: PDF `Valid` versus XSD `valid`;
- page 39 `VehicleModeEnumeration`: PDF `Air` versus XSD `air`.

Enumeration order differences are explicitly ignored. Only case/plural-sensitive lexical differences are retained.

### FR-COM21-OBS-019 — GNSS coordinate-system enumeration name is internally inconsistent

Section 3.13 and the exact V2.1 XSD use singular `GNSSCoordinateSystemEnumeration`.

The visible table body and table caption on page 36 use plural `GNSSCoordinateSystemsEnumeration`; the table index on page 46 repeats the plural form. The possible values themselves align. This is retained as a documentation identifier inconsistency, not as an XSD-value defect.

### FR-COM21-OBS-020 — grouped cross-reference/table-caption editorial residue

Independent low-severity editorial residue includes:
- page 19 `DeviceInformation.DeviceClass` and `DeviceSpecification.DeviceClass` refer to section `3.3`, while `DeviceClassEnumeration` is section `3.4`;
- page 27 `ServiceSpecification.ServiceName` says `(cf. 0)`;
- page 28 `ShortTripStop.FareZoneInformation` refers to `2.52`, while `FareZoneInformation` is section `2.26`;
- page 30 Table 52 is the `StopPointTariffInformation` table but is captioned `Description of StopInformation`; the table index on page 45 repeats that caption.

These are documentation navigation/editorial defects and are not promoted to executable XML-shape findings by themselves.

## Active falsification and rejected suspicions

1. **No negative-cardinality finding.** The leading minus in `-1:1` on pages 15, 25, 30, and 32 is VDV XML-choice notation. It is not treated as a negative or invalid cardinality.
2. **PointType choice aligns.** Page 25's five alternatives correspond to the exact V2.1 `xs:choice` members `StopPoint`, `BeaconPoint`, `GNSSLocationPoint`, `TimingPoint`, and `TSPPoint`.
3. **SubscribeResponse and UnsubscribeResponse choices align.** The visible `Active`/`OperationErrorMessage` alternatives match the exact V2.1 XSD choices; only request-side `Reply-Path` naming is retained.
4. **Connection multiplicities align.** Page 17 `DisplayContent 0:1`, `Platform 0:1`, `ConnectionState 0:1`, `TransportMode 0:1`, `ExpectedDepartureTime 0:1`, and `ScheduledDepartureTime 0:1` match the XSD.
5. **StopInformation is not conflated with JourneyStopInformation or StopInformationRequest.** Its repeatable `StopName`, `StopAnnouncement`, `Connection`, and `FareZone` declarations align with the XSD.
6. **PointSequence minimum aligns.** Page 25 and the XSD both require at least two `Point` entries.
7. **ServiceInformationList and ServiceStartList minimums align.** Both PDF and XSD require one or more entries, so they are excluded from FR-COM21-OBS-005.
8. **V2.1 service-name additions align.** The page 38 service enumeration contains the V2.1 additions named in the version history, and the exact V2.1 enumeration XSD contains the same lexemes.
9. **Most enumerations align.** Ordering differences are not treated as defects; the four lexical families in FR-COM21-OBS-018 are retained because XML enumeration values are exact strings.
10. **Inline-formatting markup is not treated as undeclared XML children.** Pages 12-14 explicitly require formatting markup to be escaped before insertion into `Value`; it is therefore string content, not schema child elements.

## Fresh-read freeze result

Twenty independent observations are frozen:
- 18 structure/type/cardinality/name/lexeme observations with potential XML or validator relevance;
- one documentation identifier inconsistency;
- one grouped editorial/cross-reference observation.

These are fresh observations, not yet historical finding mappings. Executable positive/negative evidence is still required where it is sensible before any observation is promoted or revalidated as a confirmed finding under the Evidence Gate.

No XSD was changed. The exact `VDV-301-2.1` XSD family remains the executable validation authority. Historical COMMON findings may now be reopened only for deduplication, mapping, falsification, and Evidence-Gate revalidation.
