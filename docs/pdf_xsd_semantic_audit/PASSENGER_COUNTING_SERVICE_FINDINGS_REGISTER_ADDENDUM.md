# PassengerCountingService findings register addendum

Status: V1.0/V2.1 semantic/provenance first-pass completed; PCS-001 now executable-confirmed.

Authority rule:

```text
Validation follows the exact selected service/dependency family.
Historical aggregate provenance is preserved where relevant, while the operational superbranch may use later official self-contained packaging after semantic-diff review.
PDF-required values that are absent from the selected XSD dependency pool are reported as discrepancies, not silently injected.
```

## PCS-001 - V2.1 OperationNotSupported vs selected Enums V1.0

Classification:

```text
state: executable-confirmed PDF/XSD dependency/value-set discrepancy
mismatch_kind: schema_family_or_dependency_value_set
likely_source_issue: xsd_dependency_alignment_or_release_packaging_error_candidate
classification_confidence: very high
version_scope: V2.1
validation_behavior: exact selected Enums V1.0 pool rejects OperationNotSupported
final_handling_bucket: official_schema_family_clarification_candidate
```

Static evidence:

```text
VDV 301-2-8 V2.1 documents OperationNotSupported for the newly added optional counting-control/state operations.
IBIS-IP_PassengerCountingService_V2.1.xsd explicitly includes Common V1.0 and Enums V1.0.
Enums V1.0 lacks OperationNotSupported.
Enums V2.1 contains OperationNotSupported but is not selected by the PCS service XSD.
Common V1.0 DataAcceptedResponseDataStructure uses ErrorCodeEnumeration for ErrorCode.
```

Executable evidence:

```text
GitHub Actions run: 33109367265
head tested: 3ea0215bca353697466e90f8be6af3e3087810bd
tool: tools/validate_pcs_v21_operation_not_supported.py
result: PASS
```

Observed behaviour:

```text
1. Exact PCS V2.1 dependency route compiled successfully.
2. DataAcceptedResponseStructure with ErrorCode=DataNotValid validated successfully.
3. The same structure with ErrorCode=OperationNotSupported failed strict validation.
4. lxml reported that OperationNotSupported is not in the V1.0 enumeration set:
   DataEstimated, FaultData, NoScheduleDataAvailable, DeviceMissing,
   NoServiceResponse, ImportantDataNotAvailable, DataNotValid.
5. An explanatory Enums V2.1-only control accepted OperationNotSupported.
```

Impact:

```text
A PCS V2.1 payload using the documented OperationNotSupported value cannot pass strict validation against the exact service-selected dependency pool.
The SDK must not silently substitute Enums V2.1 for Enums V1.0.
The discrepancy should remain visible as a schema/release-family issue candidate.
```

## PCS-002 - V1.0 operation-root packaging history

Classification:

```text
state: OK with note
mismatch_kind: historical_aggregate_routing / later_self_contained_packaging
likely_source_issue: none
classification_confidence: high
version_scope: V1.0
validation_behavior: operational superbranch uses later official self-contained V1.0 packaging; original tag-1.0 aggregate mapping retained as provenance
final_handling_bucket: resolver_profile_requirement
```

Observation:

```text
The original VDV-301-1.0 PCS service XSD defined PCS-specific structures while IBIS_IP_V1.0.xsd declared the operation roots and PassengerCountingServiceGroup.
A later official release retained service version V1.0 but moved those operation declarations into a self-contained PCS V1.0 service XSD.
Semantic diff review showed this to be packaging-oriented rather than a payload-constraint change.
```

Operational handling:

```text
The superbranch stores the later official self-contained PCS V1.0 revision once.
The original aggregate-owned root mapping remains documented as provenance; no duplicate full V1.0 tag mirror is required.
```
