# SOURCE LOCATOR REVIEW — DRCOM10-005 — 2026-11-11

Status: **six original-body pages and six exact selected XSD profiles independently verified; CI and terminal closure tracked exclusively in `00_START_HERE/CURRENT_STATE.json`.**

## Identity and falsification target

Unique existing finding **DRCOM10-005**, extending scope from V1.0 to all six published Common versions V1.0–V2.4 **without duplicating** historical `FR-COM21-OBS-012`, `FR-COM23-010` or their V2.x counterparts. The PDF `ShortTripStopList` top-level container is correctly named. The repeated **inner child** in each PDF is also labelled `ShortTripStopList` 1:*, while each exact selected XSD defines `ShortTripStopListStructure/xs:sequence/xs:element[@name='ShortTripStop']` of `ShortTripStopStructure`, implicit minimum 1 and explicit `maxOccurs=unbounded`. Schema-strict XML with the wrong inner PDF-derived child is INVALID; PDF discrepancy may explain but may never waive/repair it.

**V1.0-specific type-reference facet:** printed Table 46 displays `+StopPointTariffInformation` as the row's type/reference (§1.49), while the official Common V1.0 XSD uses `ShortTripStopStructure`. Both types expose the same required `JourneyStopInformation` followed by `FareZoneInformation` with exactly the same nested types. This difference in **type identity** does not show a distinct XML instance-shape difference. For V2.0–V2.4 the original PDF's type reference is already `+ShortTripStop`; do not carry the V1.0 secondary facet forward.

## Exact pinned original PDF body evidence and selected schema

All six image contents were reopened from GitHub's `tools/render_vdv_pdf_pages.py` fallback artifacts used in earlier audited findings, not extracted text alone. The original render manifest for **each** records official source URL/SHA256/byte size and a page-specific PNG SHA256, and the extracted PNG hash/byte length was recalculated against it. Each actual visible body image including section, full table caption, inner child and nearby structure was visually inspected. For V2.1 and V2.3, reusable `DRCOM10-003` artifacts supplied the previously missing p28/p30 pages, so the queued new render requests 43097923313 and 43097965762 are **not** reported as completed.

