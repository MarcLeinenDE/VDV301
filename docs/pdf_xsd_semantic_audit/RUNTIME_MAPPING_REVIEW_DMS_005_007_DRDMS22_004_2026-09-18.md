# Runtime-mapping review — DMS-005 / DMS-006 / DMS-007 / DRDMS22-004 — 2026-09-18

Status: **completed / reviewed / not implemented**.

## Result

The four remaining DeviceManagementService runtime candidates in this block were reviewed against the official DMS V2.2 profile, the explicit V2.4 candidate/integration boundary where applicable, the DMS revalidation evidence, and EV-127.

### DMS-005

Decision: `candidate -> reviewed`.

Runtime boundary:

- DMS V2.2 official or explicitly selected V2.4 candidate/integration context;
- exact documentation identifier `DeviceManagementService.DeviceStatusInformationResponseData`;
- selected schema exposes the Get-prefixed local response-data element `DeviceManagementService.GetDeviceStatusInformationResponseData`;
- no non-Get alias is created or accepted.

Effect: resolver/profile warning only.

### DMS-006

Decision: `candidate -> reviewed`.

Runtime boundary:

- official DMS V2.2 strict profile only;
- XSD result is **INVALID** because `DeviceStatusImpact` or `DeviceStatusPriority` is missing;
- submitted structure otherwise follows the PDF-visible Name + Flag shape.

Effect: preserve the XSD INVALID result and decorate it with the Known-Issues advisory. V2.4 optionality is not back-applied.

### DMS-007

Decision: `candidate -> reviewed`.

Runtime boundary:

- DMS V2.2 official or explicitly selected V2.4 candidate/integration context;
- exact resolver/configuration operation name `GetUpdateStates`;
- selected operation inventory uses `GetUpdateHistory`.

Effect: warning only; no alias and no automatic rewrite.

### DRDMS22-004

Decision: `candidate -> reviewed`.

Runtime boundary:

- official DMS V2.2 context;
- exact singular documentation-derived operation name `GetDeviceErrorMessage`;
- selected DMS group exposes plural `GetDeviceErrorMessagesRequest/Response`.

Effect: informational correction only; no singular alias.

## Mapping inventory after review

```text
reviewed        39
candidate       39
not_designed     1
not_applicable 113
implemented      0
```

## Gate

Primary DMS review gate **35345700143**: **SUCCESS**.

Closure/consistency gate **35345873753**: **SUCCESS**.

The successful gate verified:

- semantic registry and deterministic runtime-mapping regeneration;
- all four DMS mappings remain `reviewed_not_implemented`;
- exact DMS V2.2 identifier and operation boundaries;
- the response-data identifier at its actual local XSD position inside `GetDeviceStatusInformationResponseStructure`;
- `DeviceStatusImpact` and `DeviceStatusPriority` remain part of the V2.2 `DeviceStatusStructure`;
- EV-127 DMS instance boundaries;
- SDK baseline and all root XSDs without mutation;
- synchronized Known-Issues runtime counters and the strengthened SDK manifest consistency checks.

The first DMS gate attempt, run `35345479470`, failed only because the gate incorrectly assumed the response-data element was global. The corrected test follows the actual XSD structure and passed.

## Consistency hardening

The SDK manifest's redundant `runtime_match_distribution` is now synchronized with the canonical runtime-mapping manifest. The SDK self-test now compares all Known-Issues runtime counts against `known_issues_runtime_mapping_v0.1.json`, so stale duplicated counters fail validation instead of silently drifting.

No executable Known-Issues matcher was added and no XSD was changed.
