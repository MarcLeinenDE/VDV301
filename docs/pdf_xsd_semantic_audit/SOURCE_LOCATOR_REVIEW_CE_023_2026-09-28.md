# Source-locator review — CE-023 — 2026-09-28

Status: **terminally validated / complete**.

## Finding
CE-023 is a documentation-only defect limited to Common V2.2.

The official V2.2 PDF contains section `2.34 NetexMode` on printed page 26, but the displayed table is a corrupt duplicate carrying the `Message` structure fields:

- `Message`
- `Message-ID`
- `TimeStamp`
- `MessageType`
- `MessageText`

The actual NetexMode model is already documented earlier in the same PDF on printed page 15, section `1.18 NetexMode`, and the exact V2.2 XSD contains the corresponding main-mode/submode choice model at lines 956-970.

## Scope correction
The affected scope is **Common V2.2 only**.

Fresh exact official Common V2.3 visible-source evidence shows that section 2.34 contains the NetexMode heading/descriptive content and does **not** contain the duplicate Message table. The earlier V2.3 affected-scope interpretation is therefore withdrawn and must not re-enter canonical state. V2.4 is also not affected.

## Conformance rule
This finding does not define an XML validation exception or additional FAIL rule.

The selected XSD remains executable authority. No alias, schema patch, or special XML acceptance/rejection is derived from the corrupt V2.2 table.

SDK behaviour: **information / documentation advisory only** when the selected documentation context is Common V2.2.

## State
Canonical source-locator manifest after validation: **19 complete / 0 partial / 173 remaining**.
