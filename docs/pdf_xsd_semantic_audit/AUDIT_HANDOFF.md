# PDF/XSD semantic audit handoff

Status: living handoff for continuing the VDV301 PDF/XSD audit in a new chat.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

Important branch policy:

```text
This is the superbranch / integration working branch.
Do not open this branch as an upstream PR against VDVde/VDV301.
Do not label its full content as an official VDV release.
Official PR work remains separate; currently DMS V2.4 PR #31 is the clean official-facing draft PR path.
```

## How a new chat should resume

At the start of a new chat, read these files first, in this order:

```text
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF.md
docs/pdf_xsd_semantic_audit/00_index.md
docs/pdf_xsd_semantic_audit/VALIDATION_AUTHORITY.md
docs/pdf_xsd_semantic_audit/findings.md
docs/pdf_xsd_semantic_audit/validation_backlog.md
docs/pdf_xsd_semantic_audit/OFFICIAL_PR_CANDIDATES_AFTER_AUDIT.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_vs_xsd_diff.csv
docs/pdf_xsd_semantic_audit/generated/common_v2_4_datatypes_xsd_inventory.md
docs/pdf_xsd_semantic_audit/generated/common_v2_4_datatypes_xsd_inventory.csv
```

Then read the currently active detailed audit files:

```text
docs/pdf_xsd_semantic_audit/01_common_enums_v2_1_to_v2_4.md
docs/pdf_xsd_semantic_audit/01a_common_enums_v2_4_table_check.md
docs/pdf_xsd_semantic_audit/01b_common_enums_v2_4_continuation.md
docs/pdf_xsd_semantic_audit/01c_common_enums_additional_text_message_history.md
docs/pdf_xsd_semantic_audit/01d_common_enums_v2_4_enumeration_first_pass.md
docs/pdf_xsd_semantic_audit/01e_common_enums_v2_4_enumeration_second_pass.md
docs/pdf_xsd_semantic_audit/01f_common_enums_v2_4_pdf_vs_xsd_enum_diff.md
docs/pdf_xsd_semantic_audit/01g_common_enums_v2_4_datatypes_core_structures.md
docs/pdf_xsd_semantic_audit/01h_common_enums_v2_4_core_data_structures.md
docs/pdf_xsd_semantic_audit/01i_common_enums_v2_4_remaining_data_structures_part1.md
docs/pdf_xsd_semantic_audit/01j_common_enums_v2_4_remaining_data_structures_part2.md
docs/pdf_xsd_semantic_audit/01k_common_enums_v2_4_structure_closure.md
docs/pdf_xsd_semantic_audit/01l_common_enums_v2_4_deferred_scope_resolution.md
docs/pdf_xsd_semantic_audit/02_dms_v2_4_pdf_xsd_audit.md
docs/pdf_xsd_semantic_audit/02a_dms_v2_2_v2_3_v2_4_history_compare.md
```

Also read the broader branch context when needed:

```text
docs/superbranch_status.md
docs/schriften_coverage_audit_v0_1.md
```

Before writing anything, fetch the current branch ref:

```text
refs/heads/dev/schema-integration
```

Use the returned commit SHA as the current base. Do not rely on a remembered SHA if the branch has moved.

## Current audit objective

Long-term objective:

```text
Complete PDF-vs-XSD semantic comparison for all public VDV301 writings / schema-relevant versions V1.0 through V2.4.
```

Current active direction:

```text
Continue non-visual audit work while user-specific visual PDF checks are deferred.
```

Current method:

```text
1. Treat PDF tables/version histories as the documentation side.
2. Treat XSD files in dev/schema-integration as the schema side.
3. Record exact evidence and classify each result.
4. Do not correct XSDs during audit unless the user explicitly approves a separate correction branch/PR.
5. Keep candidate/PR/fork provenance visible.
```

## Validation authority

VDV 301-2 V2.4 General Conventions state that XML contents can be validated using XSD and that VDV provides the XSD files for the specified services. They also state that, in case of inconsistencies, the XSD definitions take precedence over the documentation.

Tool and audit implication:

```text
Validation follows XSD.
PDF differences are shown as explanatory notes, not as executable validation authority.
```

## Official PR candidate policy

Potential typo-like or correction candidates are tracked in:

```text
docs/pdf_xsd_semantic_audit/OFFICIAL_PR_CANDIDATES_AFTER_AUDIT.md
```

Rule:

```text
Do not open official correction PRs during the audit.
At the end of the full audit, recheck candidates against current upstream, open PRs, PDFs, history and local validation.
Prepare or open a PR only after explicit user approval.
```

Current examples:

```text
PR-CAND-001 GlobalCardStausID spelling, linked CE-016.
PR-CAND-002 TSPPoint Desciption spelling, linked CE-017.
```

## Established findings so far

