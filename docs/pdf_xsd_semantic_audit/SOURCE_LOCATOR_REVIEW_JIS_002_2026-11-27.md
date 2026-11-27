# Source locator review — JIS-002

Date: 2026-11-27. Existing finding, non_defect, selected_xsd, no_runtime_diagnostic unchanged.

## Original body and independent version context

JIS V1.0 seven Set requests intentionally share DataAcceptedResponseStructure in January 2014 EN aggregate and July 2016 DE standalone; no distinct earlier or later standalone release established in JIS-001 boundary audit. Same Common/Enum exact blobs and historical vs selected official packaging. No XSD defect or runtime diagnostic.

- DE 2016 p11 Table 1 (§1.2): SetBlockNumber, SetTripRef, SetDisplayContent, SetCurrentTripIndex, SetCurrentStopIndex, SetAdditionalAnnouncement and SetAdditionalTextMessage each use a local request type and the generic DataAcceptedResponseStructure. p22 §§1.23.2 and 1.24.2 explicitly delegate the response to VDV 301-2-1. The unrelated wrong request label in p22 Table 38 belongs to JIS-004 and is not adjudicated here.
- EN January 2014 aggregate p72–73 Table 49 (§9.6.1): all seven same request/response pairings; SetTripRef request at bottom p72 and response at top p73. Caption is visible on p73. Same model, not an inferred later correction. Boundary catalog evidence from JIS-001 dated 2026-11-25; no separately verified 2014 DE aggregate, 2016 EN standalone, earlier or later standalone.

## XSD authority and disproof

The selected later official JIS V1.0 has seven Set request entries (group lines 33–39, global elements/types 301–349) and no local Set response aliases. Common V1.0 lines 882–895 define DataAcceptedResponseStructure as choice between DataAcceptedResponseData and OperationErrorMessage; the former sequence has TimeStamp and DataAccepted required, ErrorCode and ErrorInformation optional. The shared type does not imply unconditional success. The exact historical aggregate VDV-301-1.0 contains the same seven JIS Set request roots/group and generic global DataAcceptedResponse at line 210. This is a distinction between the XML root and its type, not a missing JIS-local response. The historical Common/Enum blobs match selected dependencies. JIS-001 proved targeted structural packaging equivalence; existing dedup policy remains valid. No new aliases, SDK routing or diagnostics. EV-152 historical structural assertions rechecked; no fresh dedicated XML instance test for JIS-002 claimed.

## Evidence

- EV-152 run 34113437268 SUCCESS rechecked, artifact 10015273758 ZIP SHA256 338e3fb679a8375c98fba359a3478d4cf7ba0968f3e97c08209ce52c0d23dc65 independently rechecked. DE original p11 SHA256 698a4c1099476acb970382172af6e8c7f3f0dcc42036babdd1b5d498ec31e741 (207400 bytes), p22 edbf46ad4beca13d4f6099c1f5e3556707b041ea1bc5c0cae0ab2258f183857b (270426 bytes), match EV-152 evidence and actually visually inspected 2026-11-27. No new EV-152 run.
- JIS_V1.0 PDF SHA256 424181b4932e18b6ac059843fa3978fdcc07a9c6acb553f9fbe8b71ef583da73 size 772125; historical pin run 34103529949, artifact 10011459459, central pin registered in 3ee744d. No fresh raw PDF download.
- VDV301-2_V1.0_EN SHA256 e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7 size 2403598; exact-source renderer run 45625180374 artifact 15026289022 ZIP SHA256 5d147d3241d23da58f1b29b37214ca4dc13201899b8093f56ec31b4e54a42559 rechecked; all four manifest PNG sizes and hashes verified. EN p72 SHA256 78eeea46be7aca63ebaca8fc68835cc20766f5b6e532e9895cecb36b5b3ec213, p73 1701b40312c76df09212e679774700d54b688984a46f8c33323ed7a261551a9d, both actually visually read. SetTripRef row split across pages; Table 49 caption p73.
- Exact VDVde/VDV301 tag VDV-301-2.0 JIS 8c303db5a9c0548d66b90174d9c329d33092ad24 group lines 33-39 and globals/types 301-349, Common 194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c types lines 882-895, Enum a9bea5bc73003ed91ded8519db06c32c4067831d. Tag VDV-301-1.0 JIS type-only 1ee4d7aeb15f3269c5335313be9e214bdb519d2e and aggregate 41289eaed2674a169fdf77a10a2eff293c76d5c4 lines 65-71,98-104,210; same Common/Enum. Both upstream trees rechecked 2026-11-27; JIS local group/globals only seven Set request declarations, no Set response aliases; historical aggregate declares generic DataAcceptedResponse. Existing JIS-001 structural equivalence and SUPERBRANCH_V1_0_DEDUP_POLICY.md retained.
- JIS-001 boundary audit 2026-11-25 verified historical EN aggregate and DE standalone; VDV catalog checked then, no later standalone identified; no separate DE 2014 aggregate or EN 2016 standalone independently established. Rechecked actual JIS-002 response rows in each source, not extrapolated. No fresh catalog lookup in this pass.
- Canonical semantic entry non_defect/no_runtime_diagnostic and no entry in runtime mapping; historical EV-152 confirms shared response model by structural assertions (not a dedicated positive/negative JIS-002 XML test).

## Closure

129/192 locator/body/boundary entries pending both CI gates. Next JIS-003 only after terminal closure and memory review.
