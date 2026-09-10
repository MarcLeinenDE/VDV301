# Finding revalidation — Generic Subscription Layer (SUB)

Status: **completed** on 2026-09-10 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen findings: `SUB-001`, `SUB-002`. Frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Evidence: **EV-157**; successful closure run **34488450123**.
- Independently successful EV-157 run: **34487918692**, job **102906852658**, artifact **10156457016**, digest `sha256:25bf3344ba21c7a98eea97e48d5f637191a91a96bd9132993808691089eabe12`.
- Source-acquisition evidence: run **34486504933**, job **102902042657**, artifact **10155848626**, digest `sha256:8318472f56fe7c33d85bc5cda3bc02df5cfed7f987dacb832eaa4798a1ff2d4a`.
- Official Base Services V2.0 PDF: SHA-256 `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`, 2374295 bytes, 115 pages.
- Official Base Services V2.1 PDF: SHA-256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`, 2671005 bytes, 130 pages.
- Targeted visual/text pages: V2.0 pages 82, 83, 99, 103; V2.1 pages 83, 84, 112, 116.
- Exact XSD authority/history blobs are recorded machine-readably in the SUB block registry entry.
- The complete 50-file root XSD pool was recompiled and byte-hashed before/after EV-157; no XSD changed.

## Terminal states

| Finding | Terminal state | Revalidation result |
|---|---|---|
| `SUB-001` | `context_verified` | Base Services V2.0/V2.1 document `UnsubscribeData` with `TerminateSubscribeRequestStructure` / `TerminateSubscribeResponseStructure`, while exact Common V1.0/V2.0/V2.1 expose `UnsubscribeRequestStructure` / `UnsubscribeResponseStructure` and no executable `TerminateSubscribe*` aliases. This is a documentation/XSD naming discrepancy; no alias is synthesized. |
| `SUB-002` | `contextual_not_defect` | Official Base Services document generic Subscribe/Unsubscribe operations for SystemDocumentation/SystemManagement although their local XSD groups are sparse. DMS V2.1 explicitly expands generic subscription operations in its local group. Service-group membership is therefore service/version dependent and is not by itself a complete supported-operation authority. |

## Mutation decision

- XSD mutation: **none**.
- Frozen inventory mutation: **none**.
- Registry/status mutation: only the two frozen SUB findings and block/counter handoff.

## State transition

- Before: **144/192 terminal**, **48 pending**, first pending `SUB-001`.
- After: **146/192 terminal**, **46 pending**, first pending `TKT-001`.
- Next block: **TKT**.
