# PDF/XSD audit scope matrix

Status: semantic/provenance first pass and planned XSD executable-evidence phase completed; deterministic runtime/protocol evidence completed through RV-003; RV-004 is next.

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
Protocol/runtime checks must distinguish VDV-specific requirements, incorporated external standards, and diagnostic heuristics.
EV-* identifiers are reserved for executable XML/XSD evidence; RV-* identifiers are reserved for runtime/protocol evidence.
```

| Area | VDV part | Published PDF versions | Relevant XSD/routing state | Audit status | Notes |
|---|---|---|---|---|---|
| Base / General Conventions | 301-2 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | deduplicated V1.0 service set; legacy aggregate roots mapped in `schema_profiles` | first pass completed + storage refinement | BG-001/BG-002 refined; HTTP/discovery deterministic runtime rules tested in RV-001/RV-002. |
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
| TimeService | 301-2-10 | 1.0 | non-XSD SNTP/DNS-SD | first pass completed + RV-003 deterministic profile PASS | run 33119337775; live DNS-SD/SNTP exchange and clock diagnostics remain pending. |
| VideoLiveService | 301-2-11 | 1.0, 2.0 | V1.0 strict-XSD unresolved; V2.0 official | VLS-002 executable-confirmed; RV-004 next | run 33111119723; RTSP/RTP deterministic boundary is next, live media remains later. |
| VideoRecordingService | 301-2-12 | 1.0, 2.0, 2.4 | V1.0 unresolved; V2.0 official; V2.4 candidate | VRS-003 executable-confirmed | run 33111119723; V2.4 control candidate-only. |
| VideoDisplayService | 301-2-13 | 1.0, 2.0 | V1.0 unresolved; V2.0 official | VDS-002/003/004 executable-confirmed | run 33111119723. |
| TrainSet services | 301-2-14 | 2.1, 2.2 | three separately routed service families | EV-104 completed | TSM-002 executable-confirmed; TSD-003 resolved as contextual resolver rule. |
| DoorStateService | 301-2-15 | 2.1 | Common V1.0 + Enums V1.0 | first pass completed | DRS findings retained. |
| TicketValidationService | 301-2-16 | 2.1, 2.2, 2.3, 2.4 | version-specific; V2.3 doc -> XSD V2.2; V2.4 candidate | first pass completed | TVS findings retained. |
| HTMLDisplayService | 301-2-17 | 2.1, 2.2, 2.2a | non-XSD HTTP/discovery profile | first pass completed + RV-001/RV-002 deterministic PASS | HDS version-specific endpoint/discovery rules executable-tested; live fetch/discovery remains pending. |
| SystemMonitoringService | 301-2-18 | 2.2 | Common/Enums V2.2 | first pass completed | SMS-001 resolved by block 23. |
| AnalogRadioService | 301-2-19 | 2.4 | PR #27 candidate -> Common V2.3 -> Enums V2.2 | ARA-003 executable-confirmed candidate-only | run 33111831627 proves 0:1 Transmitter behavior. |
| Legacy SystemManagement/SystemDocumentation | historical 301-2 base | V1.0 XSD lineage | SystemManagement self-contained V1.0; SystemDocumentation V1.0 type-XSD + root map | integrated; legacy root adapter compiled | no duplicate aggregate mirror. |
| Network infrastructure | 301-3 | 02-2020 | non-XSD physical/network profile + discovery runtime context | first pass completed + RV-002 deterministic discovery PASS | live PTR/mDNS/endpoint/multicast/network checks remain pending. |
| Cross-service subscription modelling | 301-2 conventions + services | historical | generic Common structures + service-specific exceptions + operation-manifest layer | first pass completed | TSD-003 confirms response-context resolver requirement; live callback/heartbeat trace remains pending. |
| Executable XSD validation matrix | cross-version | historical/current/candidate | compile + legacy roots + targeted samples | **planned phase completed** | EV-001/002/101/102/103/104/105 completed. |
| Runtime/protocol validation matrix | cross-version | HTTP/DNS-SD/SNTP/RTSP/RTP | VDV rules + external standards + diagnostics | **RV-001/RV-002/RV-003 completed; RV-004 next** | deterministic profile evidence only; live integration remains separately tracked. |

## Completed executable XSD evidence

```text
Baseline / EV-001 + EV-002
run 33109011670
46 root XSDs compile PASS
DMS V2.4 samples 6/6 PASS
legacy V1.0 root adapters PASS

EV-101 / PCS-001
run 33109367265
exact PCS V2.1 route rejects OperationNotSupported; Enums V2.1 control accepts it

EV-102 / CE-018
run 33109768872
Common V1.0-V2.4 all accept empty and one-item ServiceIdentificationWithStateList

EV-103 / video compositors
run 33111119723
VLS-002, VRS-003, VDS-002/003/004 executable-confirmed

EV-104 / TrainSet
run 33111644388
TSM-002 executable-confirmed
TSD-003 contextual dual typing confirmed and resolved as resolver requirement

EV-105 / AnalogRadio candidate
run 33111831627
ARA-003 candidate-profile 0:1 Transmitter behavior executable-confirmed
```

## Completed deterministic runtime/protocol evidence

```text
RV-001 / HTTP/XML + Content-Type classifier
run 33112730418
PASS
VDV GET/POST + HTTP/1.1 version scope and RFC 9110/RFC 7303 media-type classification confirmed

RV-002 / DNS-SD + VDV discovery classifier
run 33119080288
PASS
RFC 6763 record coherence, VDV V2.2+ TXT/protocol rules and HDS V2.1/V2.2/V2.2a endpoint profiles confirmed

RV-003 / TimeService V1.0 + RFC 4330 SNTP classifier
run 33119337775
PASS
VDV TimeService discovery metadata, SNTP request/reply profile checks and no-XML-operation routing confirmed
```

The validation workflow is `workflow_dispatch` only and does not run on normal audit pushes.

## Current priority

```text
Block 25 - runtime/protocol validation profiles
25a authority/source matrix                completed
25b / RV-001 HTTP/XML + Content-Type       completed
25c / RV-002 DNS-SD/service discovery      completed
25d / RV-003 TimeService/SNTP              completed
25e / RV-004 Video RTSP/RTP boundary       NEXT
```

Rule for block 25:

```text
Every runtime check must identify its authority source:
- VDV-specific requirement
- external normative standard incorporated or relied upon by VDV
- diagnostic best practice / heuristic
```
