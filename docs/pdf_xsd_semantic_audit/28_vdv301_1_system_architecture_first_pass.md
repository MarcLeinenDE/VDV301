# VDV 301-1 Systemarchitektur - semantic first pass

Date: 2026-08-28
Status: completed

## Source

Official public VDV publication:

```text
VDV-Schrift Nr. 301-1
01/2014
Internetprotokoll basiertes integriertes Bordinformationssystem IBIS-IP
Teil 1: Systemarchitektur
https://www.vdv.de/vdv-301-1-ibis-ip-teil-1-systemarchitektur.pdfx
```

The public page also provides the English translation `VDV 301-1 IBIS-IP, Part 1: System architecture`. Its translation disclaimer explicitly states that it is a convenience translation of the German V1.0 document released in January 2014 and that the German original applies in case of inconsistencies.

Therefore the German document is the semantic authority for this audit block; the English file is a translation aid, not a separate normative version.

## Classification

VDV 301-1 is an architecture document, not a service XSD specification.

```text
validation lane: architecture_inventory
XSD comparison lane: none directly
relationship to VDV 301-2: Part 1 defines architecture; Part 2 specifies technical interfaces/XML structures
```

Do not invent a synthetic `VDV301-1.xsd` and do not count absence of such an XSD as a schema gap.

## Architecture facts relevant to the SDK

### ARCH-001 - service-oriented architecture

State: OK with note.

Part 1 replaces the old IBIS Wagenbus master/slave model with a service-oriented architecture. A service encapsulates functionally related functionality and exposes it over a specified interface. Operations are the callable functions of a service.

SDK consequence:

```text
service identity and operation identity are first-class resolver dimensions.
device identity is not a substitute for service identity.
a service may run on a device/application, but validation must remain service-scoped.
```

### ARCH-002 - provider/consumer direction and discovery premise

State: OK with note.

The hierarchy description states that higher functional components act as active information consumers/clients and use lower components as information providers/servers. Lower providers generally do not know the consuming service; consumers know the services from which they must retrieve information.

SDK consequence:

```text
discovery and endpoint resolution belong to the client/consumer side.
do not require a provider to maintain a static inventory of all consumers unless a service-specific subscription/callback rule says so.
```

This is compatible with the later DNS-SD/service-discovery model already captured in RV-002.

### ARCH-003 - vehicle is an architectural boundary

State: OK with note.

Part 1 treats each vehicle as a self-contained IBIS-IP system. Coupled vehicles are separate IBIS-IP systems connected through an appropriate coupling/traction interface.

SDK consequence:

```text
do not implicitly merge discovery/service inventories from coupled vehicles into one logical IBIS-IP system.
if cross-vehicle communication is observed, retain the vehicle/system boundary in evidence.
```

### ARCH-004 - safety boundary is architectural, not a cryptographic profile

State: OK with note.

Part 1 explicitly limits the presented architecture/applications to non-safety-related systems. Safety-relevant systems may be connected through defined interfaces/gateways, but non-interference must be guaranteed. The security chapter additionally requires contemporary adequate mechanisms against unauthorized intrusion and protection from adverse effects on safety-relevant components.

SDK consequence:

```text
301-1 supports architecture/security-boundary findings.
it does not define a concrete TLS/certificate/cipher profile.
do not promote modern security best practices into VDV-301-1 normative protocol failures without a separate authority source.
```

### ARCH-005 - communication classes: UDP multicast vs HTTP/TCP

State: OK with note.

Part 1 distinguishes two broad information classes:

```text
rapidly changing information (<1 s typical):
  simultaneous distribution more important than guaranteed delivery
  UDP is considered suitable
  broadcast is to be avoided for IPv6 compatibility
  UDP multicast is used instead

less frequently changing information (>1 s typical):
  reliable notification/transport is important
  TCP is suitable
  HTTP on top of TCP is specified for reliable IBIS-IP communication
```

SDK consequence:

```text
transport checks must be operation/profile-specific.
do not globally require HTTP for all IBIS-IP traffic.
do not globally require UDP for all cyclic/event traffic unless the selected service/profile specifies it.
```

Later General Conventions/service documents remain the version-specific implementation authority where they refine these rules.

### ARCH-006 - XML is the service information format

State: OK with note.

Part 1 states that XML is to be used for information exchange between services and explicitly points to Part 2 for the technical XML interface implementation.

SDK consequence:

```text
XML/XSD validation is an implementation lane derived from Part 2 service schemas.
301-1 supplies the architecture rationale but not the exact element/cardinality/type authority.
```

### ARCH-007 - SNTP/RTP historical wording must not become a prohibition

State: OK with note.

The 01/2014 architecture document says that additional IP protocols are conceivable, explicitly naming SNTP for time synchronization and RTP for audio/video streaming, but that these are not yet specified in that edition.

Later VDV 301 publications do specify TimeService and video service/protocol behavior.

SDK consequence:

```text
interpret the 301-1 wording in its 01/2014 publication context.
do not use `not specified in this edition` as a global prohibition against later VDV profiles.
never latest-wins and never oldest-wins: select authority by service/document/profile version.
```

This directly supports the already implemented TimeService and Video runtime lanes.

### ARCH-008 - functional components are broader than implemented services

State: OK with note.

Part 1 explicitly explains that not every identified functional component is necessarily specified/implemented as a service in this document generation. A functional component can be an abstract interface, application, service or device.

SDK consequence:

```text
do not infer an executable VDV service merely because a functional component exists in the architecture figure/list.
service inventory must come from service publications/schema/discovery authority, not from architecture component names alone.
```

This also prevents false findings when historical architecture terms such as System-Management/System-Documentation differ from later service packaging.

## Relation to existing audit rules

The architecture first pass supports, but does not replace:

```text
VALIDATION_AUTHORITY.md
MIXED_VERSION_VALIDATION_PREMISE.md
runtime/protocol authority matrix
RV-001 HTTP/XML
RV-002 DNS-SD/service discovery
RV-003 TimeService/SNTP
RV-004 Video RTSP/RTP
```

No XSD correction is proposed from VDV 301-1.

## Coverage result

With this block completed:

```text
semantic public VDV301 publication/version units: 48
semantic units with at least an audit first pass:    48
semantic first-pass PDF coverage:                    100 %
```

This is not the same as exhaustive page-by-page/table-by-table deep-read coverage. The project will track that separately rather than retroactively inflating the first-pass metric.
