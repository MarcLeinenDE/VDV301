# PDF/XSD semantic audit findings register

Status: started.

Important validation authority rule:

```text
Validation follows XSD.
PDF differences are recorded as explanatory/provider-facing notes, not as executable validation authority.
```

## Open findings

### CE-001 - Enumerations V2.3 file absent

State: unclear.

Observation:

```text
IBIS-IP_common_V2.3.xsd includes IBIS-IP_Enumerations_V2.2.xsd.
No IBIS-IP_Enumerations_V2.3.xsd is present in dev/schema-integration.
```

Impact:

```text
Low to medium until confirmed. If V2.3 did not introduce enumeration changes, this may be intentional. If V2.3 should have its own enumeration file, include/version handling needs correction.
```

Next action: check V2.3 PDF common enumeration tables and repository history before changing any include.

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
V2.4 version history says V2.2 removed SystemDocumentationService and SystemManagementService and added SystemMonitoringService.
The V2.4 ServiceNameEnumeration PDF table still lists SystemDocumentationService, SystemManagementService and SystemMonitoringService.
IBIS-IP_Enumerations_V2.4.xsd contains SystemMonitoringService but not SystemDocumentationService/SystemManagementService.
```

Impact:

```text
Payloads using the removed service names fail against XSD. Provider-facing note should explain the PDF table still lists them but XSD/version history do not.
```

Next action: check V2.2/V2.3 PDFs and repository history.

### CE-005 - TripInformation AdditionalTextMessage cardinality mismatch across V2.0 to V2.4

State: confirmed historical mismatch; do not auto-correct yet.

Observation:

```text
V2.4 consolidated PDF/history says TripInformation/AdditionalTextMessage allows 0:* / maxOccurs="unbounded".
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
VDV 301-2-1 V2.4 table 69 lists defective, notavailable, running, readyForShutdown.
IBIS-IP_Enumerations_V2.4.xsd additionally contains warning.
```

Impact: payloads using `warning` validate against XSD but are not visible in the V2.4 PDF table.

Next action: check earlier PDFs/XSDs and service-specific usage.

### CE-007 - Common enumeration case-sensitive PDF/XSD differences

State: confirmed PDF/XSD value discrepancies.

Observation:

```text
GNSSTypeEnumeration: PDF Other vs XSD other.
TicketValidationEnumeration: PDF Valid vs XSD valid.
VehicleModeEnumeration: PDF Air vs XSD air.
```

Impact:

```text
XML enumeration values are case-sensitive. PDF values listed above do not validate if used exactly as printed. Validation follows XSD.
```

Next action: check historical XSD values and examples.

### CE-008 - Submode enumeration case mismatches

State: confirmed PDF/XSD value discrepancies.

Observation:

```text
FunicularSubmodeEnumeration: PDF Unknown vs XSD unknown.
TaxiSubmodeEnumeration: PDF Unknown / Undefined / minicab vs XSD unknown / undefined / miniCab.
```

Impact: PDF spelling/case does not validate against XSD. Validation follows XSD.

Next action: check historical values and examples.

### CE-009 - RailSubmodeEnumeration specialRail vs specialTrain

State: confirmed PDF/XSD value discrepancy.

Observation:

```text
VDV 301-2-1 V2.4 RailSubmodeEnumeration table lists specialRail.
IBIS-IP_Enumerations_V2.4.xsd contains specialTrain.
```

Impact:

```text
specialRail does not validate against XSD; specialTrain validates but is not listed in the V2.4 PDF table.
```

Next action: check older Common/Enums PDFs/XSDs and external TPEG/NeTEx terminology.

### CE-010 - AirSubmodeEnumeration canalBarge XSD-only value

State: confirmed PDF/XSD value discrepancy.

Observation:

```text
VDV 301-2-1 V2.4 AirSubmodeEnumeration table does not list canalBarge.
IBIS-IP_Enumerations_V2.4.xsd contains canalBarge with an XSD annotation that it is not in TPEG.
```

Impact: `canalBarge` validates against current XSD but is not visible in the V2.4 PDF table.

Next action: check historical origin and whether intentionally retained as extension.

### CE-011 - Connection TransportMode / ConnectionMode cardinality PDF 0:* vs XSD 0:1

State: confirmed PDF/XSD cardinality discrepancy candidate.

Observation:

```text
VDV 301-2-1 V2.4 table 8 lists TransportMode 0:* and ConnectionMode 0:*.
IBIS-IP_common_V2.4.xsd contains both with minOccurs="0" but without maxOccurs, therefore maxOccurs="1" by XML Schema default.
```

Impact: repeated TransportMode/ConnectionMode entries fail against XSD although PDF table appears to allow them. Validation follows XSD.

Next action: check V2.2/V2.3 history.

### CE-012 - DeviceSpecificationWithStateList cardinality PDF 1:* vs XSD 0:*

State: confirmed PDF/XSD cardinality discrepancy candidate.

Observation:

```text
VDV 301-2-1 V2.4 table 18 lists DeviceSpecificationWithState 1:*.
IBIS-IP_common_V2.4.xsd contains DeviceSpecificationWithState minOccurs="0" maxOccurs="unbounded".
```

Impact: an empty DeviceSpecificationWithStateList may validate against XSD although PDF table indicates at least one entry. Validation follows XSD.

Next action: check historical XSD/PDF and DMS/SystemMonitoring usage.

### CE-013 - AdditionalAnnouncement third choice name and choice cardinality

State: confirmed PDF/XSD structure discrepancy candidate.

Observation:

```text
VDV 301-2-1 V2.4 table 1 lists the third AdditionalAnnouncement choice as InformationAtSpecificPoint with cardinality 1:1 +SpecificPoint.
IBIS-IP_common_V2.4.xsd defines an optional xs:choice with elements ImmediateInformation, PeriodicalInformation and SpecificPoint.
```

Impact:

```text
A payload using <InformationAtSpecificPoint> will fail against XSD; <SpecificPoint> is the XSD-valid element name. The XSD also allows omitting the entire choice because the choice has minOccurs="0".
```

Next action: check older PDF/XSD history before proposing correction.

### CE-014 - DataVersionList cardinality PDF 1:* vs XSD 0:*

State: confirmed PDF/XSD cardinality discrepancy candidate.

Observation:

```text
VDV 301-2-1 V2.4 table 12 lists DataVersion 1:*.
IBIS-IP_common_V2.4.xsd defines DataVersion with minOccurs="0" maxOccurs="unbounded".
```

Impact:

```text
An empty DataVersionList validates against XSD but appears disallowed by the PDF table. Validation follows XSD.
```

Next action: check historical schema and whether empty list is intentional for compatibility.

### CE-015 - FareZoneInformation element-name casing PDF vs XSD

State: potential PDF/XSD element-name discrepancy; visual PDF confirmation required before final classification.

Observation:

```text
PDF table extraction shows FarezoneID, FarezoneType, FarezoneLongName, FarezoneShortName.
IBIS-IP_common_V2.4.xsd uses FareZoneID, FareZoneType, FareZoneLongName, FareZoneShortName.
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
```

Impact:

```text
Payloads using GlobalCardStatusID as printed in the PDF fail against the XSD. The XSD-valid name is GlobalCardStausID, which appears typo-like but is technically authoritative for validation unless an official schema correction exists.
```

Next action: check historical XSD/PDF/fork origin before proposing correction.

### CE-017 - TSPPoint Desciption spelling candidate

State: confirmed XSD spelling observation; PDF visual confirmation required before final classification.

Observation:

```text
IBIS-IP_common_V2.4.xsd defines the TSPPoint text field as:
Desciption

The expected semantic spelling is Description, but the PDF-side table spelling still needs visual confirmation.
```

Impact:

```text
Payloads using <Description> will fail against the current XSD if the XSD only permits <Desciption>.
Payloads using <Desciption> validate against XSD but may look typo-like in provider discussions.
Validation follows XSD.
```

Next action: visually confirm the V2.4 PDF table and check historical XSD/PDF origin before proposing any correction.
