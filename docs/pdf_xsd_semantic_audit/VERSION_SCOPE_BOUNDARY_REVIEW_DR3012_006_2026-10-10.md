# DR3012-006 — SNTP/TimeService reference German-only V1.0 version boundary (2026-10-10)

**Independently verified from original visible PDF pages; full gate pending.** One original source-routing defect, no XML validity effect.

| Publication | Actual section/page | Exact routing text / meaning | Evidence |
| --- | --- | --- | --- |
| VDV301-2 **V1.0 German original** | p22 §2.5 Weitere Protokolle | Incorrect **VDV 301-2-11** for SNTP; historically VideoLiveService part, not TimeService | Existing source-locator visual EV129 p22, `SOURCE_LOCATOR_REVIEW_DR3012_006_2026-10-07.md` |
| Separate **V1.0 English translation** | p23 §4.5 Other Protocols | **Correct even in V1.0:** internal `cf. chapter 9.12` is TimeService | Run [38038529046](https://github.com/MarcLeinenDE/VDV301/actions/runs/38038529046), artifact11664686883; PNG `ceb0e04095e9576a40121435e29816c6229db9be8454193e96a66e072bf1c722` |
| Bilingual Base **V2.0** | p25 §2.5 DE / EN | Both correctly refer to **VDV 301-2-10** | Run38038541699 artifact11664264479; PNG `d4e13d1542bd8874adc3c6347e3129ba9565a62f8bb282929e4e1563cd0df1e3` |
| Bilingual Base **V2.1** | p26 §2.5 DE / EN | Both correctly refer to **VDV 301-2-10** | Run38038566530 artifact11665201453; PNG `15fc91c1bd3c51c2056ff925e611f15ede31da6ac09c4f86a6294105031ebc87` |
| Common Conventions **V2.2** | DE p19, EN p22 §2.5 | Both correct VDV301-2-10 | Run38038579949 artifact11664459254, p19 PNG `b42ff8d751c6a24dd9efa92f469494cc4f0481c316be0140ef060800457f6f90` p22 `582ea7b15d72070a8a7f63f1a58ecc0ba6497e18ac3a84b2244d34339ece4ef1` |
| Common Conventions **V2.3** | DE p19, EN p22 §2.5 | Both correct VDV301-2-10 | Run38038603575 artifact11664886682, p19 `7c10543198f362fc71be83d83a3cdef93426917e650b993f56a87049c3aae741`, p22 `2cbebcc04f7c8dccf46d28e7fd8a6f9b470bd5ec56f14e8847900b7017bbe089` |
| Common Conventions **V2.4** | DE p22, EN p25 §2.5 | Both correct VDV301-2-10 | Run38038616040 artifact11664901737, p22 `aa8394cf12cf6d1ba4c127771ad72b5da4292956c236b82cac721aee419e2424` p25 `f730712fbaac5f1c37692ef0982d71f3cb233305e3c4f53b915cac17deb02399` |

All requested official original source bytes independently matched registered SHA-256/length in `audit_registry/pdf_source_pins_v0.1.json` before PyMuPDF visual rendering. English V1.0 is a separately published translation, not assumed equivalent to German. Existing primary German p22 independently visually reviewed. Subsequent DE/EN pages were visibly inspected, not solely PDF text or TOC.

## Active falsification and source identity

The strongest alternative was that historical numbering changed or the English translation repeated the same mistake. Both are false: historic separately pinned `TIME_V1.0` identifies **TimeService VDV301-2-10** and `VLS_V1.0` identifies **VideoLiveService VDV301-2-11**. The separate V1.0 English original directly references the correctly located TimeService in its own chapter9.12. V2.0 DE+EN is already corrected to the official TimeService part-number, and V2.1 and Common2.2–2.4 do not reintroduce the defect.

## Provider and SDK implications

`confirmed_pdf_defect`, documentation/source-provenance routing only, `normative_authority=contextual_only`, `sdk_behavior=warning`, `runtime_match=not_applicable`. Do not flag a vendor XML payload as invalid from this paragraph; selected actual official XSD is still normative for any XML result. Do not back-apply the incorrect DE V1.0 reference to EN V1.0 or later releases. No upstream PR/remediation authorized by this evidence commit.

Boundary counts **64/70 → 65/70**, pending **5**, next `DR3012-007`, continue the five-pack after individual full gate and terminal-clean handoff.
