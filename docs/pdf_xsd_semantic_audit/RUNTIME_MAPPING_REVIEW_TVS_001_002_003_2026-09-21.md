# Runtime-mapping review — TicketValidationService TVS-001 / TVS-002 / TVS-003 — 2026-09-21

Status: **completed / terminal / not implemented**.

## Authority boundary

Official runtime conformance in this block is limited to the established release routes:

- TVS V2.1: `IBIS-IP_TicketValidationService_V2.1.xsd @ f6497e6469b82ee19b185c4de749d13a7ca60bed`;
- TVS V2.2: `IBIS-IP_TicketValidationService_V2.2.xsd @ 5a4be2b2ba66860f035777ec0458dba0790880e1`;
- TVS V2.3: official release route continues to use the unchanged V2.2-named XSD above;
- TVS V2.4: only candidate/integration evidence exists. It is **not official-release V2.4 XSD authority**.

## TVS-001 — GetCurrentShortHaulStopsResponse omitted from V2.4 candidate operation group

The structural observation remains **likely XSD defect / high confidence** and remains a remediation candidate.

The candidate/integration XSD defines the global response and related structures but omits the response from `TicketValidationServiceOperations`. EV-115 and upstream-master inspection confirm this boundary.

Decision: `candidate -> not_applicable` for Known-Issues runtime matching.

Reason: there is no official V2.4 release XSD profile against which this candidate-only structural inconsistency could safely drive manufacturer conformance. A strict official V2.4 request must fail closed because of the authority gap; TVS-001 remains available for candidate analysis and later upstream remediation.

## TVS-002 — RouteDeviation PDF references RouteDirectionEnumeration

Assessment remains **confirmed PDF defect**.

The selected official XSD routes type `VehicleData.RouteDeviation` as `RouteDeviationEnumeration`. In V2.2/V2.3 both enums exist and are semantically distinct:

```text
RouteDeviationEnumeration: onroute / offroute / unknown
RouteDirectionEnumeration: Forward / Backward / Clockwise / Counterclockwise / Other
```

EV-112/113/114 prove the official executable boundary.

Decision: `candidate -> reviewed`.

The advisory requires an actual XSD INVALID at RouteDeviation and must not convert arbitrary invalid values into this finding. For V2.1, where the wrong RouteDirection type is absent from the selected enum pool, the later directional value set must not be back-applied merely to create a match.

## TVS-003 — stale CurrentStopPoint names after CurrentTariffStop rename

Assessment remains **confirmed PDF defect**.

Official V2.2/V2.3 history and XSD authority use the renamed CurrentTariffStop family. Stale PDF names such as `TicketValidationService.GetCurrentStopPointResponse` remain in documentation locations. EV-113/114 confirm that the current names validate and stale names do not.

Decision: `candidate -> reviewed`.

The advisory is restricted to exact stale CurrentStopPoint identifiers in their renamed CurrentTariffStop contexts. No generic name-normalisation is permitted.

## Expected inventory after persistence

```text
reviewed        72
candidate        5
not_designed     0
not_applicable 115
implemented      0
```

No executable matcher, compatibility alias, enum substitution or XSD mutation is introduced.

## Primary gate

Primary runtime-mapping gate **35646946304**: **SUCCESS**.

The gate re-ran EV-112, EV-113, EV-114 and EV-115, preserved the official-release/candidate authority split, verified the TVS-001 structural boundary without promoting it to official V2.4 conformance, and passed the semantic-registry, deterministic runtime-mapping, SDK-manifest and root-XSD regression checks.

## Closure gate

Closure/consistency gate **35647099114**: **SUCCESS** on persisted HEAD `3e529c761c252a60e4a3267cafe8b460582e660a`.

Final runtime-mapping inventory after this block:

```text
reviewed        72
candidate        5
not_designed     0
not_applicable 115
implemented      0
```

TVS-001 remains a candidate/integration remediation finding with no Known-Issues runtime matcher. TVS-002 and TVS-003 are reviewed official-route XSD-invalid advisories. No alias, enum substitution, candidate-to-official promotion or XSD mutation was introduced.
