# VDV301 audit workflow contract

Status: **canonical continuation contract**  
Applies to: `dev/schema-integration`  
Purpose: make the audit reproducible across maintainers, AI sessions and new chats **without relying on chat history**.

This file defines **how the work must be done**. `CURRENT_STATE.json` defines **where the work currently stands**. If chat history, a historical report or an older handoff conflicts with this contract plus the current canonical registries, the contract/current canonical state wins unless a later explicit correction record says otherwise.

---

## 1. Non-negotiable authority rules

1. The exact selected XSD/dependency profile is the executable XML conformance authority.
2. If an instance violates that exact XSD, the result is **FAIL** even when the XSD appears typo-like or conflicts with the PDF.
3. A PDF/XSD conflict may explain the FAIL. It may never silently create an alias, normalization, repair or waiver.
4. `official_release`, `candidate_integration`, documentation-only and unresolved authority are distinct.
5. Never apply `latest wins`.
6. A candidate/open PR/integration XSD becomes official only after the exact released/merged authority and bytes are independently verified.
7. Historical profiles remain validated against their historical exact dependency route.
8. Audit/revalidation does not authorize XSD remediation. XSD changes require a separate explicit remediation decision.

---

## 2. Canonical per-finding workflow

Every finding — new, historical or revalidated — follows the same path.

### Step 1 — identify the existing finding identity

- Reuse the existing `finding_id`.
- Never create a second identity for the same issue.
- Check semantic registry, source-locator registry, runtime mapping, evidence and correction overlays before changing anything.
- A revalidation of an already complete finding does **not** create new progress credit.

### Step 2 — establish version scope independently

For every potentially affected version:

- inspect the exact publication/version;
- inspect the exact XSD/dependency profile;
- classify authority independently;
- verify first/last affected version;
- identify explicit later correction boundaries.

Never extrapolate one version to another merely because filenames or structures look similar.

### Step 3 — inspect the original PDF source

Use the exact byte-pinned official source whenever available.

For any PDF-backed claim where layout or location matters, inspect the **visible document body**, including:

- printed page;
- actual visible section heading;
- actual visible table/figure caption or number;
- relevant row/member/value/cardinality;
- nearby rows, grouping, footnotes and explanatory prose.

Text extraction/OCR/search may locate a page, but they are not the locator authority when visible layout is material.

### Step 4 — hard PDF locator rule: body beats TOC/history/sequence inference

For a canonical PDF locator:

- use the **actual visible body heading/table/figure on the cited page**;
- never derive a section/table number from numerical sequence;
- never use the table of contents as the final locator authority;
- never copy a cross-reference from version history as though it were the actual target location;
- if TOC, history and visible body disagree, preserve the inconsistency as evidence, but the canonical target locator follows the **visible body**;
- if the claim itself is about a bad TOC/history cross-reference, pin both the visible source of the bad reference and the actual target;
- a locator may be marked complete only when the target is independently reconstructable from the byte-pinned source.

**A green JSON/schema gate alone does not prove a PDF locator is visually correct.**

### Step 5 — inspect the exact XSD authority

Record:

- exact XSD file;
- exact Git blob;
- release tag/ref/variant where authority is material;
- component/type/element/enum;
- XPath/component locator;
- compact line hint when practical;
- exact rule/value/cardinality/compositor.

For `official_release` lanes, verify the exact upstream release-tag/file/blob whenever deterministically possible.

### Step 6 — compare PDF and XSD in full context

Check, as applicable:

- identifier spelling/case;
- type;
- cardinality;
- required/optional;
- enum values;
- sequence/choice/group;
- nesting;
- root vs local operation context;
- request/response/data-event role;
- version history;
- later correction.

Do not judge isolated tokens without context.

### Step 7 — active disproof attempt

Before confirming the finding, try to make it disappear:

- notation/legend explanation?
- intentional compositor/group?
- wrong schema/dependency version?
- PDF label vs actual XML element distinction?
- later/earlier history explaining it?
- candidate vs official authority confusion?
- body-vs-TOC numbering contradiction?

Record the strongest counter-explanation when material.

### Step 8 — executable evidence where validation behavior is affected

When technically practical, add or verify:

- valid positive case;
- targeted invalid negative case;
- exact selected XSD profile;
- exact expected result.

Static inspection alone must not be overstated as executable behavior.

### Step 9 — classify the finding

Use evidence-backed classifications such as:

- documentation/PDF defect;
- XSD typo/defect;
- cross-artifact mismatch;
- authority gap;
- historical/superseded observation;
- non-defect;
- provider/implementation error;
- candidate-specific difference.

When source attribution is uncertain, preserve the mismatch instead of forcing a blame direction.

### Step 10 — decide SDK behavior

Determine explicitly:

- XSD validation alone sufficient?
- advisory on an existing XSD FAIL?
- advisory on an XSD-valid result?
- informational only?
- resolver/profile warning?
- unsupported profile?
- no runtime diagnostic?

