# Exhaustive independent validation policy

Status: SDK/audit governance baseline.

## Core rule

The SDK MUST NOT stop validation at the first finding or first failed validation layer.

A validation run must continue through every independent check for which the required evidence/input is still available. The purpose is to return the fullest technically valid finding set from one observation/run.

Example: an XML/XSD failure does not suppress independent HTTP checks such as method, HTTP version, Content-Type or other observable transport metadata.

## Dependency-aware execution

Checks are organized by explicit prerequisites, not by a global fail-fast pipeline.

A failed check blocks another check only when the second check genuinely requires the failed/missing result as an input.

Examples:

- malformed/non-parseable XML can block XSD validation and checks requiring an XML element tree;
- XSD-invalid but parseable XML does not automatically block independent HTTP, discovery, transport or metadata checks;
- invalid Content-Type does not suppress XSD validation when the XML bytes are otherwise available and parseable;
- a discovery failure may block a check that requires a resolved endpoint, but must not suppress checks on discovery evidence already captured;
- one failed service operation must not suppress independent checks for other captured operations/messages.

## Per-check outcomes

The execution/result model must distinguish at least:

- `PASS` — the check executed and the observed evidence conforms;
- `FAIL` — the check executed and a mandatory applicable requirement is violated;
- `WARNING` — the check executed and an advisory/recommended/non-hard-fail condition is relevant;
- `NOT_APPLICABLE` — the check does not apply to the selected profile/evidence;
- `BLOCKED_BY_DEPENDENCY` — the check is applicable in principle but cannot execute because a specific prerequisite is unavailable/invalid.

`BLOCKED_BY_DEPENDENCY` is not a PASS and not a substitute for FAIL. It must identify the blocking prerequisite/check.

An implementation may additionally expose INFO/profile notes, but these do not replace the outcomes above.

## Result aggregation

A run returns an aggregate collection of all executed and dependency-blocked checks, not one terminal error.

Overall conformance may be FAIL when one or more hard failures exist, while the report still contains all other PASS/FAIL/WARNING/NOT_APPLICABLE/BLOCKED results discovered in that run.

The SDK must preserve every occurrence needed for evidence. Presentation may group repeated findings, but grouping must not discard occurrences.

## Authority independence

Validation layers retain their own authority:

- selected XSD for VDV XML structure/content;
- VDV PDF/profile rules for non-XSD requirements;
- externally normative protocol rules through the external-standard authority chain;
- known-issue diagnostics as explanatory overlays that never override normative validation.

A failure in one authority layer does not invalidate evidence available to another independent authority layer.

## Diagnostic requirements

Each blocked check must expose:

- the check that could not execute;
- the prerequisite/check that blocked it;
- why that prerequisite is required;
- what evidence would allow execution.

Each FAIL/WARNING retains its own source/authority references. Do not collapse multiple independent violations into only the first/root-cause message.

## Implementation gate

Before a runtime validator is considered complete, tests must demonstrate at least:

1. two independent simultaneous failures are both reported;
2. XSD FAIL plus HTTP/Content-Type FAIL are both reported when both checks can execute;
3. malformed XML blocks XSD-dependent checks but HTTP checks still execute;
4. one blocked check does not stop an unrelated validation branch;
5. aggregate result is FAIL when any mandatory executed check fails;
6. repeated occurrences are retained losslessly even if presentation groups them.

This policy is mandatory for later runtime matcher/validator implementation.
