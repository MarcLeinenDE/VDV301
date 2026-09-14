# Finding / provenance baseline freeze — 2026-09-14

Status: **frozen**.

The mandatory legacy-finding revalidation and final readiness reconciliation are complete. This freeze creates the immutable audit-knowledge baseline that later SDK knowledge design or a separately authorized remediation phase must reference.

## Frozen scope

- Frozen finding inventory: **192** entries.
- Final terminal findings: **192**.
- Pending findings: **0**.
- Unresolved findings: **0** at the finding-claim level after `CIS-001` readiness reconciliation.
- Machine-readable baseline: `audit_registry/finding_provenance_baseline_2026-09-14.json`.
- Finding-state digest: `411519c4aaaeb370dfa336d729988d37007a78dfaf5bc6d5fcfb1dfa3f49f792`.
- Authority/provenance digest: `1f4d5b9468668c7b1839585b710fc63ad6a5ef6196f14afbe58c36377c809e95`.
- 50-root-XSD manifest digest: `081cff20627157441c6fb6da11f4026906080e7dd44479e45c8bbcc1ef3dcb26`.
- Baseline payload digest: `d5bf14df302d57a0fc3d71792e1cb00583fafd3e9c7efd19721fd0de353dd576`.

## EV-168 freeze evidence

- Run: **34844500027**.
- Job: **103977033739**.
- Artifact: **10347158213**.
- Artifact digest: `sha256:cf92dcd1e0ca3ca24efc7d8327e3a9ce10d6fc1fc1e2342c0a56ac6ecf36a608`.
- Evidence head: `f0eab8251939ef69c921e721fa5d8db1c049055e`.
- Freeze closure run: **34844751295**.
- Full 50-root-XSD regression: **PASS**.

## Authority guards retained

- `latest-wins` remains forbidden.
- Candidate/integration XSD authority is not promoted to official authority.
- CIS V1.1 has no strict release-XSD profile; its release-XSD identity remains unresolved and routing remains fail-closed.
- The selected XSD remains normative validation authority wherever a strict selected profile exists.

## Phase boundary

`finding_knowledge_ready = true` and the finding/provenance baseline is now frozen.

This **does not authorize XSD changes or official-facing remediation**. Remediation remains a separate explicit decision. SDK finding-knowledge design may reference this frozen baseline without reopening historical findings silently; any later evidence change requires an explicit new baseline/version rather than mutation of this snapshot.

No XSD, PDF source bytes, source-pin registry or original frozen finding inventory was modified by this freeze.
