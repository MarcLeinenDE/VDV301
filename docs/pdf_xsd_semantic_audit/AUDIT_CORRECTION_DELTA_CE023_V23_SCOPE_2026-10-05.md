# Audit correction delta — CE-023 Common V2.3 scope

Date: 2026-10-05  
Finding: `CE-023`  
Reason: current-standard visible-body revalidation exposed an incorrect historical V2.3 scope withdrawal.

## Prior recorded state

The 2026-09-03 CE revalidation and Common findings addendum recorded CE-023 as affected only in Common V2.2 and explicitly withdrew Common V2.3 after a visible check of printed page 26.

That historical statement is preserved as history but is **superseded for current canonical state** by this correction delta.

## Exact V2.3 source recheck

Official Common V2.3 PDF:

- SHA-256: `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`
- pinned render/read run: `33656579631`
- artifact: `9856965744`
- page count: 58

The PDF SHA was recomputed from the downloaded artifact and exactly matches the registered pin.

Rendered page hashes also exactly match the artifact manifest:

- printed p.26: `d177fad7b44a43305467991ce985551f38fffa28ad3b880410ac9104551d7ca2`
- printed p.27: `a71c6c8a01f3516223469873682c358c530b16f066f9b097ef28ec107b465cd8`

### Visible body

Printed p.26 visibly shows:

- section **2.34 NetexMode**
- descriptive prose: “A combined Mode and SubMode information in accordance with Netex.”
- no table body yet on that page.

Printed p.27 is the continuation of the same section and visibly shows **Table 34 — Description of NetexMode**, but the table content is the `Message` structure:

- `Message-ID`
- `TimeStamp`
- `MessageType`
- `MessageText`

Therefore the prior disproof was incomplete: checking p.26 alone missed the continued corrupt table on p.27.

## Exact XSD comparison

Official Common V2.3 XSD:

- `IBIS-IP_common_V2.3.xsd`
- blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`
- `NetexMode` complex type lines 1036-1050

The XSD contains the actual NetexMode model with a main-mode choice and a submode choice. It does not contain the Message fields shown in the corrupt PDF table.

## V2.4 negative control

Exact byte-pinned Common V2.4 printed p.29 visibly shows:

- `2.32 LogMessage`
- `2.33 Message`
- `2.34 Point`

There is no duplicate `2.34 NetexMode` table in the V2.4 publication. V2.4 therefore remains outside CE-023 scope.

## Corrected canonical decision

CE-023 is a documentation-only copy/paste/table defect affecting:

- **Common V2.2**
- **Common V2.3**

Common V2.4 is not affected.

No XSD defect, XML alias or special validation rule follows. Exact selected XSD authority remains unchanged.

## Historical handling

Do not rewrite the old 2026-09-03 reports to pretend the earlier conclusion never existed. Current registries and handoff state must reference this delta and carry the corrected V2.2-V2.3 scope.
