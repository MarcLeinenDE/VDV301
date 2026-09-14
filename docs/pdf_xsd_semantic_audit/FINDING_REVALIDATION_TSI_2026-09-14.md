# Finding revalidation — TrainSetInformationService (TSI)

Status: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen finding: `TSI-001`. Frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Aggregate evidence: **EV-161**; successful closure run **34822926605**.
- Independently successful EV-161 validation run: **34822675019**, job **103907586878**, artifact **10339022101**, digest `sha256:705aa436963a49f4478099f884b63d19d14f02f79a18c3cde89603ecb31fced8`.
- Exact TrainSet V2.1 source reused from EV-160 source acquisition: run **34816735900**, artifact **10336466475**, digest `sha256:30089b9d4f2c86dd57f8bb184844a428ee08e91b0d327517c84f6689ea231bfb`.
- Official TrainSetServices V2.1 PDF: SHA-256 `8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e`, 1708401 bytes, 51 pages. Physical page 24 defines the fields of a coach data set; physical page 25 says the response returns a sequence of coach data sets, one per coach. The embedded page-25 XSD diagram was treated as visual evidence because Poppler does not expose its labels reliably.
- Exact official V2.1 TSI XSD blob `897f373e31b76aa23d8bc206854b042524e4c102` models a single flat coach-field sequence with no repeated coach wrapper. EV-109 and EV-161 both prove one flat record validates and a second documented coach record is rejected.
- V2.2 blob `7ab1f8f892bfcea2a8b8a055f07de92c143356f9` introduces `SingleCoach` with `maxOccurs=unbounded`; this is correction-history evidence only and is not back-applied to V2.1.
- The complete **50-file root XSD pool** passed again and no XSD changed.

## Terminal state

| Finding | Terminal state | Revalidation result |
|---|---|---|
| `TSI-001` | `executable_confirmed` | Official V2.1 prose requires multiple coach data sets while exact V2.1 validation cannot represent more than one flat coach record. |

## Mutation decision

- XSD mutation: **none**.
- Frozen inventory mutation: **none**.
- PDF source registry/pin mutation: **none**.
- Registry/status mutation: only `TSI-001` and the TSI block/counter handoff.

## State transition

- Before: **161/192 terminal**, **31 pending**, first pending `TSI-001`.
- After: **162/192 terminal**, **30 pending**, first pending `TSM-001`.
- Next block: **TSM**.
