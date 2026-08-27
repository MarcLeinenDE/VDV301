# PDF/XSD audit scope matrix

Status: semantic/provenance first pass completed; executable XSD evidence completed; deterministic runtime/protocol evidence RV-001 through RV-004 completed. Remaining technical work is live/integration evidence plus SDK implementation.

Core rules:

```text
Validation follows the selected XSD family where an executable XSD exists.
No latest-wins substitution across service versions or external protocol versions.
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
Protocol/runtime checks must distinguish VDV-specific requirements, incorporated external standards, and diagnostic heuristics.
EV-* identifiers are reserved for executable XML/XSD evidence; RV-* identifiers are reserved for runtime/protocol evidence.
Unexecuted live/integration checks are open capability tests, not failed conformance findings.
```

| Area | VDV part | Published PDF versions | Relevant XSD/routing state | Audit status | Notes |
|---|---|---|---|---|---|
| Base / General Conventions | 301-2 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | deduplicated V1.0 service set; legacy aggregate roots mapped in `schema_profiles` | first pass completed + storage refinement | BG-001/BG-002 refined; HTTP/discovery rules deterministic-tested in RV-001/RV-002. |
| Common Data Structures and Enumerations | 301-2-1 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | version-specific Common/Enums including generic subscription structures | first pass completed; CE-018 executable-confirmed | run 33109768872 confirms 0:* behavior. |
| DeviceManagementService | 301-2-0 | historical V1.0 XSD plus 2.0, 2.1, 2.2, 2.4 docs | V1.0 official type-XSD + legacy root map; V2.0/V2.1/V2.2 official; V2.3 integration; V2.4 candidate | first pass completed; candidate samples passed | six DMS V2.4 regression samples passed. |
| BeaconLocationService | 301-2-2 | 1.0 | standalone V1.0 | first pass completed | old combined LocationService packaging not retained. |
| CustomerInformationService | 301-2-3 | 1.1, 2.0, 2.2, 2.3 | V1.0 official type-XSD + legacy root map; later versions service-local | first pass completed + legacy root adapter compiled | CIS-002 resolved by block 23. |
| DistanceLocationService | 301-2-4 | 1.0 | standalone V1.0 | first pass completed | old combined LocationService packaging not retained. |
| GNSSLocationService | 301-2-5 | 1.0 | standalone V1.0 | first pass completed | old combined LocationService packaging not retained. |
| JourneyInformationService | 301-2-6 | 1.0 | later official self-contained V1.0 revision selected | first pass completed | historical original aggregate packaging recorded. |
| NetworkLocationService | 301-2-7 | 1.0 | V1.0 | first pass completed | byte-identical across 1.0/2.0 tags. |
| PassengerCountingService | 301-2-8 | 1.0, 2.1 | later official self-contained V1.0 revision + V2.1 official | PCS-001 executable-confirmed | run 33109367265 proves OperationNotSupported conflict. |
| Ticketing / TicketInformation | 301-2-9 | 1.0 | later official self-contained V1.0 revision selected | first pass completed | TKT findings retained. |
| TimeService | 301-2-10 | 1.0 | non-XSD SNTP/DNS-SD | first pass + RV-003 deterministic PASS | live DNS-SD/SNTP exchange and clock diagnostics remain in block 26. |
| VideoLiveService | 301-2-11 | 1.0, 2.0 | V1.0 strict-XSD unresolved; V2.0 official | VLS-002 executable-confirmed + RV-004 deterministic PASS | live ListAllLiveStreams/RTSP/RTP remains in block 26. |
| VideoRecordingService | 301-2-12 | 1.0, 2.0, 2.4 | V1.0 unresolved; V2.0 official; V2.4 candidate | VRS-003 executable-confirmed | run 33111119723; V2.4 control candidate-only. |
| VideoDisplayService | 301-2-13 | 1.0, 2.0 | V1.0 unresolved; V2.0 official | VDS-002/003/004 executable-confirmed | run 33111119723. |
| TrainSet services | 301-2-14 | 2.1, 2.2 | three separately routed service families | EV-104 completed | TSM-002 executable-confirmed; TSD-003 resolved as contextual resolver rule. |
| DoorStateService | 301-2-15 | 2.1 | Common V1.0 + Enums V1.0 | first pass completed | DRS findings retained. |
| TicketValidationService | 301-2-16 | 2.1, 2.2, 2.3, 2.4 | version-specific; V2.3 doc -> XSD V2.2; V2.4 candidate | first pass completed | TVS findings retained. |
| HTMLDisplayService | 301-2-17 | 2.1, 2.2, 2.2a | non-XSD HTTP/discovery profile | first pass + RV-001/RV-002 deterministic PASS | real discovery/fetch remains in block 26. |
| SystemMonitoringService | 301-2-18 | 2.2 | Common/Enums V2.2 | first pass completed | SMS-001 resolved by block 23. |
| AnalogRadioService | 301-2-19 | 2.4 | PR #27 candidate -> Common V2.3 -> Enums V2.2 | ARA-003 executable-confirmed candidate-only | run 33111831627 proves 0:1 Transmitter behavior. |
| Legacy SystemManagement/SystemDocumentation | historical 301-2 base | V1.0 XSD lineage | SystemManagement self-contained V1.0; SystemDocumentation V1.0 type-XSD + root map | integrated; legacy root adapter compiled | no duplicate aggregate mirror. |
| Network infrastructure | 301-3 | 02-2020 | non-XSD physical/network profile + discovery runtime context | first pass + RV-002 deterministic discovery PASS | real network/multicast/inventory checks remain in block 26. |
| Cross-service subscription modelling | 301-2 conventions + services | historical | generic Common structures + service-specific exceptions + operation-manifest layer | first pass completed | TSD-003 confirms response-context resolver requirement; live callbacks/heartbeat remain in block 26. |
| Executable XSD validation matrix | cross-version | historical/current/candidate | compile + legacy roots + targeted samples | **planned deterministic phase completed** | EV-001/002/101/102/103/104/105 completed. |
| Runtime/protocol validation matrix | cross-version | HTTP/DNS-SD/SNTP/RTSP/RTP | VDV rules + external standards + diagnostics | **planned deterministic phase completed** | RV-001/002/003/004 completed. |
| Live/integration validation | cross-version | real implementations | network/device/provider/capture evidence | **open by environment** | canonical backlog: `26_live_integration_validation_backlog.md`. |

