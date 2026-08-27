# Superbranch V1.0 deduplication policy

Status: active integration-storage rule for `dev/schema-integration`.

Purpose:

```text
Keep the superbranch complete for service/version validation without storing byte-identical or packaging-only historical copies of the same schema semantics multiple times.
```

This policy does not rewrite official VDV history. Official tag/blob provenance remains recorded in the audit documentation.

## 1. Storage rule

```text
Byte-identical XSDs are stored once.
If a later official tag contains the same service version with a self-contained packaging revision and the diff shows no changed payload constraints, the superbranch may select that later official revision as its operational copy.
Original tag/blob provenance remains recorded.
If payload constraints differ, the revisions must remain separately routable and may not be collapsed.
```

The superbranch is an integration working set, not a byte-for-byte mirror of every historical Git tag.

## 2. VDV-301-1.0 vs VDV-301-2.0 result

### Byte-identical across both tags

```text
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
IBIS-IP_NetworkLocationService_V1.0.xsd
```

No duplicate storage is needed.

### Original V1.0 aggregate packaging later split into standalone V1.0 service XSDs

`IBIS-IP_LocationService_V1.0.xsd` from tag VDV-301-1.0 combines GNSS/Distance structures and Beacon structures. By VDV-301-2.0 the same service-version content is represented by standalone files:

```text
IBIS-IP_GNSSLocationService_V1.0.xsd
IBIS-IP_DistanceLocationService_V1.0.xsd
IBIS-IP_BeaconLocationService_V1.0.xsd
```

The superbranch keeps the standalone files and does not also store the old combined `LocationService_V1.0` packaging file.

### Same service version, later official self-contained packaging

For these V1.0 services, the VDV-301-2.0 tag moves operation roots/groups from the old aggregate into the service XSD while retaining the payload structures checked in the diff:

```text
JourneyInformationService V1.0
PassengerCountingService V1.0
SystemManagementService V1.0
```

The superbranch selects the VDV-301-2.0 V1.0 blobs:

```text
JIS  8c303db5a9c0548d66b90174d9c329d33092ad24
PCS  4161872be76740abfdd1cddf96f8a736333fc8be
SMSy 2d32630a0f1981e980e6a466e3f6a69136410f24
```

TicketInformationService V1.0 also uses the later self-contained official revision `3fda66d872ab0d1c511247f13e715cf3ad56afe7`. Its diff additionally removes unused `SetRazziaResponse*` type definitions; no corresponding global `SetRazziaResponse` root existed in the original aggregate.

### Original type-only V1.0 services still needed

These service XSDs have no later self-contained V1.0 official replacement:

```text
CustomerInformationService V1.0  7a95fc03c06c8c84d078bf06d18ef5873a15c215
DeviceManagementService V1.0    602a963f91000d0d39e3c271bacb3c7aba73e6d4
SystemDocumentationService V1.0 8995c4a230bf81d5e47b9313ee7725ff3cd4b7b5
```

They remain exact official type-XSDs from tag VDV-301-1.0.

## 3. What happens to IBIS_IP_V1.0.xsd

The original aggregate root is official historical evidence:

```text
VDV-301-1.0 / IBIS_IP_V1.0.xsd
blob 41289eaed2674a169fdf77a10a2eff293c76d5c4
```

It is **not** stored as an active superbranch runtime XSD because it includes old same-name service revisions and would conflict with the later self-contained V1.0 files in the flat integration set.

For CIS V1.0, DMS V1.0 and SystemDocumentation V1.0, the aggregate's exact global operation-root declarations are preserved as resolver metadata in:

```text
schema_profiles/VDV-301-1.0-root-map.csv
```

A generated validation harness may include the official service XSD and re-declare exactly the official rootname/type pair from that map. Such a harness is an integration adapter, not an official VDV schema.

## 4. Strict historical reconstruction

If a future task explicitly requires byte-for-byte reconstruction of the complete `VDV-301-1.0` release package, use the official tag and the recorded blob inventory. Do not confuse that archival/reproduction task with the operational superbranch layout.

## 5. Validation authority

```text
Field/type/cardinality authority -> selected official service XSD + exact Common/Enums dependencies.
Root element identity for legacy type-only V1.0 services -> official IBIS_IP_V1.0 root map.
Candidate schemas remain candidate-labelled.
No latest-wins substitution across service versions.
```

No XSD content is edited by this policy; it only selects which official revision is stored operationally.
