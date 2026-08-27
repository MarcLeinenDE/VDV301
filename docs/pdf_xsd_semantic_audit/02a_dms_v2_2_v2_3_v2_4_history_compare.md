# DeviceManagementService V2.2 / V2.3 / V2.4 history comparison

Status: completed first pass.

Scope:

```text
IBIS-IP_DeviceManagementService_V2.2.xsd
IBIS-IP_DeviceManagementService_V2.3.xsd
IBIS-IP_DeviceManagementService_V2.4.xsd
```

Purpose:

```text
Confirm that the DMS V2.4 candidate applies only the documented DMS V2.4 technical correction scope, plus the expected version-family dependency move to common/enumerations V2.4.
```

Authority rule:

```text
Validation follows XSD.
PDF differences are retained as provider-facing explanation notes.
No schema change is made during this audit pass.
```

Important provenance note:

```text
DMS V2.2 is the official upstream baseline file present in the branch.
DMS V2.3 is integration/fork/candidate material and is useful as a historical comparison point, but it is not treated as an official public VDV DMS writing unless separately confirmed.
DMS V2.4 is candidate/integration material in dev/schema-integration and is the basis of the clean official-facing DMS V2.4 draft PR path.
```

## 1. Dependency include history

### DMS V2.2

Observed include family:

```text
IBIS-IP_common_V2.2.xsd
IBIS-IP_Enumerations_V2.2.xsd
```

### DMS V2.3

Observed include family:

```text
IBIS-IP_common_V2.3.xsd
IBIS-IP_Enumerations_V2.2.xsd
```

Interpretation:

```text
This mirrors the broader CE-001 observation that there is no separate Enumerations V2.3 file in the integration branch.
Do not infer a V2.3 enumeration include defect from DMS alone.
```

### DMS V2.4

Observed include family:

```text
IBIS-IP_common_V2.4.xsd
IBIS-IP_Enumerations_V2.4.xsd
```

Interpretation:

```text
DMS V2.4 uses the V2.4 schema-family dependency pool as expected for the V2.4 candidate.
```

## 2. DMS V2.2 to DMS V2.3 comparison

First-pass semantic delta:

```text
Dependency include move:
  common V2.2 -> common V2.3
  enumerations remain V2.2

GetDeviceErrorMessagesResponseData.ErrorMessage:
  V2.2 minOccurs="10" maxOccurs="unbounded"
  V2.3 minOccurs="0" maxOccurs="unbounded"

SubdeviceErrorMessages.ErrorMessage:
  V2.2 minOccurs="10" maxOccurs="unbounded"
  V2.3 minOccurs="0" maxOccurs="unbounded"
```

No V2.3-specific public DMS document was used as authority in this pass. Therefore the V2.3 file is treated as a useful intermediate comparison point, not as the normative source for V2.4.

### Finding

Status: OK with provenance note.

No new DMS-specific CE finding opened.

## 3. DMS V2.3 to DMS V2.4 comparison

First-pass semantic delta:

```text
Dependency include move:
  common V2.3 -> common V2.4
  enumerations V2.2 -> enumerations V2.4

ErrorMessage minOccurs remains corrected:
  GetDeviceErrorMessagesResponseData.ErrorMessage remains 0:*
  SubdeviceErrorMessages.ErrorMessage remains 0:*

New V2.4 technical correction reflected:
  DeviceStatusImpact required -> optional
  DeviceStatusPriority required -> optional

New V2.4 technical correction reflected:
  InstallUpdateRequest.UpdateID required -> optional
  InstallUpdateRequest.UpdateTimestamp required -> optional
  InstallUpdateRequest.UpdateURL required -> optional

Fields already optional before V2.4 remain optional:
  InstallUpdateRequest.UpdateFileChecksum optional
  InstallUpdateRequest.UpdateFileSize optional
```

### Finding

Status: OK.

This matches the DMS V2.4 technical correction scope already documented in `02_dms_v2_4_pdf_xsd_audit.md`.

No new DMS-specific CE finding opened.

## 4. DMS V2.2 to DMS V2.4 direct comparison

Direct first-pass semantic delta from official V2.2 baseline to V2.4 candidate:

```text
Dependency include move:
  common V2.2 -> common V2.4
  enumerations V2.2 -> enumerations V2.4

Documented DMS V2.4 error-message correction:
  GetDeviceErrorMessagesResponseData.ErrorMessage minOccurs 10 -> 0
  SubdeviceErrorMessages.ErrorMessage minOccurs 10 -> 0

Documented DMS V2.4 DeviceStatusStructure correction:
  DeviceStatusImpact required -> optional
  DeviceStatusPriority required -> optional

Documented DMS V2.4 InstallUpdateRequest correction:
  UpdateID required -> optional
  UpdateTimestamp required -> optional
  UpdateURL required -> optional

Already optional and kept optional:
  UpdateFileChecksum
  UpdateFileSize
```

Guard result:

```text
No additional DMS-specific semantic delta was intentionally introduced in this first-pass audit.
```

## 5. Guard checks against accidental over-relaxation

The V2.4 candidate must not generalize InstallUpdateRequest optionality to other update-related structures.

Checked guards:

```text
UpdateStateData.UpdateID remains required.
UpdateStateData.UpdateTimestamp remains required.
UpdateStatus remains required.

UpdateHistoryEntry.UpdateID remains required.
UpdateHistoryEntry.UpdateTimestamp remains required.
UpdateHistoryEntry.UpdateURL remains required.
UpdateStatus remains required.
```

Status: guard passed.

Tool consequence:

```text
InstallUpdateRequest.UpdateURL missing can be valid in DMS V2.4.
UpdateHistoryEntry.UpdateURL missing remains invalid where the XSD requires it.
UpdateStateData.UpdateTimestamp missing remains invalid where the XSD requires it.
```

## 6. Relation to official PR #31

The official-facing DMS draft PR path should stay narrow:

```text
Add DeviceManagementService V2.4 schema candidate.
Include required V2.4 dependency files.
Align TVS V2.4 enumeration include only as dependency-family support.
```

Do not mix unrelated Common/Enums correction candidates into the DMS PR.

This history comparison supports the PR scope because it shows:

```text
DMS V2.4 candidate scope is limited to the documented DMS V2.4 technical corrections plus V2.4 dependency-family alignment.
```

## 7. Result

```text
DMS V2.2 / V2.3 / V2.4 history comparison completed first pass.
No new DMS-specific PDF/XSD mismatch opened.
DMS V2.4 candidate remains consistent with the documented correction scope checked so far.
DMS V2.3 remains labelled as integration/fork/candidate comparison material, not as an official authority.
```

## 8. Remaining tasks

Semantic tasks:

```text
Keep Common/Enums findings referenced where shared structures or enumerations are reused by DMS.
Do not duplicate Common/Enums findings as DMS findings unless DMS itself introduces a mismatch.
```

Technical validation tasks:

```text
Run VB-005 later: DMS V2.4 schema compile with common/enumerations V2.4.
Run targeted positive/negative XML samples for the checked correction scope.
```

Next audit direction:

```text
Continue with the next non-visual service block, recommended: TicketValidationService V2.2 / V2.3 / V2.4 include and semantic history.
```
