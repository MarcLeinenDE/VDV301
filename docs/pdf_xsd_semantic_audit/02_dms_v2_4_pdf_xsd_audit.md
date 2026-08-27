# DeviceManagementService V2.4 - PDF/XSD semantic audit

Status: started, first pass completed for the documented V2.4 technical correction scope.

Scope:

```text
VDV 301-2-0 DeviceManagementService V2.4
IBIS-IP_DeviceManagementService_V2.4.xsd in dev/schema-integration
```

Authority rule:

```text
Validation follows XSD.
PDF differences are retained as provider-facing explanation notes.
No schema change is made during this audit pass.
```

Context:

```text
Common/Enums V2.4 first-pass audit is mostly complete.
Visual-only checks CE-015 / CE-017 / ZoneType casing are deferred because they require manual visual PDF confirmation.
This DMS block continues the audit with work that can be done without those visual checks.
```

## 1. Source and provenance notes

### PDF side

Source document:

```text
VDV-Schrift 301-2-0
DeviceManagementService V2.4
01/2023
```

The V2.4 version history states:

```text
Functional upgrade: none.
Technical corrections:
- error messages in GetDeviceErrorMessageResponse and GetAllSubdeviceErrorMessageResponse reduced from mandatory 10 to optional,
- DeviceManagementService.DeviceStatusStructure adapted to the XML file,
- InstallUpdate data structures adapted so devices can install update packages from pre-defined storage locations.
```

### XSD side

Schema file in this branch:

```text
IBIS-IP_DeviceManagementService_V2.4.xsd
```

Branch/provenance note:

```text
This file is candidate/integration material in dev/schema-integration and is also the basis of the clean official-facing DMS V2.4 draft PR path.
It must not be described as an official upstream VDV release until accepted or published upstream.
```

## 2. GetDeviceErrorMessagesResponseData / ErrorMessage

### PDF expectation

The PDF table for `DeviceManagementService.GetDeviceErrorMessagesResponseData` defines:

```text
TimeStamp     1:1 IBIS-IP.dateTime
ErrorMessage 0:* +Message
```

It also notes that, if available, a minimum number of 10 error messages seems useful.

### XSD observation

The DMS V2.4 candidate XSD follows the V2.4 technical correction:

```text
GetDeviceErrorMessagesResponseDataStructure:
  TimeStamp required
  ErrorMessage minOccurs="0" maxOccurs="unbounded"
```

### Finding

Status: OK.

Interpretation:

```text
The historical mandatory-minimum-10 requirement is not retained as executable XSD cardinality in V2.4.
The useful-minimum-10 wording is advisory, not a validation requirement.
```

Tool implication:

```text
0 ErrorMessage elements validate according to XSD.
Repeated ErrorMessage elements validate according to XSD.
Do not fail a payload only because it contains fewer than 10 ErrorMessage elements.
```

## 3. SubdeviceErrorMessages / ErrorMessage

### PDF expectation

The PDF table for `DeviceManagementService.SubdeviceErrorMessages` defines:

```text
SubdeviceName 1:1 IBIS-IP.string
ErrorMessage  0:* +Message
```

It also notes that, if available, a minimum number of 10 error messages seems useful.

### XSD observation

The DMS V2.4 candidate XSD follows the V2.4 technical correction:

```text
SubdeviceErrorMessagesStructure:
  SubdeviceName required
  ErrorMessage minOccurs="0" maxOccurs="unbounded"
```

### Finding

Status: OK.

Tool implication:

```text
0 ErrorMessage elements validate according to XSD.
Repeated ErrorMessage elements validate according to XSD.
The minimum-10 text is a recommendation/context note, not an XSD validation failure condition.
```

## 4. DeviceStatusStructure

### PDF expectation

The PDF table for `DeviceManagementService.DeviceStatus` defines:

```text
DeviceStatusName     1:1 IBIS-IP.string
DeviceStatusFlag     1:1 IBIS-IP.boolean
DeviceStatusImpact   0:1 DeviceStateEnumeration
DeviceStatusPriority 0:1 IBIS-IP.int
```

### XSD observation

The DMS V2.4 candidate XSD follows the PDF and the documented V2.4 correction:

```text
DeviceStatusName required
DeviceStatusFlag required
DeviceStatusImpact optional
DeviceStatusPriority optional
```

### Finding

Status: OK.

Tool implication:

```text
DeviceStatusName and DeviceStatusFlag remain mandatory.
DeviceStatusImpact and DeviceStatusPriority are optional.
A DMS status entry without impact/priority should not fail for that reason alone.
```

## 5. InstallUpdateRequestStructure

### PDF expectation

The PDF table for `DeviceManagementService.InstallUpdateRequest` defines:

