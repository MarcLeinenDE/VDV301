# TimeService findings register addendum

Status: supplemental register; TimeService V1.0 semantic/provenance first-pass closure completed.

Authority rule:

```text
TimeService V1.0 is intentionally non-XSD.
VDV 301-2-10 defines the VDV-specific discovery/profile requirements.
The referenced SNTP standard defines protocol behavior.
No XML schema is invented for this service.
```

## TS-001 - no dedicated TimeService XSD

```text
state: OK with note
classification: non_xsd_service_by_design
confidence: high
version_scope: V1.0
validation_behavior: protocol_discovery_profile
service_type: _ibisip_udp._udp
protocol: SNTP / RFC 4330 as referenced by VDV
final_handling_bucket: resolver_profile_requirement
```

Observation:

```text
No IBIS-IP_TimeService_V1.0.xsd was found in checked official release tags or the integration branch.
The VDV writing explicitly assigns actual time synchronization to SNTP and says cyclic VDV time messages are not intended.
ServiceNameEnumeration V1.0 nevertheless contains TimeService as shared VDV service identity.
```

## TS-002 - English foreword wrong document number

```text
state: confirmed documentation candidate
classification: pdf_label_or_heading_error_candidate
confidence: high
version_scope: TimeService V1.0 PDF
validation_behavior: none
final_handling_bucket: official_pdf_documentation_clarification_candidate
```

Observation:

```text
The TimeService writing is VDV 301-2-10.
The German foreword is consistent with that context.
The English foreword says VDV 301-2-1 describes the TimeService and its specific data structures.
```
