# Visible-body source-locator revalidation — CE-005 / CE-006

Date: 2026-10-05  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`  
Scope: current-standard revalidation of two existing structurally complete Common/Enumerations findings; no new finding progress credit.

## CE-005 — AdditionalTextMessage cardinality mismatch

The stored visible-body locators were rechecked across every affected publication lane.

### Common V2.0

Printed page **29** visibly shows section **2.57 TripInformation**, **Table 57**. The `AdditionalTextMessage` row is shown as **0:***.

Exact selected XSD:

- `IBIS-IP_common_V2.0.xsd`
- blob `8608e3dcd665c197c34da7f6ec6af5a3758da164`
- line 637: `AdditionalTextMessage` has `minOccurs="0"` and no `maxOccurs`, therefore XSD default maxOccurs = 1.

### Common V2.1

Printed page **31** visibly shows section **2.57 TripInformation**, **Table 57**, again with `AdditionalTextMessage` = **0:***.

Exact selected XSD blob `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e`, line 636, remains bounded to maxOccurs 1.

### Common V2.2

Printed page **33** visibly shows section **2.58 TripInformation**, **Table 58**, with `AdditionalTextMessage` = **0:***.

Exact selected XSD blob `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`, line 645, remains bounded to maxOccurs 1.

### Common V2.3

Printed page **34** visibly shows section **2.58 TripInformation**, **Table 58**. Both `AdditionalTextMessage` and `AdditionalTextMessage(n)` are shown as **0:***; the explanatory text defines n = 1 to 9.

Exact official Common V2.3 blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` declares the base field and `AdditionalTextMessage1..9` individually, each without `maxOccurs`, hence each named element is individually bounded to one.

### Common V2.4

Printed page **36** visibly shows section **2.57 TripInformation**, **Table 57** with the base and numbered AdditionalTextMessage rows shown as **0:***. Printed page **37** visibly continues Table 57 and then starts section 2.58; it does not alter that cardinality statement.

The V2.4 page-37 check used the exact-byte artifact `9857652638` already pinned for COMMON_V2.4; page 36 was also visually checked from the official publication surface. Selected executable authority remains candidate/integration Common V2.4 blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`, lines 743-752, where the base and numbered fields are individually bounded to one.

### Result

No semantic change.

CE-005 remains a confirmed cross-artifact cardinality mismatch:

- PDF: repeated values are documented as `0:*`
- selected XSD: each named field is max `0:1`
- selected-XSD validation remains normative
- an instance rejected for repeating the same named element remains **FAIL**, with the documentation mismatch reported as explanatory context
- V2.4 remains candidate/integration authority only
- the corrected affected scope remains V2.0-V2.3 official plus V2.4 candidate/integration; no V1.x extension is inferred.

## CE-006 — DeviceStateEnumeration.warning omitted from PDF

The stored body anchors were visibly rechecked:

- V2.2 printed page **37** — **3.5 DeviceStateEnumeration**, **Table 70**
- V2.3 printed page **38** — **3.5 DeviceStateEnumeration**, **Table 70**
- V2.4 printed page **41** — **3.5 DeviceStateEnumeration**, **Table 69**

All three visible tables list:

- `defective`
- `notavailable`
- `running`
- `readyForShutdown`

and do **not** list `warning`.

Exact XSD authority:

- V2.2 / official V2.3 dependency route: `IBIS-IP_Enumerations_V2.2.xsd`, blob `2a23b512379b18e8f122ac1272cef8229fb86283`, line 56 contains `<xs:enumeration value="warning"/>`
- V2.4 selected candidate/integration lane: `IBIS-IP_Enumerations_V2.4.xsd`, blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`, line 56 also contains `warning`

The strongest disproof attempt fails: `warning` is not merely an inferred value or a neighbouring-version substitution. It is explicitly present in the exact selected enumeration authority for each affected lane.

### Result

No semantic change.

CE-006 remains a confirmed cross-artifact mismatch:

- `warning` is XSD-valid in the selected affected profiles
- the PDF omission does not make it invalid
- SDK behaviour remains `valid_with_advisory`
- V2.4 remains candidate/integration authority only.

## Accounting

After this block:

- CE-005: `verified_current_standard`
- CE-006: `verified_current_standard`
- structural locator count remains **40**
- current-standard verified count becomes **23**
- pending current-standard revalidation becomes **17**
- next pending finding: **CE-007**

## Gate

- GitHub Actions run: **37291258017**
- result: **SUCCESS**
- validated commit: `bf43f301fb10f6288af89f4e6f8728d4add5da84`
- structural locators: **40**
- current-standard verified: **23**
- pending current-standard revalidation: **17**
- next pending finding: **CE-007**

The gate verified CURRENT_STATE/body-registry synchronization, the CE-005 per-version TripInformation locator assertions, the CE-006 DeviceStateEnumeration locator/value assertions, and the existing audit regression suite.
