# Official release backfill same-path collision policy addendum

Status: active supplement to `OFFICIAL_RELEASE_BACKFILL_POLICY.md`; refined for deduplicated superbranch storage.

## Two distinct goals

Do not conflate:

```text
A. exact historical release reconstruction
B. operational superbranch schema storage
```

For A, every official tag/blob mapping remains authoritative and may be reconstructed exactly from the official tag.

For B, the integration branch may avoid duplicate storage when a detailed diff proves that a later official same-version file only changes packaging/self-containment and does not change the relevant payload constraints.

## Same-path rule

If two official release tags contain the same path/version token but different blobs:

```text
1. Record both tag -> blob mappings.
2. Diff the files semantically, not only by SHA.
3. Classify changes as payload constraint, operation/root packaging, comments/formatting, or dead/unexposed schema material.
4. Never collapse revisions if field types, cardinalities, value sets, ordering, compositors, or reachable operation payload semantics differ.
5. If the change is packaging/self-containment only, the superbranch may store the later official self-contained revision once.
6. Preserve the original historical source relationship in audit metadata.
7. Strict tag reproduction must use the official tag/blob inventory rather than assuming the superbranch is a release snapshot.
```

## Reviewed V1.0 collisions

Between `VDV-301-1.0` and `VDV-301-2.0`:

```text
JIS V1.0
  1ee4d7a... -> 8c303db...
  classification: aggregate-to-service self-containment packaging

PCS V1.0
  600a3ee... -> 4161872...
  classification: aggregate-to-service self-containment packaging

SystemManagement V1.0
  85390f9... -> 2d32630...
  classification: aggregate-to-service self-containment packaging

TicketInformation V1.0
  017ca64... -> 3fda66d...
  classification: self-containment packaging + removal of unused SetRazziaResponse* types
```

These reviewed cases do not require duplicate operational storage in the superbranch.

## Legacy aggregate

`IBIS_IP_V1.0.xsd` remains official historical evidence but is not stored as an active superbranch XSD. Exact legacy rootname/type mappings needed by type-only V1.0 service files are recorded in `schema_profiles/VDV-301-1.0-root-map.csv` with source tag/blob provenance.

This addendum does not authorize modifying any official XSD contents.
