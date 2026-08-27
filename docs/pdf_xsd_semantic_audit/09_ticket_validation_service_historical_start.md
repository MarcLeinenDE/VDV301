# TicketValidationService historical audit start

Status: historical audit restarted from the existing TVS V2.2/V2.3/V2.4 first pass; V2.1 official release provenance resolved and historical backfill prepared in this commit. Local XSD compilation and sample validation remain pending.

Scope:

```text
VDV 301-2-16 TicketValidationService V2.1 PDF
VDV 301-2-16 TicketValidationService V2.2 PDF
VDV 301-2-16 TicketValidationService V2.3 PDF
VDV 301-2-16 TicketValidationService V2.4 PDF
IBIS-IP_TicketValidationService_V2.1.xsd
IBIS-IP_TicketValidationService_V2.2.xsd
IBIS-IP_TicketValidationService_V2.3.xsd
IBIS-IP_TicketValidationService_V2.4.xsd candidate/integration variant in dev/schema-integration
```

This block does **not** start the TVS audit from zero. It explicitly continues from:

```text
docs/pdf_xsd_semantic_audit/03_tvs_v2_2_v2_3_v2_4_include_semantic_audit.md
```

and carries forward the already opened findings:

```text
TVS-001 - GetCurrentShortHaulStopsResponse missing from TicketValidationServiceOperations group in V2.4.
TVS-002 - VehicleData.RouteDeviation PDF type RouteDirectionEnumeration vs XSD RouteDeviationEnumeration.
```

## 1. Authority and source policy

Validation remains XSD-driven.

```text
Validation follows the selected service version's exact XSD family.
PDF differences are recorded as explanatory/provider-facing notes.
No latest-version substitution is allowed.
No XSD is corrected merely because PDF and XSD differ.
```

Historical XSD backfill follows:

```text
docs/pdf_xsd_semantic_audit/OFFICIAL_RELEASE_BACKFILL_POLICY.md
```

Only official `VDVde/VDV301` release tags may supply missing historical XSD files. Forks, pull requests and reconstructed schemas are not historical backfill sources.

## 2. Current branch baseline checked before this block

Verified starting branch state:

```text
branch: dev/schema-integration
start commit: 5116b09d81bbf78b2cb23b13436108b792f40330
last commit message: Add DoorStateService 08B handoff delta
```

Before this block the branch contained:

```text
IBIS-IP_TicketValidationService_V2.2.xsd
IBIS-IP_TicketValidationService_V2.3.xsd
IBIS-IP_TicketValidationService_V2.4.xsd
```

and did not contain:

```text
IBIS-IP_TicketValidationService_V2.1.xsd
```

No existing `09_ticket_validation_service_historical_start.md` was present.

## 3. V2.1 official release provenance and historical backfill

Official source verified:

```text
repository: VDVde/VDV301
tag: VDV-301-2.1
release commit: 585e0bea34b64887db4276f1c94d5f3e78f06c66
release tree: a8472530e840f7b365f6ba1075bfc09758ebda21
file: IBIS-IP_TicketValidationService_V2.1.xsd
blob SHA: f6497e6469b82ee19b185c4de749d13a7ca60bed
```

The V2.1 release tag contains the service XSD and therefore satisfies the official historical backfill policy.

Backfill handling in this commit:

```text
IBIS-IP_TicketValidationService_V2.1.xsd is added from the exact official release-tag blob.
The filename is unchanged.
The schema content is not edited.
The file is historical official release material, not candidate material.
```

This is a completeness/routing import for the integration branch. It is not an XSD correction and is not an upstream PR proposal.

## 4. Version-exact dependency pools observed so far

### TVS V2.1

Official V2.1 XSD includes:

```text
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

Selected pool for later technical validation:

```text
TicketValidationService V2.1
+ Common V1.0
+ Enumerations V1.0
```

The service/common version-number difference is a dependency fact, not an error.

### TVS V2.2

Official V2.2 XSD includes:

```text
IBIS-IP_common_V2.2.xsd
IBIS-IP_Enumerations_V2.2.xsd
```

Selected pool:

```text
TicketValidationService V2.2
+ Common V2.2
+ Enumerations V2.2
```

### TVS V2.3

Existing audit block 03 established:

```text
TicketValidationService V2.3
+ Common V2.2
+ Enumerations V2.2
```

No dependency-family change was observed from V2.2 to V2.3.

### TVS V2.4 in dev/schema-integration

Existing audit block 03 established the integration-branch candidate pool as:

```text
TicketValidationService V2.4
+ Common V2.4
+ Enumerations V2.4
```

Important status:

```text
The V2.4 branch variant remains candidate/integration material where it differs from current official upstream master.
Do not retroactively apply the V2.4 dependency pool to V2.1/V2.2/V2.3.
```

## 5. V2.1 -> V2.2 historical service delta

The official V2.1 service XSD uses:

```text
TicketValidationService.GetCurrentStopPointResponse
TicketValidationService.GetCurrentStopPointResponseStructure
TicketValidationService.CurrentStopPointDataStructure
CurrentStopPoint
```

The official V2.2 service XSD uses:

```text
TicketValidationService.GetCurrentTariffStopResponse
TicketValidationService.GetCurrentTariffStopResponseStructure
TicketValidationService.CurrentTariffStopDataStructure
CurrentTariffStop
```

The V2.2 PDF version history explicitly explains the semantic reason for the rename: `CurrentStopPoint` was used with different meanings in CustomerInformationService and TicketValidationService, so the TVS concept was renamed to `CurrentTariffStop`.

Result:

```text
This is a real versioned service-name transition.
The future SDK must route V2.1 payloads to the V2.1 names and V2.2+ payloads to the applicable later schema family.
Do not normalize V2.1 CurrentStopPoint into CurrentTariffStop before validation.
```

## 6. Existing TVS-001 carried forward

Existing finding:

```text
TVS-001 - V2.4 GetCurrentShortHaulStopsResponse exists as a top-level element and structure but is missing from TicketValidationServiceOperations.
```

Historical scope note:

```text
This remains a V2.4-specific XSD internal-consistency candidate because the short-haul operation was introduced in V2.4.
The V2.1 and V2.2 operation groups match their corresponding top-level service operation inventory for the checked historical stop/tariff-stop operation.
```

No XSD change is made in this block.

## 7. Existing TVS-002 historical evidence extended

Existing finding:

```text
TVS-002 - VehicleData.RouteDeviation PDF type name differs from XSD type name.
```

New historical evidence:

```text
V2.1 PDF: RouteDeviation is documented with type RouteDirectionEnumeration.
V2.1 XSD: RouteDeviation uses RouteDeviationEnumeration.

