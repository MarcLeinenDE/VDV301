# Source-locator review — DMS-005 — 2026-10-06

Status: **complete / visible-body verified / documentation identifier mismatch confirmed**.

## Result

DMS-005 is a confirmed PDF identifier mismatch in V2.2 and V2.4.

The visible response choice in Table 17 uses:
`DeviceManagementService.DeviceStatusInformationResponseData`

The selected schemas use:
`DeviceManagementService.GetDeviceStatusInformationResponseData`

## Evidence

- DMS V2.2 official PDF, printed page 23, Table 17: non-Get spelling in the choice branch; adjacent type/reference uses the Get-prefixed form.
- DMS V2.4 official PDF, printed page 22, Table 17: the same PDF-only non-Get spelling persists.
- V2.2 official XSD blob `c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d`, line 148: only the Get-prefixed element is declared.
- V2.4 candidate/integration XSD blob `d222dfd98b2be3777576388da7ace8f333d24c3f`, line 148: also only the Get-prefixed element is declared.

No exact non-Get global declaration exists in either selected schema.

## Consequence

The PDF spelling is documentation guidance only and must not create a compatibility alias. Preserve the selected schema result. V2.4 remains candidate/integration authority and is never relabelled official.
