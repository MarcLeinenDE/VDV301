# Audit handoff delta — AnalogRadioService V2.4 Deep Read

Date: 2026-08-29
Branch: `dev/schema-integration`

## Closure

`ARA_V2.4` completed the independent Fresh Read, pinned-byte visual review and post-freeze historical reconciliation.

Official PDF:

```text
VDV 301-2-19 AnalogRadioService V2.4, 01/2023
sha256 d0c8d8a3b8719c13b09f43ec98349d2e9b22d07fec0c9267bceff0812cbbc34c
size 1009640
pin run 33269415752
render/read run 33269472968
```

XSD authority remains candidate/integration:

```text
AnalogRadioService V2.4 48fb303b80936d2d762f0889ce0c359e04c16e5b
Common V2.3 official    0d8926c4063c12de9a5e68b6f0addaab35a55dc1
Enumerations V2.2      2a23b512379b18e8f122ac1272cef8229fb86283
no VDV-301-2.4 official release tag/service XSD
```

EV-105 needs no new run: canonical full-suite run `33228250613` already reran the checker on that current route and passed.

Revalidated historical findings: `ARA-001` through `ARA-004`.
New findings: `DRARA24-001`, `DRARA24-002`.

No XSD changed.

## Next natural document

`VDV301-3_02-2020` — Network Infrastructure / Netzwerkinfrastruktur.

Continue document-first: establish/pin the official source, fresh-read independently, and only after freeze reconcile historical network/discovery material.
