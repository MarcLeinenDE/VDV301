# DRCOM10-001 — May 2017 Common document revision 1.1 versus exact official 2014-import V1.0 schemas

**Date:** 2026-11-03. **Finding:** existing frozen `DRCOM10-001`, one identity and one progress unit; no new IDs. **Provenance/authority:** public VDV source-document revision is **not** itself an executable XSD variant. Exact selected XSD and includes retain PASS/FAIL authority.

## Independently checked original sources and render proof

| Original | Official, SHA256/size-pinned source | Renderer/action and exact-original evidence |
|---|---|---|
| **COMMON_V1.0** – VDV-Schrift 301-2-1, May 2017, 36 pages, publication showing internal history **Version 1.1** | `https://www.vdv.de/301-2-1-sds.pdfx`; SHA256 `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf`; 892,769 bytes | Exact-byte pinned GitHub visual fallback [run 41625122454](https://github.com/MarcLeinenDE/VDV301/actions/runs/41625122454), artifact **13225488128**, archive digest `sha256:1e95263503e6698d83a2c0648e809f8d7a9a6109524df50d19e0fb07498c6080`; original pages 9,21,27–30 rendered at 160 dpi and visually inspected |
| **COMMON_V2.0** – first relevant officially tagged successor PDF VDV-Schrift 301-2-1, February 2018, 45 pages | `https://www.vdv.de/301-2-1-sds-v-2-0.pdfx`; SHA256 `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088`; 946,088 bytes | Exact-byte pinned GitHub visual fallback [run 41625549119](https://github.com/MarcLeinenDE/VDV301/actions/runs/41625549119), artifact **13225656338**, archive digest `sha256:91648f1f0bae7766501c15c90e453a95e9da0aa79dcbd067ff9af7b30c42c7f9`; original pages 15–17,29,35–39 rendered at 160 dpi and visually inspected |

Both GitHub renderers independently retrieved the exact official PDF and **hard-checked both SHA256 and byte size** against `audit_registry/pdf_source_pins_v0.1.json` before rendering. Every locator below is based on the **actual visible original body section, table caption, printed page number and adjacent content**, not the TOC, inferred sequence or searchable text alone. No original PDF or rendered images committed to GitHub.

## Actual original V1.0 body (May 2017; 1.1 data-document changes)

| Printed page / visible section | Exact visible evidence | PNG SHA256 (160 dpi) |
|---|---|---|
| **p. 9, §1.8 `Connection`, Table 8 `Description of Connection`** | `DisplayContent` **0:1**; `ExpectedDepartureTime` **0:1**; `ScheduledDepartureTime` **0:1** – all visibly distinguishable with proper line wrapping. The immediately following §1.9 DataAcceptedResponse is separate and belongs to other findings. | `e6c7650f67345ea4fccc62d31ee02e7ab205ab22405eaf08da3ef3987e45003d` |
| **p. 21, §1.54 `TripInformation`, Table 54 `Description of TripInformation`** | `AdditionalTextMessage` **0:\*** of `+InternationalTextType` and `RouteDirection` **0:1** of `+RouteDirectionEnumeration`. Related subsequent §1.55 and §1.56 tables are context, not the source of this finding. | `b178e7bfe25f3375fa34cdb13c9acf333ad88eab1f224ca5968e1a694f88f427` |
| **p. 27, §2.14 `IBIS-IP-VersionEnumeration`, Table 75** | The list visibly retains version **`1.0`**. This does **not** turn internal data/document Version 1.1 into protocol/XSD routing Version 1.1. | `406c7c0f225de740ef0b269e04dceef370ae6ef9c4159e49047151147cdf17d6` |
| **p. 28, §2.19 `RouteDirectionEnumeration`, Table 80** | Full enum `Forward`, `Backward`, `Clockwise`, `Counterclockwise`, `Other` is visibly part of the official May-2017 PDF. | `b03493f622a524e4cba16b894b88eea05be60d727048b3c8a9b2a241473cbe2d` |
| **p. 30, §3 `Versionshistorie / Version History` → §3.1 `Version 1.1`**, German bullet list and English continuation | Explicit additions/changes to `Connection.ScheduledDepartureTime`, Connection min:max information, `TripInformation.AdditionalTextMessage` type and `TripInformation.RouteDirection`, and new `RouteDirectionEnumeration`. The **German and English history tracks** on the *same pinned printed page* both state these changes; the English version carries some German residue, not new XML authority. | `899edf6db888a5e6f51a9eb25b483f07c5f77d0ecd8c8abdab8f364ebccec6eb` |

## Historical exact XSD authority (2014 official import)

Official upstream `VDVde/VDV301` initial import commit **`604a5a5c7608977e483072f7e450d7381cc182e4`** (2014-05-16), inspected by exact blob IDs and content:
- `IBIS-IP_common_V1.0.xsd` **`194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`** includes `IBIS-IP_Enumerations_V1.0.xsd`, requires `Connection.DisplayContent` (no `minOccurs=0`), spells `ExpectedDepatureTime`, has **no** `ScheduledDepartureTime` and **no** `TripInformation.RouteDirection`. Its `AdditionalTextMessage` is optional single `IBIS-IP.string`, not a repeating internationalized item.
- `IBIS-IP_Enumerations_V1.0.xsd` **`a9bea5bc73003ed91ded8519db06c32c4067831d`** has **no** `RouteDirectionEnumeration`.
- The same exact V1.0 blobs were independently found on `dev/schema-integration`. No candidate/official distinction arises for the selected **V1.0** family.
- Historical executable evidence **EV-117**, run `33279461529`, and closeout **EV-135** run `33850713729` validate the selected V1.0 boundary: `DisplayContent` required, historical spelling accepted and the hypothetical V1.1-only fields not silently recognized. This block does **not** claim that XSD-validity is determined by PDF tables.

## First independently verified successor V2.0, not a retroactive fix

Official upstream release tag **`VDV-301-2.0`** includes the exact V2.0 family:
- `IBIS-IP_common_V2.0.xsd` **`8608e3dcd665c197c34da7f6ec6af5a3758da164`**, includes V2.0 Enumerations; `DisplayContent minOccurs=0`, corrected `ExpectedDepartureTime`, `ScheduledDepartureTime minOccurs=0` and `TripInformation.RouteDirection minOccurs=0` are independently verified in the XSD bytes.
- `IBIS-IP_Enumerations_V2.0.xsd` **`27e3c183b00381d959622d13c10543123af8eef6`** includes `RouteDirectionEnumeration`.
- **p. 16 §2.8 Connection, Table 8:** all corresponding corrected fields/cardinalities visibly present; original PNG SHA `383647858a6bdb5c1826ced25954e5f0d9aa4ad9c3bc31eeb85bb8ad2daa4238`.
- **p. 29 §2.57 TripInformation, Table 57:** `RouteDirection 0:1`, `AdditionalTextMessage 0:*` `+InternationalTextType` present; PNG `b12ff4e77d8c364b23f301320a12431951086f42cec3d0eddea8ff235fcd31e3`. Note **separate CE-005**: the V2.0 XSD still allows at most one AdditionalTextMessage, notwithstanding PDF 0:*. **Do not claim every 1.x/2.0 inconsistency is fixed.**
- **p. 36 §3.20 RouteDirectionEnumeration, Table 84:** corresponding enumeration exists; PNG `6d77711683f059cdbe5e3a8fdf322560b10e3ae056b79b547671bc45c9f58a16`.
- **p. 38 §4 Versionshistorie / Version History, §4.1 Version 1.1 and §4.2 Version 2.0:** visible historical distinction, V1.1 data-model additions remain recounted under 1.1; specific 2.0 updates follow; PNG `dd54cd035fafaf1782c9c64403188fa7bfdf962e2bdfb90c09bbc799f19bc297`.
- **p. 39 §4.2.3 Textliche Korrekturen / Textual Corrections:** V2.0 history explicitly states `XSD-Versionen 1.0 und 1.1` / `XSDs of version 1.0 and 1.1` have the `ExpectedDepatureTime` typo fixed in `IBIS-IP_common_2.0.xsd`; PNG `fdab713538450de4a185f0b9ab7bd01406d2744bf1003ca1e16fa7956d54c8cd`.

**Crucial uncertainty and correction to earlier wording:** The **official V2.0 PDF explicitly refers to an XSD 1.1**. Accordingly, the earlier unqualified historical semantic sentence **“no Common V1.1 XSD exists”** is too strong. This review independently found **no `IBIS-IP_common_V1.1.xsd` or `IBIS-IP_Enumerations_V1.1.xsd`** at official upstream `master`, upstream official `VDV-301-2.0` tag, or working branch `dev/schema-integration` (each GitHub path returned 404); no exact officially attributable V1.1 schema bytes, release tag/profile or dependency closure was verified. Absence from those checked collections **does not establish historical nonexistence**, especially given the PDF's express historical reference. Correct finding wording is: **“A V1.1 XSD is referenced in official PDF history but is not an independently verifiable selectable XSD profile in the audited official repository snapshots.”** Never invent a V1.1 profile or replace V1.0 with V2.0.

## Independent historical boundary and falsification

- **Earliest verifiable affected route:** 2014 official imported V1.0 XSD; **May-2017 official Common V1.0 PDF internally revised to data definition 1.1** and contradicting that exact V1.0 executable family. No earlier separately pinned Common V1.0 PDF original was available for an independent prior-publication visual comparison; do not invent predecessor or silently extend the PDF claim before 05/2017.
- **First verified corrected executable successor for this finding's identified fields:** Official **V2.0** Common/Enumerations family and matching **February-2018 V2.0 PDF**. The specifically recorded `ScheduledDepartureTime`/`RouteDirection`/`RouteDirectionEnumeration` inclusion, corrected `ExpectedDepartureTime` and `DisplayContent` optionality align there. No carrying of this *specific* 1.1-vs-V1.0 route defect into V2.0; other independent V2.0 PDF/XSD differences retain their own frozen IDs (e.g. `CE-005`).
- **Language:** May-2017 one pinned document has English structures/tables and both German/English version-history bullets on p30; successor V2.0 is bilingual. The original source's printed language sections were checked distinctly; no inferred independent unpublished translation or earlier issue.
- **Falsified**: page30 Version 1.1 does *not* mean protocol `IBIS-IP-VersionEnumeration` automatically 1.1 (p27 says `1.0`). **Falsified**: all Version 1.1 PDF additions automatically valid against V1.0 XSD (exact bytes say no). **Falsified**: an old XSD 1.1 *never existed* (V2.0 official PDF itself mentions it; absence of its bytes in current audited GitHub does not disprove historical existence). **Falsified**: the V2.0 first corrected successor makes old V1.0 XML valid (no latest-wins routing). **Falsified**: the AdditionalTextMessage V2.0 cardinality gap is also fixed here (separate `CE-005`).
- Existing `CE-005` owns AdditionalTextMessage type/repeatability as a separate affected-version issue, not duplicated. Other Common V1.0 spelling/cardinality findings retain their IDs.

## SDK and remediation boundaries

Classification `cross_artifact_mismatch`, `version_routing_issue`, `selected_xsd`, `sdk_behavior=error_with_advisory`. Runtime match remains **reviewed, NOT implemented**; **77 reviewed** runtime mappings continue to be descriptive only. For selected strict V1.0 schema on an instance invalid due to PDF-revision-only fields, SDK must return **FAIL** under exact V1.0 source and may add explanatory advisory. No change to XSD bytes, no alias/normalization, no synthetic 1.1 or upgrade to 2.0. Correction to historical semantic evidence/DE-EN diagnostic wording is provenance precision only.

This closes **one** new locator/body/historical-boundary evidence group **84→85/192 (107 remain)** only when all registries, semantic-blob pins, full schema gate and terminal-final HEAD checks pass. Next canonical semantic ID: **`DRCOM10-002`**.

## Supporting record references

- Prior independent frozen fresh-read `docs/pdf_xsd_semantic_audit/deep_read/COMMON_V1.0.md` and `.../COMMON_V2.0.md`.
- Historic revalidation `docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_COMMON_V10_2026-09-04.md`.
- GitHub pinned official source registry and pin file.
- Fresh exact pinned byte/visual artifacts: V1.0 run **41625122454**, artifact **13225488128**; V2.0 run **41625549119**, artifact **13225656338**.
- Independent checked official XSD blobs from `VDVde/VDV301` as pinned above, and current `dev/schema-integration` V1.0 copies.
