# 24p — Executable validation COMMON V2.0 — EV-118

Status: PASS.

## Authority

```text
official tag:                  VDV-301-2.0
IBIS-IP_common_V2.0.xsd        8608e3dcd665c197c34da7f6ec6af5a3758da164
IBIS-IP_Enumerations_V2.0.xsd  27e3c183b00381d959622d13c10543123af8eef6
route:                         Common V2.0 -> Enumerations V2.0
branch bytes:                  exact match to official tag
```

## Execution

```text
Evidence ID: EV-118
checker:     tools/validate_common_v20_ev118.py
run:         33280224191
job:         99174026383
head tested: f048cc6ac896c0eb9885999ee5c9e1d3c91d7e77
result:      PASS
```

## Confirmed boundaries

EV-118 confirms the exact V2.0 family compiles and, among its targeted checks:

- `InternationalTextType.Value` is `xs:string` and `Language` is `xs:language`;
  flat primitive-shaped content validates while the PDF-implied IBIS-IP wrapper-shaped
  Value/Language content fails.
- `AdditionalAnnouncement` is an optional XSD choice; `SpecificPoint` validates and
  PDF-only `InformationAtSpecificPoint` fails.
- `DataAcceptedResponse` is an exclusive choice: either branch alone validates; both fail.
- empty `DataVersionList` and the three checked WithState lists validate.
- `TripInformation.AdditionalTextMessage` has effective maxOccurs=1 in exact XSD;
  this check is declaration evidence, not a separately constructed full TripInformation repeat probe.
- BeaconPoint/TSPPoint `Desciption` is accepted while `Description` is rejected.
- ServiceIdentification outer `Service` validates while PDF outer `ServiceName` fails.
- exact enum lexemes `WheelChair`, `Other`, `other`, `valid`, `air` validate while the
  corresponding checked PDF-side variants fail.
- V2.0 corrections/additions such as `ExpectedDepartureTime`, `ScheduledDepartureTime`,
  `RouteDirectionEnumeration`, `readyForShutdown`, PassengerCounting/video service names
  and `starting` are positively present and are not carried forward as defects.

EV-118 does not modify the official XSD and does not turn PDF notation into executable authority.
