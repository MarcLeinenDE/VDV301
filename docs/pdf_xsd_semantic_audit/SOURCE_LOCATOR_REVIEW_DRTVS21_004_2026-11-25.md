# Source locator review — DRTVS21-004

Date: 2026-11-25. Parent 09ba18ebc77cf03cf0eff93c70644b1f9372c7da. Existing frozen editorial finding; gate_pending.

## Result: independent PDF-body and version-boundary review

Four official VDV 301-2-16 TicketValidationService editions were checked from their previously pinned, rendered original documents. The canonical scope was V2.1-only; **all four spelling anomalies persist independently in V2.1, V2.2, V2.3 and V2.4**. This is one existing finding, not four new findings or a new executable issue.

| Printed body locator | Source wording | Correct context | V2.1 | V2.2 | V2.3 | V2.4 |
|---|---|---|---|---|---|---|
| p10 §2.2 DE, description of UnsubscribeCurrentLine | `Unscubscribe` | unsubscribe | present | present | present | present |
| p10 §2.2 DE, description of UnsubscribeVehicleData | `Unscubscibe` | unsubscribe | present | present | present | present |
| p15 §3.4.2, **Table 4** caption | `GetrazziaResponsetData` | header `TicketValidationService.RazziaResponseData` | present | present | present | present |
| p15 §3.7.2, **Table 5**, OperationErrorMessage description | `Error Respone` | 'Error response' in the adjacent Table 3 | present | present | present | present |

The DE p10 operation identifiers themselves correctly read `UnsubscribeCurrentLine` and `UnsubscribeVehicleData`. The EN p12 §2.2 overview was checked as a language control, rather than wrongly assuming German prose errors are duplicated in that track. Tables 3–5 p15 are the shared English technical-body track. Table 4's caption misspelling is not the actual schema type, and Table 5's typo is explanatory text rather than `OperationErrorMessage` element spelling. In all four documents the body sections and table numbers are **visually verified**, not derived from TOC or a sequence guess.

## Exact historical source and visible-body evidence

- V2.1 historical pinned render 34087850644, artifact 10005814043, ZIP sha256 8540e52a7866f8e034f2b5ed1496f2048173d183df58f7d9db42953c5ada579a; independently verified ZIP and p10/p15 PNGs: p10=2feebfb04a4751a9c881c65825ca2116502f9e5d3cef2e7bb2510eefcbc6479c, p15=a79fbb0fe541fb9af0131d64d13d9c1fc2f34a74aebdb513c9daae93bcd988c9; visually read original printed p10 §2.2 and p15 §3.4.2 Table 4/§3.7.2 Table 5. Exact PDF pin 676c05d7615f2f2ce95ec4eb085428cb0c970a4226809566e8968200df69988d.
- V2.2 historical pinned render 33255450850, artifact 9715657871, ZIP sha256 f6c313f94fe89ad14f6ed6114a0402efc543c31d4d2353a60dde05ea7f7d6e93; independently verified ZIP and p10/p15 PNGs: p10=3bd17dd87b8f5a9551a75c6354ccedd5e9d4fb6ea3b1775772c73c065ad3ee06, p15=349285137e542cc00d6cbcc2981647f87d33c62c7271342e2f6e05a328d9b2a6; visually read original printed p10 §2.2 and p15 §3.4.2 Table 4/§3.7.2 Table 5. Exact PDF pin 1915a1b12c24386e9a8ab5638fd88af6a442b5e42586b7b2d48f03e9a4205083.
- V2.3 historical pinned render 33258612417, artifact 9716575205, ZIP sha256 0cba4a211c323be415e26120eecda08c1453cce0df18e4ec373a108e22b56c74; independently verified ZIP and p10/p15 PNGs: p10=7e283aa0c680ad38febff4fe1d0e4bdb9dd92d5400749d6aada367391dec4fba, p15=7c2fd834cfe818549cb4cdc424f64ad2d8cd16e73db714585996a9e5a666046a; visually read original printed p10 §2.2 and p15 §3.4.2 Table 4/§3.7.2 Table 5. Exact PDF pin 74d9fd279e13f2661be24319c414ef9128b61c8fc6f30ea62b63f92f94ddbff4.
- V2.4 historical pinned render 33265061000, artifact 9718391355, ZIP sha256 03a308e9ac1f792ec074020a633e83ab58973e982b58e4731466f72781; independently verified ZIP and p10/p15 PNGs: p10=368eac4abc49840cb1ff04646b7cb2bbf6dd7d7fd109917a3fd9858b63824e6f, p15=6ad831b6b2ff9c516cc096c1482eb7c6fe9c2c88e8219b41a03c0b89a81e16ee; visually read original printed p10 §2.2 and p15 §3.4.2 Table 4/§3.7.2 Table 5. Exact PDF pin e7caca3de444b3eca15d539572cd4b896e56e5bb608b4827211b51be0ad56c51.

