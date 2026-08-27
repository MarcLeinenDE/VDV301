# Official PR candidates after audit

Status: tracking list only.

Purpose:

```text
Collect possible official-facing schema/documentation correction candidates found during the PDF/XSD semantic audit.
Do not open any official VDVde/VDV301 PR from this list during the audit.
```

## Policy

The audit uses this rule:

```text
Validation follows XSD.
PDF differences are recorded as explanatory/provider-facing notes.
```

A later official PR candidate is a separate decision and must happen only after:

```text
1. the full audit pass is complete,
2. the finding is rechecked against the current official VDVde/VDV301 repository state,
3. the relevant PDF table is visually confirmed where spelling/casing is involved,
4. historical XSD/PDF versions are checked,
5. local XSD compilation and targeted sample validation are run,
6. the change scope is kept minimal and reviewable,
7. the user explicitly approves preparing or opening a PR.
```

## Do not mix with current official PR #31

Current official-facing draft PR path:

```text
VDVde/VDV301 PR #31
Add DeviceManagementService V2.4 schema candidate
```

Do not mix unrelated Common/Enums corrections into that DMS V2.4 PR.

Potential typo/correction PRs should be separate, narrow branches after the audit.

## Candidate classes

| Class | Meaning | PR suitability |
|---|---|---|
| typo-like XSD spelling | XSD spelling appears obviously wrong, e.g. transposed/missing letters | possible, but breaking; needs careful review |
| PDF/XSD case mismatch | PDF prints different case than XSD | usually provider note first; PR only after historical check |
| cardinality mismatch | PDF says different occurrence count than XSD | not a typo; needs semantic/history review |
| PDF-only value/name | PDF lists item omitted by XSD | likely documentation or XSD question; needs history |
| XSD-only value/name | XSD permits item omitted by PDF | likely documentation or XSD question; needs history |

## Current possible PR candidates

### PR-CAND-001 - `GlobalCardStausID` spelling

Linked finding:

```text
CE-016
```

Current observation:

```text
PDF: GlobalCardStatusID
XSD: GlobalCardStausID
```

Initial assessment:

```text
Strong typo-like candidate, but potentially breaking for existing consumers that already implemented the XSD spelling.
```

Required before PR decision:

```text
- visually confirm PDF table spelling,
- check V1.0-V2.4 history for the same spelling,
- search current official repo/forks for existing usage,
- test both positive and negative XML samples,
- decide whether schema change, documentation note, or compatibility alias approach is feasible.
```

### PR-CAND-002 - `Desciption` spelling in TSPPoint

Linked finding:

```text
CE-017
```

Current observation:

```text
XSD: Desciption
Expected semantic spelling likely: Description
PDF table spelling still needs visual confirmation.
```

Initial assessment:

```text
Potential typo-like candidate, but not yet mature enough for a PR because PDF visual confirmation and history are still pending.
```

Required before PR decision:

```text
- visually confirm V2.4 PDF table spelling,
- check V1.0-V2.4 history,
- search current official repo/forks for `Desciption` and `Description`,
- run sample validation,
- decide whether change is safe or whether provider-facing note is preferable.
```

### PR-CAND-003 - AdditionalAnnouncement `InformationAtSpecificPoint` vs `SpecificPoint`

Linked finding:

```text
CE-013
```

Current observation:

```text
PDF: InformationAtSpecificPoint
XSD: SpecificPoint
```

Initial assessment:

```text
Not a plain typo. It may be a table label, an intended semantic name, or a schema/documentation mismatch. Treat as historical/semantic review item, not an immediate PR.
```

### PR-CAND-004 - cardinality discrepancy candidates

Linked findings:

```text
CE-011 Connection TransportMode/ConnectionMode PDF 0:* vs XSD 0:1
CE-012 DeviceSpecificationWithStateList PDF 1:* vs XSD 0:*
CE-014 DataVersionList PDF 1:* vs XSD 0:*
```

Initial assessment:

```text
Not typo candidates. These need compatibility/history and real-world usage review before any official PR consideration.
```

## End-of-audit review checklist

At the end of the full PDF/XSD audit, perform a dedicated review block:

```text
1. List all CE findings.
2. Split them into documentation notes, tool-only notes, validation backlog items and possible official PR candidates.
3. For each possible PR candidate, re-fetch current official upstream state.
4. Check whether another open PR already covers the same issue.
5. Run local schema compilation and targeted sample validation.
6. Prepare minimal patch candidates, but do not open PRs until explicitly approved.
```
