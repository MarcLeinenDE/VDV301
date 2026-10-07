# Repository handoff integrity policy

Status: **canonical / mandatory**  
Applies to: `dev/schema-integration`

## Purpose

The repository must be sufficient for a new chat, maintainer or AI agent to continue without conversation history. Continuity may never depend on assistant memory or on a final chat response having been delivered.

## Current continuation authority

Only these surfaces define the current continuation point:

1. `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`
2. `00_START_HERE/CURRENT_STATE.json`
3. this policy
4. canonical registries/manifests explicitly named by `CURRENT_STATE.json`

Historical reports, old handoffs, old indexes, scope matrices, findings summaries and backlog documents are evidence only.

## Every prompt/work cycle

### Before work
- fetch the actual `dev/schema-integration` HEAD;
- read the canonical restart documents;
- inspect `CURRENT_STATE.json`;
- inspect the latest applicable validation/handoff-integrity run;
- recover any interrupted/pending block before starting unrelated work.

### During work
- use small terminal blocks;
- every substantive Git commit must already make an immediate chat interruption recoverable from the repository alone;
- never leave the only copy of a finding, correction, decision or next step in chat;
- never create another current-state authority outside `00_START_HERE`.

### Before the final reply
If repository content changed:
1. run/observe the required full gate for substantive canonical changes;
2. resolve failures before calling the block complete;
3. finalize `CURRENT_STATE.json`;
4. ensure the every-push handoff-integrity workflow is green for the final HEAD;
5. verify counts, latest pointers and exactly one next canonical work item.

If repository content did not change:
1. re-fetch HEAD;
2. confirm `CURRENT_STATE.json` still describes the recoverable/current state;
3. do not create a no-op handoff commit.

## Crash-safe intermediate state

A substantive commit may use:
- `work_cycle_state = "gate_pending"`;
- `pending_gate = true`;
- a concrete pending block and recovery instruction.

That state is intentionally recoverable, not complete.

A completed prompt must end with:
- `work_cycle_state = "terminal_clean"`;
- `pending_gate = false`;
- one explicit resume instruction.

## Historical control-document rule

Known old current-sounding documents must begin with:

`<!-- NON_CANONICAL_CONTINUATION_DOCUMENT -->`

Files named `AUDIT_HANDOFF_DELTA_*.md` are historical by definition.

## Validation

Machine check: `tools/validate_repository_handoff.py`  
Every-push workflow: `.github/workflows/handoff-integrity.yml`

## Recovery without chat history

1. Read `00_START_HERE/README.md`.
2. Fetch actual HEAD.
3. Read `CURRENT_STATE.json`.
4. Inspect/run handoff integrity.
5. If `pending_gate=true`, inspect the gate for the actual HEAD.
6. Repair a failed block or finalize a successful-but-unfinalized block.
7. Only then execute the recorded next work item.
