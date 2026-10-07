# Version-scope boundary review — BG-001 — 2026-10-07

Status: **verified with material scope correction**.

## Boundary result
The previous scope ended too early at VDV-301-2.0. Full official release-tag revalidation shows that the same V1.0 path/token remains release-context-sensitive through later official releases for surviving files.

Per-file last official contexts:
- PassengerCountingService V1.0: **2.0**
- SystemManagementService V1.0: **2.1**
- JourneyInformationService V1.0: **2.3**
- TicketInformationService V1.0: **2.3**

`VDV-301-2.3` is the latest official GitHub release. Current `master` is integration state and is not promoted into official scope.

## Authority consequence
Historical validation must select the exact release-tag schema pool. A V1.0 filename/version token alone is insufficient whenever multiple official release contexts contain that path with different bytes.

Selected XSD bytes remain Source of Truth for executable XML conformance. No byte substitution, normalization or waiver is introduced.
