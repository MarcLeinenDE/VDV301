# PDF/XSD semantic audit - current validation backlog

Status: deterministic repository validation is complete for the planned EV/RV phase, including the post-Common-V2.3 authority-split baseline, DMS V2.2/V2.4 EV-107/EV-108 evidence, and the strengthened TimeService RV-003 profile. Remaining open validation requires targeted new finding regression, visual closure, live/integration evidence or later provider-specific work.

## 1. Completed deterministic evidence

### XML/XSD evidence

```text
EV-001 + EV-002  run 33109011670  PASS
EV-101           run 33109367265  PASS  PCS-001
EV-102           run 33109768872  PASS  CE-018
EV-103           run 33111119723  PASS  video compositors
EV-104           run 33111644388  PASS  TrainSet context/root evidence
EV-105           run 33111831627  PASS  AnalogRadio candidate cardinality
EV-106           run 33169314332  PASS  Common V2.3 official/candidate authority split
EV-107           run 33181833930  PASS  official DMS V2.2 Deep Read declarations
EV-108           run 33182963733  PASS  candidate/integration DMS V2.4 Deep Read declarations
```

Current full-suite baseline re-run `33197358294` also re-confirmed all of the above with:

```text
50/50 root XSDs compile
39 XSD service profiles
84 direct include edges
SDK manifest/profile checks PASS
```

EV-108 authority guard remains:

```text
The public DMS V2.4 PDF is official VDV documentation.
The repository DMS V2.4 XSD checked by EV-108 is candidate/integration material.
EV-108 is not official-release XSD conformance evidence.
```

### Runtime/protocol deterministic evidence

```text
RV-001  run 33112730418  PASS  HTTP/XML + Content-Type
RV-002  run 33119080288  PASS  DNS-SD/service discovery
RV-003  run 33197358294  PASS  TimeService/SNTP, strengthened after byte-pinned Fresh Read
RV-004  run 33119694991  PASS  Video RTSP/RTP boundary
```

The repository workflow is `workflow_dispatch` only.

## 2. Targeted Common regression backlog from Deep Read

Fresh byte-pinned Common V2.3 Deep Read opened CE-021..CE-026.

Later executable strengthening may cover:

```text
CE-021 LogMessage: negative <MessageBody>, positive <Message>
CE-022 ServiceIdentification: negative outer <ServiceName>, positive outer <Service>
CE-024 UnsubscribeResponse: negative without Active, positive with Active
CE-025 Subscribe/Unsubscribe request: negative <Reply-Path>, positive <ReplyPath>
CE-026 BeaconPoint V2.3: negative <Description>, positive <Desciption>; V2.4 control <Description>
```

CE-023 is a PDF copy/paste-table finding and does not require an executable XSD defect test. CE-019 visual closure remains pending. CE-020 is already executable-confirmed by EV-106.

## 3. DMS V2.2 / V2.4 evidence status

EV-107 closes the deterministic official-V2.2 declaration side for DMS-005..DMS-007 and the executable enum spelling behind DRDMS22-003.

EV-108 closes the deterministic candidate/integration-V2.4 declaration side and confirms:

```text
DMS-005 persists against candidate/integration V2.4 XSD.
DMS-006 is aligned in checked V2.4 PDF/candidate profile.
DMS-007 persists against candidate/integration V2.4 XSD.
ErrorMessage is 0:* in V2.4 candidate.
InstallUpdate ID/Timestamp/URL/checksum/size are optional in V2.4 candidate.
```

DMS V2.2 and V2.4 visual closure remains deferred where original-PDF screenshot attempts returned cache-miss.

## 4. TimeService V1.0 evidence status

The official TimeService V1.0 PDF is byte-pinned and textually fresh-read.

Fresh findings:

```text
DRTIME10-001 English foreword wrongly points TimeService to VDV 301-2-1.
DRTIME10-002 German text excludes cyclic transmission of current time; English omits that sentence.
DRTIME10-003 minor English version-history cross-reference artifact 'cd. 1'.
```

Historical finding resolved:

