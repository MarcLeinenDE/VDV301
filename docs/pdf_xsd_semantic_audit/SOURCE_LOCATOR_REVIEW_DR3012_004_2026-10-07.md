# Source-locator review — DR3012-004 — 2026-10-07

Status: **complete / visible-body verified / documentation cross-reference defect confirmed**.

## Finding

VDV 301-2 V1.0 points the `DeviceState` member to section `9.3`, although the referenced `DeviceStateEnumeration` is visibly section `9.4`.

## Visible source evidence

Official source:
- source ID: `VDV301-2_V1.0_DE`
- SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`

### Page 59 — erroneous reference

Visible body:
- section: `7.1.8 Datenstrukturen der Operation GetDeviceStatus`
- subsection: `7.1.8.2 Response`
- table: `Tabelle 13 Beschreibung DeviceManagementService.GetDeviceStatusResponseData`

The visible `DeviceState` row:
- cardinality: `1:1`
- type: `+DeviceStateEnumeration`
- description: `Angabe zum Gerätestatus (vgl. 9.3)`

EV-129 page-59 PNG SHA-256:
`1e0a9ee8be0fffcb6414c89ca4c02107deffd12ba5270319fcb71589335a17f7`

### Page 74 — what section 9.3 actually is

The same exact pinned PDF visibly shows:
- `9.3 DeviceClassEnumeration`
- `Tabelle 55 Beschreibung von DeviceClassEnumeration`

A fresh fallback render was generated from the exact PDF in source-pin run `33752224704`, artifact `9892036202`.
- PDF SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`
- fresh page-74 render SHA-256: `5e3e35656acba17390d1f3a6fa0151678f6392546a891f755edce3466b4955fd`

### Page 75 — correct target

Visible body:
- `9.4 DeviceStateEnumeration`
- `Tabelle 56 Beschreibung von DeviceStateEnumeration`
- values: `defective`, `notavailable`, `running`

EV-129 page-75 PNG SHA-256:
`4b95e3f8487f3e83ca30ebf0c722786c9906b0f1b0057fc05447864c8619e6e4`

## Disproof attempt

The reference cannot be explained by a table-number/page-number convention or a second DeviceState definition:

- the member explicitly names `DeviceStateEnumeration`;
- section 9.3 is visibly `DeviceClassEnumeration`;
- the immediately following section 9.4 is visibly `DeviceStateEnumeration`.

The cross-reference is therefore off by one section.

## Classification and SDK behavior

Confirmed documentation/navigation defect only.

- XSD authority: **not applicable to the defect**
- XML/XSD validity behavior: **unchanged**
- runtime matcher: **not applicable**
- SDK behavior: **no runtime diagnostic**
- no implementation alias, schema override or technical validation rule is derived from the wrong section number.

The finding is retained as traceable editorial evidence only.
