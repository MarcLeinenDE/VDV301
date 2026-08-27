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
Complete table-level checks for LineInformation, StopInformation, TripInformation and DoorCountingObjectClassEnumeration.
```
