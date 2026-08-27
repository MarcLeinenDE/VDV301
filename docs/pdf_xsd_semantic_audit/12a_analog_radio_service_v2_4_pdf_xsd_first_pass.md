# AnalogRadioService V2.4 PDF/XSD first pass

Status: detailed semantic/provenance first pass completed against the branch candidate XSD. Local schema compilation/sample validation remains pending.

Source starter:

```text
docs/pdf_xsd_semantic_audit/12_analog_radio_service_historical_start.md
```

## 1. Selected candidate validation family

```text
IBIS-IP_AnalogRadioService_V2.4.xsd
-> IBIS-IP_common_V2.3.xsd
-> IBIS-IP_Enumerations_V2.2.xsd
```

Provenance:

```text
Analog service XSD: exact blob from open VDVde/VDV301 PR #27
blob 48fb303b80936d2d762f0889ce0c359e04c16e5b
```

This profile is executable candidate/integration material only. It is not labelled an official VDV release.

## 2. Operation inventory

The PDF says the service has one operation:

```text
SendTelegram
```

The candidate XSD group and top-level element use:

```text
AnalogRadioService.SendTelegram
```

Result:

```text
Aligned for the actual operation definition.
```

The operation has a request structure and no response data according to the PDF. The service XSD contains the request element only; no response element is introduced.

## 3. RadioTelegramStructure

Aligned fields:

```text
RawTelegram        PDF 1:1 / XSD required
AnalogChannel      PDF 1:1 / XSD required
Bitrate            PDF 1:1 / XSD required
Repeats            PDF 0:1 / XSD minOccurs=0
MaxRepeatInterval  PDF 0:1 / XSD minOccurs=0
```

Types also align for those fields.

### ARA-002 - field label mismatch

PDF table:

```text
TransmitterType
```

Candidate XSD:

```text
Transmitter
```

The PDF's own embedded XSD screenshot and complete XML example also use `Transmitter`.

Classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

Validation behaviour:

```text
Only `Transmitter` is accepted according to the selected candidate XSD.
Do not create a compatibility alias `TransmitterType`.
```

### ARA-003 - cardinality mismatch

PDF table:

```text
TransmitterType 1:1
```

Candidate XSD:

```text
Transmitter type="TransmitterStructure" minOccurs="0"
```

Classification:

```text
mismatch_kind: cardinality
likely_source_issue: cardinality_mismatch_candidate
subclassification: xsd_more_permissive_than_pdf
classification_confidence: high
final_handling_bucket: local_validation_required
```

Evidence strength is unusually high because the same PDF page embeds an XSD screenshot showing `minOccurs=0` directly below the contradictory table.

Validation behaviour:

```text
A RadioTelegramStructure without Transmitter is expected to be valid against the selected XSD.
This must still be demonstrated by local sample validation before the audit calls the sample validated.
```

## 4. TransmitterStructure

PDF and XSD align:

```text
LeadTime 0:1 IBIS-IP.unsignedInt
HoldTime 0:1 IBIS-IP.unsignedInt
```

No separate finding opened.

## 5. BitrateEnumeration

PDF and XSD align on values:

```text
1200
2400
```

No separate finding opened.

## 6. ARA-004 - wrong operation name in URI example

The PDF defines and repeatedly names the only operation as:

```text
SendTelegram
```

The candidate XSD and XML example use:

```text
AnalogRadioService.SendTelegram
```

But the URI example uses:

```text
192.168.1.2:8080/AnalogRadioService/SendFFSKTelegram
```

Classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

Tool implication:

```text
Do not infer `SendFFSKTelegram` as an operation alias from the example.
Use `SendTelegram` for operation routing according to the selected XSD and the normative operation description.
A provider-facing diagnostic may mention the stale/inconsistent URI example.
```

## 7. ARA-001 - provenance/routing gap

Repository state checked:

```text
Public VDV 301-2-19 V2.4 writing exists.
The writing's XML example references IBIS-IP_AnalogRadioService_V2.4.xsd.
VDVde/VDV301 GitHub official releases currently stop at VDV-301-2.3.
Current upstream master does not contain the AnalogRadioService V2.4 XSD.
Open PR #27 contains the exact XSD used in dev/schema-integration.
```

Classification:

```text
mismatch_kind: schema_family_or_provenance
likely_source_issue: schema_family_or_provenance_gap
classification_confidence: high
final_handling_bucket: official_schema_family_clarification_candidate
```

SDK routing rule:

```text
Default official-release-only profile:
  do not silently claim strict official-release AnalogRadioService V2.4 validation.

Explicit candidate/integration profile:
  AnalogRadioService V2.4 PR #27 candidate
  + Common V2.3
  + Enumerations V2.2
```

## 8. Dependency-family note

The Analog V2.4 candidate's use of Common V2.3 is retained exactly.

This is not treated as a version-number error:

```text
service version and dependency version do not have to match numerically.
```

Because Common V2.3 includes Enumerations V2.2, the transitive pool is also preserved exactly.

No Common V2.4 or Enumerations V2.4 substitution is allowed unless a different selected Analog XSD explicitly requires it.

## 9. Technical validation backlog

```text
ARA-VB-001: compile AnalogRadioService V2.4 candidate + Common V2.3 + Enumerations V2.2.
ARA-VB-002: positive SendTelegram with required fields only and no Transmitter.
ARA-VB-003: positive SendTelegram with Transmitter/LeadTime/HoldTime.
ARA-VB-004: negative sample using TransmitterType instead of Transmitter.
ARA-VB-005: positive Bitrate 1200 and 2400; negative unsupported bitrate.
ARA-VB-006: operation-routing test SendTelegram positive vs SendFFSKTelegram unsupported for selected XSD profile.
ARA-VB-007: candidate-profile provenance assertion test: report candidate/integration authority, not official-release authority.
```

No local validation task above has been executed in this block.

## 10. Result

```text
Operation and most structure fields align.
ARA-001: confirmed schema-family/provenance gap between public writing and official GitHub release state; candidate XSD traceable to PR #27.
ARA-002: confirmed PDF table field-label candidate TransmitterType vs Transmitter.
ARA-003: confirmed cardinality mismatch candidate PDF 1:1 vs XSD 0:1.
ARA-004: confirmed PDF URI-example operation-name candidate SendFFSKTelegram vs SendTelegram.
Exact candidate dependency chain retained: Analog V2.4 -> Common V2.3 -> Enums V2.2.
No XSD modified.
No local compile/sample validation claimed.
```