Each historical artifact has been retrieved from the existing GitHub Actions render evidence and independently checked locally against its archive SHA256. Both relevant PNGs per version have matching hashes and have been visibly inspected. The original official PDF source SHA256/size remains the prior pinned authority; the downloaded objects for this check are archived render ZIPs, **not new raw PDF downloads**. The interactive web PDF screenshots of V2.1–V2.3 cache-missed, so the exact-source pinned GitHub-render fallback was used; V2.4 also rendered directly. No fresh full-catalogue search is asserted; predecessor/successor scope is inherited from the independently verified earlier TVS audit.

## Exact schema authority; active disproof

- Official V2.1: `IBIS-IP_TicketValidationService_V2.1.xsd` blob `f6497e6469b82ee19b185c4de749d13a7ca60bed`; Common/Enums V1.0 exact historical route.
- Official V2.2: `IBIS-IP_TicketValidationService_V2.2.xsd` blob `5a4be2b2ba66860f035777ec0458dba0790880e1`; Common/Enums V2.2.
- Official V2.3: **the unchanged V2.2-named service, Common and Enums**, same blob as V2.2; not the separate V2.3-named candidate.
- V2.4: official PDF; full executable schema family `IBIS-IP_TicketValidationService_V2.4.xsd` blob `34b18b8c874e325dd923b366a72bb0ebee32e59e` is **candidate/integration** only. The incomplete upstream master service blob `291f41518fd48cd9dcc9f285cf9b5fec7dd72159` supports declaration inspection but is not a complete official release.

Exact selected service XSDs were re-read. V2.1/V2.2 (and V2.3 by identical official route) declare `TicketValidationService.GetRazziaResponseStructure`, `TicketValidationService.RazziaResponseDataStructure` and `OperationErrorMessage` with correct spelling. The complete V2.4 candidate and incomplete upstream master agree on the relevant declarations. None of the four PDF spelling errors is an XML element, type or valid alternative name. Strongest disproof considered: could the caption be intended as a literal XML type? Rejected by its same-page correct table header, exact XSD types and explanatory prose context; no schema alias or XML validation defect is established.

The V2.2/V2.3/V2.4 edits did not correct the four errors. No standalone predecessor before V2.1 or corrected successor beyond V2.4 was established in the previously verified official catalogue. Historical deep-read report and first-pass addendum retain their dated V2.1-only conclusions as historical evidence; the canonical scope is now V2.1–V2.4.

## Classification, SDK and next state

`confirmed_pdf_defect`; `documentation_spelling`; `contextual_only`; `no_runtime_diagnostic`. Existing finding ID `DRTVS21-004`, four editions / 16 recurring printed strings. DE and EN explanatory diagnostics expanded. No XSD changes, no runtime matcher, no aliases or validation-rule changes; no new targeted executable test required for pure editorial text, but full schema audit and handoff-integrity gates are mandatory.

Canonical registries updated in the same gate-pending commit, along with `00_START_HERE/CURRENT_STATE.json`: **126/192** complete, body-verified and version-boundary-verified, **66 remaining**. Next unstarted finding: **HDS-001**. Only mark terminal_clean after complete green gates.
