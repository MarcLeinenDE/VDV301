# Finding Revalidation — Network V2.0 / VDV 301-3 02/2020

Date: 2026-09-06  
Scope: `DRNET20-001`, `DRNET20-002`, `DRNET20-003`  
Evidence: `EV-144`, successful evidence run `34025645375`, job `101466007321`  
Closure run: `34025824480`

## Authority route

Official VDV 301-3 Network Infrastructure 02/2020 PDF, byte pin `edfedf36eeb18075b45bf5224f0da6500cdd489438091f18bada42f9668c2a99`, 558005 bytes, 37 pages. This document uses the physical/network/protocol profile lane and intentionally has no XSD lane. IEEE material is used only as terminology interpretation/falsification context; it does not replace VDV authority.

The prior all-page visual evidence is run `33270251357`, job `99147343832`, artifact `9719880284`. EV-144 freshly rendered pages 7, 8, 10, 17, 18, 19 and 29 and bound their hashes into `audit_registry/network_v20_revalidation_evidence_2026-09-06.json`.

## DRNET20-001 — context_verified

The copper-cabling sections on pages 10 and 17 recommend `1000Base-X`, while their own adjacent table specifies `1 GBase-T`. The internal VDV contradiction is the primary evidence. IEEE public material confirms Clause 40 as 1000BASE-T and independently exposes distinct 1000BASE-X/1000BASE-T terminology; this is interpretation context only. No executable XML effect exists.

## DRNET20-002 — context_verified

Pages 7 and 8 establish the functional-safety boundary as `sicherheitsrelevant` / `safety-relevant`, while the English Figure 1 caption switches to `security-relevant`. Safety and security are not treated as interchangeable here. Documentation/translation defect only.

## DRNET20-003 — context_verified

Pages 18, 19 and 29 retain grouped non-executable editorial residue (`Connection methodes`, `Not describede`, and the `in de IEEE 802.3af/at/bt` wording). Historical `NET-003` remains separately deduplicated as the page-11 `IEE 802.3` item and is not merged into this frozen finding.

## Active disproof / boundaries

The CAT6/55 m sentence is not promoted as an independent defect because its immediate 10GBASE-T context supports the scoped reading. Mixed Figure/Table 2/3 labels, the empty first-edition version history and absence of an XSD are not promoted. RV-002 remains adjacent deterministic DNS-SD classifier evidence only and is not physical/network-media conformance evidence.

## Closure

EV-144 PASS; closure rerun PASS; all 50 XSDs PASS; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **106/192 terminal, 86 pending**. The first remaining pending frozen finding is `DRS-001`; next block is `DRS` (`DOOR_V2.1_DRS`).
