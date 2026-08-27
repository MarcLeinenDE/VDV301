# AnalogRadioService findings register addendum

Status: supplemental register; V2.4 semantic/provenance first-pass closure completed.

Authority rule:

```text
The branch AnalogRadioService V2.4 XSD is candidate/integration material sourced exactly from open VDVde/VDV301 PR #27.
Validation follows that XSD only when the candidate/integration profile is explicitly selected.
PDF discrepancies do not create executable aliases.
```

## ARA-001 - public V2.4 document / schema release-provenance gap

Classification:

```text
mismatch_kind: schema_family_or_provenance
likely_source_issue: schema_family_or_provenance_gap
classification_confidence: high
version_scope: V2.4
validation_behavior: candidate/integration profile only unless official release appears
final_handling_bucket: official_schema_family_clarification_candidate
```

Observation:

```text
VDV 301-2-19 V2.4 is publicly available and its XML example references IBIS-IP_AnalogRadioService_V2.4.xsd.
Official VDVde/VDV301 GitHub releases observed during the audit stop at VDV-301-2.3.
Current upstream master lacks the AnalogRadioService V2.4 XSD.
Open PR #27 adds the exact XSD blob used in dev/schema-integration.
```

## ARA-002 - TransmitterType PDF table label vs Transmitter

Classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
version_scope: V2.4 PDF
validation_behavior: exact element name Transmitter
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

Observation:

```text
PDF table says TransmitterType.
Candidate XSD says Transmitter.
The XSD screenshot embedded in the same PDF page says Transmitter.
The complete XML example says Transmitter.
```

## ARA-003 - Transmitter cardinality PDF 1:1 vs XSD 0:1

Classification:

```text
mismatch_kind: cardinality
likely_source_issue: cardinality_mismatch_candidate
subclassification: xsd_more_permissive_than_pdf
classification_confidence: high
version_scope: V2.4
validation_behavior: XSD permits omission of Transmitter
final_handling_bucket: local_validation_required
```

Observation:

```text
PDF table says TransmitterType 1:1.
Candidate XSD defines Transmitter with minOccurs=0.
The PDF's embedded XSD screenshot visibly shows minOccurs=0.
```

## ARA-004 - URI example SendFFSKTelegram vs SendTelegram

Classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
version_scope: V2.4 PDF
validation_behavior: operation SendTelegram
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

Observation:

```text
Operation table, detailed operation description, candidate XSD and XML example use SendTelegram.
URI example uses /AnalogRadioService/SendFFSKTelegram.
```
