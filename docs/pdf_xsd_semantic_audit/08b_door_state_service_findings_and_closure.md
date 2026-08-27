# DoorStateService findings and V2.1 closure

Status: first-pass closure completed for DoorStateService V2.1; local schema compilation still pending.

Scope:

```text
docs/pdf_xsd_semantic_audit/08_door_state_service_historical_start.md
docs/pdf_xsd_semantic_audit/08a_door_state_service_v2_1_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/DOOR_STATE_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
```

## Selected validation authority

Validation remains XSD-driven.

```text
DoorStateService V2.1 -> IBIS-IP_DoorStateService_V2.1.xsd + IBIS-IP_common_V1.0.xsd + IBIS-IP_Enumerations_V1.0.xsd
```

The V2.1 service XSD explicitly includes Common V1.0 and Enumerations V1.0. This is treated as the selected executable dependency pool for DoorStateService V2.1, not as an error.

## Closure summary

The DoorStateService V2.1 first pass did not produce an immediate XSD change.

The operation set and the two central data paths are represented in the XSD:

```text
Door open states:
- GetDoorOpenStates
- SubscribeDoorOpenStates
- UnsubscribeDoorOpenStates
- RetrieveSpecificDoorOpenState

Door operation states:
- GetDoorOperationStates
- SubscribeDoorOperationStates
- UnsubscribeDoorOperationStates
- RetrieveSpecificDoorOperationState
```

The main executable structures are also present:

```text
DoorStateService.GetDoorOpenStatesResponseStructure
DoorStateService.GetDoorOperationStatesResponseStructure
DoorStateService.RetrieveSpecificDoorOpenStateRequestStructure
DoorStateService.RetrieveSpecificDoorOpenStateResponseStructure
DoorStateService.RetrieveSpecificDoorOperationStateRequestStructure
DoorStateService.RetrieveSpecificDoorOperationStateResponseStructure
DoorStateService.SpecificDoorOpenStateStructure
DoorStateService.SpecificDoorOperationStateStructure
```

## Findings carried forward

### DRS-001 - DoorOperationStates subscription names in PDF operation overview

Classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: medium
final_handling_bucket: provider_note_or_pdf_clarification_candidate
```

Decision:

```text
No XSD change.
The surrounding PDF headings and the XSD operation group point to SubscribeDoorOperationStates / UnsubscribeDoorOperationStates.
The apparent operation-overview repetition of DoorOpenStates names is carried as PDF table/wording candidate.
```

### DRS-002 - RetrieveSpecific error branch OperationErrorMessage PDF vs ErrorMessage XSD

Classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: xsd_or_pdf_naming_inconsistency_candidate
classification_confidence: medium
final_handling_bucket: local_validation_then_official_facing_review
```

Decision:

```text
No XSD change yet.
This is the strongest DoorStateService executable mismatch candidate.
Validation follows XSD: the checked RetrieveSpecific response structures use ErrorMessage.
Local positive/negative samples are required before deciding whether to treat this as an XSD correction candidate, PDF clarification, or compatibility note.
```

### DRS-003 - Get request elements without explicit type despite PDF saying no request structure

Classification:

```text
mismatch_kind: service_modelling
likely_source_issue: schema_modelling_or_generic_empty_request_candidate
classification_confidence: medium
final_handling_bucket: local_compile_and_sample_validation
```

Decision:

```text
No XSD change.
The XSD has GetDoorOpenStatesRequest and GetDoorOperationStatesRequest elements without explicit type while the PDF says no request structure.
Local schema compilation and sample validation must determine how these untyped request elements behave.
```

### DRS-004 - XSD documentation-only spelling typos

Classification:

```text
mismatch_kind: ok_note
likely_source_issue: xsd_documentation_typo_non_executable
classification_confidence: high
final_handling_bucket: documentation_only_note
```

Decision:

```text
No executable issue.
Annotation-only typos such as Opeation/Operationn are not validation defects.
Do not include in an official XSD correction PR unless documentation cleanup is explicitly desired.
```

## Tool/SDK implications

```text
- Use DoorStateService V2.1 with Common V1.0 + Enumerations V1.0.
- Preserve operation element names exactly as in the XSD.
- Do not substitute OperationErrorMessage for ErrorMessage in RetrieveSpecific response branches unless an official schema correction exists.
- Add validation samples for empty and non-empty GetDoorOpenStatesRequest / GetDoorOperationStatesRequest.
- Add positive and negative samples for ErrorMessage vs OperationErrorMessage in RetrieveSpecific responses.
```

## Local validation backlog additions

```text
DRS-VB-001: Compile DoorStateService V2.1 with Common V1.0 and Enumerations V1.0.
DRS-VB-002: Positive sample: GetDoorOpenStatesResponse with one DoorOpenStates entry.
DRS-VB-003: Positive sample: GetDoorOperationStatesResponse with one DoorOperationStates entry.
DRS-VB-004: Positive/negative pair: RetrieveSpecificDoorOpenStateResponse with ErrorMessage vs OperationErrorMessage.
DRS-VB-005: Positive/negative pair: RetrieveSpecificDoorOperationStateResponse with ErrorMessage vs OperationErrorMessage.
DRS-VB-006: Empty and non-empty GetDoorOpenStatesRequest / GetDoorOperationStatesRequest behavior.
```

## Status

DoorStateService V2.1 is closed for first-pass PDF/XSD audit.

No XSD file was modified.
No official PR candidate was opened.

Next recommended audit block:

```text
09_ticket_validation_service_historical_start.md
```
