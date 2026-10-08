# Version-scope boundary review — DISC-001 — 2026-10-08

Status: **verified / cross-language documentation contradiction / scope unchanged**.

## Source and rule boundary
DISC-001 concerns VDV 301-2 **IP allocation documentation**, not an XSD member. Exact version-, language- and page-specific PDF source pins and prior visible-body checks are in `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_DISC_001_2026-10-06.md` and EV-126 run `33754189273`.

## Lower / historical boundary
- **V1.0 German**, p20 §2.1.1: automatic ZeroConf-style allocation, `169.254.xxx.xxx`; cites the incorrect RFC 2927. There is no separately established V1.0 English authority. This is historical baseline, not evidence of a DE/EN semantic conflict by itself.
- **Base V2.0**, bilingual p21, and **Base V2.1**, bilingual p22: both German and English require/describe ZeroConf/169.254, but German cites RFC **3927** while English cites RFC **2927**. The normative allocation-policy semantics are otherwise aligned. The citation defect is separately DISC-002.

## First material policy contradiction and continuity
- **General Conventions V2.2**: German p17 states that no IP allocation method is prescribed, identifying fixed IP/DHCP as best practice. English p20 still requires ZeroConf and `169.254.xxx.xxx`. This is **first proven policy-semantic DE/EN split**, not merely an RFC number typo.
- **V2.3**: same semantic contradiction, German p17 vs English p20.
- **V2.4**: same contradiction still visible, German p20 vs English p23. This is the **last retained checked publication**; no corrected successor is established by this audit.

## Active disproof / SDK
Refuting 'only the RFC number differs': true only as a description of the V2.0/V2.1 bilingual discrepancy, not V2.2+. The latter language tracks expressly prescribe different allocation behavior.

Do not silently promote either translation to an exclusive corrected authority. No XML/XSD rule applies, no provider may fail XML schema validation because it uses DHCP/fixed IP rather than the old English ZeroConf formulation, and no universal ZeroConf/169.254 mandate can be inferred from the conflicted documents. Keep existing contextual/documentation-only classification.

External references: RFC Editor RFC2927 (https://www.rfc-editor.org/info/rfc2927/) and RFC3927 (https://www.rfc-editor.org/info/rfc3927/). DISC-002 separately addresses the wrong RFC number without resolving the V2.2+ allocation-policy contradiction.
