# Common findings register addendum after service-level audit discoveries

Status: supplemental Common register for findings discovered after the original CE-001..CE-017 first-pass chain. Keep separate until the main findings register is consolidated.

Authority rule:

```text
Validation follows the selected Common XSD version and selected authority/variant.
PDF table differences are explanatory evidence only.
No schema change is implied by opening or confirming a finding.
Candidate same-path semantic variants require explicit opt-in and never silently replace official release bytes.
```

## CE-018 - ServiceIdentificationWithStateList cardinality PDF 1:* vs XSD 0:*

State: executable-confirmed historical cardinality mismatch.

Classification:

```text
mismatch_kind: cardinality
likely_source_issue: cardinality_mismatch_candidate
subclassification: xsd_more_permissive_than_pdf
classification_confidence: very high
version_scope: executable XSD behaviour confirmed V1.0, V2.0, V2.1, V2.2, V2.3, V2.4; checked PDF 1:* wording confirmed V2.1-V2.4
validation_behavior: XSD permits empty list
final_handling_bucket: official_documentation_or_schema_alignment_review_candidate
```

PDF evidence:

```text
Checked Common documents V2.1, V2.2, V2.3 and V2.4 each show ServiceIdentificationWithStateList / ServiceIdentificationWithState as 1:*.
```

Static XSD evidence:

```text
Checked Common XSD family defines:
ServiceIdentificationWithState minOccurs="0" maxOccurs="unbounded".
```

Executable evidence:

```text
GitHub Actions run: 33109768872
head tested: 2298f1297e9d2b00aacbf244f39f6c73587f713e
tool: tools/validate_ce018_service_identification_with_state_list.py
result: PASS
```

Executed versions:

```text
Common V1.0  empty list PASS; one-item list PASS
Common V2.0  empty list PASS; one-item list PASS
Common V2.1  empty list PASS; one-item list PASS
Common V2.2  empty list PASS; one-item list PASS
Common V2.3  empty list PASS; one-item list PASS
Common V2.4  empty list PASS; one-item list PASS
```

Impact:

```text
The executable Common XSD family consistently permits zero ServiceIdentificationWithState items.
For the checked V2.1-V2.4 documents, this conflicts with the documented 1:* cardinality.
SystemMonitoringService.GetServiceStatusResponseData is a direct consumer of this list structure.
```

Handling:

```text
Validation follows the selected XSD and must accept the empty list where the selected Common XSD does.
The SDK may emit a documentation-discrepancy diagnostic, but must not reject the XSD-valid empty list solely because of the PDF 1:* wording.
No XSD change is made in the audit branch.
```

## CE-019 - ServiceIdentificationWithStateList item type/reference PDF vs XSD

State: native-text cross-version discrepancy confirmed; visible-page confirmation still pending.

Classification:

```text
mismatch_kind: type/reference
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high from native PDF text plus exact XSD cross-check; visual closure pending
version_scope: checked documentation V2.1-V2.4; exact XSD type checked in Common family
validation_behavior: exact XSD type ServiceIdentificationWithStateStructure
final_handling_bucket: unresolved_keep_open
```

PDF evidence:

```text
The ServiceIdentificationWithStateList row names the item ServiceIdentificationWithState but the associated referenced structure/type is ServiceSpecificationWithState.
The fresh byte-pinned Common V2.3 native-text read independently reconfirmed this wording.
```

XSD evidence:

```text
The list element is ServiceIdentificationWithState with type ServiceIdentificationWithStateStructure.
```

Semantic context:

```text
ServiceIdentificationWithState includes the system-wide ServiceIdentification including the device on which the service runs.
ServiceSpecificationWithState describes a service specification/state without the same system-wide identification wrapper.
The list is described as a list of unique services and their state in the system, which is semantically consistent with the XSD type.
```

Visual-check note:

