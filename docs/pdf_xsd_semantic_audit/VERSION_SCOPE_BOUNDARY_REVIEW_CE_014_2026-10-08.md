# Version-scope boundary review — CE-014 — 2026-10-08

Status: **verified / scope unchanged**.

## Finding
`CE-014` is the `DataVersionList` cardinality mismatch:
- the PDF requires `DataVersion 1:*`;
- the exact selected Common XSD permits `DataVersion 0:*`.

In V1.0 the list structure is anonymous inside `DeviceInformationStructure`; from V2.0 onward it is represented by `DataVersionListStructure`. That structural refactoring does not change the cardinality mismatch.

## Lower boundary
The mismatch is already present in Common V1.0, the earliest retained Common publication available to this audit:
- PDF: at least one `DataVersion`;
- exact V1.0 XSD: zero or more `DataVersion` entries.

No earlier retained Common publication exists from which an unaffected predecessor could be established.

## Continuity
The same PDF `1:*` versus selected-XSD `0:*` boundary persists independently through Common V2.0, V2.1, V2.2 and V2.3.

The official V2.4 PDF still requires `1:*`; the explicitly selected candidate/integration Common V2.4 XSD still permits `0:*`.

## Boundary conclusion
Existing scope is confirmed unchanged:
1. Common V1.0-V2.3 — official release/historical selected authority;
2. Common V2.4 — candidate/integration authority.

There is no earlier retained Common publication to use as a predecessor control.

## SDK consequence
An empty `DataVersionList` must remain valid whenever accepted by the exact selected XSD. CE-014 may decorate that valid result with an advisory explaining the stricter PDF cardinality; it must not convert the normative result into a failure.
