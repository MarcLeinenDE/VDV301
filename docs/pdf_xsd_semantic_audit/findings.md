# PDF/XSD semantic audit findings register

Status: started.

Important validation authority rule:

```text
Validation follows XSD.
PDF differences are recorded as explanatory/provider-facing notes, not as executable validation authority.
```

Historical consolidation note:

```text
Common/Enums historical first-pass chain V1.0/V1.x -> V2.4 is complete in files 04a through 04e.
CE-001 is closed as OK with note by 04e.
Affected-version ranges for CE-004 through CE-017 are supported by the history files but should still be used conservatively until local XSD compile/sample validation is run.
```

## Open findings

### CE-001 - Enumerations V2.3 file absent

State: OK with note.

Observation:

```text
IBIS-IP_common_V2.3.xsd includes IBIS-IP_Enumerations_V2.2.xsd.
No IBIS-IP_Enumerations_V2.3.xsd is present in dev/schema-integration.
The V2.3 PDF history records structure additions, not enumeration additions.
```

Impact:

```text
This is no longer treated as an unclear defect.
The selected V2.3 dependency pool is Common V2.3 + Enumerations V2.2.
Do not create an IBIS-IP_Enumerations_V2.3.xsd only for version-number symmetry.
Do not substitute Enumerations V2.4 when validating V2.3 payloads unless the selected service schema explicitly requires it.
```

Next action: carry this dependency fact into the executable version/dependency validation matrix.

### CE-002 - V2.4 StopPointNumber wording vs PointNumber table/XSD

State: OK with note.

Observation:

```text
V2.4 version history says StopPointNumber inserted in StopInformation.
The actual V2.4 StopInformation table uses PointNumber.
IBIS-IP_common_V2.4.xsd uses PointNumber.
```

Impact:

```text
Do not rename XSD element based only on version-history wording. Treat table name and XSD name as aligned unless additional VDV evidence says otherwise.
```

Next action: keep note and revisit if service schemas or examples refer to StopPointNumber.

### CE-003 - V2.4 common/enums mostly promising, not closed

State: partial OK.

Observation:

```text
Main V2.4 additions observed so far are present in common/enums V2.4.
Full table-level cardinality and type comparison is still pending.
```

Next action: continue table-level checks beyond affected areas.

### CE-004 - ServiceNameEnumeration V2.4 PDF table vs XSD/version-history discrepancy

State: confirmed PDF/XSD table discrepancy; likely documentation/table inconsistency, not an immediate XSD defect.

Observation:

```text
V2.2 history says SystemDocumentationService and SystemManagementService were removed and SystemMonitoringService was added.
The V2.2/V2.3/V2.4 PDF tables still list SystemDocumentationService and SystemManagementService.
IBIS-IP_Enumerations_V2.2/V2.4 contain SystemMonitoringService but not SystemDocumentationService/SystemManagementService.
```

Impact:

```text
Payloads using the removed service names fail against XSD. Provider-facing note should explain the PDF table still lists them but XSD/version history do not.
```

Next action: local validation sample for removed values in V2.2+ pools.

### CE-005 - TripInformation AdditionalTextMessage cardinality mismatch across V2.0 to V2.4

State: confirmed historical mismatch; do not auto-correct yet.

Observation:

```text
V2.0+ PDF/history says TripInformation/AdditionalTextMessage allows 0:* / maxOccurs="unbounded".
XSD history in dev/schema-integration:
V1.0: AdditionalTextMessage type IBIS-IP.string, minOccurs="0", no maxOccurs.
V2.0-V2.2: AdditionalTextMessage type InternationalTextType, minOccurs="0", no maxOccurs.
V2.3-V2.4: AdditionalTextMessage plus AdditionalTextMessage1..9, all minOccurs="0", no maxOccurs.
```

Impact:

```text
Repeated AdditionalTextMessage payloads may be valid according to PDF table but invalid against current XSD pool. Validation follows XSD.
```

