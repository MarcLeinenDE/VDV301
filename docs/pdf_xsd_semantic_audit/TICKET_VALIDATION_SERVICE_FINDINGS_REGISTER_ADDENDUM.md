# TicketValidationService findings register addendum

Status: supplemental register; historical first-pass closure completed for TicketValidationService V2.1 through V2.4. Keep separate until the main findings register is consolidated.

Authority rule:

```text
Validation follows the selected XSD family.
PDF differences are provider-facing/documentation evidence, not executable aliases.
Official release-tag provenance controls historical XSD status.
```

Source audit files:

```text
docs/pdf_xsd_semantic_audit/03_tvs_v2_2_v2_3_v2_4_include_semantic_audit.md
docs/pdf_xsd_semantic_audit/09_ticket_validation_service_historical_start.md
docs/pdf_xsd_semantic_audit/09a_ticket_validation_service_v2_1_v2_3_history_and_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/09b_ticket_validation_service_findings_and_closure.md
```

## TicketValidationService findings

### TVS-001 - GetCurrentShortHaulStopsResponse omitted from TicketValidationServiceOperations

State: open XSD internal-consistency candidate.

Classification:

```text
mismatch_kind: xsd_internal_operation_inventory
likely_source_issue: xsd_internal_consistency_candidate
classification_confidence: high for structural observation
version_scope: V2.4 XSD
final_handling_bucket: local_compile_and_sample_validation_then_official_facing_review
```

Observation:

```text
The V2.4 XSD defines TicketValidationService.GetCurrentShortHaulStopsResponse as a top-level element and defines the related response/data structures.
The TicketValidationServiceOperations group omits TicketValidationService.GetCurrentShortHaulStopsResponse.
Current official upstream master still reproduces this structure.
```

Impact:

```text
Direct top-level validation/discovery can see the operation element.
Code or tooling that derives the operation inventory from TicketValidationServiceOperations alone can miss the V2.4 short-haul operation.
```

Next action: local schema compile, operation-inventory test and representative short-haul samples before deciding any official-facing XSD correction.

### TVS-002 - VehicleData.RouteDeviation PDF type vs XSD type

State: confirmed high-confidence PDF table/documentation candidate.

Classification:

```text
mismatch_kind: type
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
version_scope: V2.1, V2.2, V2.3, V2.4 PDFs
final_handling_bucket: provider_note_or_pdf_clarification_candidate
```

Observation:

```text
The checked TVS PDFs V2.1 through V2.4 list VehicleData.RouteDeviation with RouteDirectionEnumeration.
The executable XSD route throughout the chain uses RouteDeviationEnumeration:
  V2.1 XSD directly;
  V2.2 XSD directly;
  V2.3 official document route via unchanged V2.2 XSD;
  V2.4 checked XSD directly.
```

Impact:

```text
The validator must enforce RouteDeviationEnumeration according to the selected XSD.
Do not add RouteDirectionEnumeration as an automatic compatibility alias merely to match PDF text.
```

Next action: targeted local XML sample and later provider-facing documentation note.

### TVS-003 - stale CurrentStopPoint response/table labels after CurrentTariffStop rename

State: confirmed high-confidence PDF label/heading candidate.

Classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: high
version_scope: V2.2, V2.3, V2.4 PDFs
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

Observation:

```text
From V2.2 onward the operation/data concept is renamed to CurrentTariffStop in the XSD and in the main PDF section names.
The PDF version history explicitly documents that rename.
Nevertheless V2.2 retains stale GetCurrentStopPointResponse / CurrentStopPointData labels in chapter 3.1.2 and table captions.
V2.3 states that chapter 3.1.2 was corrected to match XSD V2.2; the data-structure body is improved, but stale GetCurrentStopPointResponse / CurrentStopPointData captions remain.
V2.4 continues to carry those stale captions.
```

Impact:

```text
Executable validation uses GetCurrentTariffStopResponse / CurrentTariffStopDataStructure / CurrentTariffStop.
The stale PDF labels must not be accepted as schema aliases by the validator.
Provider-facing diagnostics may cite the PDF documentation inconsistency if a system implemented the stale names.
```

Next action: documentation clarification candidate; no XSD modification proposed.

## Routing note - TVS V2.3

This is intentionally not a separate defect finding.

```text
VDV 301-2-16 V2.3 is a documentation correction release.
Official tag VDV-301-2.3 still contains IBIS-IP_TicketValidationService_V2.2.xsd.
The V2.3 PDF explicitly says no XSD update was necessary and refers to the corresponding XSD V2.2 file.
Therefore official TVS V2.3 routing uses the V2.2 service XSD pool.
```

Classification:

```text
ok_with_note
```

Branch note:

```text
IBIS-IP_TicketValidationService_V2.3.xsd in dev/schema-integration was added as public candidate/integration material in commit c9c086ac07f7e9bdb271c54f7a274e3cf0d03749.
It is not historical official release material and must remain provenance-separated.
```
