# DR3012GC24-004 — malformed service identifiers in official 301-2 examples and glossary (2026-10-12)

**Existing frozen finding identity preserved.** Independent original-publication boundary extends the former GC V2.4-only scope to an earliest affected independent English V1.0 (01/2014) and German V1.0 (07/2016), Base V2.0/V2.1, GC V2.2/V2.3/V2.4. No new finding created; no XSD mutations.

## Actual faulty tokens versus exact identifiers

| Visible official PDF literal | Correct service identifier | Surface and earliest verified |
|---|---|---|
| `PassengerCountigService` | `PassengerCountingService` | English V1.0 p122 §14 glossary; German V1.0 p78; persists in bilingual Base V2.0/V2.1 and GC V2.2–V2.4 glossaries |
| `DeviceManagmenService` | `DeviceManagementService` | GC V2.2 German §5.2 example p55 and English example p60; persists V2.3/V2.4 |
| `CustomumerInformationService` | `CustomerInformationService` | Same GC V2.2 service-search prose (de p55/en p60); persists V2.3/V2.4 |
| `DeviceManagmentServices` | `DeviceManagementService` | Diagram service-information label GC V2.2 de p55/en p60; persists V2.3/V2.4. The plural is a diagram label and **not proven to be a literal runtime ServiceNameEnumeration field** |

## Independent official original bodies and exact pin/PNG fingerprints

German original V1.0 (07/2016) and independent English V1.0 (01/2014) are **distinct publications** and must not be conflated, despite their shared V1.0 identifier. Original PDF page numbers below are printed visible footer numbers, not TOC/history extrapolations. Six official PDFs acquired from GitHub Actions **run33752224704 artifact9892036202**, each original exact SHA256/size verified against canonical pin registry. Original V1.0 EN acquired via mandatory fallback **run38262374552 artifact11753610657**, exact SHA/size verified before 160dpi rendering. Other pages rendered from exact original PDF bytes at 144dpi, visually compared in original page layout. No PDF bytes committed.

