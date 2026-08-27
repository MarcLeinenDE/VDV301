# AUDIT HANDOFF DELTA - DoorStateService 08B

Status: supplemental delta after DoorStateService findings closure.

Branch:

```text
dev/schema-integration
```

New / updated files:

```text
docs/pdf_xsd_semantic_audit/08b_door_state_service_findings_and_closure.md
docs/pdf_xsd_semantic_audit/generated/door_state_service_findings_closure_matrix.csv
docs/pdf_xsd_semantic_audit/DOOR_STATE_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
```

DoorStateService result:

```text
DoorStateService V2.1 first-pass PDF/XSD audit closed.
Selected executable pool: DoorStateService V2.1 + Common V1.0 + Enumerations V1.0.
No XSD file modified.
No official PR candidate opened.
```

Findings carried forward:

```text
DRS-001: DoorOperationStates subscription names in PDF operation overview; likely PDF table/wording candidate.
DRS-002: RetrieveSpecific response error branch OperationErrorMessage in PDF vs ErrorMessage in XSD; strongest executable mismatch candidate.
DRS-003: Get request elements without explicit type despite PDF saying no request structure; requires local compile/sample validation.
DRS-004: XSD documentation-only typos; OK with note, no executable validation impact.
```

Validation backlog additions:

```text
Compile DoorStateService V2.1 with Common V1.0 and Enumerations V1.0.
Add positive samples for GetDoorOpenStatesResponse and GetDoorOperationStatesResponse.
Add positive/negative RetrieveSpecific response samples for ErrorMessage vs OperationErrorMessage.
Test empty and non-empty GetDoorOpenStatesRequest and GetDoorOperationStatesRequest behavior.
```

Next recommended audit block:

```text
09_ticket_validation_service_historical_start.md
```
