# Audit handoff delta — COMMON V2.0 Deep Read closure — 2026-08-30

## Closed unit

`COMMON_V2.0` / official VDV 301-2-1 V2.0.

```text
PDF SHA-256: 23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088
Fresh Read freeze: 60d8e6a444473615771bcab52e22293d96a8aa04
official XSD tag: VDV-301-2.0
Common blob: 8608e3dcd665c197c34da7f6ec6af5a3758da164
Enumerations blob: 27e3c183b00381d959622d13c10543123af8eef6
```

## EV-118

```text
checker: tools/validate_common_v20_ev118.py
run:     33280224191
job:     99174026383
result:  PASS
```

## Reconciliation

Existing CE/DRCOM10 IDs were reused wherever the independent Fresh Read rediscovered the
same semantic discrepancy. Only `DRCOM20-001` is new. `CE-020` remains V2.3-specific.

V1.x corrections that genuinely align in V2.0 were actively falsified and are not carried
forward as defects: Connection optionality/time names, RouteDirection, readyForShutdown,
PassengerCounting/video service names and ServiceState starting.

No XSD changed. No candidate authority was introduced.

## Resume

Next natural Deep Read unit: `COMMON_V2.1`.
