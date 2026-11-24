# DRTRAINSET22-001 — historical V2.2 mirror locator closure

Date: 2026-11-24. Canonical logical identity: DRTRAINSET21-001 (V2.1+V2.2). This is the historical frozen V2.2 provenance slot, not a second logical defect. See [identity reconciliation](IDENTITY_RECONCILIATION_DRTRAINSET21_001_DRTRAINSET22_001_2026-11-24.md) and [canonical review](SOURCE_LOCATOR_REVIEW_DRTRAINSET21_001_2026-11-24.md).

## Original V2.2 evidence rechecked

- German p9 §1 Ausgangslage und Übersicht item5 and English p10 §1 Initial Situation and Overview item5 point general service-interaction examples to 9.1. Item4 separately assigns re-initialisation to chapters 7 and 9.
- Actual p44 §9.1 Re-initialisation of Service Communication when a Trainset changes the Driving Direction includes a use case, but is specifically about re-initialisation. Actual p47 §10 Examples and §10.1 The master OBU requests the Status of Devices in a Slave Coach establish the dedicated general example chapter. Not inferred from TOC. Counter-hypothesis of intentional §9.1 pointer remains rejected.
- EV149 run 34029942365 artifact 9988263849: ZIP 1739681 bytes SHA256 3bdc68e04a41da03d6d8b84bcc42cf846f58c49ef79a1266741bfa904f08e04e; p9 228792 bytes SHA256 136f14e5a5c653dd2a4d14c939fb8b7b8f704ddd50f6a2cdfc4fbf1c012ec7b3 and p10 199829 bytes SHA256 b0f432f0f36a6548d6409432babe9e135d2c4dae63c04f71eb54b0430e5b4d3b re-downloaded, rehashed and visually read on 2026-11-24.
- Pinned renderer 45385413997 artifact 14916695301: ZIP 412103 bytes SHA256 10fa5e41b734228f81e9f1045d92338ed38b7c3a0a8a7639dc9e431339324b46, manifest official raw PDF SHA256 c1946694a1809933a9a4a23adff1c551effdb0a2fbc6a7f7f68faec0b0c7bd6e size 1744296; original p44 PNG 226707 bytes SHA256 8cbca3b18d79d27553e8bb48c85c94197f4eefba768b16ecf9ddd920db2ac976, p47 PNG 218769 bytes SHA256 00053bbdc56a0bcc8784a39d63f74b0a361bd5e7e547ed3abe03b2568e35b004 rehashed and visually read on 2026-11-24. Raw PDF pin checked in original renderer run, not freshly fetched in this mirror block.

## Historical scope and exact authority

The earlier canonical review independently verified both official editions and the publication catalogue (V2.1 first and V2.2 last available affected edition; both DE/EN; no earlier or corrected later standalone edition established). That same verified boundary is reused here, without claiming new V2.1 rendering or catalogue retrieval. The mirror's frozen V2.2 scope is preserved, with an explicit canonical link. Exact V2.2 service XSD blobs are the already verified canonical counter-context: IBIS-IP_TrainSetInformationService_V2.2.xsd 7ab1f8f892bfcea2a8b8a055f07de92c143356f9; IBIS-IP_TrainSetManagementService_V2.2.xsd da9465d6683e3f7d54a546ab4a13739fb3c3e902; IBIS-IP_TrainSetDataService_V2.2.xsd 7a132894c281d613e16514a6fa1bcbffe713d066. No XSD semantics are required to prove a PDF navigation defect; no new XML test, diagnostic or rule.

## Accounting and closure

One additional verified historical locator slot (120→121 of 192 frozen IDs), zero new logical defects. Semantic classification stays confirmed_pdf_defect/documentation_only/no_runtime_effect/no_runtime_diagnostic. Both original EV149 history and frozen inventory preserved. Canonical DRTRAINSET21-001 remains V2.1+V2.2; no duplicate SDK matcher. Updated mirror notes and DE/EN diagnostics now reference actual original body and canonical identity. Full gates and separate terminal_clean required. NEXT DRTRAINSET22-002.
