# TrainSet services findings and first-pass closure

Status: V2.1/V2.2 semantic/provenance first-pass closure completed. Local technical validation remains pending.

## Exact routing summary

```text
TSD V2.1 -> Common V2.0 + Enums V2.0 + CIS V2.0
TSI V2.1 -> Common V2.0
TSM V2.1 -> Common V2.0 + Enums V2.0 + TSI V2.1

TSD V2.2 -> Common V2.2 + Enums V2.2
TSI V2.2 -> Common V2.2
TSM V2.2 -> Common V2.2 + Enums V2.2 + TSI V2.2
```

No single TrainSet-wide latest dependency pool is valid.

## Findings closure

```text
TSI-001  xsd_structure_modelling_error_candidate
         V2.1 composition cannot represent documented multi-coach sequence; explicitly corrected V2.2.

TSM-001  xsd_operation_or_element_name_error_candidate
         V2.1 GetTrainSetComposition root corrected to GetTrainSetCompositionResponse in V2.2.

TSM-002  xsd_structure_modelling_error_candidate / operation-group mismatch
         V2.2 global root corrected but operation group retains stale old name.

TSD-001  service_modelling_or_generic_response_candidate
         V2.1 PDF subscription operations absent from V2.1 service XSD; V2.2 introduces specialized model.

TSD-002  pdf_table_or_documentation_error_candidate
         V2.2 operation table retains old Retrieve request types for Unsubscribe while detail text/XSD use TrainSetUnsubscribeRequestStructure.

TSD-003  service_modelling_or_generic_response_candidate
         V2.2 Subscribe response names have different types in operation-group vs global-root contexts; technical resolution pending.
```

## SDK implications

```text
- Resolve all three TrainSet services separately.
- Preserve V2.1 and V2.2 exact dependency pools.
- Do not map V2.1 payloads to V2.2 merely because V2.2 fixes known defects.
- Diagnostic output may explain that a defect is corrected in a later schema, but technical validation still follows the selected historical XSD.
- Operation-group inventory cannot be assumed identical to global-root inventory; TSM-002 demonstrates why.
- Generic subscription acknowledgement and event payload contexts may require separate resolver roles; TSD-003 remains open until technical testing.
```

## Validation status

```text
Semantic/provenance first pass: closed.
Local XSD compilation: not performed.
Sample validation: not performed.
No XSD correction: yes.
No PR/comment/merge action: yes.
```

## Next planned block

```text
20_device_management_service_v2_0_v2_1_historical_completion.md
```

Goal: close the remaining older DMS V2.0/V2.1 history before the Base/General and Network-infrastructure closure blocks.
