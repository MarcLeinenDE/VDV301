# Audit handoff delta - TimeService 15B

Status: TimeService V1.0 semantic/provenance first pass closed.

Base handoff:

```text
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF.md
```

Read additionally:

```text
docs/pdf_xsd_semantic_audit/15_time_service_historical_start.md
docs/pdf_xsd_semantic_audit/15a_time_service_v1_0_protocol_first_pass.md
docs/pdf_xsd_semantic_audit/15b_time_service_findings_and_closure.md
docs/pdf_xsd_semantic_audit/TIME_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/TIME_SERVICE_VALIDATION_BACKLOG_ADDENDUM.md
docs/pdf_xsd_semantic_audit/generated/time_service_historical_scope_matrix.csv
docs/pdf_xsd_semantic_audit/generated/time_service_findings_closure_matrix.csv
```

## Key result

TimeService V1.0 is intentionally non-XSD.

```text
validation profile: sntp_dns_sd_profile
VDV discovery type: _ibisip_udp._udp
TXT metadata: sntp-server, timezone
actual synchronization: SNTP according to RFC 4330
cyclic VDV XML time messages: not intended
```

Checked official release contexts and the integration branch do not contain `IBIS-IP_TimeService_V1.0.xsd`.

Official Enumerations V1.0 does contain `TimeService` in `ServiceNameEnumeration`, so shared VDV service identity is present without a dedicated payload schema.

## Findings

```text
TS-001: no dedicated TimeService XSD -> OK with note / non-XSD service by design
TS-002: English foreword incorrectly references VDV 301-2-1 for TimeService -> PDF documentation/reference-number candidate
```

## SDK implication

The future resolver must support protocol/discovery validation profiles in parallel with XML/XSD profiles. TimeService V1.0 must never be mapped to a fabricated XSD merely to make all services look uniform.

No runtime DNS-SD or SNTP validation has been performed.
No XSD was modified.
No upstream PR/comment/merge action was performed.

## Next block

```text
docs/pdf_xsd_semantic_audit/16_video_live_service_historical_start.md
```

Resolve V1.0/V2.0 official schema provenance and exact dependencies, then separate XML control/configuration semantics from media-transport semantics.
