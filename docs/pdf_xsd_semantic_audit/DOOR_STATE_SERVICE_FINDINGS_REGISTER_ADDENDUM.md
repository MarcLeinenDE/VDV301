# DoorStateService findings register addendum

Status: supplemental register; keep separate until the main findings register is consolidated.

Authority rule:

```text
Validation follows XSD.
PDF differences are recorded as explanatory/provider-facing notes, not as executable validation authority.
```

Source audit files:

```text
docs/pdf_xsd_semantic_audit/08_door_state_service_historical_start.md
docs/pdf_xsd_semantic_audit/08a_door_state_service_v2_1_pdf_xsd_first_pass.md
```

## DoorStateService findings

### DRS-001 - DoorOperationStates subscription names in PDF operation overview

State: confirmed PDF table/wording candidate; likely PDF copy/paste issue, not an immediate XSD defect.

Classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: medium
```

Observation:

```text
The DoorStateService V2.1 PDF operation overview appears to repeat SubscribeDoorOpenStates and UnsubscribeDoorOpenStates in the DoorOperationStates block.
The surrounding PDF section headings name SubscribeDoorOperationStates and UnsubscribeDoorOperationStates.
The XSD operation group uses SubscribeDoorOperationStates and UnsubscribeDoorOperationStates.
```

Impact:

```text
Validation follows the XSD operation names.
Provider-facing explanations should mention that the PDF overview table appears inconsistent with the section headings and executable XSD.
```

Next action: local operation-element samples and later register consolidation.

### DRS-002 - RetrieveSpecific error branch OperationErrorMessage PDF vs ErrorMessage XSD

State: confirmed PDF/XSD executable element-name discrepancy candidate.

Classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: xsd_or_pdf_naming_inconsistency_candidate
classification_confidence: medium
```

Observation:

```text
The DoorStateService V2.1 PDF RetrieveSpecificDoorOpenStateResponse and RetrieveSpecificDoorOperationStateResponse tables list OperationErrorMessage for the error branch.
The XSD uses ErrorMessage in both RetrieveSpecific response structures.
The Get response structures in the same XSD use OperationErrorMessage.
```

Impact:

```text
Payloads using <OperationErrorMessage> in the RetrieveSpecific response branches will fail against the checked XSD.
Payloads using <ErrorMessage> validate against the checked XSD but differ from the PDF table wording and from the Get-response naming pattern.
```

Next action: local positive/negative XML samples before deciding whether this is official-facing XSD correction, PDF clarification, or compatibility note.

### DRS-003 - Get request elements without explicit type despite PDF saying no request structure

State: service modelling candidate; local schema behavior must be tested.

Classification:

```text
mismatch_kind: service_modelling
likely_source_issue: schema_modelling_or_generic_empty_request_candidate
classification_confidence: medium
```

Observation:

```text
The DoorStateService V2.1 PDF says no request structure exists for GetDoorOpenStates and GetDoorOperationStates.
The XSD operation group declares DoorStateService.GetDoorOpenStatesRequest and DoorStateService.GetDoorOperationStatesRequest as elements without explicit type.
```

Impact:

```text
Do not infer final behavior without local schema compilation and sample validation.
The future tool should preserve the exact XSD and test whether these untyped request elements accept more content than intended.
```

Next action: local compile/sample validation for empty and non-empty Get request elements.

### DRS-004 - XSD documentation-only spelling typos

State: OK with note; no executable validation impact.

Classification:

```text
mismatch_kind: ok_note
likely_source_issue: xsd_documentation_typo_non_executable
classification_confidence: high
```

Observation:

```text
The XSD contains typo-like text inside xs:documentation only, such as GetDoorOpeationStates and RetrieveSpecificDoorOperationnState.
The executable operation/type/element names are not affected by those annotation spelling issues.
```

Impact:

```text
No validation behavior changes.
Do not open an XSD correction for annotation text unless the VDV specifically wants documentation cleanup.
```

Next action: carry as documentation-only note.
