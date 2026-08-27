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
- Mixed-version real-world systems are expected; validation must be service-version scoped.

## Validation authority

VDV 301-2 V2.4 General Conventions state that, in case of inconsistencies, the XSD definitions take precedence over the documentation.

Therefore this audit and the eventual tool behaviour follow this rule:

```text
Executable validation authority: XSD
PDF evidence: documented and shown as explanatory note when it differs from XSD
```

Detailed policies:

```text
docs/pdf_xsd_semantic_audit/VALIDATION_AUTHORITY.md
docs/pdf_xsd_semantic_audit/MIXED_VERSION_VALIDATION_PREMISE.md
```

## Start here / handoff

For continuing this audit in a new chat, start with:

```text
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF.md
```

Then read:

```text
docs/pdf_xsd_semantic_audit/00_index.md
docs/pdf_xsd_semantic_audit/AUDIT_SCOPE_MATRIX.md
docs/pdf_xsd_semantic_audit/MIXED_VERSION_VALIDATION_PREMISE.md
docs/pdf_xsd_semantic_audit/VALIDATION_AUTHORITY.md
docs/pdf_xsd_semantic_audit/findings.md
docs/pdf_xsd_semantic_audit/validation_backlog.md
docs/pdf_xsd_semantic_audit/OFFICIAL_PR_CANDIDATES_AFTER_AUDIT.md
docs/pdf_xsd_semantic_audit/generated/audit_scope_matrix.csv
```

Always fetch the current `dev/schema-integration` branch ref before continuing.

## Audit files

```text
00_index.md
AUDIT_HANDOFF.md
AUDIT_SCOPE_MATRIX.md
MIXED_VERSION_VALIDATION_PREMISE.md
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
03_tvs_v2_2_v2_3_v2_4_include_semantic_audit.md
04_common_enums_historical_v1_0_to_v2_4_plan.md
04a_common_enums_v1_0_v2_0_history.md
04b_common_enums_v2_0_v2_1_history.md
04c_common_enums_v2_1_v2_2_history.md
04d_common_enums_v2_2_v2_3_history.md
04e_common_enums_v2_3_v2_4_history_and_closure.md
findings.md
validation_backlog.md
generated/audit_scope_matrix.csv
generated/enumerations_v1_0_v2_0_xsd_inventory.csv
generated/enumerations_v1_0_vs_v2_0_xsd_diff.csv
generated/enumerations_v1_0_vs_v2_0_xsd_diff.md
generated/enumerations_v2_0_vs_v2_1_xsd_diff.csv
generated/enumerations_v2_0_vs_v2_1_xsd_diff.md
generated/enumerations_v2_1_vs_v2_2_xsd_diff.csv
generated/enumerations_v2_1_vs_v2_2_xsd_diff.md
generated/enumerations_v2_2_vs_v2_3_xsd_diff.csv
generated/common_v2_2_vs_v2_3_structure_delta.csv
generated/enumerations_v2_3_vs_v2_4_xsd_diff.csv
generated/common_v2_3_vs_v2_4_structure_delta.csv
generated/enumerations_v2_4_xsd_inventory.csv
generated/enumerations_v2_4_xsd_inventory.md
generated/enumerations_v2_4_pdf_inventory.csv
generated/enumerations_v2_4_pdf_vs_xsd_diff.csv
generated/common_v2_4_datatypes_xsd_inventory.csv
generated/common_v2_4_datatypes_xsd_inventory.md
```

Related tools:

```text
tools/export_xsd_enumerations.py
```

## Status overview

| Area | Status | Notes |
|---|---|---|
| Audit scope matrix | available | Master checklist for public PDF versions vs observed XSD files. |
| Mixed-version validation premise | available | Documents why all historical service versions must remain separately validatable. |
| Validation authority policy | available | XSD precedence over documentation is documented for audit and tool behaviour. |
| Official PR candidate register | available | Tracks possible post-audit correction PR candidates; no PRs during audit. |
| Common/Enums V2.4 XSD/PDF inventory and diff | partial/completed first pass | V2.4 enum diff and core structure pass exist; visual checks deferred. |
| Common/Enums V1.0-V2.4 historical audit | first pass completed | 04a through 04e complete; CE-001 closed as OK with note; local validation still pending. |
| DeviceManagementService V2.4/history | first pass completed | No DMS-specific mismatch opened; validation backlog VB-005 created. |
| TicketValidationService | first pass completed for V2.2/V2.3/V2.4 | TVS-001 and TVS-002 opened; V2.1 historical coverage still pending. |
| CustomerInformationService | next | Next recommended service-level historical block. |
| Remaining services | pending | To be split into small service-version blocks. |

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
2. Update findings.md if a CE/service finding is opened or a finding state changes.
3. Update validation_backlog.md when deferred checks or final-review gates change.
4. Update AUDIT_HANDOFF.md when the continuation point changes materially.
5. Report the final branch commit SHA to the user.
```