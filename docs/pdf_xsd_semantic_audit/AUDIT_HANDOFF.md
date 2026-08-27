# PDF/XSD semantic audit handoff

Status: living handoff for continuing the VDV301 PDF/XSD audit in a new chat.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

Important branch policy:

```text
This is the superbranch / integration working branch.
Do not open this branch as an upstream PR against VDVde/VDV301.
Do not label its full content as an official VDV release.
Official PR work remains separate; currently DMS V2.4 PR #31 is the clean official-facing draft PR path.
```

## How a new chat should resume

At the start of a new chat, read these files first, in this order:

```text
docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF.md
docs/pdf_xsd_semantic_audit/00_index.md
docs/pdf_xsd_semantic_audit/VALIDATION_AUTHORITY.md
docs/pdf_xsd_semantic_audit/findings.md
docs/pdf_xsd_semantic_audit/validation_backlog.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.md
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_vs_xsd_diff.csv
docs/pdf_xsd_semantic_audit/generated/common_v2_4_datatypes_xsd_inventory.md
docs/pdf_xsd_semantic_audit/generated/common_v2_4_datatypes_xsd_inventory.csv
```

Then read the currently active detailed audit files:

```text
docs/pdf_xsd_semantic_audit/01_common_enums_v2_1_to_v2_4.md
docs/pdf_xsd_semantic_audit/01a_common_enums_v2_4_table_check.md
docs/pdf_xsd_semantic_audit/01b_common_enums_v2_4_continuation.md
docs/pdf_xsd_semantic_audit/01c_common_enums_additional_text_message_history.md
docs/pdf_xsd_semantic_audit/01d_common_enums_v2_4_enumeration_first_pass.md
docs/pdf_xsd_semantic_audit/01e_common_enums_v2_4_enumeration_second_pass.md
docs/pdf_xsd_semantic_audit/01f_common_enums_v2_4_pdf_vs_xsd_enum_diff.md
docs/pdf_xsd_semantic_audit/01g_common_enums_v2_4_datatypes_core_structures.md
docs/pdf_xsd_semantic_audit/01h_common_enums_v2_4_core_data_structures.md
docs/pdf_xsd_semantic_audit/01i_common_enums_v2_4_remaining_data_structures_part1.md
docs/pdf_xsd_semantic_audit/01j_common_enums_v2_4_remaining_data_structures_part2.md
```

Also read the broader branch context when needed:

```text
docs/superbranch_status.md
docs/schriften_coverage_audit_v0_1.md
```

Before writing anything, fetch the current branch ref:

```text
refs/heads/dev/schema-integration
```

Use the returned commit SHA as the current base. Do not rely on a remembered SHA if the branch has moved.

## Current audit objective

Long-term objective:

```text
Complete PDF-vs-XSD semantic comparison for all public VDV301 writings / schema-relevant versions V1.0 through V2.4.
```

Current block:

```text
Common Structures / Enumerations, especially VDV 301-2-1 V2.4.
```

Current method:

```text
1. Treat PDF tables/version histories as the documentation side.
2. Treat XSD files in dev/schema-integration as the schema side.
3. Record exact evidence and classify each result.
4. Do not correct XSDs during audit unless the user explicitly approves a separate correction branch/PR.
5. Keep candidate/PR/fork provenance visible.
```

## Validation authority

VDV 301-2 V2.4 General Conventions state that XML contents can be validated using XSD and that VDV provides the XSD files for the specified services. They also state that, in case of inconsistencies, the XSD definitions take precedence over the documentation.

Tool and audit implication:

```text
Validation follows XSD.
PDF differences are shown as explanatory notes, not as executable validation authority.
```

Example:

```text
FAIL for `Valid` if XSD requires `valid`.
Provider-facing note: PDF lists `Valid`, but XSD has precedence; therefore validation fails.
```

See:

```text
docs/pdf_xsd_semantic_audit/VALIDATION_AUTHORITY.md
```

Finding states:

```text
OK
OK with note
Mismatch
Unclear
Not checked yet
Confirmed historical mismatch
Confirmed PDF/XSD value discrepancy
```

## Established findings so far

