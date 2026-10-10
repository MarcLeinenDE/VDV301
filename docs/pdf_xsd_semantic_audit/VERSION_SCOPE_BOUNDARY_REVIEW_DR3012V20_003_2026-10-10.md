# DR3012V20-003 — Heartbeat typo, bilingual Base V2.0/V2.1 version boundary (2026-10-10)

**Independently checked version scope using existing exact-byte verified original-body renders; full schema gate pending.** Historical finding ID DR3012V20-003 remains, correlated to primary same-root DR3012-003 (V1.0–V2.1). Never produce two independent manufacturer diagnostics for the same XSD-invalid XML.

## Original source and version proof

| Publication/language | Actual printed body; official source SHA-256 | Exact selected released XSD |
| --- | --- | --- |
| Part2 V1.0 DE | p65 Tables25/26 show `HertbeatIntervall`, 0:1, duration in both; `VDV301-2_V1.0_DE`, SHA256 `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75` | Official VDV-301-1.0 blob `8995c4a230bf81d5e47b9313ee7725ff3cd4b7b5`: `HeartbeatIntervall` double in SystemConfigurationData and duration in StoreSystemConfigurationRequestStructure |
| Part2 V1.0 EN separate translation | p88 Tables104/105 same PDF spelling and duration, `VDV301-2_V1.0_EN` SHA256 `e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7` | Same official V1.0 released XSD, no separate English executable schema |
| Base V2.0 DE/EN | p100 actual Tables30/31 show `HertbeatIntervall` 0:1 xs:duration; p105 §8.1.2 claims corrected `HeartbeatInterval`; `VDV301-2_BASE_V2.0` SHA256 `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37` | Official VDV-301-2.0 `IBIS-IP_SystemDocumentationService_V2.0.xsd`, blob `ab959dddbfa2b8ca420af1b079501f94cff38051`: lines30/39 `HeartbeatInterval` type IBIS-IP.duration, minOccurs=0 |
| Base V2.1 DE/EN | p113 actual Tables55/56 **still** show `HertbeatIntervall` 0:1 xs:duration; p118 §8.1.2 falsely claims already corrected; `VDV301-2_BASE_V2.1` SHA256 `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` | Official VDV-301-2.1 tag carries byte-identical V2.0 XSD blob `ab959dddbfa2b8ca420af1b079501f94cff38051`, lines30/39 `HeartbeatInterval` duration |

Exact earlier *visually reviewed original* evidence reused: V1 DE p65 render `1bf5fc05dcc3313bc74ff8994187fedaea0249fb2c9bc1a723a6fd37abff0b36`; V1 EN p88 `c9bce23ac4f0eaf8cfe873982fd6735b22c71bc25723caffe3499eaba7523ae1` (run38032750261 artifact11662262438); V2.0 p100 `3b6551a60c8514c15753fcbeaec4e678f42bca7184b98e768658902a857ec355`; V2.1 p113 `c900b67dc0e6dc806b65d0084dbf9c395ed4b475a8c6f4e663c8b54bb1f24c9c` and p118 `ce477bf0ccb6e29681438f359edbef7956ee2402a40461c5ff269daa159391fa`, all as in `VERSION_SCOPE_BOUNDARY_REVIEW_DR3012_003_2026-10-10.md`. Original V2.0 EV130 p100 PNG `fce057d9d8ebf6d8cc69407393c7341ff1fae672cc7df684ed482c02148db9c3`, p105 `0e1bea0141021712bc812bb9987a9e8f1c444ef12729628529060735dda1242a`; different render parameters can yield different PNG hashes from identical PDF bytes.

The official online PDF text layer was separately rechecked 2026-10-10 and corroborates V2.0 p100 Tables30/31, V2.1 p113 Tables55/56 and p118 version history. The web screenshot endpoint returned cache misses; **no new visual proof is claimed from those failures**. Per mandatory fallback rule, this review reuses earlier exact-byte pinned successful visual render artifacts, rather than inferring from TOC or text alone. Release XSDs were freshly re-fetched at VDVde/VDV301 tags 2.0 and 2.1 and match exact blob `ab959dddbfa2b8ca420af1b079501f94cff38051`.

## Independent boundary and disproof

The underlying PDF typo already exists in independently checked V1.0 German and EN source bodies (primary DR3012-003), but V1.0 official XML member is `HeartbeatIntervall` with structure-specific double/duration. The V20-specific historical finding first appears in bilingual Base V2.0; remains in Base V2.1 (last independently checked **dedicated** SystemDocumentationService publication). V2.1 version history is not a corrected table. No separate later dedicated service publication/correction is established; V2.2–V2.4 Common Conventions describe a different publication scope.

The actual V2.0/V2.1 released XSD uses only `HeartbeatInterval`, type `IBIS-IP.duration` in both structures. Neither wrong PDF `HertbeatIntervall` nor obsolete V1.0 `HeartbeatIntervall` becomes an alias. The V1.0 double-vs-duration mismatch **does not persist** into V2.0/2.1. Same root as DR3012-003; correlation, not duplicate findings/failures.

## Conformance and handoff

`confirmed_pdf_defect`, selected official XSD normative; `sdk_behavior=error_with_advisory` only when XML is **already XSD INVALID**, `runtime_match=reviewed_not_implemented`. Deduplicate with DR3012-003 before provider output. Do not change any XSD, PR, runtime matcher or public normative rules in this boundary-review work.

Boundary progress **68/70 → 69/70**, one pending, next `DR3012V20-004`. Commit evidence/registry/current-state atomically as `gate_pending`, run full schema-audit-validation, then separate `terminal_clean` commit and verify exact-final-HEAD handoff-integrity before new finding.
