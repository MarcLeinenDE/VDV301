# Cross-service Subscribe / Unsubscribe modelling closure

Status: first-pass cross-service closure completed; targeted compile/sample/runtime validation still pending.

Scope:

```text
VDV 301-2 General Conventions V2.3/V2.4 operation conventions
Common V1.0, V2.0, V2.2 and V2.4 generic subscription structures
CustomerInformationService V2.x
SystemMonitoringService V2.2
DeviceManagementService V2.2 as an explicit service-local modelling comparison
TrainSetDataService V2.1/V2.2 specialized Retrieve-subscription case
```

Authority rule:

```text
The selected XSD family validates concrete XML payload structures.
Service documents and General Conventions define operation semantics and transport behaviour.
A service XSD operation-group member list is not by itself a complete authoritative catalogue of every documented HTTP operation.
No XSD is changed in this block.
```

## 1. Generic subscription convention

The General Conventions define the conceptual sequence for currently valid Get-data:

```text
Get...
Subscribe...
Unsubscribe...
```

Subscribe establishes automatic delivery when the subscribed data changes. Unsubscribe terminates the subscription. Retrieve operations are parameter-dependent and, as a general convention, are not intended for ordinary subscription because they do not represent the service's complete currently-valid data state.

Common supplies generic subscription payload structures. The checked Common history confirms:

```text
SubscribeRequestStructure
SubscribeResponseStructure
UnsubscribeRequestStructure
UnsubscribeResponseStructure
```

`UnsubscribeRequestStructure` is present already in Common V1.0 and V2.0 and remains present in V2.2/V2.4.

The checked Common files contain no `TerminateSubscribeRequestStructure` or `TerminateSubscribeResponseStructure`.

## 2. SUB-001 - General-Conventions table uses non-XSD TerminateSubscribe type names

General Conventions V2.3 and V2.4 table 4 show:

```text
UnsubscribeData request  -> TerminateSubscribeRequestStructure
UnsubscribeData response -> TerminateSubscribeResponseStructure
```

This conflicts with the executable Common family, which uses:

```text
UnsubscribeRequestStructure
UnsubscribeResponseStructure
```

The operation naming convention itself also says the operation verb is `Unsubscribe`.

Classification:

```text
pdf_table_or_documentation_error_candidate
```

Validation handling:

```text
Do not create TerminateSubscribe* aliases in the SDK.
Validate against the exact selected Common XSD types/elements.
Expose the General-Conventions table wording as a documentation note if relevant.
```

Historical confidence is strengthened because Common V1.0 and V2.0 already use `UnsubscribeRequestStructure`; this is not a newly renamed V2.4 type.

## 3. CIS-002 resolution

Earlier CIS finding `CIS-002` observed that CIS service PDFs describe Subscribe/Unsubscribe operations while the CIS V2.x service operation groups contain mainly Get-response and Retrieve-specific entries rather than explicit service-prefixed Subscribe/Unsubscribe entries.

Cross-service result:

```text
CIS-002 -> resolved as ok_with_note / generic subscription modelling.
```

Reason:

```text
General Conventions define the Get/Subscribe/Unsubscribe operation family.
Common provides generic subscription request/response structures.
Therefore absence of service-prefixed Subscribe/Unsubscribe members from the local CIS operation group is not sufficient evidence of a CIS schema defect.
```

Guard:

```text
This closure does not claim that every CIS operation can be discovered solely from Common XSD.
The SDK still needs an operation manifest derived from service documentation/conventions plus schema payload mapping.
```

## 4. SMS-001 resolution

SystemMonitoringService V2.2 documents Subscribe/UnsubscribeDeviceStatus and Subscribe/UnsubscribeServiceStatus, while its local XSD group contains only the two Get response elements.

Cross-service result:

```text
SMS-001 -> resolved as ok_with_note / generic subscription modelling.
```

The SMS document itself points to generic subscription structures, and Common V2.2 supplies those structures.

No service-specific schema correction is proposed.

## 5. SUB-002 - service operation groups use inconsistent subscription encoding styles

DeviceManagementService V2.2 provides a useful contrast. Its `DeviceManagementServiceGroup` explicitly lists many service-prefixed Subscribe/Unsubscribe request/response members and assigns them the generic Common types.

CIS and SMS do not use the same group-encoding style.

Observation:

```text
DMS: explicit service-prefixed subscription members in local group, generic Common types.
CIS/SMS: documented subscription operations, but no equivalent service-prefixed members in local group.
```

Classification:

```text
service_modelling_or_generic_response_candidate
```

Current interpretation:

