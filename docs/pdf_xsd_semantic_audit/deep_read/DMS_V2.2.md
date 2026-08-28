# DeviceManagementService V2.2 - Deep Read Pass 2

Status: textual fresh read complete; byte-pinned source verified; exact official XSD/dependency cross-check complete; EV-107 executable declaration evidence complete; previous-audit comparison complete; visual closure pending because the PDF screenshot backend repeatedly returned cache-miss.

Document ID: `DMS_V2.2`

Official publication:

```text
VDV-Schrift 301-2-0
Version 2.2
08/2019
DeviceManagementService
```

Official PDF:

```text
https://www.vdv.de/301-2-0-sdes-v2-2-devicemanagementservice.pdfx
```

Byte-pinned audit source:

```text
SHA-256: 72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e
size:    1173719 bytes
pin evidence run: 33180310954
pin registry: audit_registry/pdf_source_pins_v0.1.json
```

## 1. Method and source quality

The official V2.2 publication was read afresh before the existing DMS first-pass files and DMS-001..DMS-004 register were opened.

The fresh pass covered:

```text
operation inventory
request/response names
response choice branch names
all DMS-specific structures and cardinalities
subdevice status/error structures
update operation family
update enumerations
section/table references
exact DMS V2.2 -> Common V2.2 -> Enumerations V2.2 route
```

The native text layer is good enough for semantic comparison. Direct screenshots of critical pages repeatedly returned cache-miss, including the GetDeviceStatusInformation/DeviceStatus and InstallUpdate pages. No OCR substitute is promoted over the native text.

Result:

```text
textual_fresh_read_complete: true
original_pdf_visual_review: attempted_failed_cache_miss
deep_read_state: needs_visual_review
```

## 2. Exact executable authority

DMS V2.2 is an official historical profile in this repository.

```text
IBIS-IP_DeviceManagementService_V2.2.xsd
  -> IBIS-IP_common_V2.2.xsd
  -> IBIS-IP_Enumerations_V2.2.xsd
```

The exact stored DMS V2.2 blob is:

```text
c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d
```

Validation follows this exact historical XSD family. Later V2.3 integration or V2.4 candidate corrections are explanatory history only and must not be back-applied.

## 3. Existing historical findings independently reconfirmed

### DMS-003 - ErrorMessage 10:* is historically aligned

Fresh V2.2 PDF evidence:

```text
GetDeviceErrorMessagesResponseData.ErrorMessage 10:*
SubdeviceErrorMessages.ErrorMessage             10:*
```

Exact V2.2 XSD likewise uses `minOccurs="10" maxOccurs="unbounded"` for both lists.

This is therefore not a V2.2 mismatch. The later V2.4 move to `0:*` is a versioned correction and does not relax V2.2 validation.

### DMS-004 - InstallUpdate required fields also remain required in V2.2

Fresh V2.2 PDF and exact XSD both require:

```text
UpdateID        1:1
UpdateTimestamp 1:1
UpdateURL       1:1
```

while checksum and file size are optional.

The previously recorded V2.1 historical rule therefore extends through official DMS V2.2. The V2.4 optionality remains version-specific.

### DR3012V20-007 - stale setter wording persists

The separated V2.2 DMS document still says `GetDeviceConfiguration` enables setting the variable device parameter, although the operation is a Get operation and the V2.2 operation inventory no longer contains SetDeviceConfiguration.

No duplicate finding is opened; the historical documentation issue is strengthened.

### DR3012V20-008 - response described as request persists

The V2.2 GetDeviceInformation response table still describes the response structure/data as a request structure. This strengthens the existing deep-read finding rather than creating a duplicate.

## 4. DMS-005 - GetDeviceStatusInformation response-data branch name

Fresh PDF table 17 prints response choice branch `a` as:

```text
DeviceManagementService.DeviceStatusInformationResponseData
```

while the type/reference column on the same row points to the Get-prefixed response-data structure.

The exact V2.2 XSD declares:

```text
DeviceManagementService.GetDeviceStatusInformationResponseStructure
  choice
    DeviceManagementService.GetDeviceStatusInformationResponseData
    OperationErrorMessage
```

EV-107 independently verifies that the exact XSD contains the Get-prefixed branch and does not contain the PDF-only non-Get spelling.

Classification:

```text
finding: DMS-005
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: very high
version_scope: DMS V2.2 checked
validation_behavior: exact XSD branch name is required; PDF-only branch spelling is not an alias
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

No XSD change is implied.

## 5. DMS-006 - DeviceStatus PDF omits two XSD-required fields

Fresh PDF table 20 lists only:

```text
DeviceStatusName 1:1
DeviceStatusFlag 1:1
```

The exact V2.2 XSD `DeviceStatusStructure` requires four sequence members:

```text
DeviceStatusName     1:1
DeviceStatusFlag     1:1
DeviceStatusImpact   1:1
DeviceStatusPriority 1:1
```

EV-107 confirms all four declarations and their effective `minOccurs=1`.

This is operationally important: a producer implementing only the V2.2 PDF table can emit a two-field DeviceStatus that does not conform to the selected V2.2 XSD.

Historical context:

```text
DMS V2.4 candidate/publication correction:
  DeviceStatusImpact   -> optional
  DeviceStatusPriority -> optional
