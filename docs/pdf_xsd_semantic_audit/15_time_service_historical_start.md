# TimeService V1.0 historical audit start

Status: historical service model and schema-provenance first pass resolved. TimeService is intentionally non-XSD/protocol-profile based. No local protocol/discovery validation has been performed.

Working branch base:

```text
MarcLeinenDE/VDV301 dev/schema-integration
816e0431d3b558376519c4b948bfc91300de2d32
```

Scope:

```text
VDV 301-2-10 TimeService V1.0, 02/2018
VDVde/VDV301 official release tags VDV-301-1.0, VDV-301-2.0, VDV-301-2.3
IBIS-IP_Enumerations_V1.0.xsd
SNTP according to RFC 4330 as referenced by the VDV writing
DNS-SD service-discovery profile defined by the VDV writing
```

## 1. Service model

The public VDV TimeService writing explicitly gives TimeService a special status because time synchronization is based on the standardized SNTP protocol rather than on VDV-specific XML request/response payloads.

The document specifies:

```text
protocol: SNTP according to RFC 4330
DNS-SD service type: _ibisip_udp._udp
TXT record for time-server address: sntp-server=<IP-address>
TXT record for timezone information: timezone=<timezone>, example UTC+1
```

The actual clock synchronization is performed by SNTP. The writing explicitly states that cyclic transmission of the current time as VDV messages is not intended.

## 2. Dedicated XSD search

No dedicated file named:

```text
IBIS-IP_TimeService_V1.0.xsd
```

was found in the checked official release contexts:

```text
VDV-301-1.0
VDV-301-2.0
VDV-301-2.3
```

and no such file is present in `dev/schema-integration`.

Repository code search for `TimeService` resolves to shared enumeration usage rather than a dedicated service schema.

The official V1.0 `ServiceNameEnumeration` does contain:

```text
TimeService
```

Thus service discovery/identity exists in the shared VDV model without a TimeService XML schema.

## 3. Classification

### TS-001 - no dedicated TimeService XSD

```text
state: OK with note
mismatch_kind: non_xsd_service_by_design
likely_source_issue: none
classification_confidence: high
validation_behavior: protocol/discovery profile, not XML/XSD validation
```

The absence of a TimeService XSD is not classified as a historical schema-family gap.

No TimeService XSD is to be invented or reconstructed.

## 4. Documentation candidate

### TS-002 - wrong document number in English foreword

The German foreword correctly identifies this writing as VDV 301-2-10 TimeService.

The English foreword states that `VDV 301-2-1` describes the TimeService and its specific data structures.

Because the actual document is VDV 301-2-10 and section 301-2-1 is the Common Data Structures / Enumerations writing, this is treated as a documentation/reference-number candidate.

Initial classification:

```text
mismatch_kind: document_reference_number
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: high
```

## 5. SDK resolver implication

A future validator must support a non-XSD service profile such as:

```text
service: TimeService
version: 1.0
validation_profile: sntp_dns_sd_profile
```

The profile should remain separate from XML/XSD validation and should check protocol/discovery facts appropriate to the selected TimeService version.

Do not route TimeService V1.0 to Common/Enums as though those shared schemas were a TimeService payload schema. Shared enumerations only provide cross-service identity metadata.

## 6. External protocol background

RFC 4330 defines SNTP over UDP. For implementation diagnostics, the RFC's standard NTP/SNTP destination port information may be used as external protocol evidence, clearly separated from VDV-specific service-discovery requirements.

The fact that RFC 4330 has since been obsoleted by newer NTP specifications does not retroactively change what the VDV 301-2-10 V1.0 writing selected and is not classified as a VDV PDF/XSD defect.

## 7. Next file

```text
docs/pdf_xsd_semantic_audit/15a_time_service_v1_0_protocol_first_pass.md
```
