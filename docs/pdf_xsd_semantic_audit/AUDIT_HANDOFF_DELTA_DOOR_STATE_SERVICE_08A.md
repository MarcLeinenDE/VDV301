# Audit handoff delta - DoorStateService 08A

Status: supplemental delta after DoorStateService V2.1 PDF/XSD first pass.

Created in this delta:

```text
docs/pdf_xsd_semantic_audit/08a_door_state_service_v2_1_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/generated/door_state_service_v2_1_pdf_xsd_first_pass_matrix.csv
docs/pdf_xsd_semantic_audit/DOOR_STATE_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_DOOR_STATE_SERVICE_08A.md
```

Current DoorStateService result:

```text
DoorStateService V2.1
+ IBIS-IP_DoorStateService_V2.1.xsd
+ IBIS-IP_common_V1.0.xsd
+ IBIS-IP_Enumerations_V1.0.xsd
```

First-pass status:

```text
completed; local schema compilation and XML samples still pending.
```

Findings / notes carried forward:

```text
DRS-001: PDF operation overview likely repeats DoorOpenStates subscription names where DoorOperationStates names are intended.
DRS-002: RetrieveSpecific response error branch differs: PDF OperationErrorMessage vs XSD ErrorMessage.
DRS-003: Get request elements are present in XSD without explicit type although PDF says no request structure.
DRS-004: XSD annotation typos are documentation-only; no executable validation impact.
```

No XSD changed. No official PR candidate opened.

Next recommended block:

```text
08b_door_state_service_findings_and_closure.md
```
