# Finding revalidation — VDV 301-2 General Conventions V2.2

Status: **completed** on 2026-09-03 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen V2.2-specific entries: `DR3012GC22-001` and `DR3012GC22-002`. The frozen inventory remains exactly **192 entries**. Older findings that persist into V2.2 are historical support only and are not counted again.

## Evidence

- Evidence gate: **EV-132**, closure workflow run **33782389010**; pinned successful evidence run **33782124756**.
- Official GC V2.2 PDF SHA-256: `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051`, size `1562305` bytes.
- EV-132 artifact: **9903986586**, digest `sha256:18dcb5126dd299eef76fd4a73bb6cf73be3ab653b460495a3511e212e474a7f7`.
- Targeted visible pages: 5, 6, 13, 25, 27, 31, 33, 52, 62, 64, 66, 70.
- Exact VDV-301-2.2 Common blob `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` and Enumerations blob `2a23b512379b18e8f122ac1272cef8229fb86283`.
- Root XSD pool regression gate rerun after EV-132.

## Terminal states

| Finding | Terminal state | Result |
|---|---|---|
| DR3012GC22-001 | `context_verified` | Literal unresolved Word-reference placeholders occur independently in multiple contexts/pages. The V2.2 history nevertheless states technical corrections `Keine/none`. |
| DR3012GC22-002 | `context_verified` | German TOC/body number both SRV and TXT as `3.3.1`; the adjacent English track consistently uses `3.3.1` for SRV and `3.3.2` for TXT, ruling out an intentional shared-number convention. |

Both findings are documentation/navigation defects and do not alter XML validity.

## Closure

- Frozen legacy terminal count: **78 / 192**
- Frozen legacy pending count: **114 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next top-level block: **VDV301-2**
- Next subblock: **General Conventions V2.3**
