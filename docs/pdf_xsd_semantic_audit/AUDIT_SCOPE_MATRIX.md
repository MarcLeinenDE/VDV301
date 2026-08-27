# PDF/XSD audit scope matrix

Status: initial control matrix.

Purpose:

```text
Prevent gaps in the full VDV301 PDF-vs-XSD audit by tracking every public VDV301 service/scope and every relevant published PDF version against the XSD files observed in dev/schema-integration.
```

Source basis:

```text
Official VDV IP-KOM-ÖV publication index, current branch tree of MarcLeinenDE/VDV301 dev/schema-integration, and already-created audit files.
```

Important source note:

```text
The official VDV page lists the public PDF writings. The branch tree lists the XSD files currently available in the integration branch. A mismatch between published PDF versions and branch XSD versions is not automatically a defect; it is a routing signal for the audit.
```

Authority rule:

```text
Validation follows XSD.
PDF differences are retained as provider-facing explanation notes.
No schema changes are made during audit work.
```

Generated CSV:

```text
docs/pdf_xsd_semantic_audit/generated/audit_scope_matrix.csv
```

## Matrix overview

| Area | VDV part | Published PDF versions | XSD files observed in dev/schema-integration | Audit status | Notes |
|---|---|---|---|---|---|
| Base / General Conventions | 301-2 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | no single service XSD | pending | General conventions V2.2-V2.4 provide cross-service rules; XSD precedence already documented. |
| Common Data Structures and Enumerations | 301-2-1 | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | common V1.0,V2.0,V2.1,V2.2,V2.3,V2.4; Enumerations V1.0,V2.0,V2.1,V2.2,V2.4 | partial | V2.4 first pass mostly done; V1.0-V2.3 historical audit is the next foundation block. |
| DeviceManagementService | 301-2-0 | 2.0, 2.1, 2.2, 2.4 | DMS V2.2; DMS V2.3 integration/fork comparison; DMS V2.4 candidate | partial | V2.4 semantic and V2.2/V2.3/V2.4 history first pass completed. |
| BeaconLocationService | 301-2-2 | 1.0 | BeaconLocationService V1.0 | pending | Service audit not started. |
| CustomerInformationService | 301-2-3 | 1.1, 2.0, 2.2, 2.3 | CIS V2.3; CIS V2.4 candidate/integration | pending | Official page lists PDFs through V2.3; V2.4 XSD candidate needs provenance review. |
| DistanceLocationService | 301-2-4 | 1.0 | DistanceLocationService V1.0 | pending | Service audit not started. |
| GNSSLocationService | 301-2-5 | 1.0 | GNSSLocationService V1.0 | pending | Service audit not started. |
| JourneyInformationService | 301-2-6 | 1.0 | JourneyInformationService V1.0 | pending | Route deferred from Common/Enums routes here. |
| NetworkLocationService | 301-2-7 | 1.0 | NetworkLocationService V1.0 | pending | NetworkLocationPoint deferred from Common/Enums routes here. |
| PassengerCountingService | 301-2-8 | 1.0, 2.1 | PassengerCountingService V2.1 | pending | V1.0 XSD not observed in branch tree. |
| Ticketing / TicketInformation | 301-2-9 | 1.0 | TicketInformationService V1.0 | pending | PDF/XSD naming must be mapped: TicketingService vs TicketInformationService. |
| TimeService | 301-2-10 | 1.0 | no dedicated TimeService XSD observed | pending | Likely special/no XML-schema service; must be confirmed, not assumed. |
| VideoLiveService | 301-2-11 | 1.0, 2.0 | VideoLiveService V2.0 | pending | V1.0 XSD not observed in branch tree. |
| VideoRecordingService | 301-2-12 | 1.0, 2.0, 2.4 | VideoRecordingService V2.0,V2.4 | pending | V2.4 candidate/integration material present. |
| VideoDisplayService | 301-2-13 | 1.0, 2.0 | VideoDisplayService V2.0 | pending | V1.0 XSD not observed in branch tree. |
| TrainSet services | 301-2-14 | 2.1, 2.2 | TrainSetInformation V2.2; TrainSetManagement V2.2; TrainSetData V2.2 | pending | V2.1 XSD not observed in branch tree. |
| DoorStateService | 301-2-15 | 2.1 | DoorStateService V2.1 | pending | Service audit not started. |
| TicketValidationService | 301-2-16 | 2.1, 2.2, 2.3, 2.4 | TVS V2.2,V2.3,V2.4 | partial | V2.2/V2.3/V2.4 first pass completed; V2.1 historical coverage pending. |
| HTMLDisplayService | 301-2-17 | 2.1, 2.2, 2.2a | no dedicated HTMLDisplayService XSD observed | pending | Likely non-XSD/HTTP-HTML service; must be documented as non-gap if confirmed. |
| SystemMonitoringService | 301-2-18 | 2.2 | SystemMonitoringService V2.2 | pending | Service audit not started. |
| AnalogRadioService | 301-2-19 | 2.4 | AnalogRadioService V2.4 | pending | V2.4 candidate/integration material present. |
| Network infrastructure | 301-3 | 02-2020 | not applicable / non-service | pending | Context document; not a service XSD target but may inform DNS-SD/HTTP rules. |

## Immediate audit decision

The next stable sequence is:

```text
1. Use this scope matrix as the master coverage checklist.
2. Close Common/Enums historical audit V1.0 -> V2.4, because all services depend on these shared types.
3. Then continue service waves: DMS/TVS/CIS first, then location/Journey/PCS/Ticketing, then video/train/door/system/analog/special services.
```

## Gap handling rules

If a PDF version has no matching XSD in the branch:

```text
Do not assume the XSD is missing incorrectly.
Classify as one of: older file absent from branch, no dedicated XSD service, renamed XSD, candidate/fork provenance, or unresolved.
```

If an XSD version has no matching public PDF on the VDV page:

```text
Do not treat it as official by default.
Mark as candidate/integration/fork material until provenance is established.
```

## Current priority after this matrix

```text
Common/Enums historical audit V1.0 -> V2.4.
```

Reason:

```text
Common/Enums is reused by nearly every service. Historical closure here reduces duplicate work and prevents service-level misclassification of shared-type findings.
```
