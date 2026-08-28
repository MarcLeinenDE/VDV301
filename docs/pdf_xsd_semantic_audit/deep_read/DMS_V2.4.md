# DeviceManagementService V2.4 Deep Read Pass 2

Status: textual fresh read complete; original-PDF visual closure pending because requested page rendering returned cache-miss.

## Scope and authority

Document:

```text
VDV-Schrift 301-2-0
DeviceManagementService V2.4
01/2023
```

Byte-pinned official PDF source:

```text
source_id: DMS_V2.4
SHA-256: 347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd
size: 1298127 bytes
pin run: 33182486754
```

Authority boundary:

```text
PDF: official public VDV writing.
IBIS-IP_DeviceManagementService_V2.4.xsd in dev/schema-integration: candidate/integration material.
The candidate XSD is used only as explicitly labelled comparison/executable evidence.
It is not promoted to official-release authority by this audit.
```

Fresh-read rule:

```text
The V2.4 PDF was read independently before consulting the pre-existing
02_dms_v2_4_pdf_xsd_audit.md first-pass report.
```

## V2.4 documented correction scope

The V2.4 history explicitly records no functional extension and three technical correction families:

```text
1. Device/subdevice error-message lists changed from mandatory minimum 10 to optional.
2. DeviceStatusStructure adapted to the XML definition.
3. InstallUpdate structures adapted to support packages from predefined storage locations.
```

Fresh PDF tables and the explicitly selected candidate/integration XSD are aligned for these corrected points:

```text
GetDeviceErrorMessagesResponseData.ErrorMessage  0:*
SubdeviceErrorMessages.ErrorMessage               0:*
DeviceStatusImpact                                0:1
DeviceStatusPriority                              0:1
InstallUpdate.UpdateID                            0:1
InstallUpdate.UpdateTimestamp                     0:1
InstallUpdate.UpdateURL                           0:1
InstallUpdate.UpdateFileChecksum                  0:1
InstallUpdate.UpdateFileSize                      0:1
```

Historical rule:

```text
These V2.4 corrections must not be back-applied to official DMS V2.2.
```

## DMS-005 - persists in V2.4

PDF response-choice text continues to use:

```text
DeviceManagementService.DeviceStatusInformationResponseData
```

The candidate/integration V2.4 XSD uses:

```text
DeviceManagementService.GetDeviceStatusInformationResponseData
```

EV-108 confirms the candidate XSD contains the `Get...` branch and no PDF-only alias.

State:

```text
persists_through_checked_V2.4_document
validation effect: selected XSD spelling remains authority
```

## DMS-006 - corrected/aligned in V2.4

V2.2 PDF omitted `DeviceStatusImpact` and `DeviceStatusPriority` while the V2.2 XSD required both.

V2.4 now presents:

```text
DeviceStatusName      1:1
DeviceStatusFlag      1:1
DeviceStatusImpact    0:1
DeviceStatusPriority  0:1
```

The candidate/integration V2.4 XSD has the same effective requiredness.

State:

```text
resolved_for_checked_V2.4_profile
historical V2.2 mismatch remains valid and must not be rewritten
```

## DMS-007 - persists in V2.4

The V2.4 InstallUpdate `UpdateTimestamp` description still refers to:

```text
GetUpdateStates
```

The actual operation inventory uses:

```text
GetUpdateHistory
RetrieveUpdateState
```

The candidate/integration XSD annotation likewise says `GetUpdateHistory` and `RetrieveUpdateState`.

State:

```text
persists_through_checked_V2.4_document
no GetUpdateStates alias is created
```

## Documentation-history checks

### DRDMS22-001 - resolved

The V2.2 wrong SubdeviceStatusInformation reference to table 27 is corrected in V2.4 to the relevant table 19 reference.

### DRDMS22-002 - resolved

V2.4 table-of-contents numbering for GetUpdateHistory / FinalizeUpdate / FinalizeAllPendingUpdates uses 2.33 / 2.34 / 2.35 consistently with the body.

### DRDMS22-003 - persists

`InstallationSuccessfull` remains in prose/documentation annotation context, while the executable enumeration value is:

```text
InstallationSuccessful
```

EV-108 confirms the typo form is not an executable enum value.

### DRDMS22-004 - persists

The GetDeviceErrorMessages request prose still contains singular `GetDeviceErrorMessage`, while the operation/table/schema use plural `GetDeviceErrorMessages`.

### DR3012V20-007 - persists

GetDeviceConfiguration prose continues to describe setting a variable parameter although the operation is the getter/retrieval path.

### DR3012V20-008 - persists

The GetDeviceInformation response description continues to label response structure/data as request structure/data.

## DRDMS24-001 - wrong service in the V2.4 foreword

New finding from the independent V2.4 fresh read.

The DMS V2.4 foreword states in both language sections that the document describes the `HtmlDisplayService`; the English wording additionally describes the HTML/Web-server purpose of that service.

This is incompatible with the document identity, operation inventory and remainder of VDV 301-2-0 DeviceManagementService V2.4.

Classification:

```text
classification: pdf_copy_paste_service_identity_error_candidate
confidence: very_high
validation impact: none
handling: documentation/provider note only; do not infer HTMLDisplay semantics for DMS
```

## EV-108

Executable comparison evidence:

```text
evidence: EV-108
run: 33182963733
head tested: 1ea19f21c630b5f111fc8e41e6e39479e2b1c97f
result: PASS
authority: candidate/integration DMS V2.4 XSD
```

EV-108 confirms:

```text
DMS-005 candidate response branch uses GetDeviceStatusInformationResponseData.
DMS-006 V2.4 candidate requiredness is name/flag required, impact/priority optional.
ErrorMessage cardinalities are 0:*.
All five checked InstallUpdate fields are optional.
UpdateTimestamp annotation uses GetUpdateHistory + RetrieveUpdateState.
Executable enum is InstallationSuccessful.
repository_mutated=false.
```

The full deterministic workflow also passed in that run. This does not convert candidate/integration schema authority into official authority.

## Visual-review boundary

Requested original-PDF page renders for the critical tables/pages returned cache-miss.

Therefore:

```text
textual_fresh_read_complete: true
original_pdf_visual_review: attempted_failed_cache_miss
state: needs_visual_review
```

No OCR substitute is promoted and the document is not labelled `exhaustive_read`.

## Result

```text
DMS V2.4 fresh textual read complete.
DMS-005 persists.
DMS-006 is corrected/aligned in the checked V2.4 PDF/candidate-XSD profile.
DMS-007 persists.
DRDMS22-001 and DRDMS22-002 are resolved in V2.4.
DRDMS22-003 and DRDMS22-004 persist.
DR3012V20-007 and DR3012V20-008 persist.
DRDMS24-001 newly opened for the HtmlDisplayService foreword copy/paste error.
No XSD changed.
No official-facing action authorized.
```
