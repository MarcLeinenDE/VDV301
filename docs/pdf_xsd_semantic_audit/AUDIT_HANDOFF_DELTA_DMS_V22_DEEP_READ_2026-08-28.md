# Audit Handoff Delta - DMS V2.2 Deep Read

Date: 2026-08-28

Base state before this delta:

```text
branch: dev/schema-integration
head before final DMS V2.2 report commit: bfcab6be97f18daa3e2c21a4c8bf0af5ac0cbe43
phase: Deep Read Pass 2
```

## Completed in this delta

### DMS V2.2 source provenance

Official PDF was byte-pinned before Fresh Read:

```text
source_id: DMS_V2.2
url: https://www.vdv.de/301-2-0-sdes-v2-2-devicemanagementservice.pdfx
sha256: 72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e
size: 1173719 bytes
pin evidence run: 33180310954
```

PDF bytes remain outside the public repository.

### Fresh Read result

The official V2.2 publication was read before consulting the existing DMS first-pass reports.

```text
textual_fresh_read_complete: true
visual_review: attempted but screenshot backend returned cache-miss
deep_read_state: needs_visual_review
```

Exact validation route remains:

```text
IBIS-IP_DeviceManagementService_V2.2.xsd
  -> IBIS-IP_common_V2.2.xsd
  -> IBIS-IP_Enumerations_V2.2.xsd
```

No XSD was modified.

### New DMS service findings

```text
DMS-005
  PDF GetDeviceStatusInformation response branch omits Get prefix;
  exact XSD requires DeviceManagementService.GetDeviceStatusInformationResponseData.

DMS-006
  PDF DeviceStatus table lists only DeviceStatusName/DeviceStatusFlag;
  exact V2.2 XSD additionally requires DeviceStatusImpact and DeviceStatusPriority.

DMS-007
  PDF InstallUpdate.UpdateTimestamp refers to GetUpdateStates;
  exact XSD and operation inventory use GetUpdateHistory.
```

### New documentation-only Deep Read findings

```text
DRDMS22-001  wrong table 27 reference for DeviceStatusInformation
DRDMS22-002  TOC 1.33/1.34/1.35 vs body 2.33/2.34/2.35
DRDMS22-003  InstallationSuccessfull prose/annotation typo vs executable InstallationSuccessful
DRDMS22-004  singular GetDeviceErrorMessage wording vs plural operation name
```

### Existing findings strengthened without duplicate IDs

```text
DMS-003          V2.2 still PDF/XSD-aligned at ErrorMessage 10:*
DMS-004          InstallUpdate UpdateID/UpdateTimestamp/UpdateURL requiredness extends through V2.2
DR3012V20-007    stale GetDeviceConfiguration setter wording persists in separated DMS V2.2
DR3012V20-008    GetDeviceInformation response still described as request structure/data
```

## EV-107

New permanent executable evidence:

```text
evidence_id: EV-107
run: 33181833930
head tested: 00a31f808b9955a9c9af475621c4ce87b610c05a
tool: tools/validate_dms_v22_deep_read_ev107.py
result: PASS
```

EV-107 confirms from the exact stored DMS V2.2 XSD:

```text
- GetDeviceStatusInformation response branch uses the Get-prefixed exact name.
- DeviceStatusStructure has four fields and all four are required.
- InstallUpdate.UpdateTimestamp annotation uses GetUpdateHistory + RetrieveUpdateState.
- InstallationSuccessful is the executable enum; InstallationSuccessfull is not.
```

The same run revalidated the complete deterministic baseline successfully:

```text
50/50 root XSDs compile
39 XSD service profiles
84 direct include edges
EV-103..EV-107 PASS
RV-001..RV-004 PASS
SDK manifest/profile checks PASS
```

The permanent workflow was restored to `workflow_dispatch` only after the evidence run.

## Files added/updated by the final DMS V2.2 report commit

```text
docs/pdf_xsd_semantic_audit/deep_read/DMS_V2.2.md
audit_registry/deep_read_findings_delta_dms_v22_2026-08-28.json
audit_registry/deep_read_registry_delta_dms_v22_2026-08-28.json
docs/pdf_xsd_semantic_audit/DEVICE_MANAGEMENT_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/24f_executable_validation_dms_v22.md
docs/pdf_xsd_semantic_audit/EVIDENCE_ID_POLICY.md
docs/pdf_xsd_semantic_audit/validation_backlog.md
docs/pdf_xsd_semantic_audit/findings.md
00_START_HERE/CURRENT_STATE.json
this handoff delta
```

## Next target

```text
DMS_V2.4
```

Required order:

```text
1. byte-pin official DMS V2.4 PDF
2. retain public-PDF authority separately from candidate/integration V2.4 XSD authority
3. Fresh Read PDF independently
4. exact candidate/integration XSD cross-check
5. only then compare with existing 02_dms_v2_4_pdf_xsd_audit.md
6. keep needs_visual_review if screenshot backend remains unavailable
```

Do not treat the current DMS V2.4 candidate/integration XSD as an official upstream release merely because the public V2.4 writing exists.
