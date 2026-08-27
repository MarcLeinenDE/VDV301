# Audit handoff delta - DoorStateService start

Status: supplemental handoff delta after starting DoorStateService historical audit.

## New files

```text
docs/pdf_xsd_semantic_audit/08_door_state_service_historical_start.md
docs/pdf_xsd_semantic_audit/generated/door_state_service_historical_scope_matrix.csv
```

## Current result

DoorStateService scope is started with:

```text
VDV 301-2-15 DoorStateService V2.1 PDF
IBIS-IP_DoorStateService_V2.1.xsd
```

Observed XSD mapping:

```text
DoorStateService V2.1
+ IBIS-IP_common_V1.0.xsd
+ IBIS-IP_Enumerations_V1.0.xsd
```

The XSD exists both in official `VDVde/VDV301 master` and in `MarcLeinenDE/VDV301 dev/schema-integration`.

## Candidate notes carried forward

```text
DRS-001 candidate:
PDF operation table appears to repeat SubscribeDoorOpenStates / UnsubscribeDoorOpenStates in the operation-state rows, while XSD has SubscribeDoorOperationStates / UnsubscribeDoorOperationStates.

DRS-002 candidate:
PDF retrieve-specific response tables describe OperationErrorMessage, while XSD uses ErrorMessage for retrieve-specific response error branches.

DRS-003 candidate:
PDF says GetDoorOpenStates/GetDoorOperationStates have no request structure, while XSD contains request elements without explicit type.
```

No DoorStateService finding opened yet.

## Next recommended file

```text
docs/pdf_xsd_semantic_audit/08a_door_state_service_v2_1_pdf_xsd_first_pass.md
```
