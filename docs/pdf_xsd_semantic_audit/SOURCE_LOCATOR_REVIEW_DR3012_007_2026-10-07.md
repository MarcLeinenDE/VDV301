# Source-locator review — DR3012-007 — 2026-10-07

Status: **complete / visible-body verified / documentation copy-paste defect confirmed**.

## Finding

VDV 301-2 V1.0 contains a direct semantic contradiction inside the `StopService` request table: the structure description says the identified service is stopped, while the `ServiceSpecification` member description says it points to the service to be started.

## Visible PDF evidence

Official source:
- source ID: `VDV301-2_V1.0_DE`
- SHA-256: `2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75`
- printed page: **63**
- section: **7.1.24 Datenstrukturen der Operation StopService**
- subsection: **7.1.24.1 Request**
- table: **Tabelle 21 Beschreibung DeviceManagementService.StopServiceRequestStructure**

The visible structure description states:

`Struktur, mit deren Hilfe ein bestimmter Dienst (identifiziert über die ServiceSpecification) auf einem Gerät gestoppt wird.`

The immediately following `ServiceSpecification` row states:

`Verweis auf den zu startenden Dienst (vgl. VDV 301-2-1)`

These two statements contradict each other within the same StopService request table.

EV-129 page-63 PNG SHA-256:
`8b5d94ed59fef404b29af34cedb7218e9ae564fbc8f5abcf7ffca055739b2839`

## Disproof attempt

The wording cannot be explained as a StartService substructure or a generic action description:

- the section heading is explicitly `StopService`;
- the structure is explicitly `DeviceManagementService.StopServiceRequestStructure`;
- the structure-level description explicitly says the service is stopped;
- only the field-level description switches to `zu startenden Dienst`.

This is therefore an evident copy/paste residue.

## Classification and SDK behavior

Confirmed documentation semantics/copy-paste defect only.

- XML/XSD validity behavior: **unchanged**
- XSD authority: **not applicable to this documentation defect**
- runtime matcher: **not applicable**
- SDK behavior: **informational**
- no alternate StartService meaning or operation alias is derived from the erroneous field description.

The operation remains StopService; the field identifies the service to be stopped.
