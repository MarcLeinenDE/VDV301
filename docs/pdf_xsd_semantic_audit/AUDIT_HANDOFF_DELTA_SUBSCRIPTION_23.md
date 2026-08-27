# Audit handoff delta - Cross-service subscription block 23

Status: first-pass cross-service closure completed.

Parent branch head:

```text
f1c524c6ad3ac6d583b48b946c283d63b8192aec
```

Key results:

```text
CIS-002 resolved as ok_with_note: generic subscription modelling exists in General Conventions/Common; missing local service-group entries alone are not a CIS schema defect.
SMS-001 resolved the same way.
```

New cross-service findings:

```text
SUB-001: General Conventions V2.3/V2.4 table 4 names TerminateSubscribeRequestStructure/TerminateSubscribeResponseStructure, but checked Common V1.0/V2.0/V2.2/V2.4 uses UnsubscribeRequestStructure/UnsubscribeResponseStructure. Documentation candidate; validation follows XSD.
SUB-002: DMS explicitly encodes service-prefixed subscription members in its group while CIS/SMS do not. Keep as service_modelling_or_generic_response_candidate; do not normalize XSDs.
```

TrainSet handling:

```text
TSD-001 remains historical: V2.1 document has parameterized Retrieve subscriptions absent from V2.1 schema; V2.2 introduces specialized request structures.
TSD-002 remains PDF table candidate.
TSD-003 remains open because V2.2 group and global declarations assign different semantic response types to the same Subscribe response names.
```

SDK architecture consequence:

```text
Do not derive operation support solely from XSD service-group members.
Introduce an explicit operation manifest separating operation semantics, immediate response, callback payload and heartbeat from XSD pool selection.
```

No local compile/sample/runtime subscription validation has been executed.

Next:

```text
24_executable_validation_matrix_start.md
```
