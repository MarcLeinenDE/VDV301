# Finding revalidation — VDV 301-2 General Conventions V2.3

Status: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen V2.3-specific entry: `DR3012GC23-001`. The frozen inventory remains exactly **192 entries**. Older findings persisting into V2.3 are historical support only and are not counted again.

## Evidence

- Evidence gate: **EV-133**, closure workflow run **33843433114**; pinned successful evidence run **33842952649**.
- Official GC V2.3 PDF SHA-256: `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603`, size `1057483` bytes.
- EV-133 artifact: **9925516670**, digest `sha256:7fb77ca6ca5c1950b45d49fe983118831e4cae187997d2568b203e97a89f4b33`.
- Targeted visible pages: **70 and 71**.
- Page 70 visibly establishes the predecessor German `7.1.1` / `7.1.2` numbering under `7.1 Version 2.2`.
- Page 71 visibly shows `7.2 Version 2.3` followed by German `7.1.3` / `7.1.4`, while the adjacent English headings correctly use `7.2.1` / `7.2.2`.
- Exact official Common V2.3 blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` and Enumerations V2.2 blob `2a23b512379b18e8f122ac1272cef8229fb86283`.
- EV-133 also confirms that the literal unresolved Word-reference placeholders from V2.2 are absent in V2.3.
- Root XSD pool regression gate and tracked-mutation guard passed.

## Terminal state

| Finding | Terminal state | Result |
|---|---|---|
| DR3012GC23-001 | `context_verified` | German V2.3 version-history subsection numbers remain in the 7.1 namespace despite being placed under 7.2; the adjacent English track provides a direct same-page corrective control. |

This is a documentation/navigation defect and does not alter XML instance validity or create an XSD alias.

## Closure

- Frozen legacy terminal count: **79 / 192**
- Frozen legacy pending count: **113 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next top-level block: **VDV301-2**
- Next subblock: **General Conventions V2.4 (`DR3012GC24-001…005`)**
