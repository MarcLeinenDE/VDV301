# Source-locator revalidation correction — visible-body scope

Date: 2026-09-30  
Status: **canonical correction to the wording of the complete-40 revalidation**

## Why this correction exists

The report `SOURCE_LOCATOR_REVALIDATION_COMPLETE_40_2026-09-30.md` correctly records the semantic/authority/runtime revalidation and the locator corrections found during that work, but its wording can be read too broadly as if **every PDF locator of all 40 findings had been newly rechecked against the visible body of the byte-pinned PDF under one uniform standard**.

That is not established.

## What was actually revalidated for all 40

All 40 current source-locator entries were checked for:

- finding identity;
- semantic version scope;
- runtime-scope synchronization where applicable;
- authority classification;
- DE/EN diagnostics;
- XSD locator/blob consistency;
- upstream release-tag/file/blob identity where deterministic;
- structural source-locator consistency.

The strengthened gate performs 19 upstream release-tag XSD blob checks.

## What was body-locator verified in the 2026-09-30 correction pass

The following findings received explicit current-standard PDF body-locator verification/correction during this pass:

- `CE-002`
- `CE-004`
- `CE-020`
- `CE-025`
- `CE-026`

These are tracked as `verified_current_standard` in:

`audit_registry/pdf_locator_body_verification_v0.1.json`

## What remains

The other **35** structurally complete locator findings retain their existing historical evidence and locators, but they have **not yet all been re-run end-to-end under the explicit 2026-09-30 rule**:

> canonical target locator = actual visible body heading/table/figure on the byte-pinned page; never TOC, version-history cross-reference or inferred sequence unless the visible target itself confirms it.

They are therefore tracked as `pending_current_standard`.

This does not withdraw their findings or imply their current locators are wrong. It means the project does not claim the stronger property until it is independently rechecked.

## Progress freeze

Until the 35-entry visible-body backlog is complete:

- the structural source-locator count remains frozen at **40**;
- no new finding may receive structural source-locator progress credit;
- the next canonical work is the visible-body revalidation backlog, in semantic finding order;
- after the backlog reaches zero and the gate is green, ordinary source-locator expansion resumes at the first structurally missing finding (`CIS-001` at the time of this correction).

The validator enforces this freeze through:

`tools/validate_finding_source_locators_v0_1.py`

## Canonical methodology

The restart and per-finding workflow is now defined by:

`00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`

The PDF locator hard rule is also explicit in:

`docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_COMPLETENESS_POLICY.md`

## No normative conformance change

This correction changes the claim about **locator-quality verification coverage**, not XSD conformance behavior.

The selected XSD remains normative for PASS/FAIL.


## Gate proof

The strengthened visible-body backlog gate passed:

- GitHub Actions run: **36718104921**
- result: **SUCCESS**
- validated commit: `7d4a84dd0c699b3d0260c6a46c7a329dfdc72a1c`
- structural locators: **40**
- current-standard visible-body verified: **5**
- pending current-standard body revalidation: **35**
- upstream exact release-tag XSD checks: **19**
- structural locator progress freeze: **active and validated**
