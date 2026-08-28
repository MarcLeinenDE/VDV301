# Maintenance playbook – VDV301 audited superbranch

## Purpose

This playbook is the continuation procedure for a future maintainer, new chat or different AI. It applies when VDV publishes a new/changed PDF, creates/updates/merges a PR, publishes a release/tag, or when a new public candidate schema appears.

## A. Detect change

Check all of the following public upstream surfaces:

1. official VDV301 publication page;
2. official `VDVde/VDV301` default branch;
3. official GitHub tags/releases;
4. open PRs and changed PR heads;
5. previously tracked candidate/fork sources where they remain relevant.

Record source identity before interpretation:

- URL/repository;
- PDF title/version/date;
- commit/tag/PR number and head SHA;
- blob SHA for XSDs;
- PDF SHA-256 where bytes are available;
- first-seen and last-verified dates.

Never infer authority from a filename alone.

## B. Classify provenance

Use only:

- `official`: exact public VDV release/tag/default-branch material whose authority is verified;
- `candidate`: open PR or other public proposed schema material;
- `integration`: local superbranch material used for comparison/routing but not official release authority;
- `unresolved`: exact authority/provenance cannot yet be established.

A candidate becomes official only after checking the actual merged/released bytes. Do not change the label merely because a PR is closed or merged.

## C. Impact diff

For every changed PDF/XSD/PR:

1. diff against the last audited source;
2. enumerate added/removed/changed XSDs;
3. compare direct and transitive includes/imports;
4. identify affected service/version profiles;
5. identify shared Common/Enumerations consumers;
6. identify affected operation manifests and non-XSD protocol profiles;
7. identify existing findings that reference the changed material.

Do not use `latest wins`. An old service version remains routed to its old exact dependency pool unless the historical audit proves otherwise.

## D. Update superbranch

- Official historical backfill: only exact official release-tag bytes.
- Byte-identical historical schema: store once where the dedup policy permits.
- Same service/version but semantically different official schema: keep separately routable.
- Candidate/PR material: store only with explicit candidate provenance.
- Integration material: explicit integration label and reason.
- Never edit XSD content merely to make a PDF match.

After updates, regenerate/check the schema-profile inventory. The generator is fail-closed for unclassified root XSDs.

## E. Re-run audit

If an XSD changes:

- compile exact affected profile and dependency pool;
- rerun relevant EV regression samples;
- compare operation groups/global roots/types/cardinalities/enumerations;
- re-evaluate all findings that reference the changed file or a transitive dependency.

If a PDF changes:

- perform a fresh deep read of the changed document/version;
- compare visible original, embedded text extraction and available OCR;
- compare with previous deep-read record and findings;
- do not silently carry old findings forward.

If an external protocol reference changes in the VDV document:

- update the runtime authority matrix;
- do not substitute a newer RFC merely because it supersedes an older RFC unless the selected VDV document/profile supports that change.

## F. Finding lifecycle

Findings are audit knowledge, not automatic patch instructions.

Recommended states:

- `new`
- `confirmed`
- `confirmed_executable`
- `contextual_not_defect`
- `upstream_fixed`
- `fixed_in_later_version`
- `superseded`
- `rejected_after_deep_read`
- `needs_human_review`

Never delete a historical finding just because a later version fixes it. Old service versions must remain explainable by the SDK.

Each finding should retain:

- finding ID;
- affected document/XSD profile(s);
- first/last affected version where known;
- source references;
- static evidence;
- executable evidence when available;
- confidence;
- lifecycle state;
- later fix/PR/release linkage if applicable;
- no remediation decision unless separately approved.

## G. SDK impact

After audit changes are accepted into the canonical audit baseline:

1. regenerate/update schema profile inventory;
2. update routing overrides only for non-inferable facts;
3. update operation-context manifest where needed;
4. update audit-knowledge/finding explanations;
5. add synthetic regression tests;
6. keep normative result separate from explanatory finding knowledge.

Example principle:

A payload that follows a PDF but fails the exact official XSD must still be reported XSD-invalid. If a known audit finding explains why, the SDK may attach that finding as explanation; it must not silently validate against another enumeration/schema family.

## H. Handoff/baseline update

At a meaningful phase boundary:

- update `CURRENT_STATE.json`;
- update registries;
- consolidate stale central indexes;
- keep Git history as history rather than embedding superseded full snapshots;
- record exact baseline commit and evidence run IDs in the next handoff delta/current-state update.

A future maintainer should be able to continue using only this branch plus public upstream sources.
