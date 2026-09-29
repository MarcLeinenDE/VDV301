# Source-locator review — ARA-003 — 2026-09-29

Status: **terminally validated / complete**.

## Finding
ARA-003 is the AnalogRadioService V2.4 `Transmitter` cardinality contradiction, kept separate from the ARA-002 identifier defect.

### Official PDF
Pinned PDF SHA-256: `d0c8d8a3b8719c13b09f43ec98349d2e9b22d07fec0c9267bceff0812cbbc34c`.

Printed page 11, `AnalogRadioService.RadioTelegramStructure`:
- table: transmitter row is `1:1`;
- embedded schema view on the same page: `Transmitter` has `minOccurs=0`.

The documentation defect is therefore established internally by the official PDF.

### Candidate/integration XSD
`IBIS-IP_AnalogRadioService_V2.4.xsd`
- blob: `48fb303b80936d2d762f0889ce0c359e04c16e5b`
- line 27
- `RadioTelegramStructure/Transmitter`
- `minOccurs="0"`, no explicit `maxOccurs` => 0:1.

This candidate/integration XSD is a valid selectable executable validation authority. When selected, PASS/FAIL follows this exact XSD and the result must identify its candidate provenance.

### Executable evidence
EV-105 was rechecked directly in Actions run `33228250613`, job `99036090357`.

The log records:
- candidate AnalogRadio V2.4 XSD compiled;
- declaration cardinality is 0:1;
- SendTelegram **without** Transmitter accepted;
- SendTelegram **with** Transmitter accepted;
- ARA-003 executable confirmation passed.

## SDK consequence
For the selected candidate/integration profile, both omission and one occurrence of `Transmitter` are XSD-valid. A diagnostic may explain that the official PDF table says 1:1, but must not turn a candidate-XSD-valid omission into FAIL.

No official AnalogRadioService V2.4 release-XSD authority is inferred.

## State
Canonical source-locator manifest after validation: **25 complete / 0 partial / 167 remaining**.