Next action: check examples, upstream/fork history and consumer practice before any correction.

### CE-006 - DeviceStateEnumeration contains XSD-only warning value

State: confirmed PDF/XSD table discrepancy.

Observation:

```text
DeviceStateEnumeration warning is present in V2.2+ XSD pools.
The checked V2.2/V2.3/V2.4 PDF tables list defective, notavailable, running, readyForShutdown, but do not list warning.
```

Impact: payloads using `warning` validate against XSD but are not visible in the checked PDF tables.

Next action: service-specific usage and local validation sample.

### CE-007 - Common enumeration case-sensitive PDF/XSD differences

State: confirmed PDF/XSD value discrepancies.

Observation:

```text
GNSSTypeEnumeration: PDF Other vs XSD other.
TicketValidationEnumeration: PDF Valid vs XSD valid.
VehicleModeEnumeration: PDF Air vs XSD air.
Historical first-pass support exists from V1.x/V2.0 through V2.4 for the checked values.
```

Impact:

```text
XML enumeration values are case-sensitive. PDF values listed above do not validate if used exactly as printed. Validation follows XSD.
```

Next action: local validation samples per version pool.

### CE-008 - Submode enumeration case mismatches

State: confirmed PDF/XSD value discrepancies.

Observation:

```text
FunicularSubmodeEnumeration: PDF Unknown vs XSD unknown.
TaxiSubmodeEnumeration: PDF Unknown / Undefined / minicab vs XSD unknown / undefined / miniCab.
These are supported from the V2.2 NetexMode/submode introduction through V2.4 in the historical first-pass chain.
```

Impact: PDF spelling/case does not validate against XSD. Validation follows XSD.

Next action: local validation samples per version pool.

### CE-009 - RailSubmodeEnumeration specialRail vs specialTrain

State: confirmed PDF/XSD value discrepancy.

Observation:

```text
VDV 301-2-1 V2.2+ RailSubmodeEnumeration tables list specialRail.
IBIS-IP_Enumerations_V2.2/V2.4 contain specialTrain.
```

Impact:

```text
specialRail does not validate against XSD; specialTrain validates but is not listed in the checked PDF tables.
```

Next action: check external TPEG/NeTEx terminology only as background, not as replacement authority.

### CE-010 - AirSubmodeEnumeration canalBarge XSD-only value

State: confirmed PDF/XSD value discrepancy.

Observation:

```text
VDV 301-2-1 V2.4 AirSubmodeEnumeration table does not list canalBarge.
IBIS-IP_Enumerations_V2.4.xsd contains canalBarge with an XSD annotation that it is not in TPEG.
The value is introduced/observed in the V2.4 XSD side of this audit chain.
```

Impact: `canalBarge` validates against V2.4 XSD but is not visible in the V2.4 PDF table.

Next action: local V2.4 validation sample and final PR-candidate review only after full audit.

### CE-011 - Connection TransportMode / ConnectionMode cardinality PDF 0:* vs XSD 0:1

State: confirmed PDF/XSD cardinality discrepancy candidate.

Observation:

```text
VDV 301-2-1 V2.4 table 8 lists TransportMode 0:* and ConnectionMode 0:*.
IBIS-IP_common_V2.4.xsd contains both with minOccurs="0" but without maxOccurs, therefore maxOccurs="1" by XML Schema default.
The same XSD modelling is already visible from the V2.2 introduction of ConnectionMode.
```

Impact: repeated TransportMode/ConnectionMode entries fail against XSD although PDF table appears to allow them. Validation follows XSD.

Next action: local repeated-element negative sample for V2.2+ pools.

### CE-012 - DeviceSpecificationWithStateList cardinality PDF 1:* vs XSD 0:*

State: confirmed PDF/XSD cardinality discrepancy candidate.

Observation:

```text
VDV 301-2-1 V2.4 table 18 lists DeviceSpecificationWithState 1:*.
IBIS-IP_common_V2.4.xsd contains DeviceSpecificationWithState minOccurs="0" maxOccurs="unbounded".
```

