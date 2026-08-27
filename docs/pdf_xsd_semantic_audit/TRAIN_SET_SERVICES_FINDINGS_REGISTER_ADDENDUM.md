# TrainSet services findings register addendum

Status: V2.1/V2.2 first-pass closure completed.

## TSI-001
`xsd_structure_modelling_error_candidate` — V2.1 cannot carry multiple coach records although PDF requires a sequence; V2.2 explicitly corrects this.

## TSM-001
`xsd_operation_or_element_name_error_candidate` — V2.1 uses `TrainSetManagementService.GetTrainSetComposition`; V2.2 history explicitly corrects to `...GetTrainSetCompositionResponse`.

## TSM-002
`xsd_structure_modelling_error_candidate` — V2.2 global root uses corrected `...Response`, but `TrainSetManagementServiceOperations` still uses stale old name.

## TSD-001
`service_modelling_or_generic_response_candidate` — V2.1 PDF defines parameterized Subscribe/Unsubscribe operations absent from V2.1 service XSD; V2.2 introduces specialized request structures and operations.

## TSD-002
`pdf_table_or_documentation_error_candidate` — V2.2 operation overview lists Retrieve request structures for Unsubscribe, while detailed text and XSD use `TrainSetUnsubscribeRequestStructure`.

## TSD-003
`service_modelling_or_generic_response_candidate` — V2.2 `SubscribeTripRefResponse`/`SubscribeTripInformationResponse` are generic `SubscribeResponseStructure` in the operation group but data Retrieve-response structures as global elements. Resolve with local subscription-context tests before stronger classification.
