# Upstream PR review package: V2.4 schema dependencies and DMS V2.4

Status: preparation material only. This document belongs to the development integration branch and is not intended to be part of an upstream schema-only pull request.

## Purpose

Prepare two small and reviewable upstream pull-request candidates for `VDVde/VDV301`.

The goal is to avoid a large mixed contribution and to separate dependency cleanup from the actual `DeviceManagementService V2.4` addition.

## Branches in this fork

### Candidate 1: V2.4 schema dependencies

Branch:

```text
candidate/v2.4-schema-dependencies
```

Files changed against current upstream `master`:

```text
+ IBIS-IP_common_V2.4.xsd
+ IBIS-IP_Enumerations_V2.4.xsd
~ IBIS-IP_TicketValidationService_V2.4.xsd
```

The `TicketValidationService` change is limited to the enumeration include consistency:

```xml
<xs:include schemaLocation="IBIS-IP_Enumerations_V2.2.xsd"/>
```

to:

```xml
<xs:include schemaLocation="IBIS-IP_Enumerations_V2.4.xsd"/>
```

Rationale:

- The existing official `IBIS-IP_TicketValidationService_V2.4.xsd` already refers to `IBIS-IP_common_V2.4.xsd`.
- `IBIS-IP_common_V2.4.xsd` is not present in the official repository baseline used here.
- Previous upstream review activity around V2.4 service files suggested using V2.4 common/enumeration dependencies for V2.4 service schemas.
- This candidate provides the missing V2.4 common/enumeration dependency layer before introducing DMS V2.4.

Scope limits:

- No DMS V2.4 file in this candidate.
- No unrelated service additions.
- No formatting cleanup beyond the affected files.

Suggested PR title:

```text
Add V2.4 common/enumeration schema dependencies
```

Suggested PR body:

```text
This PR adds the V2.4 common and enumeration schema files and aligns the existing TicketValidationService V2.4 schema to use V2.4 enumerations.

The current TicketValidationService V2.4 schema already references IBIS-IP_common_V2.4.xsd. This PR adds the missing V2.4 dependency files and keeps the V2.4 service schema family consistent.

Changes:
- add IBIS-IP_common_V2.4.xsd
- add IBIS-IP_Enumerations_V2.4.xsd
- update IBIS-IP_TicketValidationService_V2.4.xsd to include IBIS-IP_Enumerations_V2.4.xsd

No DeviceManagementService V2.4 changes are included in this PR.
```

Review questions for maintainers:

```text
- Should V2.4 service schemas consistently include common V2.4 and enumerations V2.4?
- Should TicketValidationService V2.4 be aligned to enumerations V2.4 in this PR or handled separately?
```

## Candidate 2: DeviceManagementService V2.4

Branch:

```text
candidate/dms-v2.4-xsd
```

Files changed against current upstream `master`:

```text
+ IBIS-IP_common_V2.4.xsd
+ IBIS-IP_Enumerations_V2.4.xsd
~ IBIS-IP_TicketValidationService_V2.4.xsd
+ IBIS-IP_DeviceManagementService_V2.4.xsd
```

Preferred upstream strategy:

- Submit Candidate 1 first.
- Submit Candidate 2 afterwards, rebased on the merged Candidate 1 result.

Reason:

- The DMS V2.4 schema should use V2.4 common/enumeration dependencies.
- Keeping the dependency change separate makes DMS V2.4 easier to review.

## DMS V2.4 derivation source

The DMS V2.4 candidate is derived from:

```text
official baseline: IBIS-IP_DeviceManagementService_V2.2.xsd
publication: VDV 301-2-0 DeviceManagementService V2.4, 01/2023
```

Public fork files were used only as comparison material, not as normative source.

## DMS V2.4 change matrix

### 1. Includes

Changed from:

```xml
<xs:include schemaLocation="IBIS-IP_common_V2.2.xsd"/>
<xs:include schemaLocation="IBIS-IP_Enumerations_V2.2.xsd"/>
```

to:

```xml
<xs:include schemaLocation="IBIS-IP_common_V2.4.xsd"/>
<xs:include schemaLocation="IBIS-IP_Enumerations_V2.4.xsd"/>
```

Reason:

- DMS V2.4 should use the same V2.4 schema-family dependency level as other V2.4 service schemas.

### 2. Device error messages

Changed only inside:

```text
DeviceManagementService.GetDeviceErrorMessagesResponseDataStructure
```

from:

```xml
<xs:element name="ErrorMessage" type="MessageStructure" minOccurs="10" maxOccurs="unbounded">
```

to:

```xml
<xs:element name="ErrorMessage" type="MessageStructure" minOccurs="0" maxOccurs="unbounded">
```

Reason:

- DMS V2.4 documents `ErrorMessage` as `0:*` for device error messages.

### 3. Subdevice error messages

Changed only inside:

