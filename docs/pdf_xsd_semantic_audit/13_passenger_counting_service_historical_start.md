# PassengerCountingService V1.0 / V2.1 historical audit start

Status: provenance, historical schema-family routing and version delta resolved. Official V1.0 service XSD backfilled byte-identically from the VDVde/VDV301 VDV-301-1.0 release tag. Local XSD compilation/sample validation remains pending.

Working branch base after backfill:

```text
MarcLeinenDE/VDV301 dev/schema-integration
389da2395e846d6ce7dcdb3541b7df66333c2b4a
```

Scope:

```text
VDV 301-2-8 PassengerCountingService V1.0, 03/2017
VDV 301-2-8 PassengerCountingService V2.1
VDVde/VDV301 official release tag VDV-301-1.0
VDVde/VDV301 official release tag VDV-301-2.1
IBIS-IP_PassengerCountingService_V1.0.xsd
IBIS-IP_PassengerCountingService_V2.1.xsd
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
IBIS_IP_V1.0.xsd official V1.0 aggregate schema
```

## 1. Authority and routing policy

```text
Validation follows the selected official XSD family.
Historical release-tag material may be backfilled unchanged.
Service-version numbers do not imply same-number Common/Enumerations dependencies.
No latest-wins substitution is allowed.
A historical aggregate schema may be part of the official validation family even when the service-specific file only contains type definitions.
```

## 2. V1.0 official provenance and backfill

Official source:

```text
Repository: VDVde/VDV301
Tag: VDV-301-1.0
Tag object: ef38d3babebfbb72e6bcdc42c7026e13bab77f69
Release commit: f5b53785f703e898632603eec3bfa3555a79fdba
Release tree: 729bbe3270e52fed3e0641466048a745d5a09b32
```

Service file:

```text
IBIS-IP_PassengerCountingService_V1.0.xsd
blob: 600a3ee6290c630a4435fb06ca9803dabaceb788
```

The exact blob is now present in `dev/schema-integration` with the same SHA. No content was changed during import.

Classification:

```text
historical official release material
not candidate material
not a schema correction
```

## 3. V1.0 two-layer schema family

The V1.0 service-specific PCS XSD explicitly includes:

```text
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

It defines the PCS-specific data structures but does not itself declare the complete global PCS operation-root set.

The same official VDV-301-1.0 release contains:

```text
IBIS_IP_V1.0.xsd
blob: 41289eaed2674a169fdf77a10a2eff293c76d5c4
```

That official aggregate schema includes the PCS V1.0 service XSD and declares:

```text
PassengerCountingService.GetAllDataResponse
PassengerCountingService.RetrieveSpecificDoorDataRequest
PassengerCountingService.RetrieveSpecificDoorDataResponse
PassengerCountingService.SetCounterDataRequest
PassengerCountingServiceGroup
```

Therefore the historical V1.0 model is intentionally two-layered:

```text
service XSD -> PCS type definitions
release aggregate -> global operation roots / operation group
```

This is a resolver requirement, not a PCS defect.

The aggregate is not backfilled in this service block because it includes the wider V1.0 release family and belongs to the later Base / General Conventions historical-family block.

## 4. V2.1 official provenance

Official source:

```text
Repository: VDVde/VDV301
Tag: VDV-301-2.1
Release commit: 585e0bea34b64887db4276f1c94d5f3e78f06c66
Release tree: a8472530e840f7b365f6ba1075bfc09758ebda21
```

Service file:

```text
IBIS-IP_PassengerCountingService_V2.1.xsd
blob: 59ef2ddb09b92db0d492974e38bad5b6be03865e
```

The file already present in `dev/schema-integration` has the same blob SHA.

## 5. Exact V2.1 dependency family

Despite the service version being V2.1, the official PCS V2.1 XSD explicitly includes:

```text
IBIS-IP_common_V1.0.xsd
IBIS-IP_Enumerations_V1.0.xsd
```

The VDV-301-2.1 release also contains Common/Enumerations V2.1, but PCS V2.1 does not select them.

Selected strict PCS V2.1 validation family:

```text
PassengerCountingService V2.1
-> Common V1.0
-> Enumerations V1.0
```

Do not substitute Common/Enumerations V2.1 merely because they are present in the same release.

## 6. V1.0 -> V2.1 service delta

The existing core operation family remains conceptually stable:

```text
GetAllData
SubscribeAllData
UnsubscribeAllData
RetrieveSpecificDoorData
SetCounterData
```

V2.1 adds optional control/state operations:

```text
StartCounting
StopCounting
GetCountingState
SubscribeCountingState
UnsubscribeCountingState
```

The V2.1 service XSD contains the corresponding request/response/group modelling for these additions.

## 7. Candidate findings for detailed pass

### PCS-001 candidate - OperationNotSupported vs selected Enumerations V1.0

The V2.1 document explicitly states for the newly added optional operations that `ErrorCodeEnumeration` was extended by:

```text
OperationNotSupported
```

However:

```text
PCS V2.1 selects Enumerations V1.0.
Enumerations V1.0 does not contain OperationNotSupported.
Enumerations V2.1 does contain OperationNotSupported.
Common V1.0 structures used by the PCS responses reference ErrorCodeEnumeration.
```

Initial classification:

```text
mismatch_kind: schema_family_or_dependency_value_set
likely_source_issue: xsd_dependency_alignment_or_release_packaging_error_candidate
classification_confidence: high
```

No dependency is changed during the audit.

### PCS-002 candidate - V1.0 operation roots are aggregate-owned

Observation:

```text
PCS V1.0 service XSD defines service-specific structures.
Official IBIS_IP_V1.0.xsd defines the PCS global operation roots and PassengerCountingServiceGroup.
```

Initial classification:

```text
state: OK with note
mismatch_kind: historical_aggregate_routing
likely_source_issue: none
classification_confidence: high
```

This is an SDK resolver requirement, not an upstream correction candidate.

## 8. Next file

```text
docs/pdf_xsd_semantic_audit/13a_passenger_counting_service_v1_0_v2_1_pdf_xsd_first_pass.md
```