## Completed executable XSD evidence

```text
EV-001 + EV-002 / run 33109011670
46 root XSDs compile PASS; DMS V2.4 samples 6/6 PASS; legacy V1.0 root adapters PASS

EV-101 / run 33109367265
PCS-001 dependency/value-set mismatch executable-confirmed

EV-102 / run 33109768872
CE-018 XSD 0:* behavior executable-confirmed across Common V1.0-V2.4

EV-103 / run 33111119723
VLS-002, VRS-003, VDS-002/003/004 executable-confirmed

EV-104 / run 33111644388
TSM-002 executable-confirmed; TSD-003 resolved as contextual resolver requirement

EV-105 / run 33111831627
ARA-003 candidate-profile 0:1 Transmitter behavior executable-confirmed
```

## Completed deterministic runtime/protocol evidence

```text
RV-001 / run 33112730418
HTTP/XML + Content-Type classifier PASS

RV-002 / run 33119080288
DNS-SD + VDV discovery/HDS classifier PASS

RV-003 / run 33119337775
TimeService V1.0 + RFC 4330 SNTP classifier PASS

RV-004 / run 33119694991
Video rtspURI + RTSP version boundary + RTP header classifier PASS
```

The validation workflow is `workflow_dispatch` only and does not run on normal audit pushes.

## Current priority

```text
26_live_integration_validation_backlog.md              completed as consolidated open-work inventory
central audit control-document consolidation           ACTIVE
SDK manifest / resolver implementation baseline        NEXT AFTER CONSOLIDATION
```

Central continuation authority after consolidation should be:

```text
1. branch HEAD
2. AUDIT_SCOPE_MATRIX.md
3. AUDIT_HANDOFF.md
4. findings.md
5. validation_backlog.md
6. detailed per-service / EV / RV evidence documents as referenced
```
