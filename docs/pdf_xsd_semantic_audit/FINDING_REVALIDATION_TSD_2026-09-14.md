# Finding revalidation — TrainSetDataService (TSD)

Status: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen findings: `TSD-001` through `TSD-004`. Frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Aggregate evidence: **EV-160**; successful closure run **34821906521**.
- Independently successful EV-160 validation run: **34820627306**, job **103901166925**, artifact **10337324977**, digest `sha256:47c862255c57a90fddbe1948f92ca1ebc991e5c5f19d1f6cc78ae117ae77fbac`.
- EV-160 source-acquisition run: **34816735900**, job **103888867262**, artifact **10336466475**, digest `sha256:30089b9d4f2c86dd57f8bb184844a428ee08e91b0d327517c84f6689ea231bfb`.
- Official TrainSetServices V2.1 PDF: SHA-256 `8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e`, 1708401 bytes, 51 pages; targeted physical pages 33–34.
- Official TrainSetServices V2.2 PDF: SHA-256 `c1946694a1809933a9a4a23adff1c551effdb0a2fbc6a7f7f68faec0b0c7bd6e`, 1744296 bytes, 54 pages; targeted physical pages 34, 35, 38 and 40.
- Official General Conventions V2.2 PDF: SHA-256 `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051`, 1562305 bytes, 79 pages; targeted physical pages 47–49 for generic Get/Subscribe/Retrieve context.
- Exact official VDV-301-2.1 commit `585e0bea34b64887db4276f1c94d5f3e78f06c66` / tree `a8472530e840f7b365f6ba1075bfc09758ebda21` and VDV-301-2.2 commit `f283697124750d12189b960b302b399769bad530` / tree `2dbde53864ef07319016b419ff6951f6e90e79dc` were fetched and compiled.
- Historical executable controls **EV-109**, **EV-110** and **EV-104** were rerun successfully before EV-160 closure.
- The complete **50-file root XSD pool** was recompiled and byte-hashed before/after EV-160; no XSD changed.

## Terminal states

| Finding | Terminal state | Revalidation result |
|---|---|---|
| `TSD-001` | `executable_confirmed` | The byte-pinned V2.1 writing specifies Retrieve/Subscribe/Unsubscribe for the TrainSetDataService while the exact official V2.1 XSD exposes only the service-specific Retrieve roots/operation members. EV-109 and EV-160 reconfirm that boundary together with the generic Common subscription structures. |
| `TSD-002` | `executable_confirmed` | The byte-pinned V2.2 operation overview assigns Retrieve*RequestStructure names to UnsubscribeTripRef and UnsubscribeTripInformation, but the detailed definition and exact official XSD use TrainSetUnsubscribeRequestStructure. EV-110 and EV-160 executable checks reconfirm the accepted/rejected shapes. |
| `TSD-003` | `contextual_not_defect` | The exact V2.2 XSD intentionally uses SubscribeResponseStructure for the immediate operation acknowledgement and the corresponding Retrieve response structures for later event payload roots. General Conventions V2.2 provides the generic Get/Subscribe/Retrieve context; TrainSetDataService explicitly extends the concept for parameter-related Retrieve operations. EV-104 and EV-160 therefore support contextual_not_defect. |
| `TSD-004` | `context_verified` | The byte-pinned V2.2 writing on physical page 40 incorrectly names RetrieveTripRefResponseStructure for SubscribeTripInformation event updates. The exact official XSD uses RetrieveTripInformationResponseStructure, while the TripRef parallel on page 38 and in the XSD is internally consistent. This is a documentation reference error. |

## Mutation decision

- XSD mutation: **none**.
- Frozen inventory mutation: **none**.
- PDF source registry/pin mutation: **none**.
- Registry/status mutation: only `TSD-001`…`TSD-004` and the TSD block/counter handoff.

## State transition

- Before: **157/192 terminal**, **35 pending**, first pending `TSD-001`.
- After: **161/192 terminal**, **31 pending**, first pending `TSI-001`.
- Next block: **TSI**.
