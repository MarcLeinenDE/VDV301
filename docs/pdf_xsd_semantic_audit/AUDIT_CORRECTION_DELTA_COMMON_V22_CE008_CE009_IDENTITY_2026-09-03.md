# Audit correction delta — COMMON V2.2 CE-008 / CE-009 identity mapping

Date: 2026-09-03
Status: correction overlay; historical delta is preserved unchanged.

## Problem

`audit_registry/deep_read_findings_delta_common_v22_2026-09-02.json` correctly maps the combined source observation `FR-COM22-013` to both `CE-008` and `CE-009`, but its `revalidated_or_scope_extended_findings` descriptions swap the two historical finding identities.

The original finding identities, independently preserved by the V2.4 enumeration audit and the later V2.3/V2.4 Deep Read mappings, are:

```text
CE-008 = Funicular/Taxi NeTEx submode case-sensitive lexeme mismatches
         (Unknown/Undefined/minicab vs unknown/undefined/miniCab)

CE-009 = RailSubmode specialRail (PDF) vs specialTrain (XSD)
```

The V2.2 delta text instead labels `CE-008` as the RailSubmode item and `CE-009` as the Funicular/Taxi case item. That description-level swap is rejected.

## Decision

- Keep the frozen/historical V2.2 delta byte history unchanged.
- Preserve its observation-to-finding membership because both IDs belong to `FR-COM22-013`.
- For all current and future registries, use the original identities above.
- EV-120 remains technically valid; the executable assertions are not invalidated by the label swap.
- V2.3 EV-121 and V2.4 EV-122 use the corrected identities.
- No XSD is changed.

This overlay is part of the CE legacy-finding revalidation closure and prevents the swapped V2.2 labels from propagating into the SDK knowledge baseline.
