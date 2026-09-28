# Source-locator completeness policy

A finding or per-version coverage may be marked `complete` only when every source surface used to support the finding is pinned precisely enough for independent re-checking.

For a PDF-backed claim this requires, where the source actually exposes them:
- pinned source identity and SHA-256,
- printed page number,
- section,
- table/figure identifier when the claim is located in a table/figure,
- a point summary identifying the exact conflicting field/value/cardinality.

For an XSD-backed claim this requires:
- exact selected XSD file and Git blob,
- component/member,
- exact line or compact line range,
- the relevant schema rule/value.

A known source must not be left at a deliberately vague locator while the coverage is labelled `complete`. If an exact locator cannot yet be established, the coverage remains partial until it is resolved.

Historical and candidate authorities remain separate. Locator completion never promotes a candidate source over an official historical authority and never changes historical PASS/FAIL by latest-wins.
