# DoorStateService historical audit start

Status: started; public PDF / observed XSD mapping and first candidate classification notes created. Local schema compilation still pending.

Scope:

```text
VDV 301-2-15 DoorStateService V2.1 PDF
IBIS-IP_DoorStateService_V2.1.xsd
```

## Authority and source policy

Validation remains XSD-driven.

```text
Validation follows the selected XSD family.
PDF differences are recorded as explanatory/provider-facing notes, not as executable validation authority.
```

This audit also applies the finding classification policy introduced in:

```text
docs/pdf_xsd_semantic_audit/FINDING_CLASSIFICATION_POLICY.md
```

Potential findings are not automatically treated as XSD defects. They are first grouped as likely XSD typo, likely PDF/table documentation issue, modelling issue, cardinality/type issue, or provenance/routing issue.

## Public PDF mapping

Observed public document:

```text
VDV-Schrift 301-2-15
Issue/date: 07/2018
Service: DoorStateService
Version: V2.1
```

The public index lists `VDV 301-2-15 IBIS-IP Beschreibung der Dienste - Dienst DoorStateService V2.1`.

The PDF foreword states that this publication describes the DoorStateService and its specific data structures.

## Repository XSD mapping

Observed service XSD:

```text
IBIS-IP_DoorStateService_V2.1.xsd
```

Observed in:

```text
VDVde/VDV301 master
MarcLeinenDE/VDV301 dev/schema-integration
```

The observed dependency pool is:

```text
DoorStateService V2.1
+ IBIS-IP_common_V1.0.xsd
+ IBIS-IP_Enumerations_V1.0.xsd
```

This mixed service/common version number is recorded as a dependency fact, not as a defect. Do not rewrite it to Common V2.1 / Enumerations V2.1 unless a version-specific official source requires that.

## First XSD observations

The XSD contains a dedicated service group:

```text
DoorStateServiceGroup
```

The group contains concrete operations for:

```text
GetDoorOpenStates
SubscribeDoorOpenStates
UnsubscribeDoorOpenStates
GetDoorOperationStates
SubscribeDoorOperationStates
UnsubscribeDoorOperationStates
RetrieveSpecificDoorOpenState
RetrieveSpecificDoorOperationState
```

Unlike the CIS/JIS generic subscription observations, DoorStateService V2.1 has local subscribe/unsubscribe request and response elements in its service group.

## Initial candidate notes for next pass

### DRS-001 candidate - operation table wording for DoorOperation subscription rows

Initial observation:

```text
The PDF operation overview appears to repeat SubscribeDoorOpenStates / UnsubscribeDoorOpenStates in the door-operation-state area.
The XSD group contains SubscribeDoorOperationStates / UnsubscribeDoorOperationStates.
```

Initial classification:

```text
likely_source_issue: pdf_table_or_documentation_error_candidate
mismatch_kind: operation_or_element_name
```

No XSD change proposed.

### DRS-002 candidate - RetrieveSpecific* error element wording

Initial observation:

```text
The PDF retrieve-specific response tables describe OperationErrorMessage.
The XSD retrieve-specific response structures use ErrorMessage for the error branch.
```

Initial classification:

```text
likely_source_issue: unresolved
mismatch_kind: operation_or_element_name
```

This needs detailed PDF/XSD first-pass review before classification as XSD issue, PDF issue, or intentional older modelling.

### DRS-003 candidate - no-request Get operations vs XSD request elements without explicit type

Initial observation:

```text
The PDF says GetDoorOpenStates and GetDoorOperationStates have no request structure.
The XSD service group contains GetDoorOpenStatesRequest and GetDoorOperationStatesRequest elements without an explicit type.
```

Initial classification:

```text
likely_source_issue: service_modelling_or_generic_response_candidate
mismatch_kind: service_modelling
```

This may simply be the service's way to provide a request element for the operation while leaving it structurally empty. It is not a defect until locally validated.

## Validation backlog impact

Add later local schema/sample checks for:

```text
DoorStateService V2.1 schema compile with Common V1.0 + Enumerations V1.0
positive GetDoorOpenStatesResponse with DoorOpenStates 1..n
positive GetDoorOperationStatesResponse with DoorOperationStates 1..n
positive/negative RetrieveSpecificDoorOpenStateResponse using ErrorMessage vs OperationErrorMessage
positive/negative RetrieveSpecificDoorOperationStateResponse using ErrorMessage vs OperationErrorMessage
empty/no-payload GetDoorOpenStatesRequest and GetDoorOperationStatesRequest behaviour
```

## Finding decision

No DRS finding is opened in the main register yet.

Candidate notes DRS-001 through DRS-003 are carried into the next detailed first-pass file.

## Next file

```text
docs/pdf_xsd_semantic_audit/08a_door_state_service_v2_1_pdf_xsd_first_pass.md
```
