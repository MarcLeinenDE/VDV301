# TrainSet services V2.1 / V2.2 PDF-XSD first pass

Status: semantic/provenance first pass completed. Local XSD compilation/sample validation remains pending.

## TSI-001 - V2.1 train composition cannot carry multiple coaches

V2.1 PDF states that `GetTrainSetComposition` returns a sequence of coach data sets, one per coach.

Official V2.1 XSD models `GetTrainSetCompositionResponseStructure` directly as one sequence of coach fields:

```text
CoachType?
CoachNumber
FrontCabin
RearCabin
CoachPositionInTrainSet
CoupledSide?
CoachState
```

There is no repeated coach wrapper.

V2.2 corrects this to:

```text
GetTrainSetCompositionResponseStructure
  SingleCoach 1:* -> SingleCoachInATrainSet
```

and the V2.2 version history explicitly states that previously it was not possible to transmit data for several coaches.

Classification:

```text
xsd_structure_modelling_error_candidate
scope: V2.1
state: historically confirmed and corrected in V2.2
```

Strict V2.1 validation must nevertheless follow the V2.1 XSD.

## TSM-001 - V2.1 response-root naming corrected in V2.2

V2.1 XSD exposes:

```text
TrainSetManagementService.GetTrainSetComposition
```

with `TrainSetInformationService.GetTrainSetCompositionResponseStructure` as its type.

The V2.2 version history explicitly states that the corrected name is:

```text
TrainSetManagementService.GetTrainSetCompositionResponse
```

Classification:

```text
xsd_operation_or_element_name_error_candidate
scope: V2.1
state: corrected in V2.2 global declaration
```

No alias is invented for V2.1 validation.

## TSM-002 - V2.2 stale operation-group member

Official V2.2 XSD globally declares the corrected element:

```text
TrainSetManagementService.GetTrainSetCompositionResponse
```

but `TrainSetManagementServiceOperations` still contains:

```text
TrainSetManagementService.GetTrainSetComposition
```

The V2.2 document history says the old name was supposed to be replaced.

Classification:

```text
xsd_structure_modelling_error_candidate
subtype: operation_group_name_mismatch
confidence: high
```

This is analogous in risk to other operation-group inventory findings: direct global-root validation and operation-group-derived inventories can disagree.

## TSD-001 - V2.1 parameterized subscriptions missing from service XSD

The V2.1 PDF already defines triples for both datasets:

```text
RetrieveTripRef / SubscribeTripRef / UnsubscribeTripRef
RetrieveTripInformation / SubscribeTripInformation / UnsubscribeTripInformation
```

The V2.1 operation table specifies generic `SubscribeResponseStructure` / `UnsubscribeResponseStructure` responses and reuses the Retrieve request structures.

Official V2.1 TrainSetDataService XSD operation group contains only:

```text
RetrieveTripRefRequest/Response
RetrieveTripInformationRequest/Response
```

V2.2 introduces dedicated parameterized subscribe/unsubscribe request structures and adds the missing operations. The V2.2 history describes this as a technical correction required for correct subscription to Retrieve data.

Classification:

```text
service_modelling_or_generic_response_candidate
scope: V2.1
state: historical modelling gap corrected/reworked in V2.2
```

## TSD-002 - V2.2 Unsubscribe request table not updated

V2.2 detailed text says:

```text
UnsubscribeTripRef -> TrainSetUnsubscribeRequestStructure
UnsubscribeTripInformation -> TrainSetUnsubscribeRequestStructure
```

and the V2.2 XSD uses those specialized structures.

However, the V2.2 operation overview table still lists:

```text
UnsubscribeTripRef Request -> RetrieveTripRefRequestStructure
UnsubscribeTripInformation Request -> RetrieveTripInformationRequestStructure
```

Classification:

```text
pdf_table_or_documentation_error_candidate
confidence: high
validation_behavior: exact XSD uses TrainSetUnsubscribeRequestStructure
```

## TSD-003 - dual Subscribe response typing by context

Within `TrainSetDataServiceOperations`, V2.2 declares:

```text
SubscribeTripRefResponse -> SubscribeResponseStructure
SubscribeTripInformationResponse -> SubscribeResponseStructure
```

The same names also exist as global elements typed as:

```text
SubscribeTripRefResponse -> RetrieveTripRefResponseStructure
SubscribeTripInformationResponse -> RetrieveTripInformationResponseStructure
```

The PDF distinguishes the immediate subscription acknowledgement (`SubscribeResponseStructure`) from subsequent event-based data updates using the Retrieve response structure.

Initial classification:

```text
service_modelling_or_generic_response_candidate
confidence: medium-high
```

Do not call this an XSD defect until local root/group validation and the generic subscription model are checked. The later SDK must understand the context if both forms are intentional.

## Technical backlog

```text
TS-VB-001 compile each V2.1 service with its exact direct/transitive pool.
TS-VB-002 compile each V2.2 service with its exact pool.
TS-VB-003 V2.1 TSI sample for one coach and negative attempt for two coaches.
TS-VB-004 V2.2 TSI positive sample with two SingleCoach entries.
TS-VB-005 compare TSM V2.2 global-root inventory vs operation-group member inventory.
TS-VB-006 validate TSD V2.1 operation inventory against the six PDF operations.
TS-VB-007 validate TSD V2.2 specialized subscribe/unsubscribe requests.
TS-VB-008 test TSD V2.2 Subscribe*Response as global roots and as operation-group members to resolve TSD-003.
```
