# TimeService V1.0 protocol/discovery first pass

Status: semantic/provenance first pass completed for the non-XSD TimeService profile. Runtime SNTP/DNS-SD validation remains pending.

Source starter:

```text
docs/pdf_xsd_semantic_audit/15_time_service_historical_start.md
```

## 1. Validation authority for this service

TimeService V1.0 does not have a service-specific XML/XSD payload family in the checked official release tags.

For this service, validation authority is therefore split by layer:

```text
VDV 301-2-10 V1.0 -> VDV-specific discovery/profile requirements
RFC 4330 -> referenced SNTP protocol semantics
DNS-SD/network runtime -> executable observation target
```

This is not an exception to the XSD-authority rule; there simply is no TimeService payload XSD to apply.

## 2. Discovery profile

VDV 301-2-10 specifies the DNS-SD service type:

```text
_ibisip_udp._udp
```

and TXT metadata including:

```text
sntp-server=<IP-address>
timezone=<timezone>
```

The document gives `UTC+1` as an example timezone value.

The V2.0 technical-correction history in the writing records the service-discovery type `_ibisip_udp._udp` for TimeService V1.0. This is protocol-profile evolution/documentation context, not a schema version change.

## 3. Time synchronization semantics

The actual time/date synchronization is delegated to SNTP according to RFC 4330.

Important tool behavior:

```text
Do not expect a VDV XML GetTime/CurrentTime operation.
Do not flag absence of cyclic VDV time messages as an error.
Do not synthesize a TimeService response schema.
Use SNTP/discovery diagnostics instead.
```

## 4. Shared VDV identity

`IBIS-IP_Enumerations_V1.0.xsd` contains `TimeService` in `ServiceNameEnumeration`.

This means a system can identify/advertise the VDV service within shared service metadata even though the service's functional protocol is not XML/XSD based.

Classification remains:

```text
TS-001 = ok_with_note / non-XSD service by design
```

## 5. TS-002 - English foreword reference-number error candidate

Observed document wording:

```text
German context: VDV 301-2-10 describes TimeService.
English foreword: VDV 301-2-1 describes TimeService and its specific data structures.
```

This is internally inconsistent with the document number and with the VDV 301 structure.

Classification:

```text
mismatch_kind: document_reference_number
likely_source_issue: pdf_label_or_heading_error_candidate
classification_confidence: high
validation_behavior: none; provider/documentation note only
```

## 6. Runtime validation backlog

```text
TS-VB-001: discover TimeService advertisement and verify `_ibisip_udp._udp`.
TS-VB-002: verify `sntp-server` TXT record syntax/value and target reachability.
TS-VB-003: verify `timezone` TXT record handling according to the selected VDV profile.
TS-VB-004: send/read an SNTP exchange using the advertised server and record protocol-level result.
TS-VB-005: confirm diagnostic behavior when DNS-SD service exists but SNTP server is unreachable.
TS-VB-006: confirm diagnostic behavior when required/expected TXT metadata is absent or malformed.
TS-VB-007: confirm tool does not require or search for TimeService XML payload operations.
```

No runtime task above has been executed in this audit block.

## 7. SDK architecture implication

The resolver needs at least two validation lanes:

```text
xsd_profile              -> XML services
protocol_discovery_profile -> TimeService/other intentionally non-XSD services
```

TimeService V1.0 maps to the second lane.

The result should expose both discovery and protocol evidence so a later diagnostic can distinguish:

```text
service not advertised
service advertised but TXT metadata invalid
SNTP endpoint unreachable
SNTP endpoint reachable but synchronization exchange fails
profile appears operational
```

No such runtime status is claimed by this historical audit.
