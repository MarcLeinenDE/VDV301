# Finding revalidation — COMMON V2.3

Status: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen legacy finding: `DRCOM23-001`. The frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Byte-pinned official Common V2.3 PDF: SHA-256 `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`, 793521 bytes.
- Exact official authority tag: `VDV-301-2.3`.
- Common V2.3 blob: `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`.
- The official Common V2.3 schema explicitly includes Enumerations V2.2 blob `2a23b512379b18e8f122ac1272cef8229fb86283`.
- Frozen observation mapping: `FR-COM23-011` -> `DRCOM23-001` (plus the pre-existing `DRCOM21-001` StopName facet).
- Preserved base evidence **EV-121** was rerun unchanged and passed.
- Current revalidation evidence: **EV-139**, closure run **33857906408**; pinned visual/evidence run **33857687723**, artifact **9930843755**.
- The exact PDF was searched for the complete `StopInformationRequest` + `ArrivalExpected` + `DepartureExpected` table anchor; page 32 was uniquely selected, rendered, and visibly inspected.
- Root XSD pool and tracked-mutation guards passed before closure.

## Terminal state

| Finding | Terminal state | Revalidation result |
|---|---|---|
| DRCOM23-001 | `executable_confirmed` | PDF page 32 visibly documents `ArrivalExpected 0:1` and `DepartureExpected 0:1` in `StopInformationRequest`; exact V2.3 XSD contains neither there. Preserved EV-121 rejects either request field and accepts both in `StopInformationStructure`. |

The strongest disproof hypothesis — that the expected-time fields are merely described in the wrong table while remaining accepted by the request schema — is rejected by executable validation.

## Closure

- Frozen legacy terminal count: **95 / 192**
- Frozen legacy pending count: **97 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next revalidation block: **COMMON**
- Next subblock: **COMMON V2.4** (`DRCOM24-001`)
