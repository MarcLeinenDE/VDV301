# Finding revalidation — VDV 301-1 V1.0

Status: **completed** on 2026-09-03 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen legacy entries: `DR3011-001` … `DR3011-003`. The frozen inventory remains exactly **192 entries**.

## Evidence

- Evidence gate: **EV-128**, workflow run **33763071038**.
- Official Part 1 V1.0 PDF SHA-256: `5418f24190468a1823699688cf86f98d812591ad2c7c2eada07b1d34889c20c2`.
- Official Part 2 V1.0 PDF SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`.
- Existing full Part-1 visual render: run **33725750019**, artifact **9881897572**; relevant pages 2, 10, 11 and 34 were re-inspected.
- `DR3011-002` is additionally cross-checked against the selected historical `IBIS-IP_SystemManagementService_V1.0.xsd`.
- Root XSD pool regression gate rerun after EV-128.

## Terminal states

| Finding | Terminal state | Result |
|---|---|---|
| DR3011-001 | `context_verified` | Page 2 visibly assigns 5.1.2 to System-Dokumentation and 5.1.3 to System-Management; page 10 nevertheless points the SystemManagementService example to 5.1.2. |
| DR3011-002 | `context_verified` | Part 1 visibly uses stale/conceptual `GetDeviceState` / `GetSystemStatus` / `SystemStatus` subscription names. Official Part 2 V1.0 and the selected historical XSD use `GetDeviceStatus` / `GetServiceStatus` terminology. No aliases are created. |
| DR3011-003 | `context_verified` | Page 34 visibly contains two consecutive `IBIS-IP` abbreviation rows with slightly different expansion wording. |

All three are documentation/context findings. They do not alter XML validity behavior and are not promoted into SDK conformance rules.

## Closure

- Frozen legacy terminal count: **60 / 192**
- Frozen legacy pending count: **132 / 192**
- XSD mutation: **none**
- Frozen inventory mutation: **none**
- Next revalidation block: **VDV301-2**
