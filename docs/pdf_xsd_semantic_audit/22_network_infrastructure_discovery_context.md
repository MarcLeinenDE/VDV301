# Network infrastructure / discovery context audit

Status: first pass completed.

Scope:

```text
VDV 301-3, issue 02/2020, Network Infrastructure
VDV 301-2 General Conventions V2.2/V2.3/V2.4 for DNS-SD and HTTP/UDP runtime rules
RFC evidence only where needed to classify an obvious reference error
```

Purpose:

```text
Define the non-XSD validation layers needed by the future VDV301 SDK/tool without mixing physical/network recommendations, service-discovery rules and XML/XSD authority.
```

Authority separation:

```text
VDV 301-3 -> physical network, topology, cabling, switches, routing and vehicle-transition context.
VDV 301-2 General Conventions -> service publication, DNS-SD, protocol selection, endpoint identity and HTTP operation conventions.
Selected service XSD family -> XML structure validation.
External HTTP/RFC standards -> separate protocol-compliance layer where VDV does not itself define the detail.
```

No XSD is modified in this block.

## 1. VDV 301-3 is a non-XSD infrastructure profile

The document describes physical/network infrastructure rather than an XML service schema. Important requirements/recommendations include:

```text
IBIS-IP is intended for non-safety-critical applications.
If non-safety and safety-relevant networks are coupled, absence of feedback of the connecting gateway/data-diode concept is required.
Copper communication cabling follows IEEE 802.3; at least 100Base-T is recommended for standard cabling.
Ethernet data-line extension is limited to 100 m; 80 m should not be exceeded where applicable test standards require it.
For the same installation positions in a vehicle, fixed IP addresses are recommended.
In a train network every vehicle receives a unique IP address.
Separate cables for train and vehicle networks are recommended.
Train-network/vehicle-network connection is generally via router; other technologies such as VLANs are also possible.
Managed switches are not required by IBIS-IP.
If managed switches are used to support the multicast concept, IGMP support is recommended/expected for sensible use of IBIS-IP multicast.
WLAN is possible, but security, interference, RAMS/LCC and operational implications must be considered.
```

SDK consequence:

```text
These rules belong to network_inventory, runtime_network_diagnostic or manual_architecture_review layers.
They must not be converted into XML/XSD failures.
Recommendation language must remain recommendation language.
```

## 2. Discovery and communication rules come from General Conventions

The checked General Conventions state that an IBIS-IP device must implement, among other things, an Ethernet interface, TCP/IP and/or UDP/IP, HTTP processing and DNS-SD functionality.

DNS-SD publishes service endpoint information through SRV and TXT records.

### SRV profile

Observed IBIS-IP protocol labels:

```text
_ibisip_udp._udp
_ibisip_http._tcp
```

SRV supplies the service name, port and target host. Ports are therefore discovered rather than globally hard-coded.

### TXT profile

For V2.4 the documented attributes include:

```text
ver          mandatory for all IBIS-IP services
path         optional
multicast    mandatory for UDP services
sntp-server  mandatory for the time-synchronisation service
coachnumber  mandatory in a train-set IBIS-IP network
deviceclass  mandatory from IBIS-IP version 2.2 onwards
deviceID     mandatory from IBIS-IP version 2.2 onwards
```

The V2.4 version history records that the DNS-SD TXT record was extended in V2.2.

### UDP service behaviour

```text
Cyclic information -> UDP service.
UDP data is sent to multicast.
A client joins the announced multicast group to receive the telegrams.
An explicit request mechanism equivalent to HTTP service requests is not intended for this form.
A cycle below 1 s should be avoided under the stated technical assumptions.
```

### HTTP service behaviour

```text
Event-triggered information -> HTTP service.
A device offering an HTTP service must provide HTTP-server functionality.
General Conventions V2.3 introduced the explicit HTTP version requirement; V2.3+ use HTTP 1.1.
Operations with data passed to the service use HTTP POST.
Operations with no data passed to the service use HTTP GET.
```

Do not retroactively label HTTP/1.1 as an explicit V2.2 document requirement merely because later versions require it.

## 3. Service identity and mixed versions

General Conventions explicitly permit multiple versions of one service on a device, but require different ports or paths for the different versions.

Functional identity includes:

```text
service name
IBIS-IP service version
device type/device class
device ID
```

Technical identity includes:

```text
system-wide unique IP address or DNS name of the device
service name
port
optional path
```

This directly supports the SDK architecture already established by the historical schema audit:

```text
DNS-SD `ver` is an input to schema/profile resolution.
The endpoint tuple must not be confused with schema identity.
The resolver still needs service + advertised version + authority/release context where historical same-version schema revisions exist.
```

## 4. IP-addressing documentation conflict

### DISC-001 - German/English IP-allocation semantics diverge

State: confirmed cross-language documentation conflict in the checked V2.2 and V2.4 texts; prior V2.3 audit observation retained for the historical chain.

German V2.2/V2.4 says in substance:

