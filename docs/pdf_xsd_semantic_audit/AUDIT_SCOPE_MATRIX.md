# PDF/XSD audit scope matrix

Status: active control matrix; refreshed after Network infrastructure / discovery context closure.

Core rules:

```text
Validation follows the selected XSD family where an executable XSD exists.
No latest-wins substitution.
Historical XSD backfill: official VDVde/VDV301 release tags only.
Open PR/candidate material remains candidate/integration.
A public document without a dedicated XSD is not automatically a gap.
Historical aggregate XSDs may be part of a version's official root-validation family.
If the same versioned path has different official blobs in different releases, release_context/schema_revision must remain distinguishable.
Exact historical release families may be isolated under schema_pools/official/<tag>/ to preserve relative includes and same-path revisions.
Intentionally non-XSD services route to explicit protocol/discovery profiles.
Media/protocol/runtime validation remains separate from XML/XSD validation.
Multi-service documents do not imply a shared dependency pool; resolve each service XSD independently.
Later schema/document corrections must not be retroactively applied to historical validation profiles.
Physical/network recommendations retain their requirement level and are not promoted to XSD failures.
External protocol standards may add checks, but their authority must be attributed separately from VDV.
```

| Area | VDV part | Published PDF versions | Relevant XSD/routing state | Audit status | Notes |
|---|---|---|---|---|---|
| Base / General Conventions | 301-2 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | original V1.0 aggregate preserved as `official:VDV-301-1.0`; later releases service-family based | first pass completed | BG-001/BG-002; same-path official V1.0 revisions; discovery rules referenced by block 22. |
| Common Data Structures and Enumerations | 301-2-1 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | version-specific Common/Enums | first pass completed + addendum | CE findings; validation pending. |
| DeviceManagementService | 301-2-0 | 2.0, 2.1, 2.2, 2.4 | V2.0/V2.1/V2.2 official; V2.3 integration; V2.4 candidate | first pass completed V2.0-V2.4 | DMS findings; validation pending. |
| BeaconLocationService | 301-2-2 | 1.0 | V1.0 | first pass completed | |
| CustomerInformationService | 301-2-3 | 1.1, 2.0, 2.2, 2.3 | version-specific | first pass completed | CIS findings. |
| DistanceLocationService | 301-2-4 | 1.0 | V1.0 | first pass completed | |
| GNSSLocationService | 301-2-5 | 1.0 | V1.0 | first pass completed | |
| JourneyInformationService | 301-2-6 | 1.0 | release-context-specific V1.0 revisions | first pass completed | JIS findings + BG-001. |
| NetworkLocationService | 301-2-7 | 1.0 | V1.0 | first pass completed | |
| PassengerCountingService | 301-2-8 | 1.0, 2.1 | release-context-specific V1.0 plus V2.1 | first pass completed | PCS findings + BG-001. |
| Ticketing / TicketInformation | 301-2-9 | 1.0 | release-context-specific V1.0 revisions | first pass completed | TKT findings + BG-001. |
| TimeService | 301-2-10 | 1.0 | non-XSD SNTP/DNS-SD | first pass completed | TS findings. |
| VideoLiveService | 301-2-11 | 1.0, 2.0 | V1.0 strict-XSD unresolved; V2.0 official | first pass completed | VLS findings. |
| VideoRecordingService | 301-2-12 | 1.0, 2.0, 2.4 | V1.0 unresolved; V2.0 official; V2.4 candidate | first pass completed | VRS findings. |
| VideoDisplayService | 301-2-13 | 1.0, 2.0 | V1.0 unresolved; V2.0 official | first pass completed | VDS findings. |
| TrainSet services | 301-2-14 | 2.1, 2.2 | three separately routed service families | first pass completed | TSI/TSM/TSD findings. |
| DoorStateService | 301-2-15 | 2.1 | Common V1.0 + Enums V1.0 | first pass completed | DRS findings. |
| TicketValidationService | 301-2-16 | 2.1, 2.2, 2.3, 2.4 | version-specific; V2.3 doc -> XSD V2.2; V2.4 candidate | first pass completed | TVS findings. |
| HTMLDisplayService | 301-2-17 | 2.1, 2.2, 2.2a | non-XSD HTTP/discovery profile | first pass completed | HDS findings. |
| SystemMonitoringService | 301-2-18 | 2.2 | Common/Enums V2.2 | first pass completed | SMS findings. |
| AnalogRadioService | 301-2-19 | 2.4 | PR #27 candidate -> Common V2.3 -> Enums V2.2 | first pass completed | ARA findings. |
| Network infrastructure | 301-3 | 02-2020 | non-XSD physical/network profile + General-Conventions discovery runtime context | first pass completed | NET-001..003; DISC-001..003; live validation pending. |
| Cross-service subscription modelling | 301-2 conventions + services | historical | generic and service-specific Subscribe/Unsubscribe structures | **next** | Resolve earlier CIS/SMS/TSD modelling notes without changing XSD. |

## Current priority

```text
docs/pdf_xsd_semantic_audit/23_cross_service_subscription_modelling_closure.md
```

Then:

```text
local XSD compilation and executable sample matrix
```
