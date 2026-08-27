# Handoff delta - finding classification policy

Status: supplemental handoff delta after adopting finding classification policy.

New files:

```text
docs/pdf_xsd_semantic_audit/FINDING_CLASSIFICATION_POLICY.md
docs/pdf_xsd_semantic_audit/generated/finding_classification_taxonomy.csv
```

Decision:

```text
Findings are not treated as one uniform defect category.
They must be grouped by mismatch kind, likely source issue, confidence and final handling bucket before any official-facing action is chosen.
```

Core rule remains:

```text
Validation follows the selected XSD family.
PDF differences are explanatory/provider-facing unless and until an official corrected schema or documentation change exists.
```

Important classification groups:

```text
xsd_typo_candidate
pdf_table_or_documentation_error_candidate
pdf_label_or_heading_error_candidate
cardinality_mismatch_candidate
service_modelling_or_generic_response_candidate
schema_family_or_provenance_gap
ok_with_note
```

Examples:

```text
Likely XSD typo candidates:
  LS-001 HoriziontalDilutionOfPrecision vs HorizontalDilutionOfPrecision.
  CE-016 GlobalCardStausID vs GlobalCardStatusID.
  CE-017 TSPPoint Desciption vs Description, pending visual PDF confirmation.

Likely PDF/table documentation issue candidates:
  CE-007 / CE-008 casing differences where XSD semantics/history appear more coherent.
  CIS-005 MyOwnVehicleMode type inconsistency across CIS PDF tables.

Cardinality mismatch candidates:
  CE-005 / CE-011 / CE-012 / CE-014 / JIS-003.
```

Future action:

```text
When consolidating findings.md and the service addenda, add classification fields or a generated classification matrix.
Do not decide official PR scope until findings are classified, local validation has run and the final review separates XSD correction candidates from PDF/documentation clarification candidates.
```
