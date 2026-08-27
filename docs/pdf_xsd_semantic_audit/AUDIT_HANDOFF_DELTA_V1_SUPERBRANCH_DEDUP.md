# Audit handoff delta - V1.0 superbranch dedup refinement

Status: operational storage model refined after explicit user review of tag1.0/tag2.0 differences.

Parent branch head before this change:

```text
b4b2145057f6842ced76b996f25cb320141c0f8a
```

Key decision:

```text
The superbranch should contain the complete practically needed schema set, not duplicate entire historical release snapshots.
Byte-identical XSDs are stored once.
Packaging-only same-version official revisions may use the later self-contained official blob after semantic diff review.
```

Changes:

```text
removed schema_pools/official/VDV-301-1.0/ complete 12-XSD mirror
added root IBIS-IP_DeviceManagementService_V1.0.xsd exact official blob 602a963...
added root IBIS-IP_SystemDocumentationService_v1.0.xsd exact official blob 8995c4a...
added root IBIS-IP_SystemManagementService_V1.0.xsd self-contained official tag2.0 blob 2d32630...
changed root IBIS-IP_PassengerCountingService_V1.0.xsd from original tag1.0 type-only blob 600a3ee... to self-contained official tag2.0 V1.0 blob 4161872...
kept JIS/TicketInformation existing later self-contained official V1.0 revisions
kept standalone GNSS/Distance/Beacon V1.0 files; old combined LocationService_V1.0 not added
```

Legacy root handling:

```text
CIS V1.0, DMS V1.0 and SystemDocumentation V1.0 remain official type-only XSDs.
Their exact operation root name/type pairs from official IBIS_IP_V1.0.xsd are stored in schema_profiles/VDV-301-1.0-root-map.csv.
tools/validate_legacy_v1_roots.py builds temporary compile harnesses from that mapping.
Generated harnesses are adapters, not official VDV XSDs.
```

Historical aggregate provenance remains:

```text
VDV-301-1.0 IBIS_IP_V1.0.xsd blob 41289eaed2674a169fdf77a10a2eff293c76d5c4
```

No upstream PR/comment/merge action. No XSD contents edited.

Technical compile/sample validation is still pending until a real executable run succeeds.
