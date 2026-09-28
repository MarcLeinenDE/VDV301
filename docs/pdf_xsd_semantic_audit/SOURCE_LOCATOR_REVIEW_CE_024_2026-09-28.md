# Source-locator review — CE-024 — 2026-09-28

Status: **terminally validated / complete**.

## Finding
CE-024 records a cardinality conflict for `UnsubscribeResponse.Active` across Common V2.2, V2.3 and V2.4.

For each affected documentation version the PDF explicitly documents:

`Active 0:1`

The corresponding selected XSD declares `Active` without `minOccurs` or `maxOccurs`, therefore the effective XSD cardinality is:

`Active 1:1`

## Exact XSD matrix
| Profile | Authority | XSD member line | Effective cardinality |
|---|---|---:|---|
| Common V2.2 | official release | 909 | 1:1 |
| Common V2.3 | official release | 989 | 1:1 |
| Common V2.4 | candidate/integration XSD; official PDF separate | 1041 | 1:1 |

The PDF-side `0:1` evidence is explicitly frozen in the V2.2, fresh V2.3 and fresh V2.4 Deep Reads. The current canonical evidence does not freeze an exact printed page/table locator for this field, so no page number is invented here.

## Conformance rule
The selected XSD remains executable authority.

An `UnsubscribeResponse` without `Active` is invalid for the selected affected XSD even though the PDF table permits omission.

SDK behaviour: **error with advisory**. Missing `Active` remains an XSD FAIL; the advisory explains the PDF/XSD cardinality contradiction. The direction of any future source correction is not inferred by the SDK.

## State
Canonical source-locator manifest after validation: **20 complete / 0 partial / 172 remaining**.
