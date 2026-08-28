# VDV301 audited superbranch – START HERE

This repository/branch is intended to be self-contained. A future maintainer, new ChatGPT conversation or another AI must be able to continue the VDV301 audit without access to previous chat history.

## Canonical branch

`dev/schema-integration`

Never treat `master` as the audit/integration work branch and never modify official-facing PR branches without explicit authorization.

## Project goal

Maintain one audited VDV301 superbranch that:

- contains the historically relevant XSD families from the first available versions through the newest auditable state;
- preserves exact official historical schema content where available;
- may also contain useful open-PR/candidate and integration material;
- makes authority/provenance explicit (`official`, `candidate`, `integration`, `unresolved`);
- never silently applies `latest XSD wins` or `latest dependency wins`;
- keeps version-exact and dependency-exact validation possible;
- audits each public VDV301 PDF/document version against the selected XSD/protocol/architecture profile;
- records findings before any decision is made about PRs, mails to VDV or local compatibility handling;
- feeds a later public VDV301 validation SDK/testkit without making the SDK a second, hand-maintained knowledge store.

## Read in this order

1. `00_START_HERE/CURRENT_STATE.json`
2. `00_START_HERE/MAINTENANCE_PLAYBOOK.md`
3. `docs/pdf_xsd_semantic_audit/DEEP_READ_METHOD.md`
4. `audit_registry/document_registry_v0.1.json`
5. `audit_registry/deep_read_registry_v0.1.json`
6. `docs/pdf_xsd_semantic_audit/findings.md`
7. `sdk_manifest/README.md` and `sdk_manifest/manifest_v0.1.json`

Detailed historical audit addenda remain evidence/background, but the files above define the continuation path.

## Authority rule

When an executable XSD profile exists, the selected XSD is the executable XML validation authority. A PDF/XSD discrepancy is a finding; it is not permission to silently rewrite or substitute the schema.

Candidate/integration schemas may be compiled and audited, but they must never be relabelled as official unless upstream provenance actually changes and the merged/released bytes are reverified.

## Change rule

Any new VDV PDF, release/tag, upstream merge or new/updated PR triggers an incremental change/impact audit before the superbranch and SDK manifest are considered current again. Follow `MAINTENANCE_PLAYBOOK.md`.
