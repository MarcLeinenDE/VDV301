# EV-116 - SystemMonitoringService V2.2 official executable evidence

Status: PASS

Date: 2026-08-29

## Exact official authority

EV-116 executes the exact official `VDV-301-2.2` family. The integration branch is blob-identical for all three selected files.

```text
SystemMonitoringService V2.2  d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c
Common V2.2                   468fee6d177e7185dbcd5d3f90cfb114e29e01ae
Enumerations V2.2             2a23b512379b18e8f122ac1272cef8229fb86283
```

No later Common/Enumerations family is substituted.

## Run

```text
checker: tools/validate_sms_v22_ev116.py
checker introduction commit: e34e0f54f53b334ebd3652393aad1744cb287852
run: 33269006407
job: 99144006184
temporary run head: 5107f5465ce084543a026f0eace204e017315136
result: PASS
```

## Confirmed

- exact three official Git blobs matched;
- the service XSD includes exact Common V2.2 + Enumerations V2.2 and compiles;
- `SystemMonitoringServiceGroup` contains exactly `GetDeviceStatusResponse` and `GetServiceStatusResponse` service-local response elements;
- Common V2.2 contains the generic Subscribe/Unsubscribe request and response structures referenced by the PDF;
- exact `SystemMonitoringService.GetServiceStatusResponse` validates on its `OperationErrorMessage` branch;
- invented `SystemMonitoringService.GetSystemStatusResponse` has no global declaration and is invalid;
- exact `SystemMonitoringService.GetDeviceStatusResponse` validates;
- SMS response-data list wrappers are required 1:1;
- Common V2.2 list-item declarations are observed as 0:* only for authority/routing context.

## Evidence boundary

EV-116 strengthens the executable side of SMS-001 and SMS-002. It does **not** by itself revalidate Common findings CE-012, CE-018 or CE-019, nor does it make PDF prose executable authority.

No XSD changed.
