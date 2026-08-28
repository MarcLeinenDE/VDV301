# EV-107 - DeviceManagementService V2.2 Deep Read declaration evidence

Status: PASS.

## Scope

```text
evidence_id: EV-107
run: 33181833930
head tested: 00a31f808b9955a9c9af475621c4ce87b610c05a
authority: official DMS V2.2 exact stored XSD
tool: tools/validate_dms_v22_deep_read_ev107.py
schema: IBIS-IP_DeviceManagementService_V2.2.xsd
```

Purpose: convert the XML-relevant DMS V2.2 Deep Read observations into deterministic schema-declaration evidence without modifying the historical XSD.

## Confirmed declarations

### GetDeviceStatusInformation response branch

Exact XSD contains:

```text
DeviceManagementService.GetDeviceStatusInformationResponseData
```

The PDF-only spelling:

```text
DeviceManagementService.DeviceStatusInformationResponseData
```

is absent from the XSD response choice.

### DeviceStatusStructure

Exact XSD sequence is:

```text
DeviceStatusName
DeviceStatusFlag
DeviceStatusImpact
DeviceStatusPriority
```

All four have effective `minOccurs=1`.

### InstallUpdate UpdateTimestamp annotation

Exact XSD documentation says:

```text
Timestamp used for GetUpdateHistory and RetrieveUpdateState responses and for logging
```

`GetUpdateStates` is not present in that annotation.

### UpdateStatusEnumeration

Executable enum contains:

```text
InstallationSuccessful
```

and does not contain:

```text
InstallationSuccessfull
```

The typo-like form exists only in prose/documentation annotation and is not an executable enum alias.

## Run result

EV-107 itself returned PASS.

The same workflow run also returned PASS for the full deterministic repository suite, including:

```text
50/50 current root XSD compile
39 XSD service profiles
84 direct include edges
EV-103, EV-104, EV-105, EV-106
RV-001, RV-002, RV-003, RV-004
SDK manifest/profile checks
```

## Authority and safety

```text
No schema byte was changed.
repository_mutated=false
DMS V2.2 remains exact historical validation authority.
PDF differences remain explanatory audit findings.
No later DMS V2.4 correction is back-applied.
```
