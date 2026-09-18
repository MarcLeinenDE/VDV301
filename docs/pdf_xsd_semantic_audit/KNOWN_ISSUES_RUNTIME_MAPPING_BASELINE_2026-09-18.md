# Known-Issues runtime-mapping baseline — 2026-09-18

Status: **reviewed inventory generated / no runtime matcher implemented**.

## Purpose

This baseline is the first handoff from the completed 192/192 semantic Known-Issues classification into the SDK runtime layer.

It is deliberately **declarative**. It does not activate text matching, payload rewriting, compatibility aliases, alternative validation outcomes, or any other runtime behaviour.

## Source

- semantic registry: `audit_registry/finding_semantic_classification_v0.1.json`
- semantic registry Git blob: `7ebc8c98120ae7b1740629729037c05cef4b0f38`
- semantic registry state: **complete**
- frozen baseline payload SHA-256: `d5bf14df302d57a0fc3d71792e1cb00583fafd3e9c7efd19721fd0de353dd576`

## Generated mapping inventory

The generator includes only semantic entries whose `runtime_match.state` is already `reviewed`.

Current semantic runtime distribution:

```text
reviewed       30
candidate      51
not_designed    1
not_applicable 110
implemented     0
```

The 30 reviewed mappings are represented by activation class:

```text
error_with_advisory  -> xsd_invalid_advisory
valid_with_advisory  -> xsd_valid_advisory
unsupported_profile  -> profile_resolution_failure
warning              -> resolver_or_profile_warning
no_runtime_diagnostic -> routing_only
```

These activation classes are implementation categories only. The copied `trigger_descriptions` remain human-reviewed descriptions and are explicitly **not executable matchers**.

## Safety and authority boundary

For every mapping:

```text
authority_guard = selected_xsd_result_remains_normative
implementation_state = reviewed_not_implemented
```

Therefore this baseline cannot:

- make XSD-invalid XML valid;
- make XSD-valid XML invalid;
- silently normalize a PDF spelling into a schema alias;
- select candidate/integration authority as official;
- match a payload merely because text looks similar to a finding description.

Unsupported strict profiles remain fail-closed.

## Deterministic generation

Files:

- `sdk_manifest/known_issues_runtime_mapping_v0.1.json`
- `sdk_manifest/known_issues_runtime_mapping_v0.1.schema.json`
- `tools/generate_known_issues_runtime_mapping_v0_1.py`
- `tools/validate_known_issues_runtime_mapping_v0_1.py`

The validator regenerates the manifest from the complete semantic registry and requires byte-identical output. It also requires exact equality of finding IDs, service, issue kind, SDK behaviour, version/authority scope and reviewed trigger descriptions.

## Gate

GitHub Actions run **35343951758** completed successfully.

The gate confirmed:

- exactly **30 reviewed mappings**;
- **0 implemented mappings**;
- deterministic regeneration is byte-identical;
- SDK manifest v0.1 self-test passes;
- all **50 root XSDs** compile;
- the gate itself is read-only and does not mutate repository content.

## Next phase

The next work is runtime-mapping review, not implementation by bulk conversion.

1. Review the **51 candidate** mappings in tightly related service/version blocks.
2. Resolve **DRTIME10-002**, the sole `not_designed` mapping.
3. Only after a mapping is reviewed, replace free-text trigger descriptions with structured profile-specific match conditions.
4. Add dedicated positive/negative evidence before marking any mapping `implemented`.

Official-facing remediation and XSD mutation remain unauthorized.
