# Finding revalidation — PassengerCountingService (PCS)

Status: **completed** on 2026-09-10 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen findings: `PCS-001`, `PCS-002`. Frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Evidence: **EV-155**; successful closure run **34448427086**.
- Independently pinned successful EV-155 run: **34447583426**, artifact **10140238171**, digest `sha256:48e3f7ad728660a342124d42976f8a1c88670c06b5ba3a63f7475b462653f633`.
- Official PCS V1.0 PDF: SHA-256 `372be7a5d39c72e4bf405e3058f5af3d809eb611ac3548b70c526788d364c402`, 918762 bytes, 18 pages.
- Official PCS V2.1 PDF: SHA-256 `572f07adbb6999463433a3e764e47f29c8157a4e63aa88ea7c927393da7ec043`, 1084925 bytes, 22 pages.
- V2.1 physical pages 12, 16 and 17 were rendered from the exact byte-pinned PDF and visibly reviewed.
- Exact upstream provenance was pinned to official tags `VDV-301-1.0`, `VDV-301-2.0`, and `VDV-301-2.1`.
- The complete root XSD pool (50 files) was revalidated and byte-hashed before/after closure; no XSD changed.

## Terminal states

| Finding | Terminal state | Revalidation result |
|---|---|---|
| `PCS-001` | `executable_confirmed` | PCS V2.1 selects Common V1.0 + Enumerations V1.0. The exact route accepts an existing V1.0 code but rejects documented `OperationNotSupported`; an Enums V2.1-only explanatory control accepts it. This confirms the PDF/XSD dependency/value-set discrepancy without substituting a newer enum family. |
| `PCS-002` | `contextual_not_defect` | Original VDV-301-1.0 PCS service contains the payload structures but not the operation root; the V1.0 aggregate supplies the root. The later official VDV-301-2.0 self-contained PCS V1.0 supplies the same root, and the same sample payload validates through both complete routes while the checked payload type signatures remain unchanged. This is historical packaging/resolver context, not a payload-contract defect. |

## Closure

- Frozen terminal count: **140 / 192**
- Frozen pending count: **52 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next revalidation block: **SMS**
- First pending finding: **SMS-001**
