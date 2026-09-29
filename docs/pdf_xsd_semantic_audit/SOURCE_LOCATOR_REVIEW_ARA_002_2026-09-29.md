# Source-locator review — ARA-002 — 2026-09-29

Status: **terminally validated / complete**.

## Finding
ARA-002 is a confirmed documentation identifier defect inside the official AnalogRadioService V2.4 PDF.

The `RadioTelegramStructure` table on printed page 11 names its final member `TransmitterType`. Three other representations in the same official PDF agree on `Transmitter`:
- printed page 11: embedded schema view,
- printed page 12: structure diagram,
- printed page 13: complete SendTelegram XML example using `<Transmitter>`.

The defect is therefore established from the official PDF alone.

## Candidate/integration corroboration
`IBIS-IP_AnalogRadioService_V2.4.xsd`, blob `48fb303b80936d2d762f0889ce0c359e04c16e5b`, line 27 declares:
`Transmitter` of type `TransmitterStructure`, `minOccurs="0"`.

That candidate/integration XSD is a valid selectable executable validation authority when that candidate profile is selected. For ARA-002 it is corroborating evidence; it is not required to establish the documentation-only defect and is not relabelled as an official release XSD.

## Separation
ARA-002 covers the **identifier** conflict only. The independent `1:1` table versus `0:1` schema-view/candidate-XSD cardinality conflict remains ARA-003.

## SDK consequence
ARA-002 is informational documentation context. It must not invent an official AnalogRadioService V2.4 release XSD. When the candidate/integration profile is selected, executable PASS/FAIL follows its exact selected XSD and the result identifies that candidate source/provenance.

## State
Canonical source-locator manifest after validation: **24 complete / 0 partial / 168 remaining**.
