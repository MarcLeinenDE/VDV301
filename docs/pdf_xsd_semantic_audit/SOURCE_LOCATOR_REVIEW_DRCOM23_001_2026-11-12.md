# Source locator review — DRCOM23-001 — 2026-11-12

**Identity:** One historical finding `DRCOM23-001`, not another `DRCOM21-001` StopName finding. Scope: official Common V2.3 request-field mismatch, with independently checked predecessors V1.0–V2.2 and successor Common V2.4 **published PDF plus explicitly selected candidate/integration XSD**. Source-level work only, no remediation.

## Discrepancy, field identity and counterevidence

In the actual official Common V2.3 **printed page 32, §2.52 StopInformationRequest, Table 52 — Description of StopInformationRequest**, the member rows show `ArrivalExpected 0:1 IBIS-IP.dateTime` and `DepartureExpected 0:1 IBIS-IP.dateTime`. The **exact official `VDV-301-2.3` Common XSD** Git blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` defines **neither** child under `StopInformationRequestStructure` (lines 584–618). The same XSD permits both under **`StopInformationStructure`** (lines 637 and 643). The PDF's neighboring `StopName 0:1` vs XSD `0:*` facet is **already separately** audited under `DRCOM21-001`; it is not this finding.

The strongest alternate explanation is intentional documentation of a request payload that the XSD already accepts through an inherited type or alternative branch. The exact XSD has no such request extension; preserved **EV-121** verifies both requested fields are rejected in `StopInformationRequestStructure` but both are accepted in `StopInformationStructure`. Another explanation is that the PDF accidentally repeated StopInformation members or that the V2.3 XSD accidentally omitted intended Request fields; the V2.3 history references the additions and the V2.4 candidate introduces both in the request, so **the two sources genuinely disagree** but the publisher's blame attribution is **not conclusively established**. Classification: `cross_artifact_mismatch`, rather than asserting an independently proven sole PDF fault. The selected official V2.3 XSD remains the executable authority (strict **INVALID** for either field in its request type).

## Original PDF visible-body and predecessor/successor evidence

Every source is exactly byte/size pinned in `audit_registry/pdf_source_pins_v0.1.json`. The cited source/PNG SHA-256 values are verified from archived official PDF render artifacts, with visible body pages inspected rather than relying on TOC/version-history section numbering:

| Official original Common PDF | Real printed page and body | Exact original PDF SHA-256 | Size, bytes | Original page PNG SHA-256 / run |
| --- | --- | --- | ---: | --- |
| V1.0 (DE) | p19 §1.48 Table 48 **StopInformation** and p20 §1.50 Table 50; **no standalone StopInformationRequest PDF member table** | `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf` | 892769 | p19 `48c89183aeb69a335687da8321990e4dc79b4ab0062181ee1ea160edbf922346`, p20 `74c8f525df2d2b14e63fdbb5b2eec2e51bd2bbb28c3110aa967fff6bdb661282`; run 33275626001/artifact 9721397514 |
| V2.0 (DE/EN) | p27 §2.51 Table 51 **StopInformationRequest**; neither Expected time field | `23806f025d0412c1b5f9c2ac98ee3cd0c1c08cc97aba4f0dd2eb88c485182088` | 946088 | `71d3999b383690495891ee390ef3836fddc87503d2d92874e4ad2e5ecd5d536f`; run 33279811315/artifact 9722644456 |
| V2.1 (DE/EN) | p29 §2.51 Table 51 **StopInformationRequest**; neither Expected time field | `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32` | 1274051 | `2493af2ea41abe8c72e1d351762acf54412b7f05cdd04f25cce7736843a1fde5`; run 33393002497/artifact 9758203545 |
| V2.2 (DE/EN) | p31 §2.52 Table 52 **StopInformationRequest**; neither Expected time field | `85168c2012e81a9a2186c98859f04f959d783b5e33b631104a1b90b29fceb203` | 1411558 | `a072381c3477de238461a0ca5a69882fbc0cc1da5b20ec417f01dbd51504aaba`; pinned fallback [run 43216104609](https://github.com/MarcLeinenDE/VDV301/actions/runs/43216104609), artifact 13944345486 |
| **V2.3 (DE/EN, affected)** | **p32 §2.52 Table 52 StopInformationRequest**: both `ArrivalExpected 0:1` and `DepartureExpected 0:1` visibly listed | `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b` | 793521 | `b9f7576dd7654b3976fd7d05e7d2d653e07a2c912ab60c7fa2d8514dcdd1b904`; run 33656579631/artifact 9856965744 (also EV-139 artifact 9930843755) |
| **V2.4 (DE/EN, correction boundary only)** | p34 §2.51 **StopInformationRequest** with `ArrivalExpected 0:1`; p35 continuation with `DepartureExpected 0:1` and actual **Table 51 caption** | `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a` | 1689647 | p34 `d3d1f03a989ae3f18349b747643307567ff3e873862014e7c642b46bedd54a16`; p35 `9a333351c0ef89a63067595482fdff7f26b59808c40f693ba2d1e32bf6fb24bd`; run 33658306978/artifact 9857652638 |

**V1.0 nuance:** Its official XSD has a `StopInformationRequestStructure` despite no directly comparable request PDF table. The missing PDF member table is not treated as evidence that the XSD type does not exist. V2.0–V2.2 original tables and corresponding selected XSDs contain neither Expected-time request field; last nonaffected predecessor is **V2.2**. First/last **official affected** is **V2.3**. V2.4 is a **published official PDF** but the separately selected Common V2.4 XSD is `candidate_integration`; that candidate now declares both request fields and is not an official released XSD, so this is a **candidate-only correction boundary**, not an official release fix. No later official successor validated. No independent language-specific alternate XSD/PDF edition established in bilingual editions.

## Exact selected XSD authority

| XSD profile | Exact Git blob | Request child rule | Status |
| --- | --- | --- | --- |
| Common V1.0 | `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c` | no request Expected-time fields; PDF has no comparable request table | official historical |
| Common V2.0 | `8608e3dcd665c197c34da7f6ec6af5a3758da164` | no request Expected-time fields; matches original PDF | official historical |
| Common V2.1 | `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e` | no request Expected-time fields; matches original PDF | official historical |
| Common V2.2 | `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` | no request Expected-time fields; matches original PDF; exact upstream V2.2 file lineage, **no fabricated `VDV-301-2.2` tag** | official historical |
| Common **V2.3** | `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` | `StopInformationRequestStructure` lines584–618 contains **neither**; `StopInformationStructure` lines637/643 **does** | **official `VDV-301-2.3` tag** |
| Common V2.4 | `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` | `StopInformationRequestStructure` lines615/617 declares both `minOccurs=0` | **candidate/integration only** |

Relevant XPath: `/xs:schema/xs:complexType[@name='StopInformationRequestStructure']/xs:sequence/xs:element[@name='ArrivalExpected' or @name='DepartureExpected']` (nodes **absent** in V2.3; present in selected candidate V2.4). Historical official V2.3 Common uses exact Enumerations V2.2 dependency; do not apply latest-wins.

**Executable regression:** Preserved `tools/validate_common_v23_ev121.py` tests distinct `ArrivalExpected` and `DepartureExpected` in a synthetic Request root **INVALID** under exact V2.3; the same fields in synthetic StopInformation root **VALID**. Historical `EV-121` and V2.3 current `EV-139` closure run **33857906408** support that result. Candidate V2.4 preserved `EV-122` accepts both request fields. These are historical validated sources; **no new version-wide XML fixture matrix executed in this locator cycle**. Synthetic roots do not imply new global production roots.

## SDK implication and completion boundary

Affected runtime scope **only official Common V2.3**, `error_with_advisory` to decorate a **pre-existing XSD-INVALID** result for the exact unexpected request elements. Runtime matcher remains **`reviewed_not_implemented`**; no namespace aliases, XSD patch, error-to-valid conversion, silent request routing or adoption of V2.4 candidate for official V2.3. Distinct `DRCOM21-001` StopName maximum discrepancy remains separate.

One new **locator-complete identity** brings total to **95/192**, **95/95** original-body and version-boundary verified, **97 remaining**. The source-locator/semantic/runtime/body/boundary/SDK mirror and `CURRENT_STATE.json` must be atomically synchronized as `gate_pending`, pass full Schema-Audit-Validation, then separately `terminal_clean` and final HEAD Handoff Integrity. Next unique finding **`DRCOM24-001`**.
