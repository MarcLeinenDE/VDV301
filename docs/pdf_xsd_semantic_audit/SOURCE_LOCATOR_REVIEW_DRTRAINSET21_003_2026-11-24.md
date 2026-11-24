# DRTRAINSET21-003 — independent source/body and version boundary review

Date: 2026-11-24. Frozen identity unchanged. Scope extends from V2.1 to V2.1+V2.2.

## Original visible body and positive controls

- V2.1 p44 and V2.2 p46, actual §9.1.4 Possible implementation for non-OBU devices in the coach IP network: GetTrainSetCompositon (missing i). Both pages above §9.1.4 spell GetTrainSetCompositionResponse correctly twice; adjacent wrong service attribution is separately tracked as DRTRAINSET21-002.
- Both p24 under §4.5 Operations of the TrainSetInformationService, unnumbered operation table, show GetTrainSetComposition and the correctly named response. §4.5.1 heading and §4.5.1.1 Request correctly use GetTrainSetComposition and explicitly say that no structure is transmitted with the request. This disproves alternate-spelling and request-root interpretations; an operation name is not a global XML request root.
- Run 45404894020 artifact 14924434625 ZIP SHA256 28ba00df6dfaafde327182233499bcbcba3435e8113719cb7fd8871e697fa727 (347322 bytes); raw PDF SHA256 8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e (1708401 bytes), both manifest PNG hashes/sizes rechecked: p24 5dcc5a96b9b5305d20283e84f708893fa8e4e47b72658f2239cf30712bc782a8 (162227 bytes); p44 0829d150beb4992122fbe2fb63375c73205acb3c2f6425d0a6b7b6f68b5b69d4 (218768 bytes). Both visibly inspected.
- Run 45402521643 artifact 14922903550 ZIP SHA256 6e9fa8bbde483cb23c3548541c1a29ee4c012248980e547204d1610a6a37cf1f (1711202 bytes); raw PDF SHA256 c1946694a1809933a9a4a23adff1c551effdb0a2fbc6a7f7f68faec0b0c7bd6e (1744296 bytes), p24 PNG f819a26753e9184af5e3aef00b19eed7fb8f55de8ae4dcb940f8ded4c9c08a18 (143094 bytes), p46 PNG 2723da34cbce712dfabc1b3c234a3706607da79ae70476c809c6780f0bbe509b (218814 bytes), both hashes/sizes rechecked and pages visibly inspected.
- EV148 run 34029363792 artifact 9988086415 ZIP SHA256 c4e963de40e4684a9625644f9df2fc8f63ebedc8b2bba38736e83723d1c8dfea; original p44 180dpi PNG SHA256 ac44110da51217c7e2c9dbee4a30c8ad8eb49964722495a7a4f3c144570ed7fc; historical evidence preserved.

## Exact schemas and counter-context

V2.1
- IBIS-IP_TrainSetInformationService_V2.1.xsd blob 897f373e31b76aa23d8bc206854b042524e4c102 lines 36: Correct global response root; also member in operations group line 29; no misspelled root.
- IBIS-IP_TrainSetInformationService_V2.1.xsd blob 897f373e31b76aa23d8bc206854b042524e4c102 lines 37: Correct type spelling, no misspelled alias.
- IBIS-IP_common_V2.0.xsd blob 8608e3dcd665c197c34da7f6ec6af5a3758da164 lines 1: Whole file contains no Compositon token or alternate composition declaration.
- IBIS-IP_Enumerations_V2.0.xsd blob 27e3c183b00381d959622d13c10543123af8eef6 lines 1: Whole file contains no Compositon token or alternate composition declaration.

V2.2
- IBIS-IP_TrainSetInformationService_V2.2.xsd blob 7ab1f8f892bfcea2a8b8a055f07de92c143356f9 lines 36: Correct global response root; also member in operations group line 29; no misspelled root.
- IBIS-IP_TrainSetInformationService_V2.2.xsd blob 7ab1f8f892bfcea2a8b8a055f07de92c143356f9 lines 37: Correct type spelling, no misspelled alias.
- IBIS-IP_common_V2.2.xsd blob 468fee6d177e7185dbcd5d3f90cfb114e29e01ae lines 1: Whole file contains no Compositon token or alternate composition declaration.
- IBIS-IP_Enumerations_V2.2.xsd blob 2a23b512379b18e8f122ac1272cef8229fb86283 lines 1: Whole file contains no Compositon token or alternate composition declaration.

Both TSI XSDs contain the correctly spelled response as group member line 29, global element line 36 and type line 37. Exact dependency chain TSI V2.1 → Common V2.0 → Enumerations V2.0; TSI V2.2 → Common V2.2 → Enumerations V2.2. IBIS-IP_common_V2.0.xsd 8608e3dcd665c197c34da7f6ec6af5a3758da164; IBIS-IP_Enumerations_V2.0.xsd 27e3c183b00381d959622d13c10543123af8eef6; IBIS-IP_common_V2.2.xsd 468fee6d177e7185dbcd5d3f90cfb114e29e01ae; IBIS-IP_Enumerations_V2.2.xsd 2a23b512379b18e8f122ac1272cef8229fb86283. All four exact transitive dependency blobs identical to corresponding upstream release tag; entire file text contains no Compositon token. All six blobs match official upstream tags and work repository. No Compositon token in the six selected files. This is a documentation-only typo, not an executable defect; no additional XML test asserted or needed for this finding, no synthesized alias, request root or runtime rule. TSI-001 and TSM root/group findings are independent and unchanged.

## Scope and governance

Official VDV index https://www.vdv.de/ip-kom-oev.aspx checked 2026-11-24: V2.1 and V2.2 only, no earlier or later standalone edition established. Both bilingual publications contain one shared English §9.1.4 technical section, not separate DE/EN occurrences. First available affected V2.1, last available affected V2.2; no asserted corrected successor. One frozen logical ID, no additional record. Original body and boundary records verified; semantic classification confirmed_pdf_defect, documentation_only, no_runtime_effect, no_runtime_diagnostic. Historical evidence preserved. Both full gates required before terminal closure. Next DRTRAINSET22-001 is a legacy mirror of DRTRAINSET21-001, not a second logical error.
