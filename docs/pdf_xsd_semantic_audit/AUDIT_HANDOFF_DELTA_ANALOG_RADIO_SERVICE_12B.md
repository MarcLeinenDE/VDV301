# AUDIT HANDOFF DELTA - AnalogRadioService 12B

Status: supplemental delta after AnalogRadioService V2.4 semantic/provenance first-pass closure.

Branch:

```text
dev/schema-integration
```

Starting head:

```text
32bf406448f39218cdd6d0cb0543b465e75c497d
```

New files:

```text
docs/pdf_xsd_semantic_audit/12_analog_radio_service_historical_start.md
docs/pdf_xsd_semantic_audit/12a_analog_radio_service_v2_4_pdf_xsd_first_pass.md
docs/pdf_xsd_semantic_audit/12b_analog_radio_service_findings_and_closure.md
docs/pdf_xsd_semantic_audit/ANALOG_RADIO_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/generated/analog_radio_service_v2_4_scope_and_findings.csv
```

Routing result:

```text
Public writing: AnalogRadioService V2.4
Candidate XSD: exact file from open upstream PR #27
blob: 48fb303b80936d2d762f0889ce0c359e04c16e5b
candidate dependency pool:
  AnalogRadioService V2.4
  -> Common V2.3
  -> Enumerations V2.2
```

Provenance result:

```text
No VDV-301-2.4 GitHub release observed.
Official releases currently stop at VDV-301-2.3.
Upstream master lacks AnalogRadioService V2.4 XSD.
PR #27 remains open/unmerged.
Branch file entered through candidate integration commit c9c086ac07f7e9bdb271c54f7a274e3cf0d03749.
```

Findings:

```text
ARA-001: public document vs candidate-only schema release provenance gap.
ARA-002: PDF table TransmitterType vs XSD/embedded-XSD/XML-example Transmitter.
ARA-003: PDF Transmitter 1:1 vs XSD 0:1.
ARA-004: URI example SendFFSKTelegram vs actual operation SendTelegram.
```

Validation status:

```text
No XSD compilation performed.
No sample XML validation performed.
No XSD changed.
No PR/comment/merge action performed.
```

Next planned block:

```text
docs/pdf_xsd_semantic_audit/13_passenger_counting_service_historical_start.md
```
