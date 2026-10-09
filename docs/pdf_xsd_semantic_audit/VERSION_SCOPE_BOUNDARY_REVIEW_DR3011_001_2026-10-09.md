# DR3011-001 — German + English V1.0 Part-1 section cross-reference boundary (2026-10-09)

**Outcome: verified, material expansion to the independently issued English V1.0 language track.** One existing finding ID, `confirmed_pdf_defect` / `contextual_only` / `no_runtime_diagnostic`. The old source locator cited only table of contents and the example; **the actual body sections have now been independently visually verified**.

## Exact original-body contradiction (not TOC-inferred)

| Source | Wrong example | Correct actual source-body headings |
| --- | --- | --- |
| Official German `VDV301-1_V1.0_DE`, SHA-256 `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2`, 1,052,021 bytes, 36 PDF pages | **Printed p10**, **Beispiel 1** describes `SystemManagementService` / `System-Management` but cites `vgl. 5.1.2` | **Printed p17** actual **§5.1.2 System-Dokumentation**; **p18** actual **§5.1.3 System-Management**. The TOC on p2 also agrees, but body headings, not the TOC, control the final locator. |
| Official separately issued English `VDV301-1_V1.0_EN` translation, SHA-256 `508cb52a9d9d459461954d46618d7b62a0ab9dc5698ef24e97fca2c458c551e4`, 1,261,072 bytes, 34 PDF pages | **Printed p11**, **Example 1** describes `SystemManagementService` / `System Management` but cites `cf. chapter 5.1.2` | **Printed p17** actual **§5.1.2 System Documentation**; **p18** actual **§5.1.3 System Management**. The English translation explicitly declares itself for convenience, without legal effect; German original applies if inconsistent. |

**Active disproof:** This is not a stale table-of-contents problem, a different German/English section numbering scheme, a legitimate service/function mapping, or a VDV 301-2 XSD mismatch. Both publications' **actual page body headings** independently disagree with the example's cross-reference. The correct intended section is §5.1.3. No XSD validation rule or provider fault follows from an editorial section citation.

## Evidence chain

- German official URL `https://www.vdv.de/vdv-301-1-ibis-ip-teil-1-systemarchitektur.pdfx`; pinned since original source review, verified again through `.github/workflows/pdf-render-fallback.yml` **run 37906160717 SUCCESS**, artifact **11604806247**, artifact digest `sha256:0983d7adef97e2ad5860a2fbdc82e2acaf9d0bd7b1691771f69d1c4142491271`. Original visible 160 dpi PNG hashes: p10 `3ab2c13ff2be2a8344fa163a2de41fd5584d61c35106a6270b9da2eecdf11112`, p17 `dc2145d6ef1422a70d90165ca81b5e3e13339f49b379c85800a5c947562a5941`, p18 `ad4d45918cb6aec3c67d9f379c85733a319d62882340a9dc017f2bb66de9bbef`.
- English official URL `https://www.vdv.de/301-1ses.pdfx`: independent first-source proposal **run 37906414201 SUCCESS**, artifact **11604343550**; first original bytes SHA-256 `508cb52a9d9d459461954d46618d7b62a0ab9dc5698ef24e97fca2c458c551e4`, size 1,261,072, 34 PDF pages. Added to canonical `audit_registry/pdf_source_pins_v0.1.json` before final render.
- Strict English `.github/workflows/pdf-render-fallback.yml` **run 37906694433 SUCCESS**, artifact **11603974595**, SHA-256 digest `sha256:90e2fe86638602714e0a24b4f8b2c42f77586d6a1b0f4730a2286ca06689ce16`, verified original source SHA-256 `508cb52a9d9d459461954d46618d7b62a0ab9dc5698ef24e97fca2c458c551e4` and exact size. Visible p11 PNG `83cb92ecee31b4b618b839c70386093bb0af7659d64e75bf68577ea6cd9e4889`, p17 `9637bbaf9eaeac43c0a4b79b73614836f1b3554917e424524d2fa01535c3619f`, p18 `4b306d690a8ccbdbcb3d977dac72ccbf5074b37f73984cea1e1eacd1cbbaab50`. All three actually reviewed.
- Old German source-locator review `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_DR3011_001_2026-10-06.md` and visual registry `audit_registry/vdv3011_visual_revalidation_evidence_2026-09-03.json` remain historical evidence. This report supersedes the **TOC-only** confidence basis by adding body headings and independent English translation.

## Version-scope upper/lower bound

The checked official <https://www.vdv.de/ip-kom-oev.aspx> VDV 301-1 architecture index and canonical source registry have **one version family: V1.0**, independently issued **German original** and **English translation**. There is **no available predecessor** and **no independently established later corrected VDV 301-1 publication** in these checked sources. This does *not* imply a proof that no successor exists anywhere; neither extrapolate the defect to hypothetical newer Part-1 versions nor claim correction. The English track also contains the defect; a German-only finding scope was incomplete.

## SDK and handoff

No runtime matcher, XML change, XSD edit, compatibility alias, waiver, provider failure or upstream remediation/PR is authorized. `normative_authority=contextual_only`, `sdk_behavior=no_runtime_diagnostic`, and `runtime_match=not_applicable` remain unchanged. The approved source-registry pin is evidence only; the official English translation remains nonbinding in case of inconsistency.

Progress: **56/70 → 57/70 boundary verified**, **13 remaining**; next `DR3011-002`. **Stop package after material language-scope addition**; require successful full `schema-audit-validation` and final `terminal_clean`/handoff-integrity before any next finding.
