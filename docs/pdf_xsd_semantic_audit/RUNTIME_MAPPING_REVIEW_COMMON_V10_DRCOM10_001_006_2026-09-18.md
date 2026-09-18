# Runtime-mapping review — COMMON V1.0 DRCOM10-001 / DRCOM10-006 — 2026-09-18

Status: **completed / reviewed / not implemented**.

## Result

The two remaining Common V1.0 candidates were reviewed separately from the structural/cardinality block because they represent different runtime mechanisms: document-revision/schema drift and exact enumeration lexical mismatch.

### DRCOM10-001 — document revision 1.1 vs official V1.0 XSD family

Decision: `candidate -> reviewed`.

Runtime boundary:

- selected strict profile is the official Common / Enumerations V1.0 XSD family;
- an advisory requires an actual **XSD INVALID** result;
- the invalid instance contains exact PDF revision-1.1-only identifier `ScheduledDepartureTime` or `RouteDirection`;
- the selected V1.0 XSD contains neither identifier in the corresponding structures;
- no official Common V1.1 XSD profile exists.

Effect: preserve the V1.0 XSD INVALID result and explain the official-document/schema drift. The runtime layer must not infer, synthesize or route to a V1.1 schema profile and must not broadly decorate arbitrary unknown elements.

### DRCOM10-006 — DoorCountingObjectClassEnumeration lexical mismatch

Decision: `candidate -> reviewed`.

Runtime boundary:

- selected strict profile is official Common / Enumerations V1.0;
- an advisory requires an actual **XSD INVALID** result;
- exact PDF lexeme `Wheelchair` appears where the selected V1.0 XSD declares `WheelChair`, or exact PDF lexeme `Others` appears where the selected XSD declares `Other`.

Effect: preserve XSD INVALID. No compatibility aliases or silent enum normalization are allowed.

Later V2.4 evidence may explain likely source attribution, but it does not change historical V1.0 validity.

## Mapping inventory after review

```text
reviewed        48
candidate       30
not_designed     1
not_applicable 113
implemented      0
```

## Gate

Primary Common V1.0 remainder gate **35348461470**: **SUCCESS**.

Closure/consistency gate **35348611447**: **SUCCESS**.

The gate verified:

- semantic registry and deterministic 48-entry runtime-mapping regeneration;
- preserved EV-117 exact-authority evidence;
- no `ScheduledDepartureTime` in V1.0 `ConnectionStructure`;
- no `RouteDirection` in V1.0 `TripInformationStructure` and no `RouteDirectionEnumeration`;
- authoritative V1.0 enum lexemes `WheelChair` and `Other`;
- absence of PDF-side `Wheelchair` and `Others` from the selected XSD;
- no synthetic V1.1 profile or enum alias policy;
- all root XSDs unchanged;
- synchronized SDK/runtime-mapping counters pass the hardened consistency validator.

No executable Known-Issues matcher was added and no XSD was changed.
