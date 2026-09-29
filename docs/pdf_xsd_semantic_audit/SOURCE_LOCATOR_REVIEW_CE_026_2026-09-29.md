# Source-locator review — CE-026 — 2026-09-29

Status: **terminally validated / complete**.

## Finding
CE-026 records the historical `BeaconPoint.Description` (PDF) versus `BeaconPoint.Desciption` (selected XSD) spelling conflict.

Affected historical scope: Common V1.0 through V2.3.

## Historical source matrix
| Profile | PDF | XSD member |
|---|---|---:|
| V1.0 | p.9 §1.5 Table 5 | `Desciption`, line 104 |
| V2.0 | p.16 §2.5 Table 5 | `Desciption`, line 104 |
| V2.1 | p.16 §2.5 Table 5 | `Desciption`, line 105 |
| V2.2 | p.16 §2.5 Table 5 | `Desciption`, line 105 |
| V2.3 | p.17 §2.5 Table 5 | `Desciption`, line 105 |

All affected PDFs use `Description`. XML names are exact; the historical selected XSD spelling `Desciption` therefore controls validation.

## V2.4 correction boundary
Common V2.4 is explicitly **not affected**.

- PDF: p.17 §2.5 Table 5 uses `Description`.
- selected candidate/integration XSD: line 105 uses `Description`.

The later correction is evidence supporting the typo assessment but never changes historical V1.0-V2.3 validation.

## Separation from CE-017
CE-026 applies only to `BeaconPoint`.

`TSPPoint.Description` versus XSD `TSPPoint.Desciption` is tracked independently as CE-017. In the selected V2.4 XSD, TSPPoint still uses `Desciption`; the BeaconPoint correction must not leak into that finding.

## Conformance rule
For affected historical profiles, XML using `<Description>` at the BeaconPoint position is rejected because the selected XSD requires `<Desciption>`.

SDK behaviour: **error with advisory**. The advisory may classify the spelling as a likely XSD typo and mention the later V2.4 correction, but it never waives the historical XSD failure.

## State
Canonical source-locator manifest after validation: **22 complete / 0 partial / 170 remaining**.