```text
There are no specifications for IP-address allocation.
The address ranges only need to be consistent between participants.
Fixed IP addresses or DHCP are a best-practice approach.
```

The English part of the same documents instead retains an older statement that addresses are allocated using part of Zero Conf, cites RFC 2927 and says 169.254.x.x specifications must be observed for an interoperable network.

Classification:

```text
pdf_table_or_documentation_error_candidate
```

SDK handling:

```text
Do not implement a hard VDV failure requiring ZeroConf or 169.254/16 from the English text alone.
Treat consistent addressing as the safe document-common rule until the source conflict is resolved.
Fixed IP/DHCP remains best practice where stated, not a universal hard requirement.
```

Historical note:

```text
VDV 301-2 V2.0 still contains the older ZeroConf wording in both language tracks, but the German text cites RFC 3927 while the English text cites RFC 2927.
The V2.2 German text materially changes to 'no IP allocation specification' while the English text remains stale.
```

## 5. RFC reference error

### DISC-002 - RFC 2927 is not the IPv4 Link-Local RFC

The English ZeroConf paragraph cites RFC 2927 for automatic address allocation.

External RFC Editor evidence:

```text
RFC 2927 = MIME Directory Profile for LDAP Schema.
RFC 3927 = Dynamic Configuration of IPv4 Link-Local Addresses and defines the 169.254/16 link-local mechanism.
```

Classification:

```text
pdf_table_or_documentation_error_candidate
```

This external evidence is used only to classify the reference number as erroneous. It does not override the German/English VDV semantic conflict in DISC-001 and does not independently create a VDV requirement to use RFC 3927.

## 6. VDV 301-3 documentation-only findings

### NET-001 - English scope says VDV 303-3

The English scope begins with `VDV 303-3` while the document is VDV 301-3.

Classification: `pdf_label_or_heading_error_candidate`.

### NET-002 - English cabling section numbered 2.3.5 instead of 2.3.4

The German table of contents/text uses section 2.3.4 for cabling of end devices with switches. The English table of contents/text uses 2.3.5.

Classification: `pdf_label_or_heading_error_candidate`.

### NET-003 - fibre section uses IEE 802.3

The fibre section prints `IEE 802.3`; the surrounding document and standard identity are IEEE 802.3.

Classification: `pdf_table_or_documentation_error_candidate`.

These three findings have no XSD effect.

## 7. Historical DNS-SD table correction

### DISC-003 - missing German TXT-record entries corrected in V2.4

The V2.4 version history explicitly states that missing entries in the German version of table 3 were added.

Classification:

```text
ok_with_note / historically corrected documentation issue
```

SDK implication:

```text
Do not infer the V2.2/V2.3 machine profile solely from an incomplete language-specific printed table when the version history records the documentation repair.
Keep the discovery profile versioned and preserve source provenance.
```

## 8. Content-Type is not a VDV-specific rule in the checked General Conventions

Searches of the checked V2.4 General Conventions did not find `Content-Type`, `application/xml` or `text/xml` as an explicit IBIS-IP requirement.

Consequently:

```text
A future SDK may and should perform HTTP Content-Type checks where justified by the applicable HTTP/media-type standards and actual operation semantics.
But that check must be attributed to the external HTTP standards/compliance layer, not falsely reported as an explicit VDV 301-2 rule.
```

This preserves the project's cross-standard policy: use underlying standards where VDV builds on them, while keeping source authority explicit.

## 9. Runtime validation layers

Recommended SDK layers:

```text
schema_validation
  exact selected XSD family only

discovery_validation
  DNS-SD SRV/TXT syntax and required IBIS-IP attributes by profile/version

http_transport_validation
  discovered host/port/path
  HTTP version by applicable General-Conventions profile
  GET vs POST convention
  external HTTP normative checks such as Content-Type where applicable

udp_runtime_validation
  advertised multicast
  multicast join/reception
  cycle/availability diagnostics

network_diagnostic
  IP consistency/reachability
  duplicate IPs
  routing/gateway reachability
  multicast reachability/IGMP symptoms

architecture_inventory
  train vs vehicle network separation
  safety coupling/data-diode evidence
  cabling/topology/switch recommendations
```

A failed best-practice or architectural recommendation must not be reported with the same severity/authority as an XSD-invalid payload or a mandatory DNS-SD attribute violation.

## 10. Technical validation status

Not executed in this block:

```text
live DNS-SD capture against a device
HTTP request/response probe
UDP multicast join/reception test
IGMP/network capture validation
physical topology/cabling verification
```

Therefore no runtime/network item is marked validated.

## 11. Closure

```text
VDV 301-3 first-pass network-infrastructure audit completed.
General-Conventions discovery/protocol context V2.2-V2.4 integrated into a separate runtime-profile layer.
NET-001..NET-003 and DISC-001..DISC-003 documented.
No XSD changed.
```

Next block:

```text
23_cross_service_subscription_modelling_closure.md
```