Impact: an empty DeviceSpecificationWithStateList may validate against XSD although PDF table indicates at least one entry. Validation follows XSD.

Next action: check service usage and local validation sample.

### CE-013 - AdditionalAnnouncement third choice name and choice cardinality

State: confirmed PDF/XSD structure discrepancy candidate.

Observation:

```text
VDV 301-2-1 V2.4 table 1 lists the third AdditionalAnnouncement choice as InformationAtSpecificPoint with cardinality 1:1 +SpecificPoint.
IBIS-IP_common_V2.4.xsd defines an optional xs:choice with elements ImmediateInformation, PeriodicalInformation and SpecificPoint.
The XSD form is present throughout checked Common history.
```

Impact:

```text
A payload using <InformationAtSpecificPoint> will fail against XSD; <SpecificPoint> is the XSD-valid element name. The XSD also allows omitting the entire choice because the choice has minOccurs="0".
```

Next action: local positive/negative XML samples.

### CE-014 - DataVersionList cardinality PDF 1:* vs XSD 0:*

State: confirmed PDF/XSD cardinality discrepancy candidate.

Observation:

```text
VDV 301-2-1 V2.4 table 12 lists DataVersion 1:*.
IBIS-IP_common_V2.4.xsd defines DataVersion with minOccurs="0" maxOccurs="unbounded".
The permissive XSD form is visible throughout checked Common history.
```

Impact:

```text
An empty DataVersionList validates against XSD but appears disallowed by the PDF table. Validation follows XSD.
```

Next action: local validation sample and service-impact review.

### CE-015 - FareZoneInformation element-name casing PDF vs XSD

State: potential PDF/XSD element-name discrepancy; visual PDF confirmation required before final classification.

Observation:

```text
PDF table extraction shows FarezoneID, FarezoneType, FarezoneLongName, FarezoneShortName.
IBIS-IP_common_V2.4.xsd uses FareZoneID, FareZoneType, FareZoneLongName, FareZoneShortName.
ZoneType uses FarezoneTypeID and FareZoneTypeName mixed casing in XSD.
```

Impact if confirmed:

```text
Element names are case-sensitive. FarezoneID/FarezoneType would fail against XSD; FareZoneID/FareZoneType validate.
```

Next action: visually confirm the PDF table, because extraction/table layout may affect casing.

### CE-016 - GlobalCardStatusID vs GlobalCardStausID spelling difference

State: confirmed PDF/XSD spelling discrepancy candidate.

Observation:

```text
VDV 301-2-1 V2.4 table 27 lists GlobalCardStatusID.
IBIS-IP_common_V2.4.xsd defines GlobalCardStausID.
The typo-like XSD spelling is observed at least in the V2.3/V2.4 XSD path.
```

Impact:

```text
Payloads using GlobalCardStatusID as printed in the PDF fail against the XSD. The XSD-valid name is GlobalCardStausID, which appears typo-like but is technically authoritative for validation unless an official schema correction exists.
```

Next action: local validation sample and post-audit PR-candidate review.

### CE-017 - TSPPoint Desciption spelling candidate

State: confirmed XSD spelling observation; PDF visual confirmation required before final classification.

Observation:

```text
IBIS-IP_common_V2.3.xsd and IBIS-IP_common_V2.4.xsd define the TSPPoint text field as:
Desciption

BeaconPoint was corrected to Description in V2.4, but TSPPoint remains Desciption.
The expected semantic spelling is Description, but the PDF-side table spelling still needs visual confirmation.
```

Impact:

```text
Payloads using <Description> will fail against the current XSD if the XSD only permits <Desciption>.
Payloads using <Desciption> validate against XSD but may look typo-like in provider discussions.
Validation follows XSD.
```

Next action: visually confirm the V2.4 PDF table and keep for post-audit PR-candidate review.

