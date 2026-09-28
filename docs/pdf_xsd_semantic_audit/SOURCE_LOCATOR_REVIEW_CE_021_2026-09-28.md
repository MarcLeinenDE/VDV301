# Source-locator review — CE-021 — 2026-09-28

Status: **terminally validated / complete**.

## Finding
CE-021 records a persistent element-name conflict in `LogMessageStructure`: the checked PDFs use required child `MessageBody` (type `Message`), while every selected Common XSD from V1.0 through V2.4 requires child `Message` of `MessageStructure`.

The type concept aligns; the XML child element name does not.

## Version-specific source matrix
| Profile | Authority | PDF | Section / table | XSD member line |
|---|---|---:|---|---:|
| Common V1.0 | official release | p. 15 | 1.32 / Table 32 | 395 |
| Common V2.0 | official release | p. 22 | 2.32 / Table 32 | 401 |
| Common V2.1 | official release | p. 24 | 2.32 / Table 32 | 400 |
| Common V2.2 | official release | p. 25 | 2.32 / Table 32 | 409 |
| Common V2.3 | official release | p. 26 | 2.32 / Table 32 | 459 |
| Common V2.4 | candidate/integration XSD; official PDF separate | p. 29 | 2.32 / Table 32 | 474 |

## Conformance rule
The selected XSD remains executable authority. `MessageBody` is not an alias for `Message`.

An implementation that emits `LogMessage.MessageBody` therefore fails XSD validation even though it follows the PDF wording.

SDK behaviour: **error with advisory**. The advisory classifies the mismatch as a likely PDF defect / stale identifier and explains that the implementation is PDF-oriented but not XSD-conformant. No automatic alias or silent repair is permitted.

## State
Canonical source-locator manifest after validation: **17 complete / 0 partial / 175 remaining**.
