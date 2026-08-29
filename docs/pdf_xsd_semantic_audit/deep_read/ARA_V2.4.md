# AnalogRadioService V2.4 — Deep Read Pass 2

Status: independent source read and pinned-byte visual review complete; historical AnalogRadio findings intentionally remain unopened for reconciliation until after this freeze.

## Source and authority boundary

- Official publication: VDV-Schrift 301-2-19, AnalogRadioService V2.4, 01/2023.
- Verified official URL: https://www.vdv.de/301-2-19-sde-v2.4-analogradioservice.pdfx
- PDF SHA-256: `d0c8d8a3b8719c13b09f43ec98349d2e9b22d07fec0c9267bceff0812cbbc34c`.
- PDF size: `1009640` bytes.
- Pin run: `33269415752`.
- No `VDV-301-2.4` release tag exists in the official GitHub repository at this audit point.
- Current official upstream master does not contain `IBIS-IP_AnalogRadioService_V2.4.xsd`.
- Integration `IBIS-IP_AnalogRadioService_V2.4.xsd` blob: `48fb303b80936d2d762f0889ce0c359e04c16e5b`.
- That integration file entered via commit `c9c086ac07f7e9bdb271c54f7a274e3cf0d03749` (`Integrate public schema candidate files`) and remains candidate/integration material, not official-release authority.
- It declares `IBIS-IP_common_V2.3.xsd` as dependency; integration Common V2.3 blob is `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`.
- No latest-version substitution is permitted.

## Render/read evidence

- Exact pinned-byte render/text run: `33269472968`.
- Job: `99145237184`.
- Artifact: `9719652068` (`ara-v24-pinned-read`).
- Artifact digest: `sha256:06c2ce302b1b98d5bbe22265806ea605bbc2abe62327b8d809a0e27da19592a3`.
- PDF pages: `16`; all pages rendered at 120 dpi.
- Extracted full-text SHA-256: `de4be3a9282310cfccbca7244bfd5e85b04b493c34e74f99494cccc2c35e7fe5`.
- Targeted visible review: pages 1, 9, 10, 11, 12, 13 and 14, with the complete extracted text read across all 16 pages.

## Independence boundary

Historical AnalogRadio finding IDs and EV-105 were deliberately not used to construct the observation list below. Candidate/integration XSD content was used only as an explicitly provenance-limited comparison aid after document-internal observations had been identified. Historical reconciliation starts only after this freeze.

## Independent observations

### FR-ARA24-OBS-001 — SendTelegram Transmitter row contradicts the same official PDF

Page 11's `AnalogRadioService.RadioTelegramStructure` table names the last member `TransmitterType`, assigns it cardinality `1:1`, and gives type `TransmitterStructure`.

The same page visibly embeds a schema view that instead shows `Transmitter` with `minOccurs=0`. Page 12's structure diagram also names the member `Transmitter`, and page 13's complete XML example uses `<Transmitter>`. The official PDF is therefore internally inconsistent in both member name and cardinality before any external XSD comparison is applied.

The provenance-limited integration candidate agrees with the schema screenshot/example side: element `Transmitter`, type `TransmitterStructure`, `minOccurs="0"`. This candidate agreement can support executable testing later but does not promote the candidate to official V2.4 release authority.

### FR-ARA24-OBS-002 — SendTelegram URI example uses a different operation name

Section 2.5.1 is titled `URI for the Operation SendTelegram`, and the operation inventory on page 10 defines only `SendTelegram`. Nevertheless the visible URI example on page 13 ends in `/AnalogRadioService/SendFFSKTelegram`.

This is a documentation operation-name inconsistency. The page 13 XML example immediately below uses the root `AnalogRadioService.SendTelegram`, reinforcing that `SendFFSKTelegram` is not the operation name used elsewhere in this document.

### FR-ARA24-OBS-003 — URI example omits the scheme shown by its own template

Immediately before the concrete example, page 13 states the service URI form as `http://Host:Port/ServiceName/Operation`. The concrete underlined example is `192.168.1.2:8080/AnalogRadioService/SendFFSKTelegram` without `http://`.

This is retained as a documentation/example inconsistency. It is not treated here as proof of a runtime implementation defect.

### FR-ARA24-OBS-004 — AnalogRadioService misspelled in operation introduction

Page 10 visibly says `The AnlogRadioService has only one operation.` while the surrounding heading, operation tables and document consistently use `AnalogRadioService`. Documentation-only spelling error.

### FR-ARA24-OBS-005 — minor English editorial residue

Visible/document-text residue includes `pre-emtion` on page 8 and `contians`, `pre-amption`, and `BitrateEnumerationis` on page 12. These are grouped as non-executable editorial defects rather than inflated into separate semantic findings.

## Active falsification and rejected suspicions

1. **Rejected cover-page `Fehler` finding.** Text extraction exposes an isolated `Fehler` on page 1, but the exact pinned-byte render of page 1 contains no visible `Fehler`. It is not promoted.
2. **Rejected missing-response defect.** Page 10 explicitly says the `SendTelegram` response is `(not provided)`. The lack of a separate service response is therefore not independently treated as an omission merely because other VDV services have request/response pairs.
3. **Rejected official-V2.4-XSD inference.** The PDF's references point users to the VDV GitHub releases page, but there is no official `VDV-301-2.4` release tag and no current upstream-master AnalogRadio V2.4 service XSD. The integration candidate remains provenance-distinct.
4. **No choice-notation issue.** The page 11 `1:1` TransmitterType row is ordinary cardinality notation, not VDV leading-minus XML-choice notation.

## Fresh-read freeze result

Five independent documentation observations are frozen. The strongest observation is the page-11 Transmitter name/cardinality contradiction, which is already established internally by the official PDF's own table, embedded schema image, structure diagram and XML example. Three plausible false-positive/authority inferences were actively rejected. No XSD was changed. Historical AnalogRadio findings may now be reopened solely for deduplication and Evidence-Gate revalidation.
