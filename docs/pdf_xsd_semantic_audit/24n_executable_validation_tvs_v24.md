# EV-115 - TicketValidationService V2.4 candidate/integration evidence

Status: PASS

Date: 2026-08-29

## Authority warning

EV-115 is **candidate/integration evidence only**. No `VDV-301-2.4` release tag exists. Current upstream master contains TVS V2.4 but lacks the referenced Common V2.4 dependency. Therefore this run must not be described as official-release V2.4 XSD conformance.

## Executed exact family

```text
TVS V2.4     34b18b8c874e325dd923b366a72bb0ebee32e59e
Common V2.4  1946fd37e29ced605654f49ea3d98cd2fbbdc8e4
Enums V2.4   2afed8cf23afa91db92b0f043cc5b4ad428b0f25
```

## Run

```text
checker: tools/validate_tvs_v24_ev115.py
run: 33265239836
job: 99134041204
temporary head: 3abb516526328690f2ab4d8d93d7d2efc2a61468
result: PASS
```

## Confirmed

- exact candidate blobs matched and family compiled;
- ShortHaul global response and structures exist;
- ShortHaul global response is omitted from TicketValidationServiceOperations (TVS-001);
- ShortHaul response error branch validates;
- ShortHaul CurrentTariffStop is 0:*;
- ShortHaul and CurrentTariffStop CurrentTripRef use IBIS-IP.NMTOKEN;
- PDF spelling IBIS-IP.NMToken is unavailable and a negative probe fails compilation;
- RouteDeviation uses RouteDeviationEnumeration; onroute valid, Forward invalid;
- CurrentLine exact type is TicketValidationService.CurrentLineDataStructure;
- CurrentTariffStop response validates while stale CurrentStopPoint response has no global declaration.

## Separate upstream-master evidence

Upstream master TVS V2.4 blob `291f41518fd48cd9dcc9f285cf9b5fec7dd72159` separately shows the same TVS-001 structural omission and the same critical TVS declarations. That file is not executed here because the current upstream-master dependency set is incomplete.

No XSD changed.
