<!-- NON_CANONICAL_CONTINUATION_DOCUMENT -->

# DRCOM10-006 — original enum source review (intermediate evidence, 2026-11-11)

**Status: WIP; not locator-complete; no new progress credit; follow `00_START_HERE/CURRENT_STATE.json` for the only current work state.**

Existing unique finding `DRCOM10-006` covers `DoorCountingObjectClassEnumeration` and presently has an **incomplete V1.0-only semantic/profile scope**. Independent original-PDF visual/source checks establish that the same mismatch also appears in V2.0, V2.1 and V2.3, with V2.2 evidence from the exact source's historical deep read and extracted official text pending a **new exact-byte visible recheck**. Do not create another finding ID. V2.4 visibly has the corrected lexemes. The selected XSD remains the only XML PASS/FAIL authority.

## Original body evidence, directly reopened in this work cycle

Each of the following **real rendered page images** was extracted from the cited historical GitHub Actions artifact, SHA-256 recalculated and compared to the recorded artifact page-hash manifest. The version-specific PDF SHA-256 and byte length in the manifest match the already pinned official source. The visibly printed section, caption and both lexemes were checked, not inferred from the TOC or OCR.

| Official PDF | Printed body locator | Visible PDF values | PDF SHA-256 / size | Verified PNG SHA-256 | Artifact provenance |
| --- | --- | --- | --- | --- | --- |
| Common V1.0 | p25, §2.5, **Table 66** | `Wheelchair`, `Others` | `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf` / 892769 | `9f04ac5752593244ed64c2dea63cc3b6cb178a16e42e30317e21661977759d6f` | run 33275626001, artifact 9721397514, `pages/page_025.png` |
| Common V2.0 | p33, §3.7, **Table 71** | `Wheelchair`, `Others` | `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088` / 946088 | `e46eca6795d0937297f467873606c5a0a04b68abfc41eb94878c41c8a373cced` | run 33279811315, artifact 9722644456, `pages/page_033.png` |
| Common V2.1 | p35, §3.7, **Table 71** | `Wheelchair`, `Others` | `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32` / 1274051 | `6b24840923db24358dcc608ddc375049b1674820caf856144ed754343f71aa1a` | run 33393002497, artifact 9758203545, `pages/page_035.png` |
| Common V2.3 | p38, §3.7, **Table 72** | `Wheelchair`, `Others` | `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b` / 793521 | `dbf014908cc54fcc23cbb4812eb1934c0631a90023608fc7d7e756f69debe4a5` | run 33656579631, artifact 9856965744, `pages/page-38.png` |
| Common V2.4 | p41, §3.7, **Table 71** | `Wheelchair`, `Other` | `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a` / 1689647 | `191d2b0b4421a8f3c923933291f334ff111f48f2e0a247399aef0ea91ba172db` | run 33658306978, artifact 9857652638, `pages/page-41.png` |

Original pinned source URLs:
- V1.0 `https://www.vdv.de/301-2-1-sds.pdfx`
- V2.0 `https://www.vdv.de/301-2-1-sds-v-2-0.pdfx`
- V2.1 `https://www.vdv.de/301-2-1-sds-v2-1-commonstructure-enums.pdfx`
- V2.2 `https://www.vdv.de/301-2-1-sdes-v2-2-commonstructure-enums.pdfx`
- V2.3 `https://www.vdv.de/301-2-1-sdes-v2-3-commonstructure-enums.pdfx`
- V2.4 `https://www.vdv.de/301-2-1-sde-v2-4-commonstructure-enums.pdfx`

**Open visual item — V2.2:** official source pin SHA-256 `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`, size 1411558 bytes. Source-only deep read `docs/pdf_xsd_semantic_audit/deep_read/COMMON_V2.2.md` and the official document text report `Wheelchair/Others` at printed p37 §3.7. The actual body table caption **has not been freshly inspected** in this cycle and no final printed table number is asserted here. The historical `common-v22-pinned-read` artifact 9840345496 was inaccessible (404); accessible newer prior render artifacts include only p23–30. New SHA-checked pinned fallback requested via `tools/pdf_render_request_v0.1.json` on work commit `3db0e652e66273efdd35c48fd217ba2c9ed7047b`; GitHub workflow run **43105456014** may still be queued. Retrieve its `vdv-pdf-render-fallback` ZIP and check its `render_manifest.json`, printed p37 image hash and actual body caption before claiming complete.

## Exact schema authority already independently checked

All exact selected `DoorCountingObjectClassEnumeration` simple types were re-read by Git blob and actual enumeration declaration, including the historical V2.3 dependency on **Enumerations V2.2**, not an invented V2.3 schema:

| Lane | Exact selected Enumerations XSD blob | Declared values and line hints | Authority |
| --- | --- | --- | --- |
| V1.0 | `a9bea5bc73003ed91ded8519db06c32c4067831d` | `WheelChair` line 68, `Other` line 71 | official_release |
| V2.0 | `27e3c183b00381d959622d13c10543123af8eef6` | `WheelChair` line 71, `Other` line 74 | official_release |
| V2.1 | `311464690ad60749ed8d326217787e4b8ed0b718` | `WheelChair` line 72, `Other` line 75 | official_release |
| V2.2; reused in V2.3 | `2a23b512379b18e8f122ac1272cef8229fb86283` | `WheelChair` line 74, `Other` line 77 | official_release (exact V2.3 dependency) |
| V2.4 | `2afed8cf23afa91db92b0f043cc5b4ad428b0f25` | `Wheelchair` line 75, `Other` line 77 | selected candidate_integration only |

No XSD was altered. Existing V1.0 EV-117/EV-135 and later deep-read validation runs (EV-118/EV-119/EV-120/EV-121) are historical executable evidence; **no new per-version enum probe was run here**. `WheelChair` is likely a historical XSD spelling problem and `Others` likely a PDF pluralization problem; this mixed source attribution remains evidence-based inference, not a waiver.

## Next terminal block actions

1. Download final GitHub render artifact for V2.2, verify exact source bytes/page PNG SHA and visually inspect body section/table/caption/values. If render fails, keep open; do not claim new credit.
2. Extend the **existing** semantic `DRCOM10-006` affected scope to independently verified Common/Enumerations V1.0, V2.0, V2.1, V2.2 and V2.3; treat V2.4 as explicitly verified **corrected/non-affected boundary**, not runtime activation.
3. Synchronize semantic classification, source locators (including required `supporting_evidence`), body verification, version boundary, runtime mapping, SDK manifest and `CURRENT_STATE.json` counts/diagnostics. Never double-count an earlier finding revalidation; this would be one new locator (90/192), not five.
4. Commit as recoverable `gate_pending`, run complete schema/audit gate, repair failures, commit separate `terminal_clean` close and verify final-HEAD schema + handoff gates. No automatic alias, XSD repair, runtime matcher or upstream PR.

