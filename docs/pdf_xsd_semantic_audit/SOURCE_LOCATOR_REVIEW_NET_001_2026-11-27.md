# Source locator review — NET-001

Date: 2026-11-27. Existing confirmed_pdf_defect, contextual_only, documentation_only, no_runtime_diagnostic unchanged.

## Original body and independent version context

NET-001 confirmed_pdf_defect, contextual_only, documentation_only, no_runtime_diagnostic: one bilingual VDV 301-3 Network Infrastructure 02/2020 publication; English printed p8 §1 Scope first paragraph has VDV 303-3, German p7 §1 Anwendungsbereich and both forewords p4, title and same-page footer establish VDV 301-3. One occurrence of 303-3 in each independent archived fulltext. No dedicated earlier or corrected later edition independently established. No XSD lane or new runtime rule; keep DRNET20-002 separate.

| Original surface | Observation |
| --- | --- |
| Cover (physical p1) | VDV-Schrift 301-3, 02/2020, Teil 3 Netzwerkinfrastruktur / Network infrastructure |
| Printed p4 Vorwort / Foreword | Both correctly identify VDV 301-3 |
| Printed p7 §1 Anwendungsbereich, first paragraph | VDV 301-3 |
| Printed p8 §1 Scope, first paragraph | VDV 303-3 |
| Printed p8 footer | VDV-Schrift 301-3, 02/2020 |
| Printed p31 §7 Versionshistorie / Version History | Empty |

## Active disproof and SDK impact

The opening Scope sentence is a local self-reference; same-language foreword and same-page footer, corresponding German paragraph, cover and publication catalog independently rule out interpreting 303-3 as a separate specification authority. Two independently archived fulltext extracts each contain exactly one 303-3 occurrence. The separate English Figure 1 safety/security caption is DRNET20-002, not duplicated here. This physical-network writing has no XSD lane. Do not generate alternative document identity, profile, alias or runtime trigger; no XSD, mapping or semantic change. No new EV-154 execution or hardware validation. Full schema gate is regression/no-mutation guard only.

## Evidence

- Exact registered source VDV301-3_02-2020 SHA256 edfedf36eeb18075b45bf5224f0da6500cdd489438091f18bada42f9668c2a99 size 558005, 37 physical pages. Original pin run 33270251357 SUCCESS; fresh pin run 34232022618 SUCCESS on ce24df3f6e637734dadf3643b3d6f8f689be001c. Fresh archive 10058187809 ZIP SHA256 5f978eccdddf1d20cd6b62b4798bceae12b11438a4cbf59d9d5a98611a17421a size 1816277; all 26 manifest entries independently rehashed after archive-prefix removal; pin-result.json records matching historical PDF SHA and size, retrieved 2026-09-08T13:27:14Z. PDF raw bytes not newly retrieved in this review.
- EV-154 run 34232483234 SUCCESS on 3645ddfeb32effd0b17432672ab91476e1accdf8, artifact 10058380451 ZIP SHA256 dcb266cad68054375d65818fda20d7ec53c59843a48525d60b3ade62f5c38396 size 1797394, ev154-result.json SHA256 43f22a890a20322499a4d1cf1fab3a9f4bb63593ead23c4f896371e1b98b89ad. All seven render hashes/sizes rechecked and byte-identical to fresh pin archive. Actual p7 PNG SHA256 be9c6c96cab9989dd79c6e5a58b62f170fcbe62450444c87707b186a68706e1e size 323271 and p8 1a50ca1b7db00fe9f7e2f8eb97e197c627ce99fd9acff602da4fe921bd9dc429 size 262659 visually inspected. EV-154 reports alternate document identity rejected; no new EV-154 execution.
- Historical run 33270251357 artifact 9719880284 ZIP SHA256 2cc403407a354af07c2dfc1cc78666e0f16fc753af6eebfaf090b0300214d930 size 4431133; fulltext SHA256 dd6ecfa0d78f0a00b86557aa2e3694883431fc6a7a1d5a92b4663981996a3276 and all 37 120-dpi PNGs verified against manifest. Cover physical p1 PNG 604e23b80819aa9158d28b167c72e52d50bc2011a6e835f794757d0bf973ea35, bilingual foreword printed p4 47326e71643c758e0fc6bea6b2b39a69bf80c0948eec0a2aef9adee30b5c4f92, empty version history printed p31 7eb51a5a8daac0ecbea9c8404ca7997220297a35832991abb7400c53bb630029 visually inspected. Both archived complete text extracts contain exactly one 303-3 occurrence. Live screenshot cache miss resolved using verified existing original renders.
- Official VDV catalog https://www.vdv.de/ip-kom-oev.aspx checked 2026-11-27 lists only dedicated 301-3 02/2020. VDV annual report 2020/2021 https://www.vdv.de/html/epaper/vdv-jahresbericht-2020-2021/index.html lists 301-3 2/2020 among 2020 new publications. Empty §7 Version History p31 visually confirmed; no independently established separate earlier or corrected later publication. DE and EN are same bilingual publication, DE unaffected control, EN affected only at p8 first paragraph.
- Active disproof: title, bilingual foreword, corresponding German scope, English same-page footer and surrounding scope content establish local self-reference, not alternative external authority. DRNET20-002 on same page concerns Figure 1 translation, not this paragraph. No XSD lane for this physical/network/protocol document, no runtime mapping, no hardware or executable validation claim; full XSD gate regression only. Existing semantic/diagnostic and source-pin records unchanged.

## Closure

136/192 locator/body/boundary entries pending both CI gates. Next NET-002 only after terminal closure and memory review.
