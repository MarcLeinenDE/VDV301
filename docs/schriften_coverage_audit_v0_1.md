# VDV301 writings coverage audit v0.1

Status: preliminary coverage audit for `dev/schema-integration`.

This document compares the schema files currently present in the superbranch with the public VDV publication index for VDV 301 writings from V1.0 to V2.4.

Important limits:

- This is a coverage and provenance audit, not yet a full table-by-table semantic validation of every PDF against every XSD.
- Several files in this branch come from open upstream PRs or public fork candidates. They must not be labelled as official until merged by `VDVde/VDV301` or released by VDV.
- The local XSD compile / sample-validation pass is still pending.

Source index used:

- VDV IP-KOM-OEV / VDV 301 publication page, public document list.
- `dev/schema-integration` tree at commit `add9ad610c9cc2ca51f3a457316fea62df94aa59` as the starting point of this audit.

## 1. High-level result

The superbranch is useful as a working schema set because it combines:

- official repository files already present in upstream master;
- open upstream PR content;
- the DMS V2.4 draft PR candidate from this fork;
- local review and validation helper material.

It is not yet a complete, formally verified representation of all VDV 301 writings from V1.0 to V2.4.

## 2. Coverage matrix

| VDV writing / service area | Public versions visible in VDV index | Files present in superbranch | Coverage status | Notes |
|---|---:|---|---|---|
| Common structures / enumerations | 1.0, 2.0, 2.1, 2.2, 2.3, 2.4 | `common` 1.0/2.0/2.1/2.2/2.3/2.4; `Enumerations` 1.0/2.0/2.1/2.2/2.4 | Mostly covered | No `IBIS-IP_Enumerations_V2.3.xsd` in branch. This may be intentional if V2.3 services still use V2.2 enumerations, but it remains an audit point. |
| General conventions | 2.2, 2.3, 2.4 | no standalone XSD expected | Documentation-only / convention layer | Needs manual rules check, especially version/include conventions and XSD precedence statements. |
| DeviceManagementService | 2.2, 2.4 visible; DMS V2.3 appears through PR/fork work | 2.2, 2.3, 2.4 | Covered as working set | DMS V2.4 is the local draft PR candidate, not official yet. DMS V2.3 comes from upstream PR/fork content. |
| Base services bundle | 1.0, 2.0, 2.1 | no explicit SystemManagement/SystemDocumentation schema files identified in branch | Gap / needs clarification | VDV index lists a base-services document bundle for DMS/SystemManagement/SystemDocumentation. Need verify whether all parts require own XSD files or are documentation-only/no schema. |
| BeaconLocationService | 1.0 | V1.0 | Covered by file presence | Needs PDF-vs-XSD semantic validation. |
| CustomerInformationService | 1.1, 2.0, 2.2, 2.3 visible; V2.4 appears from PR/fork work | 2.3, 2.4 | Partial | Missing 1.1/2.0/2.2 XSDs in branch; V2.4 is candidate material, not visibly listed as a public VDV writing on the current index page. |
| DistanceLocationService | 1.0 | V1.0 | Covered by file presence | Needs PDF-vs-XSD semantic validation. |
| GNSSLocationService | 1.0 | V1.0 | Covered by file presence | Needs PDF-vs-XSD semantic validation. |
| JourneyInformationService | 1.0 | V1.0 | Covered by file presence | Needs PDF-vs-XSD semantic validation. |
| NetworkLocationService | 1.0 | V1.0 | Covered by file presence | Needs PDF-vs-XSD semantic validation. |
| PassengerCountingService | 1.0, 2.1 | V2.1 | Partial | V1.0 XSD not present. |
| TicketingService / TicketInformationService | 1.0 | `IBIS-IP_TicketInformationService_V1.0.xsd` | Likely covered, naming audit needed | Public index says TicketingService; branch file says TicketInformationService. Confirm document terminology vs file naming. |
| TimeService | 1.0 | no dedicated file identified | Needs clarification | TimeService may be simple/documentation-only or covered elsewhere; verify PDF. |
| VideoLiveService | 1.0, 2.0 | V2.0 | Partial | V1.0 XSD not present. |
| VideoRecordingService | 1.0, 2.0, 2.4 | V2.0, V2.4 | Partial | V1.0 XSD not present; V2.4 comes from open PR/fork material. |
| VideoDisplayService | 1.0, 2.0 | V2.0 | Partial | V1.0 XSD not present. |
| TrainSetInformation/Management/Data services | 2.1, 2.2 | V2.2 files | Partial | V2.1 XSD files not present. |
| DoorStateService | 2.1 | V2.1 | Covered by file presence | Needs PDF-vs-XSD semantic validation. |
| TicketValidationService | 2.1, 2.2, 2.3, 2.4 | V2.2, V2.3, V2.4 | Partial | V2.1 not present; V2.4 include alignment is candidate/open-PR-derived. |
| HTMLDisplayService | 2.1, 2.2, 2.2a | no dedicated XSD identified | Likely documentation-only / no own XML schema | Need confirm from HTMLDisplayService PDFs. Previous working assumption: no own service XSD required. |
| SystemMonitoringService | 2.2 | V2.2 | Covered by file presence | Needs PDF-vs-XSD semantic validation. |
| AnalogRadioService | 2.4 | V2.4 | Covered as candidate file | Open PR #27 source; include level must be validated in final schema pool. |

