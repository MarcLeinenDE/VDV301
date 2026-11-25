# Source locator review — JIS-001

Date: 2026-11-25. Existing finding; non_defect, selected_xsd, no_runtime_diagnostic unchanged. No XSD, semantic classification or runtime changes.

## Original body and version boundary

JIS V1.0 shared generic subscriptions intentional in earliest independently verified 2014 EN aggregate and 2016 DE standalone; no different standalone version or corrected successor verified. Distinct official packaging, same 44 payload complex types and 31 root mappings/group, same Common/Enum blobs. No XSD defect or runtime diagnostic.

- Standalone DE July 2016: p9 §1.2 generic Subscribe/Unsubscribe types for AllData and CurrentBlockRef; p11 Table 1 caption. p12 §§1.4/1.5 and p13 §§1.7/1.8 explicit delegation to VDV 301-2-1. 
- Historical EN January 2014 aggregate: p71 §9.6.1 same four operations and generic types; p73 Table 49 caption. p74 §§9.6.3/4/6/7 reference chapters 10.51/52 and 10.57/58 respectively. No inferred table number. No separate 2014 DE aggregate or 2016 EN standalone independently established; not treated as corrected/missing behavior. Official catalog lists only standalone V1.0.

## Historical XSD disproof and SDK routing

Exact old type-only JIS and aggregate versus later self-contained JIS: 44 named complexType declarations matched after removing XML comments and inter-tag whitespace; 31 global JIS element name/type mappings match; normalized group equal. Exact Common and Enumerations dependencies match by blob. This is a targeted structural equivalence comparison, not a proof of equivalence of the entire aggregate schema or fresh instance-validation result. Historical aggregate generic subscription roots at lines 204–208, not service-specific aliases. The explicit existing dedup policy already selects later official VDV-301-2.0 JIS blob, also present in V2.1/V2.2. Retain historical provenance; no new profile or runtime modification warranted for this finding. EV-152 historical success supports active disproof; no fresh EV-152 execution claimed. Do not synthesize JIS-specific subscription aliases or report a runtime defect.

## Evidence

- Historical WIP checkpoint docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_JIS_001_WIP_2026-11-25.md; preserve as historical evidence.
- EV-152 run 34113437268 SUCCESS; artifact 10015273758 ZIP sha256 338e3fb679a8375c98fba359a3478d4cf7ba0968f3e97c08209ce52c0d23dc65 independently verified. Visible printed p9 eb4274fd531510109c62ebb9d1c293ab8e440981edad130f517d3efec5cc655c, p11 698a4c1099476acb970382172af6e8c7f3f0dcc42036babdd1b5d498ec31e741, p12 a030e788fd63f9089778abda6ed4e9d3c466bdd2c389973d698e34698e0dd1e9, p13 a5bfe1f0fabb40acfdb4f4475f2cb8f4f273c94e80bdf7010a6085490d5c823a actually read; hashes match EV-152.
- JIS_V1.0 pin 424181b4932e18b6ac059843fa3978fdcc07a9c6acb553f9fbe8b71ef583da73, 772125 bytes, original pin run 34103529949 artifact 10011459459, ZIP ee5383e391c2c2e79b229a56094f0a77edc96836516dffa464fc710450647a6a; registered in 3ee744d from verified historical evidence, not a new raw-PDF fetch.
- VDV301-2_V1.0_EN pin e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7, 2403598 bytes; fresh exact pinned render run 45625180374 SUCCESS, artifact 15026289022 ZIP 5d147d3241d23da58f1b29b37214ca4dc13201899b8093f56ec31b4e54a42559. All 4 PNG size/hash checks pass; visually read p71 e39484197bacd5004c04fb3435dce0ddf2efc09d7b6dd6cd95743006ac1968a7, p73 1701b40312c76df09212e679774700d54b688984a46f8c33323ed7a261551a9d, p74 f91cbffd43e541bcd1f8ebe593731a84e12e0fd125919bbfa1da51d689c5b2ab. p72 verified but not needed for this claim.
- Exact upstream VDV-301-1.0 JIS 1ee4d7aeb15f3269c5335313be9e214bdb519d2e (type-only) + IBIS_IP_V1.0.xsd 41289eaed2674a169fdf77a10a2eff293c76d5c4 (global roots/group) vs VDV-301-2.0/2.1/2.2 JIS 8c303db5a9c0548d66b90174d9c329d33092ad24: normalized 44/44 complex types identical, 31/31 root-name/type pairs identical, group identical. Common 194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c and Enum a9bea5bc73003ed91ded8519db06c32c4067831d identical across tags. No fresh XML instance test, not a claim of whole aggregate equivalence.
- docs/pdf_xsd_semantic_audit/SUPERBRANCH_V1_0_DEDUP_POLICY.md explicitly selects later official self-contained JIS V1.0 packaging; strict archival reconstruction uses original tag. No SDK routing gap or payload constraint change established.
- Official VDV index https://www.vdv.de/ip-kom-oev.aspx accessed 2026-11-25 (cached crawl): only standalone JIS V1.0 listed. No independently established earlier standalone or later standalone version; EN 2014 aggregate is predecessor documentation, not additional standalone version. No independent DE 2014 aggregate or EN 2016 standalone verified.

## Closure

128/192 locator/body/boundary entries pending full CI. Next JIS-002 only after terminal gate and memory review.
