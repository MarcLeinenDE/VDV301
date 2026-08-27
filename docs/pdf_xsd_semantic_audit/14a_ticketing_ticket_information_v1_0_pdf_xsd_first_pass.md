# Ticketing / TicketInformation V1.0 PDF-XSD first pass

Status: semantic/provenance first pass completed. Local XSD compilation and targeted XML validation remain pending.

Source starter:

```text
docs/pdf_xsd_semantic_audit/14_ticketing_ticket_information_service_historical_start.md
```

Public source checked:

```text
VDV-Schrift 301-2-9
Dienst TicketingService V1.0
07/2016
```

## 1. Executable service identity

Despite the schema filename `IBIS-IP_TicketInformationService_V1.0.xsd`, both official schema revisions use:

```text
TicketingService.SetRazziaRequest
TicketingService.GetTariffInformationResponse
TicketingService.RetrieveTariffInformationRequest
TicketingService.RetrieveTariffInformationResponse
TicketingService.ValidateTicketRequest
TicketingService.ValidateTicketResponse
TicketingService.GetValidationResult
TicketingServiceGroup
```

Result:

```text
TKT-002: OK with note.
Resolver/service identity = TicketingService.
Filename token TicketInformationService is provenance metadata only and must not become an XML prefix alias.
```

## 2. TKT-001 - same service version, two official release-tag schema revisions

Observed official blobs:

```text
VDV-301-1.0 -> IBIS-IP_TicketInformationService_V1.0.xsd -> 017ca64666e25d757fc0cde1f1be817f06a743fc
VDV-301-2.0 -> same filename -> 3fda66d872ab0d1c511247f13e715cf3ad56afe7
VDV-301-2.1 -> same later blob
VDV-301-2.2 -> same later blob
VDV-301-2.3 -> same later blob
```

The original V1.0 release also supplies operation roots through `IBIS_IP_V1.0.xsd`. The later revision moves them into the service file and removes the aggregate from the later release family.

Classification:

```text
mismatch_kind: schema_family_or_provenance_gap
classification_confidence: high
final_handling_bucket: resolver_profile_requirement
```

SDK implication:

```text
service=TicketingService, version=1.0 is not sufficient to identify one historical schema blob.
A strict historical profile needs release_context/schema_revision as an additional selector.
```

## 3. Core operation comparison

PDF operation concepts:

```text
SetRazzia
GetCurrentTariffInformation
SubscribeCurrentTariffInformation
UnsubscribeCurrentTariffInformation
RetrieveTariffInformation
ValidateTicket
GetValidationResult
SubscribeValidationResult
UnsubscribeValidationResult
```

The concrete service-specific XSD roots use shortened root names for the current tariff get response:

```text
TicketingService.GetTariffInformationResponse
```

and model subscription requests/responses through the shared Common V1.0 structures rather than dedicated service-specific XSD roots.

This mirrors the generic subscription modelling already observed in other VDV301 services and is not opened as a separate defect in this block.

## 4. TKT-003 - UnsubscribeValidationResult response type

PDF operation table:

```text
UnsubscribeValidationResult
Req.: UnsubscribeRequestStructure
Resp.: SubscribeResponseStructure
```

In the same operation table, `UnsubscribeCurrentTariffInformation` correctly uses:

```text
UnsubscribeRequestStructure
UnsubscribeResponseStructure
```

The detailed UnsubscribeValidationResult section says the shared VDV 301-2-1 unsubscribe structures are used.

Classification:

```text
mismatch_kind: shared_response_type_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
validation_behavior: follow the selected Common V1.0 generic unsubscribe model
```

No compatibility alias is created.

## 5. TKT-004 - ValidateTicket request legacy/wrong heading

Operation overview and XSD identify the request as:

```text
TicketingService.ValidateTicketRequestStructure
TicketingService.ValidateTicketRequest
```

The detailed PDF request table is titled:

```text
TicketInformationService.Validation.GetDataRequest
```

and the table directory repeats that title.

The actual fields under that table align with `TicketingService.ValidateTicketRequestStructure`:

```text
CardType
CardApplInformation
NumberOfCardTicketDataBlocks
CardTicketDataBlock
```

Classification:

