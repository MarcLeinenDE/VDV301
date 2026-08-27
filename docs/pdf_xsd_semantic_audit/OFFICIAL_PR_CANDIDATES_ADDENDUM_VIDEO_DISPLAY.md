# VideoDisplayService post-audit official-facing candidates

Tracking only. Do not open or modify any upstream PR without explicit user approval.

## VDS-CAND-001 - compositor family

Linked findings:

```text
VDS-002
VDS-003
VDS-004
```

Evidence summary:

```text
Public V1.0 and V2.0 PDFs consistently describe multi-field structures.
Official V2.0 XSD uses xs:choice in all checked structures.
The same V2.0 blob remains on current upstream master.
No matching upstream correction PR was found in the first-pass search.
```

Before any official-facing proposal:

```text
- compile exact V2.0 pool,
- prove PDF-shaped multi-field samples fail,
- assess whether intended fix is sequence/structured response or another model,
- search implementations/codegen impact,
- keep any patch minimal,
- require explicit user approval before PR preparation/opening.
```
