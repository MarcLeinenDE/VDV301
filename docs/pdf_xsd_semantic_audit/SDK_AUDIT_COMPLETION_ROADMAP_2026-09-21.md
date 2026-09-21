# SDK audit completion roadmap — 2026-09-21

Status: **canonical post-classification work plan**.

Purpose: preserve the remaining work after the completed 192/192 semantic finding classification and prevent the runtime-mapping, source-location, capability-conformance and later remediation tracks from being conflated or forgotten.

## Non-negotiable boundaries

1. The existing 192-finding semantic audit remains the canonical finding baseline.
2. The current Known-Issues runtime-mapping review is **not replaced** by the new field-test requirement.
3. Selected XSD authority remains normative for payload validation. Known-Issues knowledge may explain a result but must not silently change VALID/INVALID.
4. Historical service/version semantics must never be back-applied from later versions.
5. Candidate/integration material must never be presented as official release authority.
6. No upstream VDV issue/PR or documentation-error report is authorized merely because an internal finding exists.
7. Every external-facing correction must pass the stricter External-reporting gate in `FINDING_EVIDENCE_GATE.md`.
8. The additional service-operation obligation requirement originates from a field test of the frozen legacy VDV301 ServiceTool. It is a **new audit/SDK requirement**, not part of the original 192-finding classification, and must not rewrite existing findings without independent revalidation.

## Phase A — complete the current Known-Issues runtime-mapping review

Current frozen state at roadmap creation:

- branch: `dev/schema-integration`
- HEAD before roadmap persistence: `e3b5db47c6ea57f7ca2ba131c4c65d7b2ecf5998`
- reviewed: 61
- candidate: 17
- not_designed: 1
- not_applicable: 113
- implemented: 0

Required work:

- review all 17 remaining `candidate` findings in small service/version blocks;
- resolve `DRTIME10-002`, the sole `not_designed` finding;
- preserve the existing review pattern: exact authority -> evidence/disproof -> read-only gate -> persist -> closure/consistency gate -> cleanup;
- do not implement executable runtime matchers during this phase;
- do not mutate XSDs.

Completion gate:

- `candidate = 0`;
- `not_designed = 0`;
- every one of the 192 findings has a terminal runtime-mapping disposition (`reviewed` or `not_applicable`, unless later explicitly implemented);
- deterministic runtime-mapping generation and all root-XSD checks remain green.

## Phase B — source-locator completeness hardening

Reason: many findings already contain exact PDF pages and XSD identities, but locator precision is not yet uniform enough for final SDK diagnostics or external VDV reporting.

Create a machine-readable source-locator layer or schema extension. For every SDK- or reporting-relevant finding, record the exact applicable locator or an explicit reason why that source class is not applicable.

PDF/document locator minimum:

- document/source ID;
- service/document version;
- byte-pinned SHA-256 where available;
- physical PDF page;
- printed page if materially different;
- section/subsection;
- table/figure/footnote where applicable;
- literal identifier or semantic subject being cited;
- authority class.

XSD locator minimum:

- XSD filename;
- exact Git blob/immutable identity;
- schema/service version;
- authority class;
- component kind (global element, local element, type, group, enumeration, annotation, compositor, etc.);
- exact component name;
- stable component path / XPath-like semantic locator;
- line number only as optional convenience, never as the sole locator.

External-standard locator minimum when applicable:

- standard/RFC identity and edition;
- section/clause;
- role in the finding (normative dependency, terminology, protocol context, etc.).

Rules:

- do not require both PDF and XSD for findings where one source class is genuinely not applicable;
- do require an explicit `not_applicable_reason` rather than silent absence;
- a source-locator audit may expose an old finding problem; any correction must follow the existing regression/correction trail rather than silently rewriting history.

Completion gate:

- every finding eligible for SDK explanation has enough direct locator data to generate a human-readable citation without reverse-searching old evidence files;
- every remediation candidate has exact direct locators for all decisive competing sources;
- no `sdk_ready` / later `remediation_ready` state without locator completeness.

## Phase C — service/version/operation obligation matrix

This is the additional field-test requirement discovered from the frozen legacy VDV301 ServiceTool.

Purpose: distinguish **whether an operation must exist** from **whether an applicable operation's payload is structurally/semantically correct**.

Create a separate canonical manifest and schema, conceptually:

- service;
- exact service version/profile;
- operation;
- interaction direction / role;
- obligation state;
- condition, if conditional;
- exact normative authority and source locator;
- XSD operation-inventory linkage as structural corroboration only;
- expected unsupported response semantics where specified;
- probe safety / side-effect policy;
- review/evidence state.

Obligation states:

