# Ticketing / TicketInformation V1.0 findings and first-pass closure

Status: semantic/provenance first-pass closure completed. Local XSD compilation/sample validation remains pending.

Source blocks:

```text
docs/pdf_xsd_semantic_audit/14_ticketing_ticket_information_service_historical_start.md
docs/pdf_xsd_semantic_audit/14a_ticketing_ticket_information_v1_0_pdf_xsd_first_pass.md
```

## Routing closure

### Original VDV-301-1.0 release profile

```text
Public service: TicketingService V1.0
Service-file name: IBIS-IP_TicketInformationService_V1.0.xsd
Service blob: 017ca64666e25d757fc0cde1f1be817f06a743fc
Dependencies: Common V1.0 + Enumerations V1.0
Operation-root layer: IBIS_IP_V1.0.xsd blob 41289eaed2674a169fdf77a10a2eff293c76d5c4
Executable prefix: TicketingService.*
```

### Later official V1.0 schema revision, released with VDV-301-2.0+

```text
Same service-file name: IBIS-IP_TicketInformationService_V1.0.xsd
Service blob: 3fda66d872ab0d1c511247f13e715cf3ad56afe7
Dependencies: Common V1.0 + Enumerations V1.0
Operation roots/group moved into the service XSD
Executable prefix: TicketingService.*
```

The integration branch currently contains the later official blob `3fda66d8...`.

## Findings

### TKT-001 - two official schema revisions under the same V1.0 path

```text
classification: schema_family_or_provenance_gap
confidence: high
handling: release-context/schema-revision selector required
```

A flat `(service, version)` key is insufficient for strict historical routing.

### TKT-002 - TicketInformationService filename vs TicketingService executable identity

```text
classification: ok_with_note
confidence: high
handling: resolver metadata only; XML names use TicketingService
```

### TKT-003 - UnsubscribeValidationResult response type

```text
PDF: SubscribeResponseStructure
expected shared unsubscribe model / analogous operation: UnsubscribeResponseStructure
classification: pdf_table_or_documentation_error_candidate
confidence: high
```

### TKT-004 - ValidateTicket request table heading

```text
PDF: TicketInformationService.Validation.GetDataRequest
XSD/operation overview: TicketingService.ValidateTicketRequest[Structure]
classification: pdf_label_or_heading_error_candidate
confidence: high
```

### TKT-005 - GetValidationResult overview response type

```text
PDF overview: TicketingService.ValidationResultStructure
XSD: TicketingService.GetValidationResultResponseStructure
classification: pdf_table_or_documentation_error_candidate
confidence: high
```

### TKT-006 - tariff response sequence order

```text
PDF table: TimeStamp then DefaultLanguage
XSD xs:sequence: DefaultLanguage then TimeStamp
classification: pdf_table_or_documentation_error_candidate
mismatch_kind: sequence_order
confidence: high
```

Validation must follow XSD order.

### TKT-007 - GetValidationResult detail table heading vs represented structure

```text
PDF heading: GetValidationResultResponseStructure
fields shown: TimeStamp + ValidationResult
XSD type matching those fields: ValidationResultDataStructure
classification: pdf_label_or_heading_error_candidate
confidence: high
```

### TKT-008 - CardApplicationInformation vs CardApplikationInformation

```text
PDF: CardApplicationInformation
XSD: CardApplikationInformation
classification: pdf_table_or_documentation_error_candidate
confidence: medium-high
```

### TKT-009 - TicketingSevice PDF spelling

```text
PDF detail labels: TicketingSevice
XSD/service title: TicketingService
classification: pdf_label_or_heading_error_candidate
confidence: high
```

## SDK implications

```text
- Canonical service identity is TicketingService, not the XSD filename token.
- Preserve original V1.0 release profile separately from the later official V1.0 schema revision.
- Add release_context/schema_revision to the future resolver where one service/version maps to multiple official blobs.
- Original V1.0 root validation requires the official aggregate family.
- Later V1.0 revision is self-contained for the TicketingService roots/group.
- Do not accept legacy PDF labels as automatic XML aliases.
- Enforce XSD sequence ordering even if PDF table order differs.
```

## Validation status

```text
Semantic/provenance first pass: closed.
Local XSD compilation: not performed.
Sample XML validation: not performed.
No XSD modification: yes.
No upstream PR/comment/merge action: yes.
```

## Next planned historical service block

```text
15_time_service_historical_start.md
VDV 301-2-10 TimeService V1.0
```

Initial focus:

```text
Confirm whether TimeService is intentionally non-XSD/protocol-profile based.
Resolve DNS-SD/NTP or HTTP/protocol semantics from the public writing and General Conventions.
Do not invent a TimeService XSD if the service is intentionally schema-free.
```
