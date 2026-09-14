# VDV 301 finding semantic classification model

Status: design baseline for the post-freeze Known-Issues Knowledge Base.

This model is layered **on top of** the frozen finding/provenance baseline and does not mutate or reinterpret the frozen audit record.

Frozen source baseline:

- `audit_registry/finding_provenance_baseline_2026-09-14.json`
- baseline payload SHA-256: `d5bf14df302d57a0fc3d71792e1cb00583fafd3e9c7efd19721fd0de353dd576`
- finding entries SHA-256: `411519c4aaaeb370dfa336d729988d37007a78dfaf5bc6d5fcfb1dfa3f49f792`
- 192 terminal findings, 0 pending, 0 unresolved

## Purpose

The classification layer turns confirmed audit findings into a VDV-301 Known-Issues Knowledge Base suitable for SDK diagnostics.

It must support two goals at the same time:

1. **Normative correctness**: validation follows the selected authoritative XSD family. A known specification issue must never silently change an XSD-valid result into invalid, or an XSD-invalid result into valid.
2. **Useful diagnostics**: when a failure or warning is related to a known PDF/XSD/provenance inconsistency, the SDK should explain that clearly, identify the likely source of the inconsistency, cite the relevant official material, and recommend the schema-conformant form.

The classification layer therefore comments on the normative validation result; it does not override it.

## Mandatory review rule

Do **not** bulk-classify findings by keywords.

Every finding must be reviewed individually or in a tightly related service/version block. The review should use, where applicable:

- the selected XSD and its dependency graph;
- the byte-pinned official PDF;
- Common Conventions and other shared VDV-301 rules;
- parallel operations or structures in the same service;
- equivalent patterns in other services;
- version history and later official corrections;
- exact official release-tag provenance;
- candidate/integration provenance where explicitly separated from official authority;
- XML Schema semantics;
- HTTP/XML/protocol standards on which the interface depends;
- executable validation evidence;
- the frozen audit terminal-state source.

A classification may use technical inference, but inference must be labelled as inference and must not be presented as an official VDV statement.

## Core authority rule

```text
selected authoritative XSD = normative validation authority
Known-Issues layer        = explanatory/advisory knowledge
```

Consequences:

- no compatibility alias is introduced merely because a PDF contains a different name or type;
- no XSD rejection is suppressed because the PDF appears to support the rejected form;
- no XSD-accepted value is rejected solely by the Known-Issues layer;
- if no strict official XSD profile can be established, the profile is reported as unsupported/fail-closed rather than guessed;
- candidate/integration schemas must never be described as official release authority.

## Multi-axis classification

A single `category` is intentionally insufficient. Each finding is classified on several independent axes.

### 1. `primary_surface`

Where is the suspected or confirmed issue primarily located?

- `xsd`
- `pdf`
- `cross_artifact`
- `provenance`
- `external_standard`
- `contextual`
- `none`
- `undetermined`

### 2. `primary_issue_kind`

Stable machine-readable issue kind. Initial controlled vocabulary:

- `identifier_typo`
- `identifier_case_error`
- `missing_separator_or_punctuation`
- `stale_identifier_after_rename`
- `wrong_type_reference`
- `wrong_enum_reference`
- `wrong_structure_reference`
- `wrong_operation_reference`
- `missing_operation_inventory_member`
- `stale_operation_inventory_member`
- `internal_schema_inconsistency`
- `cardinality_mismatch`
- `structure_mismatch`
- `namespace_mismatch`
- `stale_diagram_or_example`
- `documentation_spelling`
- `version_routing_issue`
- `release_authority_gap`
- `semantic_contradiction`
- `intentional_design_misread`
- `editorial_residue`
- `other`

A finding may also carry `secondary_issue_kinds`.

### 3. `defect_assessment`

This is an assessment, not a replacement for the frozen finding state.

- `confirmed_pdf_defect`
- `likely_pdf_defect`
- `confirmed_xsd_defect`
- `likely_xsd_defect`
- `cross_artifact_mismatch`
- `authority_gap`
- `intentional_design`
- `non_defect`
- `undetermined`

Use `confirmed_*` only where the evidence supports the defect location directly. Otherwise use `likely_*` and preserve the confidence level.

### 4. `confidence`

- `confirmed`
- `high`
- `medium`
- `low`

The confidence applies to the semantic/defect assessment, not to the normative XSD result.

### 5. `validation_effect`

One or more runtime/engineering consequences:

- `xsd_rejects_pdf_documented_form`
- `xsd_accepts_semantically_questionable_form`
- `xsd_internal_inventory_incomplete`
- `xsd_internal_inventory_stale`
- `pdf_can_mislead_implementation`
- `code_generation_or_discovery_affected`
- `documentation_only`
- `strict_profile_unavailable`
- `no_runtime_effect`
- `other`

