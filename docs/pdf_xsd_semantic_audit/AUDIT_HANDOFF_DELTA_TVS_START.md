# Audit handoff delta - TicketValidationService historical start

Status: supplemental handoff delta after starting the historical TVS continuation block.

Branch:

```text
dev/schema-integration
```

Starting commit verified before write:

```text
5116b09d81bbf78b2cb23b13436108b792f40330
```

## New files / material

```text
IBIS-IP_TicketValidationService_V2.1.xsd
docs/pdf_xsd_semantic_audit/09_ticket_validation_service_historical_start.md
docs/pdf_xsd_semantic_audit/generated/ticket_validation_service_historical_scope_matrix.csv
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_TVS_START.md
```

## Historical V2.1 backfill provenance

```text
source repository: VDVde/VDV301
source tag: VDV-301-2.1
release commit: 585e0bea34b64887db4276f1c94d5f3e78f06c66
source blob: f6497e6469b82ee19b185c4de749d13a7ca60bed
file: IBIS-IP_TicketValidationService_V2.1.xsd
classification: historical official release material
```

The XSD is carried into the integration branch from the exact official release-tag blob. It is not a reconstructed schema and not PR/fork historical material.

## Version-exact pools currently established

```text
TVS V2.1 -> Common V1.0 + Enumerations V1.0
TVS V2.2 -> Common V2.2 + Enumerations V2.2
TVS V2.3 -> Common V2.2 + Enumerations V2.2
TVS V2.4 integration/candidate -> Common V2.4 + Enumerations V2.4
```

Do not latest-map these pools.

## Existing findings preserved

```text
TVS-001: V2.4 GetCurrentShortHaulStopsResponse omitted from TicketValidationServiceOperations group.
TVS-002: VehicleData.RouteDeviation PDF type RouteDirectionEnumeration vs XSD RouteDeviationEnumeration.
```

New historical evidence shows the TVS-002 mismatch direction already in V2.1 and V2.2.

## New candidate note

```text
TVS-003 candidate:
V2.2 changed the operation/data vocabulary to CurrentTariffStop, and its version history explicitly records the rename, but some response/table labels remain GetCurrentStopPointResponse / CurrentStopPointData. Official V2.2 XSD uses the tariff-stop names consistently.
Initial class: pdf_label_or_heading_error_candidate.
```

Do not open a replacement/duplicate finding for TVS-001 or TVS-002. Formal TVS findings-register consolidation should follow the detailed historical pass.

## Validation status

```text
No local XSD compile executed in this starter block.
No sample XML validation executed in this starter block.
No XSD correction made.
No PR/comment/merge created.
```

## Next recommended file

```text
docs/pdf_xsd_semantic_audit/09a_ticket_validation_service_v2_1_v2_2_history_and_pdf_xsd_first_pass.md
```
