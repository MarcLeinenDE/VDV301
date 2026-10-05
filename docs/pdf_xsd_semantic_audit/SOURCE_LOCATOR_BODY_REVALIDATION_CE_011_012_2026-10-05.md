# Visible-body source-locator revalidation — CE-011 / CE-012

Date: 2026-10-05  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`

## CE-011 — Connection TransportMode / ConnectionMode cardinality

### Negative control: Common V2.1

The current scope correction explicitly excludes V2.1. The live renderer cache-missed printed page 17, so the exact-byte pinned artifact was used:

- run `33393002497`
- artifact `9758203545`
- PDF SHA-256 `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32`
- printed page 17 render SHA-256 `cc088c1c95866b1109e7529ad0885ea18217012c4c2ce5ff210e0c33244ea8ec`

The visible **2.8 Connection / Table 8** body shows `TransportMode 0:1` and no `ConnectionMode` row. This confirms that V2.1 is not affected.

The exact selected V2.1 XSD blob `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e` declares `TransportMode` with `minOccurs="0"` and no `maxOccurs`, hence effective 0:1.

### Common V2.2

Printed page **18** visibly shows **2.8 Connection**, **Table 8**:

- `TransportMode 0:*`
- `ConnectionMode 0:*`

Exact selected official Common V2.2 blob `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` declares:

- line 183: `TransportMode`, `minOccurs="0"`, no maxOccurs => 0:1
- line 188: `ConnectionMode`, `minOccurs="0"`, no maxOccurs => 0:1

### Common V2.3

Printed page **18** visibly repeats the same **2.8 Connection / Table 8** cardinalities `0:*` for both fields.

Exact selected official Common V2.3 blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` retains the same effective 0:1 XSD declarations at lines 183 and 188.

### Common V2.4

Printed page **20** visibly repeats **2.8 Connection / Table 8** with `TransportMode 0:*` and `ConnectionMode 0:*`.

Selected candidate/integration Common V2.4 blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` retains the same effective 0:1 declarations. This XSD lane is not promoted to official release authority.

### Result

No semantic change.

- CE-011 remains a confirmed cross-artifact cardinality mismatch.
- affected scope remains V2.2-V2.3 official plus V2.4 candidate/integration.
- V2.1 remains an explicit aligned negative control and must not be back-extended into the finding.
- repeated `TransportMode` or `ConnectionMode` elements that violate the selected XSD must **FAIL**.
- the PDF `0:*` wording is explanatory Known-Issue context only.
- SDK behavior remains `error_with_advisory`.

## CE-012 — DeviceSpecificationWithStateList minimum cardinality

Visible body recheck:

- V1.0 printed page **11**: **1.18 DeviceSpecificationWithStateList**, **Table 18** -> `DeviceSpecificationWithState 1:*`
- V2.0 printed page **18**: **2.18 DeviceSpecificationWithStateList**, **Table 18** -> `1:*`
- V2.1 printed page **20**: **2.18 DeviceSpecificationWithStateList**, **Table 18** -> `1:*`
- V2.2 printed page **21**: **2.18 DeviceSpecificationWithStateList**, **Table 18** -> `1:*`
- V2.3 printed page **21**: **2.18 DeviceSpecificationWithStateList**, **Table 18** -> `1:*`
- V2.4 printed page **23**: **2.18 DeviceSpecificationWithStateList**, **Table 18** -> `1:*`

Exact selected XSD declarations:

- V1.0 blob `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`, line 265
- V2.0 blob `8608e3dcd665c197c34da7f6ec6af5a3758da164`, line 271
- V2.1 blob `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e`, line 271
- V2.2 blob `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`, line 275
- V2.3 blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`, line 275
- V2.4 candidate/integration blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`, line 275

Every selected XSD declares `DeviceSpecificationWithState` with `minOccurs="0" maxOccurs="unbounded"`, i.e. **0:***.

The strongest disproof attempt is whether the table's 1:* should be interpreted as an additional semantic rule on top of XSD validity. Under the project authority contract it cannot override the exact selected XSD for conformance.

### Result

No semantic change.

- CE-012 remains a confirmed cross-artifact minimum-cardinality mismatch.
- an empty `DeviceSpecificationWithStateList` that is valid against the exact selected XSD must **PASS**.
- the stricter PDF minimum may be reported as an advisory/documentation discrepancy, but must not create an extra SDK rejection.
- V2.4 remains candidate/integration XSD authority only.
- SDK behavior remains `valid_with_advisory`.

## Accounting

- CE-011: `verified_current_standard`
- CE-012: `verified_current_standard`
- structural locator count remains **40**
- current-standard verified becomes **29**
- pending becomes **11**
- next pending finding: **CE-013**

## Gate

Pending.
