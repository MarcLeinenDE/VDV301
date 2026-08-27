# TicketingService validation backlog addendum

Status: local technical validation pending.

## TKT-VB-001 - original V1.0 release family compile

```text
IBIS_IP_V1.0.xsd
IBIS-IP_TicketInformationService_V1.0.xsd blob 017ca646...
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

Goal: verify aggregate-owned TicketingService roots and complete include closure.

## TKT-VB-002 - later official V1.0 service revision compile

```text
IBIS-IP_TicketInformationService_V1.0.xsd blob 3fda66d8...
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

Goal: verify self-contained TicketingService group/roots and dependency closure.

## TKT-VB-003 - tariff response sequence order

```text
positive: DefaultLanguage then TimeStamp
negative: TimeStamp then DefaultLanguage as printed in PDF table
```

## TKT-VB-004 - ValidateTicket naming

```text
positive root: TicketingService.ValidateTicketRequest
negative/unsupported alias: TicketInformationService.Validation.GetDataRequest
```

## TKT-VB-005 - validation result wrapper/data distinction

Validate the outer `GetValidationResultResponseStructure` choice and nested `ValidationResultDataStructure` separately.

## TKT-VB-006 - spelling sensitivity

```text
positive: CardApplikationInformation
negative: CardApplicationInformation
```

## TKT-VB-007 - resolver identity

Prove that the future resolver can distinguish:

```text
TicketingService V1.0 + release_context=VDV-301-1.0
TicketingService V1.0 + release_context=VDV-301-2.0+
```

without silently promoting one blob to universal V1.0 authority.

No task in this addendum has been executed yet.
