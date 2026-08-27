# PDF/XSD semantic audit findings register

Status: started.

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
Low to medium until confirmed.
If V2.3 did not introduce enumeration changes, this may be intentional.
If V2.3 should have its own enumeration file, include/version handling needs correction.
```

Next action:

```text
Check V2.3 PDF common enumeration tables and repository history before changing any include.
```

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
Do not rename XSD element based only on version-history wording.
Treat the table name and XSD name as aligned unless additional VDV evidence says otherwise.
```

Next action:

```text
Keep note in Common/Enums audit and revisit if service schemas or examples refer to StopPointNumber.
```

### CE-003 - V2.4 common/enums mostly promising, not closed

State: partial OK.

Observation:

```text
Main V2.4 additions observed so far are present in common/enums V2.4.
Full table-level cardinality and type comparison is still pending.
```

Next action:

```text
Continue table-level checks beyond the V2.4-changed areas: full datatype, structure and enumeration pass.
```

### CE-004 - ServiceNameEnumeration V2.4 PDF table vs XSD/version-history discrepancy

State: confirmed PDF/XSD table discrepancy; likely documentation/table inconsistency, not an immediate XSD defect.

Observation:

```text
V2.4 version history says V2.2 removed SystemDocumentationService and SystemManagementService
and added SystemMonitoringService.

The V2.4 ServiceNameEnumeration PDF table still lists SystemDocumentationService,
SystemManagementService and SystemMonitoringService.

IBIS-IP_Enumerations_V2.4.xsd contains SystemMonitoringService but does not contain
SystemDocumentationService or SystemManagementService.
```

Impact:

```text
The XSD follows the version-history statement but not the still-visible enumeration table.
For tool output, do not silently call either representation definitively official without noting the conflict.
```

Next action:

```text
Check V2.2/V2.3 PDFs and official repository history, then decide whether this should be
reported as documentation inconsistency or tracked as a schema issue.
```

### CE-005 - TripInformation AdditionalTextMessage cardinality mismatch across V2.0 to V2.4

State: confirmed historical mismatch; do not auto-correct yet.

Observation:

```text
The V2.4 consolidated PDF history says that in V2.0 TripInformation/AdditionalTextMessage
was updated to maxOccurs="unbounded".

The current V2.4 TripInformation table states:

AdditionalTextMessage     0:* +InternationalTextType
AdditionalTextMessage(n)  0:* +InternationalTextType, n = 1 to 9

XSD history in dev/schema-integration:

V1.0: AdditionalTextMessage type IBIS-IP.string, minOccurs="0", no maxOccurs.
V2.0: AdditionalTextMessage type InternationalTextType, minOccurs="0", no maxOccurs.
V2.1: same as V2.0.
V2.2: same as V2.0.
V2.3: AdditionalTextMessage plus AdditionalTextMessage1..9, all minOccurs="0", no maxOccurs.
V2.4: same as V2.3.
```

Impact:

```text
Current XSD validation allows at most one occurrence of each named AdditionalTextMessage field.
The PDF appears to allow repeated elements. Therefore repeated AdditionalTextMessage payloads
may be valid according to the PDF table but invalid against the current XSD pool.
```

Next action:

```text
Check examples, upstream/fork history and consumer practice before changing any XSD.
If fixed, scope it as a separate schema-correction candidate and do not mix it into the DMS V2.4 PR.
```

### CE-006 - DeviceStateEnumeration contains XSD-only warning value

State: confirmed PDF/XSD table discrepancy.

Observation:

```text
VDV 301-2-1 V2.4 table 69 lists:
defective, notavailable, running, readyForShutdown.

IBIS-IP_Enumerations_V2.4.xsd contains the additional value:
warning.
```

Impact:

```text
A payload using warning validates against the XSD but is not visible in the V2.4 PDF table.
```

Next action:

```text
Check earlier Common/Enums PDFs and service-specific usage before classifying as schema defect or PDF omission.
```

### CE-007 - Common enumeration case-sensitive PDF/XSD differences

State: confirmed PDF/XSD value discrepancies.

Observation:

```text
GNSSTypeEnumeration:
PDF Other vs XSD other.

TicketValidationEnumeration:
PDF Valid vs XSD valid.

VehicleModeEnumeration:
PDF Air vs XSD air.
```

Impact:

```text
XML enumeration values are case-sensitive. The PDF values listed above do not validate against the XSD values if used exactly as printed.
```

Next action:

```text
Check historical XSD values and examples before deciding whether the PDF or XSD should be treated as authoritative for documentation.
For actual XML validation, the tool must follow XSD values.
```

### CE-008 - Submode enumeration case mismatches

State: confirmed PDF/XSD value discrepancies.

Observation:

```text
FunicularSubmodeEnumeration:
PDF Unknown vs XSD unknown.

TaxiSubmodeEnumeration:
PDF Unknown / Undefined / minicab
vs XSD unknown / undefined / miniCab.
```

Impact:

```text
All observed differences are case-sensitive. Payloads using the PDF spelling would not validate against the current XSD values.
```

Next action:

```text
Check historical XSD values and examples before deciding whether the PDF or XSD should be treated as authoritative for documentation.
For actual XML validation, the tool must follow XSD values.
```

### CE-009 - RailSubmodeEnumeration specialRail vs specialTrain

State: confirmed PDF/XSD value discrepancy.

Observation:

```text
VDV 301-2-1 V2.4 RailSubmodeEnumeration table lists:
specialRail.

IBIS-IP_Enumerations_V2.4.xsd contains:
specialTrain.
```

Impact:

```text
This is not a case-only difference. Payloads using specialRail according to the PDF table
will not validate against the current XSD; payloads using specialTrain validate but are not
listed in the V2.4 PDF table.
```

Next action:

```text
Check earlier Common/Enums PDFs/XSDs and external TPEG/NeTEx terminology before proposing a correction.
```

### CE-010 - AirSubmodeEnumeration canalBarge XSD-only value

State: confirmed PDF/XSD value discrepancy.

Observation:

```text
VDV 301-2-1 V2.4 AirSubmodeEnumeration table does not list canalBarge.

IBIS-IP_Enumerations_V2.4.xsd contains:
canalBarge
with an XSD annotation that it is not in TPEG.
```

Impact:

```text
Payloads using canalBarge validate against the current XSD but are not visible in the V2.4 PDF table.
```

Next action:

```text
Check historical XSD/fork origin and whether the value is intentionally retained as an extension.
```
