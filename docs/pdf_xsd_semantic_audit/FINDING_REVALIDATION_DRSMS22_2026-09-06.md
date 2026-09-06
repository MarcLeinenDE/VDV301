# Finding Revalidation — DRSMS22 / SystemMonitoringService V2.2

Date: 2026-09-06  
Scope: `DRSMS22-001`, `DRSMS22-002`, `DRSMS22-003`, `DRSMS22-004`  
Evidence: `EV-146`, successful evidence run `34026822637`, job `101469161311`  
Evidence commit: `21369ec625823fe0425193a19d3ff42b3833270a`  
Closure run: `34026992744`

## Authority route

Official byte-pinned VDV-Schrift 301-2-18 SystemMonitoringService V2.2 PDF (`996f639a81cb91ad20a8e78b6213e7c85d41ff0ec42caba4208d6c4652b140f4`, 847416 bytes) plus the exact official VDV-301-2.2 schema family: `IBIS-IP_SystemMonitoringService_V2.2.xsd` blob `d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c`, `IBIS-IP_common_V2.2.xsd` blob `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`, and `IBIS-IP_Enumerations_V2.2.xsd` blob `2a23b512379b18e8f122ac1272cef8229fb86283`. Latest-XSD-wins is forbidden.

EV-146 freshly rendered pages 5, 9, 10, 11, 12 and 13 at 180 DPI, retained both layout and raw text extraction, checked the exact Common ServiceState semantics, reran EV-116, and reran the complete 50-XSD pool.

## DRSMS22-001 — context_verified

Page 5 visibly contains the broken list-of-figures bookmark output `Fehler! Textmarke nicht definiert.`. Fresh rendering and extraction reject the hypothesis that this is an extraction-only artifact. Documentation-generation defect only.

## DRSMS22-002 — context_verified

Pages 10-11 use device wording in ServiceStatus prose. The exact Common V2.2 `ServiceIdentificationWithStateStructure` contains `ServiceIdentification` plus `ServiceState` and no `DeviceState`, rejecting the hypothesis that the wording expresses alternate device-oriented semantics. Documentation semantic/copy-paste error only.

## DRSMS22-003 — context_verified

Page 12 prints `SystemManagmentService`; page 13 prints the correct `SystemManagementService`. The alternate-name hypothesis is rejected. Editorial spelling error only.

## DRSMS22-004 — context_verified

Page 9 contains both `UnsubscribeRequestStructure` and `UnsubscribeResponseStructure` for `UnsubscribeServiceStatus`, but the isolated operation-table segment omits the visible `Req.` / `Resp.` labels present on neighboring rows. The structures are not missing; the finding is specifically the table-label omission.

## Guarded non-findings

The SMS response-table `a/b -1:1` notation remains VDV XML-choice notation and is not treated as negative cardinality. The generic Common Subscribe/Unsubscribe structures remain valid authority context and are not promoted into a service-local missing-operation defect.

## Closure

EV-146 PASS; closure rerun PASS; EV-116 rerun PASS; all 50 XSDs PASS; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **114/192 terminal, 78 pending**. The first remaining pending frozen finding is `DRTIME10-001`; next block is `DRTIME10` (`TIME_V1.0_DRTIME10`).
