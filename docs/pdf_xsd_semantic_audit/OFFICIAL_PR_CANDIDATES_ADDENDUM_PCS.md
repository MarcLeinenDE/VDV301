# Official PR candidates addendum - PassengerCountingService

Status: tracking only; no PR is opened during the audit.

## PR-CAND-007 - PCS V2.1 OperationNotSupported dependency/value-set conflict

Linked finding:

```text
PCS-001
```

Observation:

```text
VDV 301-2-8 V2.1 documents OperationNotSupported for newly added optional operations.
The official PCS V2.1 service XSD explicitly selects Common V1.0 + Enums V1.0.
Enums V1.0 does not contain OperationNotSupported.
Enums V2.1 contains the value but is not selected.
```

Initial assessment:

```text
Strong schema-family/dependency clarification candidate, but not a ready one-line patch.
```

Why no immediate patch:

```text
Changing only the explicit PCS enum include to V2.1 may conflict with Common V1.0, which itself includes Enums V1.0.
Changing PCS to Common V2.1 would alter a broader dependency family and may affect unrelated structures.
The correct upstream remedy could involve service dependency alignment, release-family packaging, or documentation clarification.
```

Required before any official-facing decision:

```text
- compile the exact official PCS V2.1 + Common V1.0 + Enums V1.0 pool,
- demonstrate the OperationNotSupported failure with a targeted sample,
- run a controlled alternative-pool experiment without treating it as authority,
- inspect release history / PR #10 context for intended dependency migration,
- assess compatibility/code-generation impact,
- prepare only a minimal candidate after full audit,
- ask the user explicitly before preparing or opening an official PR.
```
