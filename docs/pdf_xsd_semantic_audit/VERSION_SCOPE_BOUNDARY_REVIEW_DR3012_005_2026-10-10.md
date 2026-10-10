# DR3012-005 — SystemManagementService ServiceStatus/SystemStatus version-language boundary (2026-10-10)

Status: **original-body verified; exact-HEAD full gate pending**. Existing finding identity retained.

| Official PDF | Inventory (visible body) | Contradicting detailed heading(s) | Evidence |
| --- | --- | --- | --- |
| V1.0 DE `VDV301-2_V1.0_DE` p67 Table31 | GetServiceStatus, SubscribeServiceStatus, UnsubscribeServiceStatus | p69 §7.3.6 SubscribeSystemStatus / §7.3.7 UnsubscribeSystemStatus | Existing visible-body review `SOURCE_LOCATOR_REVIEW_DR3012_005_2026-10-07.md`, pinned EV129 |
| V1.0 EN `VDV301-2_V1.0_EN` p90 Table110 | Get/Subscribe/UnsubscribeServiceStatus | p91 §9.10.5 **GetSystemStatus**, §9.10.6 SubscribeSystemStatus, §9.10.7 UnsubscribeSystemStatus; underlying Table113/114 GetServiceStatus | Run [38038067682](https://github.com/MarcLeinenDE/VDV301/actions/runs/38038067682), artifact 11663978950; p90 PNG `b96ce25f700a7f45da21bb1fc4ad2d593e2a5768fdd67b80a0d092b8f36f6726`, p91 `5dad76930429c141c66a00d7d2b22d8019e16317f9b0b645f7c99fb815fa68dc` |
| Base V2.0 bilingual `VDV301-2_BASE_V2.0` p103 Table36 | Get/Subscribe/UnsubscribeServiceStatus | p104 §7.3.5 GetSystemStatus, §7.3.6 SubscribeSystemStatus, §7.3.7 UnsubscribeSystemStatus, response Table39/40 GetServiceStatus | Run [38038078632](https://github.com/MarcLeinenDE/VDV301/actions/runs/38038078632), artifact11664756069; p103 PNG `a0c5dd3357837391448001125a0755ca21a6b9c59d09f4c412974fdcf83d8aa8`, p104 `067d363f1cb8ab2889a710ab42d68f4bea5512c29cf65398834eab4fce2385bc` |
| Base V2.1 bilingual `VDV301-2_BASE_V2.1` p116 Table61 | Get/Subscribe/UnsubscribeServiceStatus | p117 §7.3.5 GetSystemStatus, §7.3.6 SubscribeSystemStatus, §7.3.7 UnsubscribeSystemStatus, response Table64/65 GetServiceStatus | Run [38038111823](https://github.com/MarcLeinenDE/VDV301/actions/runs/38038111823), artifact11665100674; p116 PNG `57e9e69411b7267cd9422aa5305c4e86b79a51b472c062a13bd463df1bc45d72`, p117 `1a7c92e33ae01a04de621fa8a123941a478923dc020dc1dde532e6e80ad75db0` |

Original official PDF SHA256 and byte sizes are pinned in source registry. The interactive PDF screenshot backend cache-missed; mandated strict byte-verifying GitHub fallback rendered the actual table/heading body pages, which were visually inspected. V1.0 English is a separate translation whose target sections cannot be inferred from German numbering.

## Scope conclusion and falsification

Original V1.0 DE and EN affected. The very next dedicated bilingual Base V2.0 and V2.1 also affected, so V1.0-only scope disproven. No separate later SystemManagementService operation-table publication is recorded in the checked official catalog; Common Conventions and SystemMonitoringService are different publication subjects, not automatically evidence of correction or continued occurrence.

Strongest alternative: `SystemStatus` might be a separate valid operation or intentional alias. Refuted as an operation *inventory* interpretation by the same original pages: inventories uniformly name `ServiceStatus`, response roots and request prose name GetServiceStatus. The selected `IBIS-IP_SystemManagementService_V1.0.xsd` is byte-identical official blob `2d32630a0f1981e980e6a466e3f6a69136410f24` in release tags `VDV-301-2.0` and `VDV-301-2.1`; it supports GetServiceStatus response identifiers, **not** independently modeled subscription operation roots. Do not overclaim XSD proof for Subscribe/Unsubscribe operation names.

**Classification**: confirmed documentation/stale identifier/heading defect, no XSD validity consequence, no new XML alias or SDK runtime matcher. Correct selected-XSD PASS/FAIL unaffected; no provider FAIL solely for PDF heading. `sdk_behavior=info`; `runtime_match=not_applicable`.

Version-boundary registry: **63/70 → 64/70**, pending **6**, next `DR3012-006`. Updated five-finding workflow permits continuing after independently verified scope expansions once this exact finding passes full gate and terminal handoff. No cross-finding effect established.
