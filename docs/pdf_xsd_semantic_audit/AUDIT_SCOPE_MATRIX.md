# PDF/XSD audit scope matrix

Status: active control matrix; refreshed after VideoDisplayService V1.0/V2.0 first-pass closure.

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
| PassengerCountingService | 301-2-8 | 1.0, 2.1 | V1.0 official historical backfill + Common V1.0 + Enums V1.0; V1.0 roots in official aggregate; V2.1 official + Common V1.0 + Enums V1.0 | first pass completed | PCS findings; local validation pending. |
| Ticketing / TicketInformation | 301-2-9 | 1.0 | release-context-specific V1.0 schema revisions + Common/Enums V1.0 | first pass completed | TKT findings; release-context key required. |
| TimeService | 301-2-10 | 1.0 | intentional non-XSD SNTP/DNS-SD profile | first pass completed | TS findings; runtime validation pending. |
| VideoLiveService | 301-2-11 | 1.0, 2.0 | V1.0 public/no official-tag XSD; V2.0 official + Common V2.0 + Enums V2.0 | first pass completed | VLS findings. |
| VideoRecordingService | 301-2-12 | 1.0, 2.0, 2.4 | V1.0 public/no official-tag XSD; V2.0 official + Common/Enums V2.0; V2.4 open PR #27 candidate + Common/Enums V2.0 | first pass completed | VRS findings; local validation pending. |
| VideoDisplayService | 301-2-13 | 1.0, 2.0 | V1.0 public/no official-tag XSD; V2.0 official blob fcfdadd3 + Common V2.0 + Enums V2.0 | first pass completed | VDS-001..VDS-005; strong compositor findings; local validation pending. |
| TrainSet services | 301-2-14 | 2.1, 2.2 | V2.1 historical official; V2.2 observed | **next** | Three service schemas separately routed. |
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
HTMLDisplayService -> non-XSD discovery_http_profile.
SystemMonitoringService V2.2 -> Common V2.2 + Enumerations V2.2.
AnalogRadioService V2.4 candidate -> Common V2.3 -> Enumerations V2.2.
PassengerCountingService V2.1 -> Common V1.0 + Enums V1.0.
TicketingService executable XML identity is TicketingService, not TicketInformationService.
TimeService V1.0 -> non-XSD SNTP/DNS-SD profile.
VideoLiveService V1.0 -> strict-XSD-unresolved; V2.0 -> Common/Enums V2.0.
VideoRecordingService V1.0 -> strict-XSD-unresolved; V2.0 -> Common/Enums V2.0; V2.4 candidate -> Common/Enums V2.0.
VideoDisplayService V1.0 -> strict-XSD-unresolved; V2.0 -> Common V2.0 + Enumerations V2.0.
```

## Current priority

```text
docs/pdf_xsd_semantic_audit/19_train_set_services_historical_start.md
```

First actions:

```text
1. Re-fetch branch head.
2. Resolve TrainSetDataService, TrainSetInformationService and TrainSetManagementService separately.
3. Check V2.1/V2.2 public document semantics and official release provenance.
4. Preserve exact dependencies per each service XSD; do not assume all three use the same pool.
5. Check whether V2.2 is a true service-XSD revision or document-only/release-context change.
6. Open findings only where evidence supports them.
7. Do not claim compile/sample validation unless actually run.
```
