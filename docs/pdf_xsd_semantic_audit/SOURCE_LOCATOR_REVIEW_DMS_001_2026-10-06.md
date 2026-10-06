# Source-locator review — DMS-001 — 2026-10-06

Status: **structurally complete / visible-body verified / contextual asymmetry preserved**.

## Finding

DMS-001 records a historical V2.0 asymmetry between the public DeviceManagementService operation inventory and the local DMS XSD group.

This review does **not** classify that asymmetry as a schema defect.

## Visible PDF evidence

Official byte-pinned source:

- source ID: `VDV301-2_BASE_V2.0`
- SHA-256: `fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37`
- deterministic visual evidence: run `33758274931`, artifact `9894357560`

Relevant visible body:

- printed page **90**, section `7.1.1 Operationen DeviceManagementService` / operation inventory:
  - subscription operations use generic `SubscribeRequestStructure` / `SubscribeResponseStructure`
  - unsubscribe operations use generic `UnsubscribeRequestStructure` / `UnsubscribeResponseStructure`
  - `SetDeviceConfiguration` uses `DataAcceptedResponseStructure`
- printed page **95**, DMS operation-detail context continues to use shared Common response structures.

The currently accessible official PDF text layer independently confirms the same operation inventory.

## Exact XSD authority

Selected DMS V2.0 service XSD:

- `IBIS-IP_DeviceManagementService_V2.0.xsd`
- blob `74189e0da65563eeb084ec2f3c400e9668d1ee1a`
- `DeviceManagementServiceGroup`, lines 8–21

The local group contains service-specific DMS roots such as:

- `DeviceManagementService.GetDeviceInformationResponse`
- `DeviceManagementService.GetDeviceConfigurationResponse`
- `DeviceManagementService.SetDeviceConfigurationRequest`
- `DeviceManagementService.GetDeviceStatusResponse`
- service-information/status roots
- start/restart/stop service requests

It is not a one-to-one copy of the public operation inventory.

Selected Common V2.0 dependency:

- `IBIS-IP_common_V2.0.xsd`
- blob `8608e3dcd665c197c34da7f6ec6af5a3758da164`
- `SubscribeRequestStructure` line 867
- `SubscribeResponseStructure` line 874
- `UnsubscribeRequestStructure` line 880
- `UnsubscribeResponseStructure` line 887
- `DataAcceptedResponseStructure` line 893

These are exactly the generic structures referenced by the PDF operation inventory.

## Active disproof

The strongest incorrect interpretation would be:

> Every operation shown in the public DMS inventory must appear as a DMS-prefixed member of `DeviceManagementServiceGroup`; otherwise the XSD is incomplete.

That interpretation is rejected because the publication explicitly assigns generic Common structures to subscription/unsubscription and acknowledgement behavior, and the exact selected Common dependency supplies them.

Therefore the local DMS group must not be treated as a complete operation-support inventory by itself.

## Classification and SDK consequence

DMS-001 remains **contextual / defect undetermined**, with no runtime validation effect.

- do not infer unsupported operations solely from absence in the local DMS group;
- do not invent DMS-prefixed Subscribe/Unsubscribe aliases;
- account for the selected V2.0 Common dependency and the public operation inventory;
- no XSD mutation is authorized.

Existing semantic classification and runtime state remain unchanged.
