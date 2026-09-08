# Finding Revalidation — LS / Location Services V1.0

Date: 2026-09-08  
Scope: `LS-001` … `LS-003`  
Evidence: `EV-153`, successful run `34229647400`, job `102072276013`  
Evidence commit: `45eeed958b3f7f1081f19d6858e54a27824c682f`  
Artifact: `10057222866`, `sha256:914a1b126e8c06145fe0ccc896f4e2a85db5204a7562ad7dada21ad660fecff7`  
Closure run: `34230809592`

## Authority route

The official VDV 301-2-2 BeaconLocationService, 301-2-4 DistanceLocationService, 301-2-5 GNSSLocationService and 301-2-7 NetworkLocationService V1.0 PDFs were freshly fetched and byte-pinned by run `34228583786`. Executable validation remains service/version exact: four separate V1.0 service schemas, each with Common V1.0 and Enumerations V1.0. No latest-wins substitution is permitted. All 50 root XSDs passed unchanged.

Fresh 180-DPI renders of BLS pages 7/8 and DLS/GNSS/NLS page 7 were manually inspected before closure.

## LS-001 — executable_confirmed

GNSS V1.0 PDF page 7 visibly prints `HorizontalDilutionOfPrecision`. Exact `IBIS-IP_GNSSLocationService_V1.0.xsd` instead defines `HoriziontalDilutionOfPrecision`. EV-153 accepts the XSD spelling and rejects the PDF spelling. This is a real PDF/XSD spelling discrepancy; selected XSD behavior remains normative. No schema correction is made by this audit closure.

## LS-002 — contextual_not_defect

Distance V1.0 PDF page 7 and exact XSD both use `Odometer-Pulses`. EV-153 accepts the exact hyphenated XML element and rejects the normalized alias `OdometerPulses`. The finding survives only as an implementation note: tooling must preserve the exact XML name.

## LS-003 — contextual_not_defect

The Location Services intentionally use service-specific root modelling. Beacon uses `BeaconLocationService.GetDataResponse` with a Data/OperationErrorMessage choice, while Distance, GNSS and Network expose raw `*.Data` roots. EV-153 confirms positive samples on their own service schemas and cross-schema rejection. A validator must route by the exact service/version schema and must not normalize these services to one generic root pattern.

## Fail-closed history and closure

The first EV-153 run (`34229230088`) failed only because `pdftotext -layout` split the long GNSS identifier during a textual evidence assertion. Authority guards and PDF pin checks had already passed. Commit `45eeed958b3f7f1081f19d6858e54a27824c682f` added robust raw-text extraction; the successful rerun changed no finding classification, XSD, or frozen inventory.

EV-153 PASS; fresh visual evidence manually inspected; complete 50-root XSD regression PASS; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **135/192 terminal, 57 pending**. The first remaining pending finding is `NET-001`; next block is `NET`.
