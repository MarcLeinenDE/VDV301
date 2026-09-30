# Source-locator completeness policy

A finding or per-version coverage may be marked `complete` only when every source surface used to support the finding is pinned precisely enough for independent re-checking.

## PDF-backed claims

For a PDF-backed claim this requires, where the source actually exposes them:

- pinned source identity and SHA-256;
- printed page number;
- **actual visible body section heading**;
- **actual visible body table/figure identifier** when the claim is located in a table/figure;
- a point summary identifying the exact conflicting field/value/cardinality.

### Hard body-locator rule

The canonical locator is taken from the **visible document body on the cited byte-pinned page**.

The following are **not** final locator authority:

- table-of-contents numbering;
- a version-history cross-reference;
- an extracted-text heading without visible-layout confirmation when layout can matter;
- a section/table number inferred from the surrounding numeric sequence;
- a neighbouring version's numbering.

Those surfaces may be used to find or explain the target, but they must not be copied into the canonical locator unless the visible target page itself confirms them.

If TOC, version history and visible body disagree:

1. preserve the contradiction as evidence when relevant;
2. pin the bad TOC/history reference if it is part of the finding;
3. pin the real target separately;
4. use the **visible body heading/table** as the canonical target locator.

A structurally valid JSON locator or green schema gate does not by itself prove that the page/section/table reference is visually correct.

Text extraction/OCR/search is a navigation aid. Where layout/location is material, visible byte-pinned rendering is required before the locator is considered body-verified.

## XSD-backed claims

For an XSD-backed claim this requires:

- exact selected XSD file and Git blob;
- component/member;
- exact line or compact line range where practical;
- the relevant schema rule/value;
- exact release/ref/variant provenance where authority matters.

For `official_release` lanes, exact upstream tag/file/blob identity must be checked whenever the release context can be deterministically resolved.

## Completeness and quality states

Source-locator work distinguishes:

1. **structural completeness** — locator fields/pins/blob identities exist and are internally consistent;
2. **visible-body verification** — the stored PDF page/section/table was checked against the actual visible byte-pinned document body.

Do not equate the two.

Existing locators that predate the explicit body-locator rule may retain their historical structural record, but they require a standardized body-locator revalidation before the set is described as fully body-verified.

A known source must not be left deliberately vague while coverage is labelled complete. If an exact locator cannot yet be established, the coverage remains partial until resolved.

Historical and candidate authorities remain separate. Locator completion never promotes a candidate source over official historical authority and never changes historical PASS/FAIL by latest-wins.

The canonical workflow is defined in:

`00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`