```text
This is a schema modelling/style inconsistency across services, not enough evidence for a payload-validity defect.
Do not normalize or rewrite the XSDs during audit.
Do not use operation-group membership alone as the SDK supported-operation catalogue.
```

## 6. TrainSetData is a real specialized exception

TrainSetDataService demonstrates why the generic rule cannot be applied mechanically to every operation.

The V2.2 XSD comments explicitly explain that subscriptions to Retrieve operations differ from subscriptions to Get operations because a Retrieve operation has one or more selection parameters. TrainSet needs `CoachNumber`, so V2.2 defines:

```text
TrainSetSubscribeRequestStructure
TrainSetUnsubscribeRequestStructure
```

with the generic callback endpoint fields plus `CoachNumber`.

This supports the existing historical interpretation:

```text
TSD-001 remains a valid historical service-modelling finding for V2.1 because the V2.1 document already describes these parameterized subscriptions while V2.1 XSD does not provide the specialized operation structures; V2.2 explicitly introduces them.
TSD-002 remains a PDF-table candidate because the V2.2 operation overview still names Retrieve request structures for Unsubscribe while detailed text/XSD use TrainSetUnsubscribeRequestStructure.
```

## 7. TSD-003 remains open

In V2.2 `TrainSetDataServiceOperations` locally assigns:

```text
SubscribeTripRefResponse         -> SubscribeResponseStructure
SubscribeTripInformationResponse -> SubscribeResponseStructure
```

but global elements of the same names are declared as:

```text
SubscribeTripRefResponse         -> RetrieveTripRefResponseStructure
SubscribeTripInformationResponse -> RetrieveTripInformationResponseStructure
```

This can plausibly correspond to two semantic stages:

```text
initial Subscribe operation acknowledgement
subsequent subscribed data callback
```

but that interpretation has not yet been proven by local schema/root tests or a runtime trace.

Therefore:

```text
TSD-003 stays service_modelling_or_generic_response_candidate.
No XSD change.
```

## 8. SubscribeResponse heartbeat semantics

Common V2.4 `SubscribeResponseStructure` is a sequence of optional members and includes optional `Heartbeat`.

Its XSD annotation explains that if a non-zero heartbeat is returned, the client can expect the service to send data at least every heartbeat interval and can use that expectation for connection-quality monitoring.

SDK consequence:

```text
Subscription runtime state cannot be reduced to a one-time XML validity check.
The operation manifest should expose heartbeat semantics and callback monitoring separately from request/response XSD validation.
```

## 9. Required SDK operation-manifest model

The audit now supports an explicit operation metadata layer independent of raw XSD-group enumeration.

Minimum fields should include:

```text
service_id
service_version
operation_name
operation_kind: get | subscribe | unsubscribe | retrieve | control | other
http_method
request_payload_schema_ref
immediate_response_schema_ref
callback_payload_schema_ref
callback_endpoint_fields
heartbeat_supported
selection_parameters
schema_authority/pool_id
source_document/reference
```

Resolver consequence:

```text
DNS-SD resolves service/version/endpoint profile.
Operation manifest resolves operation and semantic payload roles.
Selected XSD pool validates each concrete payload role.
Runtime subscription monitor checks callbacks/heartbeat.
```

This keeps transport semantics and XSD authority separate while allowing mixed service versions.

## 10. Findings closure table

```text
SUB-001  General-Conventions TerminateSubscribe* type names vs Common Unsubscribe* -> PDF documentation candidate.
SUB-002  Cross-service operation-group subscription encoding differs -> service modelling candidate; no correction now.
CIS-002  resolved -> ok_with_note / generic subscription modelling.
SMS-001  resolved -> ok_with_note / generic subscription modelling.
TSD-001  remains historical modelling finding; V2.2 supplies specialized correction.
TSD-002  remains PDF documentation candidate.
TSD-003  remains open service modelling/generic response candidate.
```

## 11. Validation status

Not executed yet:

```text
compile/root-context checks proving how local group elements and global elements are selected in each service family
positive Subscribe/Unsubscribe request/response samples
TSD V2.2 immediate-response vs callback-root samples
runtime callback/heartbeat trace
```

No technical validation claim is made.

## 12. Closure

```text
Cross-service subscription modelling first pass completed.
Generic CIS/SMS subscription notes resolved without inventing XSD elements.
General-Conventions TerminateSubscribe naming discrepancy isolated as SUB-001.
Cross-service group-style inconsistency retained conservatively as SUB-002.
TrainSet specialized Retrieve-subscription modelling retained separately.
```

Next phase:

```text
24_executable_validation_matrix_start.md
```
