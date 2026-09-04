# Finding revalidation — COMMON V2.1

Status: **completed** on 2026-09-04 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen legacy finding: `DRCOM21-001`. The frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Byte-pinned official Common V2.1 PDF: SHA-256 `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32`, 1274051 bytes.
- Exact official XSD authority: tag `VDV-301-2.1`.
- Common V2.1 blob: `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e`.
- Enumerations V2.1 blob: `311464690ad60749ed8d326217787e4b8ed0b718`.
- Frozen observation mapping: `FR-COM21-OBS-013` -> `DRCOM21-001`.
- Preserved base evidence **EV-119** was rerun unchanged and passed.
- Current revalidation evidence: **EV-137**, closure run **33857041308**; pinned visual/evidence run **33856800289**, artifact **9930503494**.
- Page 29 was rendered from the exact pinned PDF and inspected visually.
- Root XSD pool and tracked-mutation guards passed before closure.

## Terminal state

| Finding | Terminal state | Revalidation result |
|---|---|---|
| DRCOM21-001 | `executable_confirmed` | Page 29 visibly specifies `StopInformationRequest.StopName 0:1`; exact V2.1 XSD declares `minOccurs=0 maxOccurs=unbounded`; preserved EV-119 validates an instance containing two `StopName` entries. |

The strongest disproof hypothesis — that the PDF 0:1 maximum is merely non-executable prose compatible with the XSD — is rejected because the exact XSD demonstrably accepts an instance shape beyond that visible maximum.

## Closure

- Frozen legacy terminal count: **93 / 192**
- Frozen legacy pending count: **99 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next revalidation block: **COMMON**
- Next subblock: **COMMON V2.2** (`DRCOM22-001`)
