# Base / General Conventions historical schema-family closure

Status: historical first pass completed; superbranch storage model refined after tag-to-tag diff review.

## Authority rule

```text
Validation follows the selected executable XSD family.
Historical source provenance uses official VDVde/VDV301 tags.
The superbranch is a deduplicated operational integration set, not a byte-for-byte archive of every release tag.
No latest-wins substitution across service versions.
No XSD content is silently corrected.
```

## 1. What the original VDV-301-1.0 aggregate did

Official tag `VDV-301-1.0` contains:

```text
IBIS_IP_V1.0.xsd
blob 41289eaed2674a169fdf77a10a2eff293c76d5c4
```

The aggregate includes Common/Enums and multiple service XSDs. For several early service files it also supplies the global operation elements and service groups that are not present in the service file itself.

This is a packaging property of the original release.

## 2. Tag 1.0 -> tag 2.0 diff result

The earlier assumption that four same-name V1.0 service files represented four independently different historical payload models was too conservative.

Detailed diff shows:

```text
JourneyInformationService V1.0:
  later official file mainly moves global roots/group from aggregate into service XSD.

PassengerCountingService V1.0:
  later official file moves the four operation roots/group into service XSD; checked payload structures stay the same.

SystemManagementService V1.0:
  later official file moves the two operation roots/group into service XSD; checked payload structures stay the same.

TicketInformationService V1.0:
  later official file becomes self-contained and additionally drops unused SetRazziaResponse* types; original aggregate did not expose a SetRazziaResponse global root.
```

Therefore the operational superbranch does not need duplicate copies of both packaging revisions.

## 3. LocationService V1.0 packaging transition

Original `IBIS-IP_LocationService_V1.0.xsd` contains the GNSS and Distance global roots/types plus Beacon structures.

The official VDV-301-2.0 tag publishes the same service-version areas as standalone XSDs:

```text
IBIS-IP_GNSSLocationService_V1.0.xsd
IBIS-IP_DistanceLocationService_V1.0.xsd
IBIS-IP_BeaconLocationService_V1.0.xsd
```

The superbranch keeps those standalone files and does not keep the old combined LocationService packaging file.

## 4. Deduplicated V1.0 superbranch model

Operational root set:

```text
Common V1.0 and Enums V1.0: single shared copies.
NetworkLocation V1.0: single shared copy.
GNSS/Distance/Beacon V1.0: standalone official files.
JIS/PCS/SystemManagement/TicketInformation V1.0: later official self-contained V1.0 revisions from VDV-301-2.0.
CIS/DMS/SystemDocumentation V1.0: original official type-XSDs from VDV-301-1.0.
```

For the three type-only files, root declarations are carried as resolver metadata sourced exactly from `IBIS_IP_V1.0.xsd`:

```text
schema_profiles/VDV-301-1.0-root-map.csv
```

## 5. Same-path collision interpretation

`BG-001` remains useful as a provenance warning:

```text
same filename/version token does not guarantee byte identity across official release tags.
```

But for the four reviewed V1.0 cases, the diff now distinguishes packaging/self-containment changes from actual payload-constraint changes. They do not require duplicate operational storage merely because the blobs differ.

Strict byte-for-byte release reconstruction remains a separate archival use case and can use the official tag plus recorded blob inventory.

## 6. Aggregate-root interpretation

`BG-002` is refined:

```text
IBIS_IP_V1.0.xsd is authoritative historical packaging evidence and source of legacy root declarations.
It is not an active runtime dependency of the deduplicated superbranch.
```

Reason:

```text
Combining the original aggregate with later self-contained same-name V1.0 service files would create duplicate declarations / mixed packaging.
```

## 7. SDK/tool resolver consequence

Required dimensions remain:

```text
service identity
service/document version
schema authority
exact dependency pool
operation/root mapping
candidate vs official state
```

A separate release_context key is required only where an actual semantic constraint differs or where strict release reproduction is explicitly requested; blob difference alone is not enough.

## 8. Validation status

The source/diff decision is complete. Technical compilation of the deduplicated superbranch and generated legacy root adapters remains pending until an executable validation run succeeds.

See:

```text
docs/pdf_xsd_semantic_audit/24_executable_validation_matrix_start.md
```
