# DeviceManagementService historical findings and V2.0-V2.4 first-pass closure

Status: DMS historical semantic/provenance first-pass chain complete. Local technical validation remains pending.

## Routing matrix

| Service version | Schema authority | Exact pool | Status |
|---|---|---|---|
| V2.0 | official release tag | Common V2.0 + Enums V2.0 | backfilled unchanged |
| V2.1 | official release tag | Common V2.1 + Enums V2.1 | backfilled unchanged |
| V2.2 | official release | Common V2.2 + Enums V2.2 | existing official baseline |
| V2.3 | integration comparison material | Common V2.3 + Enums V2.2 | non-official comparison only |
| V2.4 | candidate/integration | Common V2.4 + Enums V2.4 | candidate profile only |

## Findings

```text
DMS-001  service_modelling_or_generic_response_candidate
         V2.0 PDF operation inventory exceeds service-XSD group/global modelling;
         ActivateDevice/DeactivateDevice have no elements in V2.0 service XSD.

DMS-002  pdf_table_or_documentation_error_candidate
         V2.0 contains repeated unresolved Word cross-reference text; absent from checked V2.1 PDF.

DMS-003  ok_with_note
         ErrorMessage 10:* is PDF/XSD-aligned in V2.0/V2.1 (and historical V2.2 XSD);
         later 0:* correction must not be applied backwards.

DMS-004  ok_with_note
         V2.1 InstallUpdate UpdateID/UpdateTimestamp/UpdateURL are PDF/XSD-required;
         later V2.4 optionality must not be applied backwards.
```

## Relation to existing 02/02a

This block does not replace or rewrite the V2.2/V2.3/V2.4 audit.

It adds the missing earlier half and clarifies the historical semantics needed by a mixed-version SDK.

## SDK consequences

```text
- Resolver key must select DMS version and exact dependency pool.
- V2.0/2.1 official backfills are valid historical validation sources.
- V2.3 remains integration comparison material only.
- V2.4 remains candidate/integration until an official release exists.
- Later corrections are explanatory context, never automatic aliases or relaxations for older schemas.
- DMS-001 requires an operation-role model that can distinguish service-specific payload roots from generic Common subscription/DataAccepted structures.
```

## Safety

```text
No XSD content changed.
No master change.
No PR/comment/merge action.
No local compile/sample validation claimed.
```

## Next audit block

```text
21_base_general_conventions_historical_family_closure.md
```
