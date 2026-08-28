# EV-108 - DMS V2.4 candidate/integration declaration evidence

Status: PASS.

## Purpose

EV-108 records deterministic declaration evidence for the repository's DMS V2.4 XSD while preserving the authority boundary:

```text
Official public PDF: VDV 301-2-0 DeviceManagementService V2.4.
Checked XSD: candidate/integration material in dev/schema-integration.
```

A successful EV-108 result does not make that XSD an official VDV release schema.

## Execution

```text
evidence_id: EV-108
workflow: schema-audit-validation
run_id: 33182963733
head_tested: 1ea19f21c630b5f111fc8e41e6e39479e2b1c97f
result: PASS
script: tools/validate_dms_v24_deep_read_ev108.py
```

The workflow was returned to `workflow_dispatch`-only immediately after the evidence run.

## Deterministic checks

EV-108 reads `IBIS-IP_DeviceManagementService_V2.4.xsd` and confirms:

```text
1. GetDeviceStatusInformation response branch
   candidate XSD: DeviceManagementService.GetDeviceStatusInformationResponseData
   PDF-only DeviceManagementService.DeviceStatusInformationResponseData is absent

2. DeviceStatusStructure
   DeviceStatusName      minOccurs=1
   DeviceStatusFlag      minOccurs=1
   DeviceStatusImpact    minOccurs=0
   DeviceStatusPriority  minOccurs=0

3. ErrorMessage lists
   GetDeviceErrorMessagesResponseData.ErrorMessage 0:*
   SubdeviceErrorMessages.ErrorMessage              0:*

4. InstallUpdateRequest
   UpdateID           optional
   UpdateTimestamp    optional
   UpdateURL          optional
   UpdateFileChecksum optional
   UpdateFileSize     optional

5. InstallUpdate.UpdateTimestamp annotation
   contains GetUpdateHistory + RetrieveUpdateState
   does not contain GetUpdateStates

6. UpdateStatusEnumeration
   InstallationSuccessful exists
   InstallationSuccessfull does not exist as executable enum value
```

The script reports `repository_mutated=false`.

## Finding implications

```text
DMS-005: persists against the checked V2.4 candidate/integration XSD.
DMS-006: corrected/aligned for checked V2.4 PDF/candidate profile.
DMS-007: persists against the checked V2.4 candidate/integration XSD.
DRDMS22-003: typo remains non-executable; enum spelling is InstallationSuccessful.
```

## Baseline guard

The same workflow run also completed the existing deterministic suite successfully, including the 50-root compilation and existing EV/RV checks.

Authority rule remains unchanged:

```text
Candidate/integration success is evidence for the explicitly selected candidate/integration profile only.
No latest-wins or authority promotion is permitted.
```
