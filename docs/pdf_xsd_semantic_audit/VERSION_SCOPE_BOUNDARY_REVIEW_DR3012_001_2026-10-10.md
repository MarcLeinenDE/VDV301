# DR3012-001 — RFC 2927 vs RFC 3927 original version/language boundary (2026-10-10)

**Evidence complete; final CI outcome in canonical CURRENT_STATE. MATERIAL scope correction: STOP current package after this finding.** Single existing DR3012-001 identity. Earlier V1.0-only classification was incomplete.

## Original visible-body version/language verification

All original PDF SHA256 hashes below were matched against the official VDV website source pins before reading. The locally re-inspected printed pages were taken from exact byte-pinned original PDF archives; their previously archived full page PNG sha256 values are given for independent reconstruction. V1.0 EN was separately requested through strict live byte-pinned GitHub renderer run **38026242425**, artifact **11659004456**, artifact digest `sha256:49a717470990a2214b3b9c8b0ff96371b3e535ebbcd7dcedc5268bb606d96302`.

| Publication | Language lane | Finding impact | Exact original PDF / visible body locator | Citation | Source SHA256 | Full page PNG SHA256 |
| --- | --- | --- | --- | --- | --- | --- |
| V1.0 | DE | **AFFECTED** | `VDV301-2_V1.0_DE`, p20 2.1.1 IP-Adressen | RFC 2927 | `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75` | `f47019ea03dcccdb4277894ee82af43aa290b781fbd4e963385e21ceadedb949` |
| V1.0 | EN | **AFFECTED** | `VDV301-2_V1.0_EN`, p21 4.1.1 IP Addresses | RFC 2927 | `e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7` | `d524a49f288e265eb5b5fe5a25fa5ff30d16e3d3ec5397d8068851936b562995` |
| V2.0 | DE | **CORRECTED / NOT AFFECTED** | `VDV301-2_BASE_V2.0`, p21 2.1.1 IP-Adressen | RFC 3927 | `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37` | `30d0cdb4e77b5f8aedec7a46fb2ac68d98ef8b21dc262e25f80bbe5e41e953cf` |
| V2.0 | EN | **AFFECTED** | `VDV301-2_BASE_V2.0`, p21 2.1.1 IP Addresses | RFC 2927 | `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37` | `30d0cdb4e77b5f8aedec7a46fb2ac68d98ef8b21dc262e25f80bbe5e41e953cf` |
| V2.1 | DE | **CORRECTED / NOT AFFECTED** | `VDV301-2_BASE_V2.1`, p22 2.1.1 IP-Adressen | RFC 3927 | `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` | `b1d9cc76d350ae67d368caf32979294f54e371a3843c9f46dfe513272c941293` |
| V2.1 | EN | **AFFECTED** | `VDV301-2_BASE_V2.1`, p22 2.1.1 IP Addresses | RFC 2927 | `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` | `b1d9cc76d350ae67d368caf32979294f54e371a3843c9f46dfe513272c941293` |
| V2.2 | EN | **AFFECTED** | `VDV301-2_GC_V2.2`, p20 2.1.1 IP Addresses | RFC 2927 | `96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051` | `5271e6215e176558a9c23a11bfffc3fd3ed43c2e9b892eac272b383f83243eaa` |
| V2.3 | EN | **AFFECTED** | `VDV301-2_GC_V2.3`, p20 2.1.1 IP Addresses | RFC 2927 | `4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603` | `d5e9199369836dcdeb96371ed575f83928f9fdbe1df610b72b87c6a54baa670e` |
| V2.4 | EN | **AFFECTED** | `VDV301-2_GC_V2.4`, p23 2.1.1 IP Addresses | RFC 2927 | `048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d` | `7d9e66400fe71ab7803188bc72d80babcbe76b42c419ab59684d3ff0e9dca97c` |

