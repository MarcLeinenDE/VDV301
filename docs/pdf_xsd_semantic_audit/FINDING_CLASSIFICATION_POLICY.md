# Finding classification policy

Status: adopted as audit policy; mandatory evidence gate added 2026-08-29.

This document defines how PDF/XSD audit findings are grouped before final handling decisions are made.

The goal is to avoid treating every mismatch as the same kind of defect. Some findings are likely XSD spelling defects, some are likely PDF/table documentation defects, some are modelling differences, and some are only routing/provenance gaps.

## Mandatory evidence gate before classification

Every finding is subject to:

```text
docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md
```

Classification is downstream of evidence. A difference must not be called a defect merely because two extracted strings, rows or schema declarations look different.

Before a finding may be called `confirmed`, the auditor must establish, where applicable:

```text
- the visible original PDF context;
- the authoritative definition of any material notation or specialized term;
- the exact selected XSD family and dependency route;
- the complete surrounding semantic/grouping context;
- the strongest plausible counter-explanation and the result of trying to disprove the finding;
- executable behaviour when the claim concerns accepted/rejected XML and testing is technically practical.
```

If a material evidence step is missing, confidence must remain candidate/unresolved/review-required. Do not compensate with inference.

## Core authority rule

```text
Validation follows the selected XSD family.
PDF differences are recorded as explanatory/provider-facing notes, not as executable validation authority.
```

This rule does not prevent later official-facing correction proposals. It only means that the future tool/SDK must validate exactly against the selected schema unless and until an official corrected schema exists.

## Required classification fields

Every finding should eventually have these fields, either directly in the main register or in a generated consolidation matrix.

```text
finding_id
service_or_common_scope
version_scope
mismatch_kind
likely_source_issue
classification_confidence
validation_behavior
final_handling_bucket
notes
```

For findings created or materially re-evaluated after adoption of the evidence gate, also retain or make reconstructable:

```text
pdf_source_id_or_publication
page_or_section
original_visual_status
notation_or_term_definition_source
selected_xsd_family
schema_identity_or_authority
full_context_checked
counter_hypothesis_checked
executable_evidence_id_or_reason_not_applicable
confidence_state
sdk_eligibility
```

## Confidence/promotion discipline

Use this progression conceptually:

```text
candidate_observation
source_verified
context_verified
executable_confirmed      # when executable behaviour is material
remediation_ready         # only after a later explicit remediation decision
```

A finding does not need to reach the final state. It is preferable to retain an unresolved candidate than to create a false confirmed finding.

`classification_confidence: high` is not permitted solely because PDF and XSD text differ. High confidence requires the relevant original-source, definition and context checks to have passed.

## mismatch_kind values

```text
spelling
case
cardinality
type
operation_or_element_name
schema_family_or_provenance
service_modelling
wrapper_modelling
value_set
ok_note
unresolved
```

## likely_source_issue values

### xsd_typo_candidate

Use this when the XSD spelling looks typo-like in normal language or VDV context and the PDF or neighbouring schema semantics point to a different intended spelling.

Typical evidence:

```text
The XSD spelling is visibly typo-like.
The PDF uses the semantically expected spelling.
Neighbouring structures or later versions use the expected spelling.
The element/type meaning is otherwise clear.
```

Examples currently matching or potentially matching this group:

```text
LS-001: HoriziontalDilutionOfPrecision vs HorizontalDilutionOfPrecision.
CE-016: GlobalCardStausID vs GlobalCardStatusID.
CE-017: TSPPoint Desciption vs Description, pending visual PDF confirmation.
```

Handling rule:

```text
Do not silently correct validation.
Validate against the XSD spelling.
Mark as post-audit official XSD correction / clarification candidate only after local compile/sample validation and source review.
```

### pdf_table_or_documentation_error_candidate

Use this when the XSD appears semantically consistent with the broader VDV301 model, while the PDF table, wording, value spelling or casing appears inconsistent.

Typical evidence:

```text
The XSD value or element is consistent across schema history.
The version history supports the XSD direction.
The PDF table conflicts with its own surrounding text or another table.
The mismatch is a case/value/table wording issue rather than an obviously broken schema identifier.
```

Examples currently matching or potentially matching this group:

```text
CE-007: common enumeration case differences such as Valid/valid, Air/air, Other/other.
CE-008: submode case differences such as Unknown/unknown and miniCab/minicab.
CE-009: specialRail in PDF vs specialTrain in XSD, pending final semantic review.
CIS-005: MyOwnVehicleMode type differs between CIS PDF table contexts while the XSD uses one shared VehicleInformationGroup.
```

Handling rule:

```text
Do not change XSD based only on PDF table wording.
Validate against XSD.
Use provider-facing explanations and later decide whether an official documentation clarification is appropriate.
```

