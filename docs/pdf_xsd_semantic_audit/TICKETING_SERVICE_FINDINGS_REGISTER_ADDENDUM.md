# TicketingService findings register addendum

Status: supplemental register; V1.0 historical semantic/provenance first-pass closure completed.

Authority rule:

```text
Validation follows the selected official XSD release-context family.
The XSD filename token TicketInformationService is not an executable XML service alias.
PDF table/heading discrepancies do not alter accepted XML names, types or sequence order.
```

## TKT-001 - same V1.0 path, two official release-tag blobs

```text
classification: schema_family_or_provenance_gap
confidence: high
version_scope: TicketingService V1.0
original_release_blob: 017ca64666e25d757fc0cde1f1be817f06a743fc
later_release_blob: 3fda66d872ab0d1c511247f13e715cf3ad56afe7
validation_behavior: select by release_context/schema_revision, not version alone
final_handling_bucket: resolver_profile_requirement
```

## TKT-002 - filename vs executable service name

```text
classification: ok_with_note
confidence: high
filename: IBIS-IP_TicketInformationService_V1.0.xsd
executable_identity: TicketingService
validation_behavior: TicketingService.* only
```

## TKT-003 - UnsubscribeValidationResult response table

```text
PDF: SubscribeResponseStructure
shared unsubscribe model: UnsubscribeResponseStructure
classification: pdf_table_or_documentation_error_candidate
confidence: high
validation_behavior: selected Common V1.0 structures
```

## TKT-004 - ValidateTicket request heading

```text
PDF: TicketInformationService.Validation.GetDataRequest
XSD: TicketingService.ValidateTicketRequest / TicketingService.ValidateTicketRequestStructure
classification: pdf_label_or_heading_error_candidate
confidence: high
validation_behavior: exact XSD root/type
```

## TKT-005 - GetValidationResult overview response type

```text
PDF: TicketingService.ValidationResultStructure
XSD: TicketingService.GetValidationResultResponseStructure
classification: pdf_table_or_documentation_error_candidate
confidence: high
```

## TKT-006 - tariff response sequence order

```text
PDF: TimeStamp -> DefaultLanguage
XSD: DefaultLanguage -> TimeStamp
classification: pdf_table_or_documentation_error_candidate
mismatch_kind: sequence_order
confidence: high
validation_behavior: XSD xs:sequence order
```

## TKT-007 - GetValidationResult detailed table heading

```text
PDF heading: TicketingService.GetValidationResultResponseStructure
PDF fields: TimeStamp, ValidationResult
XSD field-owner: TicketingService.ValidationResultDataStructure
classification: pdf_label_or_heading_error_candidate
confidence: high
```

## TKT-008 - CardApplicationInformation spelling

```text
PDF: CardApplicationInformation
XSD: CardApplikationInformation
classification: pdf_table_or_documentation_error_candidate
confidence: medium-high
validation_behavior: exact XSD spelling
```

## TKT-009 - TicketingSevice spelling in PDF labels

```text
PDF: TicketingSevice
XSD/service title: TicketingService
classification: pdf_label_or_heading_error_candidate
confidence: high
validation_behavior: no alias
```
