# Source-locator review — CE-018 — 2026-09-28

Status: **terminally validated / complete**.

## Finding
CE-018 records a cardinality conflict for `ServiceIdentificationWithStateList.ServiceIdentificationWithState`: the checked PDFs require `1:*`; every selected Common XSD from V1.0 through V2.4 permits `0:*`.

## Version-specific source matrix
| Profile | Authority | PDF | Section / table | XSD member line |
|---|---|---:|---|---:|
| Common V1.0 | official release | p. 17 | 1.39 / Table 39 | 484 |
| Common V2.0 | official release | p. 24 | 2.39 / Table 39 | 490 |
| Common V2.1 | official release | p. 26 | 2.39 / Table 39 | 489 |
| Common V2.2 | official release | p. 27 | 2.40 / Table 40 | 498 |
| Common V2.3 | official release | p. 28 | 2.40 / Table 40 | 548 |
| Common V2.4 | candidate/integration XSD; official PDF separate | p. 30 | 2.39 / Table 39 | 563 |

All selected XSDs define the member as `minOccurs="0" maxOccurs="unbounded"`.

## Conformance rule
The selected XSD remains executable authority. Therefore an empty `ServiceIdentificationWithStateList` is XSD-valid for these profiles and MUST NOT be rejected merely because the PDF states `1:*`.

SDK behaviour: **valid with advisory**, not FAIL. The advisory explains the confirmed PDF/XSD cardinality mismatch.

## Scope review
The older addendum text summarized visible PDF evidence mainly as V2.1-V2.4. Fresh cross-check confirms the same `1:*` PDF rule in V1.0 and V2.0 as well; the semantic registry's V1.0-V2.4 scope is therefore retained.

## State
Canonical source-locator manifest after validation: **14 complete / 0 partial / 178 remaining**.
