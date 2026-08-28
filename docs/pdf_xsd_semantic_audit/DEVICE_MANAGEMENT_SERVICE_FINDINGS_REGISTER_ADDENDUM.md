# DeviceManagementService findings register addendum

Status: V2.0-V2.4 semantic/provenance first-pass chain complete; byte-pinned DMS V2.2 and DMS V2.4 Deep Read Pass 2 complete textually with EV-107/EV-108; visual closure remains pending where noted.

Authority rule:

```text
Validation follows the selected exact DMS XSD family.
PDF differences are explanatory/provider-facing evidence, not schema rewrites.
Historical corrections are not back-applied to older profiles.
Candidate/integration V2.4 schema material remains candidate/integration unless separately established as official release authority.
```

## DMS-001

```text
classification: service_modelling_or_generic_response_candidate
scope: V2.0
observation: public operation inventory includes generic Subscribe/Unsubscribe and device Activate/Deactivate/Restart operations not represented completely by V2.0 service-XSD group/global elements
validation: exact V2.0 XSD only; technical generic-operation modelling review pending
```

## DMS-002

```text
classification: pdf_table_or_documentation_error_candidate
scope: V2.0 document
observation: literal unresolved cross-reference strings occur repeatedly in DMS descriptions
validation impact: none
```

## DMS-003

```text
classification: ok_with_note
scope: historical V2.0/V2.1/V2.2 -> V2.4 correction
observation: 10:* ErrorMessage is PDF/XSD-aligned in V2.0, V2.1 and byte-pinned V2.2; V2.4 public PDF and candidate/integration XSD use 0:*
validation: do not retroactively relax older profiles
fresh V2.2 evidence: deep_read/DMS_V2.2.md
fresh V2.4 evidence: deep_read/DMS_V2.4.md / EV-108
```

## DMS-004

```text
classification: ok_with_note
scope: historical V2.1/V2.2 -> V2.4 correction
observation: InstallUpdate UpdateID/UpdateTimestamp/UpdateURL are required in both V2.1 and byte-pinned V2.2 PDF/XSD; V2.4 public PDF and candidate/integration XSD make them optional
validation: do not retroactively relax V2.1/V2.2
fresh V2.2 evidence: deep_read/DMS_V2.2.md
fresh V2.4 evidence: deep_read/DMS_V2.4.md / EV-108
```

## DMS-005 - GetDeviceStatusInformation response-data branch name

State: PDF/XSD element-name mismatch, executable XSD declaration confirmed by EV-107 and persistence against the candidate/integration V2.4 XSD confirmed by EV-108.

Classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: very high
version_scope: DMS V2.2 and checked V2.4 public PDF
validation_behavior: exact selected XSD branch name required
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

V2.2 PDF evidence:

```text
Table 17 response choice branch a:
  DeviceManagementService.DeviceStatusInformationResponseData
```

Exact official DMS V2.2 XSD:

```text
DeviceManagementService.GetDeviceStatusInformationResponseStructure
  choice
    DeviceManagementService.GetDeviceStatusInformationResponseData
    OperationErrorMessage
```

EV-107:

```text
run: 33181833930
result: PASS
PDF-only non-Get branch spelling absent from exact V2.2 XSD
```

V2.4 continuity:

```text
Official public V2.4 PDF retains DeviceManagementService.DeviceStatusInformationResponseData.
Candidate/integration V2.4 XSD uses DeviceManagementService.GetDeviceStatusInformationResponseData.
EV-108 run 33182963733: PASS.
```

Handling:

```text
Do not treat DeviceManagementService.DeviceStatusInformationResponseData as an alias.
Validation follows the exact selected XSD branch name.
```

## DMS-006 - DeviceStatus PDF omits two V2.2 XSD-required fields

State: historical V2.2 structure/cardinality mismatch; resolved/aligned for the checked V2.4 public-PDF/candidate-XSD profile.

Classification:

```text
mismatch_kind: cardinality / structure omission
likely_source_issue: pdf_table_or_documentation_error_candidate with later alignment evidence
classification_confidence: very high
version_scope: DMS V2.2 historical profile; corrected/aligned in checked V2.4 profile
validation_behavior: V2.2 XSD requires four DeviceStatus fields; V2.4 candidate makes impact/priority optional
final_handling_bucket: official_documentation_or_schema_alignment_review_candidate
```

V2.2 PDF table 20:

```text
DeviceStatusName 1:1
DeviceStatusFlag 1:1
```

Exact DMS V2.2 XSD:

```text
DeviceStatusName     required
DeviceStatusFlag     required
DeviceStatusImpact   required
DeviceStatusPriority required
```

EV-107 verifies all four declarations have effective `minOccurs=1`.

V2.4 correction/alignment:

