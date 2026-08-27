# Audit handoff delta - PassengerCountingService 13B

Base:

```text
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF.md
```

This delta supersedes the older handoff's continuation point for the active service sequence.

## Completed block

```text
PassengerCountingService V1.0 / V2.1 semantic/provenance first pass closed.
```

Files:

```text
13_passenger_counting_service_historical_start.md
13a_passenger_counting_service_v1_0_v2_1_pdf_xsd_first_pass.md
13b_passenger_counting_service_findings_and_closure.md
PASSENGER_COUNTING_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
PASSENGER_COUNTING_SERVICE_VALIDATION_BACKLOG_ADDENDUM.md
OFFICIAL_PR_CANDIDATES_ADDENDUM_PCS.md
generated/passenger_counting_service_historical_scope_matrix.csv
generated/passenger_counting_service_findings_closure_matrix.csv
```

## Historical backfill

```text
IBIS-IP_PassengerCountingService_V1.0.xsd
source: VDVde/VDV301 tag VDV-301-1.0
blob: 600a3ee6290c630a4435fb06ca9803dabaceb788
status: official historical release material, copied unchanged
```

## Key routing facts

```text
PCS V1.0 service XSD -> Common V1.0 + Enums V1.0.
PCS V1.0 global operation roots/group -> official release aggregate IBIS_IP_V1.0.xsd.
PCS V2.1 -> Common V1.0 + Enums V1.0, despite V2.1 Common/Enums also being present in the release.
```

## Findings

```text
PCS-001: confirmed V2.1 dependency/value-set discrepancy; PDF requires OperationNotSupported, exact selected Enums V1.0 excludes it.
PCS-002: OK with note; V1.0 operation-root declarations are aggregate-owned by design.
```

## Local validation

```text
Not performed. Keep PASSENGER_COUNTING_SERVICE_VALIDATION_BACKLOG_ADDENDUM.md open.
```

## Next block

```text
Ticketing / TicketInformation V1.0
VDV 301-2-9
```

First questions:

```text
1. Why does the public service/document naming use TicketingService while the file is IBIS-IP_TicketInformationService_V1.0.xsd?
2. Which operation roots are service-XSD-local and which are aggregate-owned in V1.0?
3. Does the public PDF map exactly to the official V1.0 release schema family?
```
