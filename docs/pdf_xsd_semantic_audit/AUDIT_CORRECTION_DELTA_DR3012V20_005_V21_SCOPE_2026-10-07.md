# Audit correction delta — DR3012V20-005 V2.1 scope — 2026-10-07

Status: **scope correction / existing finding identity preserved / no XSD or runtime change**.

## Reason

The frozen semantic entry for `DR3012V20-005` described the unresolved SystemManagement chapter-range placeholder as a Base V2.0-only documentation defect. The current exact-byte source-locator review tested the adjacent historical versions instead of assuming that boundary.

## Exact visible-body result

### VDV 301-2 V1.0 — unaffected control

- source: `VDV301-2_V1.0_DE`
- SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`
- printed page: **66**
- visible section: `7.3 Dienst SystemManagementService`
- visible reference: complete `Kapitel 5.2 bis 5.3`
- exact-byte page PNG SHA-256: `98925a4af4b14ddd2b2bbb3c7feaf78f9a00f2aa78e3ee3bd3dc28ee6c33960d`

V1.0 is therefore not affected.

### VDV 301-2 Base V2.0 — affected in both language tracks

- source: `VDV301-2_BASE_V2.0`
- SHA-256: `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`
- printed pages: **101** German, **102** English
- both visible introductions retain unresolved chapter-range placeholders
- page-101 PNG SHA-256: `ffcd3e8eed4a21b3def22231efc418699904765ce5da5fcca70a56a0a19abe45`
- page-102 PNG SHA-256: `e363907c96eedf70df39a46dacaabda9e005adbaf5fb2dfe7046309428151d55`

### VDV 301-2 Base V2.1 — partially affected

- source: `VDV301-2_BASE_V2.1`
- SHA-256: `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a`
- printed page: **115**
- German visibly still lacks the start chapter before `bis 5.3`
- English is visibly corrected to `chapter 5.2 to 5.3`
- exact-byte page PNG SHA-256: `95e9f06d767164d6310d2f0c2001d22e1d86e950d350d4aecbc9d0384b00e6a5`

The V2.1 revalidation report already establishes that persistent older Base-Service defects remain attached to their existing finding IDs rather than being duplicated. This correction therefore expands `DR3012V20-005` instead of creating a new finding.

## Canonical correction

Affected semantic scope is now:

1. **Base V2.0** — German and English affected.
2. **Base V2.1** — German affected; English corrected.

V1.0 is retained only as an unaffected historical control.

## SDK consequence

No executable XML rule changes:

- normative authority remains contextual/documentation-only;
- validation effect remains `documentation_only` / `no_runtime_effect`;
- runtime match remains `not_applicable`;
- no XSD alias, repair, normalization or waiver is introduced;
- finding inventory remains exactly **192** identities.

## Regression rule

A version-labelled finding must not be assumed to end at that version. Adjacent released versions must be checked independently, and partial bilingual corrections must be represented explicitly in the existing finding scope.
