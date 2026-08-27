# TicketValidationService V2.1 -> V2.3 history and PDF/XSD first pass

Status: detailed historical first pass completed for the V2.1 -> V2.3 transition and its impact on the previously audited V2.4 state. Local XSD compilation and sample validation remain pending.

This file refines the starter mapping in:

```text
docs/pdf_xsd_semantic_audit/09_ticket_validation_service_historical_start.md
```

and continues the existing TVS findings from:

```text
docs/pdf_xsd_semantic_audit/03_tvs_v2_2_v2_3_v2_4_include_semantic_audit.md
```

## 1. Authority rule

```text
Validation follows the selected official/candidate XSD family.
A PDF version number must not be converted automatically into an identically numbered XSD filename.
The official release-tag contents and explicit PDF version history determine the historical routing facts.
```

This point is material for TVS V2.3.

## 2. V2.1 official release state

Official source:

```text
VDVde/VDV301 tag VDV-301-2.1
commit 585e0bea34b64887db4276f1c94d5f3e78f06c66
IBIS-IP_TicketValidationService_V2.1.xsd
blob f6497e6469b82ee19b185c4de749d13a7ca60bed
```

The exact blob is now present in `dev/schema-integration` as historical official release material.

Observed includes:

```text
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

Historical service vocabulary:

```text
GetCurrentStopPointResponse
CurrentStopPointDataStructure
CurrentStopPoint
```

## 3. V2.1 -> V2.2 official release delta

The official GitHub comparison between tags VDV-301-2.1 and VDV-301-2.2 records the TVS file as a rename:

```text
IBIS-IP_TicketValidationService_V2.1.xsd
-> IBIS-IP_TicketValidationService_V2.2.xsd
9 additions / 9 deletions
```

The material changes observed in the service file are:

```text
dependency pool:
  Common V1.0 / Enumerations V1.0
  -> Common V2.2 / Enumerations V2.2

service vocabulary:
  GetCurrentStopPointResponse
  -> GetCurrentTariffStopResponse

  CurrentStopPointDataStructure
  -> CurrentTariffStopDataStructure

  CurrentStopPoint
  -> CurrentTariffStop
```

The remaining checked TVS service structures, including VehicleData and RetrieveTripData, retain the same modelling in this transition.

The V2.2 PDF version history explicitly explains the rename: `CurrentStopPoint` is used in CIS and TVS with different meanings, therefore the TVS concept is renamed to `CurrentTariffStop`.

SDK implication:

```text
TVS document/schema V2.1 payloads use CurrentStopPoint names.
TVS V2.2 official payloads use CurrentTariffStop names.
Do not normalize names before schema validation.
```

## 4. Critical V2.3 provenance/routing result

The official release tag `VDV-301-2.3` does **not** contain an `IBIS-IP_TicketValidationService_V2.3.xsd`.

Instead the tag still contains:

```text
IBIS-IP_TicketValidationService_V2.2.xsd
blob 5a4be2b2ba66860f035777ec0458dba0790880e1
```

This is the same official TVS V2.2 blob observed in the V2.2 release state.

The official tag comparison VDV-301-2.2 -> VDV-301-2.3 contains no TVS file change.

The V2.3 PDF confirms the reason explicitly:

```text
V2.3 corrects the description of the data tables in chapter 3.1.2 so that they correspond to the correct data definitions in the corresponding XSD V2.2 file.
No XSD update is necessary.
```

Therefore the authoritative historical routing rule is:

```text
VDV 301-2-16 TicketValidationService document V2.3
-> IBIS-IP_TicketValidationService_V2.2.xsd
-> IBIS-IP_common_V2.2.xsd
-> IBIS-IP_Enumerations_V2.2.xsd
```

Classification:

```text
finding_class: ok_with_note
mismatch_kind: version_label_vs_executable_schema_family
reason: intentional documentation-only release update; official tag and PDF both retain XSD V2.2
```

This is an important example for the future SDK: service-document version and service-XSD filename are not always numerically identical.

## 5. Branch-local `IBIS-IP_TicketValidationService_V2.3.xsd`

The integration branch contains:

```text
IBIS-IP_TicketValidationService_V2.3.xsd
```

Repository history shows that this file was introduced on 2026-08-26 by audit/integration commit:

```text
c9c086ac07f7e9bdb271c54f7a274e3cf0d03749
Integrate public schema candidate files
```

It is not present in the official VDV-301-2.3 release tag.

The branch file mirrors the checked V2.2 service structure and still includes Common V2.2 + Enumerations V2.2, but its existence must not change the official historical routing rule.

Status:

```text
IBIS-IP_TicketValidationService_V2.3.xsd in dev/schema-integration
= candidate/integration material
= not historical official release backfill
= must not be selected as the authoritative official V2.3 route by default
```

If retained by the later SDK, it should be exposed only through an explicit candidate/integration provenance lane or as a non-authoritative alias, never silently as the official V2.3 schema.

## 6. TVS-002 full historical version scope

The previously opened TVS-002 is now confirmed across the complete public PDF chain V2.1 through V2.4.

PDF observation:

```text
V2.1 VehicleData.RouteDeviation -> RouteDirectionEnumeration
V2.2 VehicleData.RouteDeviation -> RouteDirectionEnumeration
V2.3 VehicleData.RouteDeviation -> RouteDirectionEnumeration
V2.4 VehicleData.RouteDeviation -> RouteDirectionEnumeration
```

Executable XSD observation:

```text
V2.1 official XSD -> RouteDeviationEnumeration
V2.2 official XSD -> RouteDeviationEnumeration
V2.3 official route uses unchanged V2.2 XSD -> RouteDeviationEnumeration
V2.4 checked XSD -> RouteDeviationEnumeration
```

Classification:

```text
finding_id: TVS-002
mismatch_kind: type
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
version_scope: V2.1, V2.2, V2.3, V2.4 PDFs
validation_behavior: use RouteDeviationEnumeration from the selected XSD family
```

Reasoning:

```text
The field is named RouteDeviation.
The executable XSD chain consistently uses RouteDeviationEnumeration.
The PDF chain consistently prints RouteDirectionEnumeration.
The PDF itself says the XSD is master in case of mismatch.
```

No automatic alias/correction should be introduced into schema validation.

## 7. TVS-003 confirmed - stale CurrentStopPoint response/table labels after V2.2 rename

The V2.2 PDF correctly changes the section/operation vocabulary to:

```text
GetCurrentTariffStop
SubscribeCurrentTariffStop
UnsubscribeCurrentTariffStop
CurrentTariffStop
```

However its chapter 3.1.2 still contains stale CurrentStopPoint-derived response/table labels, including:

```text
TicketValidationService.GetCurrentStopPointResponse
TicketValidationService.CurrentStopPointData
```

The official V2.2 XSD is internally consistent with:

```text
TicketValidationService.GetCurrentTariffStopResponse
TicketValidationService.CurrentTariffStopDataStructure
CurrentTariffStop
```

### V2.3 correction is only partial at document-label level

The V2.3 foreword/version history says chapter 3.1.2 was corrected to align with XSD V2.2.

The detailed V2.3 table body does improve the data-structure line to `CurrentTariffStopData`, but the checked PDF text still retains stale labels/captions such as:

```text
TicketValidationService.GetCurrentStopPointResponse
Table 1 Description of TicketValidationService.GetCurrentStopPointResponse
Table 2 Description of TicketValidationService.CurrentStopPointData
```

### V2.4 still carries the same stale labels/captions

The V2.4 PDF continues to show the current operation as `GetCurrentTariffStop` and the data as `CurrentTariffStop`, while the response/table captions still retain `GetCurrentStopPointResponse` / `CurrentStopPointData` wording.

Classification:

```text
finding_id: TVS-003
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: high
version_scope: V2.2, V2.3, V2.4 PDFs
validation_behavior: use GetCurrentTariffStopResponse / CurrentTariffStopDataStructure as defined by the selected XSD
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