```text
DR3012-006:
07/2016 base writing points TimeService to VDV 301-2-11.
VDV-Mitteilung 3002 10/2016 already maps TimeService to VDV-301-2-10.
VDV 301-2-11 05/2017 is VideoLiveService.
Result: wrong/stale historical document-number reference; no TimeService 301-2-11 resolver alias.
```

Strengthened RV-003 run `33197358294` confirms:

```text
_ibisip_udp._udp discovery profile
mandatory sntp-server profile field
IP-address-only sntp-server syntax
RFC 4330 request/reply checks
no XML/XSD operations
no cyclic transmission of current time expected
conservative timezone handling retained
```

No further deterministic TimeService regression is required for the established facts. Remaining TimeService work is live integration plus visual closure of cache-missed PDF pages.

## 5. Canonical remaining live backlog

The full current live/device/network backlog is:

```text
docs/pdf_xsd_semantic_audit/26_live_integration_validation_backlog.md
```

Do not recreate duplicate per-service live backlog lists in this central file.

## 6. Remaining live/integration categories

### Subscription runtime

```text
real Subscribe acknowledgement
callback delivery
heartbeat timing
Unsubscribe behavior
TrainSet parameterized subscription context
```

### Discovery / DNS-SD

```text
real PTR browse
raw SRV/TXT capture
actual mDNS vs unicast DNS transport
host resolution/reachability
multiple simultaneous versions using separate endpoint identity
TTL/cache behavior
```

### HTTP

```text
real GET/POST operations
HTTP version/status/headers
actual Content-Type/charset/encoding
redirect/auth/timeout behavior
feed real response XML to exact XSD resolver
HTMLDisplay real fetch path
```

### UDP / network

```text
multicast join/reception
cycle observation where the selected service profile actually defines cyclic UDP data
IGMP-related failure symptoms
routing/duplicate-IP diagnostics
train/vehicle network integration
physical/network architecture evidence
```

TimeService guard: do not put TimeService into a generic cyclic current-time-broadcast test merely because its DNS-SD type is `_ibisip_udp._udp`.

### TimeService

```text
real DNS-SD discovery
real SNTP request/reply
advertised endpoint reachability
clock offset/round-trip observation
actual local clock synchronization state
certificate/TLS clock-skew diagnostic integration
```

### Video

```text
real ListAllLiveStreams
rtspURI reachability
RTSP session/control sequence
SDP/auth
RTP/RTCP reception
loss/jitter/continuity
codec/resolution/frame-rate/bitrate comparison
```

### Mixed-version resolver

```text
end-to-end discovery -> profile -> exact schema route
parallel versions of one service
candidate-selection guard
TrainSet response-context routing
legacy V1.0 root-map end-to-end path
```

## 7. Environment dependency

Open live items require one or more of:

```text
real VDV301 device
provider test system
controlled simulator
network access
packet capture
physical/inventory documentation
```

Their open state is **not** a failed conformance result.

## 8. Deferred visual/document review

Current layout-sensitive examples include:

```text
CE-015 / CE-017 / CE-019 and remaining Common V2.3 table findings
DMS V2.2 findings where page renders cache-missed
DMS V2.4 continuity findings and DRDMS24-001 where page renders cache-missed
TIME V1.0: page 5 visually confirmed, foreword page 3 and version-history page 6 still cache-miss
```

These do not block exact schema/protocol classification. Do not promote affected documents to `exhaustive_read` until visible-page review is actually completed.

## 9. Official correction candidate review

No upstream action is automatic.

If an official-facing correction is later considered:

```text
- use the detailed finding register/report
- identify exact affected versions
- distinguish PDF correction from XSD/protocol correction
- add targeted regression evidence where materially useful
- obtain explicit user approval before PR/comment/review/merge action
```

## 10. SDK implementation readiness

SDK architecture may continue to be derived from the deterministic baseline, but implementation remains frozen during the current Deep Read pass.

Required guardrails:

```text
exact service/version routing
candidate authority separation
schema_variant_id for same-path variants
operation/context manifest
legacy root-map support
non-XSD protocol profiles
runtime authority + severity separation
TimeService no-cyclic-time-broadcast specialization
no unexecuted live check represented as conformance evidence
```

Current sequencing:

```text
finish Deep Read -> consolidate findings/provenance -> freeze audit baseline -> implement SDK regression suite
```
