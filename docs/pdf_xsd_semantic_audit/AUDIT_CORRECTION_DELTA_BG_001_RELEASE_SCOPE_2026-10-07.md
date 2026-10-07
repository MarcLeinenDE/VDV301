# Audit correction delta — BG-001 official release-context scope — 2026-10-07

Status: **material scope correction; finding identity preserved**.

## Previous scope
BG-001 previously named only the contrast between `VDV-301-1.0` and `VDV-301-2.0` for four same-path V1.0 service schemas.

That was sufficient to prove the routing problem exists, but it did not prove where the same release-context ambiguity ends.

## Fresh official release matrix
Exact upstream root entries were rechecked for all official GitHub releases through the current latest official release `VDV-301-2.3`.

| path | 1.0 | 2.0 | 2.1 | 2.2 | 2.3 |
| --- | --- | --- | --- | --- | --- |
| JourneyInformationService V1.0 | 1ee4d7ae… | 8c303db5… | 8c303db5… | 8c303db5… | 8c303db5… |
| PassengerCountingService V1.0 | 600a3ee6… | 4161872b… | absent | absent | absent |
| SystemManagementService V1.0 | 85390f99… | 2d32630a… | 2d32630a… | absent | absent |
| TicketInformationService V1.0 | 017ca646… | 3fda66d8… | 3fda66d8… | 3fda66d8… | 3fda66d8… |

Thus:
- all four paths change between release contexts 1.0 and 2.0;
- PCS V1.0's affected same-path lineage ends at 2.0;
- SystemManagement V1.0 persists through 2.1;
- JIS and TicketInformation V1.0 persist unchanged through 2.3.

The current upstream `master` still contains JIS and TicketInformation with the same 2.0 blobs, but master is not an official release and is excluded from official runtime scope.

## Correction
BG-001 keeps its identity and classification, but affected release-context scope is expanded to explicit official lanes:
- VDV-301-1.0
- VDV-301-2.0
- VDV-301-2.1
- VDV-301-2.2
- VDV-301-2.3

Semantic classification, source locator scope and runtime profile scope are updated together. Exact selected-XSD authority remains unchanged.

## No new defect claim
This correction does **not** claim that every byte difference changes payload validity. BG-001 remains a routing/provenance safeguard: the exact official release-tag schema pool must be selected reproducibly.
