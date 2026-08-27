# TimeService validation backlog addendum

Status: runtime technical validation pending.

## TS-VB-001 - DNS-SD advertisement

Verify that a TimeService implementation advertises the selected VDV V1.0 profile using:

```text
_ibisip_udp._udp
```

Record service instance, host/address and port information returned by discovery.

## TS-VB-002 - sntp-server TXT metadata

Verify presence, syntax and resolved target of:

```text
sntp-server=<IP-address>
```

Separate malformed/missing metadata from an unreachable SNTP endpoint.

## TS-VB-003 - timezone TXT metadata

Verify handling of the VDV-defined timezone TXT metadata. Record the raw advertised value and profile interpretation without silently normalizing it to another timezone syntax.

## TS-VB-004 - SNTP exchange

Execute an SNTP request against the advertised endpoint and record success/failure separately from DNS-SD success.

External protocol facts such as UDP destination port behavior may be checked against RFC 4330, but must remain labelled as RFC-derived rather than VDV-PDF-derived.

## TS-VB-005 - negative discovery cases

Test diagnostics for:

```text
no TimeService advertisement
wrong service type
missing sntp-server
malformed server address
unresolvable/unreachable server
```

## TS-VB-006 - no XML-operation expectation

Ensure the validator does not require:

```text
TimeService.Get*
TimeService.Subscribe*
TimeService.*Response XML payloads
```

for this profile.

## TS-VB-007 - system-time diagnostic integration

Later SDK/tool integration should distinguish service availability from whether the local device clock is actually synchronized closely enough for other protocols such as certificate/TLS validity checks.

No task in this addendum has been executed during the historical audit.
