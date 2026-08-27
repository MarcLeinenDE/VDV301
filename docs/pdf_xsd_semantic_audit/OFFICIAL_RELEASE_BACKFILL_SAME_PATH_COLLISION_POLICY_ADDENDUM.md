# Official release backfill same-path collision policy addendum

Status: active supplement to `OFFICIAL_RELEASE_BACKFILL_POLICY.md`.

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
2. Keep the currently integrated blob's provenance explicit.
3. Do not overwrite an existing different official blob merely to backfill an older tag.
4. Record the collision as a schema-family/provenance routing fact.
5. Model strict future validation with an additional release_context/schema_revision key when service+version is insufficient.
6. Preserve original aggregate/root packaging facts where the release family differs.
7. A later SDK/package layout may need per-release directories or immutable pool IDs to make both official revisions executable side by side.
```

## First confirmed case

```text
IBIS-IP_TicketInformationService_V1.0.xsd
VDV-301-1.0 -> blob 017ca64666e25d757fc0cde1f1be817f06a743fc
VDV-301-2.0+ -> blob 3fda66d872ab0d1c511247f13e715cf3ad56afe7
```

The original release uses `IBIS_IP_V1.0.xsd` as the TicketingService operation-root layer; the later revision moves those roots/group into the service file.

This addendum does not authorize any schema modification.
