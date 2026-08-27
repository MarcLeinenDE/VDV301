# TimeService V1.0 findings and first-pass closure

Status: semantic/provenance first-pass closure completed for the intentionally non-XSD TimeService. Runtime SNTP/DNS-SD validation remains pending.

Source blocks:

```text
docs/pdf_xsd_semantic_audit/15_time_service_historical_start.md
docs/pdf_xsd_semantic_audit/15a_time_service_v1_0_protocol_first_pass.md
```

## Routing closure

```text
Public service: TimeService V1.0
VDV writing: VDV 301-2-10, 02/2018
Service payload XSD: none by design in checked official release contexts
Shared service identity: ServiceNameEnumeration contains TimeService
Validation lane: protocol_discovery_profile
VDV-specific discovery type: _ibisip_udp._udp
Protocol: SNTP according to RFC 4330
TXT metadata: sntp-server and timezone
```

## Findings

### TS-001 - no dedicated TimeService XSD

```text
state: OK with note
classification: non_xsd_service_by_design
confidence: high
validation_behavior: SNTP/DNS-SD profile; no XML/XSD payload validation
```

No historical XSD backfill is required and no TimeService XSD should be created.

### TS-002 - English foreword points to VDV 301-2-1

```text
state: confirmed documentation/reference-number candidate
classification: pdf_label_or_heading_error_candidate
confidence: high
validation_behavior: none
```

The writing itself is VDV 301-2-10 and the German foreword identifies the TimeService in that context; the English foreword's `VDV 301-2-1` reference is treated as a documentation error candidate.

## SDK implications

```text
- Support a protocol_discovery_profile alongside xsd_profile.
- Route TimeService V1.0 to SNTP/DNS-SD checks, not to a fabricated XSD.
- Check `_ibisip_udp._udp` and the VDV-defined TXT metadata.
- Keep external RFC protocol evidence separate from VDV-specific discovery evidence.
- Do not expect cyclic VDV XML time messages.
- Distinguish discovery failure, metadata failure, endpoint reachability and SNTP exchange failure in diagnostics.
```

## Validation status

```text
Semantic/provenance first pass: closed.
Dedicated XSD search in checked release tags: completed; none found.
Runtime DNS-SD validation: not performed.
Runtime SNTP validation: not performed.
No XSD modification: yes.
No upstream PR/comment/merge action: yes.
```

## Next planned historical service block

```text
docs/pdf_xsd_semantic_audit/16_video_live_service_historical_start.md
```

Initial focus:

```text
VideoLiveService V1.0 and V2.0.
Resolve V1.0 official schema provenance/backfill if present in release tags.
Compare V1.0/V2.0 service and dependency families without latest-wins mapping.
Preserve any non-XML streaming/media protocol semantics separately from XML control/configuration structures.
```
