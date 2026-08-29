# Audit handoff delta — COMMON V1.0 Deep Read closure — 2026-08-30

## Closed unit

`COMMON_V1.0` / official public VDV 301-2-1 Common publication.

Pinned PDF SHA-256: `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf`.
Independent Fresh Read freeze: `f21aa84b0aae5222cbfdcc4757b599f8133e2d36`.

## Exact XSD authority

```text
official import commit: 604a5a5c7608977e483072f7e450d7381cc182e4
Common V1.0:            194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
Enumerations V1.0:      a9bea5bc73003ed91ded8519db06c32c4067831d
```

No Common V1.1 XSD was found. The PDF's internal Version 1.1 revision is retained as
documentation/data-definition history, not converted into a new executable authority.

## EV-117

```text
checker: tools/validate_common_v10_ev117.py
run:     33279461529
job:     99172025835
result:  PASS
```

The initial controlled run `33279395750` failed solely because a positive
InternationalTextType fixture omitted required `Language`; the corrected fixture passed.
No finding/XSD was altered to force success.

## Reconciliation

Existing CE identities reused:
`CE-005`, `CE-007`, `CE-012..019`, `CE-021`, `CE-022`, `CE-025`, `CE-026`.

New unique findings:
`DRCOM10-001..DRCOM10-007`.

Detailed mapping:
`audit_registry/deep_read_findings_delta_common_v10_2026-08-30.json`.

## Guardrails

- exact selected XSD remains executable validation authority;
- no latest-XSD-wins;
- no invented Common V1.1 XSD;
- no XSD modification in this closure;
- unresolved later-version visual portions are not silently closed by V1.x evidence.

## Resume

Next natural Deep Read unit: `COMMON_V2.0`.
