# Mixed-version validation premise

Status: audit premise and later tool/SDK requirement.

Purpose:

```text
Document why the audit must cover every historical VDV301 service version and why the later validator must support mixed-version real-world systems.
```

## Background

Practical deployments do not only use the latest VDV301 version.

Field systems may contain:

```text
- older V1.0 services,
- V2.0 / V2.1 / V2.2 / V2.3 services,
- current or candidate V2.4 services,
- mixed service-version combinations inside the same IBIS-IP system.
```

Therefore the audit must not treat V2.4 as a replacement for all earlier versions.

## Core premise

```text
Every service version that is or was published must be independently auditable and, where an XSD exists, independently validatable.
```

This means:

```text
VDV301 service V1.0 must be checked against its V1.0 PDF/XSD basis.
VDV301 service V2.0 must be checked against its V2.0 PDF/XSD basis.
VDV301 service V2.1 must be checked against its V2.1 PDF/XSD basis.
VDV301 service V2.2 must be checked against its V2.2 PDF/XSD basis.
VDV301 service V2.3 must be checked against its V2.3 PDF/XSD basis.
VDV301 service V2.4 must be checked against its V2.4 PDF/XSD basis.
```

Where no matching XSD exists in the branch, the audit must classify the situation instead of guessing.

## No latest-wins rule

Do not apply the newest schema version to older payloads automatically.

```text
A value that is valid in V2.4 is not automatically valid in V2.0.
A value that is invalid in V2.4 may still be valid in an older version if that older XSD allowed it.
A correction in a later PDF/XSD version must not be silently backported to earlier versions.
```

Tool consequence:

```text
Validation must be version-scoped, not global.
```

## Service version and dependency pool

A validation target is not only a service XSD file. It is the service XSD plus the exact shared dependency pool used by that service version.

Example pattern:

```text
TicketValidationService V2.2
  -> IBIS-IP_TicketValidationService_V2.2.xsd
  -> IBIS-IP_common_V2.2.xsd
  -> IBIS-IP_Enumerations_V2.2.xsd

TicketValidationService V2.4
  -> IBIS-IP_TicketValidationService_V2.4.xsd
  -> IBIS-IP_common_V2.4.xsd
  -> IBIS-IP_Enumerations_V2.4.xsd, if the candidate/version-family alignment is used
```

If the official upstream file currently uses a mixed dependency family, that exact state must be documented before deciding whether it is a defect, candidate correction, or compatibility reality.

## Mixed system interpretation

A real IBIS-IP system can legitimately expose different services with different versions.

Therefore the later tool/SDK should model validation as:

```text
System
  Service A -> declared/selected service version -> matching XSD pool
  Service B -> declared/selected service version -> matching XSD pool
  Service C -> declared/selected service version -> matching XSD pool
```

A provider-facing report should avoid global language such as:

```text
The system is invalid against VDV301.
```

Preferred language:

```text
The payload for <ServiceName> <Version> fails against the XSD pool used for that service version.
```

## Finding requirements

Every finding must identify the version scope.

Good:

```text
TVS V2.4: VehicleData.RouteDeviation PDF type RouteDirectionEnumeration vs XSD RouteDeviationEnumeration.
```

Not sufficient:

```text
RouteDeviation mismatch.
```

For shared Common/Enums findings, record the affected version range.

Example:

```text
CE-005 TripInformation.AdditionalTextMessage: historical mismatch observed across V2.0-V2.4.
```

## Audit impact

The audit sequence must be:

```text
1. Build the complete public PDF/XSD coverage matrix.
2. Close Common/Enums historically, because shared types affect many service versions.
3. Audit each service version against its matching historical PDF/XSD basis.
4. Record candidate/fork/integration material separately from official upstream files.
5. Create validation backlog entries per version pool.
```

## Validator / SDK impact

The later SDK should eventually support:

```text
- service-version aware schema loading,
- exact dependency-pool selection,
- explicit handling of missing or special/no-XSD services,
- per-service validation results in mixed-version systems,
- explanatory PDF/XSD notes without weakening XSD validation,
- optional compatibility profiles only when explicitly configured.
```

## Relationship to XSD precedence

This premise does not weaken the existing authority rule.

```text
Within the selected service version and dependency pool, validation follows the XSD.
PDF deviations are recorded as explanatory notes.
```

See also:

```text
docs/pdf_xsd_semantic_audit/VALIDATION_AUTHORITY.md
docs/pdf_xsd_semantic_audit/AUDIT_SCOPE_MATRIX.md
```