```text
Official public V2.4 PDF:
  DeviceStatusName      1:1
  DeviceStatusFlag      1:1
  DeviceStatusImpact    0:1
  DeviceStatusPriority  0:1

Candidate/integration V2.4 XSD:
  name/flag required
  impact/priority optional

EV-108 confirms the candidate-XSD declaration state.
```

Impact:

```text
A producer implementing only the V2.2 PDF table can emit an XML structure that is incomplete for the selected V2.2 XSD.
The V2.4 correction does not rewrite V2.2 validation semantics.
```

## DMS-007 - InstallUpdate UpdateTimestamp `GetUpdateStates` vs `GetUpdateHistory`

State: PDF operation/reference typo confirmed against exact V2.2 XSD and persists in the checked V2.4 public PDF; EV-107/EV-108 confirm the respective XSD annotation.

Classification:

```text
mismatch_kind: operation_or_element_name / reference
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: very high
version_scope: DMS V2.2 and checked V2.4 public PDF
validation_behavior: no direct XML cardinality/type effect; operation resolver must not invent GetUpdateStates
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

V2.2/V2.4 PDF wording:

```text
UpdateTimestamp:
  Timestamp used for GetUpdateStates and RetrieveUpdateState responses and for logging
```

Exact V2.2 and candidate/integration V2.4 XSD annotations use:

```text
GetUpdateHistory
RetrieveUpdateState
```

The DMS operation inventory contains `GetUpdateHistory`, not `GetUpdateStates`.

Executable evidence:

```text
EV-107 run 33181833930: V2.2 exact official XSD declaration confirmed.
EV-108 run 33182963733: V2.4 candidate/integration XSD declaration confirmed.
```

Handling:

```text
Do not synthesize GetUpdateStates as an operation alias or resolver route.
```

## Deep-read documentation-only addenda - V2.2

The byte-pinned V2.2 fresh read opened:

```text
DRDMS22-001  SubdeviceStatusInformation points to table 27 although the relevant DeviceStatusInformation structure is table 19; table 27 is InstallUpdateRequest.
DRDMS22-002  TOC numbers GetUpdateHistory/FinalizeUpdate/FinalizeAllPendingUpdates as 1.33/1.34/1.35 while body uses 2.33/2.34/2.35.
DRDMS22-003  prose/XSD annotation use InstallationSuccessfull while executable enum value is InstallationSuccessful; EV-107 confirms typo spelling is not an enum value.
DRDMS22-004  section 2.9 request prose says GetDeviceErrorMessage singular while operation/table/XSD use GetDeviceErrorMessages.
```

These are tracked in `audit_registry/deep_read_findings_delta_dms_v22_2026-08-28.json` and `deep_read/DMS_V2.2.md`.

## Deep-read V2.4 continuation and new finding

The byte-pinned V2.4 fresh read was completed before consulting the earlier V2.4 first-pass report.

History result:

```text
DRDMS22-001  resolved in V2.4: correct table 19 reference.
DRDMS22-002  resolved in V2.4: TOC uses 2.33/2.34/2.35.
DRDMS22-003  persists in V2.4 annotation/prose context; executable value remains InstallationSuccessful.
DRDMS22-004  persists in V2.4 request prose.
DR3012V20-007 persists: GetDeviceConfiguration setter wording remains.
DR3012V20-008 persists: GetDeviceInformation response still described as request structure/data.
```

### DRDMS24-001 - HtmlDisplayService copy/paste foreword

```text
classification: pdf_copy_paste_service_identity_error_candidate
state: confirmed_text_needs_visual_review
confidence: very_high
observation: DMS V2.4 foreword says in both language sections that the document describes HtmlDisplayService; English additionally describes the HTML/Web-server purpose.
validation impact: none
handling: do not infer HTMLDisplay semantics for DMS
```

Tracked in:

```text
audit_registry/deep_read_findings_delta_dms_v24_2026-08-28.json
docs/pdf_xsd_semantic_audit/deep_read/DMS_V2.4.md
```

## Existing Deep Read findings strengthened by DMS history

```text
DR3012V20-007  stale GetDeviceConfiguration setter wording persists through separated DMS V2.2 and checked V2.4.
DR3012V20-008  GetDeviceInformation response described as request structure/data persists through DMS V2.2 and checked V2.4.
```

No duplicate IDs are opened for these historical continuations.

## Safety / handling summary

```text
No DMS XSD was modified by either Deep Read.
EV-107/EV-108 read declarations only and report repository_mutated=false.
Official DMS V2.2 remains validated against Common V2.2 + Enumerations V2.2.
Public DMS V2.4 PDF is official documentation, but repository DMS V2.4 XSD remains candidate/integration authority.
Later V2.4 corrections are explanatory history only for V2.2.
No official-facing action is authorized by this register.
```
