# Source-locator review — DR3012V20-005 — 2026-10-07

Status: **complete / visible-body verified / version scope corrected / documentation-only**.

## Finding

The SystemManagement introduction contains an unresolved chapter-range reference. Exact-byte review shows that the defect is not limited to Base V2.0: V2.1 fixes the English track but retains the missing German range start.

## Visible PDF evidence

### Historical unaffected control — V1.0

Official source:
- source ID: `VDV301-2_V1.0_DE`
- SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`
- printed page: **66**
- visible heading: `7.3 Dienst SystemManagementService`

The range is visibly complete as `Kapitel 5.2 bis 5.3`.

Exact-byte page PNG SHA-256:
`98925a4af4b14ddd2b2bbb3c7feaf78f9a00f2aa78e3ee3bd3dc28ee6c33960d`

### Base V2.0 — both languages affected

Official source:
- source ID: `VDV301-2_BASE_V2.0`
- SHA-256: `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`

Visible body:
- printed page **101**, `7.3 Dienst SystemManagementService`: German range contains unresolved placeholders.
- printed page **102**, `SystemManagementService`: English range contains the corresponding unresolved placeholders.

Exact-byte PNG SHA-256:
- page 101: `ffcd3e8eed4a21b3def22231efc418699904765ce5da5fcca70a56a0a19abe45`
- page 102: `e363907c96eedf70df39a46dacaabda9e005adbaf5fb2dfe7046309428151d55`

### Base V2.1 — partial persistence

Official source:
- source ID: `VDV301-2_BASE_V2.1`
- SHA-256: `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`
- printed page: **115**
- visible heading: `7.3 Dienst SystemManagementService / SystemManagementService`

On the same visible bilingual page:
- German still lacks the start chapter before `bis 5.3`.
- English is corrected to `chapter 5.2 to 5.3`.

Exact-byte page-115 PNG SHA-256:
`95e9f06d767164d6310d2f0c2001d22e1d86e950d350d4aecbc9d0384b00e6a5`

The live PDF renderer cache-missed the required pages; the canonical exact-byte fallback path was therefore used as required by `AUDIT_WORKFLOW_CONTRACT.md`.

## Active disproof

The placeholder is not an intended open-ended chapter range:

- V1.0 names the complete range 5.2–5.3.
- V2.1 English restores exactly 5.2–5.3.
- only the affected language/version tracks lose the start reference.

It is therefore editorial residue, not alternate technical semantics.

## Scope correction

The former V2.0-only semantic scope was too narrow. The existing finding identity is preserved and now covers:

- Base V2.0: German + English affected.
- Base V2.1: German affected, English corrected.

The correction is recorded in:
`docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_DR3012V20_005_V21_SCOPE_2026-10-07.md`

## Classification and SDK behavior

- classification: confirmed PDF/editorial defect;
- authority: documentation-only/contextual;
- no XSD locator is applicable;
- no XML validity effect;
- runtime match: not applicable;
- SDK behavior: informational only;
- no alias, normalization, repair or waiver.
