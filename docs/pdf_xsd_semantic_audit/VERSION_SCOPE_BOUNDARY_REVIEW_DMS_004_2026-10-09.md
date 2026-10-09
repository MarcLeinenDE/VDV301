# DMS-004 — historical InstallUpdate required-field boundary (2026-10-09)

**Material scope correction, classification remains non-defect.** The exact selected XSD controls XML PASS/FAIL. The original verified list omitted an intermediate **V2.3 integration-only** context that still required three fields.

## Exact context and predecessor/successor check

| Version | Source authority | InstallUpdate request rules |
| --- | --- | --- |
| V1.0 | Upstream official `VDV-301-1.0`, DMS XSD blob `602a963f91000d0d39e3c271bacb3c7aba73e6d4` | InstallUpdate absent; no field requirement can be inferred for a nonexistent service operation |
| V2.0 | Upstream official `VDV-301-2.0`, DMS XSD blob `74189e0da65563eeb084ec2f3c400e9668d1ee1a` | InstallUpdate absent; last non-applicable predecessor |
| V2.1 | Official bilingual `VDV301-2_BASE_V2.1` PDF SHA-256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`, visible original p107 InstallUpdate request table; upstream official DMS XSD `191b43e01cdaba14b247725689a913c244a67eed`, lines 296–314 | First available operation model: `UpdateID`, `UpdateTimestamp`, `UpdateURL` all **1:1**; `UpdateFileChecksum` and `UpdateFileSize` **0:1** |
| V2.2 | Official bilingual `DMS_V2.2` PDF SHA-256 `72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e`, visible body p26; upstream official DMS XSD `c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d`, lines 247–265 | Same three required fields, same two optional fields; last **official** required-trio evidence |
| V2.3 integration | Local DMS XSD blob `5fe444cf6d10462cc23fd159eb963abbec42248f`, lines 247–265; `VDVde/VDV301` official `VDV-301-2.3` DMS file is not present; no separately pinned official DMS V2.3 PDF | **Still three required fields**, two optional. This is a selectable **integration-only** comparison, **not** an official release |
| V2.4 | Official bilingual `DMS_V2.4` PDF SHA-256 `347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd`, visible body p25; candidate/integration XSD `d222dfd98b2be3777576388da7ace8f333d24c3f`, lines 247–265 | **All five fields 0:1**. First verified published relaxation; candidate schema permits an empty request, never reclassified as official XSD |

The already validated original PDF body evidence is preserved in `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_DMS_004_2026-10-06.md`, the byte-pinned PDF source registries, and DMS revalidation evidence. A V2.3 PDF locator has deliberately **not** been fabricated: this lane cites only the exact integration XSD.

## Independent executable regression and disproof

`tools/validate_dms_instance_boundaries_ev127.py` now executes V2.3 as well as the earlier/recent schema routes. GitHub Actions run **37896539178** succeeded and confirmed:

- Official V2.1/V2.2: a complete required trio passes; omitting **each individual required field** fails.
- Integration V2.3: identical behaviour; each omission fails. The extension was executed against the exact local integration schema and its declared dependencies.
- Candidate V2.4: both empty and three-field requests pass.

Active disproof: the absence of an InstallUpdate operation before V2.1 is not equivalent to a field being optional in those releases. The V2.3 selected integration XSD proves the first **relaxation is not present in this intermediate schema**. V2.4 PDF and candidate XSD permit empty requests but cannot retroactively alter historical official validation results. No blanket rule that a device must support InstallUpdate is inferred merely from the existence of an XSD operation declaration.

## Diagnostic/SDK consequence and stop

The finding remains **`non_defect`**, `selected_xsd`, `no_runtime_diagnostic`, `runtime_match=not_applicable`. Missing trio fields in selected official V2.1/V2.2 and in V2.3 integration must produce **XSD FAIL**. The V2.4 candidate accepts missing fields. No XML normalization, alias, artificial SDK matcher, XSD mutation or upstream PR is introduced.

Canonical semantic, source locator, bilingual diagnostics, body-evidence pointer, runtime semantic SHA and boundary/SDK/current-state counts have been updated. Verification count moves **52/70 → 53/70** with **17 pending**; next `DMS-005`. Because this corrects a material omitted version lane, stop the current package here per the mandatory gate. Closure awaits successful full schema-audit-validation, `terminal_clean` state and final HEAD handoff-integrity success.
