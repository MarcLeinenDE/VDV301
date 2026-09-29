# Source-locator review — ARA-004 — 2026-09-29

Status: **terminally validated / complete**.

## Finding
ARA-004 is a documentation-only operation-name contradiction in the official AnalogRadioService V2.4 PDF.

Pinned PDF SHA-256: `d0c8d8a3b8719c13b09f43ec98349d2e9b22d07fec0c9267bceff0812cbbc34c`.

Exact evidence:
- printed page 10, operation inventory: the service operation is `SendTelegram`; no `SendFFSKTelegram` operation is defined;
- printed page 13, §2.5.1 `URI for the Operation SendTelegram`: the concrete URI example ends in `/AnalogRadioService/SendFFSKTelegram`;
- printed page 13, XML example immediately below: root is `AnalogRadioService.SendTelegram`.

The isolated `SendFFSKTelegram` path segment is therefore a confirmed documentation error.

## SDK consequence
The SDK may warn when the exact `SendFFSKTelegram` operation segment is observed in AnalogRadioService V2.4 context and explain the documented `SendTelegram` name.

It must **not**:
- register `SendFFSKTelegram` as a valid alias merely because it appears in this example;
- silently rewrite the observed operation;
- turn this documentation-only finding into an XSD rule.

Candidate/integration XSD validation remains governed by the exact selected candidate XSD and its disclosed provenance.

## Separation
The missing `http://` scheme in the same concrete URI example is a separate finding (DRARA24-001) and is not folded into ARA-004.

## State
Canonical source-locator manifest after validation: **26 complete / 0 partial / 166 remaining**.
