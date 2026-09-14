# Finding revalidation — TimeService (TS)

Status: **completed** on 2026-09-14 under the current `FINDING_EVIDENCE_GATE.md`.

## Scope

Frozen findings: `TS-001` and `TS-002`. Frozen inventory remains exactly **192 entries**.

## Authority and evidence

- Evidence: **EV-159**; successful closure run **34816125569**.
- Independently successful EV-159 run: **34815684895**, job **103885751905**, artifact **10336194085**, digest `sha256:4d5c36f36c468b92e1a3ca962eb1e76b8670f6460f2ecf667bd1cdc2c2e2d010`.
- Source/render pin run: **34814542791**, job **103882386972**, artifact **10336172299**, digest `sha256:c24cfc7d8b80652a5caaeafa4d131f31c32fcbe85e45cfb4a6bb5edb2f789c94`.
- Official VDV 301-2-10 TimeService V1.0 PDF: SHA-256 `d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3`, 515920 bytes, 10 pages.
- Physical page **4** contains the bilingual document-number contradiction used for TS-002. Physical page **6** contains the SNTP/RFC-4330 and DNS-SD TimeService profile used for TS-001. Poppler text output is retained only as a byte-derived fingerprint; semantic page evidence is rendered visual evidence.
- Exact official VDV-301-1.0 commit `f5b53785f703e898632603eec3bfa3555a79fdba` / tree `729bbe3270e52fed3e0641466048a745d5a09b32` and VDV-301-2.0 commit `f2569a91f0a7c737a0ca7c0280b28ad223d7ee08` / tree `11daf0ebb3b26745c036ee19a547ad16d39f922c` contain no dedicated TimeService XSD.
- `IBIS-IP_Enumerations_V1.0.xsd` blob `a9bea5bc73003ed91ded8519db06c32c4067831d` nevertheless contains `TimeService` in `ServiceNameEnumeration`.
- RV-003 (`ff6e3fcd35d4c2f6bff760b3e86f5adb0e72156c`) reran the deterministic SNTP/DNS-SD profile, including positive/negative cases, protocol routing, no invented XML operations and the non-cyclic delivery invariant.
- The complete **50-file root XSD pool** was recompiled and byte-hashed before/after EV-159; no XSD changed.

## Terminal states

| Finding | Terminal state | Revalidation result |
|---|---|---|
| `TS-001` | `contextual_not_defect` | TimeService V1.0 is a protocol/discovery profile by design, not an XML/XSD service. Exact VDV-301-1.0 and VDV-301-2.0 release trees plus the 50-root integration pool contain no dedicated TimeService XSD; ServiceNameEnumeration still exposes TimeService, and RV-003 executes the SNTP/DNS-SD profile including the no-cyclic and no-XML guards. |
| `TS-002` | `context_verified` | The exact byte-pinned official TimeService writing visibly contains the bilingual foreword contradiction on physical page 4: the German text identifies VDV 301-2-10 while the English text says VDV 301-2-1. This is a documentation reference error, not a schema defect. |

## Mutation decision

- XSD mutation: **none**.
- Frozen inventory mutation: **none**.
- Registry/status mutation: only `TS-001`, `TS-002` and the TS block/counter handoff.

## State transition

- Before: **155/192 terminal**, **37 pending**, first pending `TS-001`.
- After: **157/192 terminal**, **35 pending**, first pending `TSD-001`.
- Next block: **TSD**.
