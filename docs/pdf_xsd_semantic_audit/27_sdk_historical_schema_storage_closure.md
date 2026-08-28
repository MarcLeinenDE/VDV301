# SDK historical schema storage closure

Date: 2026-08-28
Status: TrainSet V2.1 storage gap closed.

During construction of the machine-readable SDK resolver inventory, the stored root XSD pool was compared against the semantically distinct historical profiles established by the audit.

A real storage gap was found for the TrainSet V2.1 family: the V2.1 service schemas had already been semantically/provenance audited, but only the V2.2 files were present in the root integration pool.

Because V2.1 and V2.2 have real semantic differences, V2.1 must remain separately routable. Deduplicating it away would violate the SDK rule that semantic constraint differences require distinct validation profiles.

## Official release backfill

Exact source:

```text
VDVde/VDV301 tag VDV-301-2.1
```

Unchanged files/blobs:

```text
IBIS-IP_TrainSetDataService_V2.1.xsd
  c2cdb73fcae265a2e4e0349ac6072e3548e36d8b

IBIS-IP_TrainSetInformationService_V2.1.xsd
  897f373e31b76aa23d8bc206854b042524e4c102

IBIS-IP_TrainSetManagementService_V2.1.xsd
  add9d1cb37e5759ff7a77855b239108d38373206
```

Before insertion, each blob was recreated in the target repository from the official-tag content and the resulting Git blob SHA matched the official source SHA exactly.

No XSD content was edited.

## Resolver consequence

The SDK must expose V2.1 and V2.2 as separate TrainSet service profiles.

```text
TrainSetDataService V2.1
  Common V2.0
  Enumerations V2.0
  CustomerInformationService V2.0

TrainSetInformationService V2.1
  Common V2.0

TrainSetManagementService V2.1
  Common V2.0
  Enumerations V2.0
  TrainSetInformationService V2.1
```

The V2.2 family remains separately routed exactly as established in the audit.

## TVS V2.3 authority clarification

The root file `IBIS-IP_TicketValidationService_V2.3.xsd` entered the integration branch in commit `c9c086ac07f7e9bdb271c54f7a274e3cf0d03749` together with public candidate files.

The audit already established the normative route:

```text
TicketValidationService document V2.3 -> official executable schema semantics V2.2
```

Therefore the local V2.3-named XSD is retained only as integration/comparison material and is not an official resolver target.
