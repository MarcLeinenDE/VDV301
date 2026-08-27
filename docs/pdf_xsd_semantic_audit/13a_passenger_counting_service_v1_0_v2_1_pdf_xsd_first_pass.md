# PassengerCountingService V1.0 / V2.1 PDF-XSD first pass

Status: semantic/provenance first pass completed. Local XSD compilation and targeted XML validation remain pending.

Source starter:

```text
docs/pdf_xsd_semantic_audit/13_passenger_counting_service_historical_start.md
```

## 1. V1.0 selected official schema family

Service structures:

```text
IBIS-IP_PassengerCountingService_V1.0.xsd
-> IBIS-IP_common_V1.0.xsd
-> IBIS-IP_Enumerations_V1.0.xsd
```

Operation-root layer from the same official release:

```text
IBIS_IP_V1.0.xsd
-> includes IBIS-IP_PassengerCountingService_V1.0.xsd
-> declares PCS global operation elements and PassengerCountingServiceGroup
```

Result:

```text
V1.0 service-level structure validation and V1.0 operation-root validation are historically separate layers of one official release family.
```

## 2. V1.0 core operation / structure comparison

Public V1.0 operation concepts checked:

```text
GetAllData
SubscribeAllData
UnsubscribeAllData
RetrieveSpecificDoorData
SetCounterData
```

Key structure alignment observed:

```text
AllData.TimeStamp             PDF 1:1 / XSD required
AllData.CountingData          PDF 0:* / XSD minOccurs=0 maxOccurs=unbounded
RetrieveSpecificDoorData.DoorID PDF 1:1 / XSD required
SpecificDoorData.TimeStamp    PDF 1:1 / XSD required
SpecificDoorData.CountingData PDF 1:1 / XSD required
SetCounterData.DoorSetList    PDF 1:* / XSD required maxOccurs=unbounded
```

No separate V1.0 field/cardinality defect was opened in this first pass.

## 3. PCS-002 - historical aggregate routing

The V1.0 service XSD itself does not contain the complete set of global operation-root declarations.

The official V1.0 aggregate `IBIS_IP_V1.0.xsd` does.

Classification:

```text
state: OK with note
mismatch_kind: historical_aggregate_routing
likely_source_issue: none
classification_confidence: high
final_handling_bucket: resolver_profile_requirement
```

SDK implication:

```text
A V1.0 resolver must distinguish service-type schema from aggregate operation-root schema.
Do not classify the absence of roots from the service-specific XSD as a missing-schema error.
Do not claim complete V1.0 root validation using only the backfilled PCS service file.
```

The wider aggregate is intentionally deferred to the Base / General Conventions historical block because it includes multiple V1.0 services.

## 4. V2.1 selected official schema family

The official PCS V2.1 service file explicitly selects:

```text
IBIS-IP_PassengerCountingService_V2.1.xsd
-> IBIS-IP_common_V1.0.xsd
-> IBIS-IP_Enumerations_V1.0.xsd
```

This exact family is authoritative for strict PCS V2.1 validation.

The V2.1 release also contains Common/Enums V2.1, but they are not selected by this PCS XSD.

## 5. V2.1 new optional operations

The public V2.1 document adds:

```text
StartCounting
StopCounting
GetCountingState
SubscribeCountingState
UnsubscribeCountingState
```

The V2.1 XSD operation group contains these operation concepts, including:

```text
PassengerCountingService.StartCountingRequest
PassengerCountingService.StartCountingResponse
PassengerCountingService.StopCountingRequest
PassengerCountingService.StopCountingResponse
PassengerCountingService.GetCountingStateRequest
PassengerCountingService.GetCountingStateResponse
PassengerCountingService.SubscribeCountingStateRequest/Response
PassengerCountingService.UnsubscribeCountingStateRequest/Response
```

The existing core operation family remains present.

## 6. PCS-001 - OperationNotSupported dependency/value-set conflict

The V2.1 document repeatedly states that `ErrorCodeEnumeration` was extended by:

```text
OperationNotSupported
```

for the optional counting-control/state operations so a service can indicate that an optional operation is unavailable.

Exact XSD chain:

```text
PCS V2.1 -> Common V1.0 -> Enumerations V1.0
```

Enumerations V1.0 values do not include `OperationNotSupported`.

Enumerations V2.1 does include `OperationNotSupported`, but that file is not selected by the PCS V2.1 XSD.

The mismatch is executable, not merely editorial, because Common V1.0 uses `ErrorCodeEnumeration` in the relevant data/wrapper structures. In particular:

```text
DataAcceptedResponseDataStructure.ErrorCode -> ErrorCodeEnumeration
IBIS-IP.boolean.ErrorCode -> ErrorCodeEnumeration
IBIS-IP.string.ErrorCode -> ErrorCodeEnumeration
```

The PCS V2.1 service group uses `DataAcceptedResponseStructure` for StartCountingResponse and StopCountingResponse, while generic subscribe responses use wrapper types from Common V1.0.

Classification:

```text
mismatch_kind: schema_family_or_dependency_value_set
likely_source_issue: xsd_dependency_alignment_or_release_packaging_error_candidate
classification_confidence: high
validation_behavior: exact selected V1.0 enum pool excludes OperationNotSupported
final_handling_bucket: local_validation_required + official_schema_family_clarification_candidate
```

Strict validator behaviour:

```text
Do not silently add OperationNotSupported to Enums V1.0.
Do not silently substitute Enums V2.1.
Do not silently substitute Common V2.1.
Report the selected dependency pool and explain the PDF/XSD conflict.
```

## 7. Why there is no automatic fix

Changing the PCS V2.1 explicit Enumerations include to V2.1 is not safely equivalent to a one-line correction because Common V1.0 itself includes Enumerations V1.0.

Changing PCS V2.1 to Common V2.1 would select a broader newer base schema and could change semantics outside the intended optional-operation fix.

Therefore:

```text
PCS-001 is a confirmed discrepancy candidate, not a ready-made patch.
```

Any official-facing correction decision must wait for the end-of-audit review and technical compile/sample tests.

## 8. Technical validation backlog

```text
PCS-VB-001: compile official PCS V1.0 service-type pool with Common V1.0 + Enums V1.0.
PCS-VB-002: when the complete V1.0 aggregate family is available locally, compile IBIS_IP_V1.0.xsd and verify PCS operation-root declarations.
PCS-VB-003: compile PCS V2.1 with its exact selected Common V1.0 + Enums V1.0 pool.
PCS-VB-004: positive PCS V2.1 response sample using a V1.0-known ErrorCode such as DataNotValid.
PCS-VB-005: negative exact-pool sample using OperationNotSupported in DataAcceptedResponseData.ErrorCode.
PCS-VB-006: control-only V2.1 Common/Enums harness showing OperationNotSupported exists in Enums V2.1, while clearly marking that pool as not selected by PCS V2.1.
PCS-VB-007: operation-group/root inventory test for V1.0 aggregate vs V2.1 service-group modelling.
```

These local tests were not executed in this block.

## 9. Result

```text
V1.0 official service XSD backfill is byte-identical to release tag source.
V1.0 operation roots are provided by the official aggregate IBIS_IP_V1.0.xsd: PCS-002 OK with note.
V2.1 exact service dependency family is Common V1.0 + Enums V1.0.
V2.1 optional operation additions are present in the service XSD group.
PCS-001 is a confirmed PDF/XSD dependency-value-set conflict around OperationNotSupported.
No XSD was modified.
No dependency was rewritten.
No local compile/sample validation is claimed.
```
