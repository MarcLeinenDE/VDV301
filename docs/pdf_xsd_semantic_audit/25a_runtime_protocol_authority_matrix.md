# Block 25a - runtime/protocol authority matrix

Status: source/authority baseline completed; implementation profiles follow in 25b-25e.

Purpose:

```text
Prevent the future SDK/tool from reporting an external protocol rule, a VDV-specific rule,
and a diagnostic heuristic as if they had the same authority.
```

## Authority classes

```text
vdv_normative
  Requirement or profile fact stated by the applicable VDV 301 writing.

external_normative
  Requirement from an external standard that governs the protocol/media layer used by VDV.
  It is not to be presented as text literally stated by VDV unless VDV explicitly incorporates it.

vdv_profile_exception_or_specialization
  VDV-specific profile behavior that specializes or appears to diverge from generic external-standard expectations.
  The VDV-selected profile must be preserved and the cross-standard tension exposed rather than silently normalized.

diagnostic_heuristic
  Useful operational test or best practice without a direct normative mandate for the tested VDV profile.
```

Severity and authority are separate dimensions. For example, a violated external `SHOULD` may be a warning, while a missing VDV-mandatory TXT key is a VDV profile error.

## HTTP / XML transport

### VDV-specific rules already established

From the checked General Conventions chain:

```text
HTTP services are used for event-triggered/request-response information.
Operations with request data use POST.
Operations without request data use GET.
General Conventions V2.3+ explicitly require HTTP/1.1.
Do not retroactively report HTTP/1.1 as an explicit V2.2 writing requirement solely from the later version.
```

Authority: `vdv_normative`.

### Content-Type authority

The checked General Conventions V2.4 audit found no explicit VDV requirement for:

```text
Content-Type
application/xml
text/xml
```

Therefore a Content-Type check belongs to the external HTTP/XML layer.

RFC 9110, HTTP Semantics, section 8.3 defines `Content-Type` as the media type of the representation. A sender generating a message containing content SHOULD generate Content-Type unless the intended media type is unknown.

RFC 7303 standardizes XML media types and XML structured-syntax handling:

```text
application/xml         standard XML media type; recommended generic application type
text/xml                alias for application/xml semantics
<type>/<subtype>+xml    structured-syntax convention indicating an XML-based media type
```

SDK rule design:

```text
HTTP-X01 malformed Content-Type header
  authority: external_normative
  result: protocol error

HTTP-X02 body present but Content-Type absent
  authority: external_normative / RFC 9110 SHOULD
  result: warning by default, not a fabricated VDV hard failure
  diagnostic XML sniffing may continue, but must be reported as diagnostic inference

HTTP-X03 application/xml on an XSD-backed VDV XML representation
  authority: external_normative
  result: compatible

HTTP-X04 text/xml on an XSD-backed VDV XML representation
  authority: external_normative
  result: compatible alias; optional note that application/xml is recommended by RFC 7303

HTTP-X05 syntactically valid +xml media type
  authority: external_normative
  result: XML-capable media type; do not automatically claim the custom media type itself is a VDV-defined type

HTTP-X06 declared non-XML media type for an operation whose selected VDV payload profile is XML/XSD
  authority: combined operation semantics + external media-type semantics
  result: media/payload mismatch
  do not call this an explicit VDV Content-Type rule

HTTP-X07 charset/encoding
  authority: external_normative / RFC 7303
  result: respect media-type charset/BOM/XML encoding rules; implement separately from XSD structure validation
```

### HTMLDisplayService exception

HTMLDisplayService is not an XSD-backed XML service. Its checked V2.1/V2.2/V2.2a writings explicitly avoid imposing HTTP-content requirements and leave browser/content compatibility to project participants.

Therefore:

```text
Do not apply the XSD-backed XML Content-Type profile to HTMLDisplayService.
For HTMLDisplayService, only generic HTTP correctness and project-configured browser/content policy apply unless a later VDV profile says more.
```

## DNS-SD / discovery

### VDV-specific profile

Checked General Conventions V2.2+ establish, among other profile facts:

```text
DNS-SD functionality is required.
ver is mandatory for IBIS-IP service advertisements.
deviceclass and deviceID are mandatory from IBIS-IP 2.2 onward.
multicast is mandatory for UDP services.
path is optional where the selected profile uses it.
IBIS-IP protocol labels include _ibisip_udp._udp and _ibisip_http._tcp.
Target host and port are discovered; ports are not globally fixed.
Different versions of one service on a device use different port or path.
```

Authority: `vdv_normative`.

### Generic DNS-SD standard

RFC 6763 defines the generic DNS-SD model:

```text
PTR discovers service-instance names.
Each service instance is described by an SRV record and TXT record with the same instance name.
SRV supplies target host and port.
TXT supplies service-specific key/value metadata.
Every DNS-SD service advertised by the PTR+SRV+TXT convention has a TXT record, even if empty.
Unknown TXT keys are ignored by generic DNS-SD clients.
```

Authority: `external_normative`.

DNS-SD is compatible with both unicast DNS and Multicast DNS. RFC 6762 defines mDNS specifically for DNS-like operation on the local link without conventional unicast DNS infrastructure.

SDK consequence:

```text
Do not equate the words DNS-SD with an unconditional mDNS-only requirement unless the selected VDV profile explicitly requires that transport/discovery mode.
Model DNS-SD record semantics separately from the mechanism used to obtain the records.
```

