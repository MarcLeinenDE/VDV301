# DR3012GC24-005 — independently versioned services versus stale global V1.0 terminology

Date 2026-10-12. Existing finding identity retained. The first documented conflicting pair of assertions appears in **Basic Services V2.0** and persists in V2.1 and General Conventions V2.2, V2.3, V2.4. German V1.0 (07/2016) and the independent English V1.0 (01/2014) serve as historical controls, not the same contradiction.

## Original publication and printed body/page boundary

| Exact original publication | Original printed pages | Role and direct visible observation |
|---|---|---|
| English V1.0 (01/2014) | §3.6 p21, §4.5 p23 | Historical control: §3.6 explains the first specification 1.0; §4.5 says version 1.0 of IBIS-IP. No explicit denial of common version. |
| German V1.0 (07/2016) | §1.6 p19, §2.5 p22 | Historical last predecessor: §1.6 explains original version 1.0; §2.5 says Version 1.0 von IBIS-IP. No explicit denial of common version. |
| Basic Services V2.0 (02/2018) | §1.6 p19 DE/EN, §2.5 p25 DE/EN | **First affected:** each service independently versioned; no common IBIS-IP version, yet later still 'version 1.0 of IBIS-IP'. |
| Basic Services V2.1 (07/2018) | §1.6 p20 DE/EN, §2.5 p26 DE/EN | Both opposing phrasings persist. |
| General Conventions V2.2 (08/2019) | DE §1.5 p11 / §2.5 p19; EN §1.5 p15 / §2.5 p22 | Both statements present independently in DE and EN original body. |
| General Conventions V2.3 (02/2021) | DE §1.5 p11 / §2.5 p19; EN §1.5 p15 / §2.5 p22 | Wording persists in both languages. |
| General Conventions V2.4 (01/2023) | DE §1.5 p14 / §2.5 p22; EN §1.5 p18 / §2.5 p25 | Last checked affected edition; no confirmed later corrected successor. |

## Exact byte-pinned original source and actual visible-page SHA256

All seven official PDF sources match canonical `audit_registry/pdf_source_registry_v0.1.json` and `audit_registry/pdf_source_pins_v0.1.json`. Six original PDFs came from archived source run33752224704 artifact9892036202 and were compared to exact SHA256 and byte sizes before 160dpi local rendering. English V1.0 was rendered and pinned independently by fallback GitHub Actions **run38271427816 artifact11756578350** (original SHA256/size checked before output). Actual page content, not TOC/history, was visually inspected. The page number in each locator matches the printed footer on the original.

| Source | PDF SHA-256 / bytes | 160dpi original rendered pages and PNG SHA-256 |
|---|---|---|
| [VDV301-2_V1.0_EN](https://www.vdv.de/301-2ses.pdfx) | `e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7` / 2403598 | p21 `d524a49f288e265eb5b5fe5a25fa5ff30d16e3d3ec5397d8068851936b562995`; p23 `ceb0e04095e9576a40121435e29816c6229db9be8454193e96a66e072bf1c722` |
| [VDV301-2_V1.0_DE](https://www.vdv.de/301-2sds-v1-0.pdfx) | `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75` / 1790447 | p19 `8fa8b03d8a1d68fc5b253ac75dee616bc0666499df9acd4330800180751eaa05`; p22 `db8f9a8e77f5b044996b575b2ae3c5cdc44a34bb246ba54b92a28b8ce497863f` |
| [VDV301-2_BASE_V2.0](https://www.vdv.de/301-2-sds-v-2-0.pdfx) | `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37` / 2374295 | p19 `1517876dedb2696bd2077f344fd4e8401bda792c7b5c9290e0d5bd5a70d2463b`; p25 `d4e13d1542bd8874adc3c6347e3129ba9565a62f8bb282929e4e1563cd0df1e3` |
| [VDV301-2_BASE_V2.1](https://www.vdv.de/301-2-sds-v2-1-basicservices.pdfx) | `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` / 2671005 | p20 `98c207c772e700539fbc49d36dd412b96c8a15571b3fd1dde359aa8c14995534`; p26 `15fc91c1bd3c51c2056ff925e611f15ede31da6ac09c4f86a6294105031ebc87` |
| [VDV301-2_GC_V2.2](https://www.vdv.de/301-2-sdes-v2-2-common-conventions.pdfx) | `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051` / 1562305 | p11 `48787d27a8a59aad6260537cb1654a91377074b68b1bdf97937d3a79cc0a1a64`; p15 `ca6c1eb0c1634d57edc7e5c46ddc74803b7a763c8ab6f9aaa5c348e15777a763`; p19 `b42ff8d751c6a24dd9efa92f469494cc4f0481c316be0140ef060800457f6f90`; p22 `582ea7b15d72070a8a7f63f1a58ecc0ba6497e18ac3a84b2244d34339ece4ef1` |
| [VDV301-2_GC_V2.3](https://www.vdv.de/301-2-sdes-v2-3-common-conventions.pdfx) | `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603` / 1057483 | p11 `d0235422a730ff3f23682cf8924194cc86f4ef3ab53133837dedab6d01429213`; p15 `bff7f8710f059e22fb63849ce8a45a1e6182d32963c7a303bba93ceb75e697a6`; p19 `7c10543198f362fc71be83d83a3cdef93426917e650b993f56a87049c3aae741`; p22 `2cbebcc04f7c8dccf46d28e7fd8a6f9b470bd5ec56f14e8847900b7017bbe089` |
| [VDV301-2_GC_V2.4](https://www.vdv.de/301-2-sde-v2.4-common-conventions.pdfx) | `048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d` / 1767094 | p14 `d9db14cec0de16ee365c14b088f2cf0b2d303affd9212446805b9f3bf08e053c`; p18 `852193396df3b1c03193a66dd79a085fdbb465935866a33a579c31d79e248867`; p22 `aa8394cf12cf6d1ba4c127771ad72b5da4292956c236b82cac721aee419e2424`; p25 `f730712fbaac5f1c37692ef0982d71f3cb233305e3c4f53b915cac17deb02399` |

## Disproof and classification

The strongest alternative explanation is that 'Version 1.0 of IBIS-IP' is shorthand for the historical full-document publication rather than an executable version shared by every service. **This interpretation is plausible in both original V1.0 publications**, which introduce the then-current specification as V1.0. It remains contextually plausible later but the unqualified phrase in §2.5 of V2.0–V2.4 stands alongside an explicit no-common-version statement in §1.6 / §1.5; that outdated wording can mislead an implementer about global version routing. Record as confirmed PDF semantic/editorial ambiguity, not a contradictory XSD rule.

**Normative result:** no executable XSD rule or provider PASS/FAIL is created by this documentary phrase. The exact selected published official XSD or explicitly selected candidate/integration XSD remains authoritative for XML. No assumed global/umbrella IBIS-IP version. Maintain service-specific version matching and separately pinned profile release/provenance, not latest-wins or silent aliases. `sdk_behavior=info`; `runtime_match.state=not_applicable`, and no new matcher/XSD mutation.

Historical scope expands the single frozen finding from GC V2.4 to **Basic Services V2.0/V2.1 + General Conventions V2.2/V2.3/V2.4**. V1.0 EN and DE are unaffected publication controls for the paired contradiction, even though the stand-alone phrase appears there. No new finding ID. Detailed bilingual diagnostic stored in semantic register.

Source locator/body and historical version-boundary completeness advance **80 → 81 of 192**; 111 remain, subject to complete schema/handoff gates and a separate terminal-closure commit.