- `MANDATORY`
- `OPTIONAL`
- `CONDITIONAL`
- `NOT_APPLICABLE`
- `UNRESOLVED` only during audit; forbidden at the manufacturer-conformance release gate.

Normative rule:

The XSD may establish operation names, request/response structures and executable inventory, but **must not by itself be treated as sufficient authority for MANDATORY/OPTIONAL/CONDITIONAL support obligations**. The exact service-version documentation is the primary authority for those obligations unless the specification explicitly delegates otherwise.

Runtime consequences:

- `NOT_APPLICABLE`: do not issue the normal audit request; no manufacturer finding.
- `OPTIONAL`: absence / specified OperationNotSupported equivalent -> `OPTIONAL_NOT_SUPPORTED`; no manufacturer finding.
- `CONDITIONAL`: evaluate the documented condition first; only when satisfied may absence become a conformance issue.
- `MANDATORY`: absence may become a manufacturer/conformance finding only after transport, discovery and test-harness causes have been excluded.
- `UNRESOLVED`: fail closed; no automated manufacturer verdict.

Probe-safety requirement:

Obligation and safe testability are separate axes. Operations with side effects (for example restart/update/control operations) must carry a probe policy such as passive/read-only, safe query, explicit opt-in, or prohibited automatic invocation.

Pilot:

Start with DeviceManagementService because it contains useful historical/version and optional-operation differences and directly covers the field-test failure mode. Only after the DMS pilot schema/gate is stable, sweep all supported service versions.

Completion gate before manufacturer-conformance automation:

- every operation in every supported service/version profile has a terminal obligation state;
- every `CONDITIONAL` entry has a machine-readable, source-backed condition;
- no unresolved obligation may generate a manufacturer fault;
- matrix and source locators regenerate deterministically.

## Phase D — implement structured Known-Issues runtime matchers

Only after Phase A and the locator hardening needed by diagnostics.

For each `reviewed` runtime mapping:

- replace free-text trigger descriptions with structured profile-specific match conditions;
- require exact service/version/authority context;
- add positive and negative executable evidence;
- preserve selected-XSD VALID/INVALID;
- never create undocumented aliases or automatic rewrites;
- link every runtime diagnostic back to its canonical finding and source locators.

Completion gate:

- no matcher is implemented from free-text matching;
- every matcher has dedicated positive/negative tests;
- deterministic manifest/generator validation remains green.

## Phase E — compose manufacturer-audit execution model

The eventual Prüf-SDK execution order must explicitly separate:

1. service/profile discovery and declared version resolution;
2. capability/operation-obligation resolution;
3. safe request planning;
4. transport/protocol result classification;
5. payload/XSD validation for applicable/supported operations;
6. semantic Known-Issues advisory matching;
7. final provider-facing explanation with exact source locators.

Hard rule:

A response such as 404 / OperationNotSupported must never become a manufacturer finding solely from the response itself. The exact service/version operation obligation must be resolved first.

## Phase F — external remediation / VDV reporting / upstream PR triage

This is a separate later phase.

For every candidate:

- re-fetch the then-current official upstream state;
- search current open/closed PRs/issues for an existing fix;
- verify exact PDF/document source and visible locator;
- verify exact XSD blob/profile and component locator;
- review predecessor/successor history;
- record the strongest plausible disproof hypothesis and why it fails;
- run executable evidence when validation behaviour is affected;
- assess compatibility/code-generation/consumer impact;
- classify the proposed action: no action, SDK-only explanation, documentation report, GitHub issue, schema PR, authority clarification;
- prepare only the narrowest defensible correction;
- obtain explicit user approval before any external issue/PR is opened.

A finding is never automatically a remediation instruction.

## Phase G — release/freeze gate

Before calling the audit/SDK knowledge base complete:

- runtime mapping terminal;
- source locators complete;
- operation-capability matrix terminal for supported profiles;
- implemented matchers fully tested;
- diagnostics link back to canonical findings and immutable sources;
- manufacturer-report semantics distinguish capability, transport and payload failures;
- remediation candidates remain provenance-separated from runtime validation;
- CURRENT_STATE and handoff documentation contain exact counts, manifests and gate IDs.

## Immediate continuation order

1. Finish Phase A.
2. First micro-block: resolve `DRTIME10-002` from `not_designed` to a justified terminal runtime-mapping disposition.
3. Continue the 17 remaining candidates in small related service/version blocks, starting with the TicketingService candidates unless evidence indicates a safer grouping.
4. Run the Phase-A terminal consistency gate.
5. Begin Phase B source-locator completeness.
6. Begin Phase C with the DMS operation-obligation pilot.
7. Only then begin executable matcher implementation and later manufacturer-audit composition.
