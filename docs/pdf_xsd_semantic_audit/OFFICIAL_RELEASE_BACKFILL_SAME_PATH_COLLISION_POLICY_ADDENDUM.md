# Official release backfill same-path collision policy addendum

Status: active supplement to `OFFICIAL_RELEASE_BACKFILL_POLICY.md`; release-pool isolation now implemented for the original VDV-301-1.0 family.

Purpose: handle cases where multiple official VDVde/VDV301 release tags contain the same repository path/versioned filename with different Git blobs.

## Rule

If two official release tags contain:

```text
same repository path
same filename/version token
but different blob SHA/content
```

then the integration branch must not silently overwrite one official revision with the other and must not treat the newest blob as universal authority for the older release context.

Required handling:

```text
1. Record every observed official tag -> blob mapping.
2. Keep the currently integrated root blob's provenance explicit.
3. Do not overwrite an existing different official blob merely to backfill an older tag.
4. Record the collision as a schema-family/provenance routing fact.
5. Model strict future validation with an additional release_context/schema_revision key when service+version is insufficient.
6. Preserve original aggregate/root packaging facts where the release family differs.
7. When relative includes or same-path collisions make a flat layout ambiguous, preserve the complete official release family in an isolated immutable pool directory.
8. Files inside an isolated official pool keep their original filenames and content unchanged.
```

## Implemented pool layout

```text
schema_pools/official/<official-tag>/
```

First implemented complete pool:

```text
schema_pools/official/VDV-301-1.0/
root: IBIS_IP_V1.0.xsd
pool_id: official:VDV-301-1.0
```

## Confirmed same-path collisions

Between official tags `VDV-301-1.0` and `VDV-301-2.0`:

```text
IBIS-IP_JourneyInformationService_V1.0.xsd
  1ee4d7aeb15f3269c5335313be9e214bdb519d2e
  8c303db5a9c0548d66b90174d9c329d33092ad24

IBIS-IP_PassengerCountingService_V1.0.xsd
  600a3ee6290c630a4435fb06ca9803dabaceb788
  4161872be76740abfdd1cddf96f8a736333fc8be

IBIS-IP_SystemManagementService_V1.0.xsd
  85390f99d6c19c88923ed9a5fc8a5706137708af
  2d32630a0f1981e980e6a466e3f6a69136410f24

IBIS-IP_TicketInformationService_V1.0.xsd
  017ca64666e25d757fc0cde1f1be817f06a743fc
  3fda66d872ab0d1c511247f13e715cf3ad56afe7
```

These are official revisions in different release contexts; this policy does not label either revision incorrect.

This addendum does not authorize any schema modification.
