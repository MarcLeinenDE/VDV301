# Version-scope boundary review — CE-026 — 2026-10-08

Status: **verified / scope unchanged**.

Historical Common V1.0-V2.3 documentation uses `BeaconPoint.Description`, while the exact selected XSDs require the typo-like `BeaconPoint.Desciption`. The typo-like XSD name remains normative for those historical profiles and `Description` is not an alias.

The selected Common V2.4 candidate/integration XSD corrects BeaconPoint to `Description`, matching the V2.4 PDF. V2.4 is therefore an explicit non-affected correction boundary and must not be back-applied to historical validation.

Boundary: V1.0-V2.3 affected; V2.4 not affected.
