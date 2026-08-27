# PDF/XSD semantic audit index

Status: started.

Branch:

```text
dev/schema-integration
```

Purpose:

This audit tracks a source-based comparison between the public VDV 301 PDF writings and the XSD files present in the integration branch.

Important limits:

- This is not an official VDV statement.
- Files from open PRs, forks, or local candidates stay labelled as candidate/integration material until accepted upstream or published by VDV.
- Semantic PDF/XSD checks are performed in small, traceable blocks.
- Local XSD compilation and sample XML validation remain a later technical validation step.

## Start here / handoff

For continuing this audit in a new chat, start with:

```text
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF.md
```

Then read:

```text
docs/pdf_xsd_semantic_audit/findings.md
docs/pdf_xsd_semantic_audit/validation_backlog.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv
```

Always fetch the current `dev/schema-integration` branch ref before continuing.

## Audit files

```text
00_index.md
AUDIT_HANDOFF.md
01_common_enums_v2_1_to_v2_4.md
01a_common_enums_v2_4_table_check.md
01b_common_enums_v2_4_continuation.md
01c_common_enums_additional_text_message_history.md
01d_common_enums_v2_4_enumeration_first_pass.md
01e_common_enums_v2_4_enumeration_second_pass.md
findings.md
validation_backlog.md
generated/enumerations_v2_4_xsd_inventory.csv
generated/enumerations_v2_4_xsd_inventory.md
```

Related tool:

```text
tools/export_xsd_enumerations.py
```

## Status overview

| Area | Status | Notes |
|---|---|---|
| Common structures / enumerations V2.1-V2.4 | started | Version-history deltas and V2.4 table-level checks are in progress. |
| Common/Enums V2.4 XSD enumeration inventory | available | XSD-side CSV/Markdown inventory has been added for `IBIS-IP_Enumerations_V2.4.xsd`. |
| Common/Enums V2.4 PDF enumeration inventory | pending | Next step: extract PDF tables 65-104 and compare exactly/case-sensitively to the XSD inventory. |
| Common structures / enumerations V1.0-V2.0 | pending | Needs older PDF/table extraction and XSD comparison. |
| DeviceManagementService | pending | DMS V2.4 candidate already has a separate derivation document; needs integration into this audit format. |
| TicketValidationService | pending | Must account for upstream V2.4 include state and open PR/candidate material. |
| CustomerInformationService | pending | Coverage and provenance unclear for older versions. |
| Remaining services | pending | To be split into small blocks after Common/Enums. |

## Evidence policy

Each finding should distinguish:

```text
PDF-derived fact
XSD-derived fact
inference / audit interpretation
open validation task
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

## Continuity policy

After each meaningful block:

```text
1. Commit audit file changes to dev/schema-integration.
2. Update findings.md if a CE finding is opened or a finding state changes.
3. Update AUDIT_HANDOFF.md when the continuation point changes materially.
4. Report the final branch commit SHA to the user.
```
