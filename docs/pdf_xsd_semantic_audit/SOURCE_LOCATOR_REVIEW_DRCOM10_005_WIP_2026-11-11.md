# DRCOM10-005 — ShortTripStopList preliminary source/body and scope review (2026-11-11)

**Status:** in progress; **not** terminal, **not** a completed source locator, and **no new audit count**. Resume from the authoritative `00_START_HERE/CURRENT_STATE.json`. Two independent original-page visual checks and both full CI gates are still outstanding.

## Stable identity and precise discrepancy

Existing unique finding `DRCOM10-005`. It is **not** a new duplicate of earlier Common or CE findings.

Every exact selected Common XSD V1.0, V2.0, V2.1, V2.2, V2.3 and candidate/integration V2.4 defines `ShortTripStopListStructure` with a repeating `ShortTripStop` child of `ShortTripStopStructure` (implicit minOccurs=1, explicit maxOccurs=unbounded). The official Common PDF versions examined in preserved deep reads refer to the repeated *inner* child as `ShortTripStopList` (same as its outer type). The key behavioral difference is **case-/spelling-exact XML element name**: the PDF-derived inner `ShortTripStopList` is schema-invalid, while the exact XSD child is `ShortTripStop`.

**Historical-only additional type reference:** Common V1.0 PDF §1.46 Table46 prints `+StopPointTariffInformation` as the inner type (cf. §1.49), whereas its XSD member uses `ShortTripStopStructure`. Both exact V1.0 complex types `ShortTripStopStructure` and `StopPointTariffInformationStructure` have the same required sequence: `JourneyStopInformation` of `JourneyStopInformationStructure`, then `FareZoneInformation` of `FareZoneInformationStructure`. Thus no distinct XML instance-shape failure attributable solely to the type label is demonstrated. The later Common V2.0–V2.4 PDFs show `+ShortTripStop` as the type, so **do not propagate the V1.0 type-name facet** into those later versions.

## Original visible PDF body: verified portions (same exact byte pins)

These four rendered PNGs were **actually reopened** from original SHA-pinned `DRCOM10-004` fallback artifact ZIPs; each PNG was independently SHA-256 recalculated, compared with its original renderer manifest and inspected visually, including the section heading and table captions. The ZIPs were created by the source-pin-verifying `tools/render_vdv_pdf_pages.py` workflow; no changed source was substituted.

| Version | PDF SHA256 | Body section/page/table | PDF child/type | Original image SHA256 | Github run/artifact |
|---|---|---|---|---|---|
| Common V1.0 | `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf` | printed p18, §1.46, **Table 46 — Description of ShortTripStopList** | `ShortTripStopList` / `StopPointTariffInformation`, 1:* | `1072f924d50e9797e9528cbe07732809e6bd856d51b5d7a7d074d67a7d30e848` | run `43029589455` / artifact `13860986360` |
| Common V2.0 | `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088` | printed p26, §2.48, **Table 48 — Description of ShortTripStopList** | `ShortTripStopList` / `ShortTripStop`, 1:* | `1e2825a759ee9374d7d3957a991231a004139a22913ed2f9076f81556115cca1` | run `43029612445` / artifact `13860711734` |
| Common V2.2 | `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203` | printed p29, §2.49, **Table 49 — Description of ShortTripStopList** | `ShortTripStopList` / `ShortTripStop`, 1:* | `248cfab843bb21903c9a462582f9262b150436fb6158c3c50746b15d486e9766` | run `43029726595` / artifact `13860087462` |
| Common V2.4 | `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a` | printed p32, §2.48, **Table 48 — Description of ShortTripStopList** | `ShortTripStopList` / `ShortTripStop`, 1:* | `b5906fb9c08b8c7cc8a249f4165974f8be64ba7d2be3ce1c6a398f1f180d03f0` | run `43029777221` / artifact `13860357046` |