```text
UpdateID           0:1 IBIS-IP.NMTOKEN
UpdateTimestamp    0:1 IBIS-IP.dateTime
UpdateURL          0:1 IBIS-IP.anyURI
UpdateFileChecksum 0:1 ChecksumStructure
UpdateFileSize     0:1 IBIS-IP.unsignedLong
```

The surrounding text explains that `UpdateURL` may be omitted when the device can retrieve the update package from a predefined storage location.

### XSD observation

The DMS V2.4 candidate XSD follows that V2.4 correction:

```text
UpdateID minOccurs="0"
UpdateTimestamp minOccurs="0"
UpdateURL minOccurs="0"
UpdateFileChecksum minOccurs="0"
UpdateFileSize minOccurs="0"
```

### Finding

Status: OK.

Tool implication:

```text
An InstallUpdateRequest without UpdateURL can be XSD-valid.
UpdateID and UpdateTimestamp are also optional in the request.
The tool should not treat missing UpdateURL as a schema failure for DMS V2.4.
```

Important boundary:

```text
This optionality is specific to InstallUpdateRequestStructure.
It must not be propagated blindly to update-state or update-history structures.
```

## 6. RetrieveUpdateState / UpdateStateData guard check

### PDF expectation

The V2.4 PDF keeps update-state identification and status fields mandatory in the update-state response path.

Checked semantic guard:

```text
Do not accidentally make UpdateStateData.UpdateTimestamp optional while implementing the InstallUpdate request correction.
```

### XSD observation

The DMS V2.4 candidate keeps the update-state response fields mandatory where required:

```text
UpdateStateData.UpdateID required
UpdateStateData.UpdateTimestamp required
UpdateStatus required
```

### Finding

Status: OK / guard passed.

Tool implication:

```text
Missing UpdateStateData.UpdateTimestamp should still fail validation if the XSD requires it.
The InstallUpdateRequest optionality must not be used as a general rule for all update-related structures.
```

## 7. GetUpdateHistory / UpdateHistoryEntry guard check

### PDF expectation

The V2.4 PDF keeps update-history entry fields mandatory where listed as 1:1, including timestamp and update URL.

Checked semantic guard:

```text
Do not accidentally make UpdateHistoryEntry.UpdateTimestamp or UpdateHistoryEntry.UpdateURL optional while implementing the InstallUpdate request correction.
```

### XSD observation

The DMS V2.4 candidate keeps the update-history entry fields mandatory where required:

```text
UpdateHistoryEntry.UpdateID required
UpdateHistoryEntry.UpdateTimestamp required
UpdateHistoryEntry.UpdateURL required
UpdateStatus required
```

### Finding

Status: OK / guard passed.

Tool implication:

```text
A history entry missing required fields fails according to XSD.
The fact that InstallUpdateRequest.UpdateURL is optional does not mean historical UpdateURL is optional.
```

## 8. Scope boundary against Common/Enums findings

DMS V2.4 uses Common/Enums structures and values. Known Common/Enums findings still apply where those shared types are referenced, especially:

```text
CE-006 DeviceStateEnumeration XSD-only warning value
CE-007 / CE-008 / CE-009 / CE-010 enumeration value discrepancies
CE-011 through CE-017 Common structure / spelling / cardinality findings where reused
```

DMS-specific audit decision:

```text
Do not duplicate Common/Enums findings as DMS findings unless DMS introduces a service-specific mismatch.
Reference the Common/Enums finding from DMS validation messages when the failing element uses a shared type.
```

## 9. DMS V2.4 first-pass result

```text
No new DMS-specific PDF/XSD mismatch opened in this pass.
DMS V2.4 candidate matches the documented V2.4 technical correction scope checked here.
```

Confirmed OK / guard passed:

```text
GetDeviceErrorMessagesResponseData.ErrorMessage 0:*
SubdeviceErrorMessages.ErrorMessage 0:*
DeviceStatusImpact optional
DeviceStatusPriority optional
InstallUpdateRequest UpdateID/UpdateTimestamp/UpdateURL optional
InstallUpdateRequest UpdateFileChecksum/UpdateFileSize optional
UpdateStateData required fields not accidentally relaxed
UpdateHistoryEntry required fields not accidentally relaxed
```

## 10. Open technical validation tasks

This semantic pass does not replace local XSD validation.

Carry to validation backlog:

```text
DMS V2.4 schema compile with common V2.4 / enumerations V2.4 dependency pool.
Positive sample: minimal GetDeviceErrorMessagesResponseData with no ErrorMessage.
Positive sample: InstallUpdateRequest without UpdateURL.
Positive sample: DeviceStatus with only name/flag.
Negative sample: UpdateStateData missing required UpdateTimestamp.
Negative sample: UpdateHistoryEntry missing required UpdateURL.
```

## 11. Next step

Next non-visual audit step:

```text
Integrate DMS V2.2 / V2.3 / V2.4 history comparison,
or continue with another service-specific block if DMS history is deferred.
```
