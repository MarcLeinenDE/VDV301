# SOURCE LOCATOR REVIEW — DRCOM10-006 — 2026-11-11

**Status:** All six exact byte-pinned original Common PDF body tables and corresponding exact selected Enumerations XSDs independently checked. One existing unique finding, five affected historical official lanes, one corrected/nonaffected V2.4 boundary. This report is evidence; canonical completion/gates remain exclusively in `00_START_HERE/CURRENT_STATE.json`.

## Identity and active falsification

Existing unique **DRCOM10-006**, not a new finding. The historic V1.0-only affected scope was insufficient: original official PDF V1.0, V2.0, V2.1, V2.2 and V2.3 each literally lists `DoorCountingObjectClassEnumeration` value `Wheelchair` and `Others`; the exact selected historical official XSDs instead permit `WheelChair` and `Other`. Enum comparison is exact and case-sensitive. The official Common V2.4 PDF visibly corrects this to `Wheelchair` and `Other`, and the separately selected V2.4 Candidate/Integration Enumerations XSD aligns. **V2.4 is boundary evidence only**, not an affected runtime lane.

Two subfacets should not be conflated: `WheelChair` is most plausibly a historic XSD spelling error, while PDF plural `Others` is most plausibly a PDF typo. Publisher intent remains inferential; record the primary mismatch as **cross_artifact_mismatch**, not two new findings or unquestioned source blame. No XSD byte changes or aliases are authorized.

## Exact official body source and page-verification evidence

All six images were actually reopened from GitHub Actions artifacts. For each, its PNG SHA-256 was calculated and compared with the historical artifact manifest or the new pinned-render manifest; the manifest's PDF SHA-256 and byte length match canonical official source pins. Actual visible body heading, caption/table number and values (with nearby quality enum) were inspected independently. V2.2 used a **new** exact-byte render after earlier archived render ZIP 9840345496 was unavailable; web PDF screenshot cache miss did not become a permanent limitation.

