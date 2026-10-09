# DR3011-002 — independent German/English V1.0 SystemManagement terminology boundary (2026-10-09)

**Status: scope verified / gate pending.** Existing finding retained, no duplicate identity. The affected artifact is the conceptual **VDV 301-1 V1.0 Part1 example in both languages**, not the concrete Part2 V1.0 operation tables. `confirmed_pdf_defect`, `contextual_only`, `sdk_behavior=info`, `runtime_match=not_applicable` remain.

## Exact visible-body contrast

| Publication | Visible source-body anchor | Exact names | Role |
| --- | --- | --- | --- |
| Part1 V1.0 **DE** official original, SHA256 `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2` | Printed p11, §3.2 Begriffe, Abbildung 3 / SystemManagementService example | `GetDeviceState`, `GetSystemStatus`, `SubscribeDeviceStatus`, `SubscribeSystemStatus`, `UnsubscribeDeviceStatus`, `UnsubscribeSystemStatus` | **Affected** conceptual documentation |
| Part1 V1.0 **EN** official separately issued translation, SHA256 `508cb52a9d9d459461954d46618d7b62a0ab9dc5698ef24e97fca2c458c551e4` | Printed p11, Example 1 / Figure 3 | Same stale/conceptual names as DE; page was personally visually checked after byte-pinned render | **Affected** translation; German original governs if inconsistent |
| Part2 V1.0 **DE** official original, SHA256 `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75` | Printed p67, §7.3.1 Operationen des SystemManagementService, Tabelle 31 | `GetDeviceStatus`, `GetServiceStatus`, `SubscribeDeviceStatus`, `SubscribeServiceStatus`, `UnsubscribeDeviceStatus`, `UnsubscribeServiceStatus` | **Not affected**, normative-terminology comparison reference |
| Part2 V1.0 **EN**, SHA256 `e3bbfa9236fbbf5cddcf18bbcfd753b2c01516436e37d9b7d96a5b7c23cf80a7` | Printed pp89–90, actual body §9.10.1 Operations of the SystemManagementService, **Table 110** (p89 first GetDeviceStatus row, p90 continuation) | Same concrete Status-based operation names as German Part2 | **Not affected**, independently checked translated reference |

PDF source and page evidence:
- Part1 EN official URL <https://www.vdv.de/301-1ses.pdfx>, first pin run **37906414201**; strict exact-byte render **37906694433**, artifact **11603974595**, digest `sha256:90e2fe86638602714e0a24b4f8b2c42f77586d6a1b0f4730a2286ca06689ce16`, visible p11 PNG `83cb92ecee31b4b618b839c70386093bb0af7659d64e75bf68577ea6cd9e4889`. Rendered original p11 inspected directly, including all six operation labels.
- Part2 EN official URL <https://www.vdv.de/301-2ses.pdfx>, previously independently pinned source run **37895410420**; exact-byte render **37912352625**, artifact **11607067999**, digest `sha256:51aa36c980aba1179f2dca01d89459334ab995661baa1f7353a96a68add927f6`. Visible p89 PNG `2730117d4cacae6ee5717dfff4778e822bd0737a7cc71a404a47fede0eafdf35`; p90 PNG `b96ce25f700a7f45da21bb1fc4ad2d593e2a5768fdd67b80a0d092b8f36f6726`. Both inspected directly, including table heading/start, continuation and rows.
- Historical DE original byte-pinned source/visible-body verification is recorded in `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_DR3011_002_2026-10-06.md`: Part1 DE p11 render 33725750019; Part2 DE p67 source-pin 33752224704. The historical visual records are retained, not rewritten.
- Historical selected schema `IBIS-IP_SystemManagementService_V1.0.xsd`, blob `2d32630a0f1981e980e6a466e3f6a69136410f24`: `SystemManagementService.GetDeviceStatusResponse` and `SystemManagementService.GetServiceStatusResponse` corroborate the table. This branch copy is **not** independently promoted to an official released XSD authority.

## Lower and upper boundaries

The official Part1 publication index and canonical pinned corpus checked for the immediately preceding DR3011-001 bilingual boundary contain **Part1 V1.0 German original and English translation**, with no earlier published Part1 predecessor and no independently confirmed newer corrected Part1 successor. The present finding extends its affected *language coverage* to both separately published V1.0 texts; it does not extrapolate to hypothetical newer versions.

Part2 DE/EN V1.0 are contemporary **unaffected control publications**, not first-corrected successors. A language translation can have different pagination (§7.3.1/Table31 DE versus §9.10.1/Table110 EN), which must not be conflated. The German original has priority over the English translation where inconsistent.

## Counter-evidence / disproof

The Part1 passage is explicitly an illustrative/conceptual example and points to Part2 for technical service/operation details. The discrepancy cannot establish that alias XML roots were ever defined, or that there was an actual historical **rename** event. It is not an inconsistency within the concrete Part2 operation tables. This finding identifies the risk of implementing the illustrative Part1 names as actual operations and disallows that inference.

No candidate/official authority promotion, XSD rewrite, optionality conversion, runtime matcher, provider failure, false-positive validation, or XML alias was performed.

## SDK and progress

Selected Part2/XSD profile controls actual XML validation. For this documentation-only finding, SDK treatment stays informational, not an automated runtime trigger. One existing finding ID only: boundary **57/70 → 58/70 verified**, **12 remaining**, next `DR3011-003`. The complete full audit gate and final `terminal_clean` handoff still must succeed before beginning the next finding.
