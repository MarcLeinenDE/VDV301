# TrainSet services findings register addendum

Status: V2.1/V2.2 first-pass closure completed. EV-104 executable evidence completed for TSM-002 and TSD-003.

## TSI-001
`xsd_structure_modelling_error_candidate` — V2.1 cannot carry multiple coach records although PDF requires a sequence; V2.2 explicitly corrects this.

## TSM-001
`xsd_operation_or_element_name_error_candidate` — V2.1 uses `TrainSetManagementService.GetTrainSetComposition`; V2.2 history explicitly corrects to `...GetTrainSetCompositionResponse`.

## TSM-002

```text
state: executable-confirmed
classification: xsd_structure_modelling_error_candidate
subtype: operation_group_name_mismatch
scope: official V2.2
confidence: high
```

Official V2.2 globally declares the corrected root:

```text
TrainSetManagementService.GetTrainSetCompositionResponse
```

but `TrainSetManagementServiceOperations` still uses:

```text
TrainSetManagementService.GetTrainSetComposition
```

Executable evidence, GitHub Actions run `33111644388`:

```text
corrected global root: valid
stale old name as global root: invalid / no matching global declaration
actual operation-group harness with stale old name: valid
same harness with corrected Response name: invalid; old name explicitly expected
```

Final handling:

```text
provider/schema finding + operation-manifest override requirement
Do not derive operation support/root inventory solely from the XSD group.
```

## TSD-001
`service_modelling_or_generic_response_candidate` — V2.1 PDF defines parameterized Subscribe/Unsubscribe operations absent from V2.1 service XSD; V2.2 introduces specialized request structures and operations.

## TSD-002
`pdf_table_or_documentation_error_candidate` — V2.2 operation overview lists Retrieve request structures for Unsubscribe, while detailed text and XSD use `TrainSetUnsubscribeRequestStructure`.

## TSD-003

```text
state: resolved - OK with contextual resolver note
classification: service_modelling_or_generic_response_context
scope: official V2.2
confidence: high after EV-104
not_an_automatic_xsd_defect: true
```

V2.2 deliberately exposes the same Subscribe response names with two context-dependent types:

```text
TrainSetDataServiceOperations:
  SubscribeTripRefResponse         -> SubscribeResponseStructure
  SubscribeTripInformationResponse -> SubscribeResponseStructure

global elements:
  SubscribeTripRefResponse         -> RetrieveTripRefResponseStructure
  SubscribeTripInformationResponse -> RetrieveTripInformationResponseStructure
```

Executable evidence, GitHub Actions run `33111644388`:

```text
global SubscribeTripRefResponse accepts Retrieve-style TripRef data event
global SubscribeTripRefResponse rejects generic Active acknowledgement
global SubscribeTripInformationResponse rejects generic Active acknowledgement and expects TripInformation
SubscribeResponseStructure accepts the generic Active acknowledgement shape for both immediate subscription acknowledgements
```

This matches the PDF distinction between immediate Subscribe acknowledgement and later event-based data delivery.

Final handling:

```text
resolver_profile_requirement / operation_manifest_context
The lexical response name alone is insufficient; validation must know acknowledgement vs subscription-data-event context.
```

Evidence document:

```text
docs/pdf_xsd_semantic_audit/24d_executable_validation_trainset.md
```
