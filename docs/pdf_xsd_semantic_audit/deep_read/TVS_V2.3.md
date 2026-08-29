# Deep Read - TicketValidationService V2.3

Document ID: `TVS_V2.3`

Status: `needs_visual_review`

Date: 2026-08-29

## Source authority

Official VDV writing:

```text
https://www.vdv.de/301-2-16-sdes-v2-3-ticketvalidation.pdfx
```

Pinned source:

```text
source_id: TVS_V2.3
sha256: 74d9fd279e13f2661be24319c414ef9128b61c8fc6f30ea62b63f92f94ddbff4
size: 404383 bytes
pin run: 33258484479
pinned_at_utc: 2026-08-29T14:46:39Z
```

The PDF is official documentation evidence. Executable XML validation follows the selected official XSD family.

## Exact official XSD authority

Official upstream tag: `VDV-301-2.3`.

The tag contains no `IBIS-IP_TicketValidationService_V2.3.xsd`. The official V2.3 route is:

```text
IBIS-IP_TicketValidationService_V2.2.xsd
  blob 5a4be2b2ba66860f035777ec0458dba0790880e1
IBIS-IP_common_V2.2.xsd
  blob 468fee6d177e7185dbcd5d3f90cfb114e29e01ae
IBIS-IP_Enumerations_V2.2.xsd
  blob 2a23b512379b18e8f122ac1272cef8229fb86283
```

The V2.3 PDF itself states that the corrected description corresponds to XSD V2.2 and that no XSD update is necessary.

## Candidate/integration separation

`dev/schema-integration` also contains:

```text
IBIS-IP_TicketValidationService_V2.3.xsd
blob b17591c5b067254dd3e2260f3ef2acd2e18394a9
introduced by c9c086ac07f7e9bdb271c54f7a274e3cf0d03749
```

It is candidate/integration material, not historical official V2.3 release authority. Filename recency must not override provenance.

## Fresh-read method

Historical V2.3 TicketValidation findings were not reopened until the PDF was byte-pinned, the official tag route was independently established, the document was read afresh, material pages were rendered from the exact pinned bytes and visually inspected, and the fresh observations were committed separately.

The independent pre-history snapshot is commit `f01099f284f753a0bbbc5ce5c03fa046c9a1bb80`.

## Visual evidence

```text
render run: 33258612417
render job: 99116563806
artifact id: 9716575205
artifact digest: sha256:0cba4a211c323be415e26120eecda08c1453cce0df18e4ec373a108e22b56c74
rendered pages: 10-19
visibly reviewed: 10-16, 18-19
dpi: 180
source sha256 verified: 74d9fd279e13f2661be24319c414ef9128b61c8fc6f30ea62b63f92f94ddbff4
```

The review is targeted, not exhaustive.

## Independent fresh observations before historical reconciliation

1. The V2.3 foreword says chapter 3.1.2 was corrected so the data tables correspond to the data definitions in XSD V2.2.
2. The version history says the description is now in line with XSD and no XSD update is necessary.
3. German and English operation overviews nevertheless still use `GetCurrentStopPoint`, `SubscribeCurrentStopPoint`, `UnsubscribeCurrentStopPoint`.
4. German and English functional-sequence prose still says `SubscribeCurrentStop`.
5. Chapter 3.1 is `GetCurrentTariffStop` and its structure body uses `CurrentTariffStopData` / `CurrentTariffStop`, but the response/table labels still say `GetCurrentStopPointResponse` / `CurrentStopPointData`.
6. The list of tables independently repeats those stale names.
7. `CurrentTripRef` is printed as `IBIS-IP.NMToken`; the official route uses `IBIS-IP.NMTOKEN`.
8. The GetCurrentLine response display again prints `TicketValidationServiceCurrentLineData` without the service-name separator dot.
9. `VehicleData.RouteDeviation` is printed with `RouteDirectionEnumeration`; the official route uses `RouteDeviationEnumeration`.

## Historical reconciliation after the independent fresh read

### TVS-002 - RouteDeviation PDF type vs XSD type

V2.3 independently reproduces the PDF-side `RouteDirectionEnumeration` label. The official release route is the exact unchanged V2.2 family where `VehicleData.RouteDeviation` is `RouteDeviationEnumeration`.

EV-114 confirms on that official route:

```text
onroute as RouteDeviationEnumeration -> valid
Forward as RouteDeviationEnumeration -> invalid
```

State: `executable_confirmed_EV-114`.

No compatibility alias is allowed.

### TVS-003 - stale CurrentStopPoint names after CurrentTariffStop rename

V2.3 sharpens the finding because the document explicitly claims the affected description was corrected to be in line with XSD V2.2, yet visible stale names remain in the response/table labels and list of tables.

EV-114 confirms:

```text
TicketValidationService.GetCurrentTariffStopResponse sample -> valid
TicketValidationService.GetCurrentStopPointResponse sample -> invalid; no matching global declaration
```

State: `executable_confirmed_EV-114_with_context_refinement`.

### DRTVS21-001 - CurrentTripRef type identifier case

V2.3 visibly repeats `IBIS-IP.NMToken`. The official route is blob-identical to the V2.2 family. EV-114 reconfirms the exact XSD declaration `IBIS-IP.NMTOKEN`; EV-113 already executed the case-sensitive unavailable-type negative probe against the identical blobs.

V2.3 scope is therefore revalidated without inventing a new finding ID.

### DRTVS21-002 - CurrentLineData missing separator dot

V2.3 visibly repeats `TicketValidationServiceCurrentLineData`. EV-114 reconfirms exact XSD type `TicketValidationService.CurrentLineDataStructure`. The finding remains limited to the missing service-name separator dot; omission of `Structure` is not independently classified.

### DRTVS21-003 - SubscribeCurrentStop

V2.3 functional-sequence text repeats `SubscribeCurrentStop`, while the detailed CurrentTariffStop-era operation is `SubscribeCurrentTariffStop`. Context disproves a second formal operation with the truncated name.

## Revalidated routing note

```text
VDV 301-2-16 V2.3 is a documentation-correction release.
Official tag VDV-301-2.3 provides IBIS-IP_TicketValidationService_V2.2.xsd, not a V2.3-named service XSD.
The PDF explicitly says no XSD update is necessary.
Official TVS V2.3 routing therefore uses the exact V2.2 service/Common/Enumerations family.
```

EV-114 additionally proves that the separate branch V2.3-named candidate currently matches the critical declarations but remains provenance-distinct. Semantic equality is not authority equivalence.

## EV-114 provenance

```text
evidence: EV-114
checker: tools/validate_tvs_v23_ev114.py
run: 33264437557
job: 99131891930
tested temporary head: ecaa7b51f5d78f950d329dd8166419ce6afad9a3
result: PASS
```

The temporary workflow was removed after execution. No XSD changed.

## Deduplication result

No V2.3-only finding ID was opened. TVS-002/TVS-003 are revalidated and DRTVS21-001..003 receive V2.3 scope extensions. DRTVS21-004 is not scope-extended because generic spelling residue has no SDK/validation consequence requiring a version-wide duplicate.

## Completion state

```text
textual fresh read: complete
targeted visible review: complete for material pages
exhaustive visual review: no
Deep Read state: needs_visual_review
```

This block authorizes no schema remediation or upstream action.

Next natural Deep Read target: `TVS_V2.4`.
