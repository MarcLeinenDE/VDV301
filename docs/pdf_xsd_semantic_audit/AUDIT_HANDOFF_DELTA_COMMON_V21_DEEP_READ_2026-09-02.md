# Audit handoff delta — COMMON V2.1 Deep Read — 2026-09-02

## Completed block

`COMMON_V2.1` is closed for Deep Read Pass 2 as `needs_visual_review` with historical reconciliation complete.

- Fresh-read freeze: `11c16e618e1d86504ba4517f9d9891429d40d2ce`
- Official PDF SHA-256: `a6a22ce5670df81302ed2c54e661abc87e1314449f9bc22d41eae437839aed32`; 1,274,051 bytes; 48 pages.
- Recovery pin/render/read run: `33608210402`; retained prior evidence run: `33393002497`.
- Exact authority: official `VDV-301-2.1`.
- Common blob: `05977c9f86c7c9dd0b48f36a4a4e9be32e94659e`.
- Enumerations blob: `311464690ad60749ed8d326217787e4b8ed0b718`.
- EV-119: PASS, run `33609779315`, job `100181942929`, checker `tools/validate_common_v21_ev119.py`.
- New unique finding: `DRCOM21-001` — `StopInformationRequest.StopName` PDF `0:1` vs exact XSD `0:*`; two StopName entries validate in EV-119.
- Remaining fresh observations deduplicate/scope-extend existing Common findings; exact mapping is in `audit_registry/deep_read_findings_delta_common_v21_2026-09-02.json`.

## Independence/provenance note

The independent twenty-observation V2.1 list was completed before historical Common findings were intentionally reopened. While preparing the freeze state, `CURRENT_STATE.json` exposed historical COMMON V2.0 finding metadata after the list was already complete but before the formal freeze commit. The list was not changed using that metadata; the exposure is recorded in the freeze report and registry delta.

## Guardrails

- No XSD was changed.
- Exact selected XSD remains executable authority.
- `-1:1` is VDV choice notation, not negative cardinality.
- Do not latest-wins substitute a later Common/Enumerations family.
- Historical findings require current Evidence-Gate revalidation; EV-119 is the V2.1 executable evidence.

## Next natural unit

`COMMON_V2.2`.

Start from source/authority evidence, not old chat history. Byte-pin and render the official COMMON V2.2 PDF, establish the exact authority route, complete an independent fresh read and freeze it before historical Common reconciliation.
