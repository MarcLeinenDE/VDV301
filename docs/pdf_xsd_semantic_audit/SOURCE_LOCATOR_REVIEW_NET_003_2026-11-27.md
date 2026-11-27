# Source locator review and bilingual scope correction — NET-003

Date: 2026-11-27. Existing confirmed_pdf_defect, contextual_only, documentation_only, no_runtime_diagnostic unchanged.

## Original body and independent version context

NET-003 confirmed_pdf_defect, contextual_only, documentation_only, no_runtime_diagnostic: one bilingual VDV 301-3 Network Infrastructure 02/2020 publication; DE printed p11 §2.2.4 Lichtwellenleiter LWL and EN p17 §2.2.4 Fibre optic cable LWL visibly print IEE 802.3. Both independent archived fulltexts contain two exact occurrences; correct IEEE 802.3 on pp7/8/10 and preceding §2.2.3 on same EN p17, correct IEEE 802.3af/at/bt on p29 and reference (12) p33. EN affected locator newly confirmed, same finding ID, both languages affected in same sole established edition. No new classification or technical/runtime rule. Historical EV-154 narrower p11 observation preserved; DRNET20-003 excludes both occurrences and remains three separate residue targets.

| Actual original body | Observation |
| --- | --- |
| Printed p11 §2.2.4 Lichtwellenleiter LWL | DE affected, IEE 802.3 |
| Printed p17 §2.2.4 Fibre optic cable LWL | EN affected, IEE 802.3, newly visually established |
| Printed pp10/17 §2.2.3 | DE and EN correct IEEE 802.3 |
| Printed pp7/8 §1 | DE and EN correct IEEE 802.3 |
| Printed p29 §5 | DE and EN correct IEEE 802.3af/at/bt |
| Printed pp32/33 References, item (12) | IEEE 802.3, IEEE Standard for Ethernet |

## Correction and disproof

Historical EV-154 German p11 observation is valid but incomplete in language coverage. Its original 180dpi render set does not include p17. Both independently archived fulltexts contain two IEE 802.3 matches; historical full-page render independently proves EN p17. Preceding §2.2.3 on same English page uses IEEE 802.3, refuting intentional alternate abbreviation. The reference list corroborates intended identity; no specific IEEE edition or new technical requirement inferred. No whole-document translation equivalence claim.

Update current semantic NET-003 language scope and bilingual diagnostic descriptions, clarify DRNET20-003 exclusion of both occurrences, preserve original EV-144/154 reports and frozen 192-ID inventory. Re-pin locator and runtime mapping semantic-registry Git blob to 4dd51f910e46d2135715e3587f9d5a82349bf5ea. Runtime mapping contents unchanged apart from provenance pointer. The three historical DRNET20-003 residue targets pp18/19/29 remain unchanged; p29 is merely a positive spelling control for NET-003. Correction creates no new identity, duplicate credit or executable alias. Targeted machine regression checks both actual affected body locators and unchanged distinct residue target set; does not replace visual evidence.

## Evidence

