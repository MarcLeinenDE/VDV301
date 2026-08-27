# Block 25c / RV-002 - DNS-SD and VDV service-discovery profile

Status: deterministic classifier implemented and executable-tested. No live DNS, mDNS or device-discovery claim is made.

## Evidence run

```text
GitHub Actions run: 33119080288
run number: 12
head tested: 9e3462247c5a552c17889d68ca863cb882caeeea
job: 98681121737
environment: Ubuntu 24.04.4 / Python 3.12.14 / lxml 6.1.2
discovery_status: 0 / PASS
```

The run also re-confirmed the prior EV and RV-001 checks with status 0.

## Reusable implementation

```text
tools/runtime_discovery_profile.py
tools/validate_discovery_runtime_rv002.py
```

The implementation accepts an already-observed/parsed DNS-SD advertisement. It intentionally does not perform DNS or mDNS network I/O. This keeps three questions separate:

```text
1. How was the service instance discovered?            -> discovery transport / PTR lookup
2. Are SRV/TXT records structurally coherent?          -> RFC 6763 layer
3. Does the advertisement match the selected VDV profile? -> VDV layer
```

## Generic DNS-SD checks

Deterministic evidence confirms:

```text
SRV + TXT coherent instance                     PASS
mDNS accepted as a DNS-SD transport             PASS
unicast DNS accepted as a DNS-SD transport      PASS
missing TXT record detected                     PASS
mismatched SRV instance name detected           PASS
mismatched TXT instance name detected           PASS
missing/invalid SRV target+port detected         PASS
```

Authority:

```text
external_normative / RFC 6763
```

The classifier therefore does not equate DNS-SD with mandatory mDNS. Transport choice and service-discovery record semantics remain separate.

## VDV General-Conventions V2.2+ checks

For the selected V2.2+ profile the classifier checks:

```text
DISC-V01  TXT ver
DISC-V02  TXT deviceclass
DISC-V03  TXT deviceID
DISC-V04  TXT multicast for UDP profiles
DISC-V07  protocol label matches selected HTTP/UDP service family
```

Executable cases:

```text
HTTP profile with ver/deviceclass/deviceID                    PASS
HTTP expects _ibisip_http._tcp                               PASS
missing deviceID is detected                                 PASS
UDP profile with multicast                                   PASS
missing UDP multicast is detected                            PASS
HTTP profile advertised with UDP protocol label is detected PASS
```

Historical guard:

```text
General-Conventions V2.1 input does not receive the V2.2+ mandatory TXT-key rules.
```

This prevents later discovery requirements from being applied retroactively.

## HTMLDisplayService version-specific handling

### V2.1

```text
protocol: _http._tcp
required TXT: content + path
content endpoint: SRV target + SRV port + TXT path
```

Executable evidence:

```text
profile valid
endpoint construction valid
```

### V2.2

Canonical profile:

```text
protocol: _http._tcp
required TXT: content + url
content endpoint: TXT url
```

Executable evidence confirms that the content endpoint is taken from `url` and is not reconstructed from the SRV target/port.

The later V2.2a-documented project-agreement transition using `_ibisip_http._tcp` for V2.2 is accepted only with a note, not silently treated as the canonical V2.2 form.

### V2.2a

```text
preferred protocol: _ibisip_http._tcp
legacy _http._tcp: accepted but deprecated
required TXT: content + url
content endpoint: TXT url
```

Both preferred and legacy/deprecated cases behave as intended in the deterministic test.

### HDS-X01 specialization

The HTMLDisplay V2.2/V2.2a content endpoint rule is retained as a service-specific VDV specialization:

```text
TXT url is the actual content address.
SRV data remains discovery metadata but is not used to reconstruct the content-resource URL.
```

The SDK must not generalize this rule to ordinary IBIS-IP HTTP services.

## Negative HDS cases

Executable evidence confirms:

```text
V2.2 missing TXT url -> profile error + no resolved content endpoint
wrong service name   -> profile error
```

## Authority matrix alignment

`generated/runtime_protocol_authority_matrix.csv` now contains `DISC-V07` explicitly so code, evidence and machine-readable authority metadata use the same stable check ID.

The matrix also distinguishes checks that this deterministic classifier cannot yet prove:

```text
DNS-X01  actual PTR discovery operation
DISC-V05 actual endpoint use/reachability
DISC-V06 simultaneous advertisements for multiple service versions using different port/path
MDNS-X01 actual multicast-DNS transport behavior
```

Those require a live or packet/capture-backed integration layer.

## What RV-002 does NOT claim

Not executed:

```text
real DNS query
real mDNS query/response
PTR browse against an IBIS-IP device
SRV/TXT packet capture
host-name resolution
TCP/UDP endpoint reachability
multicast group join
multiple simultaneously advertised versions on one device
TTL/cache/record-expiry behavior
```

No live-device conformance conclusion is made from the deterministic classifier alone.

## Result

```text
RV-002 deterministic DNS-SD / VDV discovery classifier: PASS
```

Next planned runtime evidence:

```text
RV-003 - TimeService V1.0 / SNTP
- VDV-specific TimeService discovery metadata
- RFC 4330 packet/profile semantics
- no XML-operation expectation
- separate modern RFC 5905 control note without latest-wins substitution
```
