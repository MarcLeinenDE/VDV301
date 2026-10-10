# DR3012-007 — StopService incorrect "start" member description: DE-only V1.0 boundary (2026-10-10)

**Visible source proof complete, full gate pending.** Preserve existing finding ID, no XML-XSD change.

| Original published body | Field-level and enclosing description | Evidence |
| --- | --- | --- |
| **V1.0 German**, p63 §7.1.24.1 `Tabelle 21 DeviceManagementService.StopServiceRequestStructure` | Enclosing structure says `gestoppt wird`; member `ServiceSpecification` contradicts it with `zu startenden Dienst` | Existing original visible-body review `SOURCE_LOCATOR_REVIEW_DR3012_007_2026-10-07.md`, pinned EV129 original p63 PNG SHA256 `8b5d94ed59fef404b29af34cedb7218e9ae564fbc8f5abcf7ffca055739b2839` |
| **V1.0 English**, p69 §9.3.25 `Table45` | Already correctly says `stopped services` in the member and `stop` in the request | Run [38038947278](https://github.com/MarcLeinenDE/VDV301/actions/runs/38038947278), artifact11665042099 PNG `0a883b0bec59fb3d3cf1ef13bb49a85b0dc27802d11f3b1c9afa4cb19f3c1c21` |
| **Base V2.0 bilingual**, p98 §7.1.24 `Table26` | Already correctly says `stopped services`; trailing `Fehler! Verweisquelle konnte nicht gefunden werden.` is a separate cross-reference issue, **not** continued wrong Start/Stop semantics | Run [38038963374](https://github.com/MarcLeinenDE/VDV301/actions/runs/38038963374), artifact11664652708 PNG `5d45c5901ef5452868f48c7734b21a6302c568f4e0a313d6e28541a9e7be59cf` |
| **Base V2.1 bilingual**, p103 §7.1.26 `Table26` | Correctly `stopped services`, referencing VDV301-2-1 | Run [38038996070](https://github.com/MarcLeinenDE/VDV301/actions/runs/38038996070), artifact11665291907 PNG `af75f882cc630d8cbeeb60d68aed2e3fbb47675fc50e38624ddc3b86c99f801a` |

Each independent new PNG is from source bytes verified against `audit_registry/pdf_source_pins_v0.1.json` via mandatory fallback. Original visible body, not TOC/history, governs location.

**Active falsification:** The English original translation does **not** reproduce the German field error, and the very next bilingual Base2.0 member already uses the correct stop wording. Reading the V2.0 unresolved Word cross-reference as the same semantic error would conflate distinct failure modes. Later separate DMS V2.2 and V2.4 are not used to infer a corresponding StopService member table that was not independently verified.

**Assessment:** `confirmed_pdf_defect`, original German V1.0 only, pure editorial copy-paste contradiction. `sdk_behavior=info`, `runtime_match=not_applicable`; operation remains StopService, with no alias and no provider XML validation override. A manufacturer must still pass its actually selected official XSD separately.

Boundary progress **65/70 → 66/70**; four pending, next `DR3012V20-001`. Continue the same authorized five-pack after full gate + terminal handoff.
