# Runtime-mapping review — PassengerCountingService V2.1 PCS-001 — 2026-09-21

Status: **completed / reviewed / not implemented**.

## Result

`PCS-001` was reviewed against the exact official PassengerCountingService V2.1 dependency route and preserved EV-155 evidence.

Decision: `candidate -> reviewed`.

## Runtime boundary

The advisory is eligible only when:

- selected strict profile is official PassengerCountingService V2.1;
- the exact selected route is `PCS V2.1 -> Common V1.0 -> Enumerations V1.0`;
- selected-XSD validation is already **INVALID** because `ErrorCode=OperationNotSupported` is used at an ErrorCodeEnumeration position;
- selected Enumerations V1.0 does not contain `OperationNotSupported`.

The separate Enumerations V2.1 file contains the value only as explanatory/correction-history control.

## Guards

- no Enumerations V2.1 substitution, merge or auto-upgrade;
- no enum-value injection into the selected V1.0 pool;
- `OperationNotSupported` remains invalid on the exact selected PCS V2.1 route;
- existing V1.0 values such as `DataNotValid` retain normal validity;
- selected-XSD validity remains authoritative.

## Mapping inventory after review

```text
reviewed        60
candidate       18
not_designed     1
not_applicable 113
implemented      0
```

## Evidence and primary gate

- EV-155: independent run **34447583426**, closure **34448427086**
- deterministic validator: `tools/validate_pcs_v21_operation_not_supported.py`
- primary runtime-mapping gate **35552057273**: **SUCCESS**
- closure/consistency gate **35552137233**: **SUCCESS**

The gate verified:

- exact PCS V2.1 / Common V1.0 / Enumerations V1.0 blobs;
- exact dependency includes;
- `DataNotValid` validates on the selected route;
- `OperationNotSupported` is rejected on the selected route;
- the separate Enumerations V2.1 control contains/accepts `OperationNotSupported`;
- no newer enum family is substituted into PCS V2.1;
- all root XSDs remain unchanged;
- synchronized SDK/runtime-mapping counters pass the hardened consistency validator.

No executable Known-Issues matcher was added and no XSD was changed.