| Official pinned source | Exact SHA-256 / bytes | Target printed pages and observed text |
|---|---|---|
| [VDV301-2_V1.0_EN](https://www.vdv.de/301-2ses.pdfx) | `e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7` / 2403598 | p85: §9.8.1/Tables 95–97 correct PassengerCountingService; p122: §14 Terms, PassengerCountigService typo |
| [VDV301-2_V1.0_DE](https://www.vdv.de/301-2sds-v1-0.pdfx) | `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75` / 1790447 | p78: Glossar PassengerCountigService typo |
| [VDV301-2_BASE_V2.0](https://www.vdv.de/301-2-sds-v-2-0.pdfx) | `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37` / 2374295 | p107: German glossary PassengerCountigService typo; p108: English glossary PassengerCountigService typo |
| [VDV301-2_BASE_V2.1](https://www.vdv.de/301-2-sds-v2-1-basicservices.pdfx) | `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` / 2671005 | p121: German glossary PassengerCountigService typo; p122: English glossary PassengerCountigService typo |
| [VDV301-2_GC_V2.2](https://www.vdv.de/301-2-sdes-v2-2-common-conventions.pdfx) | `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051` / 1562305 | p55: German §5.2 example DeviceManagmenService, CustomumerInformationService, diagram DeviceManagmentServices; p60: English §5.2 example same three typos; p72: German §8 glossary PassengerCountigService; p74: English §8 glossary PassengerCountigService |
| [VDV301-2_GC_V2.3](https://www.vdv.de/301-2-sdes-v2-3-common-conventions.pdfx) | `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603` / 1057483 | p55: German §5.2 three example/diagram typos; p60: English §5.2 three example/diagram typos; p73: German §8 glossary PassengerCountigService; p75: English §8 glossary PassengerCountigService |
| [VDV301-2_GC_V2.4](https://www.vdv.de/301-2-sde-v2.4-common-conventions.pdfx) | `048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d` / 1767094 | p59: German §5.2 three example/diagram typos; p64: English §5.2 three example/diagram typos; p77: German §8 glossary PassengerCountigService; p79: English §8 glossary PassengerCountigService |

**Rendered page SHA256 manifest** (per original target page):

- `VDV301-2_V1.0_EN` p85: PNG SHA256 `95645c54194fb4252960f46f11a60caecdda70b2830578df8c964abe9df5913f` (160 dpi, run38262374552)
- `VDV301-2_V1.0_EN` p122: PNG SHA256 `1a2dc2fa0cb5050ddc5daac2d1791ab14e2abd494c8ba5f7369f660758cc267b` (160 dpi, run38262374552)
- `VDV301-2_V1.0_DE` p78: PNG SHA256 `8de30767d45dc422122473c1a3488a424bcbc8ff02ed98fdc238935bf97b5b6d` (144 dpi, local exact-pin render)
- `VDV301-2_BASE_V2.0` p107: PNG SHA256 `29133351a8dc6dcd02a4093a50d368131f264c7c4b155e42dd3d904f782e09fb` (144 dpi, local exact-pin render)
- `VDV301-2_BASE_V2.0` p108: PNG SHA256 `8363f19823567f8113bcd81465df4c045ce5739cd3f4eb8743a92c0c6a0eae5f` (144 dpi, local exact-pin render)
- `VDV301-2_BASE_V2.1` p121: PNG SHA256 `4498e6c7941a91b308acd439f0d29a513f5f2e4a662b8861de0170d50ae896ae` (144 dpi, local exact-pin render)
- `VDV301-2_BASE_V2.1` p122: PNG SHA256 `5d78064a96cfd8d638cae101a3a43362f69cefd8b4b4f1ea812a0e91c497d7f1` (144 dpi, local exact-pin render)
- `VDV301-2_GC_V2.2` p55: PNG SHA256 `7c88e9b52ae20ed45eaa61382aeb282a8c9598d212870bf1ec641b3c8788e23d` (144 dpi, local exact-pin render)
- `VDV301-2_GC_V2.2` p60: PNG SHA256 `d58b4555a1a126ea48f80c1731bb4706f4b9da83fd4304445c553d9ad79cdd35` (144 dpi, local exact-pin render)
- `VDV301-2_GC_V2.2` p72: PNG SHA256 `3bcf76b9e4bac9b9db7b1a2c1f8b73516837c22a39c4cd935a0fe5ef1a1a220d` (144 dpi, local exact-pin render)
- `VDV301-2_GC_V2.2` p74: PNG SHA256 `00442db2d1887718c8283aa4f52e29e59325b027abe440d42053669b871da02c` (144 dpi, local exact-pin render)
- `VDV301-2_GC_V2.3` p55: PNG SHA256 `f67daf6aa4fcc391d1773fc33885f665628420894f28c559f25a6c6c3f997952` (144 dpi, local exact-pin render)
- `VDV301-2_GC_V2.3` p60: PNG SHA256 `7f0fe7d6d0fc850667ea2022f6313915f1c3b0308fb3e1c59a4f2101cda3a48b` (144 dpi, local exact-pin render)
- `VDV301-2_GC_V2.3` p73: PNG SHA256 `0d56d5de00967f0f41c8f031aac1b50b3f6198de50a1dcc0eb2283f902d5ca2c` (144 dpi, local exact-pin render)
- `VDV301-2_GC_V2.3` p75: PNG SHA256 `902950ce9ff64dd4227fa12ab52cb3574cf8cf539c6e2e56070238b21b8d2967` (144 dpi, local exact-pin render)
- `VDV301-2_GC_V2.4` p59: PNG SHA256 `8bf404f8e9eba39cd60dd29f5e8bc303813d110ea94c5ba7af8561ac3640ab6f` (144 dpi, local exact-pin render)
- `VDV301-2_GC_V2.4` p64: PNG SHA256 `0847ae7d4825594a930514fe3971e45259d4ab260085bd89c6cc01b81c4db576` (144 dpi, local exact-pin render)
- `VDV301-2_GC_V2.4` p77: PNG SHA256 `cd727680f411e21909e4d5868feba33d577d73c3177cedf2505ae93d2cd21b62` (144 dpi, local exact-pin render)
- `VDV301-2_GC_V2.4` p79: PNG SHA256 `d124c075869710222a4b24fccbc06bf4deb8c6e44654dad813d2c58ce635dee5` (144 dpi, local exact-pin render)

## Exact XSD authority and disproof

| Selected source/provenance | ServiceNameEnumeration rule for this finding |
|---|---|
| **VDV-301-1.0 official**, `IBIS-IP_Enumerations_V1.0.xsd` Git blob `a9bea5bc73003ed91ded8519db06c32c4067831d` | `DeviceManagementService` and `CustomerInformationService` present, **neither** `PassengerCountigService` **nor even corrected** `PassengerCountingService` appears as enumeration value. The correctly named V1.0 PassengerCountingService is nevertheless described as a service in English §9.8.1 p85 and has a separate V1.0 service XSD. Do not claim replacement token would PASS V1.0 ServiceNameEnumeration. This structural observation is **not** silently promoted into an unrelated standalone finding. |
| **VDV-301-2.0 official**, `IBIS-IP_Enumerations_V2.0.xsd` Git blob `27e3c183b00381d959622d13c10543123af8eef6` | Contains corrected `PassengerCountingService`, `DeviceManagementService`, `CustomerInformationService`; all four PDF typo literals absent. |
| **VDV-301-2.1 official**, `IBIS-IP_Enumerations_V2.1.xsd` Git blob `311464690ad60749ed8d326217787e4b8ed0b718` | Same exact three corrected values present, all typo forms absent. |
| **VDV-301-2.2 official**, `IBIS-IP_Enumerations_V2.2.xsd` Git blob `2a23b512379b18e8f122ac1272cef8229fb86283` | Same exact corrected values present, all typo forms absent. |
| **VDV-301-2.3 official tag** | No fabricated Enumerations_V2.3.xsd. Independently fetched official tag `VDV-301-2.3` which retains **the exact same** `IBIS-IP_Enumerations_V2.2.xsd` blob `2a23b512379b18e8f122ac1272cef8229fb86283`. |
| **GC V2.4 official PDF** | Official public documentation, but no separately established official tagged V2.4 enumeration XSD; official V2.4 strict profile remains unsupported/fail closed. |
| **V2.4 candidate/integration**, `IBIS-IP_Enumerations_V2.4.xsd` Git blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25` (`VDVde/VDV301#31`) | Correct three tokens present, typo forms absent; candidate executable negative/positive evidence EV-134 (run33843888080) remains valid **only** in explicitly selected candidate lane. |

Disproof controls: the erroneous tokens are in actual body (not TOC/history) and persist byte-identically in text/diagram contexts through several independently published versions. The exact spelled canonical counterparts occur in nearby official text and the exact XSD declarations. A diagram label or a prose service-search description is *not itself* proof of malformed runtime XML. A provider FAIL occurs only when an actual examined value violates the **exact selected authority** (official released XSD, or explicitly selected candidate XSD); DNS-SD/runtime service-name behavior requires its separately applicable norm/protocol rules. No typo aliases or normalization; no blind replacement into V1.0 enum. No new runtime matcher created.

## Classification / SDK

Retain `confirmed_pdf_defect` with `pdf_can_mislead_implementation` and `code_generation_or_discovery_affected`. `sdk_behavior=unsupported_profile` refers **only** to the unavailable official V2.4 strict profile; historical exact official 1.0/2.0/2.1/2.2 and reused 2.2 on 2.3 follow their actual selected schema (and may separately fail malformed values), while candidate V2.4 is a non-official selectable validation profile. DE/EN diagnostic text adjusted. Independently verified original source locator/body and boundary count advances from 79 to **80 / 192**, remaining 112, subject to successful full gate. Next missing `DR3012GC24-005`.
