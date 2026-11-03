# SOURCE LOCATOR REVIEW — DRCOM10-003 — 2026-11-03

Status: **source, visible-body and version scope evidence confirmed; gate_pending until full validation and terminal HEAD handoff are successful**.

## Finding identity and attribution

- Existing unique finding: **`DRCOM10-003`** — `ServiceSpecificationWithStateList.ServiceSpecificationWithState` minimum cardinality.
- Classification: `confirmed_pdf_defect`, `primary_issue_kind=cardinality_mismatch`, `sdk_behavior=valid_with_advisory`, normative authority `selected_xsd`.
- The original V1.0-only semantic scope was too narrow. All original Common PDF versions V1.0–V2.4 independently preserve the same 1:* documentation while each exact selected XSD permits zero child elements (0:*).
- **No new finding ID** is introduced. Other list names (DeviceSpecificationWithStateList, ServiceIdentificationWithStateList) retain their separate established CE identities. This finding addresses only ServiceSpecificationWithStateList and must not be expanded to unrelated lists.

## Independently pinned and visually checked original body

All six GitHub fallback runs completed **SUCCESS** using `tools/render_vdv_pdf_pages.py` and exact source byte hashes plus sizes from the pinned registry. The original PNGs were downloaded, their SHA-256 hashes checked against their render manifests and the actual table/section/caption visually inspected.

