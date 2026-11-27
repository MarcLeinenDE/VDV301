# Source locator review — LS-002

Date: 2026-11-27. Existing non_defect, selected_xsd, no_runtime_diagnostic unchanged.

## Original body and independent version context

DistanceLocationService V1.0 PDF EN January 2014 p70 Table 47 (§9.4) and DE July 2016 p7 Table 1 (§1.2) both print Odometer-Pulses, optional 0:1 IBIS-IP.int; historical combined LocationService and selected standalone Distance XSD declare identical exact name/type/cardinality. EV-153 confirms hyphenated name PASS, normalized OdometerPulses FAIL. Preserve XML identifier literally; non_defect, selected_xsd, no_runtime_diagnostic unchanged; no alias, XSD or runtime change.

EN p70 Table 47 and DE p7 Table 1 show the exact same optional hyphenated field, following required Distance. Unlike the long GNSS identifier on the same English page, the hyphen is within a single line and not a wrapping artifact. DE p4 foreword states separation from January 2014 aggregate; p6 history contains no entries in extracted text. VDV catalog checked for standalone Distance publication; only V1.0 listed. No separate DE historical full aggregate or EN standalone independently established.

## Exact XSD and active disproof

Historical combined official LocationService schema and later standalone Distance schema have identical global Distance root and complete two-field type after formatting normalization. Common/Enum blobs identical, prior later tags checked in LS-001. Both contain Odometer-Pulses, optional, and no normalized spelling. No entire combined-schema equivalence claimed. There is no PDF/XSD conflict; the odd punctuation is part of the published contract. Do not silently normalize in model or code generation. An internal identifier may use a language-appropriate spelling only with explicit exact XML serialization mapping.

## Executable evidence and SDK impact

Archived EV-153 positive/negative samples differ only in the opening and closing Odometer tag names. Positive valid, normalized negative rejected. Optional field absent is not a defect trigger. The finding itself is a non-defect and needs no runtime diagnostic; ordinary XSD rejection of invalid XML remains authoritative. No new EV-153 run or historical combined-schema compilation. No XSD or runtime changes.

## Evidence

- EV-153 run 34229647400 SUCCESS on 45eeed958b3f7f1081f19d6858e54a27824c682f, artifact 10057222866 ZIP SHA256 914a1b126e8c06145fe0ccc896f4e2a85db5204a7562ad7dada21ad660fecff7 size 1077575; all 25 manifest entries independently rechecked. DE original p7 PNG SHA256 5ba0c63b9343c55e108b8741e5ee7eadeb1ae036b97045e335992ca4f195af7d size 130087 visually inspected.
- Historical DLS_V1.0 pin run 34228583786 job 102068710920 artifact 10056787340 ZIP SHA256 ddbcc1774639c3d57a5cdf8efbc5f213a107f804d303cf11af520f5b1d66fe8e; all 21 manifest entries reverified after removing archive path prefix; pin-results and pdfs.sha256 agree on source SHA256 bdcbb3b2188f109944d687e6511209c5f049f25e1770bb3f4df596542d5009c4 size 441422 retrieved 2026-09-08T12:52:56Z. DLS p7 PNG byte-identical between archives. Historical pin added centrally; no new DE raw PDF download.
- Reused LS-001 EN exact-source render run 45998400696 SUCCESS artifact 15196079487 ZIP SHA256 4f155f21baf073d7ca647d6fa252c0bb02abd1a98a178b106d0f946e51925b6e; source VDV301-2_V1.0_EN SHA256 e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7 size 2403598; p70 PNG a53bb9ed4e53bd4dcfd5cfeee8859a57841c2efc30dd1aadde57ff66ea2ba161 size 313736 rechecked against manifest and visually inspected specifically at Table 47. Both live PDF screenshot requests cache-miss; archived exact originals used.
- Exact official VDV-301-1.0 historical combined IBIS-IP_LocationService_V1.0.xsd blob 2a653ba7d35a6e91b5fd691eb5c606160192ab9e root line 7, type lines 32-41, Odometer-Pulses line 39; selected VDV-301-2.0 standalone IBIS-IP_DistanceLocationService_V1.0.xsd blob e6fdc418b6ddaba75d3fbe8f048d1c6d70e023b6 root line 7, type lines 9-18, Odometer-Pulses line 16. Actual selected branch blob identical. Root declaration and complete two-field type including annotation identical after whitespace/line-ending normalization. Prior LS-001 upstream tree checks confirm tags 2.1/2.2/2.3/master same Distance and Common/Enum blobs; no new tag inspection. Common 194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c and Enum a9bea5bc73003ed91ded8519db06c32c4067831d. No claim of whole combined-schema equivalence.
- EV-153 archived result SHA256 d0e25558f3b99390ae6742473e5b00d7de43de2c466d97aa8a5e16302fcea72e, positive sample eff4890c820958bf6dd7fc6c7c9e81a56153bb20f36b0ce6d327f1a45efcd2f5 size 154, negative d78cfe545df24418680ead36f339e9c09fff626d4d7b6b6c4104c478e8c6d4f3 size 152. Diff confirms only start/end tag spelling differs, same Distance=12.5 and pulse Value=42; positive valid, normalized alias rejected; archived error expected Odometer-Pulses. No new instance run or historical combined-schema compilation.
- VDV catalog https://www.vdv.de/ip-kom-oev.aspx checked 2026-11-27: Distance 301-2-4 standalone V1.0 only, January 2014 EN aggregate and DE base service link; no independently established separate DE 2014 full aggregate or EN 2016 standalone, earlier/later standalone publication. DE p4 foreword identifies separation from January 2014; p6 version history empty by text. No official successor or spelling correction established.
- Active disproof: both PDF rows carry literal hyphen on one line, exact historical and selected XSDs agree. Not a wrap artifact or inconsistent translation. Optional field may be absent; no invented normalized alias or new advisory. Language-specific identifiers may differ from XML names only with explicit mapping. Runtime semantic entry is not_applicable, no_runtime_diagnostic; no matching runtime activation exists.

## Closure

134/192 locator/body/boundary entries pending both CI gates. Next LS-003 only after terminal closure and memory review.
