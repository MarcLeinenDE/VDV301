# COMMON V2.4 - source-only Fresh Read freeze

Date: 2026-09-03  
State: **frozen before historical reconciliation**  
Finding IDs: intentionally not assigned in this file

## Evidence / authority

Official publication source:

- `COMMON_V2.4`
- VDV 301-2-1, 01/2023
- `https://www.vdv.de/301-2-1-sde-v2-4-commonstructure-enums.pdfx`
- SHA-256: `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`
- size: `1689647` bytes
- pages: `63`
- fulltext SHA-256: `02bfe01587937052f0d9b1c4a581a7a0546b6a3ca024de94310c6894646929b1`
- fresh retrieval/render run: `33658306978`
- job: `100342316111`
- artifact: `common-v24-pinned-read`, id `9857652638`
- all 63 rendered page hashes rechecked locally against the artifact manifest

Selected V2.4 schema lane for this read:

- `IBIS-IP_common_V2.4.xsd` blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`
- `IBIS-IP_Enumerations_V2.4.xsd` blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`
- Common includes `IBIS-IP_Enumerations_V2.4.xsd`
- bytes match `MarcLeinenDE/VDV301` branch `candidate/dms-v2.4-xsd` and open draft `VDVde/VDV301#31`
- authority: **candidate / integration**, not an official release-tag family
- no upstream tag `VDV-301-2.4` resolves
- upstream commit `14880bb33beec5c5dffe96315b730bd6c094a585` already references `IBIS-IP_common_V2.4.xsd` from TicketValidationService V2.4, but its tree contains neither Common V2.4 nor Enumerations V2.4
- `latest_xsd_wins: false`

The exact selected candidate family remains the validation authority for candidate-mode execution. This audit does not promote it to official-release authority and does not modify XSD bytes.

## Independence gate

Historical COMMON V2.4 deep-read/finding material was not opened while deriving the observation list below. Authority/provenance metadata and current branch state were inspected, but no historical COMMON V2.4 finding identities were used. The list below is therefore the immutable source-only input to historical reconciliation.

Complete document inventory was traversed: 64 Common data-structure sections (2.1-2.64) and 40 Common enumeration sections (3.1-3.40). Material candidates were checked against the rendered tables, including pages 17, 18, 20, 21, 26-30, 32, 34-35, 37-39, 41-45, 47, 49-50 and 55.

## Frozen observations

### FR-COM24-001 - InternationalTextType wrapper-type mismatch

PDF 1.17 documents:

- `Value` 1:1 `IBIS-IP.string`
- `Language` 1:1 `IBIS-IP.language`

Candidate XSD `InternationalTextType` uses flat native values:

- `Value` 1:1 `xs:string`
- `Language` 1:1 `xs:language`

### FR-COM24-002 - NetexMode choices are mandatory in PDF but optional in XSD

PDF 1.18 shows two `-1:1` choice blocks: main mode and submode. Under the project-wide choice-notation rule, `-1:1` denotes a mandatory one-of choice, not negative cardinality.

Candidate XSD `NetexMode` contains two `<xs:choice minOccurs="0">` groups. An empty `NetexMode` is therefore schema-valid although the PDF requires both choice decisions.

### FR-COM24-003 - AdditionalAnnouncement choice cardinality and branch name

PDF 2.1 shows a mandatory `-1:1` choice with branches:

- `ImmediateInformation`
- `PeriodicalInformation`
- `InformationAtSpecificPoint`

Candidate XSD uses `<xs:choice minOccurs="0">` and the third branch is named `SpecificPoint`.

### FR-COM24-004 - Connection mode multiplicity

PDF 2.8 documents both `TransportMode` and `ConnectionMode` as `0:*`.

Candidate XSD `ConnectionStructure` models both as `0:1`.

### FR-COM24-005 - DataAcceptedResponse compositor

PDF 2.9 presents `DataAcceptedResponseData` and `OperationErrorMessage` as ordinary `1:1` rows.

Candidate XSD `DataAcceptedResponseStructure` puts the two fields in an exclusive mandatory `xs:choice`.

### FR-COM24-006 - list minima PDF 1:* vs XSD 0:*

The following PDF list structures require at least one item, while the candidate XSD permits an empty list container:

- `DataVersionList.DataVersion`
- `DeviceSpecificationWithStateList.DeviceSpecificationWithState`
- `ServiceIdentificationWithStateList.ServiceIdentificationWithState`
- `ServiceSpecificationWithStateList.ServiceSpecificationWithState`

### FR-COM24-007 - field-cardinality differences

PDF vs candidate XSD:

- `JourneyStopInformation.Announcement`: PDF `0:*`, XSD `0:1`
- `JourneyStopInformation.FareZone`: PDF `0:*`, XSD `0:1`
- `StopInformationRequest.StopName`: PDF `0:1`, XSD `0:*`
- `TripInformation.AdditionalTextMessage`: PDF `0:*`, XSD base field `0:1`; PDF version history also says maxOccurs="unbounded"
- `UnsubscribeResponse.Active`: PDF `0:1`, XSD required `1:1`

V2.4 explicitly aligns `StopInformationRequest.ArrivalExpected` and `DepartureExpected`: both are present as optional fields in the PDF and candidate XSD. They are not part of this mismatch group.

### FR-COM24-008 - LineInformation LineName / LineShortName type and multiplicity

PDF 2.31 documents:

- `LineName` `0:1` `IBIS-IP.string`
- `LineShortName` `0:1` `IBIS-IP.string`

Candidate XSD `LineInformationStructure` models both as `InternationalTextType`, `minOccurs="0"`, `maxOccurs="unbounded"`.

