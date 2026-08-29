# Audit handoff delta — SystemMonitoringService V2.2 Deep Read

Date: 2026-08-29

## Permanent result

- SMS V2.2 official PDF pinned: `996f639a81cb91ad20a8e78b6213e7c85d41ff0ec42caba4208d6c4652b140f4`, 847416 bytes, run `33268541691`.
- Exact official XSD family: SMS `d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c`, Common `468fee6d177e7185dbcd5d3f90cfb114e29e01ae`, Enums `2a23b512379b18e8f122ac1272cef8229fb86283`.
- Full render/read: run `33268591224`, job `99142914429`; fresh-read freeze `625bb9a4d19f1f1c47a529686defa9b1368c80ff`.
- EV-116: checker `tools/validate_sms_v22_ev116.py`, run `33269006407`, job `99144006184`, PASS on exact official authority.
- SMS-001 revalidated as contextual non-defect/generic Common subscription modelling.
- SMS-002 executable-confirmed: PDF SystemStatus headings conflict with exact ServiceStatus operation/root naming.
- SMS-003 context-verified wrong-service foreword copy/paste.
- SMS-004 upgraded from unresolved to context-verified PDF reference-number error.
- New findings: DRSMS22-001 broken cross-reference, DRSMS22-002 ServiceStatus/device-state prose copy-paste, DRSMS22-003 spelling error, DRSMS22-004 Req./Resp. label omission.
- CE-012, CE-018 and CE-019 are not revalidated by this SMS closure and stay in the Common lane.
- No XSD changed.

## Next

Start `ARA_V2.4` (AnalogRadioService V2.4, VDV 301-2-19) document-first: own official PDF pin, exact authority classification/family, fresh read before historical AnalogRadio finding reconciliation.
