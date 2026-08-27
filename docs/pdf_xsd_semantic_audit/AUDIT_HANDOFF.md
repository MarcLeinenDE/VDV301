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

At the start of a new chat, read these files first:

```text
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF.md
docs/pdf_xsd_semantic_audit/00_index.md
docs/pdf_xsd_semantic_audit/VALIDATION_AUTHORITY.md
docs/pdf_xsd_semantic_audit/findings.md
docs/pdf_xsd_semantic_audit/validation_backlog.md
docs/pdf_xsd_semantic_audit/OFFICIAL_PR_CANDIDATES_AFTER_AUDIT.md
```

Then read the active detailed audit files:

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
docs/pdf_xsd_semantic_audit/03_tvs_v2_2_v2_3_v2_4_include_semantic_audit.md
```

Supporting generated inventories:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_vs_xsd_diff.csv
docs/pdf_xsd_semantic_audit/generated/common_v2_4_datatypes_xsd_inventory.md
docs/pdf_xsd_semantic_audit/generated/common_v2_4_datatypes_xsd_inventory.csv
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

## Core method and authority

```text
1. PDF tables/version histories are documentation evidence.
2. XSD files are executable validation authority.
3. In case of PDF/XSD inconsistency, validation follows XSD.
4. No schema correction is made during audit without an explicit separate approval.
5. Potential official PR candidates are collected only for end-of-audit review.
```

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

## Current DMS result

Files:

```text
docs/pdf_xsd_semantic_audit/02_dms_v2_4_pdf_xsd_audit.md
docs/pdf_xsd_semantic_audit/02a_dms_v2_2_v2_3_v2_4_history_compare.md
```

Result:

```text
No new DMS-specific PDF/XSD mismatch opened.
DMS V2.4 candidate remains limited to the documented DMS V2.4 technical correction scope plus V2.4 dependency-family alignment.
DMS V2.3 remains labelled as integration/fork/candidate comparison material, not official authority.
```

Validation task:

```text
VB-005 DMS V2.4 schema compile and targeted positive/negative XML samples.
```

## Current TVS result

File:

```text
docs/pdf_xsd_semantic_audit/03_tvs_v2_2_v2_3_v2_4_include_semantic_audit.md
```

Result:

```text
TVS V2.2 -> V2.3: no schema delta observed; V2.3 treated as PDF/documentation correction.
TVS V2.4: new GetCurrentShortHaulStops response/data structure is present and aligned with PDF table intent.
TVS V2.4 integration branch uses common V2.4 and Enumerations V2.4.
Official upstream master currently has TVS V2.4 with common V2.4 but Enumerations V2.2.
```

New service findings:

```text
TVS-001: GetCurrentShortHaulStopsResponse is defined top-level and has structures, but is missing from TicketValidationServiceOperations group.
TVS-002: VehicleData.RouteDeviation PDF table type RouteDirectionEnumeration vs XSD RouteDeviationEnumeration.
```

Backlog / validation:

```text
VB-006 TVS V2.4 schema compile, targeted samples and operation inventory check.
SB-010 TVS V2.2/V2.3/V2.4 include and semantic history completed first pass.
```

Official PR candidate register now tracks:

```text
PR-CAND-005: TVS V2.4 GetCurrentShortHaulStopsResponse operation-group omission, linked TVS-001.
PR-CAND-006: TVS V2.4 VehicleData.RouteDeviation PDF type-name mismatch, linked TVS-002.
```

No PR is to be opened during the audit.

## Established finding IDs

Common/Enums findings currently use `CE-001` through `CE-017`.
Service-specific TVS findings currently use `TVS-001` and `TVS-002`.
DMS first-pass did not open a DMS-specific finding.

## Next recommended task

Next non-visual audit step:

```text
CustomerInformationService V2.3 / V2.4 provenance, include and semantic history.
```

Alternative:

```text
Continue TVS backwards to V2.1/V2.2 PDF history if deeper TVS historical closure is desired before moving to CIS.
```

## Working style for continuity

After each meaningful block:

```text
1. Commit audit file changes to dev/schema-integration.
2. Update findings/backlog/PR-candidate registers as needed.
3. Update AUDIT_HANDOFF.md when the continuation point changes materially.
4. Report the final branch commit SHA to the user.
```
