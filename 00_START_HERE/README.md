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

1. `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md` — **canonical methodology; mandatory for every new chat/maintainer**
2. `00_START_HERE/CURRENT_STATE.json` — current phase, interruption state, counts, latest gates and next canonical work item
3. `00_START_HERE/HANDOFF_INTEGRITY_POLICY.md` — mandatory prompt-end / crash-recovery rules
4. `00_START_HERE/MAINTENANCE_PLAYBOOK.md`
5. `docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md`
6. `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_COMPLETENESS_POLICY.md`
7. `docs/pdf_xsd_semantic_audit/VERSION_SCOPE_BOUNDARY_POLICY.md`
8. current canonical registries/manifests named by `CURRENT_STATE.json`
9. only then relevant historical/deep-read/correction evidence

`AUDIT_WORKFLOW_CONTRACT.md` plus `CURRENT_STATE.json` are the restart contract. A future chat must be able to continue without a chat handoff and must not reconstruct methodology from conversational memory.

Detailed historical audit addenda remain evidence/background. If an older handoff, historical report or chat statement conflicts with the current canonical contract/state/registries, resolve the repository evidence before continuing.

## Authority rule

When an executable XSD profile exists, the selected XSD is the executable XML validation authority. A PDF/XSD discrepancy is a finding; it is not permission to silently rewrite or substitute the schema.

Candidate/integration schemas may be compiled and audited, but they must never be relabelled as official unless upstream provenance actually changes and the merged/released bytes are reverified.

## Change rule

Any new VDV PDF, release/tag, upstream merge or new/updated PR triggers an incremental change/impact audit before the superbranch and SDK manifest are considered current again. Follow `MAINTENANCE_PLAYBOOK.md`.


## PDF locator hard rule

Canonical PDF locators use the **actual visible body heading/table/figure on the byte-pinned page**. The table of contents, version-history cross-references and inferred sequential numbering are navigation/evidence aids only and must never be substituted for the visible target locator. See `AUDIT_WORKFLOW_CONTRACT.md`.

## Prompt-end handoff rule

Every project prompt/work cycle must finish with the repository handoff-integrity check defined in `HANDOFF_INTEGRITY_POLICY.md`. A substantive block is not complete merely because chat text says it is complete.

Old files such as `docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF.md`, `00_index.md`, `AUDIT_SCOPE_MATRIX.md`, `findings.md` and `validation_backlog.md` are historical evidence only and must never override the canonical restart set.