```text
Direct screenshots of the relevant VDV PDF pages repeatedly returned cache-miss for V2.3 and control attempts against V2.2/V2.4.
Do not promote this finding to visually closed until a reliable renderer is available.
```

Impact:

```text
Validation follows ServiceIdentificationWithStateStructure.
Do not accept ServiceSpecificationWithStateStructure as an automatic alias based on PDF wording.
```

## CE-020 - Common V2.3 InternationalTextType official XSD vs PDF / PR #30 candidate

State: original-PDF table mismatch and executable official/candidate behavioural difference confirmed.

Classification:

```text
mismatch_kind: type + same-path authority collision
likely_source_issue: xsd_typo_candidate / official_documentation_or_schema_alignment_review_candidate
classification_confidence: very high for PDF/XSD/candidate byte and instance-shape difference
version_scope: Common V2.3
final upstream disposition: intentionally undecided during audit
```

Official release evidence:

```text
VDVde/VDV301 tag: VDV-301-2.3
IBIS-IP_common_V2.3.xsd
blob: 0d8926c4063c12de9a5e68b6f0addaab35a55dc1

InternationalTextType.Value    -> xs:string
InternationalTextType.Language -> xs:language
```

Candidate evidence:

```text
Open upstream PR: VDVde/VDV301 #30 "Fix the definition of InternationalTextType"
PR head: d1f1bf87b20d0cfb4b658555c9bd2779809c1f6d
candidate blob: 456a7db179ce14bc3f04e2bc05e42e16545fb0c5

InternationalTextType.Value    -> IBIS-IP.string
InternationalTextType.Language -> IBIS-IP.language
```

Original PDF visual evidence:

```text
Official VDV 301-2-1 V2.3
printed page 12 / PDF page index 11
Table 17 InternationalTextType

Value      1:1  IBIS-IP.string
Language   1:1  IBIS-IP.language
ErrorCode  0:1  ErrorCodeEnumeration
```

The original visible VDV table therefore agrees with the PR #30 candidate type names and differs from the exact official release XSD blob.

Executable evidence:

```text
Evidence ID: EV-106
GitHub Actions run: 33169314332
tool: tools/validate_common_v23_schema_variant.py
result: PASS
```

Both isolated dependency pools compile, including CustomerInformationService V2.3 against each Common variant.

Observed instance-shape difference:

```text
official Common V2.3:
  flat InternationalTextType instance    VALID
  wrapped IBIS-IP.* instance             INVALID

PR #30 candidate overlay:
  flat InternationalTextType instance    INVALID
  wrapped IBIS-IP.* instance             VALID
```

The PR #30 change is therefore not merely documentation cleanup: `IBIS-IP.string` and `IBIS-IP.language` are wrapper complex types and change the accepted XML instance shape.

Superbranch handling:

```text
Root IBIS-IP_common_V2.3.xsd stores the exact official VDV-301-2.3 blob.
PR #30 bytes are retained separately at:
  schema_variants/upstream_pr_30/IBIS-IP_common_V2.3.xsd

Variant registry:
  audit_registry/schema_variant_registry_v0.1.json

SDK overlay manifest:
  sdk_manifest/schema_variant_overlays_v0.1.json
```

Validation behaviour:

```text
authority=official, Common@2.3
  -> use official blob 0d8926c...

authority=candidate, schema_variant_id=common-v2.3-upstream-pr30
  -> assemble isolated pool and overlay blob 456a7db...

Never latest-wins.
Never silently relabel PR #30 as official.
Never delete either semantic variant while the collision exists.
```

Execution status:

```text
The post-split repository pool was revalidated in run 33169314332.
All 50 current root XSDs compiled successfully.
EV-106 separately confirms the explicit candidate overlay and its observable InternationalTextType behaviour.
```

Handling remains conservative:

```text
The audit confirms the mismatch but does not modify either XSD.
The official VDV-301-2.3 release bytes remain the default executable authority.
The PR #30 variant remains an explicit candidate until an upstream authority change is separately established.
```