### HTMLDisplayService V2.2/V2.2a specialization/tension

The checked HTMLDisplayService V2.2/V2.2a profile publishes:

```text
SRV: HtmlDisplayService, protocol, port, host
TXT: content, url
```

It states that `url` contains the access URL and that the SRV port is provided but has no meaning.

Generic RFC 6763, in contrast, defines the SRV target host/port as the location where the advertised service is reached and says target/port must not be duplicated as TXT key/value attributes.

Classification for SDK design:

```text
HDS-X01
state: cross-standard profile tension requiring explicit VDV specialization
classification: vdv_profile_exception_or_specialization
not_a_schema_finding: true
```

Handling:

```text
For HTMLDisplayService V2.2/V2.2a, follow the VDV service-specific `url` semantics for locating display content.
Do not replace that URL with SRV host/port merely to make the profile look like generic DNS-SD.
Still validate the surrounding DNS-SD records syntactically and report the specialization as a profile note.
```

This should not be generalized to normal IBIS-IP HTTP services.

## TimeService / SNTP

VDV 301-2-10 V1.0 explicitly delegates time/date synchronization to SNTP according to RFC 4330 and advertises the source through the TimeService discovery profile.

VDV profile facts already established:

```text
service type: _ibisip_udp._udp
TXT: sntp-server=<IP-address>
TXT: timezone=<VDV profile value>
no VDV XML GetTime/CurrentTime operation is expected
```

Authority:

```text
service discovery/TXT semantics -> vdv_normative
SNTP message/exchange semantics -> external protocol authority explicitly referenced by VDV
```

Important standards-version rule:

```text
RFC 4330 is now obsolete and was obsoleted by RFC 5905.
Nevertheless, TimeService V1.0 explicitly references RFC 4330.
The SDK must not silently replace the VDV-selected SNTP profile with a later RFC merely because a newer standard exists.
```

A modern diagnostics layer may additionally report compatibility with current NTP implementations, but must label that as a separate control.

RFC 4330 specifies UDP and identifies NTP/SNTP destination port 123 for client requests.

## Video RTSP/RTP

The checked VideoLiveService V2.0 writing states that RTP and RTSP are used for real-time video transmission, publishes an `rtspURI`, and delegates stream START/STOP behavior to RTSP rather than defining VDV XML START/STOP operations.

The checked writing does not identify a specific RTSP or RTP RFC number in its references/searchable text.

Therefore:

```text
VDV-specific rule:
  extract/use the published rtspURI and keep media control separate from the IBIS-IP XML operation.

Not justified as a VDV-specific rule from current evidence:
  require RTSP/1.0 specifically
  require RTSP/2.0 specifically
  claim a particular RTP RFC version was named by the VDV writing
```

External standards context:

```text
RFC 2326 defines RTSP 1.0 and is now obsolete.
RFC 7826 defines RTSP 2.0 and obsoletes RFC 2326; RTSP 2.0 is not generally backwards compatible with RTSP 1.0 except for basic version negotiation.
RFC 3550 defines RTP and RTCP for real-time media transport.
```

SDK handling:

```text
RTSP-V01 parse the VDV-provided URI and record scheme/host/port/path/userinfo without exposing credentials in normal logs.
RTSP-V02 attempt protocol negotiation/capability observation against the endpoint where permitted.
RTSP-V03 report the observed RTSP protocol version separately from VDV conformance unless an applicable VDV source pins it.
RTP-V01 validate media reception separately from RTSP control success and separately from XML/XSD success.
RTP-V02 expose packet/timestamp/sequence diagnostics as external-protocol/runtime evidence, not XML findings.
```

## Network diagnostic / heuristics

Useful checks that are not automatically hard VDV failures include:

```text
duplicate IP detection
endpoint reachability
route/gateway diagnostics
multicast join/reception symptoms
IGMP state where managed-switch multicast architecture is used
latency/time-offset observations
certificate-validity problems caused by an incorrect system clock
```

Each diagnostic must carry its own source/severity and must not be reported as `xsd_invalid`.

## Stable external references

```text
RFC 9110 - HTTP Semantics
https://www.rfc-editor.org/rfc/rfc9110.html

RFC 7303 - XML Media Types
https://www.rfc-editor.org/rfc/rfc7303.html

RFC 6763 - DNS-Based Service Discovery
https://www.rfc-editor.org/rfc/rfc6763.html

RFC 6762 - Multicast DNS
https://www.rfc-editor.org/rfc/rfc6762.html

RFC 4330 - Simple Network Time Protocol Version 4
https://www.rfc-editor.org/rfc/rfc4330.html

RFC 5905 - Network Time Protocol Version 4; obsoletes RFC 4330
https://www.rfc-editor.org/rfc/rfc5905.html

RFC 2326 - RTSP 1.0; obsolete
https://www.rfc-editor.org/rfc/rfc2326.html

RFC 7826 - RTSP 2.0; obsoletes RFC 2326
https://www.rfc-editor.org/rfc/rfc7826.html

RFC 3550 - RTP/RTCP
https://www.rfc-editor.org/rfc/rfc3550.html
```

## Next

```text
25b HTTP/XML transport profile
- reusable Content-Type classifier
- deterministic positive/negative unit samples
- no live device required

25c DNS-SD profile validator
25d TimeService/SNTP profile
25e RTSP/RTP boundary
```
