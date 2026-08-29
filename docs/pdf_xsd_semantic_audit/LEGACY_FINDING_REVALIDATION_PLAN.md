# Legacy finding revalidation plan

Status: mandatory phase adopted 2026-08-29; execution starts only after Deep Read Pass 2 is complete.

## Purpose

The current Deep Read re-evaluates findings when their documents or subjects are touched. That is not sufficient for the final audit baseline because older findings that are never revisited during the Deep Read could otherwise retain assumptions made before the current evidence discipline existed.

Therefore every pre-existing finding must ultimately pass the same evidence standard defined in:

```text
docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md
```

There is no grandfathering based on age, earlier confidence labels, prior first-pass closure or presence in a historical register.

## Sequencing

```text
finish Deep Read Pass 2
  -> freeze complete finding inventory
  -> revalidate all findings not already explicitly revalidated under the current Evidence Gate
  -> reconcile duplicates/superseded/withdrawn findings
  -> require zero pending SDK-relevant findings
  -> freeze findings/provenance baseline
  -> only then begin remediation decisions and SDK finding-knowledge implementation
```

Deep-Read completion and finding-baseline readiness are separate milestones.

## Complete inventory scope

At the start of this phase, build one inventory from every current finding source, including at minimum:

```text
docs/pdf_xsd_semantic_audit/findings.md
all *_FINDINGS_REGISTER_ADDENDUM.md files
all Deep Read finding deltas
all correction/supersession overlays
audit_registry/deep_read_findings_v0.1.json
all later finding registries/deltas
EV/RV evidence records that confirm, refine or reject findings
historical first-pass reports where a finding still survives into the current state
```

The inventory is frozen only after Deep Read Pass 2 because the finding set can still grow, split, merge, be refined or be withdrawn during the current pass.

## Revalidation eligibility

A finding may skip a second full review only if its current record proves that it was already re-evaluated after adoption of `FINDING_EVIDENCE_GATE.md` and all applicable gate steps were actually completed.

A mere recent edit, restatement, high-confidence label or executable test is not sufficient by itself. The record must make the source/context/definition/disproof work reconstructable.

## Mandatory revalidation steps

Each finding is checked independently against the Evidence Gate:

1. **Original source** – inspect the relevant original byte-pinned PDF page when layout can affect meaning.
2. **Definition provenance** – resolve notation, terminology, table conventions and inherited protocol terms from the authoritative definition.
3. **Exact authority route** – identify exact XSD/service/dependency/variant authority; never latest-wins.
4. **Full semantic context** – inspect surrounding rows/elements, grouping, request/response role, root/group context and version history.
5. **Disproof attempt** – actively test the strongest plausible explanation under which the finding would not be a defect.
6. **Executable evidence** – when XML validity/shape/cardinality/compositor/enum/root behavior is material and technically testable, add or verify positive/negative executable evidence.

A finding that cannot pass a material step remains open; uncertainty is never replaced by inference.

## Revalidation states

```text
pending
source_verified
context_verified
executable_confirmed
contextual_not_defect
withdrawn
unresolved
superseded
```

For documentation-only findings, `context_verified` can be the terminal technical state when executable validation is genuinely not applicable. The reason must be recorded.

## Required record fields

For each inventoried finding, retain or make reconstructable:

```text
finding_id
current_claim
source_registers
pdf_source_id / publication / page-or-section
original_visual_status
notation_or_term_definition_source
selected_xsd_family / non-XSD profile
schema identity / authority class
full_context_checked
counter_hypothesis_checked
executable_evidence_id_or reason_not_applicable
revalidation_state
current classification
validation_behavior
sdk_eligibility
supersedes / superseded_by / withdrawal_reason where applicable
```

## SDK hard gate

The SDK must not consume the final finding knowledge base until this phase is complete.

Readiness requires:

```text
zero pending findings
zero unreconciled duplicate/superseded findings
zero unresolved finding that could alter SDK accept/reject/routing behavior
all XML-validity claims intended for SDK diagnostics executable-confirmed where technically practical
all candidate/integration authority explicitly labelled
```

An unresolved documentation-only issue may remain in the audit if it cannot affect validation behavior, but it must remain labelled unresolved and cannot be promoted into an SDK rule.

## Remediation hard gate

No finding may be treated as an official PDF/XSD correction proposal merely because it survived an older audit pass. Official-facing handling is a later explicit decision based on the revalidated finding set.

## False-finding regression rule

If the second pass uncovers another false finding or a systematic interpretation error:

```text
- withdraw/refine all affected findings;
- search the full inventory for the same reasoning pattern;
- re-evaluate dependent EV/RV evidence;
- add a reusable methodology guard;
- preserve a correction trail;
- do not silently rewrite history.
```

The 2026-08-29 `-1:1` / XML-choice correction is the reference example.

## Completion criterion

This phase is complete only when the machine-readable revalidation registry contains a terminal state for every frozen finding inventory entry and the SDK readiness gate evaluates true.
