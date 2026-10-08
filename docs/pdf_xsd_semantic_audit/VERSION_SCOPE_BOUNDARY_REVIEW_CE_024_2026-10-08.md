# Version-scope boundary review — CE-024 — 2026-10-08

Status: **verified / scope unchanged**.

## Finding
CE-024 is the `UnsubscribeResponse.Active` cardinality mismatch:
- affected PDFs document `Active 0:1`;
- affected selected XSDs require `Active` exactly once.

## Lower boundary
Common V2.1 is an aligned negative control. Its exact XSD models `UnsubscribeResponse` as an `xs:choice` between `Active` and `OperationErrorMessage`, and the V2.1 PDF documents the same alternative structure. `Active` is therefore not independently mandatory in V2.1.

## First affected version
In Common V2.2 the XSD changes to a sequence:
- required `Active`;
- optional `OperationErrorMessage`.

The V2.2 PDF nevertheless documents `Active 0:1`. This is the first affected boundary.

## Continuity
The same PDF `0:1` versus XSD `1:1` mismatch persists in official Common V2.3 and in the selected Common V2.4 candidate/integration XSD lane.

## Boundary conclusion
Existing scope is confirmed unchanged:
1. Common V2.2-V2.3 — official release authority;
2. Common V2.4 — candidate/integration authority.

Common V2.1 is explicitly outside CE-024.

## SDK consequence
An `UnsubscribeResponse` without `Active` must **FAIL** whenever the exact selected affected XSD requires it. The PDF's optionality is explanatory Known-Issue context only and must never relax the selected-XSD result.
