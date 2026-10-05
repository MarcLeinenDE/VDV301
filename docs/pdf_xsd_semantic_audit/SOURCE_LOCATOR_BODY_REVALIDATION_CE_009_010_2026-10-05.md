# Visible-body source-locator revalidation — CE-009 / CE-010

Date: 2026-10-05  
Workflow: `00_START_HERE/AUDIT_WORKFLOW_CONTRACT.md`

## CE-009 — RailSubmode specialRail vs specialTrain

Visible body checks:

- Common V2.2 printed page **43**: **3.30 RailSubmodeEnumeration**, **Table 95** visibly lists `specialRail`.
- Common V2.3 printed page **44**: **3.30 RailSubmodeEnumeration**, **Table 95** visibly lists `specialRail`.
- Common V2.4 printed page **47**: **3.30 RailSubmodeEnumeration**, **Table 94** visibly lists `specialRail`.

Exact selected XSD authority:

- V2.2/V2.3: `IBIS-IP_Enumerations_V2.2.xsd`, blob `2a23b512379b18e8f122ac1272cef8229fb86283`, line 422: `specialTrain`
- V2.4 candidate/integration: `IBIS-IP_Enumerations_V2.4.xsd`, blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`, line 423: `specialTrain`

The active disproof attempt was whether `specialRail` could be a harmless display synonym. It cannot be treated that way for XML conformance because the selected XSD defines a literal enumeration boundary and no alias declaration exists.

Result: no semantic change.

- CE-009 remains a confirmed cross-artifact mismatch.
- XML must use `specialTrain` for these selected XSDs.
- `specialRail` from the PDF is not accepted as an alias.
- a provider payload using `specialRail` where the selected XSD requires `specialTrain` must **FAIL**.
- SDK behaviour remains `error_with_advisory`.

## CE-010 — AirSubmode canalBarge omitted from PDF

Visible body checks:

- Common V2.2 printed page **45**: **3.36 AirSubmodeEnumeration**, **Table 101**; `canalBarge` is not listed.
- Common V2.3 printed page **46**: **3.36 AirSubmodeEnumeration**, **Table 101**; `canalBarge` is not listed.
- Common V2.4 printed page **49**: **3.36 AirSubmodeEnumeration**, **Table 100**; `canalBarge` is not listed.

Exact selected XSD authority:

- V2.2/V2.3: `IBIS-IP_Enumerations_V2.2.xsd`, blob `2a23b512379b18e8f122ac1272cef8229fb86283`, line 588 contains `<xs:enumeration value="canalBarge">`.
- V2.4 candidate/integration: `IBIS-IP_Enumerations_V2.4.xsd`, blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`, line 589 contains the same `canalBarge` enumeration.

The strongest disproof attempt is the semantically odd placement of a value named `canalBarge` inside AirSubmode. That does not change executable authority: the exact selected XSD explicitly contains the value. The PDF omission cannot create an additional validation rejection.

Result: no semantic change.

- CE-010 remains a confirmed cross-artifact mismatch.
- `canalBarge` is XSD-valid in the selected affected profiles.
- SDK behaviour remains `valid_with_advisory`.
- V2.4 remains candidate/integration authority only.

## Accounting

- CE-009: `verified_current_standard`
- CE-010: `verified_current_standard`
- structural locator count remains **40**
- current-standard verified becomes **27**
- pending becomes **13**
- next pending finding: **CE-011**

## Gate

Pending.
