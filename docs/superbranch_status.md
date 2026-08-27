# Schema integration superbranch status

Status: working branch for the VDV301 Tool, not an upstream pull-request branch.

Branch:

```text
dev/schema-integration
```

Purpose:

- collect the practically usable VDV301 XSD state from official releases, current upstream and traceable open candidates;
- provide a stable working source for the VDV301 Tool/SDK;
- keep audit provenance and validation helpers with the integration state;
- avoid redundant historical schema copies where they do not change executable payload semantics.

Do not open this branch as a pull request against `VDVde/VDV301` as a whole.

## Historical V1.0 integration model

The superbranch is now deduplicated rather than carrying a complete second copy of the `VDV-301-1.0` tag.

Rules:

```text
byte-identical historical XSDs -> one copy
packaging-only same-version official revisions -> later self-contained official copy after diff review
genuine semantic differences -> keep separately routable
legacy aggregate-only operation roots -> provenance-backed schema profile metadata
```

Current V1.0 additions/selections include:

```text
CustomerInformationService V1.0      official tag1.0 type-XSD
DeviceManagementService V1.0         official tag1.0 type-XSD
SystemDocumentationService V1.0      official tag1.0 type-XSD
JourneyInformationService V1.0       self-contained official tag2.0 V1.0 revision
PassengerCountingService V1.0        self-contained official tag2.0 V1.0 revision
SystemManagementService V1.0         self-contained official tag2.0 V1.0 revision
TicketInformationService V1.0        self-contained official tag2.0 V1.0 revision
GNSS/Distance/Beacon V1.0             standalone official files
```

The old combined `IBIS-IP_LocationService_V1.0.xsd` and the complete `IBIS_IP_V1.0.xsd` release mirror are not active superbranch runtime files.

Legacy root mappings for CIS/DMS/SystemDocumentation are in:

```text
schema_profiles/VDV-301-1.0-root-map.csv
```

## Included newer candidate areas

```text
IBIS-IP_common_V2.4.xsd
IBIS-IP_Enumerations_V2.4.xsd
IBIS-IP_TicketValidationService_V2.4.xsd
IBIS-IP_DeviceManagementService_V2.4.xsd
IBIS-IP_DeviceManagementService_V2.3.xsd
IBIS-IP_TicketValidationService_V2.3.xsd
IBIS-IP_CustomerInformationService_V2.4.xsd
IBIS-IP_AnalogRadioService_V2.4.xsd
IBIS-IP_VideoRecordingService_V2.4.xsd
```

Candidate/integration material remains explicitly non-release authority.

## Validation helpers

```text
tools/validate_xsd_pool.py
tools/validate_legacy_v1_roots.py
```

The legacy-root validator builds temporary adapter schemas from official root mappings; those adapters are not official VDV XSDs.

## Current caution

This branch is an integration working set, not a historical tag archive and not an official VDV release. Tool output must preserve official/candidate provenance and the exact selected service/dependency profile.
