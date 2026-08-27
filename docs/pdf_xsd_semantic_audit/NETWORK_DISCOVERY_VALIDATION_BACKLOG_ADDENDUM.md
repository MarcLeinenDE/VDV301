# Network / discovery validation backlog addendum

Status: open runtime and protocol tasks.

```text
ND-VB-001 Capture DNS-SD publication from a real/test IBIS-IP service and verify SRV service/protocol/target/port.
ND-VB-002 Verify TXT `ver` for all discovered services.
ND-VB-003 Verify `deviceclass` and `deviceID` for profiles where IBIS-IP >=2.2 requires them.
ND-VB-004 Verify UDP service `multicast` TXT value and successful multicast join/reception.
ND-VB-005 Verify HTTP endpoint construction from discovered host + port + optional path.
ND-VB-006 Verify HTTP GET for operations with no request payload and POST for operations with request data.
ND-VB-007 Verify HTTP/1.1 specifically for General-Conventions V2.3+ profiles; do not retroactively mark V2.2 from this rule alone.
ND-VB-008 Add external HTTP-standard checks, including Content-Type where applicable, with source attribution separate from VDV findings.
ND-VB-009 Detect duplicate/inconsistent IP addressing and report as network diagnostic, not XSD error.
ND-VB-010 Exercise routed train/vehicle-network and multicast diagnostics, including IGMP-related failure symptoms.
ND-VB-011 Define manual/inventory evidence fields for safety-network coupling, data-diode/no-feedback architecture, cabling length and physical separation.
ND-VB-012 Add regression test proving DISC-001 does not cause an automatic hard requirement for 169.254/16.
```

No item is marked passed until actually executed.