This difference changes both XML shape/type and repeatability.

### FR-COM24-009 - case/spelling-sensitive XML identifiers

Rendered PDF tables and candidate XSD differ for:

- `FareZoneInformation`: PDF `FarezoneID`, `FarezoneType`, `FarezoneLongName`, `FarezoneShortName`; XSD `FareZoneID`, `FareZoneType`, `FareZoneLongName`, `FareZoneShortName`
- `GlobalCardStatus`: PDF `GlobalCardStatusID`; XSD `GlobalCardStausID`
- `LogMessage`: PDF `MessageBody`; XSD `Message`
- `TSPPoint`: PDF `Description`; XSD `Desciption`
- `ZoneType`: PDF `FarezoneTypeName`; XSD `FareZoneTypeName`

V2.4 corrections observed and excluded from this group:

- `BeaconPoint.Description` now aligns with the candidate XSD
- `SubscribeRequest.ReplyPath` aligns
- `UnsubscribeRequest.ReplyPath` aligns

### FR-COM24-010 - ServiceIdentification family substitutions

PDF 2.37 `ServiceIdentification` uses outer row `ServiceName` with type/reference `ServiceSpecification`; candidate XSD uses outer element `Service` of `ServiceSpecificationStructure`.

PDF 2.39 `ServiceIdentificationWithStateList` associates `ServiceIdentificationWithState` with `ServiceSpecificationWithState`; candidate XSD item type is `ServiceIdentificationWithStateStructure`.

### FR-COM24-011 - ShortTripStopList child element name

PDF 2.48 names the repeated child `ShortTripStopList` (`1:*`). Candidate XSD `ShortTripStopListStructure` names the child `ShortTripStop` (`1:*`).

### FR-COM24-012 - enumeration inventory mismatches

- PDF `DeviceStateEnumeration` omits `warning`; candidate XSD contains `warning`.
- PDF `ServiceNameEnumeration` still lists `SystemDocumentationService` and `SystemManagementService`; candidate XSD omits both and contains `SystemMonitoringService`.
- `AnalogRadioService` is present in both V2.4 PDF and candidate XSD and is not a mismatch.

### FR-COM24-013 - case/spelling-sensitive enumeration lexemes

PDF vs candidate XSD:

- `GNSSTypeEnumeration`: `Other` vs `other`
- `TicketValidationEnumeration`: `Valid` vs `valid`
- `VehicleModeEnumeration`: `Air` vs `air`
- `RailSubmodeEnumeration`: `specialRail` vs `specialTrain`
- `AirSubmodeEnumeration`: PDF omits candidate-XSD value `canalBarge`
- `FunicularSubmodeEnumeration`: `Unknown` vs `unknown`
- `TaxiSubmodeEnumeration`: `Unknown` vs `unknown`, `Undefined` vs `undefined`, and `minicab` vs `miniCab`

The V2.4 `DoorCountingObjectClassEnumeration` uses `Wheelchair` and `Other`, matching the candidate XSD; the older `WheelChair` difference is not present here.

### FR-COM24-014 - V2.4/version-history cross-reference residue

The V2.4 history records `StopPointNumber` as added to StopInformation, while the actual V2.4 table and candidate XSD use `PointNumber`.

The same history says `BlockNumber` was inserted in TripInformation `(2.58)`, while the actual V2.4 TripInformation section is 2.57 and 2.58 is TripSequence.

Inherited V2.3 history on the same publication likewise references TripInformation changes at 2.58 although the current TripInformation section is 2.57.

The line `LineSymbolCode renamed in LineInformation structure (2.31)` does not state the target name; the actual table/candidate XSD expose `LineSymbolText`.

### FR-COM24-015 - grouped documentation/editorial residue

Source-visible documentation issues retained as non-schema observations include:

- Table 52 caption says `Description of StopInformation` although section 2.52 is `StopPointTariffInformation`.
- section 2.5 heading is singular `CardApplInformation` while displayed structure/XSD type is plural `CardApplInformations`.
- section 3.13 heading/XSD use singular `GNSSCoordinateSystemEnumeration`, while the PDF table/caption uses plural `GNSSCoordinateSystemsEnumeration`.
- wording residue includes `dorr`, `Infromation`, and `WateSubmode`.
- NetexMode descriptions for `TaxiSubmode` and `SelfDriveSubmode` still say `sub type of air transportation`.

## Active falsification / aligned boundaries

The Fresh Read deliberately did not promote the following to findings:

- `-1:1` is XML choice notation, not an invalid negative cardinality.
- `PointType` shows a required one-of choice and aligns with XSD choice semantics.
- leading `+` denotes a referenced structure/type and is not a multiplicity marker.
- the 16 IBIS-IP primitive wrapper structures align in their ordinary Value/ErrorCode boundaries.
- `DisplayContent.AdditionalInformation` and `AdditionalInformation1..9` align in existence/repeatability direction.
- V2.4 `StopInformationRequest.ArrivalExpected` and `DepartureExpected` align with the candidate XSD.
- V2.4 `BeaconPoint.Description` aligns.
- V2.4 `DoorCountingObjectClassEnumeration.Wheelchair` aligns.
- `ReplyPath` in SubscribeRequest and UnsubscribeRequest aligns.
- enumeration ordering differences are ignored.
- no XSD modification is proposed or performed.

## Freeze

Frozen observation count: **15**.

Historical reconciliation may now map, merge, split or reject these observations only by explicit evidence. It must not silently alter the source-only observation text above. Any executable finding remains subject to the Evidence Gate and must be tested against the exact selected candidate blobs recorded above.
