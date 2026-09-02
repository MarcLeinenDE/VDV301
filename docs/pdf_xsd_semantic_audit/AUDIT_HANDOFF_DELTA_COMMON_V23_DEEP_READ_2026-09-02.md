# Audit handoff delta — COMMON V2.3 Deep Read — 2026-09-02

## Completed block

`COMMON_V2.3` is closed for Deep Read Pass 2 as `needs_visual_review` with historical reconciliation complete.

- Independent source-only freeze: `885905349b9812b64a92b9f6d27d211fe9f2aa14`.
- Official PDF SHA-256: `d59620b22e7f6d3e47ad0dabdac5ce4b6e8ec5d2965fb68a95003ded8dd4986b`; 793,521 bytes; 58 pages.
- Fresh pin/render/read run: `33656579631`, job `100336514663`, artifact `9856965744`.
- Exact authority: official `VDV-301-2.3` Common blob `0d8926c4063c12de9a5e68b6f0addaab35a55dc1` plus its declared Enumerations V2.2 blob `2a23b512379b18e8f122ac1272cef8229fb86283`.
- EV-121: PASS, run `33657653888`, job `100340112497`, checker `tools/validate_common_v23_ev121.py`.
- New unique finding: `DRCOM23-001` — PDF documents `ArrivalExpected` and `DepartureExpected` in `StopInformationRequest`, while exact official `StopInformationRequestStructure` contains neither; EV-121 rejects both there and accepts both in `StopInformation`.
- Remaining frozen observations map to existing Common identities; exact mapping is in `audit_registry/deep_read_findings_delta_common_v23_2026-09-02.json`.

## Audit corrections discovered

- `CE-023`: V2.3 removed from affected scope. Exact pinned page 26 has no duplicate Message table under NetexMode. V2.2 remains confirmed affected.
- V2.2 machine-readable CE-004/CE-006 revalidation descriptions were swapped and are corrected: CE-004 = stale removed ServiceName values; CE-006 = DeviceState `warning` omitted from PDF.

## Guardrails

- No XSD changed.
- Exact selected XSD family remains executable authority.
- `-1:1` is VDV choice notation.
- V2.3 officially reuses Enumerations V2.2; do not latest-wins substitute V2.4.
- Historical reconnaissance does not override the independent fresh source freeze.

## Next natural unit

`COMMON_V2.4`.
