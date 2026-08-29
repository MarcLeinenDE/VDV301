# 24o — Executable validation COMMON V1.0 — EV-117

Status: PASS.

## Authority

Exact historical official V1.0 family:

```text
official import commit 604a5a5c7608977e483072f7e450d7381cc182e4
IBIS-IP_common_V1.0.xsd       194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
IBIS-IP_Enumerations_V1.0.xsd a9bea5bc73003ed91ded8519db06c32c4067831d
route                          Common V1.0 -> Enumerations V1.0
```

The official 05/2017 Common PDF is byte-pinned as `a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf` and carries an internal
document/data-definition revision `Version 1.1`. No `IBIS-IP_common_V1.1.xsd` was found.
EV-117 therefore does not invent a V1.1 schema authority.

## Execution

```text
Evidence ID: EV-117
checker:     tools/validate_common_v10_ev117.py
run:         33279461529
job:         99172025835
head tested: 104ff8d49af248258fcf174d62610c43179fdcf5
result:      PASS
```

An earlier controlled run `33279395750` / job `99171853097` failed only because the
positive Beacon/TSP test fixture omitted the required `Language` child of
`InternationalTextType`. The fixture was corrected; no XSD, finding or authority
classification was changed to obtain the PASS.

## Confirmed executable boundaries

EV-117 pins the exact Git blobs and confirms, among other checks:

- Connection V1.0 has required `DisplayContent`, typo-like `ExpectedDepatureTime`, no
  `ExpectedDepartureTime` and no `ScheduledDepartureTime`.
- TripInformation V1.0 has single optional `AdditionalTextMessage` of type
  `IBIS-IP.string`, no `RouteDirection`; Enumerations V1.0 has no `RouteDirectionEnumeration`.
- AdditionalAnnouncement uses optional `xs:choice`; omitted choice and `SpecificPoint`
  validate, PDF-only `InformationAtSpecificPoint` does not.
- DataAcceptedResponse uses an exclusive XSD choice; either branch validates, both together fail.
- empty DeviceSpecificationWithStateList, ServiceIdentificationWithStateList and
  ServiceSpecificationWithStateList validate.
- exact typo/case element names are enforced for BeaconPoint/TSPPoint and ServiceIdentification.
- historical enum lexemes are case-sensitive: `WheelChair`, `Other`, `other`, `valid`
  and `air` validate in their respective types while the checked PDF-side alternatives fail.
- `PassengerCountingService` and `starting` are not members of the exact V1.0
  ServiceName/ServiceState enumerations.

## Evidence-Gate boundary

EV-117 proves only the executable declarations and instance behaviour it tests. The
finding conclusions also rely on the independently frozen, byte-pinned Fresh Read in
`deep_read/COMMON_V1.0.md`. No XSD change is implied.
