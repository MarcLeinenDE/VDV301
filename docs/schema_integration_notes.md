# Schema Integration Notes

Status: development integration branch, not an official VDV release branch.

This branch is used to compare and consolidate schema candidates from the official `VDVde/VDV301` repository and selected public forks. Files in this branch are intentionally classified by provenance and must not be treated as official VDV release files unless they are present in, or merged into, the official VDV repository/release.

## Baseline

- Official repository: `VDVde/VDV301`
- Baseline commit: `14880bb33beec5c5dffe96315b730bd6c094a585`
- Baseline branch: `master`
- Status: official GitHub master at the time of integration

## Integrated public fork candidates

### From `TobiasHuberAt/VDV301` master

Source commit: `1be43b9209df5b6a5ee25a3bed2528977b06103e`

Integrated as fork candidates:

- `IBIS-IP_common_V2.4.xsd`
- `IBIS-IP_Enumerations_V2.4.xsd`
- `IBIS-IP_AnalogRadioService_V2.4.xsd`
- `IBIS-IP_VideoRecordingService_V2.4.xsd`
- `IBIS-IP_DeviceManagementService_V2.3.xsd`
- `IBIS-IP_CustomerInformationService_V2.4.xsd`
- `IBIS-IP_TicketValidationService_V2.4.xsd` with V2.4 enumerations include

### From `thomlud/VDV301` master

Source commit: `82097762f38d39efd8a9e322499a453fb6da9634`

Integrated as fork candidate:

- `IBIS-IP_TicketValidationService_V2.3.xsd`

## Known gaps after integrating public candidates

- `IBIS-IP_DeviceManagementService_V2.4.xsd` still has to be derived and validated.

## Checked non-gap

- `HTMLDisplayService V2.2a`: no separate XSD is currently expected because the service describes DNS-SD / HTTP / HTML behavior and no dedicated XML operation schema.
