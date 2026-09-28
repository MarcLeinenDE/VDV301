# Source-locator review — CE-016 — 2026-09-28

Status: **terminally validated / complete**.

## Finding

CE-016 records the spelling-sensitive XML identifier mismatch in `GlobalCardStatus`.

The official PDFs use `GlobalCardStatusID`. Every exact selected Common XSD from V1.0 through V2.3, and the explicitly selected V2.4 candidate/integration XSD, uses `GlobalCardStausID`.

The typo-like XSD spelling remains executable authority for the selected profile.

## Version-specific source matrix

| Profile | Authority | PDF | Section / table | XSD line |
|---|---|---:|---|---:|
| Common V1.0 | official release | p. 14 | 1.27 / Table 27 | 320 |
| Common V2.0 | official release | p. 21 | 2.27 / Table 27 | 326 |
| Common V2.1 | official release | p. 23 | 2.27 / Table 27 | 325 |
| Common V2.2 | official release | p. 24 | 2.27 / Table 27 | 329 |
| Common V2.3 | official release | p. 24 | 2.27 / Table 27 | 379 |
| Common V2.4 | candidate/integration XSD; official PDF separate | p. 26 | 2.27 / Table 27 | 379 |

## Conformance rule

XML using the PDF spelling `GlobalCardStatusID` fails against the affected selected XSD. The SDK must validate the historical profile exactly and explain that the required XSD name `GlobalCardStausID` is typo-like; the explanation does not waive the FAIL.

V2.4 remains explicitly candidate/integration and is not promoted to official-release authority.

## Historical rule

A later correction must not remove or reinterpret CE-016 for an older affected profile.

## Validation

The persisted entry was checked against the semantic-registry scope, pinned PDF identities, exact XSD blobs/components and canonical counters.

## State

Canonical source-locator manifest after validation: **12 complete / 0 partial / 180 remaining**.