## CE-021 - LogMessage `MessageBody` PDF vs XSD `Message`

State: native-text and exact-XSD cross-version mismatch confirmed; visible-page closure pending.

Classification:

```text
mismatch_kind: element_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
version_scope: checked V2.2, V2.3, V2.4 PDF and XSD
validation_behavior: XSD requires Message
final_handling_bucket: official_documentation_or_schema_alignment_review_candidate
```

PDF evidence:

```text
LogMessage:
  MessageProvider 1:1 +DeviceSpecification
  MessageBody     1:1 +Message
```

The checked V2.2, byte-pinned V2.3 and V2.4 native PDF text all use `MessageBody`.

XSD evidence:

```text
LogMessageStructure:
  MessageProvider
  Message type="MessageStructure"
```

Checked V2.2/V2.3/V2.4 Common XSDs use `Message`.

Impact / handling:

```text
<MessageBody> is not an alias.
Validation follows XSD and requires <Message>.
Do not synthesize PDF-oriented aliases in the SDK.
```

## CE-022 - ServiceIdentification `ServiceName` PDF vs XSD `Service`

State: native-text and exact-XSD cross-version mismatch confirmed; visible-page closure pending.

Classification:

```text
mismatch_kind: element_name
likely_source_issue: pdf_table_copy_or_naming_error_candidate
classification_confidence: high
version_scope: checked V2.2-V2.4
validation_behavior: XSD requires Service
final_handling_bucket: official_documentation_or_schema_alignment_review_candidate
```

PDF evidence:

```text
ServiceIdentification:
  ServiceName 1:1 +ServiceSpecification
  Device      1:1 +DeviceSpecification
```

XSD evidence:

```text
ServiceIdentificationStructure:
  Service type="ServiceSpecificationStructure"
  Device  type="DeviceSpecificationStructure"
```

Context:

```text
ServiceSpecificationStructure itself legitimately contains an inner ServiceName.
That nested field does not make ServiceName the valid outer ServiceIdentification element name.
```

Impact / handling:

```text
<ServiceName> at ServiceIdentification level is rejected by the exact XSD.
Use <Service>.
```

## CE-023 - Common V2.3 duplicate/corrupt second NetexMode table

State: V2.3-specific PDF copy/paste table error confirmed in native text; visual closure pending.

Classification:

```text
mismatch_kind: duplicate_or_copy_paste_table
likely_source_issue: pdf_table_error_candidate
classification_confidence: high
version_scope: Common V2.3 in checked V2.2/V2.3/V2.4 chain
validation_behavior: no XSD defect implied
final_handling_bucket: documentation_correction_candidate
```

Evidence:

```text
V2.3 section 1.18 correctly describes NetexMode with main-mode/submode choices.

Later V2.3 section 2.34 is again titled NetexMode but its table body is:
  Message-ID
  TimeStamp
  MessageType
  MessageText
```

Cross-version context:

```text
V2.2: after Message comes 2.34 Point.
V2.4: after Message comes 2.34 Point.
```

XSD context:

```text
Official Common V2.3 NetexMode uses:
  PtMainMode / PrivateMainMode
  PtSubmodeChoiceGroup / PrivateSubmodeChoiceGroup
```

Impact / handling:

```text
Do not derive NetexMode XML shape from the corrupt second V2.3 table.
Validation follows the selected XSD.
```

## CE-024 - UnsubscribeResponse `Active` PDF 0:1 vs XSD 1:1

State: static cross-version cardinality mismatch confirmed; executable sample not yet separately assigned.

Classification:

```text
mismatch_kind: cardinality
subclassification: xsd_stricter_than_pdf
classification_confidence: high
version_scope: checked V2.2-V2.4
validation_behavior: Active is required by XSD
final_handling_bucket: official_documentation_or_schema_alignment_review_candidate
```

PDF evidence:

```text
UnsubscribeResponse:
  Active                0:1
  OperationErrorMessage 0:1
```

