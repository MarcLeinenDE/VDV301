# Runtime-mapping review — TicketingService V1.0 TKT-004 / TKT-006 / TKT-008 — 2026-09-21

Status: **review decision complete / not yet persisted into semantic registry at report creation**.

## Authority boundary

All three findings are scoped only to the **later official self-contained TicketInformationService V1.0 schema revision** carried by the official VDV-301-2.0 release context:

```text
release context: VDV-301-2.0
XSD file: IBIS-IP_TicketInformationService_V1.0.xsd
blob: 3fda66d872ab0d1c511247f13e715cf3ad56afe7
PDF: VDV 301-2-9 TicketingService V1.0
PDF SHA-256: 96241226c7a25b0384527dd3de5fcd9448c8e75f38bfb4ffd7b607680bfc6b43
```

The earlier official VDV-301-1.0 release carries a different blob at the same V1.0 file path. Therefore **service name + V1.0 alone is insufficient runtime authority**. No advisory in this block may be generalized to the earlier revision.

## TKT-004 — wrong ValidateTicket request root in PDF heading

Finding assessment remains **confirmed PDF defect**.

- PDF physical page 10: `TicketInformationService.Validation.GetDataRequest`
- selected XSD: `TicketingService.ValidateTicketRequest`
- EV-158: exact XSD root validates; PDF-heading-derived root is rejected.

Decision: `candidate -> reviewed`.

Runtime boundary: only decorate an existing XSD INVALID caused by the exact PDF-heading root in the exact later official V1.0 release context. No TicketInformationService alias and no automatic root rewrite.

## TKT-006 — GetTariffInformationResponse element order

Finding assessment remains **confirmed PDF defect**.

- PDF physical page 9: `TimeStamp -> DefaultLanguage`
- selected XSD `xs:sequence`: `DefaultLanguage -> TimeStamp -> TariffInformationGroup`
- EV-158: XSD-order prefix progresses to the next required business structure; PDF order is rejected at the misplaced field.

Decision: `candidate -> reviewed`.

Runtime boundary: only decorate the matching sequence failure inside `TicketingService.GetTariffInformationResponseDataStructure`. Do not label unrelated sequence errors as TKT-006 and never reorder the payload automatically.

## TKT-008 — CardApplicationInformation vs CardApplikationInformation

Finding assessment remains **confirmed PDF defect**.

- PDF physical page 11: `CardApplicationInformation`
- selected XSD / `CardApplikationValidation`: `CardApplikationInformation`
- EV-158: XSD spelling validates; PDF spelling is rejected.

Decision: `candidate -> reviewed`.

Runtime boundary: only decorate the exact rejected `CardApplicationInformation` element in the `CardApplikationValidation` context. The XSD spelling remains mandatory for PASS/FAIL; no alias or normalization is permitted.

## Expected mapping inventory after persistence

```text
reviewed        64
candidate       14
not_designed     0
not_applicable 114
implemented      0
```

No executable matcher is implemented in this review block and no XSD is changed.