V2.2 PDF: RouteDeviation is documented with type RouteDirectionEnumeration.
V2.2 XSD: RouteDeviation uses RouteDeviationEnumeration.
```

The prior V2.4 audit already observed the same PDF/XSD direction there.

Initial historical classification:

```text
mismatch_kind: type
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high for V2.1/V2.2 evidence direction
validation_behavior: validate RouteDeviation against RouteDeviationEnumeration in the selected XSD family
```

The exact full version range, including an explicit V2.3 PDF recheck, is deferred to the detailed 09a pass rather than inferred.

## 8. TVS-003 candidate - stale V2.2 CurrentStopPoint response/table labels after tariff-stop rename

V2.2 PDF section and operation names use:

```text
GetCurrentTariffStop
SubscribeCurrentTariffStop
UnsubscribeCurrentTariffStop
CurrentTariffStopData
CurrentTariffStop
```

However, the same V2.2 detailed response area still contains stale labels/headings such as:

```text
TicketValidationService.GetCurrentStopPointResponse
TicketValidationService.CurrentStopPointData
```

The V2.2 table list repeats those stale `CurrentStopPoint` labels.

The official V2.2 XSD is internally consistent with the renamed tariff-stop vocabulary:

```text
TicketValidationService.GetCurrentTariffStopResponse
TicketValidationService.CurrentTariffStopDataStructure
CurrentTariffStop
```

The PDF version history itself says that `CurrentStopPoint` was renamed to `CurrentTariffStop`.

Initial classification:

```text
candidate_id: TVS-003
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: high
validation_behavior: use the exact V2.2 XSD names; do not accept stale PDF labels as aliases
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

No main-register entry is opened yet in this starter block. The detailed 09a pass should confirm how V2.3 corrected chapter 3.1.2 and then decide whether TVS-003 is formally opened/closed as a historical PDF documentation issue.

## 9. Subscription modelling note

The TVS PDFs describe service-specific Subscribe/Unsubscribe concepts, while the service XSD operation group is focused on concrete data/request/response elements. This resembles previously observed generic subscription modelling in CIS/JIS and must not be reclassified as a TVS defect without a cross-service review.

The separate CIS subscription/HTTP analysis is background only and is not used here as TVS-specific executable authority.

## 10. Findings register continuity

The existing source of record for TVS-001 and TVS-002 is currently:

```text
docs/pdf_xsd_semantic_audit/03_tvs_v2_2_v2_3_v2_4_include_semantic_audit.md
```

The current `findings.md` does not yet consolidate TVS-001/TVS-002. Do not allocate replacement IDs or duplicate them. A TVS findings-register addendum should be created only after the historical 09a pass has fixed the version scope and TVS-003 disposition.

## 11. Technical validation backlog for the historical chain

No local compilation or sample validation was run as part of this starter block.

Carry forward / add:

```text
TVS-VB-001: Compile V2.1 with Common V1.0 + Enumerations V1.0.
TVS-VB-002: Compile V2.2 with Common V2.2 + Enumerations V2.2.
TVS-VB-003: Compile V2.3 with Common V2.2 + Enumerations V2.2.
TVS-VB-004: Compile the V2.4 integration/candidate pool with Common V2.4 + Enumerations V2.4.
TVS-VB-005: Positive/negative V2.1 vs V2.2 sample pair for GetCurrentStopPointResponse vs GetCurrentTariffStopResponse.
TVS-VB-006: VehicleData sample using RouteDeviationEnumeration; negative check for any payload modelling that follows the PDF-only RouteDirectionEnumeration type assumption.
TVS-VB-007: V2.4 operation inventory comparison for GetCurrentShortHaulStopsResponse vs TicketValidationServiceOperations.
```

Do not mark any of these pools or samples as technically validated until the checks are actually executed.

## 12. Result and next file

Result of this starter block:

```text
The previous TVS audit is preserved and extended, not restarted.
V2.1 official XSD provenance is resolved from release tag VDV-301-2.1.
V2.1 is restored to the integration branch as historical official release material.
V2.1 -> V2.2 CurrentStopPoint -> CurrentTariffStop transition is established as a versioned schema change.
TVS-001 is carried forward as V2.4-specific.
TVS-002 gains historical V2.1/V2.2 evidence.
TVS-003 is introduced only as a candidate for stale V2.2 PDF labels/headings.
No XSD correction was made.
No PR, comment or merge was created.
No local XSD compilation/sample validation was claimed.
```

Next recommended file:

```text
docs/pdf_xsd_semantic_audit/09a_ticket_validation_service_v2_1_v2_2_history_and_pdf_xsd_first_pass.md
```