**Pending actual visible original-body checks:** V2.1 p28 §2.48 Table48 and V2.3 p30 §2.49 Table49. Their earlier deep reads and official PDF **text layer** explicitly show the same inner name/type and 1:* (V2.1 official SHA256 `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32`, V2.3 SHA256 `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`). However, the fresh web PDF screenshots failed with a render-cache miss, and the new deterministic GitHub fallback jobs have not completed. **Do not mark these two versions as newly visual/body verified yet.** New pinned visual workflow runs: V2.1 `43097923313`; V2.3 `43097965762` (queued at last inspection). Older all-pages render evidence exists in deep reads, but V2.1 historical artifact `9837875704` was missing (404); V2.3 historical artifact `9856965744` download timed out. No independent target-image digest is available for these two in this cycle.

## Exact selected XSDs independently re-read

| Profile | Exact Common XSD Git blob | ShortTripStopList type / child line | ShortTripStopStructure members | StopPointTariffInformationStructure members | Authority |
|---|---|---|---|---|---|
| V1.0 | `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c` | 509 / 511 | 514–518 | 592–596 | official release, Enum V1.0 |
| V2.0 | `8608e3dcd665c197c34da7f6ec6af5a3758da164` | 515 / 517 | 520–524 | 598–602 | official release, Enum V2.0 |
| V2.1 | `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e` | 514 / 516 | 519–523 | 597–601 | official release, Enum V2.1 |
| V2.2 | `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` | 523 / 525 | 528–532 | 606–610 | official release, Enum V2.2 |
| V2.3 | `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` | 573 / 575 | 578–582 | 662–666 | official release, **Enum V2.2** |
| V2.4 | `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` | 588 / 590 | 593–597 | 704–708 | candidate/integration, Enum V2.4; upstream PR #31 still open |

All six declarations have `<xs:element name="ShortTripStop" type="ShortTripStopStructure" maxOccurs="unbounded"/>`. The two referenced structures have identical required member names, order and types across these exact snapshots. The preserved V1.0 `EV-117` / `EV-135` report independently confirms the **child-name** executable boundary; **no fresh six-version executable-instance regression was run here**, and the later-version XSD conclusions are static declaration evidence.

## Active disproof / scope

- **Outer vs inner element:** The PDF's topmost table header is properly named `ShortTripStopList`; it is the **repeated member inside the list** whose PDF label also says `ShortTripStopList`. The XSD child is `ShortTripStop`; replacing the wrapper name would be a different claim.
- **Type identity:** The PDF's V1.0 `StopPointTariffInformation` is a different name from the XSD's `ShortTripStopStructure`, but both exact types expand to the same XML content model. No fabricated type-based XML invalidity.
- **History:** V2.0 onward visually confirmed PDF type `ShortTripStop`; do not carry V1.0 type misreference beyond its version. All six selected XSD blobs checked; no corrected member-name successor in this audited set.
- **Authority:** Official release schema V1.0–V2.3; V2.4 open candidate/integration. Never relabel candidate official or use newer XSD for historical data.
- **SDK:** Preserve strict selected-XSD `INVALID` for an inner wrong-name child, with optional explanatory `error_with_advisory`. Runtime mapping remains reviewed, **not implemented**; no schema or compatibility mutations.

## Pending closure criteria

1. Original visible Common V2.1 p28 and V2.3 p30 rendered through exact pinned-byte fallback with verifiable PNG/source hashes.
2. Update one unique `DRCOM10-005` semantic scope, both-language diagnostics, runtime mapping, source-locator record, body register, version-boundary register and SDK/Current State mirrors.
3. Full schema-audit-validation and handoff-integrity **SUCCESS on substantive HEAD**, then a separately committed `terminal_clean` handoff with both **final HEAD** checks SUCCESS. Credit **89/192** only after completion; currently **88/192**.
4. Once completed, persist only distilled, nonredundant finding knowledge through a reviewed PR in private `MarcLeinenDE/ai-mem` `memory/projects/vdv301/`, preserving actual workrepo CI/Commit provenance. Do not claim synchronisation or modify ai-mem before success.
