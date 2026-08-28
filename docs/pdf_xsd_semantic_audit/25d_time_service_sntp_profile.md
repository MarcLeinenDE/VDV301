# Block 25d / RV-003 - TimeService V1.0 and SNTP profile

Status: deterministic classifier implemented and executable-tested; strengthened after byte-pinned TimeService V1.0 Deep Read. No live TimeService/SNTP exchange or system-clock synchronization claim is made.

## Current evidence run

Latest strengthened run:

```text
GitHub Actions run: 33197358294
head tested: 215fd3cbb00619b0cf0232856c7163a52402318b
result: PASS
```

The run re-confirmed the complete deterministic repository suite:

```text
50 root XSDs compile
EV-101 through EV-108 pass
RV-001 through RV-004 pass
SDK manifest/profile checks pass
39 XSD service profiles
84 direct include edges
```

Historical RV-003 implementation run `33119337775` remains provenance evidence for the initial deterministic classifier.

## Fresh-read source

Official TimeService source is now byte-pinned:

```text
VDV-Schrift 301-2-10 TimeService V1.0, 02/2018
SHA-256: d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3
size: 515920 bytes
pin run: 33196758957
report: deep_read/TIME_V1.0.md
```

The Fresh Read was completed independently before using this RV document as a comparison template.

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

Fresh-read and executable cases confirm:

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

The earlier VDV 301-2 V1.0 generic TXT table additionally labels `sntp-server` mandatory for the time-synchronization service.

Therefore the classifier accepts IPv4/IPv6 address literals but does not silently broaden that field to a hostname.

## TimeService is not a cyclic time-broadcast service

The German TimeService V1.0 service text explicitly states that cyclic transmission of the current time is not intended beyond SNTP synchronization.

The adjacent English section omits that sentence; this is tracked as `DRTIME10-002`.

The runtime profile now carries an explicit architecture guard:

```text
cyclic_time_broadcast_expected() == False
```

Strengthened run `33197358294` confirms:

```text
OK TimeService does not expect cyclic transmission of current time
```

SDK consequence:

```text
Do not interpret the DNS-SD type _ibisip_udp._udp as a generic cyclic UDP multicast-time stream.
Time synchronization remains the SNTP path.
```

## timezone guard

The separated TimeService writing describes the `timezone` TXT metadata, including an example such as `timezone=UTC+1`, but the Fresh Read did not establish a formal hard optional/mandatory cardinality comparable to the older explicit mandatory wording for `sntp-server`.

Therefore RV-003 behavior remains deliberately conservative:

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

Negative cases detect as expected:

```text
wrong Originate Timestamp
Stratum 0
zero Transmit Timestamp
wrong reply mode
reply VN different from request VN
```

This is deterministic protocol evidence only, not a claim of a live device exchange.

## No XML/XSD expectation

Executable architecture guard:

```text
validation_kind() == protocol_discovery_profile
expected_xml_operations() == ()
```

Consequences:

```text
Do not synthesize TimeService.Get*
Do not synthesize TimeService.Subscribe*
Do not search for a TimeService XML response XSD
```

TimeService availability and SNTP operation belong to the protocol/discovery runtime lane.

## Historical document-number correction - DR3012-006

The VDV 301-2 V1.0 base writing dated 07/2016 points further TimeService/SNTP implementation information to `VDV 301-2-11`.

Historical context is now resolved:

```text
VDV-Mitteilung 3002 | 10/2016 -> VDV-301-2-10 Dienst TimeService V1.0
VDV-Schrift 301-2-11 | 05/2017 -> VideoLiveService
VDV-Schrift 301-2-10 | 02/2018 -> TimeService V1.0
```

`DR3012-006` is therefore reclassified as a high-confidence wrong/stale document-number cross-reference. Resolver rule: never route TimeService to VDV 301-2-11 from that historical sentence.

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
latest strengthened run: 33197358294
no-cyclic-time-broadcast guard: PASS
no XML/XSD synthesis: PASS
```
