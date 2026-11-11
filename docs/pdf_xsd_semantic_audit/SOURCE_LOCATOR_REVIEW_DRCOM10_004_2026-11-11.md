# SOURCE LOCATOR REVIEW — DRCOM10-004 — 2026-11-11

Status: **six-version original-body/source/authority evidence verified; canonical gate status and terminal closure tracked exclusively in `00_START_HERE/CURRENT_STATE.json`**.

## Identity, finding and historical scope

Unique established finding: **`DRCOM10-004`** for repeated `JourneyStopInformation.Announcement` and `JourneyStopInformation.FareZone`.

The prior semantic scope (Common V1.0 only) was incomplete. Original byte-pinned PDFs from each published Common V1.0, 2.0, 2.1, 2.2, 2.3, and 2.4 each visibly give **0:\*** for both elements; the corresponding exact selected XSD definitions all give **0:1** (`minOccurs=0`, omitted `maxOccurs` default 1). The mismatch affects XML-validity but does not justify changing the exact selected XSD.

The prior `confirmed_pdf_defect` source attribution is intentionally corrected to **`cross_artifact_mismatch`** (confirmed discrepancy; incorrect originating artifact/author intent not independently proven). Classification: `primary_issue_kind=cardinality_mismatch`; `normative_authority=selected_xsd`; `sdk_behavior=error_with_advisory`.

## Pinned original body and exact XSD source-by-source

All six runs used the deterministic `tools/render_vdv_pdf_pages.py` GitHub workflow and checked original source SHA256 and byte size against the canonical pins before producing PNGs. Each target PNG digest was verified against its artifact manifest and the **actual visible body** inspected, including nearby rows, visible section heading and table caption.