```text
SubdeviceErrorMessagesStructure
```

from:

```xml
<xs:element name="ErrorMessage" type="MessageStructure" minOccurs="10" maxOccurs="unbounded">
```

to:

```xml
<xs:element name="ErrorMessage" type="MessageStructure" minOccurs="0" maxOccurs="unbounded">
```

Reason:

- DMS V2.4 documents `ErrorMessage` as `0:*` for subdevice error messages.

### 4. DeviceStatusStructure

Changed only inside:

```text
DeviceStatusStructure
```

from mandatory `DeviceStatusImpact` and `DeviceStatusPriority` to optional elements:

```xml
<xs:element name="DeviceStatusImpact" type="DeviceStateEnumeration" minOccurs="0"> </xs:element>
<xs:element name="DeviceStatusPriority" type="IBIS-IP.int" minOccurs="0"></xs:element>
```

Unchanged mandatory elements:

```xml
<xs:element name="DeviceStatusName" type="IBIS-IP.string"/>
<xs:element name="DeviceStatusFlag" type="IBIS-IP.boolean"/>
```

Reason:

- DMS V2.4 documents `DeviceStatusImpact` and `DeviceStatusPriority` as `0:1`, while `DeviceStatusName` and `DeviceStatusFlag` remain `1:1`.

### 5. InstallUpdateRequestStructure

Changed only inside:

```text
DeviceManagementService.InstallUpdateRequestStructure
```

The following request fields are made optional:

```xml
<xs:element name="UpdateID" type="IBIS-IP.NMTOKEN" minOccurs="0">
<xs:element name="UpdateTimestamp" type="IBIS-IP.dateTime" minOccurs="0">
<xs:element name="UpdateURL" type="IBIS-IP.anyURI" minOccurs="0">
```

Already optional in the baseline and unchanged:

```xml
<xs:element name="UpdateFileChecksum" type="ChecksumStructure" minOccurs="0">
<xs:element name="UpdateFileSize" type="IBIS-IP.unsignedLong" minOccurs="0">
```

Reason:

- DMS V2.4 adapts `InstallUpdateRequest` for cases where update files can be retrieved from a preconfigured storage location.

Important scope protection:

- `UpdateStateData.UpdateTimestamp` remains mandatory.
- `UpdateHistoryEntry.UpdateTimestamp` remains mandatory.
- `UpdateHistoryEntry.UpdateURL` remains mandatory.
- `RetrieveUpdateStateRequest.UpdateID` remains mandatory.
- `FinalizeUpdateRequest.UpdateID` remains mandatory.

## Validation checklist before upstream PR

The DMS branch must pass these checks before opening a PR:

```text
[ ] complete selected XSD pool compiles
[ ] DMS V2.4 schema compiles with common V2.4 / enumerations V2.4
[ ] zero device ErrorMessage entries are valid
[ ] zero subdevice ErrorMessage entries are valid
[ ] DeviceStatus without Impact/Priority is valid
[ ] DeviceStatus without DeviceStatusFlag is invalid
[ ] InstallUpdateRequest without UpdateURL is valid
[ ] UpdateStateData without UpdateTimestamp is invalid
[ ] no unrelated DMS structures changed
[ ] no broad formatting-only rewrite
```

## Suggested DMS PR title

```text
Add DeviceManagementService V2.4 schema
```

## Suggested DMS PR body

```text
This PR adds IBIS-IP_DeviceManagementService_V2.4.xsd derived from the existing official DeviceManagementService V2.2 schema and the documented changes in VDV 301-2-0 DeviceManagementService V2.4 (01/2023).

The changes are limited to the DMS V2.4 corrections documented in the publication:
- device and subdevice ErrorMessage occurrences changed from mandatory 10 to optional;
- DeviceStatusImpact and DeviceStatusPriority made optional;
- InstallUpdateRequest fields adapted for preconfigured update storage locations.

The schema uses the V2.4 common/enumeration dependency level:
- IBIS-IP_common_V2.4.xsd
- IBIS-IP_Enumerations_V2.4.xsd

Public fork files were used only as comparison material, not as normative source.
```

## Suggested reviewer note

```text
I intentionally kept the DMS changes narrow. The only semantic DMS changes are the documented V2.4 changes around error message cardinalities, optional DeviceStatus fields, and optional InstallUpdateRequest fields.

Please especially review whether the V2.4 dependency level should be common V2.4 plus enumerations V2.4, matching the direction already visible in prior V2.4 service schema reviews.
```

## Current recommendation

Proceed with this order:

```text
1. Validate candidate/v2.4-schema-dependencies.
2. Open or prepare PR for candidate/v2.4-schema-dependencies.
3. After dependency direction is accepted, rebase/squash candidate/dms-v2.4-xsd.
4. Validate DMS V2.4 again.
5. Open or prepare DMS V2.4 PR.
```

Do not open either PR before the validation result is documented.