### 6. `sdk_behavior`

How the Known-Issues layer should behave if the finding is matched at runtime:

- `error_with_advisory`
- `valid_with_advisory`
- `warning`
- `info`
- `unsupported_profile`
- `no_runtime_diagnostic`

The normative XSD validator still owns the actual `VALID`/`INVALID` decision.

## Semantic basis

Every manually reviewed finding must record one or more `semantic_basis` entries. Initial controlled basis types:

- `official_pdf_explicit`
- `official_xsd_explicit`
- `xsd_internal_consistency`
- `parallel_operation_pattern`
- `parallel_structure_pattern`
- `common_conventions`
- `cross_service_pattern`
- `version_history`
- `later_official_correction`
- `official_release_provenance`
- `candidate_integration_provenance`
- `executable_validation`
- `xml_schema_semantics`
- `http_standard`
- `external_protocol_standard`
- `domain_semantics`
- `technical_inference`

Each basis entry contains a short evidence note. If `technical_inference` is used, it must be clear that it is our engineering assessment rather than quoted normative text.

## Bilingual user-facing diagnostics

Machine codes are stable English identifiers. All human-facing SDK text is mandatory in **German and English**.

Each reviewed finding provides:

- `title_de`, `title_en`
- `short_de`, `short_en`
- `long_de`, `long_en`
- `recommendation_de`, `recommendation_en`

### Writing rules

The text should be understandable to an integrator who knows the interface but is not an XSD specialist.

Prefer:

> Die verwendete Bezeichnung existiert in dieser XSD-Version nicht.

instead of:

> The QName lookup failed against the global element symbol space.

Technical terms may be used where helpful, but should be explained in plain language.

Do not write categorical claims such as `the XSD is wrong` unless the defect location is directly confirmed. Prefer calibrated language:

- `Die Hinweise sprechen stark dafür, dass ...`
- `Sehr wahrscheinlich handelt es sich um ...`
- `The available evidence strongly indicates that ...`
- `This is very likely ...`

### Diagnostic structure

Long explanations should answer, in this order where applicable:

1. What did the validator observe?
2. Why is the normative result VALID/INVALID/UNSUPPORTED?
3. What known specification inconsistency is relevant?
4. What should the implementer use or do?
5. Which official sources and finding support the statement?

## Example diagnostic policy

If the PDF documents an old identifier but the selected XSD only accepts the renamed identifier:

```text
normative_result = INVALID
known_issue      = true
sdk_behavior     = error_with_advisory
```

The SDK may explain the documentation inconsistency and recommend the XSD-valid identifier, but it must not accept the stale PDF identifier as an alias.

If the XSD appears internally inconsistent but the submitted XML is still valid according to the selected XSD:

```text
normative_result = VALID
known_issue      = true
sdk_behavior     = valid_with_advisory or warning
```

The advisory may explain the likely XSD defect, but it must not invalidate the document.

## Runtime matching

Classification and runtime detection are separate concerns.

Each finding therefore has a `runtime_match` object with a state such as:

- `not_designed`
- `candidate`
- `reviewed`
- `implemented`
- `not_applicable`

Possible later trigger types include:

- exact XSD validation error + QName/path;
- rejected element/attribute/type name;
- rejected enumeration value;
- selected service/version profile;
- schema operation-group inventory check;
- structural post-validation rule;
- profile-selection/provenance failure.

No trigger should be activated solely from a guessed textual similarity.

## Source references

A classification entry should cite at least:

- `finding_id`;
- frozen baseline terminal-state source;
- relevant official PDF source/version and page(s), where applicable;
- relevant XSD file/symbol/version, where applicable;
- executable evidence ID/run where applicable;
- any Common Conventions, standards, or version-history source used in the semantic assessment.

## Review lifecycle

Suggested states:

- `unreviewed`
- `in_review`
- `manually_reviewed`
- `runtime_mapping_reviewed`
- `sdk_ready`

A finding is not `sdk_ready` merely because its high-level category has been assigned. Its bilingual explanation, source references, semantic basis, and runtime-match policy must also be reviewed.

## Pilot

The first pilot classification intentionally covers different failure modes:

- `TVS-001` — likely XSD operation-inventory omission;
- `TVS-002` — wrong semantic type reference in the PDF;
- `TVS-003` — stale PDF identifier after an official rename;
- `TSM-002` — stale XSD operation-group member after root-name correction;
- `TSM-003` — stale PDF diagram relative to the exact XSD structure;
- `TSD-004` — wrong response-structure reference in the PDF.

The pilot exists to validate the model before the remaining findings are reviewed block by block.
