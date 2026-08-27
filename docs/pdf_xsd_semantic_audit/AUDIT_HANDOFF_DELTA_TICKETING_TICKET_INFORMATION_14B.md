# Audit handoff delta - Ticketing / TicketInformation 14B

Status: TicketingService V1.0 semantic/provenance first pass closed.

Base handoff:

```text
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF.md
```

Read additionally:

```text
docs/pdf_xsd_semantic_audit/14_ticketing_ticket_information_service_historical_start.md
docs/pdf_xsd_semantic_audit/14a_ticketing_ticket_information_v1_0_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/14b_ticketing_ticket_information_findings_and_closure.md
docs/pdf_xsd_semantic_audit/TICKETING_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/TICKETING_SERVICE_VALIDATION_BACKLOG_ADDENDUM.md
docs/pdf_xsd_semantic_audit/OFFICIAL_RELEASE_BACKFILL_SAME_PATH_COLLISION_POLICY_ADDENDUM.md
docs/pdf_xsd_semantic_audit/generated/ticketing_service_historical_scope_matrix.csv
docs/pdf_xsd_semantic_audit/generated/ticketing_service_findings_closure_matrix.csv
```

## Key new routing fact

`TicketingService V1.0` has more than one official schema revision under the same filename.

```text
VDV-301-1.0:
  IBIS-IP_TicketInformationService_V1.0.xsd
  blob 017ca64666e25d757fc0cde1f1be817f06a743fc
  + Common V1.0
  + Enumerations V1.0
  + operation roots/group from IBIS_IP_V1.0.xsd

VDV-301-2.0 through checked later tags:
  same service filename
  blob 3fda66d872ab0d1c511247f13e715cf3ad56afe7
  + Common V1.0
  + Enumerations V1.0
  + operation roots/group moved into service XSD
```

The integration branch currently contains the later blob `3fda66d8...`.

Do not overwrite it with the older blob in the flat branch. Future strict routing needs `release_context/schema_revision` or immutable pool IDs.

## Executable service identity

```text
Public service: TicketingService
XSD filename: TicketInformationService
XML roots/types/group: TicketingService.* / TicketingServiceGroup
```

Do not generate a `TicketInformationService.*` XML alias from the filename.

## Findings opened

```text
TKT-001 same-path official schema revision/provenance ambiguity
TKT-002 filename vs executable service identity - OK with note
TKT-003 UnsubscribeValidationResult response table SubscribeResponseStructure
TKT-004 ValidateTicket request legacy/wrong table heading
TKT-005 GetValidationResult overview response type mismatch
TKT-006 tariff response sequence order PDF vs XSD
TKT-007 GetValidationResult detail table heading mismatch
TKT-008 CardApplicationInformation vs CardApplikationInformation
TKT-009 TicketingSevice PDF spelling
```

No XSD was modified.
No upstream PR, comment or merge was performed.
No local XSD compilation/sample validation was claimed.

## Next block

```text
docs/pdf_xsd_semantic_audit/15_time_service_historical_start.md
```

Start by checking whether TimeService V1.0 is intentionally non-XSD and mapping its exact discovery/protocol semantics.
