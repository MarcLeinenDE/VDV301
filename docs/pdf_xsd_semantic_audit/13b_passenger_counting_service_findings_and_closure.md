# PassengerCountingService V1.0 / V2.1 findings and first-pass closure

Status: semantic/provenance first-pass closure completed. Local XSD compilation/sample validation remains pending.

Source blocks:

```text
docs/pdf_xsd_semantic_audit/13_passenger_counting_service_historical_start.md
docs/pdf_xsd_semantic_audit/13a_passenger_counting_service_v1_0_v2_1_pdf_xsd_first_pass.md
```

## Historical routing closure

### V1.0

```text
Public document: VDV 301-2-8 PassengerCountingService V1.0
Official service XSD source: VDVde/VDV301 tag VDV-301-1.0
Service blob: 600a3ee6290c630a4435fb06ca9803dabaceb788
Backfilled unchanged into dev/schema-integration.
Service dependency pool: Common V1.0 + Enums V1.0.
Operation roots/group: official release aggregate IBIS_IP_V1.0.xsd.
```

### V2.1

```text
Public document: VDV 301-2-8 PassengerCountingService V2.1
Official service XSD source: VDVde/VDV301 tag VDV-301-2.1
Service blob: 59ef2ddb09b92db0d492974e38bad5b6be03865e
Service dependency pool: Common V1.0 + Enums V1.0.
```

## Findings

### PCS-001 - OperationNotSupported excluded by selected V2.1 dependency pool

```text
state: confirmed PDF/XSD dependency/value-set discrepancy
mismatch_kind: schema_family_or_dependency_value_set
confidence: high
validation_behavior: exact PCS V2.1 pool excludes OperationNotSupported
handling: local validation + post-audit schema-family clarification candidate
```

Reason:

```text
PDF V2.1 documents OperationNotSupported for new optional operations.
PCS V2.1 explicitly selects Common V1.0 + Enums V1.0.
Enums V1.0 lacks OperationNotSupported.
Enums V2.1 contains it but is not selected.
Common V1.0 response/wrapper types route ErrorCode positions through ErrorCodeEnumeration.
```

No automatic schema/dependency fix is proposed.

### PCS-002 - V1.0 aggregate operation-root model

```text
state: OK with note
mismatch_kind: historical_aggregate_routing
confidence: high
validation_behavior: V1.0 service structures + official aggregate operation roots
handling: resolver profile requirement
```

This is not an upstream defect.

## SDK implications

```text
- Preserve PCS V1.0 and V2.1 as separate official profiles.
- PCS V1.0 service schema alone is not the whole official root-validation family; operation roots live in IBIS_IP_V1.0.xsd.
- Preserve PCS V2.1 -> Common V1.0 -> Enums V1.0 exactly.
- Do not latest-wins-map PCS V2.1 to Common/Enums V2.1.
- When OperationNotSupported appears, diagnostics should distinguish PDF-required semantics from XSD-selected value-set authority.
- Historical aggregate schemas need an explicit resolver concept in the later SDK.
```

## Validation status

```text
Semantic/provenance first pass: closed.
V1.0 backfill integrity: verified by identical Git blob SHA.
Local XSD compilation: not performed.
Sample XML validation: not performed.
No XSD correction: yes.
No upstream PR/comment/merge action: yes.
```

## Next planned historical service block

```text
Ticketing / TicketInformation V1.0
VDV 301-2-9
```

Initial focus:

```text
Resolve public PDF naming TicketingService vs repository file IBIS-IP_TicketInformationService_V1.0.xsd.
Resolve the exact V1.0 aggregate/service schema relationship.
Compare operation names and types without assuming the filename or PDF title is the executable service name.
```
