# Ticketing / TicketInformation V1.0 historical audit start

Status: historical provenance, public-document naming and release-context routing resolved for first pass. Local XSD compilation/sample validation remains pending.

Working branch base:

```text
MarcLeinenDE/VDV301 dev/schema-integration
13ee0d22a35606a1d4027b12081d03120bfc38c1
```

Scope:

```text
VDV 301-2-9 TicketingService V1.0, 07/2016
VDVde/VDV301 official tag VDV-301-1.0
VDVde/VDV301 official tags VDV-301-2.0 through VDV-301-2.3
IBIS-IP_TicketInformationService_V1.0.xsd
IBIS_IP_V1.0.xsd from the original V1.0 release
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

## 1. Public service name vs schema filename

The public VDV writing consistently describes the service as:

```text
TicketingService
```

The repository file is named:

```text
IBIS-IP_TicketInformationService_V1.0.xsd
```

However, the XSD types, groups and global elements use the executable prefix:

```text
TicketingService.*
TicketingServiceGroup
```

Therefore the filename is not the executable service name.

Initial classification:

```text
TKT-002
state: OK with note
mismatch_kind: file_name_vs_executable_service_name
validation_behavior: use TicketingService.* roots/types, never infer TicketInformationService.* aliases from filename
```

## 2. Two official blobs under the same V1.0 filename

Original official release tag:

```text
VDV-301-1.0
IBIS-IP_TicketInformationService_V1.0.xsd
blob 017ca64666e25d757fc0cde1f1be817f06a743fc
```

That service file contains the TicketingService-specific type/group definitions but not the full global operation-root set.

The same V1.0 release contains:

```text
IBIS_IP_V1.0.xsd
blob 41289eaed2674a169fdf77a10a2eff293c76d5c4
```

The aggregate includes the TicketInformationService-named file and declares the executable `TicketingService.*` roots and `TicketingServiceGroup`.

Later official release context:

```text
VDV-301-2.0 and later checked tags
IBIS-IP_TicketInformationService_V1.0.xsd
blob 3fda66d872ab0d1c511247f13e715cf3ad56afe7
```

This later file moves the `TicketingService.*` operation roots/group into the service XSD itself. `IBIS_IP_V1.0.xsd` is removed from the V2.0 release family.

The current `dev/schema-integration` file is byte-identical to the later official blob `3fda66d8...`.

Initial classification:

```text
TKT-001
state: confirmed provenance/routing ambiguity for a flat schema pool
mismatch_kind: schema_family_or_provenance_gap
validation_behavior: strict V1.0 routing requires release-context/schema-revision identity in addition to service version
```

No XSD is overwritten in this audit block.

## 3. Original V1.0 official family

Strict original-release profile:

```text
IBIS_IP_V1.0.xsd
  -> IBIS-IP_TicketInformationService_V1.0.xsd blob 017ca646...
  -> IBIS-IP_common_V1.0.xsd
  -> IBIS-IP_Enumerations_V1.0.xsd
```

Operation roots are aggregate-owned in this profile.

## 4. Later official V1.0 schema revision

Strict later-release profile observed from VDV-301-2.0 onward:

```text
IBIS-IP_TicketInformationService_V1.0.xsd blob 3fda66d8...
  -> IBIS-IP_common_V1.0.xsd
  -> IBIS-IP_Enumerations_V1.0.xsd
```

Operation roots are service-XSD-owned in this profile.

The service version remains V1.0 even though the schema packaging/root ownership changed.

## 5. Initial PDF/XSD mismatch candidates

The public PDF operation/table pass exposes the following candidates for detailed audit:

```text
TKT-003: UnsubscribeValidationResult response table says SubscribeResponseStructure.
TKT-004: ValidateTicket request detail table is labelled TicketInformationService.Validation.GetDataRequest.
TKT-005: GetValidationResult overview names TicketingService.ValidationResultStructure rather than the XSD response wrapper type.
TKT-006: tariff response-data table orders TimeStamp before DefaultLanguage; XSD xs:sequence requires DefaultLanguage before TimeStamp.
TKT-007: detailed GetValidationResult data table is labelled GetValidationResultResponseStructure although its fields match ValidationResultDataStructure.
TKT-008: PDF CardApplicationInformation vs XSD CardApplikationInformation spelling.
TKT-009: recurring TicketingSevice spelling in PDF table labels.
```

No XSD correction is implied by these observations.

## 6. Next file

```text
docs/pdf_xsd_semantic_audit/14a_ticketing_ticket_information_v1_0_pdf_xsd_first_pass.md
```
