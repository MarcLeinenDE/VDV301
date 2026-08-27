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
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_vs_xsd_diff.csv
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

Current block:

```text
Common Structures / Enumerations, especially VDV 301-2-1 V2.4.
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

Example:

```text
FAIL for `Valid` if XSD requires `valid`.
Provider-facing note: PDF lists `Valid`, but XSD has precedence; therefore validation fails.
```

See:

```text
docs/pdf_xsd_semantic_audit/VALIDATION_AUTHORITY.md
```

Finding states:

```text
OK
OK with note
Mismatch
Unclear
Not checked yet
Confirmed historical mismatch
Confirmed PDF/XSD value discrepancy
```

## Established findings so far

```text
CE-001: No separate IBIS-IP_Enumerations_V2.3.xsd in branch; common V2.3 includes Enumerations V2.2. State unclear.
CE-002: V2.4 version history says StopPointNumber but table/XSD use PointNumber. OK with note; do not rename.
CE-003: V2.4 common/enums mostly promising but not fully closed.
CE-004: ServiceNameEnumeration V2.4: PDF table still shows SystemDocumentationService/SystemManagementService, but version history says removed and XSD omits them. Confirmed discrepancy; likely PDF table inconsistency.
CE-005: TripInformation AdditionalTextMessage cardinality mismatch across V2.0-V2.4. PDF/history says 0:* / maxOccurs unbounded; XSD permits only 0:1 per named field. Confirmed historical mismatch; do not auto-correct.
CE-006: DeviceStateEnumeration XSD contains warning, not listed in V2.4 PDF table. Confirmed discrepancy.
CE-007: Case-sensitive enum value mismatches: PDF Other/Valid/Air vs XSD other/valid/air. Confirmed discrepancy.
CE-008: Submode case differences: Funicular/Taxi Unknown/Undefined/minicab vs XSD unknown/undefined/miniCab. Confirmed discrepancy.
CE-009: RailSubmodeEnumeration PDF specialRail vs XSD specialTrain. Confirmed discrepancy.
CE-010: AirSubmodeEnumeration XSD-only canalBarge. Confirmed discrepancy.
```

The authoritative text for these findings is `findings.md`.

## Machine inventory files

Exporter:

```text
tools/export_xsd_enumerations.py
```

Generated XSD inventory:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.md
```

Generated PDF inventory and diff:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_vs_xsd_diff.csv
docs/pdf_xsd_semantic_audit/01f_common_enums_v2_4_pdf_vs_xsd_enum_diff.md
```

## Next recommended task

Continue with Common/Enums V2.4 common data structures 2.1-2.64:

```text
LineInformation
StopInformation
TripInformation
DisplayContent
Connection
DeviceInformation / DeviceSpecification family
then the remaining structures in table order
```

Use the same evidence style:

```text
PDF table expectation
XSD observation
finding classification
validation follows XSD
PDF discrepancy becomes provider-facing note
no schema changes during audit
```

Alternative if we want to close known enum findings first:

```text
Check CE-006, CE-009 and CE-010 against older Common/Enums PDFs/XSDs and external TPEG/NeTEx terminology.
```

## Working style for continuity

After each meaningful block:

```text
1. Commit audit file changes to dev/schema-integration.
2. Update findings.md if a new CE finding is opened or a finding state changes.
3. Update AUDIT_HANDOFF.md only when the continuation point changes materially.
4. Report the final branch commit SHA to the user.
```

This avoids depending on chat memory alone and lets a new chat continue without gaps.
