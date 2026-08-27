# Audit handoff delta - Base / General block 21

Status: Base/general historical schema-family first pass completed.

Branch before block:

```text
f0296f4a048caafa79de09a74ca08a1969843869
```

Key result:

```text
The original VDV-301-1.0 aggregate family is now preserved as an immutable, release-isolated pool at:
schema_pools/official/VDV-301-1.0/
```

Root:

```text
IBIS_IP_V1.0.xsd
blob 41289eaed2674a169fdf77a10a2eff293c76d5c4
```

All twelve XSD blobs are copied unchanged from official tag `VDV-301-1.0`.

Important new resolver rule:

```text
Four V1.0 filenames have different official blobs in VDV-301-1.0 vs VDV-301-2.0:
JourneyInformationService
PassengerCountingService
SystemManagementService
TicketInformationService
```

Therefore strict historical routing may require `release_context/schema_revision` in addition to service/version.

The original aggregate must never be combined with later same-name revisions.

No local XSD compilation/sample validation has yet been executed.

Next block:

```text
22_network_infrastructure_discovery_context.md
```
