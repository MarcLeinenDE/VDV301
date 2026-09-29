# Source-locator review — CE-025 — 2026-09-29

Status: **terminally validated / complete**.

## Finding
CE-025 records the historical request-element spelling conflict `Reply-Path` (PDF) versus `ReplyPath` (selected XSD).

The affected historical scope is Common V1.0 through V2.3. Both `SubscribeRequest` and `UnsubscribeRequest` are covered separately. XML names are exact, so the PDF hyphenated spelling is not an alias.

## Historical source matrix
| Profile | SubscribeRequest PDF | XSD ReplyPath | UnsubscribeRequest PDF | XSD ReplyPath |
|---|---|---:|---|---:|
| V1.0 | p.24 §1.63 Table 63 | 860 | p.25 §1.65 Table 65 | 873 |
| V2.0 | p.32 §2.66 Table 66 | 871 | p.33 §2.68 Table 68 | 884 |
| V2.1 | p.30 §2.55 Table 55 | 871 | p.32 §2.58 Table 58 | 886 |
| V2.2 | p.32 §2.56 Table 56 | 880 | p.34 §2.61 Table 61 | 903 |
| V2.3 | p.33 §2.56 Table 56 | 960 | p.35 §2.61 Table 61 | 983 |

## V2.4 correction boundary
V2.4 is explicitly **not affected**.

- SubscribeRequest: p.36 §2.55 Table 55 uses `ReplyPath`; selected candidate XSD line 1012 also uses `ReplyPath`.
- UnsubscribeRequest: p.38 §2.60 Table 60 uses `ReplyPath`; selected candidate XSD line 1035 also uses `ReplyPath`.

This later documentation correction does not alter historical validation behaviour.

## Conformance rule
For V1.0–V2.3, `<Reply-Path>` is rejected where the selected XSD expects `<ReplyPath>`.

SDK behaviour: **error with advisory**. The advisory explains the confirmed historical PDF defect. No alias or silent normalization is permitted.

## State
Canonical source-locator manifest after validation: **21 complete / 0 partial / 171 remaining**.
