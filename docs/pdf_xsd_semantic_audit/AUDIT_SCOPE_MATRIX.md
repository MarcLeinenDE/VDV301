# PDF/XSD audit scope matrix

Status: active control matrix; executable baseline completed, finding-driven validation in progress.

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
| Common Data Structures and Enumerations | 301-2-1 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | version-specific Common/Enums including generic subscription structures | first pass completed + addendum; CE-018 executable-confirmed | run 33109768872 confirms empty and one-item ServiceIdentificationWithStateList in Common V1.0-V2.4. |
| DeviceManagementService | 301-2-0 | historical V1.0 XSD plus 2.0, 2.1, 2.2, 2.4 docs | V1.0 official type-XSD + legacy root map; V2.0/V2.1/V2.2 official; V2.3 integration; V2.4 candidate | first pass completed V2.0-V2.4; executable candidate samples passed | six DMS V2.4 regression samples passed in run 33109011670. |
| BeaconLocationService | 301-2-2 | 1.0 | standalone V1.0 | first pass completed | old combined LocationService packaging not retained. |
| CustomerInformationService | 301-2-3 | 1.1, 2.0, 2.2, 2.3 | V1.0 official type-XSD + legacy root map; later versions service-local | first pass completed + legacy root adapter compiled | CIS-002 resolved by block 23. |
| DistanceLocationService | 301-2-4 | 1.0 | standalone V1.0 | first pass completed | old combined LocationService packaging not retained. |
| GNSSLocationService | 301-2-5 | 1.0 | standalone V1.0 | first pass completed | old combined LocationService packaging not retained. |
| JourneyInformationService | 301-2-6 | 1.0 | later official self-contained V1.0 revision selected | first pass completed | historical original aggregate packaging recorded; no duplicate operational copy. |
| NetworkLocationService | 301-2-7 | 1.0 | V1.0 | first pass completed | byte-identical across 1.0/2.0 tags. |
| PassengerCountingService | 301-2-8 | 1.0, 2.1 | later official self-contained V1.0 revision + V2.1 official | first pass completed; PCS-001 executable-confirmed | run 33109367265 proves exact V2.1 route rejects OperationNotSupported while Enums V2.1 control accepts it. |
| Ticketing / TicketInformation | 301-2-9 | 1.0 | later official self-contained V1.0 revision selected | first pass completed | TKT findings; no duplicate original packaging copy. |
| TimeService | 301-2-10 | 1.0 | non-XSD SNTP/DNS-SD | first pass completed | TS findings. |
| VideoLiveService | 301-2-11 | 1.0, 2.0 | V1.0 strict-XSD unresolved; V2.0 official | first pass completed; **EV-103 next** | VLS-002 compositor target. |
| VideoRecordingService | 301-2-12 | 1.0, 2.0, 2.4 | V1.0 unresolved; V2.0 official; V2.4 candidate | first pass completed; **EV-103 next** | VRS-003 compositor target. |
| VideoDisplayService | 301-2-13 | 1.0, 2.0 | V1.0 unresolved; V2.0 official | first pass completed; **EV-103 next** | VDS compositor targets. |
| TrainSet services | 301-2-14 | 2.1, 2.2 | three separately routed service families | first pass completed | TSM-002/TSD-003 are EV-104 targets. |
| DoorStateService | 301-2-15 | 2.1 | Common V1.0 + Enums V1.0 | first pass completed | DRS findings. |
| TicketValidationService | 301-2-16 | 2.1, 2.2, 2.3, 2.4 | version-specific; V2.3 doc -> XSD V2.2; V2.4 candidate | first pass completed | TVS findings. |
| HTMLDisplayService | 301-2-17 | 2.1, 2.2, 2.2a | non-XSD HTTP/discovery profile | first pass completed | HDS findings. |
| SystemMonitoringService | 301-2-18 | 2.2 | Common/Enums V2.2 | first pass completed | SMS-001 resolved by block 23. |
| AnalogRadioService | 301-2-19 | 2.4 | PR #27 candidate -> Common V2.3 -> Enums V2.2 | first pass completed | ARA-003 is EV-105 target. |
| Legacy SystemManagement/SystemDocumentation | historical 301-2 base | V1.0 XSD lineage | SystemManagement self-contained V1.0 from tag 2.0; SystemDocumentation V1.0 type-XSD + root map | integrated; legacy root adapter compiled | no duplicate aggregate mirror. |
| Network infrastructure | 301-3 | 02-2020 | non-XSD physical/network profile + discovery runtime context | first pass completed | NET/DISC findings; live validation later. |
| Cross-service subscription modelling | 301-2 conventions + services | historical | generic Common structures + service-specific exceptions + operation-manifest layer | first pass completed | SUB-001/SUB-002; TSD-003 open for EV-104. |
| Executable validation matrix | cross-version | historical/current/candidate | root compile + legacy root adapters + targeted samples | **in progress** | EV-001/EV-002, EV-101 and EV-102 passed; EV-103 next. |

## Executed technical baseline

```text
GitHub Actions run: 33109011670
head tested: 8dac3ec3a9e6fbebec2b3c3d4f381d69cfc07066
46 root XSDs: compile PASS
DMS V2.4 samples: 6/6 PASS
Legacy V1.0 root adapters: CIS/DMS/SystemDocumentation PASS
```

## Executed targeted finding evidence

```text
EV-101 / PCS-001
GitHub Actions run: 33109367265
exact PCS V2.1 route compile: PASS
DataNotValid against exact Enums V1.0 route: PASS
OperationNotSupported against exact Enums V1.0 route: correctly rejected
OperationNotSupported against Enums V2.1 explanatory control: accepted
PCS-001: executable-confirmed

EV-102 / CE-018
GitHub Actions run: 33109768872
Common V1.0-V2.4 harnesses: PASS
empty ServiceIdentificationWithStateList: accepted in every tested Common version
one-item ServiceIdentificationWithStateList: accepted in every tested Common version
CE-018: executable-confirmed xsd_more_permissive_than_pdf
```

The workflow is `workflow_dispatch` only and does not run on normal audit pushes.

## Current priority

```text
EV-103 - Video service xs:choice modelling candidates
```

Targets:

```text
VLS-002  VideoLiveService V2.0 LiveStreamData compositor
VRS-003  VideoRecordingService V2.0 recording-state compositor
VDS       VideoDisplayService V2.0 capability/request/response compositor findings
```

Test principle:

```text
1. Compile exact official V2.0 service/dependency pools.
2. Build minimal one-choice-field samples expected to validate.
3. Build PDF-shaped multi-field records expected to fail if xs:choice is the operative restriction.
4. Record each service/finding independently; do not change XSDs.
```

Planned order after EV-103:

```text
EV-104 TrainSet TSM-002/TSD-003 root/modelling cases
EV-105 AnalogRadio ARA-003 candidate cardinality
then runtime/discovery/HTTP/SNTP/RTSP layers
```
