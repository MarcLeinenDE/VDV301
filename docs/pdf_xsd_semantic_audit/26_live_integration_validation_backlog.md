# Block 26 - Live / integration validation backlog

Status: canonical remaining technical-validation backlog after completion of semantic audit, EV-001/002/101-105 and deterministic RV-001-RV-004.

Purpose:

```text
Keep only checks that require a real implementation, network, packet capture, endpoint or physical/inventory evidence.
Do not repeat deterministic checks already proven by EV/RV harnesses.
Do not report an unexecuted live check as failed or passed.
```

## 1. Subscription callback / heartbeat integration

Foundation already completed:

```text
cross-service subscription modelling closure
CIS-002 and SMS-001 resolved as generic subscription modelling
TSD-003 resolved as acknowledgement-vs-data-event context rule
Common SubscribeResponseStructure heartbeat semantics recorded
```

Live tasks:

```text
LI-SUB-001 Execute a real Subscribe operation against a conforming/test service.
LI-SUB-002 Capture the immediate SubscribeResponse acknowledgement separately from later callback data.
LI-SUB-003 Verify callback target IP/port/path actually receives the event payload.
LI-SUB-004 Validate callback XML against the exact service/version/context schema route.
LI-SUB-005 If Heartbeat > 0 is returned, observe callback/data timing and distinguish missed-heartbeat diagnostic from XML validity.
LI-SUB-006 Execute Unsubscribe and verify callbacks cease according to the selected service semantics.
LI-SUB-007 Exercise a parameterized TrainSetData V2.2 Retrieve subscription and verify CoachNumber context.
```

## 2. DNS-SD / discovery live evidence

Foundation already completed:

```text
RV-002 deterministic RFC 6763 + VDV discovery classifier PASS
HDS V2.1/V2.2/V2.2a profiles deterministic PASS
DNS-SD transport is not hard-wired to mDNS
```

Live tasks:

```text
LI-DISC-001 Perform real service browse / PTR discovery and record instance names.
LI-DISC-002 Capture matching SRV and TXT records with raw values.
LI-DISC-003 Verify actual DNS-SD transport in deployment: mDNS or unicast DNS.
LI-DISC-004 Resolve discovered target host/address and test endpoint reachability separately from advertisement validity.
LI-DISC-005 Observe TTL/cache expiry and service disappearance/reappearance behavior where relevant.
LI-DISC-006 Advertise or observe two versions of the same service on one device and verify different port and/or path as required by the selected General-Conventions profile.
LI-DISC-007 Verify HDS V2.2/V2.2a real content endpoint follows TXT `url` rather than generic SRV host/port reconstruction.
```

## 3. HTTP live integration

Foundation already completed:

```text
RV-001 deterministic GET/POST and HTTP-version profile checks PASS
Content-Type classifier distinguishes VDV authority from RFC 9110/RFC 7303 authority
```

Live tasks:

```text
LI-HTTP-001 Invoke representative payloadless operation and capture actual HTTP method/version/status/headers/body.
LI-HTTP-002 Invoke representative request-data operation and capture same evidence.
LI-HTTP-003 Record Content-Type exactly as supplied by implementation; classify with RV-001 rules.
LI-HTTP-004 Compare declared charset/media encoding with actual XML byte stream where applicable.
LI-HTTP-005 Record redirects, authentication challenges, connection close/reuse and timeout behavior without inventing VDV rules where none exist.
LI-HTTP-006 Feed returned XML to the exact service/version XSD resolver and keep transport result separate from schema result.
LI-HTTP-007 Test HTMLDisplay HTTP fetch separately from XSD-backed XML services.
```

## 4. UDP multicast / network runtime

Foundation already completed:

```text
VDV discovery multicast metadata rules classified
VDV 301-3 network requirements/recommendations separated from XSD authority
```

Live tasks:

```text
LI-UDP-001 Join an advertised multicast group and confirm reception of the selected UDP service.
LI-UDP-002 Record packet source/destination, port, cadence and payload separately from schema validation.
LI-UDP-003 Validate received XML/telegram payload with the exact selected service schema/profile where applicable.
LI-UDP-004 Observe packet cadence and flag sub-1-second cycle only with the documented recommendation authority.
LI-UDP-005 Diagnose multicast failure symptoms including IGMP/switch behavior where architecture makes IGMP relevant.
LI-NET-001 Detect duplicate IP addresses / inconsistent addressing as network diagnostic.
LI-NET-002 Verify routing between train/vehicle-network contexts where present.
LI-NET-003 Inventory physical architecture evidence: safety coupling/no-feedback gateway, cabling lengths, network separation, switches/VLAN/router design.
```