No XSD change is proposed.

## 8. TVS-001 current-state recheck

Current official upstream master still contains the V2.4 top-level element:

```text
TicketValidationService.GetCurrentShortHaulStopsResponse
```

but the `TicketValidationServiceOperations` sequence omits that element.

Thus the prior TVS-001 observation remains reproducible in current upstream state.

Classification remains:

```text
finding_id: TVS-001
mismatch_kind: xsd_internal_operation_inventory
likely_source_issue: xsd_internal_consistency_candidate
classification_confidence: high for the structural observation
final_handling_bucket: local_compile_and_sample_validation_then_official_facing_review
```

Do not change the XSD during the audit.

## 9. Version-exact SDK routing matrix after this pass

```text
TVS document V2.1
  -> official IBIS-IP_TicketValidationService_V2.1.xsd
  -> Common V1.0
  -> Enumerations V1.0

TVS document V2.2
  -> official IBIS-IP_TicketValidationService_V2.2.xsd
  -> Common V2.2
  -> Enumerations V2.2

TVS document V2.3
  -> official historical route remains IBIS-IP_TicketValidationService_V2.2.xsd
  -> Common V2.2
  -> Enumerations V2.2
  -> branch-local TVS_V2.3 file is candidate/integration material only

TVS document V2.4
  -> public PDF requires new V2.4 service functionality
  -> dev/schema-integration currently uses TVS V2.4 + Common V2.4 + Enumerations V2.4 as candidate/integration pool
  -> current official upstream master differs in its enum include and remains a separate provenance fact
```

This matrix must be encoded explicitly in the later SDK resolver. It must not be derived with `schema filename version == PDF/service version` or `latest Common/Enums wins` logic.

## 10. Technical validation status

No local selected-pool XSD compilation or sample XML validation was completed in this pass.

The current runtime did not provide a local checkout/download path for the full dependency pools; therefore no compile-success statement is made.

Required later checks:

```text
V2.1 official pool compile
V2.2 official pool compile
V2.3 official routing sample validation using the V2.2 service XSD pool
candidate/integration V2.3 alias compile only if the SDK retains that alias
V2.4 candidate/integration pool compile
positive/negative CurrentStopPoint vs CurrentTariffStop cross-version samples
positive VehicleData.RouteDeviation sample using RouteDeviationEnumeration
V2.4 operation-inventory sample checks for TVS-001
```

## 11. Result

```text
Historical V2.1 XSD coverage is restored from an official release tag.
The V2.1 -> V2.2 rename and dependency transition are established.
TVS document V2.3 is proven to route officially to XSD V2.2, not to an identically numbered XSD.
The branch-local TVS V2.3 file is reclassified as candidate/integration material.
TVS-002 is extended to the full V2.1-V2.4 PDF chain.
TVS-003 is confirmed as a high-confidence PDF label/heading issue for V2.2-V2.4.
TVS-001 remains reproducible in current upstream master.
No XSD correction is made.
```