| Common PDF | Original PDF sha256 | Byte size | Printed actual body locator | Original child name/type / cardinality | Image SHA256 | Render run / artifact |
|---|---|---:|---|---|---|---|
| V1.0 | `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf` | 892769 | p18, §1.46, **Table 46 — Description of ShortTripStopList** | `ShortTripStopList` / `StopPointTariffInformation`, **1:\*** | `1072f924d50e9797e9528cbe07732809e6bd856d51b5d7a7d074d67a7d30e848` | [43029589455](https://github.com/MarcLeinenDE/VDV301/actions/runs/43029589455) / `13860986360` |
| V2.0 | `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088` | 946088 | p26, §2.48, **Table 48 — Description of ShortTripStopList** | `ShortTripStopList` / `ShortTripStop`, **1:\*** | `1e2825a759ee9374d7d3957a991231a004139a22913ed2f9076f81556115cca1` | [43029612445](https://github.com/MarcLeinenDE/VDV301/actions/runs/43029612445) / `13860711734` |
| V2.1 | `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32` | 1274051 | p28, §2.48, **Table 48 — Description of ShortTripStopList** | `ShortTripStopList` / `ShortTripStop`, **1:\*** | `35196477a114a3364371b8d5daff78799eb1316531d04295804cadbe9551e321` | [41649658472](https://github.com/MarcLeinenDE/VDV301/actions/runs/41649658472) / `13236253276` |
| V2.2 | `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203` | 1411558 | p29, §2.49, **Table 49 — Description of ShortTripStopList** | `ShortTripStopList` / `ShortTripStop`, **1:\*** | `248cfab843bb21903c9a462582f9262b150436fb6158c3c50746b15d486e9766` | [43029726595](https://github.com/MarcLeinenDE/VDV301/actions/runs/43029726595) / `13860087462` |
| V2.3 | `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b` | 793521 | p30, §2.49, **Table 49 — Description of ShortTripStopList** | `ShortTripStopList` / `ShortTripStop`, **1:\*** | `6ec4140ae6d492af3e4cd05598613efb55ba228ad72977ea9fd4adf6b69c0429` | [41649819541](https://github.com/MarcLeinenDE/VDV301/actions/runs/41649819541) / `13235912787` |
| V2.4 | `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a` | 1689647 | p32, §2.48, **Table 48 — Description of ShortTripStopList** | `ShortTripStopList` / `ShortTripStop`, **1:\*** | `b5906fb9c08b8c7cc8a249f4165974f8be64ba7d2be3ce1c6a398f1f180d03f0` | [43029777221](https://github.com/MarcLeinenDE/VDV301/actions/runs/43029777221) / `13860357046` |

Original official URLs (independently SHA/size pinned via `audit_registry/pdf_source_registry_v0.1.json` and `audit_registry/pdf_source_pins_v0.1.json`):
- Common V1.0: https://www.vdv.de/301-2-1-sds.pdfx
- Common V2.0: https://www.vdv.de/301-2-1-sds-v-2-0.pdfx
- Common V2.1: https://www.vdv.de/301-2-1-sds-v2-1-commonstructure-enums.pdfx
- Common V2.2: https://www.vdv.de/301-2-1-sdes-v2-2-commonstructure-enums.pdfx
- Common V2.3: https://www.vdv.de/301-2-1-sdes-v2-3-commonstructure-enums.pdfx
- Common V2.4: https://www.vdv.de/301-2-1-sde-v2-4-commonstructure-enums.pdfx

Every corresponding XSD declaration is `<xs:element name="ShortTripStop" type="ShortTripStopStructure" maxOccurs="unbounded"/>` inside `ShortTripStopListStructure`.

| Profile | Git blob for exact Common XSD | Type/child, two structure definitions (line hints) | Enumerations exact dependency | Authority |
|---|---|---|---|---|
| V1.0 | `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c` | `509/511; 514–518; 592–596` | Enumerations V1.0 | official_release; exact upstream tag VDV-301-1.0 |
| V2.0 | `8608e3dcd665c197c34da7f6ec6af5a3758da164` | `515/517; 520–524; 598–602` | Enumerations V2.0 | official_release; exact upstream tag VDV-301-2.0 |
| V2.1 | `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e` | `514/516; 519–523; 597–601` | Enumerations V2.1 | official_release; exact upstream tag VDV-301-2.1 |
| V2.2 | `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` | `523/525; 528–532; 606–610` | Enumerations V2.2 | official_release; exact upstream tag VDV-301-2.2 |
| V2.3 | `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` | `573/575; 578–582; 662–666` | Enumerations V2.2 | official_release; exact upstream tag VDV-301-2.3 |
| V2.4 | `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` | `588/590; 593–597; 704–708` | Enumerations V2.4 | candidate_integration (explicit only) |

The exact upstream `VDVde/VDV301` release files for `VDV-301-1.0` through `VDV-301-2.3` were independently re-fetched and their Git blob SHAs matched the listed values. V2.4's official PDF publication does **not** promote its locally selected Candidate/Integration XSD to an official released XSD. Upstream PR #31 remained open and unmerged on 2026-11-11.

## Independent scope and alternatives

- **First checked affected:** published Common V1.0 (§1.46 Table46, p18). No earlier independently verified Common 301-2-1 publication exists in the tracked corpus; document's internal V1.1 history is not a separate released XSD.
- **All adjacent versions:** V2.0 §2.48 p26; V2.1 §2.48 p28; V2.2 §2.49 p29; V2.3 §2.49 p30; V2.4 §2.48 p32. Every published original visible body table repeats the *outer* name for the inner child; all six selected XSDs consistently use `ShortTripStop`.
- **Last checked affected:** official PDF V2.4; selected XSD Candidate/Integration. No independently verified corrected subsequent Common publication/released XSD in scope.
- **Language track:** original publications mix German contextual wording and English structure member labels; no second distinct independently published German/English Common source is inferred for the same versions. Each original publication is checked separately; no inferred cross-language fix.
- **Notation/false-positive check:** 1:* row is an ordinary repeated list child, not `-1:1` choice notation; the outer table's own name and inner child are distinct XML roles. Neighboring ShortTripStop structure page explicitly lists JourneyStopInformation and FareZoneInformation as 1:1.
- **Type alternative check:** V1.0's differently named `StopPointTariffInformationStructure` and `ShortTripStopStructure` have the same two-member required sequence; there is no separate runnable failing instance solely from the type-name label. Later PDFs correctly type `ShortTripStop`.
- **Executable limitation:** preserved V1.0 `EV-117` / `EV-135` positive/negative instances demonstrate exact XSD child-name boundary. The present scope expansion compares five other exact XSD declarations and original PDFs; **no fresh per-version XML instance test** is claimed.

## Classification and SDK consequence

Confirmed `primary_surface=cross_artifact`, `primary_issue_kind=structure_mismatch (specific facet: child_identifier_mismatch)`, `defect_assessment=cross_artifact_mismatch`; ancillary V1.0-only wrong referenced type/model name with **equivalent XML instance shape**. Attribution to the publisher's PDF versus XSD as the one *intended* defect is unproven, so the prior unqualified `confirmed_pdf_defect` is made conservative. This is still a material code-generation/documentation collision.

SDK `error_with_advisory` on existing strict XSD `INVALID`, `reviewed_not_implemented`. Normative XML result stays selected-XSD strict for released V1.0–V2.3 or separately chosen candidate V2.4; no alias, no automatic rewrite, no new runtime matcher or XSD mutation. Full bilingual diagnostics live in semantic classification registry and must remain synchronized with runtime selected profile and this exact scope.

## Audit closure / continuation

- Canonical machines: semantic registry, source locator registry, PDF-body verification registry, boundary verification registry, SDK runtime-mapping registry and SDK manifest, all one unique `DRCOM10-005`.
- This substantive evidence and registry update stays crash-safe as `gate_pending` until full schema-audit-validation is successful on its exact HEAD.
- A separate terminal-clean commit may then update **only** `CURRENT_STATE.json` and `sdk_manifest/manifest_v0.1.json`, with final-head audit/handoff workflows verified. The next unique finding will be `DRCOM10-006`.
- Previous `SOURCE_LOCATOR_REVIEW_DRCOM10_005_WIP_2026-11-11.md` is historical intermediate evidence. Its two missing visual images were recovered and checked in this completed source analysis; queued GitHub new-render actions are not represented as successful runs.
