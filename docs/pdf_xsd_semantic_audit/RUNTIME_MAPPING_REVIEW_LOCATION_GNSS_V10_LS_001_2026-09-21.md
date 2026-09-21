# Runtime-mapping review — GNSSLocationService V1.0 LS-001 — 2026-09-21

Status: **completed / reviewed / not implemented**.

## Result

`LS-001` was reviewed against the exact official GNSSLocationService V1.0 XSD and preserved EV-153 evidence.

Decision: `candidate -> reviewed`.

## Runtime boundary

The advisory is eligible only when:

- selected strict profile is official GNSSLocationService V1.0;
- the selected XSD result is already **INVALID**;
- `GNSSLocationService.Data` contains exact PDF spelling `HorizontalDilutionOfPrecision`;
- the selected XSD declares `HoriziontalDilutionOfPrecision` and does not declare the PDF spelling.

Effect: preserve XSD INVALID and explain the known PDF/XSD identifier mismatch.

## Guards

- the PDF spelling must not be accepted or normalized as an alias;
- `HoriziontalDilutionOfPrecision` remains the authoritative selected-XSD XML name;
- no generalized spelling-correction logic is introduced for other GNSS identifiers;
- selected-XSD validity remains authoritative.

## Mapping inventory after review

```text
reviewed        59
candidate       19
not_designed     1
not_applicable 113
implemented      0
```

## Evidence and primary gate

- EV-153: run **34229647400**, job **102072276013**, closure **34230809592**
- primary runtime-mapping gate **35551852822**: **SUCCESS**

The gate verified:

- exact GNSS V1.0 / Common V1.0 / Enumerations V1.0 blobs;
- `HoriziontalDilutionOfPrecision` exists and validates;
- `HorizontalDilutionOfPrecision` is absent and rejected;
- preserved EV-153 evidence identity;
- no alias/normalization policy is introduced;
- all root XSDs remain unchanged.

No executable Known-Issues matcher was added and no XSD was changed.
