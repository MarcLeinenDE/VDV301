# COMMON V2.4 — Deep Read closure

Date: 2026-09-03
State: **closed / needs_visual_review**
Authority: **selected candidate/integration V2.4 family; not an official release tag**

## Frozen source basis

The immutable source-only observation set is `COMMON_V2.4_FRESH_2026-09-03.md`, frozen by commit `789f02f697809b1eef4d3b1a366a3599649a6d7d` before historical reconciliation. The official PDF is SHA-256 `01c233239d6d488dd814e3c9fc2a21841913298ef25442a21ab9208c4120452a`, 1,689,647 bytes, 63 pages. Run `33658306978` rendered all pages; all 63 page hashes were rechecked.

Selected executable schema family:

- Common blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4`
- Enumerations blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`
- bytes match branch `candidate/dms-v2.4-xsd` / open draft `VDVde/VDV301#31`
- no official `VDV-301-2.4` tag exists
- therefore candidate/integration authority is explicit and must not be relabelled official

## Historical reconciliation

| Frozen group | Finding identity | Decision |
|---|---|---|
| FR-COM24-001 | DRCOM20-001 | persists in selected candidate family |
| FR-COM24-002 | DRCOM22-001 | persists |
| FR-COM24-003 | CE-013 | persists |
| FR-COM24-004 | CE-011 | persists |
| FR-COM24-005 | DRCOM10-002 | persists |
| FR-COM24-006 | CE-014 / CE-012 / CE-018 / DRCOM10-003 | persists |
| FR-COM24-007 | DRCOM10-004 / DRCOM21-001 / CE-005 / CE-024 | persists |
| FR-COM24-008 | **DRCOM24-001** | **new unique finding** |
| FR-COM24-009 | CE-015 / CE-016 / CE-021 / CE-017 | persists; Beacon/ReplyPath older findings explicitly excluded |
| FR-COM24-010 | CE-022 / CE-019 | persists |
| FR-COM24-011 | DRCOM10-005 | persists |
| FR-COM24-012 | CE-006 / CE-004 | persists |
| FR-COM24-013 | CE-007 / CE-008 / CE-009 / CE-010 | persists; old DoorCounting mismatch fixed |
| FR-COM24-014 | CE-002 / DRCOM10-007 | history/cross-reference residue |
| FR-COM24-015 | DRCOM10-007 | grouped editorial residue |

## DRCOM24-001

PDF `LineInformation` documents `LineName` and `LineShortName` as `IBIS-IP.string`, `0:1`. The selected candidate XSD models both as `InternationalTextType`, `0:*`. The difference changes XML shape/type and repeatability.

EV-122 is executable confirmation: run `33716645876`, job `100527119224`, checker `tools/validate_common_v24_ev122.py`. Candidate InternationalText instances and repetition validate; the PDF-shaped value-only form does not.

## Scope corrections at V2.4

The Fresh Read actively prevents incorrect historical extension:

- `DRCOM23-001`: V2.4 adds `ArrivalExpected` and `DepartureExpected` to `StopInformationRequest`; PDF and candidate XSD align.
- `CE-025`: `ReplyPath` aligns in V2.4.
- `CE-026`: `BeaconPoint.Description` aligns in V2.4.
- `DRCOM10-006`: V2.4 DoorCounting uses `Wheelchair` / `Other`; the older lexeme mismatch is fixed.
- `CE-020`: remains a V2.3 official-vs-PR30 authority-collision identity, not a V2.4 finding.
- `CE-023`: remains V2.2-only.

## Historical note correction

`01g_common_enums_v2_4_datatypes_core_structures.md` contained a stale first-pass statement that V2.4 `InternationalTextType` used `IBIS-IP.string` / `IBIS-IP.language` in XSD. The exact selected blobs use `xs:string` / `xs:language`. The old statement is preserved only as historical provenance and superseded by the fresh freeze, EV-122, and `AUDIT_CORRECTION_DELTA_COMMON_V24_INTERNATIONALTEXT_AUTHORITY_2026-09-03.md`.

## Closure

- 15 frozen source-only observation groups reconciled.
- New unique finding: `DRCOM24-001`.
- EV-122 PASS.
- No XSD changed.
- Deep Read Pass 2 is frozen complete after this final planned unit.
- Next project phase: full legacy finding revalidation under the current Evidence Gate.
