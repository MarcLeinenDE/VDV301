# Finding revalidation — SystemMonitoringService (SMS)

Status: **completed** on 2026-09-10 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen findings: `SMS-001`, `SMS-002`, `SMS-003`, `SMS-004`. Frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Evidence: **EV-156**; successful closure run **34460497412**.
- Independently successful EV-156 run: **34460160697**, job **102815828711**, artifact **10145182333**, digest `sha256:67c01039e53841c4fb549af2414c6c957ab8de8a85df7a8ff594f85b2a9ffb19`.
- Supporting executable boundary: **EV-116**, run **33269006407**.
- Earlier independent full render/read evidence: run **33268591224**, artifact **9719396063**, digest `sha256:b7b73746ecdf6b904543c7d6a5312753a57a0b9effec6fe31d1dc83bdfdcec4a`.
- Official SMS V2.2 PDF: SHA-256 `996f639a81cb91ad20a8e78b6213e7c85d41ff0ec42caba4208d6c4652b140f4`, 847416 bytes, 15 pages.
- Physical pages 4, 9, 10, 11, 12 and 13 are the targeted visual evidence set.
- Official upstream tag `VDV-301-2.2` resolves to commit `f283697124750d12189b960b302b399769bad530`.
- Exact XSD blobs: service `d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c`, Common `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`, Enumerations `2a23b512379b18e8f122ac1272cef8229fb86283`.
- The complete root XSD pool was revalidated and byte-hashed before/after EV-156; no XSD changed.

## Terminal states

| Finding | Terminal state | Revalidation result |
|---|---|---|
| `SMS-001` | `contextual_not_defect` | The SMS PDF explicitly routes Subscribe/Unsubscribe payload structures to VDV 301-2-1, and exact Common V2.2 contains the generic Subscribe/Unsubscribe structures. Their absence as service-local SMS elements is therefore not a schema defect. |
| `SMS-002` | `executable_confirmed` | The PDF operation table/body and exact XSD use `ServiceStatus`, while headings 2.5–2.7 use `SystemStatus`. Exact `GetServiceStatusResponse` validates; invented `GetSystemStatusResponse` is rejected. The defect is the PDF naming/headings, not executable behavior. |
| `SMS-003` | `context_verified` | Official SMS PDF page 4 visibly contains an unrelated HTMLDisplayService paragraph in the English foreword. Documentation-only copy/paste defect. |
| `SMS-004` | `context_verified` | Version history page 12 cites `VDV 302-2`, while page 13 identifies the Base Services source as `VDV 301-2-0`. This is a documentation reference-number error. |

## Closure

- Frozen terminal count: **144 / 192**
- Frozen pending count: **48 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next revalidation block: **SUB**
- First pending finding: **SUB-001**
