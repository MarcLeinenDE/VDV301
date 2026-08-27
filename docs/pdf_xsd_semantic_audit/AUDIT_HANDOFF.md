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
docs/pdf_xsd_semantic_audit/findings.md
docs/pdf_xsd_semantic_audit/validation_backlog.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv
```

Then read the currently active detailed audit files:

```text
docs/pdf_xsd_semantic_audit/01_common_enums_v2_1_to_v2_4.md
docs/pdf_xsd_semantic_audit/01a_common_enums_v2_4_table_check.md
docs/pdf_xsd_semantic_audit/01b_common_enums_v2_4_continuation.md
docs/pdf_xsd_semantic_audit/01c_common_enums_additional_text_message_history.md
docs/pdf_xsd_semantic_audit/01d_common_enums_v2_4_enumeration_first_pass.md
docs/pdf_xsd_semantic_audit/01e_common_enums_v2_4_enumeration_second_pass.md
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

Finding states:

```text
OK
OK with note
Mismatch
Unclear
Not checked yet
Confirmed historical mismatch
```

## Established findings so far

```text
CE-001: No separate IBIS-IP_Enumerations_V2.3.xsd in branch; common V2.3 includes Enumerations V2.2. State unclear.
CE-002: V2.4 version history says StopPointNumber but table/XSD use PointNumber. OK with note; do not rename.
CE-003: V2.4 common/enums mostly promising but not fully closed.
CE-004: ServiceNameEnumeration V2.4: PDF table still shows SystemDocumentationService/SystemManagementService, but version history says removed and XSD omits them. Likely documentation/table inconsistency; still open.
CE-005: TripInformation AdditionalTextMessage cardinality mismatch across V2.0-V2.4. PDF/history says 0:* / maxOccurs unbounded; XSD permits only 0:1 per named field. Confirmed historical mismatch; do not auto-correct.
CE-006: DeviceStateEnumeration XSD contains warning, not listed in V2.4 PDF table. Open.
CE-007: Case-sensitive enum value mismatches, e.g. PDF Other/Valid/Air vs XSD other/valid/air. Open.
CE-008: Submode spelling/case candidates, e.g. Funicular/Taxi values. Open.
```

The authoritative text for these findings is `findings.md`.

## Files added for machine inventory

Exporter:

```text
tools/export_xsd_enumerations.py
```

Generated inventory:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.md
```

The CSV is the XSD-side machine inventory for `IBIS-IP_Enumerations_V2.4.xsd`. Use it for exact PDF table comparison, especially tables 65-104 of VDV 301-2-1 V2.4.

## Next recommended task

Continue with:

```text
Create a PDF-side enumeration inventory for VDV 301-2-1 V2.4 tables 65-104,
then compare it exactly/case-sensitively against generated/enumerations_v2_4_xsd_inventory.csv.
```

Expected output files:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_inventory.csv
docs/pdf_xsd_semantic_audit/01f_common_enums_v2_4_pdf_vs_xsd_enum_diff.md
```

The next diff should classify every value-level delta as:

```text
only_in_pdf
only_in_xsd
case_or_spelling_difference
same
unclear_due_pdf_extraction
```

Do not modify `IBIS-IP_Enumerations_V2.4.xsd` during this audit step.

## Working style for continuity

After each meaningful block:

```text
1. Commit audit file changes to dev/schema-integration.
2. Update findings.md if a new CE finding is opened or a finding state changes.
3. Update AUDIT_HANDOFF.md only when the continuation point changes materially.
4. Report the final branch commit SHA to the user.
```

This avoids depending on chat memory alone and lets a new chat continue without gaps.
