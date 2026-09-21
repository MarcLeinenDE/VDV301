# Runtime-mapping review — SystemMonitoringService V2.2 SMS-002 — 2026-09-21

Status: **completed / reviewed / not implemented**.

## Result

`SMS-002` was reviewed against the exact official SystemMonitoringService V2.2 XSD family, EV-116 and preserved EV-156 evidence.

Decision: `candidate -> reviewed`.

## Runtime boundary

The advisory is eligible only when:

- selected strict profile is official SystemMonitoringService V2.2;
- selected-XSD validation is already **INVALID**;
- the rejected global root is exactly `SystemMonitoringService.GetSystemStatusResponse`;
- the selected XSD declares `SystemMonitoringService.GetServiceStatusResponse` and no `GetSystemStatusResponse` root.

Effect: preserve XSD INVALID and explain the known PDF heading/name defect.

## Guards

- no `GetSystemStatusResponse` compatibility alias;
- no generalized `SystemStatus` operation-family aliasing;
- no automatic root rewrite;
- `GetServiceStatusResponse` remains the authoritative executable root;
- selected-XSD validity remains normative.

## Mapping inventory after review

```text
reviewed        61
candidate       17
not_designed     1
not_applicable 113
implemented      0
```

## Evidence and primary gate

- EV-156: independent run **34460160697**, closure **34460497412**
- EV-116: run **33269006407**
- primary runtime-mapping gate **35552308342**: **SUCCESS**
- closure/consistency gate **35552407083**: **SUCCESS**

The gate verified:

- exact SMS V2.2 / Common V2.2 / Enumerations V2.2 blobs;
- preserved EV-116;
- `GetServiceStatusResponse` validates;
- invented `GetSystemStatusResponse` is rejected;
- no alias or automatic rewrite is introduced;
- all root XSDs remain unchanged;
- synchronized SDK/runtime-mapping counters pass the hardened consistency validator.

No executable Known-Issues matcher was added and no XSD was changed.
