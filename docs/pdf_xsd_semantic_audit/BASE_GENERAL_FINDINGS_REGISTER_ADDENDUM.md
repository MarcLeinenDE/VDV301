# Base / General findings register addendum

## BG-001 - official same-path V1.0 schema revisions across release contexts

State: confirmed schema-family/provenance routing fact.

Classification: `schema_family_or_provenance_gap`.

Affected files confirmed between official tags `VDV-301-1.0` and `VDV-301-2.0`:

```text
JourneyInformationService_V1.0: 1ee4d7ae... -> 8c303db5...
PassengerCountingService_V1.0: 600a3ee6... -> 4161872b...
SystemManagementService_V1.0: 85390f99... -> 2d32630a...
TicketInformationService_V1.0: 017ca646... -> 3fda66d8...
```

Impact:

```text
A resolver keyed only by service/version can select the wrong official schema revision.
Do not use latest-wins behaviour.
Use release_context/schema_revision or immutable pool_id for exact historical routing.
```

Validation remains against the selected official blob/pool.

## BG-002 - original V1.0 aggregate root is release-specific

State: resolved as `ok_with_note`.

Observation:

```text
Official VDV-301-1.0 contains IBIS_IP_V1.0.xsd and eleven direct includes.
Official VDV-301-2.0 removes that aggregate and has no corresponding IBIS_IP_V2.0.xsd aggregate.
```

Impact:

```text
Use the aggregate root only for the exact original VDV-301-1.0 pool.
Do not invent later aggregate schemas.
```

No correction candidate.
