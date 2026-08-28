# Cross-service subscription findings register addendum

## SUB-001 - `TerminateSubscribe*` documentation types vs Common `Unsubscribe*`

State: confirmed documentation/XSD naming discrepancy.

Classification: `pdf_table_or_documentation_error_candidate`.

Evidence history:

```text
VDV 301-2 V1.0 table 4 (fresh Deep Read Pass 2):
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
It is already present in the public VDV 301-2 V1.0 base publication.
Affected-document history is therefore extended back to V1.0.
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
```

Handling:

```text
Do not derive supported operations solely from service-group membership.
Do not rewrite schemas to force one style.
Use a separate operation manifest in the SDK.
```

## Cross-reference resolutions

```text
CIS-002 -> resolved as ok_with_note / generic subscription modelling.
SMS-001 -> resolved as ok_with_note / generic subscription modelling.
TSD-001 -> remains historical service-modelling finding.
TSD-002 -> remains PDF documentation candidate.
TSD-003 -> later executable evidence supports contextual acknowledgement-vs-data-event resolver semantics; see EV-104 documentation.
```
