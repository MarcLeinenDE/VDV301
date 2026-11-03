# DR3012V21-001 – wrong service part identifiers in historical 301-2 source (2026-11-03)

**Already-existing frozen finding ID retained.** Previous V2.1-only scope was disproven by the actual original body of six other publications. This is a confirmed PDF service-document cross-reference error, **not** a schema/payload validity failure. No new finding ID, schema mutation or runtime matcher.

## Exact byte-pinned original sources and scope

| Official original edition | Source ID | PDF SHA256 / bytes | Actual visible section/page |
|---|---|---|---|
| 01/2014, independent English V1.0 (unaffected) | `VDV301-2_V1.0_EN` | `e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7` / 2403598 | p39 §7.1.1 |
| 07/2016, German V1.0 (first affected) | `VDV301-2_V1.0_DE` | `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75` / 1790447 | p39 §5.1.1 / p43–44 §5.2 / p47 §5.3 |
| 02/2018, bilingual Basic Services V2.0 | `VDV301-2_BASE_V2.0` | `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37` / 2374295 | p58–59 §5.1.1 / p68–69 §5.2.1.1 / p74–75 §5.3 |
| 07/2018, bilingual Basic Services V2.1 | `VDV301-2_BASE_V2.1` | `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` / 2671005 | p59–60 §5.1.1 / p69–70 §5.2.1.1 / p75–76 §5.3 |
| 08/2019, bilingual General Conventions V2.2 | `VDV301-2_GC_V2.2` | `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051` / 1562305 | p55 DE §5.2.1, p60 EN §5.2.1 |
| 02/2021, bilingual General Conventions V2.3 | `VDV301-2_GC_V2.3` | `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603` / 1057483 | p55 DE §5.2.1, p60 EN §5.2.1 |
| 01/2023, bilingual General Conventions V2.4 | `VDV301-2_GC_V2.4` | `048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d` / 1767094 | p59 DE §5.2.1, p64 EN §5.2.1 |