- Source VDV301-3_02-2020 SHA256 edfedf36eeb18075b45bf5224f0da6500cdd489438091f18bada42f9668c2a99 size 558005, 37 pages; reused local archives, independently rehashed. Historical run 33270251357 SUCCESS artifact 9719880284 ZIP SHA256 2cc403407a354af07c2dfc1cc78666e0f16fc753af6eebfaf090b0300214d930 size 4431133; fulltext SHA256 dd6ecfa0d78f0a00b86557aa2e3694883431fc6a7a1d5a92b4663981996a3276 and 37 PNG hashes verified. Fresh pin run 34232022618 SUCCESS artifact 10058187809 ZIP SHA256 5f978eccdddf1d20cd6b62b4798bceae12b11438a4cbf59d9d5a98611a17421a size 1816277; 26 manifest entries verified, full-text.txt SHA256 37441c55979a7676c033aed6c7fdc4469589ed3091eab3acb10ef8ec00d50b1b. Both fulltexts contain two exact word-boundary IEE 802.3 matches (DE p11 and EN p17), eleven IEEE 802.3 matches including suffixed references. No new raw PDF retrieval.
- EV-154 run 34232483234 SUCCESS on 3645ddfeb32effd0b17432672ab91476e1accdf8 artifact 10058380451 ZIP SHA256 dcb266cad68054375d65818fda20d7ec53c59843a48525d60b3ade62f5c38396 size 1797394; ev154-result.json SHA256 43f22a890a20322499a4d1cf1fab3a9f4bb63593ead23c4f896371e1b98b89ad. All seven render hashes/sizes match archived result and fresh pin archive. Historical NET-003 result inspected p7/8/11/29, did not render p17; remains valid for narrower observation. No new EV-154 execution. EN evidence is historical full-page archive, not EV-154 subset.
- Actual visible affected DE p11 §2.2.4 180dpi SHA256 91bfa3416a4193d1ec2aadce859aec85708fb8d113f0e2167728c7886c3ccb2f size 356200; EN p17 §2.2.4 120dpi SHA256 c2272f6b9fa56869cda4a00195e6320ed32b6b87ce9f23c27e97d49fd8d00680, verified against historical manifest. Both second paragraphs contain IEE 802.3; preceding EN §2.2.3 correctly uses IEEE 802.3. Live screenshots p11 and p17 cache miss; reused exact pinned original renders.
- Visible same-document controls: p7 §1 Anwendungsbereich 180dpi be9c6c96cab9989dd79c6e5a58b62f170fcbe62450444c87707b186a68706e1e; p8 §1 Scope 180dpi 1a50ca1b7db00fe9f7e2f8eb97e197c627ce99fd9dc429; p10 §2.2.3 Leitungen auf Kupferbasis 120dpi 51cb3352eec2597e9f94401fcdfaec5882f909bbb21f9e8b7efb5ee9cf29b9c6; p29 both §5 PoE 180dpi 2d29469bf5e5a5ba63e92f9cc8461200d703d46a9f11e710ca356cd09283ecd2; p32 actual heading Regelwerke – Normen und Empfehlungen / References 120dpi 08e3849e873bf312a370c44f455487a44781183602dfb25d5be35aa33865d812 and continuing p33 item (12) IEEE 802.3 IEEE Standard for Ethernet 120dpi f985e4e2481667f90a740eaf9606ff15b4579d5f8a4be69e2d2cc7b9f68742a7; p31 empty §7 history 120dpi 7eb51a5a8daac0ecbea9c8404ca7997220297a35832991abb7400c53bb630029. No specific dated IEEE standard edition inferred.
- Official VDV catalog https://www.vdv.de/ip-kom-oev.aspx checked 2026-11-27: dedicated 301-3 only 02/2020 listed; same-day NET-001 annual-report evidence reused. One bilingual publication; both affected tracks; no independently established separate earlier or corrected later edition. Prior reports and frozen finding/provenance baseline preserved.
- Cross-finding scan: all 192 semantic entries, all 137 existing locator/body/boundary entries and all runtime mappings searched for IEE 802.3 or NET-003 references. Only NET-003 and DRNET20-003 semantic entries and latter existing locator/body/boundary entries match; no runtime matcher. Clarify DRNET20-003 exclusion of both DE/EN occurrences, preserve actual p18/19/29 targets and prior evidence; p29 NET-003 positive spelling control only. Regression guard requires both affected NET-003 body locators, unchanged DRNET20-003 target pages, no runtime mapping, no XSD lane. Scope correction creates no new identity or extra progress credit; historical EV-144/EV-154 records untouched.

## Closure

138/192 locator/body/boundary entries pending both CI gates. All six network findings now have structural/body/boundary entries. Next PCS-001 only after terminal closure and memory review.
