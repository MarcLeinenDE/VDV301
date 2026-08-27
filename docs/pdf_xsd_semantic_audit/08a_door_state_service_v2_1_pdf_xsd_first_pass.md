# DoorStateService V2.1 PDF/XSD first pass

Status: first pass completed for DoorStateService V2.1; local schema compilation still pending.

Scope:

```text
VDV 301-2-15 DoorStateService V2.1 PDF
IBIS-IP_DoorStateService_V2.1.xsd
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

Authority rule:

```text
Validation follows the selected XSD family.
PDF differences are recorded as explanatory/provider-facing notes, not as executable validation authority.
```

## Selected dependency pool

```text
DoorStateService V2.1
+ IBIS-IP_common_V1.0.xsd
+ IBIS-IP_Enumerations_V1.0.xsd
```

This dependency combination is intentionally kept as observed in the XSD. The V2.1 service file includes the V1.0 common/enumeration schema family.

## PDF service context

The PDF describes DoorStateService as the service for providing door open state and door operation state for one or more vehicle doors. It is intended to provide door-specific state information, especially for passenger-counting raw data use cases.

The public PDF is:

```text
VDV-Schrift 301-2-15
07/2018
DoorStateService
V2.1
```

## Operation overview: PDF vs XSD

The XSD operation group contains these executable service operation elements:

```text
DoorStateService.GetDoorOpenStatesRequest
DoorStateService.GetDoorOpenStatesResponse
DoorStateService.SubscribeDoorOpenStatesRequest
DoorStateService.SubscribeDoorOpenStatesResponse
DoorStateService.UnsubscribeDoorOpenStatesRequest
DoorStateService.UnsubscribeDoorOpenStatesResponse
DoorStateService.GetDoorOperationStatesRequest
DoorStateService.GetDoorOperationStatesResponse
DoorStateService.SubscribeDoorOperationStatesRequest
DoorStateService.SubscribeDoorOperationStatesResponse
DoorStateService.UnsubscribeDoorOperationStatesRequest
DoorStateService.UnsubscribeDoorOperationStatesResponse
DoorStateService.RetrieveSpecificDoorOpenStateRequest
DoorStateService.RetrieveSpecificDoorOpenStateResponse
DoorStateService.RetrieveSpecificDoorOperationStateRequest
DoorStateService.RetrieveSpecificDoorOperationStateResponse
```

The PDF table lists the expected operation families. The Get and Retrieve operation names align at service-operation level, but the PDF operation table appears to repeat the DoorOpenStates subscription names in the DoorOperationStates block.

Classification:

```text
DRS-001 candidate
likely_source_issue: pdf_table_or_documentation_error_candidate
```

Reasoning: the surrounding PDF headings explicitly name SubscribeDoorOperationStates and UnsubscribeDoorOperationStates, and the XSD also uses DoorOperationStates for the operation-state subscription elements.

## GetDoorOpenStates

PDF:

```text
GetDoorOpenStates request: no request structure.
GetDoorOpenStates response: DoorStateService.GetDoorOpenStatesResponseStructure.
GetDoorOpenStatesResponseData contains TimeStamp 1:1 and DoorOpenStates 1:*.
SpecificDoorOpenState contains TimeStamp, DoorID and OpenState.
```

XSD:

```text
DoorStateService.GetDoorOpenStatesRequest exists as an element without explicit type.
DoorStateService.GetDoorOpenStatesResponse uses DoorStateService.GetDoorOpenStatesResponseStructure.
GetDoorOpenStatesResponseStructure choice:
  GetDoorOpenStatesResponseData
  OperationErrorMessage
GetDoorOpenStatesResponseData:
  TimeStamp 1:1
  DoorOpenStates minOccurs="1" maxOccurs="unbounded"
SpecificDoorOpenStateStructure:
  TimeStamp 1:1
  DoorID 1:1
  OpenState 1:1 DoorOpenStateStructure
```

First-pass result:

```text
Response data/cardinality aligns.
Request modelling needs a validation sample because the XSD has a request element without explicit type even though the PDF says no request structure.
```

## GetDoorOperationStates

PDF:

```text
GetDoorOperationStates request: no request structure.
GetDoorOperationStates response: DoorStateService.GetDoorOperationStatesResponseStructure.
GetDoorOperationStatesResponseData contains TimeStamp 1:1 and DoorOperationStates 1:*.
SpecificDoorOperationState contains TimeStamp, DoorID and OperationState.
```

XSD:

```text
DoorStateService.GetDoorOperationStatesRequest exists as an element without explicit type.
DoorStateService.GetDoorOperationStatesResponse uses DoorStateService.GetDoorOperationStatesResponseStructure.
GetDoorOperationStatesResponseStructure choice:
  GetDoorOperationStatesResponseData
  OperationErrorMessage
GetDoorOperationStatesResponseData:
  TimeStamp 1:1
  DoorOperationStates minOccurs="1" maxOccurs="unbounded"
