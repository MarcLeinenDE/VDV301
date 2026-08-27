# AnalogRadioService V2.4 findings and first-pass closure

Status: semantic/provenance first-pass closure completed. Local XSD compilation/sample validation remains pending.

Source blocks:

```text
docs/pdf_xsd_semantic_audit/12_analog_radio_service_historical_start.md
docs/pdf_xsd_semantic_audit/12a_analog_radio_service_v2_4_pdf_xsd_first_pass.md
```

## Candidate routing closure

```text
Public document: VDV 301-2-19 AnalogRadioService V2.4
Candidate XSD authority: VDVde/VDV301 PR #27
Candidate XSD blob: 48fb303b80936d2d762f0889ce0c359e04c16e5b
Dependency chain:
  AnalogRadioService V2.4 candidate
  -> Common V2.3
  -> Enumerations V2.2
```

Official-release status:

```text
No VDV-301-2.4 GitHub release tag observed.
Current official releases stop at VDV-301-2.3.
Current upstream master does not contain the AnalogRadioService V2.4 XSD.
PR #27 remains open/unmerged.
```

Therefore no official-release-only resolver may silently promote this candidate to official status.

## Findings

### ARA-001 - public V2.4 writing vs candidate-only XSD provenance

```text
classification: schema_family_or_provenance_gap
confidence: high
handling: explicit candidate/integration route; official schema-family clarification candidate
```

### ARA-002 - TransmitterType vs Transmitter

```text
PDF table: TransmitterType
XSD + embedded XSD screenshot + XML example: Transmitter
classification: pdf_table_or_documentation_error_candidate
confidence: high
handling: validate exact XSD name; documentation clarification candidate
```

### ARA-003 - Transmitter cardinality

```text
PDF table: 1:1
XSD: 0:1
classification: cardinality_mismatch_candidate / xsd_more_permissive_than_pdf
confidence: high
handling: local positive sample without Transmitter required before technical-validation closure
```

### ARA-004 - URI example operation name

```text
Defined operation: SendTelegram
URI example: SendFFSKTelegram
classification: pdf_table_or_documentation_error_candidate
confidence: high
handling: no alias; documentation clarification candidate
```

## SDK implications

```text
- Separate public-document version from schema-authority status.
- Support explicit candidate/integration schema profiles.
- Preserve Analog V2.4 -> Common V2.3 -> Enums V2.2 exactly.
- Do not force V2.4 dependencies for numeric symmetry.
- Do not accept TransmitterType or SendFFSKTelegram as automatic aliases.
- Provider diagnostics may explain the known PDF table/example inconsistencies.
```

## Validation status

```text
Semantic/provenance first pass: closed.
Local XSD compilation: not performed.
Sample XML validation: not performed.
No XSD modification: yes.
No PR/comment/merge action: yes.
```

## Next planned historical service block

Return to the earliest still-pending service in the scope matrix:

```text
docs/pdf_xsd_semantic_audit/13_passenger_counting_service_historical_start.md
```

Initial focus:

```text
PassengerCountingService public V1.0 and V2.1 writings.
Resolve official historical V1.0 XSD provenance/backfill from release tags if available.
Compare V1.0 -> V2.1 dependency and service deltas without latest-wins mapping.
```
