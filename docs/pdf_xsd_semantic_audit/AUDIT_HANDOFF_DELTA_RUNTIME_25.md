# Audit handoff delta - deterministic runtime phase / block 25

Status: block 25 deterministic runtime/protocol evidence completed.

## Phase result

```text
RV-001 HTTP/XML + Content-Type       PASS
RV-002 DNS-SD/service discovery      PASS
RV-003 TimeService/SNTP              PASS
RV-004 Video RTSP/RTP boundary       PASS
```

No live-device/network conformance is claimed by these deterministic classifiers.

## Evidence runs

```text
RV-001  run 33112730418  HTTP/XML + Content-Type
RV-002  run 33119080288  DNS-SD + VDV discovery/HDS
RV-003  run 33119337775  TimeService V1.0 + RFC 4330 SNTP
RV-004  run 33119694991  Video rtspURI + RTSP/RTP boundary
```

All four evidence runs completed with their target status `0`. RV-004 also re-ran the previously integrated EV/RV checks and reported all statuses 0.

## Runtime authority model

Every runtime finding must retain both severity and authority.

Authority classes in the current machine-readable matrix include:

```text
vdv_normative
external_normative
external_normative_referenced_by_vdv
vdv_profile_exception_or_specialization
combined_semantics
diagnostic_heuristic
```

Source:

```text
docs/pdf_xsd_semantic_audit/generated/runtime_protocol_authority_matrix.csv
```

Do not transform external-protocol rules into fictitious VDV requirements.

## RV-001 key rules

```text
VDV General Conventions:
  no request data -> GET
  request data -> POST
  HTTP/1.1 explicit from V2.3 onward; do not retroactively enforce on V2.2

External HTTP/XML:
  malformed Content-Type -> external protocol error
  missing Content-Type with known body/media -> RFC warning, not VDV hard failure
  application/xml -> compatible
  text/xml -> compatible alias with note
  +xml -> XML-capable with note
  declared non-XML media type for an XSD-backed XML payload -> combined media/payload error

HTMLDisplay:
  do not force HTML payloads through XSD/XML media expectations
```

## RV-002 key rules

```text
DNS-SD record semantics are separate from DNS-SD transport.
mDNS is not an unconditional synonym/requirement for DNS-SD; unicast DNS may also carry DNS-SD.

General Conventions V2.2+:
  ver
  deviceclass
  deviceID
  multicast for UDP
  protocol label matching HTTP/UDP family

Do not apply V2.2+ mandatory TXT rules retroactively to older selected profiles.

HTMLDisplay:
  V2.1 -> _http._tcp + content/path, endpoint from SRV host/port + path
  V2.2 -> _http._tcp + content/url, endpoint from TXT url
  V2.2a -> _ibisip_http._tcp preferred; _http._tcp accepted/deprecated; endpoint from TXT url
```

## RV-003 key rules

```text
TimeService V1.0 is protocol_discovery_profile, not XML/XSD service.
No TimeService.Get*/Subscribe* XML operations are synthesized.

VDV discovery:
  _ibisip_udp._udp
  sntp-server=<IP-address>
  timezone retained raw; current evidence does not justify inventing a hard missing-timezone cardinality rule

RFC 4330 selected by VDV:
  >=48-byte header
  client mode 3
  request VN 1..4
  UDP destination port 123 SHOULD-level check
  server reply mode 4
  reply VN follows request
  usable stratum 1..15
  non-zero transmit timestamp
  originate timestamp echoes request transmit timestamp

RFC 5905 is modern control context only; do not latest-wins replace the VDV-selected RFC 4330 profile.
```

## RV-004 key rules

```text
VideoLive metadata -> rtspURI boundary
RTSP control and RTP/RTCP media remain separate from HTTP/XML validity.
Valid XML metadata does not prove media availability.
No synthetic VDV XML START/STOP operations.

VDV evidence does not currently pin RTSP/1.0 or RTSP/2.0 as a VDV-specific requirement.
Record observed version.
Do not latest-wins RTSP/2.0.

External RTSP control:
  RTSP/1.0 request must not receive RTSP/2.0 response under tracked version-negotiation rule
  RTSP 2.0 is not treated as backwards-compatible drop-in replacement

External RTP:
  RFC 3550 version 2
  fixed header >=12 bytes
  CSRC count must match available header length
```

## Remaining live work

Canonical remaining live/device/network backlog:

```text
docs/pdf_xsd_semantic_audit/26_live_integration_validation_backlog.md
```

It covers:

```text
subscription callbacks/heartbeat
live DNS-SD/mDNS/PTR
real HTTP endpoints/headers
UDP multicast + IGMP/network diagnostics
real SNTP exchange/clock diagnostics
real RTSP/RTP media path
mixed-version end-to-end resolver
physical/network inventory evidence
```

These tasks require a real implementation, simulator, network access, packet capture and/or physical documentation. Their open state is not a failed conformance result.

## Workflow state

```text
.github/workflows/schema-audit-validation.yml
trigger: workflow_dispatch only
```

Normal audit commits must not generate automatic Actions runs / failed-run mail.

## Next project phase

```text
1. consolidate central AUDIT_HANDOFF.md / findings.md / validation_backlog.md / 00_index.md
2. freeze semantic/audit baseline
3. derive SDK manifest and resolver implementation baseline
```
