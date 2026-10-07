# Version-scope boundary review — CE-012 — 2026-10-07

Status: **verified / scope unchanged**.

## Finding
`CE-012` is the `DeviceSpecificationWithStateList` cardinality mismatch:
- the PDF requires `DeviceSpecificationWithState 1:*`;
- the exact selected Common XSD permits `0:*`.

An empty list is therefore XSD-valid in the affected profiles despite the stricter PDF cardinality.

## Lower boundary
The mismatch is already present in Common V1.0, the earliest retained/published Common lineage available to this audit. No earlier Common publication exists from which an unaffected predecessor could be established.

Common V1.0 is therefore the first affected available publication, not an inferred continuation from a later version.

## Continuity
The same PDF `1:*` versus selected-XSD `0:*` boundary is independently located and/or executable-confirmed in Common V2.0, V2.1, V2.2 and V2.3.

The official V2.4 PDF remains `1:*`; the explicitly selected candidate/integration Common V2.4 XSD remains `0:*`.

## Boundary conclusion
Existing scope is confirmed unchanged:
1. Common V1.0-V2.3 — official release/historical selected authority;
2. Common V2.4 — candidate/integration authority.

There is no earlier retained Common publication to use as a predecessor control.

## SDK consequence
An empty `DeviceSpecificationWithStateList` must remain valid whenever accepted by the exact selected XSD. CE-012 may decorate the valid result with an advisory explaining the stricter PDF cardinality; it must not turn the result into a failure.
