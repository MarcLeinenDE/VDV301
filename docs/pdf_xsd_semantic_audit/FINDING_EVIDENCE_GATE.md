# Finding evidence gate

Status: adopted as mandatory audit policy from 2026-08-29.

## Purpose

This gate exists to prevent false findings caused by an unverified interpretation of notation, terminology, table layout, schema context or version history. A visible difference is not yet a defect.

The audit feeds later remediation decisions and the validation SDK. Therefore false-positive findings are treated as a methodology failure, not as harmless noise.

## Core rule: prove the meaning before judging the mismatch

Before a new or existing finding is promoted beyond a candidate state, the auditor must establish what every material symbol, term, label, grouping and version reference actually means in its original context.

This is especially mandatory for:

- Min:Max/cardinality notation and choice markers;
- table prefixes, letters, indentation, grouping and footnotes;
- operation/request/response labels;
- wrapper/type terminology;
- enumeration spelling and case;
- protocol terminology inherited from another standard;
- cross-references and version-history statements.

Do not infer a meaning merely because it looks familiar.

## Definition-source order

When notation or terminology is not self-evident, resolve it in this order:

1. definition, legend, glossary or explanatory text in the same official VDV publication;
2. normative/base VDV publication explicitly defining the convention used by the document;
3. official predecessor/successor publication when needed to establish historical meaning;
4. referenced external standard/RFC/specification when the VDV text delegates the meaning to it.

The source used to resolve the meaning must be recorded. If the original definition cannot be established with sufficient confidence, the finding stays unresolved or `visual_review_required`.

## Mandatory evidence steps

Every substantive PDF/XSD finding must pass the following steps where applicable.

### 1. Original-source verification

Inspect the visible original PDF page, preferably from byte-pinned source material. Verify surrounding rows, headings, footnotes, grouping and page context, not only an extracted line.

If only native text/OCR is available and layout can affect meaning, do not promote the finding beyond a review-required state.

### 2. Notation/term provenance

Resolve any notation or specialized term from its original definition before interpreting it.

Example: `-1:1` cannot be evaluated as a numeric cardinality until the VDV Min:Max/Choice definition is consulted. The leading minus is an XML-choice marker, not a negative minimum.

### 3. Exact executable authority

Identify the exact selected XSD family and exact dependency route. Record the relevant schema version/file and, where authority/provenance is material, the Git blob/tag/variant identity.

Never compare a PDF against a neighbouring or latest schema merely because it is easier to find.

### 4. Full-context comparison

Compare the complete semantic unit rather than an isolated token:

- neighbouring rows/elements;
- sequence/choice/group context;
- request vs response role;
- acknowledgement vs data-event role;
- global root vs local operation-group role;
- predecessor/successor history;
- surrounding explanatory prose.

### 5. Disproof attempt

Before confirmation, actively try to invalidate the proposed finding.

At minimum ask:

- Is there a legend/definition that changes the apparent meaning?
- Is this an intentional choice/group convention?
- Is the PDF row only a label while detail text gives the real structure?
- Is the XSD using a shared/generic model intentionally?
- Is the apparent mismatch caused by the wrong schema/version/dependency family?
- Does another section or version history explicitly explain the difference?

Record the strongest counter-explanation considered and why it did or did not resolve the issue.

### 6. Executable confirmation when validation behaviour is affected

If a finding claims that valid/invalid XML behaviour differs, add a positive/negative executable sample whenever technically practical.

Static inspection alone may establish a spelling/documentation defect, but claims about accepted XML shape, cardinality, compositor behaviour, enum acceptance or root availability should be executable-confirmed before being used as SDK validation knowledge.

## Finding promotion states

Use the following confidence progression conceptually even if an older register uses legacy wording:

```text
candidate_observation
  -> source_verified
  -> context_verified
  -> executable_confirmed          # when executable behaviour is material
  -> remediation_ready             # only in later explicit remediation phase
```

A finding may stop at any earlier state. Lack of evidence must reduce certainty; it must never be filled by assumption.

## Hard stop conditions

Do not mark a finding `confirmed` when any material condition below remains unresolved:

- the visible PDF layout could change the interpretation and has not been inspected;
- the notation/term meaning has not been traced to an authoritative definition;
- the exact XSD family/dependency route is unknown;
- a plausible intentional modelling explanation has not been checked;
- a claimed XML-validity difference can be tested but has not yet been tested and the finding is intended to drive SDK behaviour.

Use `candidate`, `unresolved`, `needs_visual_review` or equivalent instead.

## Finding record requirements

For new findings, record or be able to reconstruct:

```text
finding_id
claim
pdf_source_id / publication / page-or-section
original_visual_status
notation_or_term_definition_source
selected_xsd_family
schema_identity / authority class
full_context_checked
counter_hypothesis_checked
executable_evidence_id_or_reason_not_applicable
confidence_state
validation_behavior
sdk_eligibility
```

## SDK eligibility rule

Audit knowledge and executable validation rules are different layers.

```text
candidate/unresolved finding
  -> may appear only as internal audit context; must not cause a validation failure

source/context verified documentation finding
  -> may explain a result, but does not override the selected XSD

executable-confirmed validation-behaviour finding
  -> may be used by the SDK as explanatory diagnostic knowledge while the selected XSD remains normative authority

remediation decision
  -> separate later phase; never inferred automatically from finding existence
```

The SDK must never normalize, reject, accept or reroute payloads because of an unverified finding.

## Regression rule after a corrected false finding

When a false finding is discovered because the audit misunderstood notation or context:

1. correct or withdraw every affected finding;
2. search the existing audit for the same reasoning pattern;
3. add a reusable methodology guard so the failure mode cannot silently recur;
4. re-evaluate any executable evidence whose rationale depended on the wrong interpretation;
5. keep an explicit correction trail rather than silently rewriting history.

The 2026-08-29 `-1:1` correction is the first explicit application of this rule.