XSD evidence:

```text
UnsubscribeResponseStructure:
  Active                minOccurs default 1
  OperationErrorMessage minOccurs 0
```

Impact:

```text
A response without Active may appear valid from the PDF table but fails XSD validation.
```

## CE-025 - subscription request `Reply-Path` PDF vs XSD `ReplyPath`

State: historical PDF/XSD element-name mismatch confirmed; corrected in checked V2.4 documentation.

Classification:

```text
mismatch_kind: element_name
classification_confidence: high
version_scope: checked V2.2-V2.3; documentation corrected V2.4
validation_behavior: XSD requires ReplyPath
final_handling_bucket: historically_corrected_documentation_issue
```

PDF evidence:

```text
V2.2/V2.3 SubscribeRequest and UnsubscribeRequest tables:
  Reply-Path
```

XSD evidence:

```text
SubscribeRequestStructure:
  ReplyPath

UnsubscribeRequestStructure:
  ReplyPath
```

V2.4 PDF uses `ReplyPath`.

Impact / handling:

```text
<Reply-Path> does not become an alias for historical validation.
Use the selected XSD element <ReplyPath>.
```

## CE-026 - BeaconPoint `Description` PDF vs V2.3 XSD `Desciption`

State: historical spelling mismatch confirmed; corrected in Common V2.4 XSD.

Classification:

```text
mismatch_kind: element_name_spelling
classification_confidence: high
version_scope: Common V2.3 historical mismatch; corrected in Common V2.4 XSD
validation_behavior_v2_3: XSD requires Desciption
final_handling_bucket: historically_corrected_schema_issue
```

V2.3 PDF evidence:

```text
BeaconPoint:
  Description 0:* +InternationalTextType
```

Official V2.3 XSD:

```text
BeaconPointStructure:
  Desciption
```

Later correction evidence:

```text
Common V2.4 XSD:
  BeaconPointStructure -> Description
```

Important separation:

```text
TSPPoint still uses Desciption in V2.4 XSD and remains tracked separately as CE-017.
```

Impact / handling:

```text
For official Common V2.3, validation still follows the historical XSD spelling <Desciption>.
The later V2.4 correction does not retroactively change V2.3.
```

## COMMON V1.0 / public V1.x Deep Read scope extension — 2026-08-30

Source: byte-pinned official 05/2017 VDV 301-2-1 publication, SHA-256 `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf`.
Exact executable authority remains official Common V1.0 `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c` plus
Enumerations V1.0 `a9bea5bc73003ed91ded8519db06c32c4067831d`.

EV-117 run `33279461529` PASS.

Existing IDs revalidated/refined for V1.x where applicable:

```text
CE-005: V1x_scope_context_verified_with_EV-117_exact_V1.0_type_and_cardinality_support
CE-007: V1x_scope_executable_enum_lexeme_boundaries_confirmed_EV-117
CE-012: V1x_scope_executable_empty_list_confirmed_EV-117
CE-013: V1x_scope_executable_choice_and_name_boundary_confirmed_EV-117
CE-014: V1x_scope_exact_V1.0_anonymous_DataVersion_0star_declaration_confirmed_EV-117
CE-015: V1x_scope_visible_pdf_and_exact_XSD_case_boundary_confirmed_EV-117
CE-016: V1x_scope_visible_pdf_and_exact_XSD_spelling_boundary_confirmed_EV-117
CE-017: V1x_scope_executable_Description_vs_Desciption_boundary_confirmed_EV-117
CE-018: V1x_scope_executable_empty_list_confirmed_EV-117
CE-019: V1x_scope_visible_pdf_type_reference_and_exact_XSD_type_confirmed_EV-117
CE-021: V1x_scope_visible_pdf_and_exact_XSD_Message_declaration_confirmed_EV-117
CE-022: V1x_scope_executable_outer_Service_vs_ServiceName_boundary_confirmed_EV-117
CE-025: V1x_scope_visible_pdf_and_exact_XSD_ReplyPath_declaration_confirmed_EV-117
CE-026: V1x_scope_executable_Description_vs_Desciption_boundary_confirmed_EV-117
```

