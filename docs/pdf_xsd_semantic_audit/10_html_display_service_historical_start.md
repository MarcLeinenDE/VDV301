# HTMLDisplayService historical audit start

Status: historical first pass started from branch head `1e4e690a25dff05dd6b75ba33173427b558340f8`; public PDF versions and official repository XSD pools checked. No dedicated HTMLDisplayService XSD has been found and the service documentation indicates this is intentional service modelling rather than a schema-provenance gap.

Scope:

```text
VDV 301-2-17 HTMLDisplayService V2.1 (07/2018)
VDV 301-2-17 HTMLDisplayService V2.2 (08/2019)
VDV 301-2-17 HTMLDisplayService V2.2a (02/2021)
official VDVde/VDV301 release-tag XSD pools V2.1, V2.2 and V2.3
current VDVde/VDV301 repository
MarcLeinenDE/VDV301 dev/schema-integration
```

## 1. Authority and routing policy

The general audit rule remains:

```text
If an executable XSD exists for the selected service/version family, validation follows that XSD.
Do not create an XSD merely because a public service document exists.
Do not map a non-XSD service to a neighbouring or latest schema family.
```

For HTMLDisplayService the first question is therefore whether the absence of a dedicated XSD is an unresolved provenance gap or an intentional property of the service.

## 2. Public PDF mapping

The official VDV publication index exposes:

```text
HTMLDisplayService V2.1
HTMLDisplayService V2.2
HTMLDisplayService V2.2a
```

The service is described as providing a URL to a web server for multifunction displays. The display browser obtains the content via HTTP/HTML.

The V2.1 document explicitly compares HTMLDisplayService with TimeService and states that HTMLDisplayService does not define its own protocol.

This is strong evidence that service execution is not modelled as a normal XML request/response service with a dedicated service XSD.

## 3. Official repository/tag check

Checked official release trees:

```text
VDV-301-2.1
VDV-301-2.2
VDV-301-2.3
```

No dedicated file such as:

```text
IBIS-IP_HTMLDisplayService_*.xsd
IBIS-IP_HtmlDisplayService_*.xsd
```

is present in those checked release pools.

A current upstream code search for `HTMLDisplayService` returns shared enumeration references rather than a dedicated service schema.

Relevant shared XSD fact:

```text
IBIS-IP_Enumerations_V2.1.xsd contains HTMLDisplayService in ServiceNameEnumeration.
IBIS-IP_Enumerations_V2.1.xsd also contains MultiFunctionalDisplay in DeviceClassEnumeration.
```

Therefore the service is known to the shared IBIS-IP type system even though it has no dedicated service XSD.

## 4. Initial classification

### HDS-001 candidate - no dedicated HTMLDisplayService XSD

Initial state:

```text
Not a schema-family/provenance gap.
Likely intentional non-XSD service modelling.
```

Classification:

```text
mismatch_kind: service_modelling
likely_source_issue: ok_with_note
classification_confidence: high
final_handling_bucket: no_action_note
```

Reasoning:

```text
1. Three public service-document versions exist.
2. Official release-tag XSD pools checked for the corresponding period contain no dedicated HTMLDisplayService schema.
3. Current upstream likewise exposes no dedicated service schema.
4. The PDF explicitly says the service does not define its own protocol and instead provides a URL from DNS-SD for browser/HTTP access.
```

No historical XSD backfill is required or permitted on the evidence currently available.

## 5. Next detailed pass

Continue in:

```text
docs/pdf_xsd_semantic_audit/10a_html_display_service_protocol_profile_and_closure.md
```

The detailed pass must preserve the version-specific DNS-SD profile instead of treating the three documents as interchangeable.
