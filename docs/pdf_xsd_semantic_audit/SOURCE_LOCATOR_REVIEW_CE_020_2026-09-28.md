# Source-locator review — CE-020 — 2026-09-28

Status: **terminally validated / complete**.

## Finding
CE-020 records an authority/variant split for Common V2.3 `InternationalTextType`.

The official PDF documents:
- `Value` as `IBIS-IP.string`
- `Language` as `IBIS-IP.language`

The official V2.3 XSD instead defines:
- `Value` as `xs:string`
- `Language` as `xs:language`

The retained PR #30 candidate variant changes exactly these two XSD member types to the PDF-described IBIS-IP wrapper types.

## Authority matrix
| Variant | Authority | XSD blob | InternationalTextType |
|---|---|---|---|
| official Common V2.3 | official release / default | `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` | `xs:string`, `xs:language` |
| common-v2.3-upstream-pr30 | candidate / explicit opt-in | `456a7db179ce14bc3f04e2bc05e42e16545fb0c5` | `IBIS-IP.string`, `IBIS-IP.language` |

Official PDF locator: Common V2.3, p. 36, section 2.61, Table 61.

Both XSD variants locate `InternationalTextType` at lines 805-809 of their pinned blobs.

## Conformance rule
There is no latest-wins behaviour.

- If official Common V2.3 is selected, the official XSD is authoritative and its primitive instance shape is required.
- If the PR #30 candidate variant is explicitly selected, that candidate XSD becomes the selected executable authority for that run.
- The candidate variant does not retroactively correct, replace, or weaken the historical official V2.3 profile.

SDK behaviour: **warning on authority ambiguity**. Actual XML PASS/FAIL is always evaluated against the explicitly selected XSD variant.

## State
Canonical source-locator manifest after validation: **16 complete / 0 partial / 176 remaining**.