The selected-XSD result remains normative.

For a runtime-mapped finding:

- runtime `profile_scope` must equal the semantic **affected** scope;
- `correction_boundary_not_affected` lanes are evidence only and must never be runtime trigger lanes.

### Step 11 — provider-facing diagnostics

Every terminal SDK-relevant finding must have complete German and English diagnostics:

- title;
- short;
- long;
- recommendation.

Diagnostics explain the standard/source issue without exposing unnecessary internal validator architecture.

### Step 12 — update all canonical stores, validate, then close

Keep synchronized as applicable:

- `audit_registry/finding_semantic_classification_v0.1.json`
- `audit_registry/finding_source_locators_v0.1.json`
- `sdk_manifest/known_issues_runtime_mapping_v0.1.json`
- evidence/review/correction reports
- `00_START_HERE/CURRENT_STATE.json`

Then run the complete gate.

A finding is terminally complete only after:

- scope resolved;
- authority resolved;
- classification resolved;
- source locator complete;
- PDF locator visually/body verified where applicable;
- XSD authority pinned;
- SDK implication resolved;
- required evidence present;
- DE/EN diagnostics complete;
- gate SUCCESS.

---

## 3. Source-locator quality rule

A source locator has two distinct qualities:

1. **structural completeness** — fields, pins, blobs, pages, sections etc. exist and are internally consistent;
2. **body verification** — page/section/table was actually checked against the visible byte-pinned document body.

Do not equate the first with the second.

For existing historical locators created before this rule was made explicit, body verification must be independently rechecked before the locator set is called fully revalidated.

---

## 4. Correction rule

If a wrong finding, wrong scope or wrong locator is discovered:

1. correct the current canonical registry;
2. preserve historical evidence rather than silently rewriting old reports;
3. search all existing findings for the same failure pattern;
4. add a reusable gate/policy guard where possible;
5. rerun affected evidence/gates;
6. update `CURRENT_STATE.json`.

Examples of reusable failure patterns:

- TOC/body numbering drift;
- version-history cross-reference mistaken for actual section;
- candidate XSD relabelled official;
- later corrected version accidentally left in affected runtime scope;
- finding identity swap;
- inferred sequential table number rather than visible table number.

---

## 5. Progress accounting

The canonical semantic inventory contains 192 findings.

Progress is credited by unique finding identity only.

- revalidation of an existing complete finding: no new point;
- correction of an existing finding: no new point;
- duplicate identity: forbidden;
- partial coverage: not complete;
- body-locator quality review alone: no new finding point.

Always distinguish:

- semantic-classification completion;
- source-locator structural completion;
- source-locator visible-body verification;
- runtime-mapping review/implementation.

They are different milestones.

---

## 6. New-chat / no-handoff restart procedure

A new chat or maintainer must **not** ask the user to reconstruct prior chat history.

Read in this order:

1. `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md` — methodology and non-negotiable rules.
2. `00_START_HERE/CURRENT_STATE.json` — current phase, counts, latest gate, next work.
3. `00_START_HERE/MAINTENANCE_PLAYBOOK.md` — upstream-change handling.
4. `docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md`.
5. `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_COMPLETENESS_POLICY.md`.
6. current canonical registries/manifests named by `CURRENT_STATE.json`.
7. only then the relevant historical/deep-read/correction evidence for the next finding.

Before writing:

- determine actual branch HEAD;
- fetch current canonical files again;
- inspect the latest successful/failed gate;
- compute the next unresolved work item from the canonical registry rather than from remembered chat order;
- never rewind newer canonical work because an old handoff says otherwise.

If chat history conflicts with the repository, stop and resolve the repository evidence first.

---

## 7. Small-block execution rule

Work in small terminal blocks.

For each completed finding/block, report:

- what was found;
- classification;
- affected versions and authority;
- provider/SDK consequence;
- evidence;
- gate run/result;
- new HEAD;
- next canonical work item.

Do not batch so much work that a timeout can leave several findings half-written and ambiguous.

---

## 8. Current audit/remediation separation

Current audit work establishes facts and SDK knowledge.

It does **not** itself authorize:

- changing historical XSD bytes;
- merging correction changes;
- opening/altering upstream PRs;
- deciding final VDV remediation wording.

For not-yet-merged PRs, direct correction may later be appropriate when explicitly authorized.
For old released versions, correction branches may later be requested from VDV.
Those are separate remediation steps based on the revalidated audit baseline.

---

## 9. Definition of consistency

The project is consistent only when all of the following agree:

- semantic finding identity and affected scope;
- source-locator affected scope;
- runtime affected scope;
- exact authority class;
- XSD blob/profile;
- PDF body locator;
- DE/EN diagnostic;
- evidence;
- current-state counts;
- latest successful gate.

A green gate is necessary but not sufficient if the gate does not cover the relevant failure mode. When a new failure mode is discovered, extend the methodology/gate before continuing.
