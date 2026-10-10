# DR3012V20-001 — historical V2.0 bilingual RFC conflict and overlap with DR3012-001 (2026-10-10)

**Independently reviewed historical finding identity; full gate pending.** Do not create an additional SDK runtime failure: `DR3012-001` already records the identical root RFC 2927 vs RFC 3927 error across V1.0–V2.4.

| Publication/language | Visible IPv4 link-local text | Reference |
| --- | --- | --- |
| Original V1.0 DE and EN separately | Both wrong `RFC2927`, **no** German-correct/English-wrong split | `VERSION_SCOPE_BOUNDARY_REVIEW_DR3012_001_2026-10-10.md` original body p20 DE/p21 EN |
| Bilingual Base V2.0 original p21 §2.1.1 | **DE correct RFC3927; EN wrong RFC2927** | Same exact original page PNG SHA256 `30d0cdb4e77b5f8aedec7a46fb2ac68d98ef8b21dc262e25f80bbe5e41e953cf`, original SHA256 `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`; bibliography original p110 correctly RFC3927 |
| Bilingual Base V2.1 original p22 §2.1.1 | **DE correct RFC3927; EN wrong RFC2927** | Original p22 PNG SHA256 `b1d9cc76d350ae67d368caf32979294f54e371a3843c9f46dfe513272c941293`, source SHA256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` |
| Common Conventions V2.2–V2.4 | English text continues wrong RFC2927, independently corresponding German addressing paragraph not established | Prior full original-language release audit `VERSION_SCOPE_BOUNDARY_REVIEW_DR3012_001_2026-10-10.md`; do **not** claim ongoing DE/EN juxtaposition in later editions |

The original byte-pinned visible pages were already independently rendered and visually checked as part of the canonical DR3012-001 boundary correction, plus V20-001 original source-locator review; underlying exact PDF bytes and page hashes agree. We reuse the original pinned artifacts, not an inferred TOC reference.

## Identity, disproof and coverage boundary

DR3012V20-001 was historically recorded as a V2.0 DE-vs-EN mismatch, but the stronger independently audited `DR3012-001` covers the *same underlying citation error* from V1.0 through the latest checked Common V2.4 English track. The earlier German and English V1.0 are each wrong rather than contradictory to one another. Bilingual **contrast** starts V2.0 and is still visible V2.1. The English factual error itself persists through V2.4; later Common Conventions has no independently verified corresponding German address passage, so this narrower bilingual-contrast observation is not extrapolated as such.

The independent disproof test against RFC authority is already conclusive: `RFC2927` concerns LDAP/MIME schema, while `RFC3927` specifies link-local IPv4 `169.254/16`; the V2.0/V2.1 German passages and bibliography corroborate that the wrong English RFC was an editorial slip, not an alternative protocol. Preserve frozen ID for provenance but **correlate** it to primary `DR3012-001` when producing reports. One underlying issue must not produce two independent vendor errors or SDK diagnostics.

`confirmed_pdf_defect`; source-only, `sdk_behavior=warning` as historical knowledge, `runtime_match=not_applicable`. Official selected XSD still governs XML PASS/FAIL, completely unaffected. No XSD rewrite, invented alias or upstream remediation authorized by this audit.

Boundary **66/70 -> 67/70**, three pending, next `DR3012V20-002`. Continue same five-item package after exact-HEAD full gate and terminal handoff.
