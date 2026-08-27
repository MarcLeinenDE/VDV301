# Block 25d / RV-003 - TimeService V1.0 and SNTP profile

Status: deterministic classifier implemented and executable-tested. No live TimeService/SNTP exchange or system-clock synchronization claim is made.

## Evidence run

```text
GitHub Actions run: 33119337775
run number: 13
head tested: a22c3139cf0ae73c34aae253fdda275de9ce9981
job: 98681993414
environment: Ubuntu 24.04.4 / Python 3.12.14 / lxml 6.1.2
time_status: 0 / PASS
```

The run also re-confirmed all prior EV checks plus RV-001 and RV-002 with status 0.

## Reusable implementation

```text
tools/runtime_time_profile.py
tools/validate_time_runtime_rv003.py
```

The implementation is deliberately network-independent. It separates:

```text
VDV TimeService discovery/profile rules
RFC 4330 SNTP packet semantics referenced by VDV
modern RFC 5905 control/provenance note
system-clock diagnostic state
```

No socket is opened and the system clock is never modified by the deterministic classifier.

## VDV TimeService V1.0 discovery evidence

Executable cases confirm:

```text
TimeService + _ibisip_udp._udp + valid sntp-server IPv4 -> PASS
valid IPv6 sntp-server                                  -> PASS
wrong discovery protocol                               -> detected
missing sntp-server                                    -> detected
hostname instead of IP address in sntp-server          -> detected
wrong service name                                     -> detected
timezone raw value retained verbatim                   -> PASS
```

The selected profile source says:

```text
sntp-server=<IP-address>
```

Therefore the classifier accepts IPv4/IPv6 address literals but does not silently broaden that VDV field to a hostname.

### timezone guard

The historical audit established the `timezone` TXT metadata but did not establish a hard cardinality rule strong enough to justify inventing a mandatory failure.

Therefore RV-003 behavior is intentionally conservative:

```text
timezone present and non-empty -> preserve raw value / pass_with_note
timezone absent                -> profile_note, not hard failure
timezone present but empty     -> warning
```

No silent conversion to IANA TZ names, POSIX TZ syntax or another timezone representation occurs.

## RFC 4330 request evidence

Authority:

```text
external_normative_referenced_by_vdv
source: RFC 4330
```

Executable checks confirm:

```text
minimum SNTP/NTP base header: 48 bytes
unicast client request mode: 3
request VN range used by RFC 4330 table: 1..4
UDP destination port 123: SHOULD-level check
```

Cases:

```text
VN4/mode3 request to UDP 123 -> PASS
VN1/mode3 compatibility request -> PASS
VN5 request -> detected
mode4 used as client request -> detected
non-123 destination -> warning, not VDV/XSD hard failure
short packet -> structural error
```

The destination-port classification remains RFC-derived. It is not reported as if VDV 301 itself defined UDP port 123.

## RFC 4330 unicast reply evidence

Deterministic reply checks confirm:

```text
server reply mode 4
reply VN matches request VN
usable client stratum 1..15
non-zero reply Transmit Timestamp
reply Originate Timestamp equals request Transmit Timestamp
```

Negative cases all detect as expected:

```text
wrong Originate Timestamp
Stratum 0
zero Transmit Timestamp
wrong reply mode
reply VN different from request VN
```

This provides a deterministic foundation for a later live SNTP diagnostic without implying that any real device has been contacted.

## No XML/XSD expectation

Executable architecture guard:

```text
validation_kind() == protocol_discovery_profile
expected_xml_operations() == ()
```

This reinforces the historical TimeService conclusion:

```text
Do not synthesize TimeService.Get*
Do not synthesize TimeService.Subscribe*
Do not search for a TimeService XML response XSD
```

TimeService availability and SNTP operation belong to the protocol/discovery runtime lane.

## RFC 5905 handling

RFC 5905 obsoletes RFC 4330 and describes NTPv4, but the selected VDV TimeService V1.0 writing explicitly references RFC 4330.

SDK rule:

```text
Do not latest-wins substitute RFC 5905 for the VDV-selected RFC 4330 profile.
RFC 5905 may be exposed as a modern compatibility/control observation only.
```

This mirrors the project's schema-version policy: newer external standards do not silently rewrite the historical profile selected by the VDV writing.

## What RV-003 does NOT claim

Not executed:

```text
real DNS-SD TimeService discovery
real UDP socket to the advertised SNTP server
actual request/reply round trip
timeout/retry behavior
round-trip delay/clock-offset calculation from a live exchange
clock discipline / setting the local system clock
reachability of advertised sntp-server
system-clock accuracy
certificate/TLS consequences of clock skew
```

These remain integration/diagnostic tasks.

## Result

```text
RV-003 deterministic TimeService V1.0 / RFC 4330 SNTP classifier: PASS
```

Next planned runtime evidence:

```text
RV-004 - Video RTSP/RTP boundary
- rtspURI syntax/profile handling
- RTSP version observation without latest-wins assumption
- control-plane vs media-plane separation
- RTP/RTCP evidence model
- no claim of live stream availability until real endpoint tests are run
```
