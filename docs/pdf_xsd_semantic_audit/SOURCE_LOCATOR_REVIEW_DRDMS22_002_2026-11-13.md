# Source-locator review — DRDMS22-002 — 2026-11-13

**Independent result:** Confirmed **documentation-only** erroneous table-of-contents numbering, confined to the original published **DeviceManagementService V2.2** PDF among the checked versions. One existing finding ID, no XSD changes, no XML runtime validity change. V2.1 has correctly matched section numbers and the official published V2.4 PDF has the correct 2.33–2.35 entries. V2.3 has an integration XSD only; no official standalone DMS V2.3 PDF was registered or independently verified.

## Original V2.2 source and actual visible body — not inferred from TOC

| Surface | Actual printed page and visible location | Direct evidence |
| --- | --- | --- |
| **Offending source** | Original **printed p7**, **`Inhaltsverzeichnis / Content` continuation**; no table caption | TOC lists `1.33 Data Structures of Operation GetUpdateHistory`, `1.33.1/.2 Request/Response`; `1.34 FinalizeUpdate`, `1.34.1/.2`; `1.35 FinalizeAllPendingUpdates`, `1.35.1/.2` |
| Neighboring TOC control | Same p7 | Preceding `2.32 RetrieveUpdateState` and its `2.32.1/.2` entries are correctly numbered. Wrong shift is localized to the following three operation sections, not a deliberate alternative document hierarchy |
| TOC continuation | Original **printed p8**, `Inhaltsverzeichnis / Content` continuation | Next top-level entry `2 Versionshistorie / Version History`, showing that `1.33`–`1.35` do not denote a separate consistent top-level-1 hierarchy |
| **Correct target** | Original **printed p29**, actual visible heading **`2.33 Data Structures of Operation GetUpdateHistory`** and **`2.33.1 Request`, `2.33.2 Response`** | Real section identifier 2.33; response context in actual Table34, UpdateHistory body in Table35 (not a TOC-inferred heading) |
| **Correct targets** | Original **printed p30**, actual visible headings **`2.34 Data Structures of Operation FinalizeUpdate`** and **`2.35 Data Structures of Operation FinalizeAllPendingUpdates`** | Real subsections `2.34.1/.2` and `2.35.1/.2`, same operation names; visible FinalizeUpdate structure Tables37/38; no XML identifier differs |

### Strongest disproof attempt

An alternative intentional hierarchy, an OCR/text-layer extraction error or a genuine `1.33` section would have explained the difference. The actual page is rendered from SHA-pinned original bytes and visibly prints `1.33`, `1.34`, `1.35`; its immediately preceding `2.32` and immediately following top-level `2 Versionshistorie` rule out a consistent separate hierarchy. Independently visible **body** headings 2.33–2.35 and all six 2.33.x–2.35.x member headings contradict the TOC. Operation *names* are identical and correspond to selected DMS service group: only the navigation labels are wrong.

## Original source / visual hash pins

Each original PDF was downloaded by GitHub Actions via the official VDV source URL; the project's `tools/render_vdv_pdf_pages.py` checks exact original **SHA-256 AND byte size** from the canonical PDF pins before rendering. Required original page images were **actually visually inspected**; these are not just extracted text, OCR, TOC inference or adjoining-version headings.

