# PDF/XSD audit scope matrix

Status: active control matrix; refreshed after HTMLDisplayService historical first-pass closure.

Purpose:

```text
Prevent gaps in the full VDV301 PDF-vs-XSD audit by tracking every public VDV301 service/scope and every relevant published PDF version against the XSD/routing material established for dev/schema-integration.
```

Source basis:

```text
Official VDV IP-KOM-ÖV publication index,
official VDVde/VDV301 release tags,
current MarcLeinenDE/VDV301 dev/schema-integration branch,
and completed audit blocks / handoff deltas.
```

## Authority and source rules

```text
Validation follows the selected XSD family where a dedicated executable XSD exists.
PDF differences are retained as provider-facing/documentation evidence.
No latest-version substitution is allowed.
A public service document without a dedicated XSD is not automatically a schema gap.
Historical XSD backfill may use official VDVde/VDV301 release tags only.
Candidate/PR material must remain provenance-separated from official historical material.
```

See:

```text
docs/pdf_xsd_semantic_audit/MIXED_VERSION_VALIDATION_PREMISE.md
docs/pdf_xsd_semantic_audit/VALIDATION_AUTHORITY.md
docs/pdf_xsd_semantic_audit/OFFICIAL_RELEASE_BACKFILL_POLICY.md
docs/pdf_xsd_semantic_audit/FINDING_CLASSIFICATION_POLICY.md
```

Generated CSV:

```text
docs/pdf_xsd_semantic_audit/generated/audit_scope_matrix.csv
```

## Matrix overview

| Area | VDV part | Published PDF versions | Relevant XSD/routing state | Audit status | Notes |
|---|---|---|---|---|---|
| Base / General Conventions | 301-2 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | no single service XSD | pending dedicated historical block | Cross-service HTTP/DNS-SD rules may be used only when explicitly sourced. |
| Common Data Structures and Enumerations | 301-2-1 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | Common V1.0..V2.4; Enumerations V1.0,V2.0,V2.1,V2.2,V2.4 | first pass completed | Historical chain 04a-04e closed; local compile/sample backlog remains. |
| DeviceManagementService | 301-2-0 | 2.0, 2.1, 2.2, 2.4 | DMS V2.2 official; V2.3 integration comparison; V2.4 candidate/integration | partial / V2.2-V2.4 first pass completed | Older V2.0/V2.1 historical coverage remains separate. |
| BeaconLocationService | 301-2-2 | 1.0 | BeaconLocationService V1.0 | first pass completed | Service-local PDF/XSD pass completed. |
| CustomerInformationService | 301-2-3 | 1.1, 2.0, 2.2, 2.3 | historical official backfills V1.0,V2.0,V2.2; official V2.3; V2.4 candidate/integration | first pass completed for public versions | CIS-001..CIS-005 retained; V1.1 exact-XSD mapping remains routing/provenance note. |
| DistanceLocationService | 301-2-4 | 1.0 | DistanceLocationService V1.0 | first pass completed | Location-service findings/notes retained. |
| GNSSLocationService | 301-2-5 | 1.0 | GNSSLocationService V1.0 | first pass completed | Location-service findings/notes retained. |
| JourneyInformationService | 301-2-6 | 1.0 | JourneyInformationService V1.0 | first pass completed | JIS findings retained; local validation pending. |
| NetworkLocationService | 301-2-7 | 1.0 | NetworkLocationService V1.0 | first pass completed | Location-service findings/notes retained. |
| PassengerCountingService | 301-2-8 | 1.0, 2.1 | PassengerCountingService V2.1 observed; V1.0 historical file not yet integrated in current branch state | pending | Historical release-tag search/backfill decision needed. |
| Ticketing / TicketInformation | 301-2-9 | 1.0 | TicketInformationService V1.0 | pending | PDF/XSD naming map TicketingService vs TicketInformationService must be resolved explicitly. |
| TimeService | 301-2-10 | 1.0 | no dedicated TimeService XSD observed | pending | Possible non-XSD service; must be confirmed rather than assumed. |
| VideoLiveService | 301-2-11 | 1.0, 2.0 | VideoLiveService V2.0 observed | pending | V1.0 historical provenance/backfill check needed. |
| VideoRecordingService | 301-2-12 | 1.0, 2.0, 2.4 | V2.0 official; V2.4 candidate/integration | pending | V1.0 historical provenance and V2.4 candidate separation required. |
| VideoDisplayService | 301-2-13 | 1.0, 2.0 | VideoDisplayService V2.0 observed | pending | V1.0 historical provenance/backfill check needed. |
| TrainSet services | 301-2-14 | 2.1, 2.2 | V2.1 official release material exists historically; V2.2 service XSDs observed | pending | Three service schemas must remain dependency-routed separately. |
| DoorStateService | 301-2-15 | 2.1 | DoorStateService V2.1 + Common V1.0 + Enumerations V1.0 | first pass completed | DRS-001..DRS-004 retained; local compile/sample validation pending. |
| TicketValidationService | 301-2-16 | 2.1, 2.2, 2.3, 2.4 | V2.1 official backfill; V2.2 official; document V2.3 routes officially to XSD V2.2; branch V2.3 candidate only; V2.4 integration/candidate | first pass completed | TVS-001..TVS-003 retained; local validation pending. |
| HTMLDisplayService | 301-2-17 | 2.1, 2.2, 2.2a | no dedicated service XSD by design; version-specific DNS-SD/HTTP profile | first pass completed | HDS-001 closed OK with note. V2.1 content/path; V2.2 content/url; V2.2a adds `_ibisip_http._tcp` transition. |
| SystemMonitoringService | 301-2-18 | 2.2 | SystemMonitoringService V2.2 | **next** | Next planned historical PDF/XSD block. |
| AnalogRadioService | 301-2-19 | 2.4 | AnalogRadioService V2.4 candidate/integration material | pending | Keep provenance candidate/integration unless official release authority is confirmed. |
| Network infrastructure | 301-3 | 02-2020 | not applicable / non-service | pending context audit | May inform DNS-SD/HTTP/network profile checks. |

