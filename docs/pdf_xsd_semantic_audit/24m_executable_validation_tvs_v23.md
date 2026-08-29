# EV-114 - TicketValidationService V2.3 official-route / candidate authority guard

Status: PASS

Date: 2026-08-29

## Purpose

EV-114 protects the V2.3 resolver boundary. The official VDV-301-2.3 release routes TVS through the V2.2-named schema family, while `dev/schema-integration` separately contains a V2.3-named candidate/integration file. The test must not confuse semantic equality with provenance authority.

## Exact inputs

```text
official-route service: IBIS-IP_TicketValidationService_V2.2.xsd
blob: 5a4be2b2ba66860f035777ec0458dba0790880e1
Common V2.2: 468fee6d177e7185dbcd5d3f90cfb114e29e01ae
Enumerations V2.2: 2a23b512379b18e8f122ac1272cef8229fb86283

candidate/integration service: IBIS-IP_TicketValidationService_V2.3.xsd
blob: b17591c5b067254dd3e2260f3ef2acd2e18394a9
```

## Execution

```text
checker: tools/validate_tvs_v23_ev114.py
temporary head: ecaa7b51f5d78f950d329dd8166419ce6afad9a3
run: 33264437557
job: 99131891930
result: PASS
```

## Confirmed results

- all four exact repository blobs matched the expected identities;
- official-route and candidate service blobs are provenance-distinct;
- both service files include Common V2.2 + Enumerations V2.2 and compile;
- their critical TVS declarations currently match;
- official-route `VehicleData.RouteDeviation` is `RouteDeviationEnumeration`;
- official-route `CurrentTripRef` is `IBIS-IP.NMTOKEN`;
- official-route `CurrentLineData` type is `TicketValidationService.CurrentLineDataStructure`;
- official-route `GetCurrentTariffStopResponse` exists while stale `GetCurrentStopPointResponse` does not;
- `RouteDeviationEnumeration`: `onroute` valid, `Forward` invalid;
- `GetCurrentTariffStopResponse` sample valid, stale `GetCurrentStopPointResponse` sample invalid.

## Authority boundary

EV-114 does not by itself prove the official tag inventory; that provenance was independently established from tag `VDV-301-2.3` and the V2.3 PDF. EV-114 proves the repository-side identity/behavior consequences and guards against latest-filename-wins routing.

The branch V2.3-named file must remain candidate/integration authority unless separately promoted by an official release source.

No XSD was modified.