SpecificDoorOperationStateStructure:
  TimeStamp 1:1
  DoorID 1:1
  OperationState 1:1 DoorOperationStateStructure
```

First-pass result:

```text
Response data/cardinality aligns.
Request modelling has the same issue as GetDoorOpenStates.
```

## Subscribe/Unsubscribe operations

PDF:

```text
SubscribeDoorOpenStates / UnsubscribeDoorOpenStates use the base Subscribe/Unsubscribe structures.
SubscribeDoorOperationStates / UnsubscribeDoorOperationStates use the base Subscribe/Unsubscribe structures.
```

XSD:

```text
SubscribeDoorOpenStatesRequest      type SubscribeRequestStructure
SubscribeDoorOpenStatesResponse     type SubscribeResponseStructure
UnsubscribeDoorOpenStatesRequest    type UnsubscribeRequestStructure
UnsubscribeDoorOpenStatesResponse   type UnsubscribeResponseStructure
SubscribeDoorOperationStatesRequest    type SubscribeRequestStructure
SubscribeDoorOperationStatesResponse   type SubscribeResponseStructure
UnsubscribeDoorOperationStatesRequest  type UnsubscribeRequestStructure
UnsubscribeDoorOperationStatesResponse type UnsubscribeResponseStructure
```

First-pass result:

```text
Executable XSD modelling is coherent and aligns with the section headings.
The PDF overview table likely has copied DoorOpenStates operation names in the operation-state subscription rows.
```

## RetrieveSpecificDoorOpenState

PDF:

```text
Request: DoorID 1:1 IBIS-IP.NMTOKEN.
Response choice:
  DoorOpenState 1:1 DoorStateService.SpecificDoorOpenState
  OperationErrorMessage IBIS-IP.string
```

XSD:

```text
Request choice:
  DoorID 1:1 IBIS-IP.NMTOKEN
Response choice:
  DoorOpenState type DoorStateService.SpecificDoorOpenStateStructure
  ErrorMessage type IBIS-IP.string
```

First-pass result:

```text
DoorID and success response align.
Error response element name differs: PDF OperationErrorMessage vs XSD ErrorMessage.
```

Classification:

```text
DRS-002 candidate
mismatch_kind: operation_or_element_name
likely_source_issue: xsd_or_pdf_naming_inconsistency_candidate
```

This is executable, unlike pure documentation typos. Validation follows the XSD, so `ErrorMessage` is currently the executable element name for the RetrieveSpecific response branches.

## RetrieveSpecificDoorOperationState

PDF:

```text
Request: DoorID 1:1 IBIS-IP.NMTOKEN.
Response choice:
  DoorOperationState 1:1 DoorStateService.SpecificDoorOperationState
  OperationErrorMessage IBIS-IP.string
```

XSD:

```text
Request choice:
  DoorID 1:1 IBIS-IP.NMTOKEN
Response choice:
  DoorOperationState type DoorStateService.SpecificDoorOperationStateStructure
  ErrorMessage type IBIS-IP.string
```

First-pass result:

```text
DoorID and success response align.
Error response element name differs in the same way as RetrieveSpecificDoorOpenState.
```

DRS-002 therefore applies to both RetrieveSpecific response structures.

## Request modelling candidate

The PDF says there is no request structure for GetDoorOpenStates and GetDoorOperationStates. The XSD nevertheless declares the corresponding request elements without an explicit type.

```text
<xs:element name="DoorStateService.GetDoorOpenStatesRequest"/>
<xs:element name="DoorStateService.GetDoorOperationStatesRequest"/>
```

Classification:

```text
DRS-003 candidate
mismatch_kind: service_modelling
likely_source_issue: schema_modelling_or_generic_empty_request_candidate
```

This must be locally compiled/tested before classification is strengthened, because an untyped element may behave differently than an explicitly empty request structure.

## Non-executable XSD documentation typos

The XSD contains typo-like words in xs:documentation only, for example:

```text
GetDoorOpeationStates
RetrieveSpecificDoorOperationnState
operationn state
```

Classification:

```text
DRS-004 note
mismatch_kind: ok_note
likely_source_issue: xsd_documentation_typo_non_executable
```

No validation impact is opened for these because they occur in documentation text, not executable element/type names.

## Findings carried forward

```text
DRS-001 PDF operation table copy/paste candidate for DoorOperationStates subscriptions.
DRS-002 RetrieveSpecific error element name PDF OperationErrorMessage vs XSD ErrorMessage.
DRS-003 Get request elements without explicit type despite PDF saying no request structure.
DRS-004 XSD documentation-only typo notes, no executable impact.
```

## Decision

No XSD change is proposed in this pass.

DoorStateService V2.1 remains executable as:

```text
IBIS-IP_DoorStateService_V2.1.xsd
+ IBIS-IP_common_V1.0.xsd
+ IBIS-IP_Enumerations_V1.0.xsd
```

Local schema compilation and positive/negative XML samples are required before any official-facing correction proposal.