```

That later correction explains the history but does not retroactively change V2.2.

Classification:

```text
finding: DMS-006
mismatch_kind: cardinality / structure omission
likely_source_issue: pdf_table_or_documentation_error_candidate with later schema/document alignment evidence
classification_confidence: very high
version_scope: DMS V2.2 historical profile
validation_behavior: V2.2 XSD requires Impact and Priority
final_handling_bucket: official_documentation_or_schema_alignment_review_candidate
```

## 6. DMS-007 - InstallUpdate UpdateTimestamp references non-existent `GetUpdateStates`

Fresh PDF table 27 describes `UpdateTimestamp` as used for:

```text
GetUpdateStates and RetrieveUpdateState responses and for logging
```

The V2.2 operation inventory contains `GetUpdateHistory`, not `GetUpdateStates`.

The exact V2.2 XSD annotation says:

```text
Timestamp used for GetUpdateHistory and RetrieveUpdateState responses and for logging
```

EV-107 confirms this exact XSD annotation and confirms `GetUpdateStates` is not present there.

Classification:

```text
finding: DMS-007
mismatch_kind: operation_or_element_name / reference
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: very high
validation_behavior: none directly; do not invent a GetUpdateStates operation or route
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

## 7. Deep-read documentation findings

### DRDMS22-001 - wrong table reference in SubdeviceStatusInformation

PDF table 23 describes `DeviceStatusInformation` as detailed status `cf. table 27`.

Actual context:

```text
Table 19 = DeviceStatusInformationStructure
Table 27 = InstallUpdateRequestStructure
```

The intended reference is therefore not table 27. This is documentation/navigation only and does not change XSD validation.

### DRDMS22-002 - TOC section numbering 1.33..1.35

The table of contents prints:

```text
1.33 GetUpdateHistory
1.34 FinalizeUpdate
1.35 FinalizeAllPendingUpdates
```

while the body correctly uses:

```text
2.33
2.34
2.35
```

The same TOC then begins top-level section `2 Versionshistorie / Version History`, making the numbering conflict explicit.

### DRDMS22-003 - `InstallationSuccessfull` prose typo vs executable enum

The update-history prose says `InstallationSuccessfull`, while the enumeration table and executable XSD value are:

```text
InstallationSuccessful
```

The V2.2 XSD documentation annotation itself also carries the typo-like prose spelling, but EV-107 confirms it is not an executable enumeration value.

Handling:

```text
do not create InstallationSuccessfull as an enum alias
```

### DRDMS22-004 - singular GetDeviceErrorMessage wording

Section 2.9 is correctly titled `GetDeviceErrorMessages`, but its request prose says `GetDeviceErrorMessage` singular. The actual operation/table/XSD use the plural form.

Handling:

```text
do not synthesize singular operation alias
```

## 8. EV-107 executable evidence

```text
Evidence ID: EV-107
GitHub Actions run: 33181833930
head tested: 00a31f808b9955a9c9af475621c4ce87b610c05a
tool: tools/validate_dms_v22_deep_read_ev107.py
result: PASS
```

Confirmed from the exact stored XSD:

```text
GetDeviceStatusInformation response branch:
  DeviceManagementService.GetDeviceStatusInformationResponseData
  PDF-only DeviceManagementService.DeviceStatusInformationResponseData absent

DeviceStatusStructure:
  DeviceStatusName     required
  DeviceStatusFlag     required
  DeviceStatusImpact   required
  DeviceStatusPriority required

InstallUpdate.UpdateTimestamp annotation:
  GetUpdateHistory + RetrieveUpdateState
  GetUpdateStates absent

UpdateStatusEnumeration:
  InstallationSuccessful present
  InstallationSuccessfull absent as enum value
```

The same run also re-executed the whole deterministic repository suite successfully:

```text
50/50 root XSDs compile
39 XSD service profiles
84 direct include edges
EV-103..EV-107 PASS
RV-001..RV-004 PASS
SDK manifest/profile checks PASS
```

## 9. Comparison with previous DMS audit

Only after the fresh read were the earlier DMS reports opened.

They already covered:

```text
DMS-001 V2.0 operation/group modelling
DMS-002 V2.0 unresolved Word references
DMS-003 historical ErrorMessage 10:* rule
DMS-004 historical InstallUpdate requiredness
V2.2/V2.3/V2.4 dependency and correction history
```

The fresh V2.2 deep read adds:

```text
DMS-005 response-data branch name mismatch
DMS-006 DeviceStatus PDF omission of two mandatory V2.2 XSD fields
DMS-007 GetUpdateStates vs GetUpdateHistory reference
DRDMS22-001 wrong table 27 reference
DRDMS22-002 TOC 1.33..1.35 numbering
DRDMS22-003 InstallationSuccessfull prose typo
DRDMS22-004 singular GetDeviceErrorMessage wording
```

and strengthens:

```text
DMS-003
DMS-004 (scope now explicitly V2.1-V2.2)
DR3012V20-007
DR3012V20-008
```

## 10. Conclusion

```text
textual fresh read: complete
byte-pinned official PDF: yes
exact official DMS V2.2 XSD route: verified
EV-107: PASS
old-audit comparison: complete
new service findings: DMS-005..DMS-007
new deep-read documentation findings: DRDMS22-001..DRDMS22-004
visual page closure: pending because screenshot backend returns cache-miss
deep_read_state: needs_visual_review
```

No XSD is modified.

## 11. Next target

```text
DMS_V2.4
DeviceManagementService V2.4
```

Before Fresh Read, byte-pin the official V2.4 PDF and retain the candidate/integration XSD authority label separately from the public V2.4 writing.
