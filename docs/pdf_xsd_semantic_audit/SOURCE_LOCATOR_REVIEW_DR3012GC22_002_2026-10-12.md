# DR3012GC22-002 — German DNS-SD SRV/TXT duplicate 3.3.1 across GC V2.2–V2.4 (2026-10-12)

**Existing frozen semantic identity:** DR3012GC22-002. Revalidated and scope-corrected; never create new IDs for the same regression/persistence.

## Version boundary — exact official bytes and visible body

| Publication | SHA-256 exact pinned original | Visible German body | Visible English body | Assessment |
| --- | --- | --- | --- | --- |
| VDV 301-2 Basic Services **V2.1**, last adjacent predecessor | `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`, 2,671,005 bytes | printed p33 **§3.3 / §3.3.1 Nutzung des SRV-Records**, p36 **§3.3.2 Nutzung des TXT-Records** | Not needed to establish German clean predecessor | **Not affected**; source is integrated Basic Services, not a dedicated GC V2.1 |
| GC **V2.2** | `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051`, 1,562,305 bytes | p25 **§3.3 / §3.3.1 SRV**, p27 **§3.3.1 TXT**; DNS-SD paragraph also references TXT as §3.3.1 | p31 **§3.3.1 SRV**, p33 **§3.3.2 TXT** | **First affected dedicated GC edition** |
| GC **V2.3** | `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603`, 1,057,483 bytes | p25 **§3.3 / §3.3.1 SRV**, p27 **§3.3.1 TXT** | p31 **§3.3.1 SRV**, p33 **§3.3.2 TXT** | **Still affected, not corrected** |
| GC **V2.4** | `048f805fe3ddc894556899a94e36ec1b8cdc5a88fac5ad87235e4d`, 1,767,094 bytes | p28 **§3.3 / §3.3.1 SRV**, p30 **§3.3.1 TXT** | p35 **§3.3.1 SRV**, p37 **§3.3.2 TXT** | **Still affected, latest registered official GC publication** |

All headings and visible DNS-SD introductory cross-references above were evaluated as document-body locators, independent of TOC/version-history guesses. Source URLs and exact SHA-256 / size are in `audit_registry/pdf_source_registry_v0.1.json` and `audit_registry/pdf_source_pins_v0.1.json`.

## Render provenance and audit evidence

- [Last nonaffected Base V2.1](https://github.com/MarcLeinenDE/VDV301/actions/runs/38225286619), original SHA256 685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a, artifact 11735936030, p33 9b4d9706702059c27abf9017546fb71ec130cbb96f16a2eec21ff06ded8c63a2 and p36 aa905a30a48f9a1ca70af4bfc9ec53713cfaec4469623fdb68fb554880fc5f64
- [V2.2 EV-132](https://github.com/MarcLeinenDE/VDV301/actions/runs/33782124756), original SHA256 96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051, artifact 9903986586, printed p25/27/31/33 rendered and manually rechecked, p27 120c46814cf8c1c3d91160e2fb43f59dc5a4e34552b6e4848b68f10fa8a31091
- [V2.3 fresh original](https://github.com/MarcLeinenDE/VDV301/actions/runs/38224916667), original SHA256 4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603, artifact 11735744597, printed p25 0bd2e2b6fbf574f388fab30903459dbb90125fe29143e4d8842da5c886a23b91; p27 cb49ed9796eadd3c0428db878f5d83e9eba39c4b8d8e49b0d9bbfede363907f9; p31 5c7b101b1416e343a3646930d9086b8e8db8b78b732b3c6aeb6731e12758f489; p33 b8a2f7c03e60f451701bafef299785f490124bb0141069e8cc000fbdbd0a6819
- [V2.4 fresh original](https://github.com/MarcLeinenDE/VDV301/actions/runs/38225082730), original SHA256 048f805fe3ddc894556899a94e36ec1b8cdc5a88fac5ad87235e4d, artifact 11736490358, printed p28 2c3f9512a32d1dde6cf872127e9253a1e6c6d52827318af4da0c4a7f5054aa9f; p30 bee1cac337117b0fed9436be7b7878e4529fee0acf4157a13ccd09f62709e0be; p35 01d684a06b47b92e4ac7165062e86e4720e16ffcb356903ff90274aa74918bdd; p37 dd822a5b4e6fe0c764e23a173bd21626477a4f10c3f5fe2ccd57f47b43078fb6

Each fresh renderer fetched the official PDF, validated SHA-256 and size against the immutable pin, and rendered original pages at 160 dpi; the downloadable Actions artifacts preserve `render_manifest.json` with each PNG hash. EV-132 independently covers V2.2 body pages 25,27,31,33. Exact original p27 (V2.2), p27 (V2.3), p30 (V2.4) and p36 (V2.1) were directly inspected along with the English corresponding p33/p33/p37.

## Disproof and classification

The strongest counter-hypothesis is that the German TXT section intentionally shares the SRV section number (or that this is only a TOC error). It fails: German **body headings**, not merely TOC, duplicate 3.3.1 in three editions; English body and its explicit chapter references distinguish 3.3.1 SRV from 3.3.2 TXT in each edition. The immediately preceding V2.1 source also has the correct distinct German headings.

This is a confirmed publication **editorial/documentation/navigation and cross-reference defect**, with `normative_authority=contextual_only`, `sdk_behavior=no_runtime_diagnostic`, `runtime_match=not_applicable`, **no XML conformance effect** and no provider-facing FAIL. No schema declaration or executable content is affected. Exact XSD remains the executable authority for independently schema-validatable matters; this finding requires no XML example and no XSD locator. No XSD modification, PR remediation or branch rewrite authorized.

**Scope-correction history:** frozen terminal V2.2-only record was incomplete. Existing ID DR3012GC22-002 now covers V2.2, V2.3 and V2.4; V2.1 clean prior control; no later corrected GC release established. Updated semantic classification, source locators, body verification, version-scope boundary, SDK semantic-blob reference, current state. New unique locator credit **75/192**; boundary **75/75**; semantic **192/192**. Full gate and terminal handoff are required after this evidence commit.
