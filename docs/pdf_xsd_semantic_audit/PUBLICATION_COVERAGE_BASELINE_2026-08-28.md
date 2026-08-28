# VDV301 public PDF coverage baseline

Date: 2026-08-28
Status: semantic first-pass coverage complete

Canonical public list source:

```text
https://www.vdv.de/ip-kom-oev.aspx
section: VDV 301 Systemarchitektur / Dienste / Netzwerkinfrastruktur
```

Purpose: keep three different progress metrics separate. Do not report one percentage as if it meant all three.

## Denominator

Current VDV public page lists 50 physical PDF links in the VDV301 section.

Two pairs are separate DE/EN files for the same semantic publication/version content:

```text
VDV 301-1 System architecture: DE + EN = 2 physical PDFs / 1 semantic unit
VDV 301-2 V1.0 interface/base services: DE + EN = 2 physical PDFs / 1 semantic unit
```

Therefore:

```text
physical PDF links: 50
semantic publication/version units: 48
```

The English VDV 301-1 file explicitly states that it is a convenience translation of the German V1.0/01-2014 document and that the German original applies in case of inconsistency. It is therefore not counted as a second normative semantic version.

## Metric A - semantic PDF first-pass coverage

Current status after the dedicated VDV 301-1 architecture block:

```text
48 / 48 semantic publication/version units covered by the audit first pass
= 100 %
```

`First-pass covered` means the document/version has been read for audit-relevant semantics, version history, service/protocol model, relevant tables and PDF/XSD/protocol differences. It does NOT mean every page and every sentence has been independently marked as exhaustively reviewed.

VDV 301-1 closure:

```text
docs/pdf_xsd_semantic_audit/28_vdv301_1_system_architecture_first_pass.md
```

## Metric B - PDF <-> executable XSD comparison coverage

Not every VDV301 PDF has a dedicated/exact XSD by design or by available provenance.

Current semantic publication units without a direct exact XSD comparison lane include:

```text
VDV 301-1 System architecture                       architecture document
CustomerInformationService V1.1                    exact XSD unresolved
TimeService V1.0                                   intentionally protocol/discovery, no service XSD
VideoLiveService V1.0                              exact service XSD unresolved
VideoRecordingService V1.0                         exact service XSD unresolved
VideoDisplayService V1.0                           exact service XSD unresolved
HTMLDisplayService V2.1                            intentionally discovery/HTTP, no service XSD
HTMLDisplayService V2.2                            intentionally discovery/HTTP, no service XSD
HTMLDisplayService V2.2a                           intentionally discovery/HTTP, no service XSD
VDV 301-3 Network infrastructure                    network/protocol document, not service XSD
```

Thus the current public set contains:

```text
38 semantic publication/version units with a selected executable XSD comparison lane
10 semantic units without a direct exact service-XSD lane
```

All 38 currently pairable semantic units have received at least a PDF/XSD first-pass comparison:

```text
PDF/XSD first-pass coverage of pairable semantic units: 38 / 38 = 100 %
PDF/XSD pairable units as share of all semantic PDFs:     38 / 48 = 79.2 %
```

The 10 non-pairable units are not automatically `audit missing`:

```text
- some are non-XSD by design;
- some are architecture/network documents;
- four service-version cases have unresolved exact-XSD provenance.
```

Candidate/integration XSDs count as executable comparison lanes only when they are explicitly labelled candidate/integration; they are never upgraded to official authority by this percentage.

## Metric C - exhaustive page-by-page deep-read coverage

Status: not previously measured with a defensible denominator.

Do NOT infer 100 % here.

The historical audit used `first pass completed` as the service/document completion marker. Some high-value documents, especially Common/Enumerations, General Conventions and finding-heavy service structures, received deeper table-level review, while other service documents received a targeted semantic first pass.

Tracking rule going forward:

```text
not_started
  no meaningful document review yet

targeted_first_pass
  architecture/service/version/protocol semantics and audit-relevant tables checked

table_level_deep_pass
  systematic table/structure-level comparison performed

exhaustive_read
  complete page/table/figure review explicitly tracked and closed
```

Current honest statement:

```text
Semantic first-pass PDF coverage:                100 %
Pairable PDF/XSD first-pass coverage:             100 %
Exhaustive all-pages/all-tables reading coverage: not yet defensibly quantified
```

The next optional document-work phase is therefore not `finish unread VDV301 PDFs`; it is a second-pass/deep-read phase targeted by risk and audit value.

## Scope group inventory

| Public area | Physical PDFs | Semantic units | First-pass state | XSD lane |
|---|---:|---:|---|---|
| VDV 301-1 System architecture DE/EN | 2 | 1 | covered | architecture / no direct service XSD |
| VDV 301-2 V1.0 interface/base services DE/EN | 2 | 1 | covered | legacy aggregate/service XSD routing |
| Base Services V2.0/V2.1 | 2 | 2 | covered | executable XSD families |
| General Conventions V2.2/V2.3/V2.4 | 3 | 3 | covered | common/service/protocol authority mapping |
| DeviceManagementService | 2 | 2 | covered | official/candidate routes as versioned |
| Common Data Structures + Enumerations | 6 | 6 | covered, deep table work performed | executable XSD |
| BeaconLocationService | 1 | 1 | covered | executable XSD |
| CustomerInformationService | 4 | 4 | covered | V1.1 unresolved; later executable |
| DistanceLocationService | 1 | 1 | covered | executable XSD |
| GNSSLocationService | 1 | 1 | covered | executable XSD |
| JourneyInformationService | 1 | 1 | covered | executable XSD |
| NetworkLocationService | 1 | 1 | covered | executable XSD |
| PassengerCountingService | 2 | 2 | covered | executable XSD |
| TicketingService | 1 | 1 | covered | executable XSD + alias/provenance note |
| TimeService | 1 | 1 | covered | non-XSD protocol/discovery profile |
| VideoLiveService | 2 | 2 | covered | V1.0 unresolved; V2.0 executable |
| VideoRecordingService | 3 | 3 | covered | V1.0 unresolved; V2.0 official; V2.4 candidate |
| VideoDisplayService | 2 | 2 | covered | V1.0 unresolved; V2.0 executable |
| TrainSet service document | 2 | 2 | covered | executable versioned service families |
| DoorStateService | 1 | 1 | covered | executable XSD |
| TicketValidationService | 4 | 4 | covered | official/integration/candidate routing as audited |
| HTMLDisplayService | 3 | 3 | covered | non-XSD discovery/HTTP profiles |
| SystemMonitoringService | 1 | 1 | covered | executable XSD |
| AnalogRadioService | 1 | 1 | covered | candidate executable XSD |
| VDV 301-3 Network infrastructure | 1 | 1 | covered | network/protocol profile |
| **Total** | **50** | **48** | **48 covered / 0 pending** | **38 direct executable-XSD semantic units** |