## 5. TimeService / SNTP live integration

Foundation already completed:

```text
RV-003 deterministic TimeService discovery + RFC 4330 request/reply classifier PASS
TimeService correctly routes to protocol_discovery_profile and has no synthetic XML operations
```

Live tasks:

```text
LI-TIME-001 Discover a real TimeService and capture raw TXT `sntp-server` and `timezone` values.
LI-TIME-002 Send an SNTP request to the advertised address and record destination port, request/reply bytes and timing.
LI-TIME-003 Classify the reply with RV-003 packet rules.
LI-TIME-004 Calculate observed offset/round-trip metrics only from real exchange timestamps.
LI-TIME-005 Distinguish advertisement success, endpoint reachability, protocol validity and actual clock synchronization.
LI-TIME-006 Report local system-time skew as a separate diagnostic because it can affect certificate/TLS validity in other systems.
```

## 6. Video RTSP/RTP live integration

Foundation already completed:

```text
EV-103 validates current Video XML compositor behavior
RV-004 deterministic rtspURI, RTSP version-negotiation and RTP-header boundary PASS
```

Live tasks:

```text
LI-VIDEO-001 Invoke real VideoLiveService.ListAllLiveStreams and capture HTTP/XML/XSD evidence.
LI-VIDEO-002 Extract each returned rtspURI and test DNS/host reachability separately.
LI-VIDEO-003 Establish RTSP connection and record observed protocol version; do not latest-wins RTSP/2.0.
LI-VIDEO-004 Exercise applicable OPTIONS/DESCRIBE/SETUP/PLAY/PAUSE/TEARDOWN behavior and retain exact response/status evidence.
LI-VIDEO-005 Parse/validate SDP where supplied by the endpoint.
LI-VIDEO-006 Record authentication requirements/challenges without treating them as VDV-defined unless sourced.
LI-VIDEO-007 Receive RTP and, where available, RTCP; record SSRC, sequence, timestamps, payload type and transport mode.
LI-VIDEO-008 Measure packet loss/reordering/jitter/continuity as media diagnostics.
LI-VIDEO-009 Compare codec/resolution/frame-rate/bitrate observations with VideoLive metadata when technically available.
LI-VIDEO-010 Keep `XML metadata valid`, `RTSP control works` and `media is usable` as independent result states.
```

## 7. Mixed-version resolver end-to-end

Foundation already completed:

```text
General Conventions explicitly allow independently versioned services and parallel service versions.
Exact dependency routing is established across the audit.
No latest-XSD-wins rule is allowed.
```

Live/integration tasks:

```text
LI-RES-001 Feed a discovery snapshot with different service versions into the resolver and verify each maps to its exact profile/pool.
LI-RES-002 Include two versions of one service simultaneously and verify endpoint/version separation.
LI-RES-003 Include official + candidate-capable profiles and confirm candidate material is never selected without explicit authority configuration.
LI-RES-004 Verify a service whose response requires operation-context routing (TrainSetData Subscribe acknowledgement vs callback data).
LI-RES-005 Verify legacy V1.0 type-only service roots via the provenance-backed root map in an end-to-end payload path.
```

## 8. Provider/device availability requirement

The following classes cannot be completed purely from the repository:

```text
real DNS-SD/mDNS/PTR behavior
real endpoint reachability
real HTTP headers/statuses
real subscription callbacks/heartbeat timing
real multicast/IGMP behavior
real SNTP exchange/system clock state
real RTSP/RTP media behavior
physical/network topology evidence
```

They require one or more of:

```text
real device
provider test system
controlled simulator
packet capture
network access
physical/inventory documentation
```

Their open state is therefore not an audit defect.

## 9. Exit criteria before SDK/tool production baseline

The SDK can be designed and implemented before every live task above is executed, provided:

```text
- deterministic EV/RV rules remain regression-tested;
- live checks are exposed as optional runtime capabilities;
- each result retains source authority and confidence;
- no unexecuted live test is presented as conformance evidence;
- exact service/version/candidate routing is preserved.
```

A production field-validation tool should later use this backlog as its integration-test plan.

## 10. Next project step

```text
Consolidate central audit control documents.
Then freeze the semantic/audit baseline and derive the SDK manifest / resolver model.
```
