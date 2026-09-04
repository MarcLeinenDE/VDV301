# Finding revalidation — COMMON V2.0

Status: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen legacy finding: `DRCOM20-001`. The frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Byte-pinned official Common V2.0 PDF: SHA-256 `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088`, 946088 bytes.
- Exact official XSD authority: tag `VDV-301-2.0`.
- Common V2.0 blob: `8608e3dcd665c197c34da7f6ec6af5a3758da164`.
- Enumerations V2.0 blob: `27e3c183b00381d959622d13c10543123af8eef6`.
- Preserved base evidence **EV-118** was rerun unchanged and passed.
- Current revalidation evidence: **EV-136**, closure run **33856581531**; pinned visual/evidence run **33851287947**, artifact **9928439083**.
- Page 13 was rendered from the exact pinned PDF and inspected visually because `pdftotext` splits `IBIS-IP.language` across lines.
- Root XSD pool and tracked-mutation guards passed before closure.

## Terminal state

| Finding | Terminal state | Revalidation result |
|---|---|---|
| DRCOM20-001 | `executable_confirmed` | Page 13 visibly types `InternationalTextType.Value` as `IBIS-IP.string` and `Language` as `IBIS-IP.language`; the exact official V2.0 XSD instead declares `xs:string` and `xs:language`. EV-118 confirms the direct primitive instance shape is valid while the literal PDF wrapper-shaped nesting is invalid. |

The strongest disproof hypothesis — that the PDF type notation could be consumed literally without changing XML instance shape — is therefore rejected by executable validation. The XSD remains the validation authority; no wrapper alias is introduced.

## Closure

- Frozen legacy terminal count: **92 / 192**
- Frozen legacy pending count: **100 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next revalidation block: **COMMON**
- Next subblock: **COMMON V2.1** (`DRCOM21-001`)
