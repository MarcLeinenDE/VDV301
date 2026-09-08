# Finding Revalidation — JIS / JourneyInformationService V1.0

Date: 2026-09-08  
Scope: `JIS-001` … `JIS-005`  
Evidence: `EV-152`, successful run `34113437268`, job `101714662141`  
Evidence commit: `4da900b4acf993b14bdfbe5f48e0fb386fbad3fe`  
Artifact: `10015273758`, `sha256:338e3fb679a8375c98fba359a3478d4cf7ba0968f3e97c08209ce52c0d23dc65`  
Closure run: `34224429423`

## Authority route

The official VDV 301-2-6 JourneyInformationService V1.0 PDF was re-fetched and byte-pinned at SHA-256 `424181b4932e18b6ac059843fa3978fdcc07a9c6acb553f9fbe8b71ef583da73` / 772125 bytes. The exact executable authority is the historical route `JIS V1.0 -> Common V1.0 -> Enumerations V1.0`. All 50 root XSDs passed unchanged.

Fresh 180-DPI renders of physical pages 9, 11, 12, 13, 17, 19 and 22 were manually inspected before closure.

## JIS-001 — contextual_not_defect

The apparent missing JIS-local Subscribe/Unsubscribe schema surface is intentional shared modelling. The PDF operation overview uses the generic Subscribe/Unsubscribe request and response structures; sections 1.4/1.5 and 1.7/1.8 explicitly delegate them to VDV 301-2-1. Exact Common V1.0 defines those structures. No JIS-local alias is inferred.

## JIS-002 — contextual_not_defect

The seven JIS `Set*` operations have local request structures, while their positive response uses the shared `DataAcceptedResponseStructure` shown by the PDF and defined in exact Common V1.0. The lack of JIS-local `Set*Response` roots is not a schema defect.

## JIS-003 — executable_confirmed

PDF table 29 visibly specifies `LineInformation` as `1:*`. Exact `JourneyInformationService.AllLineInformationData` declares `LineInformation` without `maxOccurs`, so XML Schema default `maxOccurs=1` applies. EV-152 accepts a one-entry instance and rejects an otherwise equivalent two-entry instance. This is a real PDF/XSD cardinality mismatch; selected XSD behavior remains normative.

## JIS-004 — context_verified

In section 1.22 `RetrieveAllRoutesPerLine`, table 38 visibly labels the request as `JourneyInformationService.SetBlockNumberRequest` even though the row contains `LineRef`. Section 1.23 separately defines the actual SetBlockNumber request with `BlockRef`. Exact XSD defines `JourneyInformationService.RetrieveAllRoutesPerLineRequest` with `LineRef`. This is a documentation copy/paste label defect only.

## JIS-005 — executable_confirmed

PDF table 21 visibly names the successful choice row `SpecificGNSSPointInformationData`; table 22 then defines the Data-suffixed structure. Exact XSD instead requires choice element `SpecificGNSSPointInformation` typed as `JourneyInformationService.SpecificGNSSPointInformationData`. EV-152 accepts the XSD element name and rejects the PDF Data-suffixed element name. Selected XSD behavior remains normative.

## Fail-closed history and closure

The first EV-152 run (`34113029896`) failed before completion; commit `4da900b4acf993b14bdfbe5f48e0fb386fbad3fe` hardened the global operation locator. The successful rerun changed no finding classification, XSD, or frozen inventory.

EV-152 PASS; all seven visual pages inspected; complete 50-root XSD regression PASS; frozen 192-finding inventory unchanged; no XSD mutation. Revalidation count is now **132/192 terminal, 60 pending**. The first remaining pending finding is `LS-001`; next block is `LS`.
