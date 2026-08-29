# EV-111 - DoorStateService V2.1 RetrieveSpecific errors and untyped Get requests

Status: completed / PASS.

Purpose: executable evidence for `DRS-002` and the declaration semantics behind `DRS-003` after the byte-pinned DoorState V2.1 Fresh Read under the mandatory Finding Evidence Gate.

## Exact authority

```text
DoorStateService V2.1
  IBIS-IP_DoorStateService_V2.1.xsd
  official VDV-301-2.1 blob abff0f3960e2ec7a9caaa9ddeb6efff8f4183805

Dependencies selected by that exact service file:
  IBIS-IP_common_V1.0.xsd
  official VDV-301-2.1 blob 194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c

  IBIS-IP_Enumerations_V1.0.xsd
  official VDV-301-2.1 blob a9bea5bc73003ed91ded8519db06c32c4067831d
```

The checked integration-branch copies match the official tag. No XSD was modified for this evidence.

## Source context

Visible pinned-byte page 12 shows both RetrieveSpecific error alternatives as `OperationErrorMessage`. The exact XSD uses `ErrorMessage` in both RetrieveSpecific response types, while its Get response types use `OperationErrorMessage`.

The PDF also says the two Get operations have no request structure. The exact XSD declares their local operation-group elements with no explicit or inline type.

## Harness

```text
tools/validate_door_v21_ev111.py
```

Workflow evidence:

```text
run: 33242337308
job: 99073684198
head tested: 356d1b792730b66a4f5ec3b99b82e6d66185315c
environment: Ubuntu 24.04 / Python 3.12.14 / lxml 6.1.2
result: PASS
```

The temporary push-trigger workflow was deleted immediately after the run. The reusable checker remains; the normative XSDs are unchanged.

## DRS-002 results

The probe exposes global test roots typed directly to the exact normative RetrieveSpecific response complex types.

Results:

```text
ProbeRetrieveOpenResponse
  <ErrorMessage><Value>diagnostic</Value></ErrorMessage>                  -> valid
  <OperationErrorMessage><Value>diagnostic</Value></OperationErrorMessage> -> invalid

ProbeRetrieveOperationResponse
  <ErrorMessage><Value>diagnostic</Value></ErrorMessage>                  -> valid
  <OperationErrorMessage><Value>diagnostic</Value></OperationErrorMessage> -> invalid
```

Decisive validation errors:

```text
Open-state response:
Element 'OperationErrorMessage': This element is not expected.
Expected is one of ( DoorOpenState, ErrorMessage ).

Operation-state response:
Element 'OperationErrorMessage': This element is not expected.
Expected is one of ( DoorOperationState, ErrorMessage ).
```

Conclusion:

```text
DRS-002 executable behaviour confirmed.
For the exact selected XSD, RetrieveSpecific error branches use ErrorMessage.
The PDF's OperationErrorMessage form is rejected in those branches.
```

## DRS-003 results and evidence boundary

The checker first parses the exact normative DoorState XSD and verifies that both local group declarations have neither a `type` attribute nor an inline type:

```xml
<xs:element name="DoorStateService.GetDoorOpenStatesRequest"/>
<xs:element name="DoorStateService.GetDoorOperationStatesRequest"/>
```

Under XML Schema semantics, an element declaration without an explicit or inline type uses `xs:anyType`.

To execute that declaration semantics without modifying the source schema, the checker creates an ephemeral non-normative probe schema that reproduces the exact untyped declaration form at global scope. It tests:

```text
DoorStateService.GetDoorOpenStatesRequest
  empty                                    -> valid
  arbitrary unexpected nested child       -> valid

DoorStateService.GetDoorOperationStatesRequest
  empty                                    -> valid
  arbitrary unexpected nested child       -> valid
```

Evidence boundary:

```text
- The real DoorState declarations are local members of DoorStateServiceGroup.
- EV-111 does not claim that a global DoorState Get request root exists.
- The probe is only an executable demonstration of the exact untyped declaration form's default xs:anyType semantics.
```

Conclusion:

```text
DRS-003 declaration semantics confirmed.
The XSD declaration is more permissive than an explicitly empty request content model.
This is not by itself a remediation decision or authorization to rewrite the XSD.
```

## SDK implications

```text
- Keep the exact mixed-version DoorState V2.1 -> Common V1.0 -> Enumerations V1.0 route.
- For RetrieveSpecific response diagnostics, explain PDF OperationErrorMessage vs executable ErrorMessage; do not normalize silently.
- Do not model the Get request as explicitly empty merely from the PDF wording; preserve exact XSD authority and report the anyType modelling note.
- Do not invent global request roots that do not exist in the selected schema.
```
