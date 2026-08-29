# Deep Read - TicketValidationService V2.4

Document ID: `TVS_V2.4`

Status: `needs_visual_review`

Date: 2026-08-29

## Official PDF source

```text
URL: https://www.vdv.de/301-2-16-sde-v2.4-ticketvalidationservice.pdfx
sha256: e7caca3de444b3eca15d539572cd4b896e56e5bb608b4827211b51be0ad56c51
size: 864860 bytes
pin run: 33264912909
pinned_at_utc: 2026-08-29T17:10:21Z
```

The PDF is official VDV documentation. Chapter 3 explicitly states that the XSD is master when description and XSD differ.

## V2.4 authority split

There is no upstream `VDV-301-2.4` release tag. Current upstream master head `14880bb33beec5c5dffe96315b730bd6c094a585` contains TVS V2.4 blob `291f41518fd48cd9dcc9f285cf9b5fec7dd72159`, merged through PRs #23/#26. It references Common V2.4 + Enumerations V2.2, but current upstream master does not contain the referenced Common V2.4 file. Therefore the current upstream-master family is dependency-incomplete and is not treated like an exact release-tag family.

For executable Deep-Read comparison the complete candidate/integration family is:

```text
IBIS-IP_TicketValidationService_V2.4.xsd  34b18b8c874e325dd923b366a72bb0ebee32e59e
IBIS-IP_common_V2.4.xsd                   1946fd37e29ced605654f49ea3d98cd2fbbdc8e4
IBIS-IP_Enumerations_V2.4.xsd             2afed8cf23afa91db92b0f043cc5b4ad428b0f25
```

This family is candidate/integration authority only. EV-115 success is not official-release V2.4 conformance.

## Independent fresh-read method

The PDF was fresh-read before historical V2.4 findings were opened. Interactive screenshots returned cache miss. Exact pinned bytes were rendered with the repository fallback. The independent pre-history state was permanently frozen at commit `f50e347a0584c751e3a4f84eecea687eff051fda`.

## Visual evidence

```text
render run: 33265061000
render job: 99133563822
artifact: 9718391355
artifact digest: sha256:03a308e9ac1f792ec074020a633e83ab58973c90573e982b58e4731466f72781
rendered pages: 4, 10-19
visibly reviewed material pages: 4, 10, 14, 15, 16, 17, 18, 19
dpi: 180
```

Targeted review only; not exhaustive.

## Fresh observations before historical reconciliation

- The foreword explicitly says V2.4 adds the short-haul operation and “requires new XSD 2.4”.
- German/English operation overviews still use CurrentStopPoint-era names, while adding GetCurrentShortHaulStops.
- German/English functional-sequence prose still says SubscribeCurrentStop.
- Chapter 3.1 is GetCurrentTariffStop but response/table labels and list of tables still say GetCurrentStopPointResponse / CurrentStopPointData.
- CurrentTripRef is printed as IBIS-IP.NMToken in both CurrentTariffStopData and the new ShortHaul data.
- GetCurrentLine again prints TicketValidationServiceCurrentLineData without the service-name separator dot.
- VehicleData.RouteDeviation is printed with RouteDirectionEnumeration.
- The new GetCurrentShortHaulStops section visibly defines the new response and CurrentShortHaulStopsData, with CurrentTariffStop 0:* and CurrentTripRef 0:1.
- Version history introduces GetCurrentShortHaulStops and retains the earlier CurrentTariffStop rename/correction history.
- Visible -1:1 entries are VDV choice notation, not invalid cardinality.

## Historical reconciliation

### TVS-001 - ShortHaul response omitted from TicketValidationServiceOperations

The official PDF provides independent context that GetCurrentShortHaulStops is a real new V2.4 operation and requires XSD 2.4.

Current upstream master TVS V2.4 structurally declares `TicketValidationService.GetCurrentShortHaulStopsResponse` and its response/data structures, but omits that global response from `TicketValidationServiceOperations`. Its current dependency family is incomplete, so no upstream-master compile claim is made.

EV-115 independently confirms on the complete candidate/integration family:

```text
ShortHaul global response exists
ShortHaul response/data structures exist
ShortHaul response omitted from TicketValidationServiceOperations
ShortHaul global response error branch -> valid
CurrentTariffStop in ShortHaul data -> 0:*
CurrentTripRef -> IBIS-IP.NMTOKEN
```

State: `upstream_master_structurally_confirmed_and_candidate_integration_executable_confirmed_EV-115`.

### TVS-002 - RouteDeviation type mismatch

Official V2.4 PDF visibly prints `RouteDirectionEnumeration`; upstream master service and candidate/integration service declare `RouteDeviationEnumeration`. EV-115 confirms candidate V2.4 enum separation: `onroute` valid, `Forward` invalid as RouteDeviation.

State: `candidate_integration_executable_confirmed_EV-115_with_upstream_master_declaration_correspondence`.

### TVS-003 - stale CurrentStopPoint names

Official V2.4 PDF visibly retains CurrentStopPoint-era overview/response/table names despite CurrentTariffStop detailed naming and version history. Upstream master service and candidate service use the CurrentTariffStop root. EV-115 validates the new root and rejects the stale root.

State: `candidate_integration_executable_confirmed_EV-115_with_official_pdf_context`.

### DRTVS21-001..003 scope

DRTVS21-001 recurs twice in V2.4 (`IBIS-IP.NMToken`); EV-115 confirms exact candidate type `IBIS-IP.NMTOKEN` and rejects the PDF spelling as an unavailable type. DRTVS21-002 and DRTVS21-003 also recur and are context-verified with the same boundaries used in earlier versions.

No new V2.4-only finding ID is necessary after deduplication.

## EV-115 provenance

```text
evidence: EV-115
checker: tools/validate_tvs_v24_ev115.py
run: 33265239836
job: 99134041204
tested temporary head: 3abb516526328690f2ab4d8d93d7d2efc2a61468
result: PASS
authority: candidate/integration only
```

The checker itself prints an authority guard and the temporary workflow was removed after execution. No XSD was modified.

## Completion

```text
textual fresh read: complete
targeted visible review: complete for material pages
exhaustive visual review: no
Deep Read state: needs_visual_review
```

The TicketValidationService V2.1-V2.4 Deep Read sequence is complete. No remediation or upstream action is authorized by this block.

Next natural target: `HDS_V2.1`.
