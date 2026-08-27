# PDF/XSD audit scope matrix

Status: active control matrix; refreshed after V1.0 superbranch deduplication review.

Core rules:

```text
Validation follows the selected XSD family where an executable XSD exists.
No latest-wins substitution across service versions.
Historical source provenance: official VDVde/VDV301 release tags only.
The superbranch is a deduplicated operational integration set, not a byte-for-byte archive of every tag.
Open PR/candidate material remains candidate/integration.
A public document without a dedicated XSD is not automatically a gap.
Byte-identical historical XSDs are stored once.
Packaging-only same-version official revisions may be collapsed only after semantic diff review.
Actual payload-constraint differences must remain separately routable.
Legacy aggregate-root declarations may be represented as provenance-backed resolver metadata when the operational service XSD is type-only.
Intentionally non-XSD services route to explicit protocol/discovery profiles.
Media/protocol/runtime validation remains separate from XML/XSD validation.
Multi-service documents do not imply a shared dependency pool; resolve each service XSD independently.
Later schema/document corrections must not be retroactively applied across service versions.
Supported-operation discovery must not be derived solely from service-XSD operation-group membership; use operation semantics + payload-schema mapping.
```

| Area | VDV part | Published PDF versions | Relevant XSD/routing state | Audit status | Notes |
|---|---|---|---|---|---|
| Base / General Conventions | 301-2 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | deduplicated V1.0 service set; legacy aggregate roots mapped in `schema_profiles` | first pass completed + storage refinement | BG-001/BG-002 refined; no full V1.0 pool mirror. |
| Common Data Structures and Enumerations | 301-2-1 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | version-specific Common/Enums including generic subscription structures | first pass completed + addendum | CE findings; SUB-001 cross-reference; validation pending. |
| DeviceManagementService | 301-2-0 | historical V1.0 XSD plus 2.0, 2.1, 2.2, 2.4 docs | V1.0 official type-XSD + legacy root map; V2.0/V2.1/V2.2 official; V2.3 integration; V2.4 candidate | first pass completed V2.0-V2.4; V1.0 integrated for completeness | DMS findings; explicit subscription group style informs SUB-002. |
| BeaconLocationService | 301-2-2 | 1.0 | standalone V1.0 | first pass completed | old combined LocationService packaging not retained. |
| CustomerInformationService | 301-2-3 | 1.1, 2.0, 2.2, 2.3 | V1.0 official type-XSD + legacy root map; later versions service-local | first pass completed | CIS-002 resolved by block 23. |
| DistanceLocationService | 301-2-4 | 1.0 | standalone V1.0 | first pass completed | old combined LocationService packaging not retained. |
| GNSSLocationService | 301-2-5 | 1.0 | standalone V1.0 | first pass completed | old combined LocationService packaging not retained. |
| JourneyInformationService | 301-2-6 | 1.0 | later official self-contained V1.0 revision selected | first pass completed | historical original aggregate packaging recorded; no duplicate operational copy. |
| NetworkLocationService | 301-2-7 | 1.0 | V1.0 | first pass completed | byte-identical across 1.0/2.0 tags. |
| PassengerCountingService | 301-2-8 | 1.0, 2.1 | later official self-contained V1.0 revision + V2.1 official | first pass completed | PCS findings; original aggregate packaging retained as provenance only. |
| Ticketing / TicketInformation | 301-2-9 | 1.0 | later official self-contained V1.0 revision selected | first pass completed | TKT findings; no duplicate original packaging copy. |
| TimeService | 301-2-10 | 1.0 | non-XSD SNTP/DNS-SD | first pass completed | TS findings. |
| VideoLiveService | 301-2-11 | 1.0, 2.0 | V1.0 strict-XSD unresolved; V2.0 official | first pass completed | VLS findings. |
| VideoRecordingService | 301-2-12 | 1.0, 2.0, 2.4 | V1.0 unresolved; V2.0 official; V2.4 candidate | first pass completed | VRS findings. |
| VideoDisplayService | 301-2-13 | 1.0, 2.0 | V1.0 unresolved; V2.0 official | first pass completed | VDS findings. |
| TrainSet services | 301-2-14 | 2.1, 2.2 | three separately routed service families | first pass completed | TSD-003 remains open after block 23. |
| DoorStateService | 301-2-15 | 2.1 | Common V1.0 + Enums V1.0 | first pass completed | DRS findings. |
| TicketValidationService | 301-2-16 | 2.1, 2.2, 2.3, 2.4 | version-specific; V2.3 doc -> XSD V2.2; V2.4 candidate | first pass completed | TVS findings. |
| HTMLDisplayService | 301-2-17 | 2.1, 2.2, 2.2a | non-XSD HTTP/discovery profile | first pass completed | HDS findings. |
| SystemMonitoringService | 301-2-18 | 2.2 | Common/Enums V2.2 | first pass completed | SMS-001 resolved by block 23. |
| AnalogRadioService | 301-2-19 | 2.4 | PR #27 candidate -> Common V2.3 -> Enums V2.2 | first pass completed | ARA findings. |
| Legacy SystemManagement/SystemDocumentation | historical 301-2 base | V1.0 XSD lineage | SystemManagement self-contained V1.0 from tag 2.0; SystemDocumentation V1.0 type-XSD + root map | integrated for historical completeness | no duplicate aggregate mirror. |
| Network infrastructure | 301-3 | 02-2020 | non-XSD physical/network profile + discovery runtime context | first pass completed | NET/DISC findings; live validation pending. |
| Cross-service subscription modelling | 301-2 conventions + services | historical | generic Common structures + service-specific exceptions + operation-manifest layer | first pass completed | SUB-001/SUB-002; TSD-003 open. |
| Executable validation matrix | cross-version | historical/current/candidate | root compile + legacy root adapters + targeted samples | **next** | start EV-001/EV-002 with deduplicated layout. |

## Current priority

```text
docs/pdf_xsd_semantic_audit/24_executable_validation_matrix_start.md
```
