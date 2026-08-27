# HTMLDisplayService protocol profile history and first-pass closure

Status: first-pass historical audit closed for HTMLDisplayService V2.1, V2.2 and V2.2a. This is a non-XSD service profile; no service-XSD compilation claim is applicable.

Source block:

```text
docs/pdf_xsd_semantic_audit/10_html_display_service_historical_start.md
```

## 1. Service model closure

HTMLDisplayService is not treated as a missing-schema service.

The checked documentation describes this flow:

```text
DNS-SD publishes how to reach the HTMLDisplayService.
A multifunction display/browser uses the discovered URL.
The browser contacts a web server.
Display content is delivered as HTML over HTTP.
```

The V2.1/V2.2/V2.2a documents compare the service to TimeService and state that it does not define its own protocol.

The checked official VDV release-tag XSD pools contain no dedicated HTMLDisplayService XSD.

Result:

```text
HTMLDisplayService is intentionally a discovery/HTTP profile, not a normal XML service-XSD family.
```

## 2. V2.1 executable/profile facts

Document:

```text
VDV 301-2-17 V2.1, 07/2018
```

DNS-SD profile:

```text
SRV:
  service name: HtmlDisplayService
  protocol: _http._tcp
  port
  target host

TXT:
  content
  path
```

URL construction:

```text
http://host:port/path
```

`path` may include query or fragment components.

`content` is a project-specific content name; examples in the document include Routepath, MFD and Connectioninformation. If multiple URLs are published, separate DNS-SD entries are used.

## 3. V2.2 profile delta

Document:

```text
VDV 301-2-17 V2.2, 08/2019
```

The functional service remains browser/HTTP based. The relevant technical change is in service discovery.

DNS-SD profile:

```text
SRV:
  service name: HtmlDisplayService
  protocol: _http._tcp
  port
  host

TXT:
  content
  url
```

The document says:

```text
url contains the URL for access.
url may also contain query or fragment components.
Port is provided by the SRV record but has no meaning.
Host indicates which device publishes the service.
```

Version history records:

```text
New TXT entry: url.
It replaces host, port and path as the access-address construction mechanism.
```

This is a real version-specific profile change and must be represented in the later SDK resolver.

## 4. V2.2a profile delta

Document:

```text
VDV 301-2-17 V2.2a, 02/2021
```

The `content` + `url` TXT model remains.

Protocol discovery changes to:

```text
_http._tcp               deprecated / future use discouraged
_ibisip_http._tcp        introduced for future IBIS-IP-conform discovery
```

The document says the next service version after 2.2 is intended to use `_ibisip_http._tcp` and remove `_http._tcp` in order to align with the V2.2 General Conventions. It also allows project-specific use of `_ibisip_http._tcp` already with V2.2 by mutual agreement.

Important resolver implication:

```text
Do not collapse V2.2 and V2.2a into one exact discovery profile without retaining the compatibility note.
V2.2a explicitly recognises both protocol labels, with _http._tcp deprecated.
```

## 5. HTTP content scope

The checked service documents explicitly state that no requirements are imposed on the HTTP content because such requirements would become obsolete quickly; compatibility is to be agreed between display supplier and service provider.

Audit consequence:

```text
Do not invent an HTML/XSD payload schema for this service.
Do not derive a Content-Type or browser-feature requirement from VDV 301-2-17 alone if the document does not state it.
Any additional HTTP-level conformance rule used by the SDK must be grounded separately in VDV General Conventions and/or the applicable HTTP standards and labelled with that source authority.
```

## 6. HDS-001 closure - no dedicated XSD

State: closed as OK with note.

Classification:

```text
mismatch_kind: service_modelling
likely_source_issue: ok_with_note
classification_confidence: high
final_handling_bucket: no_action_note
```

Executable/tool behaviour:

```text
HTMLDisplayService must not enter the normal service-XSD compiler path.
The SDK needs a non-XSD service-profile validator for this service.
Shared IBIS-IP schema facts such as ServiceNameEnumeration and DeviceClassEnumeration remain independently applicable where referenced by other XSD-backed services.
```

## 7. SDK routing matrix

```text
HTMLDisplayService V2.1
  validation kind: discovery_http_profile
  dedicated service XSD: none by design
  DNS-SD protocol: _http._tcp
  TXT keys: content, path
  access URL: derived from host + port + path

HTMLDisplayService V2.2
  validation kind: discovery_http_profile
  dedicated service XSD: none by design
  DNS-SD protocol: _http._tcp
  TXT keys: content, url
  access URL: url TXT value
  compatibility note: _ibisip_http._tcp may be used project-specifically by mutual agreement per later V2.2a note

HTMLDisplayService V2.2a
  validation kind: discovery_http_profile
  dedicated service XSD: none by design
  DNS-SD protocols: _http._tcp deprecated; _ibisip_http._tcp introduced/recommended for future alignment
  TXT keys: content, url
  access URL: url TXT value
```

## 8. Validation backlog

No dedicated service XSD exists to compile for this block.

Later executable tests should instead include:

```text
HDS-VB-001: V2.1 DNS-SD positive profile with content + path and _http._tcp.
HDS-VB-002: V2.1 negative profile using V2.2-only url semantics without explicit compatibility rule.
HDS-VB-003: V2.2 positive profile with content + url and _http._tcp.
HDS-VB-004: V2.2a positive profile with content + url and _ibisip_http._tcp.
HDS-VB-005: V2.2a compatibility test for deprecated _http._tcp.
HDS-VB-006: multiple-content publication via separate DNS-SD entries.
HDS-VB-007: HTTP fetch/profile checks only for rules backed by VDV General Conventions or external HTTP standards; do not infer them from this service document alone.
```

## 9. First-pass result

```text
HTMLDisplayService V2.1/V2.2/V2.2a historical first pass: closed.
No dedicated service XSD: intentional, not a historical backfill gap.
No XSD file added or changed.
HDS-001: closed OK with note.
Version-specific discovery profile retained.
No PR, comment or merge performed.
```

## 10. Next audit block

According to the service sequence in the audit scope matrix:

```text
docs/pdf_xsd_semantic_audit/11_system_monitoring_service_historical_start.md
```

Target:

```text
SystemMonitoringService V2.2 PDF vs IBIS-IP_SystemMonitoringService_V2.2.xsd and its exact dependency pool.
```
