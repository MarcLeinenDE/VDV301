# TicketValidationService findings register addendum

Status: supplemental register; historical first-pass closure completed for TicketValidationService V2.1 through V2.4. TVS V2.1 has now also been independently re-read and its in-scope findings processed under the current Evidence Gate. Keep separate until the main findings register is consolidated.

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
docs/pdf_xsd_semantic_audit/deep_read/TVS_V2.1.md
audit_registry/deep_read_findings_delta_tvs_v21_2026-08-29.json
docs/pdf_xsd_semantic_audit/24k_executable_validation_tvs_v21.md
```

## TicketValidationService findings

### TVS-001 - GetCurrentShortHaulStopsResponse omitted from TicketValidationServiceOperations

State: open XSD internal-consistency candidate; **not revalidated by the TVS V2.1 Deep Read because its scope is V2.4**.

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

Next action: revalidate under the current Evidence Gate in the correct V2.4 authority/context before any SDK or official-facing decision.

### TVS-002 - VehicleData.RouteDeviation PDF type vs XSD type

State: `executable_confirmed_EV-112` for V2.1 under the current Evidence Gate. Later-version historical scope remains subject to its own per-version revalidation.

Classification:

```text
mismatch_kind: type
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
version_scope: V2.1, V2.2, V2.3, V2.4 PDFs
V2.1_revalidation_state: executable_confirmed_EV-112
final_handling_bucket: provider_note_or_pdf_clarification_candidate
```

Historical observation:

```text
The checked TVS PDFs V2.1 through V2.4 list VehicleData.RouteDeviation with RouteDirectionEnumeration.
The executable XSD route throughout the historical chain was recorded as RouteDeviationEnumeration:
  V2.1 XSD directly;
  V2.2 XSD directly;
  V2.3 official document route via unchanged V2.2 XSD;
  V2.4 checked XSD directly.
```

Current V2.1 Evidence-Gate revalidation:

```text
PDF page 16 visibly prints RouteDirectionEnumeration for VehicleData.RouteDeviation.

Exact official VDV-301-2.1 family:
  TicketValidationService V2.1
  -> Common V1.0
  -> Enumerations V1.0

Exact XSD declaration:
  RouteDeviation type = RouteDeviationEnumeration

EV-112 run 33249561880:
  RouteDeviationEnumeration exists
  RouteDirectionEnumeration absent from exact Enumerations V1.0
  onroute/offroute/unknown -> valid
  NOT_A_ROUTE_DEVIATION    -> invalid
```

Impact:

```text
The validator must enforce RouteDeviationEnumeration according to the selected XSD.
Do not add RouteDirectionEnumeration as an automatic compatibility alias merely to match PDF text.
```

Next action: no V2.1 deterministic evidence is pending. Revalidate the V2.2/V2.3/V2.4 instances independently in their own exact authority/context before treating the multi-version historical statement as frozen SDK knowledge.

### TVS-003 - stale CurrentStopPoint response/table labels after CurrentTariffStop rename

State: confirmed historical PDF label/heading candidate; **not revalidated by the TVS V2.1 Deep Read because its scope begins at V2.2**.

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

Next action: revalidate in the V2.2+ Deep Read blocks before baseline freeze; no XSD modification is proposed.

## New TVS V2.1 Deep Read findings

### DRTVS21-001 - CurrentTripRef PDF type identifier case

State: `executable_confirmed`.

Classification:

```text
mismatch_kind: type_identifier_case
likely_source_issue: pdf_type_identifier_typo_candidate
version_scope: V2.1 PDF
```

Evidence:

```text
PDF page 14: IBIS-IP.NMToken
exact XSD:    IBIS-IP.NMTOKEN

EV-112:
  IBIS-IP.NMTOKEN exists
  IBIS-IP.NMToken does not exist
  a probe schema using IBIS-IP.NMToken fails compilation
```

Impact:

```text
No case-normalizing alias is allowed.
Exact selected XSD/Common type names remain authoritative.
```

### DRTVS21-002 - GetCurrentLine response display missing separator dot

State: `context_verified`.

Classification:

```text
mismatch_kind: pdf_type_display_identifier
likely_source_issue: pdf_type_display_identifier_typo_candidate
subtype: missing_service_name_separator_dot
version_scope: V2.1 PDF
```

Evidence:

```text
PDF page 15 response display:
  TicketValidationServiceCurrentLineData

immediately following table:
  TicketValidationService. CurrentLineData

exact XSD type:
  TicketValidationService.CurrentLineDataStructure
```

Boundary:

```text
The PDF intentionally omits the Structure suffix in other shortened display names.
That suffix omission is not classified as a defect here.
The finding is limited to the missing service-name separator dot.
```

Impact: documentation/context diagnostic only; no schema alias or normalization.

### DRTVS21-003 - SubscribeCurrentStop vs SubscribeCurrentStopPoint

State: `context_verified`.

Classification:

```text
mismatch_kind: operation_name
likely_source_issue: pdf_operation_name_editorial_error_candidate
version_scope: V2.1 PDF
```

Evidence:

```text
German flow page 11:  SubscribeCurrentStop
English flow page 13: SubscribeCurrentStop

formal operation overviews pages 10/12:
  SubscribeCurrentStopPoint

detailed section page 14:
  SubscribeCurrentStopPoint

exact XSD operation group:
  SubscribeCurrentStopPoint
```

Impact: documentation/operation-name diagnostic only; no alias.

### DRTVS21-004 - minor non-executable PDF editorial residue

State: `context_verified`.

Classification:

```text
mismatch_kind: documentation_spelling
likely_source_issue: pdf_documentation_typo_non_executable
version_scope: V2.1 PDF
```

Visible targeted-page examples:

```text
Unscubscribe
GetrazziaResponsetData
Error Respone
```

Impact: none on XML validation.

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

## V2.1 Evidence-Gate closure boundary

```text
TVS-002       revalidated for V2.1 with EV-112
DRTVS21-001  executable-confirmed
DRTVS21-002  context-verified with explicit display-convention boundary
DRTVS21-003  context-verified
DRTVS21-004  context-verified non-executable

TVS-001      not revalidated here; V2.4 scope
TVS-003      not revalidated here; V2.2+ scope
```

The broader historical TicketValidation inventory is not frozen by this V2.1 closure. Later version blocks must independently apply the current Evidence Gate.
