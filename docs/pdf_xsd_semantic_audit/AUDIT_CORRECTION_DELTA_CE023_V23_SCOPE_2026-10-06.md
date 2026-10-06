# Audit correction delta — CE-023 V2.3 scope

Date: 2026-10-06  
Finding: `CE-023`  
Reason: current-standard visible-body revalidation disproved the previous V2.3 scope withdrawal.

## Previous current-state claim

The prior reconciliation treated CE-023 as a Common V2.2-only documentation defect and stated that fresh visible V2.3 evidence had removed Common V2.3 from the affected scope.

That conclusion is now superseded for CE-023 only.

Historical reports containing the old decision are retained unchanged as audit history. This correction delta is the new current authority for CE-023 scope.

## Exact V2.3 source recheck

Official Common V2.3 PDF:

- SHA-256: `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`
- historical exact-byte render/read run: `33656579631`
- artifact: `9856965744`
- artifact bytes were re-opened during the 2026-10-06 current-standard revalidation.

Visible body:

- printed p.26 begins section **2.34 NetexMode** and shows the NetexMode descriptive prose.
- printed p.27 continues that section with **Table 34**, captioned **Description of NetexMode**.
- the displayed Table 34 is visibly the **Message** structure: `Message-ID`, `TimeStamp`, `MessageType`, `MessageText`.

Rendered-page SHA-256 values:

- p.26: `b541889bb83952a6f9e7aef044bc70834ea1acbe23e80d34c7d4f3d8ed9fa7ea`
- p.27: `da2ebb0aaa92ca1aac51a842d20b2dcda3c11d8abe1c150e6f5b783167763d89`

This directly disproves the previous statement that V2.3 did not contain the corrupt duplicate/copy-paste NetexMode table.

## V2.2 confirmation

The official Common V2.2 PDF, SHA-256
`85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`,
was also rechecked visibly.

Printed p.26 visibly shows:

- section **2.34 NetexMode**
- a second **Message** table
- caption **Table 34 — Description of NetexMode**

Thus V2.2 remains affected.

The real NetexMode structure is separately visible on printed p.15, section **1.18 NetexMode**, and the exact V2.2 XSD `NetexMode` complex type at lines 956-970 contains the expected mode/submode choice model rather than Message fields.

## V2.4 negative control

Official Common V2.4 PDF SHA-256:
`01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`.

Printed p.29 visibly shows:

- section **2.32 LogMessage**
- section **2.33 Message**
- section **2.34 Point**

There is no second NetexMode section/table at 2.34. V2.4 therefore remains **not affected**.

## Corrected CE-023 scope

Current affected scope:

- **Common V2.2** — documentation defect confirmed
- **Common V2.3** — documentation defect confirmed
- **Common V2.4** — not affected

The defect remains documentation-only:

- no XSD alias follows;
- no XML validation exception follows;
- the exact selected XSD remains authoritative;
- runtime matching remains not applicable;
- SDK behavior remains informational documentation advisory only.

## Superseded statements

For CE-023 only, any prior statement equivalent to:

- “V2.3 scope withdrawn”
- “V2.3 not affected”
- “V2.2-only”

is superseded by this correction delta.

No other CE finding identity or scope is changed by this correction.
