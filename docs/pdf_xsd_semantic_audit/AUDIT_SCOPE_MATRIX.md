# PDF/XSD audit scope matrix

Status: active control matrix; refreshed after TrainSet services V2.1/V2.2 first-pass closure.

Core rules:

```text
Validation follows the selected XSD family where an executable XSD exists.
No latest-wins substitution.
Historical XSD backfill: official VDVde/VDV301 release tags only.
Open PR/candidate material remains candidate/integration.
A public document without a dedicated XSD is not automatically a gap.
Historical aggregate XSDs may be part of a version's official root-validation family.
If the same versioned path has different official blobs in different releases, release_context/schema_revision must remain distinguishable.
Intentionally non-XSD services route to explicit protocol/discovery profiles.
Media/protocol runtime validation remains separate from XML/XSD validation.
Multi-service documents do not imply a shared dependency pool; resolve each service XSD independently.
```

| Area | VDV part | Published PDF versions | Relevant XSD/routing state | Audit status | Notes |
|---|---|---|---|---|---|
| Base / General Conventions | 301-2 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | no single service XSD | pending dedicated historical block | Cross-service authority; V1.0 aggregate family. |
| Common Data Structures and Enumerations | 301-2-1 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | version-specific Common/Enums | first pass completed + addendum | CE findings; validation pending. |
| DeviceManagementService | 301-2-0 | 2.0, 2.1, 2.2, 2.4 | V2.2 official; V2.3 integration; V2.4 candidate/integration | **next: historical completion** | close V2.0/V2.1. |
| BeaconLocationService | 301-2-2 | 1.0 | V1.0 | first pass completed | |
| CustomerInformationService | 301-2-3 | 1.1, 2.0, 2.2, 2.3 | historical official plus candidate | first pass completed | CIS findings. |
| DistanceLocationService | 301-2-4 | 1.0 | V1.0 | first pass completed | |
| GNSSLocationService | 301-2-5 | 1.0 | V1.0 | first pass completed | |
| JourneyInformationService | 301-2-6 | 1.0 | V1.0 | first pass completed | JIS findings. |
| NetworkLocationService | 301-2-7 | 1.0 | V1.0 | first pass completed | |
| PassengerCountingService | 301-2-8 | 1.0, 2.1 | historical official version-specific pools | first pass completed | PCS findings. |
| Ticketing / TicketInformation | 301-2-9 | 1.0 | release-context-specific V1.0 revisions | first pass completed | TKT findings. |
| TimeService | 301-2-10 | 1.0 | non-XSD SNTP/DNS-SD | first pass completed | TS findings. |
| VideoLiveService | 301-2-11 | 1.0, 2.0 | V1.0 strict-XSD unresolved; V2.0 official | first pass completed | VLS findings. |
| VideoRecordingService | 301-2-12 | 1.0, 2.0, 2.4 | V1.0 unresolved; V2.0 official; V2.4 candidate | first pass completed | VRS findings. |
| VideoDisplayService | 301-2-13 | 1.0, 2.0 | V1.0 unresolved; V2.0 official | first pass completed | VDS findings. |
| TrainSet services | 301-2-14 | 2.1, 2.2 | three separately routed service families for each version | first pass completed | TSI/TSM/TSD findings; V2.1->V2.2 technical corrections. |
| DoorStateService | 301-2-15 | 2.1 | Common V1.0 + Enums V1.0 | first pass completed | DRS findings. |
| TicketValidationService | 301-2-16 | 2.1, 2.2, 2.3, 2.4 | version-specific; doc V2.3 -> XSD V2.2; V2.4 candidate | first pass completed | TVS findings. |
| HTMLDisplayService | 301-2-17 | 2.1, 2.2, 2.2a | non-XSD HTTP/discovery profile | first pass completed | HDS findings. |
| SystemMonitoringService | 301-2-18 | 2.2 | Common/Enums V2.2 | first pass completed | SMS findings. |
| AnalogRadioService | 301-2-19 | 2.4 | PR #27 candidate -> Common V2.3 -> Enums V2.2 | first pass completed | ARA findings. |
| Network infrastructure | 301-3 | 02-2020 | non-service context | pending | DNS-SD/HTTP/network context. |

## Current priority

```text
docs/pdf_xsd_semantic_audit/20_device_management_service_v2_0_v2_1_historical_completion.md
```

Then:

```text
Base / General Conventions historical-family closure
Network infrastructure / discovery-context audit
cross-service subscription modelling closure
local XSD compilation and executable sample matrix
```
