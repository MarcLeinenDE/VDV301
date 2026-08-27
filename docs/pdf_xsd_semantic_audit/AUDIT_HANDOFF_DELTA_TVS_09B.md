# Audit handoff delta - TicketValidationService 09B closure

Status: supplemental handoff delta after completing the historical TVS first pass.

Branch:

```text
dev/schema-integration
```

## New audit files

```text
docs/pdf_xsd_semantic_audit/09a_ticket_validation_service_v2_1_v2_3_history_and_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/09b_ticket_validation_service_findings_and_closure.md
docs/pdf_xsd_semantic_audit/TICKET_VALIDATION_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
```

Updated generated routing matrix:

```text
docs/pdf_xsd_semantic_audit/generated/ticket_validation_service_historical_scope_matrix.csv
```

## Critical routing correction from the starter pass

The official VDV-301-2.3 tag does not contain a TVS V2.3 XSD. It retains the exact TVS V2.2 file:

```text
IBIS-IP_TicketValidationService_V2.2.xsd
blob 5a4be2b2ba66860f035777ec0458dba0790880e1
```

The V2.3 PDF explicitly says the release corrects chapter 3.1.2 to match the corresponding XSD V2.2 and that no XSD update is necessary.

Therefore official historical routing is:

```text
TVS document V2.3 -> TVS XSD V2.2 + Common V2.2 + Enumerations V2.2
```

The branch-local `IBIS-IP_TicketValidationService_V2.3.xsd` was introduced as public candidate/integration material by commit `c9c086ac07f7e9bdb271c54f7a274e3cf0d03749`. It is not historical official release material and must remain provenance-separated.

## Historical official backfill

```text
TVS V2.1 XSD source: official VDVde/VDV301 tag VDV-301-2.1
source/target blob: f6497e6469b82ee19b185c4de749d13a7ca60bed
pool: TVS V2.1 + Common V1.0 + Enumerations V1.0
```

Backfill is complete and byte-identical by Git blob SHA.

## Finding status

```text
TVS-001: open XSD internal-consistency candidate; V2.4 GetCurrentShortHaulStopsResponse missing from TicketValidationServiceOperations; current upstream master still reproduces it.

TVS-002: confirmed PDF table/documentation candidate; RouteDeviation is printed as RouteDirectionEnumeration in PDFs V2.1-V2.4 while XSD route uses RouteDeviationEnumeration.

TVS-003: confirmed PDF label/heading candidate; V2.2-V2.4 retain stale GetCurrentStopPointResponse / CurrentStopPointData captions after CurrentTariffStop rename.
```

## Technical validation status

```text
Local selected-pool XSD compilation: pending.
Sample XML validation: pending.
No pool is claimed locally validated.
```

## Prohibited actions preserved

```text
No master modification.
No official PR creation/update.
No PR comments.
No merge.
No XSD correction due solely to PDF mismatch.
```

## Next recommended audit block

After accepting this TVS first-pass closure, continue the scope matrix with:

```text
docs/pdf_xsd_semantic_audit/10_html_display_service_historical_start.md
```

The first question is whether HTMLDisplayService intentionally has no dedicated XSD because the service payload is HTML/HTTP-based, rather than treating the absence automatically as a provenance gap.