## 3. Immediate findings

### 3.1 Superbranch is not complete for historical V1.0/V2.0/V2.1 variants

The branch focuses on the useful current working set plus selected historic files, not on preserving every historical XSD version listed by the VDV publication index.

Missing or unclear historical schema variants include at least:

```text
CustomerInformationService V1.1 / V2.0 / V2.2
PassengerCountingService V1.0
VideoLiveService V1.0
VideoRecordingService V1.0
VideoDisplayService V1.0
TrainSet* V2.1
TicketValidationService V2.1
Base-services SystemManagement/SystemDocumentation schema representation
TimeService V1.0 schema representation
HTMLDisplayService schema representation
Enumerations V2.3, if such a separate schema is expected
```

### 3.2 Current/current-ish V2.2-V2.4 work is much better covered

For tool development, the branch covers many of the practical newer service areas:

```text
common V2.4
Enumerations V2.4
DeviceManagementService V2.4
TicketValidationService V2.4
CustomerInformationService V2.4 candidate
AnalogRadioService V2.4 candidate
VideoRecordingService V2.4 candidate
SystemMonitoringService V2.2
TrainSet* V2.2
DoorStateService V2.1
PassengerCountingService V2.1
```

But several of these are candidate/integration state, not official VDV release state.

### 3.3 The branch now also includes PR #30's isolated common V2.3 fix

`IBIS-IP_common_V2.3.xsd` contains the `InternationalTextType` type fix from PR #30:

```xml
<xs:element name="Value" type="IBIS-IP.string"/>
<xs:element name="Language" type="IBIS-IP.language"/>
```

This is intentionally integrated for the working schema set.

## 4. Next audit steps

### Step A: document acquisition

Download or otherwise make available all public VDV 301 PDFs listed in the VDV index for V1.0 to V2.4, at least the service-specific documents that have or may have XSD counterparts.

### Step B: extract service/version inventory from PDFs

For each PDF:

- service name;
- version;
- operations;
- request/response structures;
- shared structures/enumerations;
- version-history change notes;
- whether an own service XSD is expected.

### Step C: XSD semantic diff

For each XSD in branch:

- check include versions;
- check operation names;
- check request/response element names;
- check cardinalities;
- check data types;
- check enumerations;
- check known documented version changes.

### Step D: schema-pool compile and sample validation

Run local validation for the selected pool:

- compile all included XSDs;
- fail on unresolved includes;
- sample-valid / sample-invalid checks for DMS V2.4;
- later expand sample cases for CIS, TVS, PCS, Video, TrainSet, etc.

## 5. Current recommendation for the VDV301 Tool

Use `dev/schema-integration` as an integrated working schema source only with provenance labelling:

```text
Source set: MarcLeinenDE/VDV301 dev/schema-integration
Status: integrated working schema set based on VDVde master + open PR/candidate material
Not an official VDV release
```

Do not label the whole set as VDV-official until the relevant files are merged/released upstream.