## Important resolved routing exceptions

```text
Common V2.3 -> Enumerations V2.2.
DoorStateService V2.1 -> Common V1.0 + Enumerations V1.0.
TicketValidationService document V2.3 -> official TicketValidationService XSD V2.2 + Common V2.2 + Enumerations V2.2.
HTMLDisplayService V2.1/V2.2/V2.2a -> non-XSD discovery_http_profile, not a neighbouring service XSD.
```

These are intentional routing facts and must not be normalised to matching version numbers for symmetry.

## Gap handling rules

If a PDF version has no matching XSD in the branch:

```text
Do not assume the XSD is missing incorrectly.
Classify as one of:
- historical official file absent from branch,
- intentionally no dedicated XSD,
- document version intentionally reuses an older XSD,
- renamed XSD/service,
- candidate/integration provenance,
- unresolved.
```

If an XSD version has no matching public PDF:

```text
Do not treat it as official by default.
Keep candidate/integration/fork provenance explicit until official release authority is established.
```

## Current priority

```text
docs/pdf_xsd_semantic_audit/11_system_monitoring_service_historical_start.md
```

Planned first checks:

```text
1. Re-fetch dev/schema-integration head before writing.
2. Read existing SystemMonitoringService references/findings to avoid duplication.
3. Map VDV 301-2-18 V2.2 PDF to IBIS-IP_SystemMonitoringService_V2.2.xsd.
4. Resolve the exact Common/Enumerations dependency pool from the service XSD and official release provenance.
5. Compare operations/data structures and classify PDF/XSD differences without changing the schema.
6. Add local compile/sample tasks, but do not claim validation until actually executed.
```
