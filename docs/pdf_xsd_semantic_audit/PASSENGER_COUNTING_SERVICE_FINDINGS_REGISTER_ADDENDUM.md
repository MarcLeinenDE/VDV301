# PassengerCountingService findings register addendum

Status: V1.0/V2.1 semantic/provenance first-pass closure completed.

Authority rule:

```text
Validation follows the exact selected service/dependency family.
Historical aggregate routing is preserved where present.
PDF-required values that are absent from the selected XSD dependency pool are reported as discrepancies, not silently injected.
```

## PCS-001 - V2.1 OperationNotSupported vs selected Enums V1.0

Classification:

```text
state: confirmed PDF/XSD dependency/value-set discrepancy
mismatch_kind: schema_family_or_dependency_value_set
likely_source_issue: xsd_dependency_alignment_or_release_packaging_error_candidate
classification_confidence: high
version_scope: V2.1
validation_behavior: exact selected Enums V1.0 pool excludes OperationNotSupported
final_handling_bucket: local_validation_required + official_schema_family_clarification_candidate
```

Observation:

```text
VDV 301-2-8 V2.1 documents OperationNotSupported for the newly added optional counting-control/state operations.
IBIS-IP_PassengerCountingService_V2.1.xsd explicitly includes Common V1.0 and Enums V1.0.
Enums V1.0 lacks OperationNotSupported.
Enums V2.1 contains OperationNotSupported but is not selected by the PCS service XSD.
Common V1.0 structures used by these responses reference ErrorCodeEnumeration.
```

Impact:

```text
A payload using OperationNotSupported in the documented ErrorCode path is expected to fail strict validation against the exact selected PCS V2.1 dependency pool.
No newer enum pool may be substituted silently.
```

## PCS-002 - V1.0 operation roots are aggregate-owned

Classification:

```text
state: OK with note
mismatch_kind: historical_aggregate_routing
likely_source_issue: none
classification_confidence: high
version_scope: V1.0
validation_behavior: service type schema + official aggregate operation-root schema
final_handling_bucket: resolver_profile_requirement
```

Observation:

```text
The official PCS V1.0 service XSD defines PCS-specific structures.
The official VDV-301-1.0 aggregate IBIS_IP_V1.0.xsd includes that service XSD and declares the PCS operation roots and PassengerCountingServiceGroup.
```

Impact:

```text
SDK schema resolution for V1.0 must understand the aggregate layer.
The absence of global operation roots from the service-specific V1.0 file is not a schema defect.
```
