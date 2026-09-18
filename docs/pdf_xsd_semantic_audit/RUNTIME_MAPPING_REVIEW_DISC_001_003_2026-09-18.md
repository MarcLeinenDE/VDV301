# Runtime-mapping review — DISC-001 / DISC-002 / DISC-003 — 2026-09-18

Status: **completed / runtime matching not applicable**.

## Result

The three NetworkDiscovery findings remain valid semantic/documentation knowledge, but no finding-specific runtime matcher is justified.

The observable DNS-SD runtime lane is already governed independently by `tools/runtime_discovery_profile.py` and RV-002. A device advertisement cannot reliably reveal which language-version PDF conflict, wrong RFC citation, or historical table omission caused an implementation choice.

### DISC-001

Decision: `candidate -> not_applicable`.

The German/English IP-allocation conflict is source-context knowledge. It prevents the SDK from presenting one language track as a universal VDV ZeroConf/169.254 rule, but it is not an observable DNS-SD advertisement condition.

### DISC-002

Decision: `candidate -> not_applicable`.

The RFC 2927/3927 mismatch is a documentation-reference correction. It has no unique runtime packet signature and does not independently make RFC 3927 a universal VDV allocation requirement.

### DISC-003

Decision: `candidate -> not_applicable`.

The missing German V2.3 table entries are a historical documentation omission. Runtime requirements for the V2.2+ discovery keys remain independently enforced by the discovery profile; `ver`, `deviceclass` and `deviceID` checks are not weakened by the faulty table.

## Mapping inventory after review

```text
reviewed       35
candidate      43
not_designed    1
not_applicable 113
implemented     0
```

## Gate

GitHub Actions run **35345071891**: **SUCCESS**.

A later workflow-only commit changed the temporary gate file but did not change semantic classification, the runtime mapping manifest, or any XSD. The successful run remains the authority for the reviewed DISC data.

The successful gate verified:

- semantic and runtime-mapping registries;
- deterministic mapping regeneration;
- independent RV-002 discovery behavior;
- V2.2+ `ver`, `deviceclass` and `deviceID` rules remain active;
- SDK manifest self-test;
- all 50 root XSDs with no mutation.

No runtime matcher was implemented and no XSD was changed.
