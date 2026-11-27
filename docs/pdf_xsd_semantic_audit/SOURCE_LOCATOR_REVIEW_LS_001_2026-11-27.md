# Source locator review — LS-001

Date: 2026-11-27. Existing cross_artifact_mismatch, selected_xsd, error_with_advisory, xsd_invalid_advisory, reviewed_not_implemented unchanged.

## Original body and independent version context

GNSSLocationService V1.0 PDF EN January 2014 p70 Table 48 and DE July 2016 p7 Table 1 both print HorizontalDilutionOfPrecision, optional 0:1 IBIS-IP.double; historical combined LocationService and selected standalone GNSS XSD declare HoriziontalDilutionOfPrecision, optional minOccurs=0/default maxOccurs=1, same type. EV-153 confirms selected XSD spelling PASS and PDF spelling FAIL. Retain cross_artifact_mismatch, selected_xsd, error_with_advisory; no alias, XSD or runtime change.

EN p70 §9.5 and DE p7 §1.2 show the same optional HDOP field next to VDOP. The EN hyphen is a visible line-break hyphen, not part of the name; DE wraps without a hyphen. The 2016 foreword says the document was separated from the January 2014 aggregate; p6 records unspecified spelling corrections on 11 March 2016, not a named HDOP correction. VDV catalog checked anew, only standalone V1.0 listed. No separate DE historical full aggregate or EN standalone independently established.

## Exact XSD and active disproof

Historical combined official LocationService schema and later standalone GNSS schema contain the same GNSS root and complete 14-field type after formatting normalization. Common/Enum exact blobs identical. Both contain the misspelling with optional cardinality; no alternative correct-spelling element. This confirms conflict predates the split, not translation, PDF line wrapping, or version mismatch. Do not equate complete combined schema to standalone GNSS: it contains additional service declarations. Existing deduplication policy remains valid for the targeted GNSS structure. Conventional terminology strongly suggests an XSD typo, but no explicit official erratum or changed official declaration was established; preserve existing cross_artifact_mismatch classification without definitive attribution.

## Executable evidence and SDK impact

Archived EV-153 positive/negative samples differ only in the opening and closing HDOP element spelling. Positive valid, negative rejected. Optional field absent is not a defect trigger; matching invalid XSD result can be decorated, never overridden. No new EV-153 run or historical combined-schema compilation. No XSD or runtime changes.

## Evidence

- EV-153 run 34229647400 SUCCESS rechecked on 45eeed958b3f7f1081f19d6858e54a27824c682f, artifact 10057222866 ZIP SHA256 914a1b126e8c06145fe0ccc896f4e2a85db5204a7562ad7dada21ad660fecff7 size 1077575; all 25 manifest entries verified. DE original p7 PNG SHA256 400ca6d9488609131a9fcab6ff024b7e8d310d972f48174d96cd7b429e5bce8e size 341322 visually inspected.
- Historical GNSS_V1.0 pin run 34228583786 job 102068710920 artifact 10056787340 ZIP SHA256 ddbcc1774639c3d57a5cdf8efbc5f213a107f804d303cf11af520f5b1d66fe8e; all 21 manifest entries verified after removal of archive path prefix; pin-results and pdfs.sha256 agree on source SHA256 e6a19a333a6c149a2d4b726a189acf16a9891d85dd28a7c5b008cdf254b631f5 size 449287 retrieved 2026-09-08T12:52:58Z. Same p7 PNG hash as EV-153. Historical pin added centrally; no new DE raw PDF download.
- EN exact-source fallback run 45998400696 SUCCESS artifact 15196079487 ZIP SHA256 4f155f21baf073d7ca647d6fa252c0bb02abd1a98a178b106d0f946e51925b6e size 288968; VDV301-2_V1.0_EN source SHA256 e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7 size 2403598; p70 PNG a53bb9ed4e53bd4dcfd5cfeee8859a57841c2efc30dd1aadde57ff66ea2ba161 size 313736 verified against manifest and visually inspected. Printed EN wraps as HorizontalDilutionOfPre- / cision, DE HorizontalDilutionOfPrec / ision. Both rows optional 0:1; vertical neighbor same type and correct spelling.
- Exact upstream VDV-301-1.0 historical combined IBIS-IP_LocationService_V1.0.xsd blob 2a653ba7d35a6e91b5fd691eb5c606160192ab9e root line 8, type lines 10-31, spelling line 20; selected VDV-301-2.0 standalone IBIS-IP_GNSSLocationService_V1.0.xsd blob a74a22079af25cdd028a3e519019d9b3326d9971 root line 7, type lines 9-30, spelling line 19. Actual selected branch blob identical. Root declaration and entire GNSS type (14 ordered fields incl. annotation) identical after whitespace/line-ending normalization. Same Common 194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c and Enum a9bea5bc73003ed91ded8519db06c32c4067831d in both routes; 2.1/2.2/2.3/master same standalone blob and dependencies. Requested VDV-301-2.4 tag not found; no equivalence claim for a missing tag. SUPERBRANCH_V1_0_DEDUP_POLICY.md existing split retained; no full combined-schema equivalence asserted.
- EV-153 archived result SHA256 d0e25558f3b99390ae6742473e5b00d7de43de2c466d97aa8a5e16302fcea72e, positive sample fecf00bc529c4a0cdc60486cd14740525ce9010a95d3c3f3c15d2156889d9f67 size 369 and negative 781a02377aa78a458bab916e26780d33f94894425abcf377bbd13ef1c76a2822 size 367 verified. Only start/end name differs, result positive valid and negative rejected. Historical initial failed run 34229230088 caused by line-wrap text extraction, repaired without classification change. No new instance run or historical combined-schema compilation.
- Fresh VDV public catalog check 2026-11-27 https://www.vdv.de/ip-kom-oev.aspx lists GNSS 301-2-5 V1.0 only, January 2014 EN aggregate and DE base service link; no independently established separate DE 2014 aggregate or EN 2016 standalone, earlier/later standalone publication. DE p6 history records spelling corrections 11.03.2016 without identifying the affected field; cannot infer an authoritative correction to this XSD. No independent erratum confirming source attribution; conventional spelling supports likely XSD typo but classification remains cross_artifact_mismatch.
- Runtime mapping exact official GNSS V1.0 xsd_invalid_advisory, xsd_result_invalid, decorate_existing_invalid, reviewed_not_implemented. Optional HDOP absent does not trigger finding. Preserve invalid result, no normalization.

## Closure

133/192 locator/body/boundary entries pending both CI gates. Next LS-002 only after terminal closure and memory review.
