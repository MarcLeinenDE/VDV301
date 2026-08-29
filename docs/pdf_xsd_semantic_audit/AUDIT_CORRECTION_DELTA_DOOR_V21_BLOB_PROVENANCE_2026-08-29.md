# Audit correction delta - DoorState V2.1 dependency blob provenance

Date: 2026-08-29

## Correction

The DoorState V2.1 closure commit `c99c73e58b23218fcf42a383e285fcdc28c93b4b` recorded incorrect Git blob identifiers for the two dependency files:

```text
incorrectly recorded Common V1.0 blob:       267be9bf692da6781a003cee7db92e2072b71182
incorrectly recorded Enumerations V1.0 blob: 399205aac6b912032812661176ebab0a9897d3c3
```

Independent verification performed immediately while starting the following TVS V2.1 audit shows that both the current integration branch and the official upstream `VDVde/VDV301` tag `VDV-301-2.1` resolve to:

```text
IBIS-IP_common_V1.0.xsd       194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
IBIS-IP_Enumerations_V1.0.xsd a9bea5bc73003ed91ded8519db06c32c4067831d
```

The DoorStateService file itself remains correctly recorded as:

```text
IBIS-IP_DoorStateService_V2.1.xsd abff0f3960e2ec7a9caaa9ddeb6efff8f4183805
```

## Scope and impact

This is a provenance-metadata correction only.

```text
No XSD bytes were changed.
No validation result changes.
EV-111 remains valid because it executed the actual branch files checked out at head 356d1b792730b66a4f5ec3b99b82e6d66185315c.
The selected DoorState route remains DoorState V2.1 -> Common V1.0 -> Enumerations V1.0.
```

The affected DoorState report, EV-111 record, addendum, registry delta, handoff and current-state metadata are corrected in the same permanent commit as this delta.
