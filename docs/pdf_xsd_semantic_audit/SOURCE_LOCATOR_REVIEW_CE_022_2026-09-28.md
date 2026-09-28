# Source-locator review — CE-022 — 2026-09-28

Status: **terminally validated / complete**.

## Finding
CE-022 records an outer-element naming/model conflict in `ServiceIdentification`.

The checked PDFs place `ServiceName` directly at the outer `ServiceIdentification` level and reference `ServiceSpecification`. Every selected Common XSD from V1.0 through V2.4 instead requires outer element `Service` of `ServiceSpecificationStructure`, followed by `Device`.

`ServiceName` does legitimately exist in the XSD, but one level deeper inside `ServiceSpecificationStructure`. This nested placement supports the classification as a likely PDF table-copy/naming defect rather than an alternative XML alias.

## Version-specific source matrix
| Profile | Authority | PDF | Section / table | outer XSD Service | inner XSD ServiceName |
|---|---|---:|---|---:|---:|
| Common V1.0 | official release | p. 17 | 1.37 / Table 37 | 472 | 455 |
| Common V2.0 | official release | p. 24 | 2.37 / Table 37 | 478 | 461 |
| Common V2.1 | official release | p. 26 | 2.37 / Table 37 | 477 | 460 |
| Common V2.2 | official release | p. 27 | 2.38 / Table 38 | 486 | 469 |
| Common V2.3 | official release | p. 28 | 2.38 / Table 38 | 536 | 519 |
| Common V2.4 | candidate/integration XSD; official PDF separate | p. 30 | 2.37 / Table 37 | 551 | 534 |

## Conformance rule
The selected XSD remains executable authority.

An outer `<ServiceName>` inside `ServiceIdentification` is rejected. The required outer element is `<Service>`; its nested `ServiceSpecificationStructure` then contains `<ServiceName>`.

SDK behaviour: **error with advisory**. The FAIL remains, while the advisory explains the likely PDF table-copy/naming defect and the correct nesting. No outer-level alias or silent repair is permitted.

## State
Canonical source-locator manifest after validation: **18 complete / 0 partial / 174 remaining**.