- **Independent English V1.0 01/2014**: original §7.1.1 p39 cites **chapter 9.1** for DeviceManagementService and **chapter 9.9** for SystemDocumentationService. It does **not** assign the incorrect external document numbers. Verified through fresh exact-byte GitHub PDF fallback **run [41617239025](https://github.com/MarcLeinenDE/VDV301/actions/runs/41617239025), artifact 13221179508**; source SHA and size checked before 160 dpi original-page render.
- **German V1.0 07/2016 (first affected)**: original §5.1.1 printed p39 says DeviceManagementService **VDV 301-2-2**, SystemDocumentationService **VDV 301-2-4**. Additional true body occurrences p43/44/47. The independent original does not match the 2014 English editorial track.
- **Basic Services V2.0 and V2.1**: two language tracks in the same bilingual originals repeat both part-number mistakes in system configuration, startup and example (§§5.1.1/5.2.1.1/5.3). Original V2.1 pages 59/60/69/70/75/76 were previously captured by the GitHub EV-131 **run33781385699 artifact9903719333**. V2.0 English p59 has an additional broken word-processor cross-reference suffix; this is not confused with the part-number mismatch.
- **General Conventions V2.2 / V2.3 / V2.4**: German and English §5.2.1 keep citing **VDV 301-2-2** for DMS. The SystemDocumentationService 301-2-4 citation was removed with the separated Basic section; there is **no demonstrated correction** of that old statement in the GC editions. No later corrected publication established.

Other six original PDFs were acquired by GitHub Actions **run33752224704 artifact9892036202**, reverified against exact SHA256 and byte sizes and locally rendered at 160 dpi with the repository's PyMuPDF pinned-byte method (live screenshot provider cache miss did not prevent review). PDF bytes and PNG originals are not committed to git. The numeric page identifiers in this report refer to the actual printed footer of the original body, not a TOC/version-history guess.

### Independent original-page PNG SHA256

- `VDV301-2_V1.0_EN`: p39 `2ca5eb9ba16dad71eebb81051997b7686e89edb1350df1ab3e0d94574485129a`
- `VDV301-2_V1.0_DE`: p39 `024d24a9cb302330f66b66f5502ad50f02ab4cbb04e59b8bad3e8efffe27f8db`; p43 `8cdef0a5b683c35c1476b566b9c81af2fbe44603f6287c8756756af873d02610`; p44 `cb70cf7319c4f5ea5a90bdc88fe657174d7df9354e49643b7af0c65615d53bbe`; p47 `2201de8d85d81a16c5c4308c3aa348de90863cbc0f156602a084e16bd76515b6`
- `VDV301-2_BASE_V2.0`: p58 `1d656c01ff725ac17ff15d6db2d86ab7642151293ce28f95962cf94dd2420474`; p59 `0b89a8316effb1aaa491397e2165faca627bdd169e554d0215ea5add0e2f40ca`; p68 `328bded62b30351aae0bd0fea8a4ef2a66591eb89de0ec38f55ad82a5ac0a65d`; p69 `e6ca40c18ceb1da2f804ff3a9837465c1bb075013d47b4046e364c1fef66be2f`; p74 `704c0ccc3f3540e4b786be1ebd467d3b8287be1e90f95b7a245d942af9d64e76`; p75 `d4b647328b25a8c51327d5f2501f6e07e6d3f089ec8ff6be334bef330d38adff`
- `VDV301-2_BASE_V2.1`: p59 `dbff96634b2c621be91b7dea09afebbdf2e4c043c24ba87533158b9bf4c0d2c4`; p60 `db309cdda89ca2496e24bfa2ec048946aa14e111678e998d08742987112ff361`; p69 `8dc269da00538150a56274e410e4e171591d48dd786180f12fd60a3fa8e28202`; p70 `105121751ae04247b9712b4c8b25bbfbb553ae0efaaf8cf377172a069355c2fd`; p75 `50199d9d62bb3f946c649ec8ebcaeb90e837f29002681dbfa89c18db21d81f02`; p76 `6656982f53106b491c6a40d0a63859cdd83ff22c600d08284b60ec725bd158f6`
- `VDV301-2_GC_V2.2`: p55 `152084cc51167e28fc0bd9fdfd1fb89f27200db2834814727455a5da27683b58`; p60 `63b8b513c4d0196c1650d200e477d70d665c489b675680ac3282a85682f53305`
- `VDV301-2_GC_V2.3`: p55 `d3c52ec72d5141ccc862afb3f0c2740f0814daf7942072e37fd66bccdd0e0cbc`; p60 `79390d478456397dc93c289b9780930505020c16123e01f88f6e2ae6c0f101a2`
- `VDV301-2_GC_V2.4`: p59 `9c916aa73320fa3004f8da0fc7a5bd4447050c068c06fedc40fd3a99358319ae`; p64 `f30535f99f009cc8ca13093b6675faeb432a44a01f4a6b816a3be6c9cd3daa53`

## Official part-number counterevidence and disproof

- The official individual **VDV 301-2-2 BeaconLocationService V1.0** and **VDV 301-2-4 DistanceLocationService V1.0** documents are themselves dated 07/2016; the official [VDV-Mitteilung 3002, 10/2016, §3.4 and §3.6 printed p9](https://www.vdv.de/3002-mds.pdfx) independently documents both part mappings. The official [VDV 301 publications catalog](https://www.vdv.de/ip-kom-oev.aspx) identifies dedicated DMS as **VDV 301-2-0**, not 301-2-2.
- Possible disproof “the erroneous numbers were the valid contemporaneous 2016 numbering” fails against those dedicated July 2016 publications and the independent October 2016 official overview.
- Possible disproof “the original English V1.0 has the same text” fails against the separately published English 2014 page 39. Translation date and edition source identity matter.
- The dedicated service schema is not selected by the incorrect prose numbers. The official tag `VDV-301-2.0` contains DMS V2.0 blob `74189e0da65563eeb084ec2f3c400e9668d1ee1a` and SystemDocumentation V2.0 blob `ab959dddbfa2b8ca420af1b079501f94cff38051`; `VDV-301-2.1` contains DMS V2.1 `191b43e01cdaba14b247725689a913c244a67eed`, SystemDocumentation V2.0 identical blob and SystemManagement V1.0 blob `2d32630a0f1981e980e6a466e3f6a69136410f24`.
- Official `VDV-301-2.2` and `VDV-301-2.3` both contain DMS V2.2 XSD blob `c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d`; neither authorizes a wrong document number. For GC V2.4 only the official publication is asserted; an official DMS V2.4 release-tag XSD is **not established**.

## Classification and SDK consequences

`confirmed_pdf_defect`, `version_routing_issue`, `normative_authority=contextual_only`, `sdk_behavior=warning`, `runtime_match=not_applicable`. Documentation/provenance only: the **exact selected XSD** continues to determine XML PASS/FAIL even when a historical XSD or PDF has a typo. There is no new executable data constraint, compatibility alias, forced operation or provider failure from this finding. Existing EV-131 remains valid for the V2.1 lane, which is now only one of six affected historical publication editions.

This finding advances complete original-source locators, visible-body checks and independent version boundaries **81 → 82 of 192** with **110 remaining**, subject to full schema and final handoff gates. Next semantic-order finding: `DRARA24-001`.