| Original Common PDF | Printed page | Visible body locator | PDF minimum | Exact XSD minimum | Selected XSD authority | Original render |
|---|---:|---|---|---|---|---|
| V1.0 | 18 | §1.44, Table 44 | `1:*` | `0:*` | official_release | [41649308454](https://github.com/MarcLeinenDE/VDV301/actions/runs/41649308454) / artifact 13237115551 |
| V2.0 | 25 | §2.44, Table 44 | `1:*` | `0:*` | official_release | [41649627068](https://github.com/MarcLeinenDE/VDV301/actions/runs/41649627068) / artifact 13236717262 |
| V2.1 | 27 | §2.44, Table 44 | `1:*` | `0:*` | official_release | [41649658472](https://github.com/MarcLeinenDE/VDV301/actions/runs/41649658472) / artifact 13236253276 |
| V2.2 | 29 | §2.45, Table 45 | `1:*` | `0:*` | official_release | [41649692297](https://github.com/MarcLeinenDE/VDV301/actions/runs/41649692297) / artifact 13237295692 |
| V2.3 | 29 | §2.45, Table 45 | `1:*` | `0:*` | official_release | [41649819541](https://github.com/MarcLeinenDE/VDV301/actions/runs/41649819541) / artifact 13235912787 |
| V2.4 | 32 | §2.44, Table 44 | `1:*` | `0:*` | candidate_integration | [41649868856](https://github.com/MarcLeinenDE/VDV301/actions/runs/41649868856) / artifact 13237122674 |

The six PDF sources use the officially registered URLs and exact SHA-256 bytes in `audit_registry/pdf_source_registry_v0.1.json` and `audit_registry/pdf_source_pins_v0.1.json`. Verifiable per-original render and XSD evidence:

- **Common V1.0**: official PDF SHA-256 `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf`, actual visible body printed p18 §1.44 **Table 44**; `ServiceSpecificationWithState` row 1:*; original PNG SHA-256 `1072f924d50e9797e9528cbe07732809e6bd856d51b5d7a7d074d67a7d30e848`; GitHub run `41649308454`, artifact `13237115551`; selected `IBIS-IP_common_V1.0.xsd` Git blob `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`, line 465; `ServiceSpecificationWithStateListStructure/xs:sequence/xs:element[@name='ServiceSpecificationWithState']` has `minOccurs="0" maxOccurs="unbounded"`; exact Enumerations dependency V1.0; authority `official_release`.
- **Common V2.0**: official PDF SHA-256 `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088`, actual visible body printed p25 §2.44 **Table 44**; `ServiceSpecificationWithState` row 1:*; original PNG SHA-256 `e4b8d430df720dcd02243f8ad3388ac51518a4a9b34d3b49dca76d16d20ce754`; GitHub run `41649627068`, artifact `13236717262`; selected `IBIS-IP_common_V2.0.xsd` Git blob `8608e3dcd665c197c34da7f6ec6af5a3758da164`, line 471; `ServiceSpecificationWithStateListStructure/xs:sequence/xs:element[@name='ServiceSpecificationWithState']` has `minOccurs="0" maxOccurs="unbounded"`; exact Enumerations dependency V2.0; authority `official_release`.
- **Common V2.1**: official PDF SHA-256 `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32`, actual visible body printed p27 §2.44 **Table 44**; `ServiceSpecificationWithState` row 1:*; original PNG SHA-256 `8351cb9e29d2090214b452e086dfc57442edd03f9752934eff6a379e0c0af1d5`; GitHub run `41649658472`, artifact `13236253276`; selected `IBIS-IP_common_V2.1.xsd` Git blob `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e`, line 470; `ServiceSpecificationWithStateListStructure/xs:sequence/xs:element[@name='ServiceSpecificationWithState']` has `minOccurs="0" maxOccurs="unbounded"`; exact Enumerations dependency V2.1; authority `official_release`.
- **Common V2.2**: official PDF SHA-256 `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203`, actual visible body printed p29 §2.45 **Table 45**; `ServiceSpecificationWithState` row 1:*; original PNG SHA-256 `248cfab843bb21903c9a462582f9262b150436fb6158c3c50746b15d486e9766`; GitHub run `41649692297`, artifact `13237295692`; selected `IBIS-IP_common_V2.2.xsd` Git blob `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`, line 479; `ServiceSpecificationWithStateListStructure/xs:sequence/xs:element[@name='ServiceSpecificationWithState']` has `minOccurs="0" maxOccurs="unbounded"`; exact Enumerations dependency V2.2; authority `official_release`.
- **Common V2.3**: official PDF SHA-256 `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`, actual visible body printed p29 §2.45 **Table 45**; `ServiceSpecificationWithState` row 1:*; original PNG SHA-256 `75ec9b40024deb4000fbbcbe9f44b5bd615241c722facd354bc7134d216516ac`; GitHub run `41649819541`, artifact `13235912787`; selected `IBIS-IP_common_V2.3.xsd` Git blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1`, line 529; `ServiceSpecificationWithStateListStructure/xs:sequence/xs:element[@name='ServiceSpecificationWithState']` has `minOccurs="0" maxOccurs="unbounded"`; exact Enumerations dependency V2.2; authority `official_release`.
- **Common V2.4**: official PDF SHA-256 `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`, actual visible body printed p32 §2.44 **Table 44**; `ServiceSpecificationWithState` row 1:*; original PNG SHA-256 `b5906fb9c08b8c7cc8a249f4165974f8be64ba7d2be3ce1c6a398f1f180d03f0`; GitHub run `41649868856`, artifact `13237122674`; selected `IBIS-IP_common_V2.4.xsd` Git blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`, line 544; `ServiceSpecificationWithStateListStructure/xs:sequence/xs:element[@name='ServiceSpecificationWithState']` has `minOccurs="0" maxOccurs="unbounded"`; exact Enumerations dependency V2.4; authority `candidate_integration`.

The cited page and table labels are the **visible original body**, not inferred from contents lists or neighboring document versions. The PDF table's ordinary 1:* cell is present in the same visual context as adjacent 1:* list tables.

## Active disproof and historical boundary

- **Notation counterargument:** Check whether a VDV choice marker or a special local legend makes 1:* optional. Rejected: target row has the normal unprefixed `1:*` minimum-one notation. The adjacent `ServiceStartList.ServiceIdentification` also has visible 1:* and the exact XSD uses an unbounded occurrence with default `minOccurs=1`, confirming the local notation is not a concealed choice.
- **Schema-context counterargument:** Perhaps an outer optional root or compositor makes the child's cardinality effectively one when present. Rejected for the inner item: the exact `ServiceSpecificationWithStateListStructure` uses a straight `xs:sequence` with one `xs:element minOccurs=0 maxOccurs=unbounded`; no choice or XSD minimum-one override.
- **Latest-wins/version confusion:** Every exact Common XSD blob was individually read, with its historical selected dependency. Common V2.3 includes **Enumerations V2.2**, not an invented V2.3 enum. Candidate/integration V2.4 is not an official released V2.4 XSD, even though its PDF is official.
- **First affected in the checked Common document family:** V1.0, publication 05/2017; no earlier separate 301-2-1 Common document checked in the canonical six-PDF source family. Intermediate affected V2.0, V2.1, V2.2, V2.3 each independently verified. Last checked affected original V2.4, publication 01/2023. **No independently verified corrected successor in the currently pinned source inventory**; do not claim no future revision exists.
- **Language scope:** The single original PDF in each selected family contains English field/type names with German text and descriptions; no separate DE/EN document was inferred. The actual numeric table cells show the same 1:*.
- **Executable evidence:** Frozen V1.0 EV-117/EV-135 demonstrates an empty list validates; Common V2.0 historical EV-118 mentions positive empty-list behavior. All six exact XSD declarations have now been inspected; **this block does not claim a new six-profile executable instance test**.

## SDK and provider consequence

A present `ServiceSpecificationWithStateList` element without `ServiceSpecificationWithState` children is XML-valid under each exact selected Common XSD. In an audit against any of these explicit profiles, **PASS remains PASS**; attach an optional documentation warning if the precise context matches. Do not make a provider FAIL, do not invent a `minOccurs=1` semantic rule, and do not repair historical XSD bytes based on the PDF. A missing list container is not automatically allowed in its consuming parent: outer structure cardinality remains governed separately by the selected XSD.

Mapping stays `reviewed_not_implemented`; **zero new runtime matchers** were implemented. No XSD, official PR branch, release tag or schema source byte was modified.

## Closure conditions

Synchronize semantic DE/EN diagnoses, runtime `profile_scope` (affected versions only), canonical source locators, visible-body verification, mandatory historical boundary registry, SDK summary and `CURRENT_STATE.json`. One new unique locator increases progress **86 → 87 of 192**, only after successful substantive schema-audit-validation and final terminal-HEAD handoff checks. Next finding: `DRCOM10-004`.