```text
CE-001: No separate IBIS-IP_Enumerations_V2.3.xsd in branch; common V2.3 includes Enumerations V2.2. State unclear.
CE-002: V2.4 version history says StopPointNumber but table/XSD use PointNumber. OK with note; do not rename.
CE-003: V2.4 common/enums mostly promising but not fully closed.
CE-004: ServiceNameEnumeration V2.4: PDF table still shows SystemDocumentationService/SystemManagementService, but version history says removed and XSD omits them. Confirmed discrepancy; likely PDF table inconsistency.
CE-005: TripInformation AdditionalTextMessage cardinality mismatch across V2.0-V2.4. PDF/history says 0:* / maxOccurs unbounded; XSD permits only 0:1 per named field. Confirmed historical mismatch; do not auto-correct.
CE-006: DeviceStateEnumeration XSD contains warning, not listed in V2.4 PDF table. Confirmed discrepancy.
CE-007: Case-sensitive enum value mismatches: PDF Other/Valid/Air vs XSD other/valid/air. Confirmed discrepancy.
CE-008: Submode case differences: Funicular/Taxi Unknown/Undefined/minicab vs XSD unknown/undefined/miniCab. Confirmed discrepancy.
CE-009: RailSubmodeEnumeration PDF specialRail vs XSD specialTrain. Confirmed discrepancy.
CE-010: AirSubmodeEnumeration XSD-only canalBarge. Confirmed discrepancy.
CE-011: Connection TransportMode/ConnectionMode cardinality PDF 0:* vs XSD 0:1. Confirmed discrepancy candidate.
CE-012: DeviceSpecificationWithStateList cardinality PDF 1:* vs XSD 0:*. Confirmed discrepancy candidate.
CE-013: AdditionalAnnouncement third choice PDF InformationAtSpecificPoint vs XSD SpecificPoint, plus optional XSD choice. Confirmed discrepancy candidate.
CE-014: DataVersionList cardinality PDF 1:* vs XSD 0:*. Confirmed discrepancy candidate.
CE-015: FareZoneInformation PDF extraction casing Farezone* vs XSD FareZone*. Visual PDF confirmation required.
CE-016: GlobalCardStatusID vs XSD GlobalCardStausID spelling difference. Confirmed discrepancy candidate.
CE-017: TSPPoint Desciption spelling candidate. XSD observation confirmed; PDF visual confirmation required.
```

The authoritative text for these findings is `findings.md`.

## Machine inventory files

Exporter:

```text
tools/export_xsd_enumerations.py
```

Generated XSD enumeration inventory:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_xsd_inventory.md
```

Generated PDF enumeration inventory and diff:

```text
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_inventory.csv
docs/pdf_xsd_semantic_audit/generated/enumerations_v2_4_pdf_vs_xsd_diff.csv
docs/pdf_xsd_semantic_audit/01f_common_enums_v2_4_pdf_vs_xsd_enum_diff.md
```

Generated XSD datatype inventory:

```text
docs/pdf_xsd_semantic_audit/generated/common_v2_4_datatypes_xsd_inventory.csv
docs/pdf_xsd_semantic_audit/generated/common_v2_4_datatypes_xsd_inventory.md
```

## Current result of 01g

```text
- All 16 observed IBIS-IP wrapper datatypes in IBIS-IP_common_V2.4.xsd follow the expected Value + optional ErrorCode pattern.
- InternationalTextType is still OK against the PDF-described structure.
- NetexMode structure is still OK partial; value-level differences are tracked in CE-008 to CE-010.
```

## Current result of 01h

```text
Core V2.4 common structures checked in first pass:
Connection
DeviceInformation / DeviceSpecification family
DisplayContent
LineInformation
StopInformation / StopInformationRequest
TripInformation

New findings:
CE-011 Connection TransportMode/ConnectionMode PDF 0:* vs XSD 0:1.
CE-012 DeviceSpecificationWithStateList PDF 1:* vs XSD 0:*.

No new mismatch found for DisplayContent, LineInformation V2.4 additions, StopInformation V2.4 additions or TripInformation V2.4 additions beyond CE-005.
```

## Current result of 01i

```text
Remaining V2.4 common structures part 1 checked:
AdditionalAnnouncement
Announcement
BayArea
BeaconPoint
CardApplInformation
CardTicketData
DataAcceptedResponse
DataAcceptedResponseData
DataVersion
DataVersionList
Destination
DoorCounting / DoorCountingList / DoorInformation
DoorOpenState / DoorOperationState / DoorState
FareZoneInformation
GlobalCardStatus
GNSSPoint

New findings:
CE-013 AdditionalAnnouncement PDF choice InformationAtSpecificPoint vs XSD SpecificPoint, and choice cardinality note.
CE-014 DataVersionList PDF 1:* vs XSD 0:*.
CE-015 FareZoneInformation casing difference needs visual confirmation.
CE-016 GlobalCardStatusID vs XSD GlobalCardStausID.
```

## Current result of 01j

```text
Remaining V2.4 common structures part 2 checked:
GNSSCoordinate
JourneyStopInformation checked core fields
Point / PointType checked core shape
SpecificPoint
StopSequence
TimingPoint
ViaPoint
ZoneType with casing note

New finding:
CE-017 TSPPoint Desciption spelling candidate.

Deferred scope resolution in validation_backlog.md:
NetworkLocationPoint
OperationalInformation
PassengerCounting
PassengerCountingData
PathDestination
Route
```

## Next recommended task

Create a Common/Enums V2.4 structure closure pass:

```text
01k_common_enums_v2_4_structure_closure.md

Tasks:
- resolve deferred structure names from SB-005,
- visually confirm CE-015 and CE-017 from the PDF,
- classify all Common/Enums V2.4 structure tables as closed / partial / pending,
- then decide whether to move next to Common/Enums V2.3 history or DMS V2.4 audit integration.
```

Use the same evidence style:

```text
PDF table expectation
XSD observation
finding classification
validation follows XSD
PDF discrepancy becomes provider-facing note
no schema changes during audit
```

## Working style for continuity

After each meaningful block:

```text
1. Commit audit file changes to dev/schema-integration.
2. Update findings.md if a new CE finding is opened or a finding state changes.
3. Update AUDIT_HANDOFF.md only when the continuation point changes materially.
4. Report the final branch commit SHA to the user.
```

This avoids depending on chat memory alone and lets a new chat continue without gaps.