| Official document | Exact PDF SHA-256 / size | Pinned Github fallback run / artifact | Verified PNG page SHA-256 |
| --- | --- | --- | --- |
| **V2.1 Basic Services** `VDV301-2_BASE_V2.1` | `685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a` / **2671005** bytes | [run 43430528486](https://github.com/MarcLeinenDE/VDV301/actions/runs/43430528486), artifact **14039261564** | TOC **p12** `77ca3ccaea9ca5dd6a92cfe6a63e682d0b4ea113c63ce51c4e665bb8abe40f8f`; body **p110** `71590d242ddb6c73c5d73467c3a26c25b64475a65624a1e87270448dd7ab8704`; body **p111** `e6b0f8eec39f12b244b676a1ed74ca92a641ce551a9596b570799cfba7a31426` |
| **V2.2 DeviceManagementService** `DMS_V2.2` | `72cef70072e5f586ba57e7886657b1808a87ec7a6c4f39a519263105eb83f97e` / **1173719** bytes | [run 43430200687](https://github.com/MarcLeinenDE/VDV301/actions/runs/43430200687), artifact **14039321817** | TOC **p7** `7ba7a0d7a676b099c5572e7eecfa44f2a0f25e49f16f991dbdca8976a23f14fc`; TOC **p8** `67a272779832689f83a690b77b6be500719c38434b89ead4f5fabc39d947e1c1`; body **p29** `b74925c5220df036e53b76c12be1dd6aecffca17a0cac4cfab48664873976617`; body **p30** `4e3b5f36e5c1895f4738ab7c4150b6476f525f442e6ec2231ff40785d64b9b39` |
| **V2.4 DeviceManagementService** `DMS_V2.4` | `347b9d5684b653d241370884a0163b0154c3028df23ad9cc61318275de1b17fd` / **1298127** bytes | [run 43430886725](https://github.com/MarcLeinenDE/VDV301/actions/runs/43430886725), artifact **14039251920** | TOC **p6** `b10e637ffc60fecf715e14e02d4bf6d44beffe8684a048e21a14065d6de3834d`; TOC **p7** `fb1d73419fe8294adb00455117f32d45da9c42e82fc04d5fd6b786441b985ab3`; body **p28** `75d481b4dc8d300560950a1a3a77b4f3d23f01a6aab04531d8255e3cda22c95e`; body **p29** `815a6dc2f176b33b9b2a7fe5a131e528311e207f3260ce04408db2d2238e1f37` |

## Exact historical version boundaries and executable authority

| Version | Direct checked source and authority | Boundary |
| --- | --- | --- |
| V1.0, separate official German/English publications | Both registered separately; exact official historical DMS XSD `IBIS-IP_DeviceManagementService_V1.0.xsd`, Git blob `602a963f91000d0d39e3c271bacb3c7aba73e6d4`, independently checked against official `VDVde/VDV301@VDV-301-1.0` | **Not applicable**: this exact selected service XSD contains none of the three newer operation declarations. No claims that the V1.0 DE or EN TOC used a particular later section number |
| V2.0, official bilingual Basic Services | Exact official DMS XSD `IBIS-IP_DeviceManagementService_V2.0.xsd`, Git blob `74189e0da65563eeb084ec2f3c400e9668d1ee1a`, upstream `VDV-301-2.0` | **Last non-applicable predecessor**: same three operations not yet declared |
| **V2.1, official bilingual Basic Services** | Original pinned TOC p12 **`7.1.42 GetUpdateHistory`, `7.1.43 FinalizeUpdate`, `7.1.44 FinalizeAllPendingUpdates`**, all Request/Response subsections correct; original body p110–111 uses same identifiers; official release XSD `IBIS-IP_DeviceManagementService_V2.1.xsd` blob `191b43e01cdaba14b247725689a913c244a67eed` with all operations in `DeviceManagementServiceGroup` lines89–94 | **Last existing, nonaffected operation-bearing predecessor**. No 1.x vs 2.x drift |
| **V2.2, official standalone DMS** | Pinned official TOC p7 **`1.33`**, **`1.34`**, **`1.35`** + six 1.x subsection references vs actual p29/p30 `2.33`, `2.34`, `2.35` + 2.x; selected exact official XSD `IBIS-IP_DeviceManagementService_V2.2.xsd` blob `c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d` service group lines73–78 | **First and last verified affected publication** |
| V2.3 | Local `IBIS-IP_DeviceManagementService_V2.3.xsd` blob `5fe444cf6d10462cc23fd159eb963abbec42248f` is **integration comparison only**; no official standalone DMS V2.3 PDF in canonical publication registry | **Documentation status unverified**; no inferred defective or corrected V2.3 publication |
| **V2.4, official standalone DMS PDF** | Exact official PDF TOC p6/p7: `2.33`, `2.34`, `2.35` + correct subsections; original body p28/p29 same section identifiers. Selected `IBIS-IP_DeviceManagementService_V2.4.xsd` blob `d222dfd98b2be3777576388da7ace8f333d24c3f` is **candidate/integration only**, not an official released XSD | **First independently checked corrected official PDF successor**; out of affected scope. Official PDF is not an official strict 2.4 XSD authority |

The bilingual publications contain their technical operation headings/TOC in English (with German framework headings); **no separate second German technical table or separately published same-version German document is invented**. Distinct V1.0 original DE and EN publications were treated independently as registered controls.

## Finding identity, classification, SDK / evidence

- **Same existing ID:** `DRDMS22-002`, **not** an additional finding for each wrong subheading/version.
- **Classification:** `confirmed_pdf_defect`, `editorial_residue`, `documentation_navigation_error`, `documentation_only`, `no_runtime_effect`, `sdk_behavior=no_runtime_diagnostic`, `runtime_match=not_applicable`.
- **Exact historical XSD context:** V2.2 `DeviceManagementServiceGroup` declares `GetUpdateHistoryRequest/Response`, `FinalizeUpdateRequest/Response`, `FinalizeAllPendingUpdatesRequest/Response` at lines73–78; selected official V2.1 has them at lines89–94. Their operation names, types and request/response model are not changed by a PDF TOC prefix.
- **Executable tests:** no XML validity difference is claimed; executable new XML acceptance/rejection tests are **not applicable** to document-only numbering. Earlier EV-141 pinned V2.2 visual closure run33974702338 remains historical evidence, not relabelled as a new test.
- **No remediation:** XSD/dependency files and runtime SDK code unchanged. No operation alias `1.33`, no changed section-based router, no inference about V2.3 official PDF.
- **Registry synchronization:** semantic `version_scope` retained V2.2 (with proven historical boundaries), 1 complete unique new locator, 1 verified body entry and 1 verified scope-boundary entry, and all canonical state/SDK count mirrors move together from **97/192 to 98/192** after a gated atomic commit. Keep older 97/192 and legacy EV-141 snapshots untouched.
- **Required gates:** full schema-audit-validation and handoff-integrity on substantive `gate_pending` commit, independent `terminal_clean` commit, then both final-head checks. Only after green final HEAD add compact knowledge to private ai-mem via reviewed PR.
- **Next unique finding:** `DRDMS22-003` (not started).