This does **not** visually close unresolved V2.x portions of CE-019/021/022/etc.;
it only establishes the V1.x scope from the independently pinned source.

New unique V1.x Deep Read findings are `DRCOM10-001..DRCOM10-007`; detailed machine-
readable evidence is in `audit_registry/deep_read_findings_delta_common_v10_2026-08-30.json`.

Validation continues to follow the exact selected XSD family. No alias is synthesized
from PDF spelling, casing, cardinality or type-reference wording.

## COMMON V2.0 Deep Read scope extension — 2026-08-30

Source: byte-pinned official V2.0 VDV 301-2-1 publication, SHA-256 `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088`.
Exact executable authority: official tag `VDV-301-2.0`, Common `8608e3dcd665c197c34da7f6ec6af5a3758da164` plus
Enumerations `27e3c183b00381d959622d13c10543123af8eef6`. EV-118 run `33280224191` PASS.

Existing IDs revalidated/refined:

```text
CE-005: V2.0_scope_visible_table_and_version_history_plus_exact_0to1_XSD_declaration_EV-118
CE-007: V2.0_scope_executable_enum_lexeme_boundaries_confirmed_EV-118
CE-012: V2.0_scope_executable_empty_DeviceSpecificationWithStateList_confirmed_EV-118
CE-013: V2.0_scope_executable_optional_choice_and_SpecificPoint_name_boundary_EV-118
CE-014: V2.0_scope_executable_empty_DataVersionList_confirmed_EV-118
CE-015: V2.0_scope_visible_pdf_and_exact_XSD_FareZone_case_boundary_confirmed_EV-118
CE-016: V2.0_scope_visible_pdf_and_exact_XSD_GlobalCardStausID_boundary_confirmed_EV-118
CE-017: V2.0_scope_executable_TSPPoint_Description_vs_Desciption_boundary_EV-118
CE-018: V2.0_scope_visible_pdf_1star_plus_executable_empty_ServiceIdentificationWithStateList_EV-118
CE-019: V2.0_scope_visible_pdf_type_reference_plus_exact_ServiceIdentificationWithStateStructure_EV-118
CE-021: V2.0_scope_visible_MessageBody_vs_exact_XSD_Message_declaration_EV-118
CE-022: V2.0_scope_executable_outer_Service_vs_ServiceName_boundary_EV-118
CE-025: V2.0_scope_visible_Reply-Path_vs_exact_ReplyPath_declarations_EV-118
CE-026: V2.0_scope_executable_BeaconPoint_Description_vs_Desciption_boundary_EV-118
DRCOM10-002: V2.0_scope_executable_DataAcceptedResponse_choice_boundary_EV-118
DRCOM10-003: V2.0_scope_executable_empty_ServiceSpecificationWithStateList_EV-118
DRCOM10-004: V2.0_scope_exact_JourneyStop_Announcement_FareZone_0to1_declarations_EV-118
DRCOM10-005: V2.0_scope_refined_child_name_facet_persists_type_facet_aligned_exact_XSD_EV-118
DRCOM10-006: V2.0_scope_executable_DoorCountingObjectClass_lexemes_EV-118
DRCOM10-007: V2.0_scope_context_verified_grouped_editorial_residue
```

New unique finding:

```text
DRCOM20-001 InternationalTextType PDF IBIS-IP.string/IBIS-IP.language vs exact
             V2.0 XSD xs:string/xs:language; executable instance-shape difference EV-118
```

`CE-020` remains V2.3-specific because it additionally tracks PR #30 and the explicit
same-path authority collision. No V2.0 candidate overlay is inferred.

Validation follows the exact selected V2.0 XSD family; no PDF alias or multiplicity is synthesized.