```text
CE-001: No separate IBIS-IP_Enumerations_V2.3.xsd in branch; common V2.3 includes Enumerations V2.2. State unclear.
CE-002: V2.4 version history says StopPointNumber but table/XSD use PointNumber. OK with note; do not rename.
CE-003: V2.4 common/enums mostly promising but not closed across all versions.
CE-004: ServiceNameEnumeration V2.4: PDF table still shows SystemDocumentationService/SystemManagementService, but version history says removed and XSD omits them. Confirmed discrepancy; likely PDF table inconsistency.
CE-005: TripInformation AdditionalTextMessage cardinality mismatch across V2.0-V2.4. PDF/history says 0:* / maxOccurs unbounded; XSD permits only 0:1 per named field. Confirmed historical mismatch; do not auto-correct.
CE-006: DeviceStateEnumeration XSD contains warning, not listed in V2.4 PDF table. Confirmed discrepancy.
CE-007: Case-sensitive enum value mismatches: PDF Other/Valid/Air vs XSD other/valid/air. Confirmed discrepancy.
CE-008: Submode case differences: Funicular/Taxi Unknown/Undefined/minicab vs XSD unknown/undefined/miniCab. Confirmed discrepancy.
CE-009: RailSubmodeEnumeration PDF specialRail vs XSD specialTrain. Confirmed discrepancy.
CE-010: AirSubmodeEnumeration XSD-only canalBarge. Confirmed discrepancy.
CE-011: Connection TransportMode/ConnectionMode cardinality PDF 0:* vs XSD 0:1. Confirmed discrepancy candidate.
CE-012: DeviceSpecificationWithStateList cardinality PDF 1:* vs XSD 0:*. Confirmed discrepancy candidate.
CE-013: AdditionalAnnouncement third choice PDF InformationAtSpecificPoint vs XSD SpecificPoint, plus optional XSD choice. Confirmed discrepancy candidate.
CE-014: DataVersionList cardinality PDF 1:* vs XSD 0:*. Confirmed discrepancy candidate.
CE-015: FareZoneInformation PDF extraction casing Farezone* vs XSD FareZone*. Visual PDF confirmation deferred.
CE-016: GlobalCardStatusID vs XSD GlobalCardStausID spelling difference. Confirmed discrepancy candidate.
CE-017: TSPPoint Desciption spelling candidate. XSD observation confirmed; PDF visual confirmation deferred.
```

The authoritative text for these findings is `findings.md`.

## Current Common/Enums V2.4 result

```text
01g: wrapper datatypes, InternationalTextType and NetexMode documented.
01h: core structures checked; CE-011 and CE-012 opened.
01i: remaining structures part 1 checked; CE-013 to CE-016 opened.
01j: remaining structures part 2 checked; CE-017 opened and SB-005 deferred names carried forward.
01k: structure closure pass started; visual checks explicitly deferred.
01l: SB-005 deferred names resolved for Common/Enums V2.4 first-pass closure.
```

Deferred manual visual checks:

```text
CE-015 FareZoneInformation Farezone* vs FareZone* casing.
CE-017 TSPPoint Desciption vs expected Description spelling.
ZoneType first-field casing/spelling if PDF differs from XSD FarezoneTypeID.
```

Decision:

```text
Do not block other audit work on these visual checks.
Carry them in SB-006 until the user can perform manual visual confirmation.
```

## Current DMS result

Files:

```text
docs/pdf_xsd_semantic_audit/02_dms_v2_4_pdf_xsd_audit.md
docs/pdf_xsd_semantic_audit/02a_dms_v2_2_v2_3_v2_4_history_compare.md
```

DMS V2.4 first-pass result:

```text
No new DMS-specific PDF/XSD mismatch opened.
DMS V2.4 candidate matches the documented V2.4 technical correction scope checked here.
```

DMS V2.2/V2.3/V2.4 history result:

```text
No new DMS-specific CE finding opened.
DMS V2.4 candidate remains limited to the documented DMS V2.4 technical correction scope plus V2.4 dependency-family alignment.
DMS V2.3 remains labelled as integration/fork/candidate comparison material, not as an official authority.
```

Checked OK / guard passed:

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

Validation task:

```text
VB-005 DMS V2.4 schema compile and targeted positive/negative XML samples.
```

## Next recommended task

Next non-visual audit step:

```text
TicketValidationService V2.2 / V2.3 / V2.4 include and semantic history.
```

Reason:

```text
TVS V2.4 already has known version-family dependency issues in upstream/candidate material, so it is the next high-value service block after DMS.
```

## Working style for continuity

After each meaningful block:

```text
1. Commit audit file changes to dev/schema-integration.
2. Update findings.md if a CE finding is opened or a finding state changes.
3. Update validation_backlog.md when deferred checks or final-review gates change.
4. Update AUDIT_HANDOFF.md when the continuation point changes materially.
5. Report the final branch commit SHA to the user.
```

This avoids depending on chat memory alone and lets a new chat continue without gaps.