| Common original | Printed page | Actual body | PDF cardinality | Selected XSD cardinality | Schema authority | GitHub render |
|---|---:|---|---|---|---|---|
| V1.0 | p15 | §1.30, Table 30 | 0:* (both) | 0:1 (both) | official_release | [43029589455](https://github.com/MarcLeinenDE/VDV301/actions/runs/43029589455) |
| V2.0 | p22 | §2.30, Table 30 | 0:* (both) | 0:1 (both) | official_release | [43029612445](https://github.com/MarcLeinenDE/VDV301/actions/runs/43029612445) |
| V2.1 | p24 | §2.30, Table 30 | 0:* (both) | 0:1 (both) | official_release | [43029633452](https://github.com/MarcLeinenDE/VDV301/actions/runs/43029633452) |
| V2.2 | p25 | §2.30, Table 30 | 0:* (both) | 0:1 (both) | official_release | [43029726595](https://github.com/MarcLeinenDE/VDV301/actions/runs/43029726595) |
| V2.3 | p25 | §2.30, Table 30 | 0:* (both) | 0:1 (both) | official_release | [43029753257](https://github.com/MarcLeinenDE/VDV301/actions/runs/43029753257) |
| V2.4 | p27 | §2.30, Table 30 | 0:* (both) | 0:1 (both) | candidate_integration | [43029777221](https://github.com/MarcLeinenDE/VDV301/actions/runs/43029777221) |

- **V1.0** — official original PDF: `https://www.vdv.de/301-2-1-sds.pdfx`, SHA-256 `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf`, 892769 bytes; actual body printed p15 §1.30 **Table 30**, both Announcement and FareZone 0:*; original PNG SHA-256 `c3b1a0dd568d237aa96a07ec2888b21b2c3ea005a157cbd5ab811cf06bc1efd8`, run `43029589455`, artifact `13860986360`. Exact `IBIS-IP_common_V1.0.xsd` Git blob `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`, JourneyStopInformationStructure starts line 356, Announcement line 367, FareZone line 377: each `minOccurs="0"`, no maxOccurs (default 1). Selected authority `official_release`, Enumerations V1.0.
- **V2.0** — official original PDF: `https://www.vdv.de/301-2-1-sds-v-2-0.pdfx`, SHA-256 `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088`, 946088 bytes; actual body printed p22 §2.30 **Table 30**, both Announcement and FareZone 0:*; original PNG SHA-256 `7a4a8c44c8f4ee279c67bd4eecc6c9b0b19359224ecb421037b676a4baa60dbc`, run `43029612445`, artifact `13860711734`. Exact `IBIS-IP_common_V2.0.xsd` Git blob `8608e3dcd665c197c34da7f6ec6af5a3758da164`, JourneyStopInformationStructure starts line 362, Announcement line 373, FareZone line 383: each `minOccurs="0"`, no maxOccurs (default 1). Selected authority `official_release`, Enumerations V2.0.
- **V2.1** — official original PDF: `https://www.vdv.de/301-2-1-sds-v2-1-commonstructure-enums.pdfx`, SHA-256 `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32`, 1274051 bytes; actual body printed p24 §2.30 **Table 30**, both Announcement and FareZone 0:*; original PNG SHA-256 `d1647155d5a5207786eb91f9aa3cab6ae0c2791b8f58be45b183a513e6bfdc87`, run `43029633452`, artifact `13861146672`. Exact `IBIS-IP_common_V2.1.xsd` Git blob `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e`, JourneyStopInformationStructure starts line 361, Announcement line 372, FareZone line 382: each `minOccurs="0"`, no maxOccurs (default 1). Selected authority `official_release`, Enumerations V2.1.
- **V2.2** — official original PDF: `https://www.vdv.de/301-2-1-sdes-v2-2-commonstructure-enums.pdfx`, SHA-256 `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`, 1411558 bytes; actual body printed p25 §2.30 **Table 30**, both Announcement and FareZone 0:*; original PNG SHA-256 `2ebf0c6f83c5c86acb9ce7875d36967d61d006476b7bb044479972f30ef9cf03`, run `43029726595`, artifact `13860087462`. Exact `IBIS-IP_common_V2.2.xsd` Git blob `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`, JourneyStopInformationStructure starts line 365, Announcement line 376, FareZone line 386: each `minOccurs="0"`, no maxOccurs (default 1). Selected authority `official_release`, Enumerations V2.2.
- **V2.3** — official original PDF: `https://www.vdv.de/301-2-1-sdes-v2-3-commonstructure-enums.pdfx`, SHA-256 `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`, 793521 bytes; actual body printed p25 §2.30 **Table 30**, both Announcement and FareZone 0:*; original PNG SHA-256 `61a57d7bd6194de20519348928b77733dfc5f4cdcb7dd8ab53fd38fa4528742c`, run `43029753257`, artifact `13861042204`. Exact `IBIS-IP_common_V2.3.xsd` Git blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`, JourneyStopInformationStructure starts line 415, Announcement line 426, FareZone line 436: each `minOccurs="0"`, no maxOccurs (default 1). Selected authority `official_release`, Enumerations V2.2.
- **V2.4** — official original PDF: `https://www.vdv.de/301-2-1-sde-v2-4-commonstructure-enums.pdfx`, SHA-256 `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`, 1689647 bytes; actual body printed p27 §2.30 **Table 30**, both Announcement and FareZone 0:*; original PNG SHA-256 `b1a79f174ca8e52b15defa7c1dc3d9850cacd73f47d4093ebf7f52f2d918569d`, run `43029777221`, artifact `13860357046`. Exact `IBIS-IP_common_V2.4.xsd` Git blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`, JourneyStopInformationStructure starts line 415, Announcement line 426, FareZone line 436: each `minOccurs="0"`, no maxOccurs (default 1). Selected authority `candidate_integration`, Enumerations V2.4.

The visible target for every version is **Table 30: Description of JourneyStopInformation**, not a table number inferred from TOC or history. The actual body headings are `1.30` for V1.0 and `2.30` for V2.0–V2.4.

## Falsification attempts

1. **Could `0:*` be a special option/choice notation?** No: both entries appear as ordinary unprefixed rows in Table 30, without a choice dash or grouping. Nearby `StopAlternativeName` and `Connection` are likewise 0:* in the PDF and actually `maxOccurs=unbounded` in the XSD; `Platform` is 0:1 in both, corroborating the local notation.
2. **Could the XSD children be repeatable via a surrounding choice or group?** No: each exact selected `JourneyStopInformationStructure/xs:sequence` declares `Announcement` and `FareZone` separately as `xs:element minOccurs="0"`, with **no maxOccurs**. The XML Schema default is 1. Repeated occurrences violate the content model. This scope applies to the same JourneyStopInformation instance.
3. **Wrong Common release/dependency?** No: each XSD source blob was independently inspected. The official Common V2.3 XSD includes Enumerations **V2.2**, not a hypothetical V2.3 Enum. V2.4 is a separately selected candidate/integration XSD, and its matching official PDF does not make the XSD official.
4. **Could a later release have corrected it?** All intermediate V2.0–V2.3 and most recent V2.4 PDFs are independently affected. As of 2026-11-11 the VDV public catalog still lists Common publications through V2.4, and the official GitHub release list through V2.3, with [upstream PR #31](https://github.com/VDVde/VDV301/pull/31) still open and not merged. No corrected successor verified in the audited corpus. Do not claim a future revision cannot exist.
5. **Could language variation explain the discrepancy?** The original pages carry English XML member names and description, with German-origin document context; the same two 0:* values appear in every actual visible table. No independently published alternate-language Common source was inferred.

## Validation and SDK consequence

- Preserved V1.0 executable evidence `EV-117` / `EV-135` includes positive one-occurrence and negative two-occurrence checks for each field. **This block re-read six exact XSD declarations and did not claim fresh executable sample tests for all later versions.**
- A second Announcement or FareZone under the same JourneyStopInformation must be **XSD FAIL** in the selected Common profile; the failure may be decorated with `DRCOM10-004` and the precisely versioned PDF discrepancy. Never convert FAIL into PASS, introduce a repetition waiver or modify source XSD bytes.
- The runtime mapping stays `reviewed_not_implemented`; no matcher code is added.
- The source of publisher error remains undetermined; the exact XSD is the selected executable authority irrespective of whether future VDV correction changes the PDF or the XSD.

## Closure and next item

Once synchronized and fully gated: **88 / 192 unique finding locators complete**, **88 original bodies independently verified**, **88 version-boundary records verified**, **104 open**. Next unique finding **`DRCOM10-005`**. A terminal state requires the substantive schema-audit-validation and the separate final HEAD handoff integrity workflow to be SUCCESS; `CURRENT_STATE.json` alone is the continuation authority.