V1.0 EN original citation begins at **printed p21, §4.1.1 IP Addresses** and 169.254/16 continues at **p22** (p22 original PNG `97ea33b41cf12a374acc3241f7e2a529e60820d79a85ee74649904b57dac7af1`). The *separately translated* English V1.0 is not a German original. Base V2.0 and V2.1 are **bilingual in a single official file**: both the German **correct RFC 3927** and adjacent English **wrong RFC 2927** can be read together on the *same* printed page. Common Conventions V2.2–V2.4 have an English §2.1.1 addressing paragraph: do not imply an independently checked German equivalent of that paragraph. V2.2–V2.4 bibliography itself already gives **RFC 3927** (respective p75, p76, p80) while the addressing paragraph still says RFC 2927, an additional internal inconsistency.

Original source/provenance: official publisher <https://www.vdv.de/>; recorded URLs and exact source hashes are in `audit_registry/pdf_source_registry_v0.1.json` and `audit_registry/pdf_source_pins_v0.1.json`. Six full-PDF originals and their canonical page PNGs came from pin-validation GitHub run **33752224704**, artifact **9892036202** (digest `sha256:263b468f0d5752fa160e7d03e5097482c49e3e56650c8b33d014cc0cf5297030`). Historic first DE V1.0 revalidation remains `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_DR3012_001_2026-10-06.md` and EV-129.

## Independent external authority and disproof attempt

- RFC 2927: [MIME Directory Profile for LDAP Schema](https://www.rfc-editor.org/rfc/rfc2927.html) – an LDAP/MIME schema document; it is not the auto-configured link-local IPv4 address specification.
- RFC 3927: [Dynamic Configuration of IPv4 Link-Local Addresses](https://www.rfc-editor.org/rfc/rfc3927.html) – governs link-local auto-configuration of IPv4 address prefixes `169.254/16`.
- The citation occurs inside the visible §2.1.1 addressing paragraph, directly associated with automatic Zero Conf addressing and `169.254.xxx.xxx`, not as an independent bibliography example.
- The corrected German V2.0 paragraph independently confirms that RFC 3927 was the intended link-local reference. This disproves a reading of RFC 2927 as an intentional alternative. However, the contemporaneous English translation and all later checked English Common Conventions retain the defect.

## Explicit release boundaries

- **First affected**: VDV 301-2 V1.0 German original and separate English translation (both wrong). No earlier Part2 publication pinned in checked official corpus.
- **First known corrected German language passage**: bilingual Base V2.0 (§2.1.1 p21); still correct German in V2.1 (§2.1.1 p22). From V2.2 the checked Common Conventions paragraph is English; do not assert German passage fate without an independent German source.
- **English affected continuum**: V1.0 separate translation → bilingual Base V2.0 and V2.1 English passages → Common Conventions V2.2, V2.3, **V2.4** English passages. Last independently checked affected source: V2.4 p23; no independently verified corrected English successor. Absence is corpus-scoped, not universal.
- An unaffected **DE** passage in an otherwise affected bilingual **release** does not remove the EN affected lane from that version. Do not collapse release/translation/version authority into one latest-wins result.

## SDK and norm consequences

`confirmed_pdf_defect`, `primary_surface=external_standard`, `normative_authority=contextual_only`, `runtime_match=not_applicable`, `sdk_behavior=warning` only. RFC 3927 may inform external-network interpretation but no additional universal VDV implementation requirement, XML/XSD validation rule, provider FAIL, alias, normalization, or normative XSD rewrite is introduced from this citation error.

**Progress: 59/70 → 60/70 boundary verified, 10 remaining; next DR3012-002 (NEW package).** Gate-pending proof is in CURRENT_STATE; do not start second package finding before this one's full audit and terminal handoff are green.

## Gate repair and affected-only semantics

First full gate run **38026461279** caught `document_version` metadata inconsistencies: source registry versions are exact `1.0`/`2.0`/`2.1`/`2.2`/`2.3`/`2.4`, not `V1.0` etc. Repaired all DR3012-001 PDF locators to exact registry form. More importantly, the corrected **German** Base V2.0 and V2.1 paragraphs are retained only as `scope_role=correction_boundary_not_affected` in source locator evidence and boundary checks; they have been removed from semantic `version_scope` and cannot become runtime matching profiles. For bilingual releases with independent explicit DE/EN lanes, the source-locator validator now distinguishes the language tokens instead of conflating both lanes by numeric version alone. The affected semantic scope contains only V1.0 DE/EN and English V2.0–V2.4. The full gate is required before terminal closure.
