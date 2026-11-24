# DRTRAINSET21-001 — official V2.1+V2.2 wrong §9.1 pointer to examples: source locator and semantic boundary

Date: 2026-11-24. Frozen canonical finding ID `DRTRAINSET21-001`. **Confirmed PDF navigation defect** `documentation_only` / `no_runtime_effect` / `no_runtime_diagnostic`. **Confirmed affected scope V2.1 AND V2.2**, bilingual DE/EN in each. No standalone earlier TrainSet 301-2-14 release or later corrected standalone successor in [official VDV catalogue](https://www.vdv.de/ip-kom-oev.aspx) checked 2026-11-24. Explicit [legacy duplicate reconciliation](IDENTITY_RECONCILIATION_DRTRAINSET21_001_DRTRAINSET22_001_2026-11-24.md) for pre-existing DRTRAINSET22-001.

## Independent official-pinned sources

| Publication | Official original SHA256 / size | Visible error (§1 overview item5) | True visible body §9.1 | True visible body §10 |
|---|---|---|---|---|
| [TrainSet V2.1 05/2018](https://www.vdv.de/vdv-301-2-14-v2-1-sds-trainsetservices.pdfx) | `8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e` / 1708401B | German p9 `(Abschnitt 9.1)`; English p10 `(section 9.1)` | p42 `Re-initialisation of Service Communication when a Trainset changes the Driving Direction` | p45 `10 Examples`, `10.1 The master OBU requests the Status of Devices in a Slave Coach` |
| [TrainSet V2.2 08/2019](https://www.vdv.de/301-2-14-sdes-v2-2-trainsetservices.pdfx) | `c1946694a1809933a9a4a23adff1c551effdb0a2fbc6a7f7f68faec0b0c7bd6e` / 1744296B | Same German p9 and English p10 `9.1` pointer | p44 same original §9.1 re-initialisation | p47 same actual `10 Examples` cross-service scenario |

**Visual evidence—not TOC- or extract-only:** On 2026-11-24 the historical original GitHub EV148/EV149 ZIPs were re-downloaded, SHA-verified and original 180dpi p6 TOC/p9 DE/p10 EN images directly visually checked. V2.1 [EV148 run34029363792](https://github.com/MarcLeinenDE/VDV301/actions/runs/34029363792) Artifact 9988086415, ZIP SHA `c4e963de40e4684a9625644f9df2fc8f63ebedc8b2bba38736e83723d1c8dfea`, original DE p9 PNG SHA `1887dff1f50a690cf5e1c0f7d7fcce3a6cd842fe628b1dcec471d2bc51f430fd` and EN p10 PNG SHA `359e20a7722059c8c1b626ac0777be1ec298df1e50ed3fd851373c58f7ace616`. V2.2 [EV149 run34029942365](https://github.com/MarcLeinenDE/VDV301/actions/runs/34029942365) Artifact 9988263849, ZIP SHA `3bdc68e04a41da03d6d8b84bcc42cf846f58c49ef79a1266741bfa904f08e04e`, DE p9 PNG `136f14e5a5c653dd2a4d14c939fb8b7b8f704ddd50f6a2cdfc4fbf1c012ec7b3` and EN p10 PNG `b0f432f0f36a6548d6409432babe9e135d2c4dae63c04f71eb54b0430e5b4d3b`. These are same PDF sources as their archived official SHA pins.

**Stronger independent direct original target-body checks newly performed:**
- [VDV-2.1 exact-byte PDF render #45385075482](https://github.com/MarcLeinenDE/VDV301/actions/runs/45385075482) SUCCESS, **fresh official PDF download matched SHA256/size**, Artifact 14915538304, ZIP SHA `fadf50916447af0f62a950f382f0b02ad788cdf1726178f746adef3d0b007e73`: original real §9.1 p42 PNG SHA `c02cc4a26a337081fb8f50c13fe2f5166c96501a9294bef89207bc0d3919f45d`, real §10 p45 PNG SHA `f726e78d81ffce9641c7de330dca1b42f9976606be29c2615a32b9abcb80390d`; both file SHA verified locally, **actually visually inspected**.
- [VDV-2.2 exact-byte PDF render #45385413997](https://github.com/MarcLeinenDE/VDV301/actions/runs/45385413997) SUCCESS, fresh official PDF SHA256/size verified, Artifact 14916695301, ZIP SHA `10fa5e41b734228f81e9f1045d92338ed38b7c3a0a8a7639dc9e431339324b46`: original actual §9.1 p44 PNG SHA `8cbca3b18d79d27553e8bb48c85c94197f4eefba768b16ecf9ddd920db2ac976`, §10 p47 PNG SHA `00053bbdc56a0bcc8784a39d63f74b0a361bd5e7e547ed3abe03b2568e35b004`, both SHA verified and visibly inspected.
- Interactive web original PDF screenshot returned cache miss; existing source-pinned mandatory fallback was used, **not** a reason to leave body unverifiable. Original current PDF bytes were freshly fetched/checked **in GitHub CI**, not copied into Git repository.

## Active disproof

Strongest counter-hypothesis: section 9.1 has a use-case-like re-initialisation scenario and might intentionally be item5's example. **Rejected** by exact original body-context and item4 vs item5 separation: item4 already assigns re-initialisation to 7/9; item5 introduces general cross-service interaction examples, expressly grouped under real **10 Examples**, including p45/p47 master OBU requesting status of slave-coach devices and proxy services. Both languages and versions show same defect, no corrected later TrainSet edition established.

## Exact official XSD authority, non-XML effect

Six `IBIS-IP_TrainSet*Service_` official selected files independently fetched on 2026-11-24 and **verified byte-identical** between current `dev/schema-integration` and official `VDVde/VDV301@VDV-301-2.1` / `@VDV-301-2.2`:

| Version | InformationService Git blob | ManagementService Git blob | DataService Git blob |
|---|---|---|---|
| V2.1 | `897f373e31b76aa23d8bc206854b042524e4c102` | `add9d1cb37e5759ff7a77855b239108d38373206` | `c2cdb73fcae265a2e4e0349ac6072e3548e36d8b` |
| V2.2 | `7ab1f8f892bfcea2a8b8a055f07de92c143356f9` | `da9465d6683e3f7d54a546ab4a13739fb3c3e902` | `7a132894c281d613e16514a6fa1bcbffe713d066` |

The PDF navigation mistake **does not modify selected official XSD semantics, any XML instance PASS/FAIL, or SDK/runtime routing**. Retain `no_runtime_diagnostic` and `runtime_match=not_applicable`; no additional XML executable test or new alias. Historical EV109 V2.1 XSD tests remain independent existing context, not reinterpreted as tests of a document section pointer. No schema or SDK code changed.

## Identity and historical accounting

**Same logical error** persisted V2.1→V2.2. Original freeze had two version-labelled records `DRTRAINSET21-001` and `DRTRAINSET22-001`. As required by boundary policy, canonical DRTRAINSET21-001 scope now includes both editions. The pre-existing DRTRAINSET22-001 is retained, **explicitly marked legacy duplicate** in semantic notes with linked overlay. Historical EV evidence and frozen 192-ID inventory are not altered. The 192 denominator is frozen registry IDs (not necessarily 192 unrelated defect causes). A future DRTRAINSET22-001 locator checks its *archival V2.2 source slot* without treating same issue as new semantic defect.

## Closure requirements

After atomic substantive `gate_pending` commit with updated semantic registry SHA synchronized in locator and runtime mapping manifests and 118 mirrored counts, require full Schema Audit Validation and Handoff Integrity success. Then separate `terminal_clean` CURRENT_STATE + SDK manifest only and check **both final HEAD gates**. After successful closure: **118/192** completed frozen ID locators, **118/118** visible source body, **118/118** independent version boundaries, **74** remaining. Next frozen `DRTRAINSET21-002` NOT STARTED.
