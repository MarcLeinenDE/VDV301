# Source-locator review — CE-019 — 2026-09-28

Status: **terminally validated / complete**.

## Finding
CE-019 records a wrong PDF structure/type reference for `ServiceIdentificationWithStateList.ServiceIdentificationWithState`. The checked PDFs reference `ServiceSpecificationWithState`; every selected Common XSD from V1.0 through V2.4 types the list item as `ServiceIdentificationWithStateStructure`.

This is separate from CE-018, which concerns the same list item's cardinality.

## Version-specific source matrix
| Profile | Authority | PDF | Section / table | XSD member line |
|---|---|---:|---|---:|
| Common V1.0 | official release | p. 17 | 1.39 / Table 39 | 484 |
| Common V2.0 | official release | p. 24 | 2.39 / Table 39 | 490 |
| Common V2.1 | official release | p. 26 | 2.39 / Table 39 | 489 |
| Common V2.2 | official release | p. 27 | 2.40 / Table 40 | 498 |
| Common V2.3 | official release | p. 28 | 2.40 / Table 40 | 548 |
| Common V2.4 | candidate/integration XSD; official PDF separate | p. 30 | 2.39 / Table 39 | 563 |

## Conformance rule
The selected XSD remains executable authority. An implementation that substitutes the PDF-referenced `ServiceSpecificationWithState` model for the XSD-required `ServiceIdentificationWithStateStructure` is not XSD-conformant.

SDK behaviour: **error with advisory**. The FAIL remains; the advisory explains that the PDF contains a misleading/wrong structure reference and that the XSD model is semantically consistent with system-wide service identification including device context.

## State
Canonical source-locator manifest after validation: **15 complete / 0 partial / 177 remaining**.
