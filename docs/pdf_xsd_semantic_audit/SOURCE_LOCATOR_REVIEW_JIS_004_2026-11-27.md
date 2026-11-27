# Source locator review — JIS-004

Date: 2026-11-27. Existing confirmed_pdf_defect, selected_xsd, documentation_only, no_runtime_diagnostic unchanged.

## Original body and independent version context

JIS V1.0 RetrieveAllRoutesPerLine request table header and caption incorrectly name SetBlockNumberRequest in EN January 2014 p82 Table 86 and DE July 2016 p22 Table 38. Both operation overviews and both exact official XSD routes correctly distinguish required LineRef from BlockRef. Confirmed PDF-only label defect; no semantic, XSD or runtime change.

- EN January 2014 p82 §9.6.21.1 Table 86: header and caption incorrectly identify SetBlockNumberRequest, actual LineRef required (1:1) and retrieval prose correct. §9.6.21.2 uses shared ListAllRoutes response. Adjacent §9.6.22.1 Table 87 correctly uses SetBlockNumberRequest with required BlockRef; response uses common acknowledgement. EN p72 overview differentiates both, Table 49 caption p73 previously confirmed.
- DE July 2016 p22 §1.22.1 Table 38 duplicates the same wrong header/caption with LineRef, §1.22.2 shares response with ListAllRoutes. §1.23.1 Table 39 correctly identifies SetBlockNumberRequest with BlockRef. DE p11 Table 1 overview correctly differentiates requests and responses. Both exact pinned body render pairs visually checked.

## Exact XSD and active disproof

Historical official VDV-301-1.0 type-only JIS lines 234-244 and aggregate globals 63-65 / group 96-98 distinguish both operations; exact selected official VDV-301-2.0 JIS lines 293-306 and group 31-33 do likewise. Both require one IBIS-IP.NMTOKEN (LineRef versus BlockRef); operation names and response roles differ. The exact selected XSD and both PDF overviews agree. Shared generic Set acknowledgement (JIS-002) does not justify a shared request. Distinct contexts and fields disprove an intentional alias. A copy/paste label defect is strongly supported, not a renamed XML operation. No XSD mutation, no new runtime matcher; EV-152 contextual evidence, no dedicated new instance test because no executable conflict. Prior JIS-001 catalog boundary and JIS-003 later tag/branch checks reused, no fresh catalog query.

## Evidence

- EV-152 run 34113437268 SUCCESS previously rechecked; archived ZIP 10015273758 SHA256 338e3fb679a8375c98fba359a3478d4cf7ba0968f3e97c08209ce52c0d23dc65 independently rechecked. DE original p22 SHA256 edbf46ad4beca13d4f6099c1f5e3556707b041ea1bc5c0cae0ab2258f183857b size 270426 and p11 698a4c1099476acb970382172af6e8c7f3f0dcc42036babdd1b5d498ec31e741 size 207400 verified and visually inspected. JIS_V1.0 PDF SHA256 424181b4932e18b6ac059843fa3978fdcc07a9c6acb553f9fbe8b71ef583da73 size 772125, pin 34103529949. No new DE raw download.
- EN exact-source fallback run 45995480791 SUCCESS artifact 15196055861 ZIP SHA256 4328dc888410dbf6a5327874c6289434f702d0f35ac5939d317c1e12af5845df; VDV301-2_V1.0_EN source SHA256 e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7 size 2403598; p82 PNG 420a767ac2158a0fc1536f143a5ba5889ef2317d61daa2a02cdf1a9ce922b9a7 size 264785 verified against manifest and visually inspected.
- EN operation overview p72 re-used artifact 15026289022 from run 45625180374 ZIP SHA256 5d147d3241d23da58f1b29b37214ca4dc13201899b8093f56ec31b4e54a42559; p72 SHA256 78eeea46be7aca63ebaca8fc68835cc20766f5b6e532e9895cecb36b5b3ec213 size 200135 rechecked and visually inspected. Table 49 caption on p73 verified previously in JIS-002.
- Historical official VDV-301-1.0 JIS type-only blob 1ee4d7aeb15f3269c5335313be9e214bdb519d2e lines 234-244 and aggregate 41289eaed2674a169fdf77a10a2eff293c76d5c4 globals 63-65 and group 96-98; selected VDV-301-2.0 JIS 8c303db5a9c0548d66b90174d9c329d33092ad24 lines 31-33,293-306; actual selected branch blob identical. Prior JIS-003 upstream 2.1/2.2/2.3/master identical blob check retained; exact historical and selected declarations directly rechecked. Common/Enum exact V1.0 route unchanged.
- JIS-001 catalog boundary dated 2026-11-25 reused: no independently established separate DE 2014 aggregate, EN 2016 standalone, earlier/later standalone publication. No fresh catalog lookup; both language body tables directly checked. EV-152 historical context evidence reviewed; no new instance test because this is documentation-only, not a validation behavior difference.

## Closure

131/192 locator/body/boundary entries pending both CI gates. Next JIS-005 only after terminal closure and memory review.
