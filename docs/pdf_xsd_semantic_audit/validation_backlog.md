# PDF/XSD semantic audit - current validation backlog

Status: deterministic repository validation is complete for the planned EV/RV phase. Remaining open validation requires live/integration evidence or later provider-specific regression work.

## 1. Completed deterministic evidence

### XML/XSD evidence

```text
EV-001 + EV-002  run 33109011670  PASS
  46 root XSDs compile
  DMS V2.4 targeted samples 6/6
  legacy V1.0 root adapters

EV-101  run 33109367265  PASS
  PCS-001 OperationNotSupported dependency/value-set mismatch

EV-102  run 33109768872  PASS
  CE-018 ServiceIdentificationWithStateList XSD 0:* behavior

EV-103  run 33111119723  PASS
  VLS/VRS/VDS compositor findings

EV-104  run 33111644388  PASS
  TrainSet TSM-002 + TSD-003 context resolution

EV-105  run 33111831627  PASS
  AnalogRadio ARA-003 candidate cardinality
```

### Runtime/protocol deterministic evidence

```text
RV-001  run 33112730418  PASS  HTTP/XML + Content-Type
RV-002  run 33119080288  PASS  DNS-SD/service discovery
RV-003  run 33119337775  PASS  TimeService/SNTP
RV-004  run 33119694991  PASS  Video RTSP/RTP boundary
```

The repository workflow is `workflow_dispatch` only.

## 2. Canonical remaining live backlog

The full current live/device/network backlog is:

```text
docs/pdf_xsd_semantic_audit/26_live_integration_validation_backlog.md
```

Do not recreate duplicate per-service backlog lists in this central file.

## 3. Remaining live/integration categories

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
cycle observation
IGMP-related failure symptoms
routing/duplicate-IP diagnostics
train/vehicle network integration
physical/network architecture evidence
```

### TimeService

```text
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

## 4. Environment dependency

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

## 5. Deferred visual/document review

Some documentation-only spelling/casing candidates may still benefit from manual visual PDF confirmation, especially where PDF text extraction could affect typography/case.

Examples retained in detailed CE registers include:

```text
FareZone/Farezone casing candidates
TSPPoint Desciption/Description candidate
```

These do not block SDK design because executable validation follows the selected XSD.

## 6. Official correction candidate review

No upstream action is automatic.

If an official-facing correction is later considered:

```text
- use detailed finding register
- identify exact affected versions
- distinguish PDF correction from XSD correction
- add targeted regression evidence
- obtain explicit user approval before PR/comment/review/merge action
```

## 7. SDK implementation readiness

The SDK may now be implemented against the completed deterministic baseline.

Required guardrails during implementation:

```text
exact service/version routing
candidate authority separation
operation/context manifest
legacy root-map support
non-XSD protocol profiles
runtime authority + severity separation
no unexecuted live check represented as conformance evidence
```

Next project phase after central audit-document consolidation:

```text
freeze audit baseline -> derive SDK manifest/resolver model -> implement SDK regression suite
```
