# PDF/XSD semantic audit - current validation backlog

Status: deterministic repository validation is complete for the planned EV/RV phase, including the post-Common-V2.3 authority-split baseline. Remaining open validation requires targeted new finding regression, live/integration evidence or later provider-specific work.

## 1. Completed deterministic evidence

### XML/XSD evidence

```text
EV-001 + EV-002  run 33109011670  PASS
  historical baseline root compilation
  DMS V2.4 targeted samples
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

EV-106  run 33169314332  PASS
  Common V2.3 official vs explicit PR #30 candidate overlay
  official/candidate InternationalTextType instance-shape difference
  post-authority-split current root pool: 50/50 roots compile
  current inventory: 39 XSD service profiles, 84 direct include edges
```

### Runtime/protocol deterministic evidence

```text
RV-001  run 33112730418  PASS  HTTP/XML + Content-Type
RV-002  run 33119080288  PASS  DNS-SD/service discovery
RV-003  run 33119337775  PASS  TimeService/SNTP
RV-004  run 33119694991  PASS  Video RTSP/RTP boundary
```

The repository workflow is `workflow_dispatch` only.

## 2. New targeted Common regression backlog from Deep Read

Fresh byte-pinned Common V2.3 Deep Read opened CE-021..CE-026.

Static evidence is sufficient to keep the findings open, but later executable regression should cover the instance-impacting cases:

```text
CE-021 LogMessage:
  negative <MessageBody>
  positive <Message>

CE-022 ServiceIdentification:
  negative outer <ServiceName>
  positive outer <Service>

CE-024 UnsubscribeResponse:
  negative response without Active
  positive response with Active

CE-025 SubscribeRequest / UnsubscribeRequest:
  negative <Reply-Path>
  positive <ReplyPath>

CE-026 BeaconPoint Common V2.3:
  negative <Description>
  positive <Desciption>
  V2.4 control: <Description> according to selected V2.4 XSD
```

CE-023 is a PDF copy/paste-table finding and does not require an executable XSD defect test; the selected XSD already defines the actual NetexMode shape.

CE-019 visual closure remains pending. CE-020 is already executable-confirmed by EV-106.

## 3. Canonical remaining live backlog

The full current live/device/network backlog is:

```text
docs/pdf_xsd_semantic_audit/26_live_integration_validation_backlog.md
```

Do not recreate duplicate per-service backlog lists in this central file.

## 4. Remaining live/integration categories

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

## 5. Environment dependency

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

## 6. Deferred visual/document review

The Deep Read uses byte-pinned official PDF sources, but the current PDF screenshot backend repeatedly returns cache-miss for several VDV publications.

Current layout-sensitive examples include:

```text
CE-015 FareZone/Farezone and ZoneType casing
CE-017 TSPPoint Desciption/Description
CE-019 ServiceIdentificationWithStateList type/reference table
CE-021..CE-026 where visible-page confirmation would strengthen native-text evidence
```

These do not block exact XSD validation. Do not promote affected documents to `exhaustive_read` until visible-page review is actually completed.

## 7. Official correction candidate review

No upstream action is automatic.

If an official-facing correction is later considered:

```text
- use detailed finding register
- identify exact affected versions
- distinguish PDF correction from XSD correction
- add targeted regression evidence
- obtain explicit user approval before PR/comment/review/merge action
```

## 8. SDK implementation readiness

SDK architecture may continue to be derived from the deterministic baseline, but implementation remains frozen during the current Deep Read pass according to CURRENT_STATE.

Required guardrails:

```text
exact service/version routing
candidate authority separation
schema_variant_id for same-path variants
operation/context manifest
legacy root-map support
non-XSD protocol profiles
runtime authority + severity separation
no unexecuted live check represented as conformance evidence
```

Current audit sequencing remains:

```text
finish Deep Read -> consolidate findings/provenance -> freeze audit baseline -> implement SDK regression suite
```
