# Base / General Conventions historical schema-family closure

Status: historical first pass completed.

Scope:

```text
VDV 301-2 general/base release packaging
Official VDVde/VDV301 tags VDV-301-1.0 and VDV-301-2.0 as the decisive aggregate-family transition
Original aggregate root IBIS_IP_V1.0.xsd
Exact historical release-pool routing for the future SDK/tool
```

Authority rules:

```text
Validation follows the selected executable XSD family.
Historical backfill uses official VDVde/VDV301 release tags only.
No latest-wins substitution.
No XSD is modified in this audit block.
A same-version filename is not sufficient identity when different official release tags contain different blobs.
```

## 1. Original VDV-301-1.0 aggregate family

The official tag `VDV-301-1.0` contains `IBIS_IP_V1.0.xsd`, blob:

```text
41289eaed2674a169fdf77a10a2eff293c76d5c4
```

The aggregate directly includes these eleven files:

```text
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
IBIS-IP_CustomerInformationService_V1.0.xsd
IBIS-IP_JourneyInformationService_V1.0.xsd
IBIS-IP_DeviceManagementService_V1.0.xsd
IBIS-IP_LocationService_V1.0.xsd
IBIS-IP_NetworkLocationService_V1.0.xsd
IBIS-IP_SystemManagementService_V1.0.xsd
IBIS-IP_SystemDocumentationService_v1.0.xsd
IBIS-IP_TicketInformationService_V1.0.xsd
IBIS-IP_PassengerCountingService_V1.0.xsd
```

The aggregate itself supplies global operation roots/groups for multiple services. Therefore the original V1.0 family is not faithfully represented by selecting a service XSD in isolation where the service file only supplies structures.

## 2. Exact official V1.0 pool preserved side by side

To preserve relative includes and exact official blob identity, the complete twelve-XSD family from tag `VDV-301-1.0` is stored unchanged under:

```text
schema_pools/official/VDV-301-1.0/
```

This directory is a release-context pool, not a corrected schema family. Original filenames are preserved inside the directory.

No root-level XSD was replaced to create this pool.

## 3. Same-path official revision collisions

Comparison of official `VDV-301-1.0` and `VDV-301-2.0` release trees shows four files whose filename/version token stays V1.0 while the official blob changes:

```text
IBIS-IP_JourneyInformationService_V1.0.xsd
  VDV-301-1.0 -> 1ee4d7aeb15f3269c5335313be9e214bdb519d2e
  VDV-301-2.0 -> 8c303db5a9c0548d66b90174d9c329d33092ad24

IBIS-IP_PassengerCountingService_V1.0.xsd
  VDV-301-1.0 -> 600a3ee6290c630a4435fb06ca9803dabaceb788
  VDV-301-2.0 -> 4161872be76740abfdd1cddf96f8a736333fc8be

IBIS-IP_SystemManagementService_V1.0.xsd
  VDV-301-1.0 -> 85390f99d6c19c88923ed9a5fc8a5706137708af
  VDV-301-2.0 -> 2d32630a0f1981e980e6a466e3f6a69136410f24

IBIS-IP_TicketInformationService_V1.0.xsd
  VDV-301-1.0 -> 017ca64666e25d757fc0cde1f1be817f06a743fc
  VDV-301-2.0 -> 3fda66d872ab0d1c511247f13e715cf3ad56afe7
```

Consequence:

```text
(service, advertised_version) is not always sufficient to select an exact historical schema.
release_context/schema_revision must be available to the resolver where official same-path collisions exist.
```

## 4. Aggregate packaging transition at V2.0

The official VDV-301-2.0 release tree no longer contains `IBIS_IP_V1.0.xsd` and does not introduce a corresponding `IBIS_IP_V2.0.xsd` aggregate root. At the same time several service files are renamed/versioned or expanded.

Interpretation:

```text
The original V1.0 aggregate-root packaging is a release-family property, not a universal VDV301 validation pattern.
Do not force later service families through IBIS_IP_V1.0.xsd.
Do not reconstruct a synthetic V2.0 aggregate.
```

## 5. Findings

### BG-001 - official same-path V1.0 blob collisions across release contexts

Classification:

```text
mismatch_kind: schema_family_or_provenance
likely_source_issue: schema_family_or_provenance_gap
validation_behavior: exact release-context pool required where strict historical identity matters
final_handling_bucket: official_schema_family_clarification_candidate / local_validation_required
```

This is not an assertion that either official revision is wrong. Both are official in their own release contexts.

### BG-002 - V1.0 aggregate root is release-specific packaging

Classification:

```text
mismatch_kind: ok_note
likely_source_issue: ok_with_note
validation_behavior: use IBIS_IP_V1.0.xsd only with its exact VDV-301-1.0 pool
final_handling_bucket: no_action_note
```

## 6. SDK/tool resolver consequences

Required resolver dimensions now include:

```text
service identity
service/document version
release_context or immutable pool_id where needed
schema authority: official_release | candidate_integration | non_xsd_protocol_profile
root model: service_xsd | aggregate_xsd | protocol_profile
exact dependency pool
```

For the original release:

```text
pool_id: official:VDV-301-1.0
pool_dir: schema_pools/official/VDV-301-1.0/
aggregate_root: IBIS_IP_V1.0.xsd
```

The SDK must never combine the original aggregate root with later same-name V1.0 service revisions from another official release context.

## 7. Validation status

Not yet executed in this block:

```text
local XSD compilation of schema_pools/official/VDV-301-1.0/IBIS_IP_V1.0.xsd
positive/negative XML sample validation through the aggregate root
comparison compile using intentionally mixed same-name revisions
```

Therefore this block does not claim technical validation.

## 8. Closure

```text
Base/general historical schema-family first pass completed.
Original VDV-301-1.0 release pool preserved byte-identically and isolated.
Aggregate-root transition documented.
Same-path collision rule generalized beyond Ticketing.
No schema correction performed.
```

Next block:

```text
22_network_infrastructure_discovery_context.md
```
