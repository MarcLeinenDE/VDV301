# PassengerCountingService validation backlog addendum

Status: local technical validation pending after semantic/provenance closure.

## PCS-VB-001 - V1.0 service-type pool compile

```text
IBIS-IP_PassengerCountingService_V1.0.xsd
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

Goal: confirm the backfilled official service-type pool compiles unchanged.

## PCS-VB-002 - V1.0 aggregate-family compile

When the wider official V1.0 aggregate family is available locally:

```text
IBIS_IP_V1.0.xsd
```

Goal: confirm PCS global operation roots/group compile through the official aggregate family.

## PCS-VB-003 - V2.1 exact selected pool compile

```text
IBIS-IP_PassengerCountingService_V2.1.xsd
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

Goal: compile exactly what the service schema selects; do not substitute V2.1 Common/Enums.

## PCS-VB-004 - ErrorCode positive/negative samples

```text
Positive exact-pool sample: DataNotValid.
Negative exact-pool sample: OperationNotSupported.
Control-only newer-pool check: OperationNotSupported exists in Enums V2.1 but that pool is not selected by PCS V2.1.
```

## PCS-VB-005 - operation inventory / resolver test

```text
V1.0: service-specific type definitions + aggregate operation roots.
V2.1: service-local operation group plus its global declarations.
```

Goal: design the later SDK resolver so historical aggregate routing is explicit and testable.

No task in this addendum has been executed locally yet.
