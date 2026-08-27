# Common findings register addendum after service-level audit discoveries

Status: supplemental Common register for findings discovered after the original CE-001..CE-017 first-pass chain. Keep separate until the main findings register is consolidated.

Authority rule:

```text
Validation follows the selected Common XSD version.
PDF table differences are explanatory evidence only.
No schema change is implied by opening or confirming a finding.
```

## CE-018 - ServiceIdentificationWithStateList cardinality PDF 1:* vs XSD 0:*

State: executable-confirmed historical cardinality mismatch.

Classification:

```text
mismatch_kind: cardinality
likely_source_issue: cardinality_mismatch_candidate
subclassification: xsd_more_permissive_than_pdf
classification_confidence: very high
version_scope: executable XSD behaviour confirmed V1.0, V2.0, V2.1, V2.2, V2.3, V2.4; checked PDF 1:* wording confirmed V2.1-V2.4
validation_behavior: XSD permits empty list
final_handling_bucket: official_documentation_or_schema_alignment_review_candidate
```

PDF evidence:

```text
Checked Common documents V2.1, V2.2, V2.3 and V2.4 each show ServiceIdentificationWithStateList / ServiceIdentificationWithState as 1:*.
```

Static XSD evidence:

```text
Checked Common XSD family defines:
ServiceIdentificationWithState minOccurs="0" maxOccurs="unbounded".
```

Executable evidence:

```text
GitHub Actions run: 33109768872
head tested: 2298f1297e9d2b00aacbf244f39f6c73587f713e
tool: tools/validate_ce018_service_identification_with_state_list.py
result: PASS
```

Executed versions:

```text
Common V1.0  empty list PASS; one-item list PASS
Common V2.0  empty list PASS; one-item list PASS
Common V2.1  empty list PASS; one-item list PASS
Common V2.2  empty list PASS; one-item list PASS
Common V2.3  empty list PASS; one-item list PASS
Common V2.4  empty list PASS; one-item list PASS
```

Impact:

```text
The executable Common XSD family consistently permits zero ServiceIdentificationWithState items.
For the checked V2.1-V2.4 documents, this conflicts with the documented 1:* cardinality.
SystemMonitoringService.GetServiceStatusResponseData is a direct consumer of this list structure.
```

Handling:

```text
Validation follows the selected XSD and must accept the empty list where the selected Common XSD does.
The SDK may emit a documentation-discrepancy diagnostic, but must not reject the XSD-valid empty list solely because of the PDF 1:* wording.
No XSD change is made in the audit branch.
```

## CE-019 - ServiceIdentificationWithStateList item type/reference PDF vs XSD

State: potential PDF table/documentation type discrepancy; visual confirmation pending.

Classification:

```text
mismatch_kind: type
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: medium-high pending visual PDF confirmation
version_scope: text extraction indicates persistence across checked V2.1-V2.4 documents
validation_behavior: exact XSD type ServiceIdentificationWithStateStructure
final_handling_bucket: unresolved_keep_open
```

Observed PDF extraction:

```text
The ServiceIdentificationWithStateList row names the item ServiceIdentificationWithState but the associated referenced structure/type is extracted as ServiceSpecificationWithState.
```

XSD evidence:

```text
The list element is ServiceIdentificationWithState with type ServiceIdentificationWithStateStructure.
```

Semantic context:

```text
ServiceIdentificationWithState includes the system-wide ServiceIdentification including the device on which the service runs.
ServiceSpecificationWithState describes a service specification/state at a device without the same system-wide identification wrapper.
The list is described as a list of all unique services and their state in the system, which is semantically consistent with the XSD type.
```

Visual-check note:

```text
Direct screenshots of the relevant VDV PDF pages repeatedly failed or timed out during this pass.
Do not raise confidence to final/confirmed PDF error until a visual table check is completed.
```

Impact:

```text
Validation follows ServiceIdentificationWithStateStructure.
Do not accept ServiceSpecificationWithStateStructure as an automatic alias based on PDF extraction.
```
