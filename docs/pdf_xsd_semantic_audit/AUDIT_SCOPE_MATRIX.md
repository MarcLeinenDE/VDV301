# PDF/XSD audit scope matrix

Status: active control matrix; refreshed after VideoRecordingService V1.0/V2.0/V2.4 first-pass closure.

Purpose:

```text
Track every public VDV301 service/scope and relevant document version against exact executable schema/protocol routing in dev/schema-integration.
```

Core rules:

```text
Validation follows the selected XSD family where an executable XSD exists.
No latest-wins substitution.
Historical XSD backfill: official VDVde/VDV301 release tags only.
Open PR/candidate material remains candidate/integration.
A public document without a dedicated XSD is not automatically a gap.
Historical aggregate XSDs may be part of a version's official root-validation family.
If the same versioned path has different official blobs in different releases, release_context/schema_revision must remain distinguishable.
Intentionally non-XSD services must route to explicit protocol/discovery profiles instead of fabricated schemas.
Media/protocol runtime validation remains separate from XML/XSD validation.
```

| Area | VDV part | Published PDF versions | Relevant XSD/routing state | Audit status | Notes |
|---|---|---|---|---|---|
| Base / General Conventions | 301-2 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | no single service XSD | pending dedicated historical block | Cross-service authority; V1.0 aggregate family needs dedicated treatment. |
| Common Data Structures and Enumerations | 301-2-1 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | Common V1.0..V2.4; Enums V1.0,V2.0,V2.1,V2.2,V2.4 | first pass completed + addendum | CE-001..CE-019; local validation pending. |
| DeviceManagementService | 301-2-0 | 2.0, 2.1, 2.2, 2.4 | V2.2 official; V2.3 integration; V2.4 candidate/integration | partial / V2.2-V2.4 first pass completed | Older V2.0/V2.1 separate. |
| BeaconLocationService | 301-2-2 | 1.0 | V1.0 | first pass completed | |
| CustomerInformationService | 301-2-3 | 1.1, 2.0, 2.2, 2.3 | historical official backfills V1.0,V2.0,V2.2; official V2.3; V2.4 candidate | first pass completed for public versions | CIS findings retained. |
| DistanceLocationService | 301-2-4 | 1.0 | V1.0 | first pass completed | |
| GNSSLocationService | 301-2-5 | 1.0 | V1.0 | first pass completed | |
| JourneyInformationService | 301-2-6 | 1.0 | V1.0 | first pass completed | JIS findings retained. |
| NetworkLocationService | 301-2-7 | 1.0 | V1.0 | first pass completed | |
| PassengerCountingService | 301-2-8 | 1.0, 2.1 | V1.0 official historical backfill + Common V1.0 + Enums V1.0; V1.0 roots in official IBIS_IP_V1.0 aggregate; V2.1 official + Common V1.0 + Enums V1.0 | first pass completed | PCS findings; local validation pending. |
| Ticketing / TicketInformation | 301-2-9 | 1.0 | original V1.0 blob 017ca646 + Common/Enums V1.0 + aggregate roots; later official V1.0 revision blob 3fda66d8 + Common/Enums V1.0 | first pass completed | TKT findings; release-context key required. |
| TimeService | 301-2-10 | 1.0 | intentional non-XSD `sntp_dns_sd_profile`; SNTP/DNS-SD | first pass completed | TS findings; runtime validation pending. |
| VideoLiveService | 301-2-11 | 1.0, 2.0 | V1.0 public but strict-XSD-unresolved; V2.0 official blob d8c52f5d + Common V2.0 + Enums V2.0 | first pass completed | VLS findings; XML/media validation pending. |
| VideoRecordingService | 301-2-12 | 1.0, 2.0, 2.4 | V1.0 public/no official-tag XSD; V2.0 official blob 6ef0dae6 + Common V2.0 + Enums V2.0; V2.4 exact open PR #27 candidate blob 07ff2c41 + Common V2.0 + Enums V2.0 | first pass completed | VRS-001..VRS-005; VRS-003 strong compositor candidate; local validation pending. |
| VideoDisplayService | 301-2-13 | 1.0, 2.0 | V2.0 observed | **next** | Resolve V1.0 provenance and exact V2.0 pool. |
| TrainSet services | 301-2-14 | 2.1, 2.2 | V2.1 historical official; V2.2 observed | pending | Three service schemas separately routed. |
| DoorStateService | 301-2-15 | 2.1 | V2.1 + Common V1.0 + Enums V1.0 | first pass completed | DRS findings; local validation pending. |
| TicketValidationService | 301-2-16 | 2.1, 2.2, 2.3, 2.4 | V2.1 official; V2.2 official; doc V2.3 -> XSD V2.2; V2.4 candidate | first pass completed | TVS findings; local validation pending. |
| HTMLDisplayService | 301-2-17 | 2.1, 2.2, 2.2a | non-XSD discovery_http_profile | first pass completed | HDS-001 OK with note. |
| SystemMonitoringService | 301-2-18 | 2.2 | official V2.2 + Common V2.2 + Enums V2.2 | first pass completed | SMS findings + CE inheritance. |
| AnalogRadioService | 301-2-19 | 2.4 | public V2.4 doc; exact XSD candidate from open PR #27 -> Common V2.3 -> Enums V2.2 | first pass completed | ARA findings; candidate only. |
| Network infrastructure | 301-3 | 02-2020 | non-service context | pending | DNS-SD/HTTP/network context. |

## Resolved non-obvious routing facts

```text
Common V2.3 -> Enumerations V2.2.
DoorStateService V2.1 -> Common V1.0 + Enumerations V1.0.
TicketValidationService document V2.3 -> official TVS XSD V2.2 + Common V2.2 + Enumerations V2.2.
HTMLDisplayService V2.1/V2.2/V2.2a -> non-XSD discovery_http_profile.
SystemMonitoringService V2.2 -> Common V2.2 + Enumerations V2.2.
AnalogRadioService V2.4 candidate -> Common V2.3 -> Enumerations V2.2.
PassengerCountingService V2.1 -> Common V1.0 + Enums V1.0.
TicketingService executable XML identity is TicketingService, not TicketInformationService.
TimeService V1.0 -> non-XSD SNTP/DNS-SD profile.
VideoLiveService V1.0 -> public-document-known but strict-XSD-unresolved; do not map to V2.0.
VideoLiveService V2.0 -> Common V2.0 + Enumerations V2.0.
VideoRecordingService V1.0 -> public-document-known but strict-XSD-unresolved; do not map to V2.0.
VideoRecordingService V2.0 -> Common V2.0 + Enumerations V2.0.
VideoRecordingService V2.4 candidate -> Common V2.0 + Enumerations V2.0; do not map to Common/Enums V2.4.
```

## Current priority

```text
docs/pdf_xsd_semantic_audit/18_video_display_service_historical_start.md
```

First actions:

```text
1. Re-fetch branch head.
2. Check official release tags for VideoDisplayService V1.0/V2.0.
3. Backfill only from official tags if a missing historical XSD exists.
4. Resolve exact V2.0 dependency pool.
5. Compare V1.0/V2.0 PDF structures and operation semantics.
6. Check for compositor/type-name issues analogous to VideoLive/VideoRecording.
7. Do not claim compile/sample/media validation unless actually executed.
```
