# Source-locator review — DMS-004 — 2026-10-06

Status: **complete / visible-body verified / version-specific required fields confirmed**.

DMS-004 is not a defect in the historical profiles. InstallUpdate field requirements are version-specific.

- V2.1 and V2.2: UpdateID, UpdateTimestamp and UpdateURL are required; checksum and size are optional.
- V2.4: all five fields are documented as optional. The repository V2.4 XSD is candidate/integration authority and also permits an empty request.

Visible sources:
- V2.1 official PDF, printed page 107: three core fields 1:1; checksum/size 0:1.
- V2.2 official PDF, printed page 26: same model.
- V2.4 official PDF, printed page 25: all five fields 0:1.

Exact XSDs:
- V2.1 blob 191b43e01cdaba14b247725689a913c244a67eed, lines 296-314.
- V2.2 blob c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d, lines 247-265.
- V2.4 candidate/integration blob d222dfd98b2be3777576388da7ace8f333d24c3f, lines 247-265.

EV-127 confirms omission of each required V2.1/V2.2 core field is rejected, while the V2.4 candidate/integration profile accepts an empty request.

Consequence: validate against the exact selected version. Never back-apply V2.4 optionality to V2.1/V2.2 and never relabel the V2.4 candidate/integration XSD as official.
