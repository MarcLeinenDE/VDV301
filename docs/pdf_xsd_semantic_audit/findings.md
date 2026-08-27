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

State: discrepancy noted; likely documentation/table inconsistency, not an immediate XSD defect.

Observation:

```text
V2.4 version history says V2.2 removed SystemDocumentationService and SystemManagementService
and added SystemMonitoringService.

The V2.4 ServiceNameEnumeration PDF table still lists SystemDocumentationService,
SystemManagementService and SystemMonitoringService.

IBIS-IP_Enumerations_V2.4.xsd contains SystemMonitoringService but does not contain
SystemDocumentationService or SystemManagementService in the checked ServiceNameEnumeration snippet.
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

### CE-005 - TripInformation AdditionalTextMessage cardinality mismatch

State: schema/PDF discrepancy; needs confirmation before any schema change.

Observation:

```text
VDV 301-2-1 V2.4 TripInformation table lists:
AdditionalTextMessage     0:* +InternationalTextType
AdditionalTextMessage(n)  0:* +InternationalTextType, n = 1 to 9

IBIS-IP_common_V2.4.xsd contains:
AdditionalTextMessage, AdditionalTextMessage1 ... AdditionalTextMessage9
as optional elements without maxOccurs.

In XML Schema, missing maxOccurs means default maxOccurs="1".
```

Impact:

```text
The XSD allows at most one occurrence of each named AdditionalTextMessage field.
The PDF appears to allow multiple occurrences for the base field and each numbered field.
This may matter for multilingual or repeated passenger text messages because InternationalTextType
itself represents one language/value pair.
```

Next action:

```text
Compare V2.0, V2.1, V2.2 and V2.3 common XSD history for this field.
Check examples and PR/fork history.
Do not change the schema until intent is confirmed.
```
