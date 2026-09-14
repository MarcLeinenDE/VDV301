# Finding revalidation — VideoDisplayService (VDS)

Status: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen findings: `VDS-001` through `VDS-008`. Frozen inventory remains exactly **192 entries**.

## Evidence

- Aggregate evidence: **EV-164**; closure run **34839487830**.
- Successful EV-164 validation run: **34838003303**, job **103956188197**, artifact **10345007994**, digest `sha256:ef85ea5999c2fee585b493fb3705031d6a231e251efab7bcce6d92e30d6f05dd`, head `233e54e59bb027a629c9f16274666b336866951d`.
- Underlying executable compositor evidence: **EV-103**, run `33111119723`, job `98653897734`, artifact `9662552176`.
- VDS V1.0 PDF: official byte pin `9280cc239cf71bb158ab5941b522a2c4c822420e07ed44f4d4111d9689418480`, visual run `33225843645`.
- VDS V2.0 PDF: official byte pin `c287df20d8225af2afcd37dfdb487eb4922b89ce78c287da91745d12b410c8a2`, visual run `33226294383`.
- Official V2.0 XSD authority: `VDV-301-2.0` / commit `f2569a91f0a7c737a0ca7c0280b28ad223d7ee08`; VDS blob `fcfdadd3b62a584370cae326004050b4dc832e23`, Common `8608e3dcd665c197c34da7f6ec6af5a3758da164`, Enums `27e3c183b00381d959622d13c10543123af8eef6`.
- Complete regression pool: **50 root XSDs — PASS**.

## Terminal decisions

| Finding | State | Decision |
|---|---|---|
| VDS-001 | `context_verified` | The provenance gap itself is verified: the official V1.0 publication exists, but no exact official V1.0 VideoDisplayService service XSD is confirmed in the checked official release route. V2.0 is explicitly not substituted. |
| VDS-002 | `executable_confirmed` | Official V2.0 PDF describes a multi-field capability record; exact V2.0 XSD uses `xs:choice`. EV-103 confirms the executable boundary. |
| VDS-003 | `executable_confirmed` | Official V2.0 PDF requires `ViewID + Timeout`; exact V2.0 XSD uses `xs:choice`. EV-103 confirms the executable boundary. |
| VDS-004 | `executable_confirmed` | Official V2.0 response tables group related fields; exact V2.0 XSD response structures use `xs:choice`. EV-103 confirms the executable boundary. |
| VDS-005 | `context_verified` | Broken generated cross references are visibly present in byte-pinned V1.0 and corrected/absent in V2.0. Documentation-only. |
| VDS-006 | `context_verified` | Corrected finding only: the leading minus is valid VDV XML-choice notation. The surviving issue is the visually verified incomplete/degenerate application (`a`/`-1:1` without a visible peer alternative). The older invalid-cardinality interpretation is superseded and must not be reused. |
| VDS-007 | `context_verified` | Cross-document `VideoDisplayService v1.1` reference label conflicts with the dedicated official VDS V1.0 identity. No V1.1 validation profile or schema alias is inferred. |
| VDS-008 | `context_verified` | VDS expands RTP/SOA incorrectly; terminology was rechecked against RFC 3550 and the OASIS SOA Reference Model. No XML/XSD validation behavior changes. |

## Authority boundaries

- VDS V1.0 remains documentation authority only for this audit because the exact strict V1.0 service-XSD route remains unresolved.
- VDS V2.0 executable conclusions use the exact official release-tag XSD family only.
- `VDS-006` must always be read through the 2026-08-29 choice-notation correction overlay.
- Documentation terminology/reference findings do not override XSD authority and do not create SDK rejection/acceptance rules.

## Closure

Prestate: **168 terminal / 24 pending**, first pending `VDS-001`.

Poststate: **176 terminal / 16 pending**, first pending `VLS-001`. Next block: **VLS**.

No XSD, frozen inventory, PDF source registry, or PDF source-pin mutation is part of this closure.
