# Source locator review — NET-002

Date: 2026-11-27. Existing confirmed_pdf_defect, contextual_only, documentation_only, no_runtime_diagnostic unchanged.

## Original body and independent version context

NET-002 confirmed_pdf_defect, contextual_only, documentation_only, no_runtime_diagnostic: one bilingual VDV 301-3 Network Infrastructure 02/2020 publication; DE printed p14 §2.3.4 versus EN p20 §2.3.5, corresponding preceding §2.3.3 on pp13/19, TOCs pp5/6, corresponding Figure 4 pp15/21. Both cabling paragraphs contain equivalent three recommendations (bandwidth-appropriate cable/connectors, same coding at both ends, Figure 4 reference); all five depicted connection examples and their acceptance marks agree. No missing technical subsection established. Both independent archived fulltext extracts show exactly two standalone occurrences each of 2.3.4 and 2.3.5. No XSD lane or new runtime rule; no independently established separate earlier or corrected later edition.

| Surface | DE | EN |
| --- | --- | --- |
| TOC | p5 2.3.3 → 2.3.4 | p6 2.3.3 → 2.3.5 |
| Previous body | p13 2.3.3 | p19 2.3.3 |
| Cabling paragraph | p14 2.3.4 | p20 2.3.5 |
| Figure 4 | p15 | p21 |

## Active disproof and SDK impact

Both body paragraphs recommend choosing connector/cable by necessary bandwidth, same coding at both ends, and refer to Figure 4. All five connection examples and approval/rejection marks agree in both diagrams. No separate EN 2.3.4 content is present; no missing technical section established by this comparison. The TOC repeats the body misnumbering, not an independent extra defect. No whole-document translation-equivalence claim. Preserve official source number in locators, distinguish proposed correction from published wording; no technical rule or profile version derived from the section number. No hardware conformity claim, XSD or runtime change.

## Evidence

- Source pin VDV301-3_02-2020 SHA256 edfedf36eeb18075b45bf5224f0da6500cdd489438091f18bada42f9668c2a99 size 558005, 37 pages; reused local archives from NET-001, independently rehashed this review. Historical run 33270251357 artifact 9719880284 ZIP SHA256 2cc403407a354af07c2dfc1cc78666e0f16fc753af6eebfaf090b0300214d930, all 37 PNG hashes and fulltext SHA256 dd6ecfa0d78f0a00b86557aa2e3694883431fc6a7a1d5a92b4663981996a3276 match manifest. Fresh pin run 34232022618 artifact 10058187809 ZIP SHA256 5f978eccdddf1d20cd6b62b4798bceae12b11438a4cbf59d9d5a98611a17421a; all 26 manifest entries verified. No new raw PDF retrieval.
- EV-154 run 34232483234, artifact 10058380451 ZIP SHA256 dcb266cad68054375d65818fda20d7ec53c59843a48525d60b3ade62f5c38396. All seven render hashes/sizes match result and are byte-identical to fresh pin archive. Visually inspected original p6 180dpi SHA256 f48e04a4663ce0e3d6175176074e971948630d223564f2b8c7e2636c4cb0a98e (230957 bytes), p14 709480cd89494e6da2c9ea590c7826d8c17ec6ce5be1360ce89a54ce70c90a77 (311919), p20 30b8f5d5139833ada803a58c9cff112c1f0273f1ff892363380963897edf1b16 (285445). No new EV-154 execution.
- Historical 120dpi visual controls: p5 TOC 25b64a568cb3419f0cb4f07323e2c7de1e2d128be577287eaaba40b1dcf6da1a; p13 prior DE heading 0becf52b6a86c677e22132bd85ee711493e2c3fe5fb51fc8aa6c411d2ffc721b; p19 prior EN heading 30958f0e276fbc75c3f85372fe17c13e5fd03579d9d4f24cb3f3ef2de569d4d7; p15 DE Figure4 27d423c2edeec8251b69cdaebeb3f44b2f7930c6376a920549cb6462f2e78ae4; p21 EN Figure4 d1b56e39cde5e240004924683ba195fc03d7bb08f2fa647995998da3d4ca52a8; p31 empty version history 7eb51a5a8daac0ecbea9c8404ca7997220297a35832991abb7400c53bb630029. Each actually visually inspected. Live official PDF screenshot p14 successful, p20 cache miss; exact pinned archived images decisive.
- Both independent archived fulltext extracts contain two occurrences each of 2.3.4 and 2.3.5 (TOC + corresponding body). Both preceding subsections §2.3.3 and subsequent Figure4 correspond; DE and EN paragraph content and five diagram examples/marks match. No inference of omitted technical requirements or technical equivalence of entire bilingual publication. The paragraph recommendations are not upgraded into normative hardware rules.
- Official VDV catalog https://www.vdv.de/ip-kom-oev.aspx checked again 2026-11-27 lists only dedicated 301-3 02/2020. Prior NET-001 same-day annual-report evidence (2020/2021 report identifies 02/2020 as new publication) reused, no new annual report retrieval. p31 history empty visually confirmed. DE unaffected numbering control and EN affected in same publication; no separate earlier or corrected later edition independently established. No XSD lane, no runtime matching or hardware validation, full gate regression only.

## Closure

137/192 locator/body/boundary entries pending both CI gates. Next NET-003 only after terminal closure and memory review.
