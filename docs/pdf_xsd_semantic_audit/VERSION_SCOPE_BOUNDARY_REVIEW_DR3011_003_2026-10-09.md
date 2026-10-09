# DR3011-003 — bilingual V1.0 Part 1 abbreviation duplication (2026-10-09)

**Outcome: version/language boundary independently verified, material bilingual scope extension; GATE PENDING.** Existing finding `DR3011-003` only. The DE/EN wording distinction is material and was not previously captured.

## Visible byte-pinned original evidence

| Official Part 1 V1.0 publication | Body locator | Actual `IBIS-IP` entries | Determination |
| --- | --- | --- | --- |
| **German original**, `VDV301-1_V1.0_DE`, PDF SHA256 `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2` (1,052,021 bytes) | Printed **p34**, actual body **§9 Abkürzungen**, table **Abkürzung / Beschreibung** | Two adjacent rows: first **Integriertes-Bord Informations-System auf Basis Internet Protokoll**, second **Integriertes-Bord-Informations-System auf Internet-Protokoll Basis** | **Duplicate abbreviation AND different long forms** |
| **Separately published English translation**, `VDV301-1_V1.0_EN`, PDF SHA256 `508cb52a9d9d459461954d46618d7b62a0ab9dc5698ef24e97fca2c458c551e4` (1,261,072 bytes) | Printed **p32**, actual body **§9 Abbreviations**, table **Abbreviation / Description** | Two adjacent rows both say **Integrated On-board Information System based on Internet Protocol** | **Duplicate abbreviation but IDENTICAL long forms** |

- DE official URL: <https://www.vdv.de/vdv-301-1-ibis-ip-teil-1-systemarchitektur.pdfx>. Pinned evidence run **33725750019**, artifact **9881897572**, render PNG printed p34 sha256 `c61689499c594d47cd99cc7b61de57b4f0183b20ca9c33ee508ab411bc7a709b`. Exact source SHA256 was recomputed from the downloaded official-source artifact and visible page independently inspected for this boundary pass.
- EN official URL: <https://www.vdv.de/301-1ses.pdfx>. Previously independently byte pinned, source proposal run **37906414201**. Strict exact-byte render run **37955160113**, artifact **11627128733**, digest `sha256:c7b827d5d65107ae3b314be797846eaf9f9ca1421beed052d7f13d7744ea5021`, visible p32 PNG sha256 `1d6a01918ab3e058578455c777c31743a949fcd1a556fa402c3b74683b936061`. Both IBIS-IP table rows visually inspected. The printed EN page is **32**, not the DE page **34**.
- The English translation is a separate official publication but expressly does not displace the German original in case of inconsistencies.
- Historical DE locator review `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_DR3011_003_2026-10-06.md` remains preserved as earlier evidence; this report adds the independently verified EN scope.

## Release boundary and active disproof

The checked official VDV Part1 architecture publication index and pinned PDF source registry contain German original **V1.0** and separately issued English **V1.0** translation, but no Part1 predecessor or independently verified later corrected edition. That absence is corpus-scoped evidence, not a general claim that no successor exists anywhere. Both separately inspected V1.0 editions have two adjacent entries with exactly the same abbreviation in the same table, so neither separate namespaces, different terms, nor a translation quirk explain the duplication. The wording difference in DE does **not** persist into EN; this is an explicit language-lane distinction, not another finding ID.

## Classification and SDK

Confirmed `confirmed_pdf_defect` / `editorial_residue` / `contextual_only`; `sdk_behavior=no_runtime_diagnostic`, `runtime_match=not_applicable`, and **no XML/XSD/provider consequence**. A corrected glossary would remove the duplicate in both editions and additionally reconcile the two long forms in DE. There is no evidence here for any provider FAIL, XML alias, unofficial XSD promotion, remediation commit, or runtime matcher.

Progress **58/70 → 59/70** verified, **11 pending**, next finding `DR3012-001`. **STOP package after material bilingual scope expansion and EN wording correction**. Before terminal closure require full `schema-audit-validation` SUCCESS for this exact pending HEAD and final `handoff-integrity` SUCCESS on the terminal HEAD.
