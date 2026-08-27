# TicketValidationService findings and historical first-pass closure

Status: first-pass historical TVS audit closed for V2.1 through V2.4. Local XSD compilation/sample validation remains open and is required before any executable correction proposal.

Source blocks:

```text
docs/pdf_xsd_semantic_audit/03_tvs_v2_2_v2_3_v2_4_include_semantic_audit.md
docs/pdf_xsd_semantic_audit/09_ticket_validation_service_historical_start.md
docs/pdf_xsd_semantic_audit/09a_ticket_validation_service_v2_1_v2_3_history_and_pdf_xsd_first_pass.md
```

## 1. Historical routing closure

The first-pass routing result is:

```text
PDF/service document V2.1
  -> TVS XSD V2.1 official release tag
  -> Common V1.0 + Enumerations V1.0

PDF/service document V2.2
  -> TVS XSD V2.2 official release tag
  -> Common V2.2 + Enumerations V2.2

PDF/service document V2.3
  -> TVS XSD V2.2 official release tag
  -> Common V2.2 + Enumerations V2.2
  -> intentional documentation-only service release; no official TVS V2.3 XSD in tag

PDF/service document V2.4
  -> new TVS V2.4 functionality exists
  -> dev/schema-integration route remains candidate/integration: TVS V2.4 + Common V2.4 + Enumerations V2.4
```

The branch-local `IBIS-IP_TicketValidationService_V2.3.xsd` is not official historical release material. It remains candidate/integration material and must not override the official V2.3 -> V2.2 XSD routing fact.

## 2. Finding decisions

### TVS-001 - V2.4 operation inventory omission

State: open XSD internal-consistency candidate.

```text
Top-level GetCurrentShortHaulStopsResponse exists.
TicketValidationServiceOperations omits it.
Current upstream master still reproduces the omission.
No schema edit made.
```

Classification:

```text
xsd_internal_consistency_candidate
```

### TVS-002 - RouteDeviation PDF type mismatch

State: confirmed high-confidence PDF table/documentation candidate across V2.1-V2.4.

```text
PDF: RouteDirectionEnumeration
XSD route: RouteDeviationEnumeration
```

Classification:

```text
pdf_table_or_documentation_error_candidate
```

Validation remains exact-XSD driven.

### TVS-003 - stale CurrentStopPoint labels after CurrentTariffStop rename

State: confirmed high-confidence PDF label/heading candidate across V2.2-V2.4.

```text
Executable XSD vocabulary: GetCurrentTariffStopResponse / CurrentTariffStopDataStructure / CurrentTariffStop
PDF retains selected response/table captions using GetCurrentStopPointResponse / CurrentStopPointData.
```

Classification:

```text
pdf_label_or_heading_error_candidate
```

No XSD change proposed.

## 3. Routing note - TVS V2.3 document version does not equal XSD filename version

State: OK with note, not an error finding.

Official evidence aligns:

```text
VDV-301-2.3 release tag keeps IBIS-IP_TicketValidationService_V2.2.xsd.
V2.3 PDF states chapter 3.1.2 was corrected to match the corresponding XSD V2.2 and no XSD update was necessary.
```

Tool requirement:

```text
The SDK resolver must allow document/service version V2.3 to resolve to service XSD V2.2.
Never synthesize or require TVS V2.3 solely from the document version.
```

## 4. Historical official backfill closure

Added to `dev/schema-integration`:

```text
IBIS-IP_TicketValidationService_V2.1.xsd
```

Provenance:

```text
VDVde/VDV301 tag VDV-301-2.1
blob f6497e6469b82ee19b185c4de749d13a7ca60bed
```

Target branch blob SHA was verified identical after integration.

No fork/PR/candidate material was used as the historical V2.1 backfill source.

## 5. Local validation backlog

Still open:

```text
1. Compile TVS V2.1 + Common V1.0 + Enumerations V1.0.
2. Compile TVS V2.2 + Common V2.2 + Enumerations V2.2.
3. Validate representative V2.3 service-document payloads against the official V2.2 XSD pool.
4. Compile the V2.4 integration/candidate pool selected by dev/schema-integration.
5. Positive/negative cross-version stop/tariff-stop samples.
6. Positive VehicleData.RouteDeviation sample using RouteDeviationEnumeration.
7. V2.4 top-level-vs-operation-group inventory tests for TVS-001.
```

No file/pool is described as locally validated by this closure.

## 6. First-pass closure result

```text
TicketValidationService historical PDF/XSD audit V2.1-V2.4: first-pass closed.
Historical official V2.1 XSD backfill: completed and provenance-verified.
Official V2.3 routing: resolved to TVS XSD V2.2 pool.
TVS-001: open XSD internal-consistency candidate.
TVS-002: confirmed PDF documentation candidate, V2.1-V2.4.
TVS-003: confirmed PDF label/heading candidate, V2.2-V2.4.
Branch-local TVS V2.3 XSD: candidate/integration only.
Local technical validation: pending.
No XSD correction, PR, comment or merge performed.
```

## 7. Next audit block

The scope matrix lists HTMLDisplayService directly after TicketValidationService.

Suggested next starter file, after this TVS closure is accepted:

```text
docs/pdf_xsd_semantic_audit/10_html_display_service_historical_start.md
```

Initial question for that block:

```text
Does HTMLDisplayService intentionally have no dedicated XSD because its payload/content model is HTTP/HTML-based, or is there a historical schema/provenance gap?
```
