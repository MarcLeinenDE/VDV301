# DeviceManagementService findings register addendum

Status: V2.0-V2.4 semantic/provenance first-pass chain complete; byte-pinned DMS V2.2 Deep Read Pass 2 complete textually with EV-107; visual closure remains pending where noted.

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
observation: 10:* ErrorMessage is PDF/XSD-aligned in V2.0, V2.1 and byte-pinned V2.2; V2.4 later corrects to 0:*
validation: do not retroactively relax older profiles
fresh V2.2 evidence: deep_read/DMS_V2.2.md
```

## DMS-004

```text
classification: ok_with_note
scope: historical V2.1/V2.2 -> V2.4 correction
observation: InstallUpdate UpdateID/UpdateTimestamp/UpdateURL are required in both V2.1 and byte-pinned V2.2 PDF/XSD; V2.4 later makes them optional
validation: do not retroactively relax V2.1/V2.2
fresh V2.2 evidence: deep_read/DMS_V2.2.md
```

## DMS-005 - GetDeviceStatusInformation response-data branch name

State: PDF/XSD element-name mismatch, executable XSD declaration confirmed by EV-107.

Classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: very high
version_scope: DMS V2.2 checked
validation_behavior: exact XSD branch name required
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

PDF evidence:

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
PDF-only non-Get branch spelling absent from exact XSD
```

Handling:

```text
Do not treat DeviceManagementService.DeviceStatusInformationResponseData as an alias.
Validation follows DeviceManagementService.GetDeviceStatusInformationResponseData.
```

## DMS-006 - DeviceStatus PDF omits two V2.2 XSD-required fields

State: structure/cardinality mismatch, executable declaration confirmed by EV-107.

Classification:

```text
mismatch_kind: cardinality / structure omission
likely_source_issue: pdf_table_or_documentation_error_candidate with later alignment evidence
classification_confidence: very high
version_scope: DMS V2.2 historical profile
validation_behavior: V2.2 XSD requires four DeviceStatus fields
final_handling_bucket: official_documentation_or_schema_alignment_review_candidate
```

PDF table 20:

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

Historical context:

```text
V2.4 correction makes DeviceStatusImpact and DeviceStatusPriority optional.
This later correction explains the history but does not alter V2.2 validation.
```

Impact:

```text
A producer implementing only the V2.2 PDF table can emit an XML structure that is incomplete for the selected V2.2 XSD.
```

## DMS-007 - InstallUpdate UpdateTimestamp `GetUpdateStates` vs `GetUpdateHistory`

State: PDF operation/reference typo confirmed against exact XSD and operation inventory; EV-107 confirms the XSD annotation.

Classification:

```text
mismatch_kind: operation_or_element_name / reference
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: very high
version_scope: DMS V2.2 checked
validation_behavior: no direct XML cardinality/type effect; operation resolver must not invent GetUpdateStates
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

PDF table 27:

```text
UpdateTimestamp:
  Timestamp used for GetUpdateStates and RetrieveUpdateState responses and for logging
```

Exact DMS V2.2 XSD annotation:

```text
Timestamp used for GetUpdateHistory and RetrieveUpdateState responses and for logging
```

The DMS operation inventory contains `GetUpdateHistory`, not `GetUpdateStates`.

EV-107 run `33181833930` confirms the exact XSD wording and absence of `GetUpdateStates` in that annotation.

Handling:

```text
Do not synthesize GetUpdateStates as an operation alias or resolver route.
```

## Deep-read documentation-only addenda

The byte-pinned V2.2 fresh read additionally opened:

```text
DRDMS22-001  SubdeviceStatusInformation points to table 27 although the relevant DeviceStatusInformation structure is table 19; table 27 is InstallUpdateRequest.
DRDMS22-002  TOC numbers GetUpdateHistory/FinalizeUpdate/FinalizeAllPendingUpdates as 1.33/1.34/1.35 while body uses 2.33/2.34/2.35.
DRDMS22-003  prose/XSD annotation use InstallationSuccessfull while executable enum value is InstallationSuccessful; EV-107 confirms typo spelling is not an enum value.
DRDMS22-004  section 2.9 request prose says GetDeviceErrorMessage singular while operation/table/XSD use GetDeviceErrorMessages.
```

These are tracked in `audit_registry/deep_read_findings_delta_dms_v22_2026-08-28.json` and `deep_read/DMS_V2.2.md`.

## Existing Deep Read findings strengthened by DMS V2.2

```text
DR3012V20-007  stale GetDeviceConfiguration setter wording persists into separated DMS V2.2.
DR3012V20-008  GetDeviceInformation response still described as request structure/data in DMS V2.2.
```

No duplicate IDs are opened for these historical continuations.

## Safety / handling summary

```text
No DMS XSD was modified by the V2.2 Deep Read.
EV-107 reads declarations only and reports repository_mutated=false.
Official DMS V2.2 remains validated against Common V2.2 + Enumerations V2.2.
Later V2.4 corrections are explanatory history only for V2.2.
No official-facing action is authorized by this register.
```
