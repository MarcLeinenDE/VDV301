# Finding Revalidation — NET / VDV 301-3 Network Infrastructure 02/2020

Date: 2026-09-08  
Scope: `NET-001` … `NET-003`  
Evidence: `EV-154`, successful run `34232483234`, job `102081822927`  
Evidence commit: `3645ddfeb32effd0b17432672ab91476e1accdf8`  
Artifact: `10058380451`, `sha256:dcb266cad68054375d65818fda20d7ec53c59843a48525d60b3ade62f5c38396`  
Closure run: `34266935807`

## Authority route

The official VDV-Schrift 301-3 Network Infrastructure 02/2020 PDF was freshly fetched and byte-pinned at SHA-256 `edfedf36eeb18075b45bf5224f0da6500cdd489438091f18bada42f9668c2a99` (558005 bytes). The fresh bytes match the independent historical pin. Definition provenance comes from the independent frozen-head Deep Read performed before historical reconciliation. VDV 301-3 intentionally has no XSD lane; therefore the complete 50-root XSD run is retained only as a regression/no-mutation guard and is not used as executable evidence for these findings.

Fresh 180-DPI renders of physical pages 6, 7, 8, 11, 14, 20 and 29 were manually inspected before closure.

## NET-001 — context_verified

English Scope page 8 visibly says `VDV 303-3`. German Scope page 7, the page footer and the publication identity all establish `VDV 301-3`. The alternate-document interpretation is therefore actively disproved. The finding is a local English documentation-number typo.

## NET-002 — context_verified

The German cabling subsection is visibly numbered `2.3.4` on page 14. The corresponding English subsection is visibly numbered `2.3.5` on page 20, and the English table of contents on page 6 skips directly from `2.3.3` to `2.3.5`. Intentional bilingual renumbering is unsupported; the finding is an editorial subsection-numbering error.

## NET-003 — context_verified

German page 11 visibly prints `IEE 802.3`. The same exact publication uses the correct `IEEE 802.3` spelling elsewhere, including the PoE reference `IEEE 802.3af/at/bt` on page 29. An intentional alternate abbreviation is therefore actively disproved; this is a local IEEE spelling typo.

## Closure

EV-154 PASS; fresh byte-pinned visual evidence manually inspected; complete 50-root XSD regression PASS as no-mutation guard; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **138/192 terminal, 54 pending**. The first remaining pending finding is `PCS-001`; next block is `PCS`.
