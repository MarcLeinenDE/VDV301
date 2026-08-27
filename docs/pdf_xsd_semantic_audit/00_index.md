# PDF/XSD semantic audit index

Status: started.

Branch:

```text
dev/schema-integration
```

Purpose:

This audit tracks a source-based comparison between the public VDV 301 PDF writings and the XSD files present in the integration branch.

Long-term target:

```text
Complete PDF-vs-XSD semantic comparison for all public VDV301 writings and schema-relevant versions V1.0 through V2.4.
```

Important limits:

- This is not an official VDV statement.
- Files from open PRs, forks, or local candidates stay labelled as candidate/integration material until accepted upstream or published by VDV.
- Semantic PDF/XSD checks are performed in small, traceable blocks.
- Local XSD compilation and sample XML validation remain a later technical validation step.
- Possible official correction PRs are tracked only as post-audit candidates and are not opened during the audit.
- Manual/visual PDF checks are explicitly allowed to remain deferred while non-visual audit work continues.

## Validation authority

VDV 301-2 V2.4 General Conventions state that, in case of inconsistencies, the XSD definitions take precedence over the documentation.

Therefore this audit and the eventual tool behaviour follow this rule:

```text
Executable validation authority: XSD
PDF evidence: documented and shown as explanatory note when it differs from XSD
```

Detailed policy:

```text
docs/pdf_xsd_semantic_audit/VALIDATION_AUTHORITY.md
```

## Start here / handoff

For continuing this audit in a new chat, start with:

```text
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF.md
```

Then read:

```text
docs/pdf_xsd_semantic_audit/00_index.md
docs/pdf_xsd_semantic_audit/VALIDATION_AUTHORITY.md
docs/pdf_xsd_semantic_audit/findings.md
docs/pdf_xsd_semantic_audit/validation_backlog.md
docs/pdf_xsd_semantic_audit/OFFICIAL_PR_CANDIDATES_AFTER_AUDIT.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_vs_xsd_diff.csv
```

Always fetch the current `dev/schema-integration` branch ref before continuing.

## Audit files

```text
00_index.md
AUDIT_HANDOFF.md
VALIDATION_AUTHORITY.md
OFFICIAL_PR_CANDIDATES_AFTER_AUDIT.md
01_common_enums_v2_1_to_v2_4.md
01a_common_enums_v2_4_table_check.md
01b_common_enums_v2_4_continuation.md
01c_common_enums_additional_text_message_history.md
01d_common_enums_v2_4_enumeration_first_pass.md
01e_common_enums_v2_4_enumeration_second_pass.md
01f_common_enums_v2_4_pdf_vs_xsd_enum_diff.md
01g_common_enums_v2_4_datatypes_core_structures.md
01h_common_enums_v2_4_core_data_structures.md
01i_common_enums_v2_4_remaining_data_structures_part1.md
01j_common_enums_v2_4_remaining_data_structures_part2.md
01k_common_enums_v2_4_structure_closure.md
01l_common_enums_v2_4_deferred_scope_resolution.md
02_dms_v2_4_pdf_xsd_audit.md
02a_dms_v2_2_v2_3_v2_4_history_compare.md
findings.md
validation_backlog.md
generated/enumerations_v2_4_xsd_inventory.csv
generated/enumerations_v2_4_xsd_inventory.md
generated/enumerations_v2_4_pdf_inventory.csv
generated/enumerations_v2_4_pdf_vs_xsd_diff.csv
generated/common_v2_4_datatypes_xsd_inventory.csv
generated/common_v2_4_datatypes_xsd_inventory.md
```

Related tool:

```text
tools/export_xsd_enumerations.py
```

## Status overview

| Area | Status | Notes |
|---|---|---|
| Validation authority policy | available | XSD precedence over documentation is documented for audit and tool behaviour. |
| Official PR candidate register | available | Tracks possible post-audit correction PR candidates; no PRs during audit. |
| Common/Enums V2.4 XSD enumeration inventory | available | XSD-side CSV/Markdown inventory exists for `IBIS-IP_Enumerations_V2.4.xsd`. |
| Common/Enums V2.4 PDF enumeration inventory | available | PDF-side inventory exists for VDV 301-2-1 V2.4 tables 65-104. |
| Common/Enums V2.4 PDF/XSD enumeration diff | completed first pass | Exact/case-sensitive diff exists; findings CE-004 and CE-006 through CE-010 remain open for historical classification. |
| Common/Enums V2.4 datatypes/core structures | mostly completed first pass | Datatype inventory, InternationalTextType and NetexMode are documented in 01g. |
| Common/Enums V2.4 common structures | visual checks deferred | 01h, 01i, 01j, 01k and 01l cover most structures; SB-005 resolved; CE-015/CE-017/ZoneType visual checks deferred. |
| DeviceManagementService V2.4 | first pass completed | `02_dms_v2_4_pdf_xsd_audit.md`; no new DMS-specific mismatch opened; validation backlog VB-005 created. |
| DMS V2.2/V2.3/V2.4 history | first pass completed | `02a_dms_v2_2_v2_3_v2_4_history_compare.md`; confirms DMS V2.4 candidate scope remains narrow; no new DMS-specific CE finding. |
| Common structures / enumerations V1.0-V2.3 | pending | Needs older PDF/table extraction and XSD comparison. |
| TicketValidationService | next | TVS V2.2/V2.3/V2.4 include and semantic history is the recommended next non-visual block. |
| CustomerInformationService | pending | Coverage and provenance unclear for older versions. |
| Remaining services | pending | To be split into small blocks after Common/Enums/DMS/TVS. |

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
Confirmed PDF/XSD value discrepancy
```

## Continuity policy

After each meaningful block:

```text
1. Commit audit file changes to dev/schema-integration.
2. Update findings.md if a CE finding is opened or a finding state changes.
3. Update validation_backlog.md when deferred checks or final-review gates change.
4. Update AUDIT_HANDOFF.md when the continuation point changes materially.
5. Report the final branch commit SHA to the user.
```
