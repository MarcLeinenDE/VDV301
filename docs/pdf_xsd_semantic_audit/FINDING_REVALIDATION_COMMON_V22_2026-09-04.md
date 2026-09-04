# Finding revalidation — COMMON V2.2

Status: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen legacy finding: `DRCOM22-001`. The frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Byte-pinned official Common V2.2 PDF: SHA-256 `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`, 1411558 bytes.
- No upstream `VDV-301-2.2` release tag is invented.
- Exact authority route: historical upstream V2.2 file lineage.
- Common V2.2 blob: `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` at last V2.2 file modification `775def7b24901bfd515c80fa5fe57f12562873fd`.
- Enumerations V2.2 blob: `2a23b512379b18e8f122ac1272cef8229fb86283` at last modification `591ca66d8b94bb5c2a7f9440b3e31e28f8261a88`.
- Frozen observation mapping: `FR-COM22-002` -> `DRCOM22-001`.
- Preserved base evidence **EV-120** was rerun unchanged and passed.
- Current revalidation evidence: **EV-138**, closure run **33857443446**; pinned visual/evidence run **33857241506**, artifact **9930671790**.
- Page 15 was rendered from the exact pinned PDF and inspected visually.
- Root XSD pool and tracked-mutation guards passed before closure.

## Terminal state

| Finding | Terminal state | Revalidation result |
|---|---|---|
| DRCOM22-001 | `executable_confirmed` | Page 15 visibly marks both `NetexMode` choice groups as `-1:1` in VDV choice notation; exact historical V2.2 XSD defines two top-level `xs:choice` compositors with `minOccurs=0`; preserved EV-120 validates an empty `NetexMode`. |

The strongest disproof hypothesis — that the PDF one-of presentation and XSD optional compositors have no executable instance-shape consequence — is rejected by the empty-instance validation.

## Closure

- Frozen legacy terminal count: **94 / 192**
- Frozen legacy pending count: **98 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next revalidation block: **COMMON**
- Next subblock: **COMMON V2.3** (`DRCOM23-001`)
