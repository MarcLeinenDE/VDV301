# Audit handoff delta - TrainSet services 19B

Continuation point after V2.1/V2.2 TrainSet services first-pass closure.

## Completed

```text
19_train_set_services_historical_start.md
19a_train_set_services_v2_1_v2_2_pdf_xsd_first_pass.md
19b_train_set_services_findings_and_closure.md
TRAIN_SET_SERVICES_FINDINGS_REGISTER_ADDENDUM.md
TRAIN_SET_SERVICES_VALIDATION_BACKLOG_ADDENDUM.md
OFFICIAL_PR_CANDIDATES_ADDENDUM_TRAIN_SET.md
generated/train_set_services_historical_scope_matrix.csv
generated/train_set_services_findings_closure_matrix.csv
```

## Key routing

```text
TSD 2.1 -> Common 2.0 + Enums 2.0 + CIS 2.0
TSI 2.1 -> Common 2.0
TSM 2.1 -> Common 2.0 + Enums 2.0 + TSI 2.1
TSD 2.2 -> Common 2.2 + Enums 2.2
TSI 2.2 -> Common 2.2
TSM 2.2 -> Common 2.2 + Enums 2.2 + TSI 2.2
```

## Key findings

```text
TSI-001 V2.1 multi-coach structure defect corrected V2.2.
TSM-001 V2.1 response-root name corrected V2.2.
TSM-002 V2.2 operation group still has stale old response-root name.
TSD-001 V2.1 subscription modelling absent from XSD despite PDF; V2.2 introduces technical correction.
TSD-002 V2.2 Unsubscribe operation overview still lists old Retrieve request types.
TSD-003 V2.2 generic subscription acknowledgement vs global event-response typing requires local context testing.
```

## Safety

```text
No XSD changed.
No PR/comment/merge action.
No compile/sample validation claimed.
master untouched.
```

## Next block

```text
20_device_management_service_v2_0_v2_1_historical_completion.md
```
