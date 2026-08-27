# DeviceManagementService findings register addendum

Status: V2.0-V2.4 semantic/provenance first-pass chain complete.

## DMS-001

```text
classification: service_modelling_or_generic_response_candidate
scope: V2.0
observation: public operation inventory includes generic Subscribe/Unsubscribe and device Activate/Deactivate/Restart operations not represented completely by V2.0 service-XSD group/global elements
validation: exact V2.0 XSD only; technical generic-operation modelling review pending
```

## DMS-002

```text
classification: pdf_table_or_documentation_error_candidate
scope: V2.0 document
observation: literal unresolved cross-reference strings occur repeatedly in DMS descriptions
validation impact: none
```

## DMS-003

```text
classification: ok_with_note
scope: historical V2.0/V2.1/V2.2 -> V2.4 correction
observation: 10:* ErrorMessage was PDF/XSD-aligned in early versions; V2.4 later corrects to 0:*
validation: do not retroactively relax older profiles
```

## DMS-004

```text
classification: ok_with_note
scope: V2.1 -> V2.4 correction
observation: InstallUpdate UpdateID/UpdateTimestamp/UpdateURL are required in V2.1 PDF/XSD; V2.4 later makes them optional
validation: do not retroactively relax V2.1
```
