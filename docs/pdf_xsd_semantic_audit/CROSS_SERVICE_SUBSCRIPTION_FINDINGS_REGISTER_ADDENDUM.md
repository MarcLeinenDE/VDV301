# Cross-service subscription findings register addendum

## SUB-001 - `TerminateSubscribe*` documentation types vs Common `Unsubscribe*`

State: confirmed documentation/XSD naming discrepancy.

Classification: `pdf_table_or_documentation_error_candidate`.

Evidence history:

```text
VDV 301-2 V1.0 table 4 (fresh Deep Read Pass 2):
  UnsubscribeData -> TerminateSubscribeRequestStructure / TerminateSubscribeResponseStructure

VDV 301-2 Base Services V2.0 notation table (fresh Deep Read Pass 2):
  UnsubscribeData -> TerminateSubscribeRequestStructure / TerminateSubscribeResponseStructure

General Conventions V2.3/V2.4 table 4:
  UnsubscribeData -> TerminateSubscribeRequestStructure / TerminateSubscribeResponseStructure

Checked Common V1.0/V2.0/V2.2/V2.4:
  UnsubscribeRequestStructure / UnsubscribeResponseStructure
  no TerminateSubscribe* structures found
```

Deep Read consequence:

```text
The discrepancy is not merely a late V2.3/V2.4 documentation regression.
It is present in the public VDV 301-2 V1.0 base publication and persists in Base Services V2.0.
Affected-document history therefore extends across the early base-service publications.
```

Handling:

```text
Validation follows selected Common XSD.
Do not create executable TerminateSubscribe aliases.
Retain SUB-001 as explanatory audit knowledge for historical profiles.
```

## SUB-002 - inconsistent service-XSD encoding of generic subscription operations

State: cross-service modelling observation; technical intent not fully proven in the original first-pass document, with later EV/context work recorded elsewhere.

Classification: `service_modelling_or_generic_response_candidate`.

Evidence:

```text
DMS V2.2 operation group explicitly lists service-prefixed Subscribe/Unsubscribe elements typed with generic Common structures.

CIS V2.x and SMS V2.2 document subscription operations but their local operation groups omit equivalent service-prefixed subscription entries.

Fresh VDV 301-2 Base Services V2.0 Deep Read adds:
  - SystemDocumentationService V2.0 PDF documents Subscribe/UnsubscribeSystemConfiguration,
    while the exact service group contains only service-specific payload roots and omits equivalent generic subscription entries.
  - SystemManagementService is still exact V1.0 in official tag VDV-301-2.0; the PDF documents subscription operations,
    while the exact V1.0 group contains only GetDeviceStatusResponse and GetServiceStatusResponse.
```

Handling:

```text
Do not derive supported operations solely from service-group membership.
Do not rewrite schemas to force one style.
Use a separate operation manifest in the SDK.
Route every operation against its exact service/document version and dependency pool.
```

## Cross-reference resolutions

```text
CIS-002 -> resolved as ok_with_note / generic subscription modelling.
SMS-001 -> resolved as ok_with_note / generic subscription modelling.
TSD-001 -> remains historical service-modelling finding.
TSD-002 -> remains PDF documentation candidate.
TSD-003 -> later executable evidence supports contextual acknowledgement-vs-data-event resolver semantics; see EV-104 documentation.
```
