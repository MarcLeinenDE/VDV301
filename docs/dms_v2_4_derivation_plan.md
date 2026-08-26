# DMS V2.4 XSD derivation plan

Status: preparation note for a possible upstream pull request. This document is part of the development integration work and is not an official VDV release file.

## Goal

Prepare a conservative `IBIS-IP_DeviceManagementService_V2.4.xsd` candidate for later review.

The candidate must be derived from:

- official baseline XSD: `VDVde/VDV301` `IBIS-IP_DeviceManagementService_V2.2.xsd`, baseline commit `14880bb33beec5c5dffe96315b730bd6c094a585`;
- official publication: VDV 301-2-0 DeviceManagementService V2.4, 01/2023;
- public fork files only as comparison material, not as normative source.

## Non-goals

The PR candidate must not include unrelated cleanups, formatting changes, schema reordering, or undocumented structure changes.

`dev/schema-integration` may contain broader public candidate material. The later upstream PR branch must stay smaller and easier to review.

## Normative DMS V2.4 change matrix

### 1. Device error messages

Documented V2.4 target:

- `DeviceManagementService.GetDeviceErrorMessagesResponseData / ErrorMessage`: `0:*`.
- Existing V2.2 XSD still uses mandatory `minOccurs="10"`.

Planned XSD change:

```xml
<xs:element name="ErrorMessage" type="MessageStructure" minOccurs="0" maxOccurs="unbounded">
```

Scope limitation:

- Only the `GetDeviceErrorMessagesResponseDataStructure` `ErrorMessage` particle is changed.

### 2. Subdevice error messages

Documented V2.4 target:

- `DeviceManagementService.SubdeviceErrorMessages / ErrorMessage`: `0:*`.
- Existing V2.2 XSD still uses mandatory `minOccurs="10"`.

Planned XSD change:

```xml
<xs:element name="ErrorMessage" type="MessageStructure" minOccurs="0" maxOccurs="unbounded">
```

Scope limitation:

- Only the `SubdeviceErrorMessagesStructure` `ErrorMessage` particle is changed.

### 3. DeviceStatusStructure

Documented V2.4 target:

- `DeviceStatusName`: `1:1`.
- `DeviceStatusFlag`: `1:1`.
- `DeviceStatusImpact`: `0:1`.
- `DeviceStatusPriority`: `0:1`.

Planned XSD change:

```xml
<xs:element name="DeviceStatusImpact" type="DeviceStateEnumeration" minOccurs="0"> </xs:element>
<xs:element name="DeviceStatusPriority" type="IBIS-IP.int" minOccurs="0"></xs:element>
```

Scope limitation:

- `DeviceStatusName` and `DeviceStatusFlag` remain mandatory.

### 4. InstallUpdateRequestStructure

Documented V2.4 target:

- `UpdateID`: `0:1`.
- `UpdateTimestamp`: `0:1`.
- `UpdateURL`: `0:1`.
- `UpdateFileChecksum`: `0:1`.
- `UpdateFileSize`: `0:1`.

Planned XSD change:

```xml
<xs:element name="UpdateID" type="IBIS-IP.NMTOKEN" minOccurs="0">
<xs:element name="UpdateTimestamp" type="IBIS-IP.dateTime" minOccurs="0">
<xs:element name="UpdateURL" type="IBIS-IP.anyURI" minOccurs="0">
```

`UpdateFileChecksum` and `UpdateFileSize` are already optional in the V2.2 XSD and should remain unchanged.

Scope limitation:

- Only the particles inside `DeviceManagementService.InstallUpdateRequestStructure` are changed.
- Similar names inside `UpdateStateDataStructure`, `UpdateHistoryEntryStructure`, `RetrieveUpdateStateRequestStructure`, and `FinalizeUpdateRequestStructure` remain mandatory according to their own tables.

### 5. Include version decision

This is the open review point before committing a PR candidate.

Option A: DMS-only PR with existing official dependencies:

```xml
<xs:include schemaLocation="IBIS-IP_common_V2.3.xsd"/>
<xs:include schemaLocation="IBIS-IP_Enumerations_V2.2.xsd"/>
```

Pros:

- very small PR;
- compiles against the current official repository contents.

Cons:

- less consistent with other V2.4 service schema candidates;
- does not address the already existing official `TicketValidationService V2.4` dependency on missing `IBIS-IP_common_V2.4.xsd`.

Option B: V2.4 schema-pool completion PR:

```xml
<xs:include schemaLocation="IBIS-IP_common_V2.4.xsd"/>
<xs:include schemaLocation="IBIS-IP_Enumerations_V2.4.xsd"/>
```

This requires at least these additional files/changes in the same PR or in a preceding dependency PR:

- add `IBIS-IP_common_V2.4.xsd`;
- add `IBIS-IP_Enumerations_V2.4.xsd`;
- align `IBIS-IP_TicketValidationService_V2.4.xsd` to avoid mixed V2.4 common with V2.2 enumerations.

Pros:

- consistent V2.4 schema family;
- can remove the known local compile gap around `TicketValidationService V2.4` and missing `common_V2.4`.

Cons:

- broader PR;
- requires a separate verification pass for Common/Enumerations V2.4 before submitting upstream.

Current recommendation:

- Do not open an upstream PR before this include-version decision is explicitly resolved.
- For internal derivation, build and test both candidate variants if needed.

## Validation checklist before upstream PR

The final PR branch must pass at least these checks:

1. XSD compile check for the complete selected schema pool.
2. Positive XML check: DeviceErrorMessages with zero `ErrorMessage` entries is accepted by DMS V2.4.
3. Positive XML check: SubdeviceErrorMessages with zero `ErrorMessage` entries is accepted by DMS V2.4.
4. Positive XML check: DeviceStatus with only `DeviceStatusName` and `DeviceStatusFlag` is accepted by DMS V2.4.
5. Negative XML check: DeviceStatus without `DeviceStatusFlag` remains invalid.
6. Positive XML check: InstallUpdateRequest without `UpdateURL` is accepted by DMS V2.4.
7. Negative scope check: `UpdateStateData.UpdateTimestamp`, `UpdateHistoryEntry.UpdateURL`, and similar non-request fields remain mandatory.
8. Diff review confirms no formatting-only rewrite of the original DMS XSD.

## PR text skeleton

```text
Add IBIS-IP_DeviceManagementService_V2.4.xsd derived from the existing official DMS V2.2 schema and the documented changes in VDV 301-2-0 DeviceManagementService V2.4 (01/2023).

The changes are limited to the DMS V2.4 corrections documented in the publication:
- error message occurrences reduced from mandatory 10 to optional;
- DeviceStatusImpact and DeviceStatusPriority made optional;
- InstallUpdateRequest fields adapted for pre-defined update storage locations.

Public fork files were used only as comparison material, not as normative source.
```
