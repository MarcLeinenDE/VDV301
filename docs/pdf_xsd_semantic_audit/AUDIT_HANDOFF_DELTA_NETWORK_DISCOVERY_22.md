# Audit handoff delta - Network / discovery block 22

Status: first pass completed.

Parent branch head:

```text
37319107aaed467e9588cc0bf5cda11adfa43572
```

Key outcomes:

```text
VDV 301-3 is treated as a non-XSD physical/network profile.
DNS-SD/HTTP/UDP runtime semantics are sourced from VDV 301-2 General Conventions, not misattributed to VDV 301-3.
Runtime checks are split from schema validation.
```

New findings:

```text
NET-001 English scope says VDV 303-3.
NET-002 English cabling heading is 2.3.5 while German is 2.3.4.
NET-003 fibre section says IEE 802.3.
DISC-001 German/English IP-allocation semantics conflict in V2.2+ checked material.
DISC-002 RFC 2927 is an LDAP-schema RFC, not IPv4 Link-Local; RFC 3927 is the relevant 169.254/16 RFC.
DISC-003 V2.4 history records repair of missing German DNS-SD table entries; OK with note.
```

Critical SDK consequence:

```text
Do not hard-enforce ZeroConf/169.254 solely from the stale English wording.
Use DNS-SD ver/service identity to route to the exact service schema/profile.
Keep endpoint identity separate from schema-family identity.
HTTP/1.1 is explicit from General Conventions V2.3 onward.
GET/POST convention belongs to VDV runtime validation.
Content-Type was not found as an explicit checked VDV rule; implement it later in the external HTTP standards layer where applicable.
```

No live DNS-SD, HTTP, UDP multicast or network validation has been executed.

Next:

```text
23_cross_service_subscription_modelling_closure.md
```
