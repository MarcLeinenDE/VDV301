# AnalogRadioService V2.4 historical audit start

Status: first-pass audit started from `dev/schema-integration` head `32bf406448f39218cdd6d0cb0543b465e75c497d`. Public VDV document, branch XSD provenance and exact candidate dependency chain resolved. Local XSD compilation/sample validation remains pending.

Scope:

```text
VDV 301-2-19 AnalogRadioService V2.4, 01/2023
IBIS-IP_AnalogRadioService_V2.4.xsd in dev/schema-integration
VDVde/VDV301 PR #27 candidate source
IBIS-IP_common_V2.3.xsd
IBIS-IP_Enumerations_V2.2.xsd
```

## 1. Authority and provenance policy

```text
Validation follows the selected XSD family when a candidate/integration profile is explicitly selected.
A public PDF does not by itself turn an open-PR XSD into official release material.
Historical official backfill may use release tags only.
Open PR material remains candidate/integration material even when it corresponds to a public VDV writing.
No dependency version is rewritten merely for numeric symmetry.
```

## 2. Public document

Observed public VDV document:

```text
VDV-Schrift 301-2-19
AnalogRadioService V2.4
01/2023
```

The document describes one HTTP/XML operation, `SendTelegram`, through which an on-board unit triggers an analogue-radio / traffic-light-pre-emption telegram at a radio device.

The document itself references the schema filename:

```text
IBIS-IP_AnalogRadioService_V2.4.xsd
```

in its XML example.

## 3. Official GitHub release status

Current `VDVde/VDV301` GitHub releases checked during this pass end at:

```text
VDV-301-2.3
```

No official VDV-301-2.4 release tag was observed.

Current upstream `master` does not contain:

```text
IBIS-IP_AnalogRadioService_V2.4.xsd
```

Therefore the AnalogRadioService V2.4 schema cannot be classified as official release-tag material from the currently observed upstream release state.

## 4. Exact candidate source

Upstream PR found:

```text
VDVde/VDV301 PR #27
Title: New AnalogRadioService and updated VideoRecordingService
State: open
Merged: no
Head commit: 0aa728aab47a7f13b6f36da415581d51592c4ca7
```

PR #27 adds:

```text
IBIS-IP_AnalogRadioService_V2.4.xsd
```

with blob SHA:

```text
48fb303b80936d2d762f0889ce0c359e04c16e5b
```

The file in `MarcLeinenDE/VDV301 dev/schema-integration` has the same blob SHA.

Branch integration history:

```text
c9c086ac07f7e9bdb271c54f7a274e3cf0d03749
Integrate public schema candidate files
```

Classification:

```text
source authority: public upstream PR candidate
branch status: candidate/integration material
historical official release status: no
```

This satisfies the candidate-lane traceability requirement but does not satisfy the official historical-release lane.

## 5. Exact candidate dependency chain

The candidate AnalogRadioService XSD explicitly includes:

```text
IBIS-IP_common_V2.3.xsd
```

The selected branch Common V2.3 explicitly includes:

```text
IBIS-IP_Enumerations_V2.2.xsd
```

Therefore the candidate/integration validation family is:

```text
AnalogRadioService V2.4 candidate
-> Common V2.3
-> Enumerations V2.2
```

This is intentionally **not** rewritten to Common/Enumerations V2.4.

The V2.4 service document also references General Conventions V2.3 in its references section, which is compatible with the fact that this service was developed against the V2.3-era base conventions. This is supporting context, not a rule to rewrite schema dependencies.

## 6. Initial service structure

Candidate XSD operation inventory:

```text
AnalogRadioService.SendTelegram
```

`AnalogRadioService.RadioTelegramStructure`:

```text
RawTelegram        1:1  IBIS-IP.string
AnalogChannel      1:1  IBIS-IP.unsignedInt
Bitrate            1:1  BitrateEnumeration
Repeats            0:1  IBIS-IP.unsignedInt
MaxRepeatInterval  0:1  IBIS-IP.unsignedInt
Transmitter        0:1  TransmitterStructure
```

`TransmitterStructure`:

```text
LeadTime 0:1 IBIS-IP.unsignedInt
HoldTime 0:1 IBIS-IP.unsignedInt
```

`BitrateEnumeration`:

```text
1200
2400
```

## 7. Candidate findings for detailed pass

### ARA-001 candidate - public document / schema release-provenance gap

The public V2.4 document references the AnalogRadioService V2.4 XSD, but the exact XSD is currently observed only in open PR #27 / integration material and not in an official VDV-301-2.4 GitHub release.

Initial classification:

```text
mismatch_kind: schema_family_or_provenance
likely_source_issue: schema_family_or_provenance_gap
classification_confidence: high for observed repository state
```

This is a routing/provenance finding, not an XSD content defect.

### ARA-002 candidate - TransmitterType table label vs Transmitter XSD element

The PDF table labels the final RadioTelegramStructure field:

```text
TransmitterType
```

The candidate XSD, the XSD screenshot embedded directly below the table, and the XML example use:

```text
Transmitter
```

Initial classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
```

### ARA-003 candidate - Transmitter cardinality PDF 1:1 vs XSD 0:1

The same PDF table says:

```text
TransmitterType 1:1
```

The candidate XSD defines:

```text
Transmitter minOccurs="0"
```

The PDF page itself embeds an XSD screenshot showing the optional element.

Initial classification:

```text
mismatch_kind: cardinality
likely_source_issue: cardinality_mismatch_candidate
subclassification: xsd_more_permissive_than_pdf
classification_confidence: high
```

### ARA-004 candidate - URI example uses SendFFSKTelegram

The operation overview, detailed section, XSD and XML example use:

```text
SendTelegram
```

The URI example instead shows:

```text
/AnalogRadioService/SendFFSKTelegram
```

Initial classification:

```text
mismatch_kind: operation_or_element_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
```

## 8. Next file

```text
docs/pdf_xsd_semantic_audit/12a_analog_radio_service_v2_4_pdf_xsd_first_pass.md
```
