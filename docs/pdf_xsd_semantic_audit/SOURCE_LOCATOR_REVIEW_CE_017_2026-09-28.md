# Source-locator review — CE-017 — 2026-09-28

Status: **terminally validated / complete**.

## Finding

CE-017 records the XML identifier mismatch in `TSPPoint`: the PDFs use `Description`; the exact selected XSDs require the typo-like element `Desciption`.

## Version-specific source matrix

| Profile | Authority | PDF | Section / table | XSD line |
|---|---|---:|---|---:|
| Common V1.0 | official release | p. 21 | 1.56 / Table 56 | 662 |
| Common V2.0 | official release | p. 29 | 2.59 / Table 59 | 673 |
| Common V2.1 | official release | p. 31 | 2.59 / Table 59 | 672 |
| Common V2.2 | official release | p. 33 | 2.60 / Table 60 | 681 |
| Common V2.3 | official release | p. 35 | 2.60 / Table 60 | 761 |
| Common V2.4 | candidate/integration XSD; official PDF separate | p. 37 | 2.59 / Table 59 | 813 |

The PDF pages were re-verified against the official pinned VDV sources. Each table names the member `Description`.

## Conformance rule

The selected XSD remains executable authority. A provider sending `TSPPoint.Description` fails against affected selected schemas; the exact schema member is `Desciption`. The diagnostic explains the likely typo but does not waive the FAIL.

## Hygiene

The earlier V2.4 working note that still said visual PDF confirmation was required has been retained as historical evidence and explicitly marked superseded by the later rendered-table review. It is no longer an open task.

## State

Canonical source-locator manifest after validation: **13 complete / 0 partial / 179 remaining**.