## CustomerInformationService findings

### CIS-001 - V1.1 public PDF without confirmed version-exact XSD mapping

State: unresolved provenance / validation-routing gap.

Observation:

```text
The public VDV page lists CustomerInformationService V1.1.
No version-exact IBIS-IP_CustomerInformationService_V1.1.xsd has been confirmed in the checked source set.
Official release-tag backfill found CIS V1.0, CIS V2.0 and CIS V2.2 service XSDs, but not a separate CIS V1.1 service XSD.
```

Impact:

```text
Do not silently validate CIS V1.1 traffic against CIS V1.0 or CIS V2.0.
For a future tool/SDK, CIS V1.1 must remain public-PDF-known but exact-XSD-mapping-open until publication/release context is resolved.
```

Next action: resolve CIS V1.1 release/publication context before claiming strict XSD validation for V1.1.

### CIS-002 - PDF Subscribe/Unsubscribe operations vs service-XSD operation group modelling

State: OK with note / cross-service modelling check pending.

Observation:

```text
The CIS V2.0/V2.2/V2.3 PDFs list service-specific Get, Subscribe and Unsubscribe operation concepts.
The checked CIS V2.x service XSD operation group contains the concrete Get response elements and RetrievePartialStopSequence request/response elements, but not service-specific Subscribe/Unsubscribe elements.
```

Impact:

```text
This is not treated as a CIS schema defect at this stage.
Subscribe/Unsubscribe may be modelled generically outside the local CIS operation group.
Validation follows the selected XSD family.
```

Next action: perform a cross-service subscription modelling review before classifying this as anything stronger than a provider-facing note.

### CIS-003 - GetCurrentConnectionInformation naming vs GetCurrentConnectionResponse table wording

State: PDF label inconsistency candidate.

Observation:

```text
The operation naming in the checked CIS V2.x material uses GetCurrentConnectionInformation in the operation overview and CustomerInformationService.GetCurrentConnectionInformationResponse in XSD.
Some PDF table wording appears as GetCurrentConnectionResponse / CurrentConnectionData in the detailed structure area.
```

Impact:

```text
Do not rename the XSD based on shorter PDF table wording.
The XSD-valid operation element is CustomerInformationService.GetCurrentConnectionInformationResponse.
```

Next action: keep as provider-facing naming note; no schema correction proposed.

### CIS-004 - RetrievePartialStopSequence naming vs RetrievePartialStopRequest table wording

State: PDF label inconsistency candidate.

Observation:

```text
The operation overview and XSD use RetrievePartialStopSequence.
Some PDF detail-table wording appears as RetrievePartialStopRequest.
The XSD-valid request element is CustomerInformationService.RetrievePartialStopSequenceRequest.
```

Impact:

```text
Do not rename the XSD based on shorter PDF table wording.
The XSD-valid element names remain RetrievePartialStopSequenceRequest and RetrievePartialStopSequenceResponse.
```

Next action: keep as provider-facing naming note; no schema correction proposed.

### CIS-005 - MyOwnVehicleMode type differs between CIS PDF tables and XSD shared group

State: confirmed PDF/XSD documentation discrepancy candidate; likely PDF table inconsistency, not an immediate XSD defect.

Observation:

```text
In the checked CIS V2.2/V2.3 PDF tables, MyOwnVehicleMode is shown as NetexMode in the AllData context but as PtModesEnumeration in the VehicleData context.
The CIS V2.2/V2.3 XSDs use a shared VehicleInformationGroup for AllData and VehicleData.
In that XSD group, MyOwnVehicleMode has type NetexMode.
```

Impact:

```text
Validation follows the XSD: MyOwnVehicleMode is validated as NetexMode in the checked V2.2/V2.3 service schema family.
A provider following the PtModesEnumeration table wording may fail strict XSD validation.
```

Next action: add local sample validation and include CIS-005 in post-audit review before considering any official-facing clarification or correction proposal.
