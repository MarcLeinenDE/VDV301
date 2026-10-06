# Source-locator review — DR3011-002 — 2026-10-06

Status: **complete / visible-body verified / documentation terminology defect confirmed**.

## Finding

VDV 301-1 V1.0 uses stale/conceptual SystemManagement identifiers that do not match the concrete operation terminology in VDV 301-2 V1.0.

## Part 1 visible evidence

Official source:
- source ID: `VDV301-1_V1.0_DE`
- SHA-256: `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2`
- printed page: **11**
- visible anchor: **3.2 Begriffe / Abbildung 3: Einordnung der Begriffe Gerät, Dienst und Operation**

The visible SystemManagementService example uses:
- `GetDeviceState`
- `GetSystemStatus`
- `SubscribeDeviceStatus`
- `SubscribeSystemStatus`
- `UnsubscribeDeviceStatus`
- `UnsubscribeSystemStatus`

Exact-byte visual evidence:
- run `33725750019`
- artifact `9881897572`
- page-11 PNG SHA-256 `16fe0129866d3ca79ea64f047354fd2ea90c824e18e06332581e5b3d547d4bef`

## Part 2 visible cross-check

Official source:
- source ID: `VDV301-2_V1.0_DE`
- SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`
- printed page: **67**
- visible anchor: **7.3.1 Operationen des SystemManagementService**
- visible table: **Tabelle 31 Beschreibung von Operationen des SystemManagementService**

The visible operation table uses:
- `GetDeviceStatus`
- `SubscribeDeviceStatus`
- `UnsubscribeDeviceStatus`
- `GetServiceStatus`
- `SubscribeServiceStatus`
- `UnsubscribeServiceStatus`

Exact-byte visual evidence:
- source-pin run `33752224704`
- artifact `9892036202`
- page-67 PNG SHA-256 `2241db5cef5651ee67e2fd80bd1db142df53b00ed13c5817f8c67139c4770bfe`

The live PDF screenshot endpoint cache-missed for both documents during this review. Both locators were therefore verified through exact-byte GitHub Actions artifacts in accordance with the mandatory fallback rule.

## XSD corroboration

Selected historical schema:
- file: `IBIS-IP_SystemManagementService_V1.0.xsd`
- Git blob: `2d32630a0f1981e980e6a466e3f6a69136410f24`
- lines 8–37 contain `SystemManagementServiceGroup` and the `GetDeviceStatusResponse` / `GetServiceStatusResponse` declarations.

This XSD is used here only as corroborating historical schema context. DR3011-002 remains `documentation_only`; this review does not promote the branch copy to independent official-release authority.

## Disproof attempt

No notation or compositor rule explains the naming difference. The Part 1 page is explicitly conceptual and refers the reader to Part 2 for operation/service details. Part 2 then gives the concrete SystemManagement operation table with the Status terminology. The historical schema context independently agrees on the GetDeviceStatus/GetServiceStatus response identifiers.

## Classification and SDK behavior

Confirmed PDF/documentation terminology defect / stale identifier after rename.

- XML/XSD validity behavior: **unchanged**
- runtime matcher: **not applicable**
- SDK behavior: **informational only**
- alias generation for stale Part-1 names: **forbidden**
- concrete operation identifiers follow the selected Part-2/XSD context.