| PDF | Actual visible printed locator | PDF enum values | Source PDF SHA-256 | Size | PNG SHA-256 | GitHub run / artifact |
| --- | --- | --- | --- | ---: | --- | --- |
| V1.0 | p25 §2.5 **Table 66** | `Wheelchair` / `Others` | `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf` | 892769 | `9f04ac5752593244ed64c2dea63cc3b6cb178a16e42e30317e21661977759d6f` | [33275626001](https://github.com/MarcLeinenDE/VDV301/actions/runs/33275626001) / `9721397514` |
| V2.0 | p33 §3.7 **Table 71** | `Wheelchair` / `Others` | `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088` | 946088 | `e46eca6795d0937297f467873606c5a0a04b68abfc41eb94878c41c8a373cced` | [33279811315](https://github.com/MarcLeinenDE/VDV301/actions/runs/33279811315) / `9722644456` |
| V2.1 | p35 §3.7 **Table 71** | `Wheelchair` / `Others` | `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32` | 1274051 | `6b24840923db24358dcc608ddc375049b1674820caf856144ed754343f71aa1a` | [33393002497](https://github.com/MarcLeinenDE/VDV301/actions/runs/33393002497) / `9758203545` |
| V2.2 | p37 §3.7 **Table 72** | `Wheelchair` / `Others` | `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203` | 1411558 | `f32eff839640963aeae32439e28610c500520141980aa784937bf82542e24215` | [43105456014](https://github.com/MarcLeinenDE/VDV301/actions/runs/43105456014) / `13894152180` |
| V2.3 | p38 §3.7 **Table 72** | `Wheelchair` / `Others` | `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b` | 793521 | `dbf014908cc54fcc23cbb4812eb1934c0631a90023608fc7d7e756f69debe4a5` | [33656579631](https://github.com/MarcLeinenDE/VDV301/actions/runs/33656579631) / `9856965744` |
| V2.4 | p41 §3.7 **Table 71** | `Wheelchair` / `Other` | `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a` | 1689647 | `191d2b0b4421a8f3c923933291f334ff111f48f2e0a247399aef0ea91ba172db` | [33658306978](https://github.com/MarcLeinenDE/VDV301/actions/runs/33658306978) / `9857652638` |

Each row is the visible **Description of DoorCountingObjectClassEnumeration** table, not a TOC-inferred table. The V1.0 page uses §2.5 Table66, all V2.x pages use §3.7 with their distinct actual table numbers. The exact official URLs, image archive filenames, and hash evidence are also retained in the canonical source-locator registry and intermediate [WIP evidence](SOURCE_LOCATOR_REVIEW_DRCOM10_006_WIP_2026-11-11.md). Source bytes were not modified.

## Exact XSD/dependency boundary

| Common lane | Exact selected Enumerations XSD Git blob | XML-valid `Wheel...` and Other | Authority |
| --- | --- | --- | --- |
| V1.0 | `IBIS-IP_Enumerations_V1.0.xsd` / `a9bea5bc73003ed91ded8519db06c32c4067831d` | `WheelChair` (line 68), `Other` (line 71) | official_release |
| V2.0 | `IBIS-IP_Enumerations_V2.0.xsd` / `27e3c183b00381d959622d13c10543123af8eef6` | `WheelChair` (line 71), `Other` (line 74) | official_release |
| V2.1 | `IBIS-IP_Enumerations_V2.1.xsd` / `311464690ad60749ed8d326217787e4b8ed0b718` | `WheelChair` (line 72), `Other` (line 75) | official_release |
| V2.2 | `IBIS-IP_Enumerations_V2.2.xsd` / `2a23b512379b18e8f122ac1272cef8229fb86283` | `WheelChair` (line 74), `Other` (line 77) | official_release |
| V2.3 | `IBIS-IP_Enumerations_V2.2.xsd` / `2a23b512379b18e8f122ac1272cef8229fb86283` | `WheelChair` (line 74), `Other` (line 77) | official_release |
| V2.4 | `IBIS-IP_Enumerations_V2.4.xsd` / `2afed8cf23afa91db92b0f043cc5b4ad428b0f25` | `Wheelchair` (line 75), `Other` (line 77) | candidate_integration (nonaffected) |

- V1.0: release-tag `VDV-301-1.0`; V2.0: release-tag `VDV-301-2.0`; V2.1: release-tag `VDV-301-2.1`. For V2.2, preserve exact historical upstream provenance rather than inventing an unavailable `VDV-301-2.2` tag.
- V2.3: official Common XSD `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` explicitly includes **IBIS-IP_Enumerations_V2.2.xsd** blob `2a23b512379b18e8f122ac1272cef8229fb86283`; do not invent an Enumerations V2.3 or apply latest-wins.
- V2.4: official Common PDF publication, but the selected Enumerations XSD `2afed8cf23afa91db92b0f043cc5b4ad428b0f25` remains **candidate/integration**. An official PDF does not confer official XSD release status.

## Boundary, disproof and SDK consequence

- **Last verified nonaffected predecessor:** none published separately before the first audited Common V1.0 source; explicitly not invented.
- **First affected:** original Common V1.0 p25 §2.5 Table66. **Material adjacent official lanes:** V2.0, V2.1, V2.2, V2.3 all independently affected. **Last affected:** V2.3 p38 Table72. **First corrected published document:** V2.4 p41 Table71 (candidate XSD checked separately and nonaffected). There is no independently published alternate language-track version for the same lexical tokens in this corpus.
- **Strongest disproof attempt:** maybe V1.0-only historical anomaly or already corrected in V2.0; original V2.0–V2.3 body rows and exact original XSD declarations disprove that. V2.3's reused Enumerations V2.2 XSD is mandatory, not a change to accept `Wheelchair`. V2.4 corrects the mismatch and must **not** trigger a finding.
- Existing V1.0 `EV-117`/`EV-135` positive-negative probes and historical per-version `EV-118`, `EV-119`, `EV-120`, `EV-121` validate context of strict historical enum lexemes. No fresh per-version XML test was run by this locator block.
- **Classification:** confirmed cross-artifact mismatch with mixed probable source attribution. **SDK:** `error_with_advisory` only on existing strict XSD INVALID in V1.0–V2.3; `reviewed_not_implemented` (not a productive matcher). V2.4 excluded. No alias `Wheelchair` or `Others`, no automatic case fix, no XSD rewrite or upstream PR.
- The full DE/EN title, short, long and recommendation strings are in canonical semantic classification; runtime `profile_scope` is copied verbatim from its affected-only `version_scope`.

## Audit durability and closure

Update exactly one existing semantic finding and runtime review mapping, add one source-locator entry with six version/boundary coverage lanes and required `supporting_evidence`, add one visible-body verification and one version-boundary entry. Progress becomes **90 of 192** unique locator findings (90 original-body and 90 boundary verified, **102 open**) only after the complete GitHub schema-audit gate and a separate `terminal_clean` handoff; evidence/registry changes are first committed with recoverable `gate_pending`.

The earlier V1.0-only history and WIP remain preserved; no silent historical deletion. The pending and final GitHub run IDs and exact terminal commit are recorded in `00_START_HERE/CURRENT_STATE.json`, not fabricated in this evidence report.

