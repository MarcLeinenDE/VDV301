# Executable validation - PCS-001 OperationNotSupported

Status: completed; PCS-001 executable-confirmed.

## Scope

PassengerCountingService V2.1 exact dependency route:

```text
IBIS-IP_PassengerCountingService_V2.1.xsd
  -> IBIS-IP_common_V1.0.xsd
  -> IBIS-IP_Enumerations_V1.0.xsd
```

Explanatory control only:

```text
IBIS-IP_Enumerations_V2.1.xsd
```

The V2.1 enum file is not substituted into the PCS production route.

## Static premise

PCS V2.1 defines StartCountingResponse and StopCountingResponse with `DataAcceptedResponseStructure`.

Common V1.0 defines:

```text
DataAcceptedResponseStructure
  -> DataAcceptedResponseDataStructure
       -> TimeStamp
       -> DataAccepted
       -> ErrorCode : ErrorCodeEnumeration (optional)
       -> ErrorInformation (optional)
```

Enums V1.0 contains ErrorCode values through `DataNotValid` but not `OperationNotSupported`.

Enums V2.1 adds `OperationNotSupported`.

## Executed tool

```text
tools/validate_pcs_v21_operation_not_supported.py
```

Evidence run:

```text
workflow: schema-audit-validation
run number: 5
run id: 33109367265
head SHA tested: 3ea0215bca353697466e90f8be6af3e3087810bd
Python: 3.12.14
lxml: 6.1.2
pcs_status: 0
```

## Results

```text
PASS exact PCS V2.1 dependency route compiled
PASS exact route accepted ErrorCode=DataNotValid
PASS exact route rejected ErrorCode=OperationNotSupported
PASS Enums V2.1 explanatory control accepted OperationNotSupported
```

Validator evidence for the rejection:

```text
OperationNotSupported is not an element of the set:
DataEstimated
FaultData
NoScheduleDataAvailable
DeviceMissing
NoServiceResponse
ImportantDataNotAvailable
DataNotValid
```

## Finding conclusion

PCS-001 is no longer merely inferred from include/dependency inspection.

It is executable-confirmed that:

```text
The exact PCS V2.1 XSD route cannot validate the OperationNotSupported value documented for the optional operations.
```

Classification remains:

```text
schema_family_or_dependency_value_set discrepancy
xsd_dependency_alignment_or_release_packaging_error_candidate
```

No XSD change is made.
No Enums V2.1 substitution is introduced.

## SDK consequence

The future SDK must:

```text
1. keep the exact PCS V2.1 dependency route authoritative;
2. surface OperationNotSupported validation failure as a known documented discrepancy when applicable;
3. never auto-upgrade the enum dependency;
4. keep schema authority and documentation diagnostics separate.
```

## Next planned executable block

```text
24b_executable_validation_ce_018.md
EV-102 - ServiceIdentificationWithStateList PDF 1:* vs XSD minOccurs=0
```