```text
mismatch_kind: label_or_heading
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: high
validation_behavior: executable XSD name remains TicketingService.ValidateTicketRequest
```

## 6. TKT-005 - GetValidationResult overview response type

PDF operation overview:

```text
GetValidationResult Resp. TicketingService.ValidationResultStructure
```

Executable XSD:

```text
TicketingService.GetValidationResult
  type=TicketingService.GetValidationResultResponseStructure
```

The detailed PDF response section also uses `TicketingService.GetValidationResultResponse` wording.

Classification:

```text
mismatch_kind: response_type_name
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
```

## 7. TKT-006 - tariff-response element order

PDF `GetTariffInformationResponseDataStructure` table order:

```text
TimeStamp
DefaultLanguage
TripRef
Line
StopPointTariffInformation
ShortTripStopList
```

Both checked official XSD revisions define an `xs:sequence` beginning:

```text
DefaultLanguage
TimeStamp
TariffInformationGroup
```

Because XML Schema sequence order is executable, this is not cosmetic.

Classification:

```text
mismatch_kind: sequence_order
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: high
validation_behavior: DefaultLanguage must precede TimeStamp for the selected XSD
```

Local positive/negative samples remain required before technical closure.

## 8. TKT-007 - GetValidationResult detailed table heading

The detailed PDF table labelled:

```text
TicketingService.GetValidationResultResponseStructure
```

contains only:

```text
TimeStamp
ValidationResult
```

Those fields correspond to the XSD type:

```text
TicketingService.ValidationResultDataStructure
```

The actual XSD `GetValidationResultResponseStructure` is the outer choice wrapper:

```text
ValidationResultData
or
OperationErrorMessage
```

Classification:

```text
mismatch_kind: label_or_heading
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: high
```

## 9. TKT-008 - CardApplicationInformation spelling

PDF table:

```text
CardApplicationInformation
```

XSD group `CardApplikationValidation`:

```text
CardApplikationInformation
```

The XSD spelling is internally consistent with the group name and is present in both official schema revisions checked.

Classification:

```text
mismatch_kind: element_name_spelling
likely_source_issue: pdf_table_or_documentation_error_candidate
classification_confidence: medium-high
validation_behavior: exact XSD spelling CardApplikationInformation
```

This is not classified as an XSD typo candidate in this pass because `Applikation` is an intentional German-language spelling and is internally consistent in the schema.

## 10. TKT-009 - recurring TicketingSevice PDF spelling

Several PDF detail tables use:

```text
TicketingSevice
```

while the service title, operation overview and XSD consistently use:

```text
TicketingService
```

Classification:

```text
mismatch_kind: heading_spelling
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: high
validation_behavior: no alias
```

## 11. Original V1.0 SetRazzia orphan-type note

The original `VDV-301-1.0` service-type XSD contains service-specific types:

```text
TicketingService.SetRazziaResponseStructure
TicketingService.SetRazziaResponseDataStructure
```

but the official V1.0 aggregate operation layer exposes only `TicketingService.SetRazziaRequest`; the PDF specifies the shared `DataAcceptedResponseStructure` for the response. The later official V1.0 schema revision removes those unused service-specific response types.

This is recorded as historical modelling context under TKT-001 rather than opened as another correction finding.

## 12. Technical validation backlog

```text
TKT-VB-001: compile original VDV-301-1.0 aggregate family including blob 017ca646....
TKT-VB-002: compile later self-contained V1.0 service blob 3fda66d8... with Common/Enums V1.0.
TKT-VB-003: positive tariff response with DefaultLanguage before TimeStamp.
TKT-VB-004: negative tariff response with PDF table order TimeStamp before DefaultLanguage.
TKT-VB-005: positive ValidateTicket request using TicketingService.ValidateTicketRequest and XSD field names.
TKT-VB-006: negative sample using TicketInformationService.Validation.GetDataRequest as an XML root/alias.
TKT-VB-007: positive GetValidationResult wrapper and nested ValidationResultData structure.
TKT-VB-008: negative sample using CardApplicationInformation where XSD requires CardApplikationInformation.
TKT-VB-009: resolver test proving original-release and later-release V1.0 profiles remain distinguishable.
```

No local validation task above is claimed as executed.