### pdf_label_or_heading_error_candidate

Use this for operation/table headings where the detailed wording appears shortened, stale or inconsistent, but the XSD element names are coherent.

Examples:

```text
CIS-003: GetCurrentConnectionInformation vs GetCurrentConnectionResponse wording.
CIS-004: RetrievePartialStopSequence vs RetrievePartialStopRequest wording.
JIS-004: RetrieveAllRoutesPerLine / SetBlockNumberRequest table-label candidate.
JIS-005: SpecificGNSSPointInformationData vs SpecificGNSSPointInformation naming.
```

Handling rule:

```text
Do not rename schema elements based on table heading wording.
Validate against XSD and keep provider-facing notes.
```

### cardinality_mismatch_candidate

Use this where PDF cardinality and XSD cardinality differ **after the PDF notation has been resolved from its authoritative definition**.

A leading choice marker or other table convention must not be interpreted as cardinality without first checking the VDV notation definition and the complete visible grouping.

Subclassification:

```text
xsd_more_restrictive_than_pdf
xsd_more_permissive_than_pdf
unresolved_cardinality_direction
```

Examples:

```text
CE-005: TripInformation AdditionalTextMessage PDF 0:* vs XSD non-repeatable / numbered fields.
CE-011: TransportMode / ConnectionMode PDF 0:* vs XSD 0:1.
CE-012: DeviceSpecificationWithStateList PDF 1:* vs XSD 0:*.
CE-014: DataVersionList PDF 1:* vs XSD 0:*.
JIS-003: ListAllLineInformation LineInformation PDF 1:* vs XSD 1:1.
```

Handling rule:

```text
Validate against XSD.
Add local positive/negative samples.
Only propose a schema/document correction after service-impact review.
```

### service_modelling_or_generic_response_candidate

Use this when PDF operation concepts are present but XSD modelling appears to use shared/generic structures outside the local service group.

Examples:

```text
CIS-002: Subscribe/Unsubscribe concepts vs local CIS operation group.
JIS-001: Subscribe/Unsubscribe concepts vs local JIS operation group.
JIS-002: Set* requests vs generic DataAcceptedResponseStructure.
```

Handling rule:

```text
Do not classify as schema defect until cross-service modelling is reviewed.
Preserve the selected service XSD behaviour.
```

### schema_family_or_provenance_gap

Use this where a PDF version exists but no version-exact XSD mapping is confirmed.

Example:

```text
CIS-001: CustomerInformationService V1.1 public PDF without confirmed version-exact CIS V1.1 XSD.
```

Handling rule:

```text
Do not silently map to a neighbouring version.
Document exact routing status for the future tool/SDK.
```

### ok_with_note

Use this when a suspected discrepancy is resolved as aligned or intentionally service-specific.

Examples:

```text
CE-001: Common V2.3 intentionally uses Enumerations V2.2.
LS-002: DistanceLocationService Odometer-Pulses is identical in PDF and XSD.
LS-003: Location services use different wrapper styles by service.
```

Handling rule:

```text
No correction candidate.
Carry the exact behaviour into the executable validation matrix.
```

## final_handling_bucket values

```text
no_action_note
provider_facing_warning
local_validation_required
official_pdf_documentation_clarification_candidate
official_xsd_correction_candidate
official_schema_family_clarification_candidate
unresolved_keep_open
```

No finding may enter an official correction candidate bucket solely from a candidate observation. The evidence gate and later explicit remediation review must both be satisfied.

## Inference discipline

A finding may say `likely XSD typo` or `likely PDF table error`, but only when the evidence is stated. Do not hide the inference.

Use wording like:

```text
Classification: likely XSD typo candidate based on PDF spelling and semantic context.
Classification: likely PDF documentation/table issue based on XSD consistency and surrounding VDV301 semantics.
```

Avoid wording like:

```text
The XSD is wrong.
The PDF is wrong.
```

until final local validation and official-facing review are complete.

For every non-trivial inference, record the strongest plausible alternative explanation considered. A finding that has not survived a deliberate disproof attempt is not fully confirmed.

## Tool/SDK behaviour

For the future validation tool/SDK:

```text
Always validate against the selected XSD version family.
Emit explanatory diagnostics when a known PDF/XSD discrepancy may explain a provider payload.
Do not auto-normalize case, spelling or element names.
Do not substitute a corrected-looking spelling unless a corrected official schema exists.
```

Additionally:

```text
candidate/unresolved findings must never cause accept/reject decisions;
source/context-verified findings may provide explanatory diagnostics only;
claims about executable XML behaviour should be executable-confirmed before being encoded as SDK behaviour knowledge;
no finding automatically authorizes a schema override or remediation.
```
