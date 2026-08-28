# VDV 301-2 Allgemeine Konventionen V2.2 - Deep Read Pass 2

Status: textual fresh read complete; exact official release-tag/XSD inventory and previous-audit comparison complete; visual closure pending.

Document ID: `VDV301-2_GC_V2.2`

Official publication:

```text
VDV-Schrift 301-2
Version 2.2
08/2019
Allgemeine Konventionen / General conventions
```

Official PDF:

```text
https://www.vdv.de/301-2-sdes-v2-2-common-conventions.pdfx?forced=true
```

## 1. Method and source quality

The original VDV PDF was read afresh before the earlier General-Conventions/network/subscription audit was opened.

The full native text layer was checked across:

```text
publication structure and versioning model
IP addressing
DNS-SD SRV/TXT records
service identity and coexistence of service versions
HTTP/UDP operation conventions
system start
operation naming
subscription notation
XML/XSD rules
version history
German/English text tracks
```

Visual screenshot review was attempted on the actual PDF handle. The VDV PDF backend returned a cache/internal error for the requested pages, so layout-sensitive observations remain pending visual confirmation.

No dedicated independent OCR copy of this V2.2 General-Conventions document was found in the available File Library. Existing XSD aggregate documentation, SDK manifests and tool/test reports are not counted as OCR substitutes.

Result:

```text
deep_read_state: needs_visual_review
```

## 2. Structural change of the VDV 301-2 publication family

V2.2 explicitly explains that the former monolithic service specification had become too extensive and that individual services are now maintained as separate `VDV 301-2-x` documents.

The VDV 301-2 document itself becomes the technical-basics / General-Conventions publication.

This is important for the SDK resolver because document identity and service identity are no longer interchangeable.

The fresh read also states that:

```text
each IBIS-IP service is independently versioned;
there is no single common IBIS-IP service version;
multiple versions of one service may coexist;
clients and servers must ensure service-version compatibility;
service-document version corresponds to service version.
```

Functional service identity includes service name, service version, device class/type and device ID. Technical identity uses host/IP, service, port and optional path.

SDK consequence:

```text
DNS-SD service version is a resolver input.
Endpoint identity is not schema identity.
Multiple versions must remain independently routable.
Never apply latest-XSD-wins.
```

## 3. Exact official V2.2 release-tag inventory

Official upstream tag:

```text
VDV-301-2.2
commit/tree context: f283697124750d12189b960b302b399769bad530
```

The complete release-tag XSD inventory was compared with the operational superbranch.

No additional historical official XSD backfill is required.

The official tag already demonstrates a broad mixed-version service pool, including for example:

```text
CustomerInformationService V2.2
DeviceManagementService V2.2
DoorStateService V2.1
PassengerCountingService V2.1
SystemMonitoringService V2.2
TicketValidationService V2.2
TrainSet services V2.2
Video services V2.0
legacy V1.0 services
Common/Enumerations V1.0 through V2.2 as required by the contained services
```

SystemDocumentation and SystemManagement are no longer part of the V2.2 Base-Service document model; the version history records removal of SystemDocumentation and the renaming/separation of SystemManagement as SystemMonitoring.

Current stored root-XSD count remains 50. The last actually executed full-root compilation baseline remains 49; this Deep Read block does not claim 50/50 execution.

## 4. New V2.2-specific findings

### DR3012GC22-001 - unresolved Word cross references

The V2.2 General-Conventions publication contains repeated literal Word-generation placeholders equivalent to:

```text
Fehler! Verweisquelle konnte nicht gefunden werden.
```

They occur in several independent contexts, including device-class discussion, system start and XML/table-reference text.

The version history nevertheless lists no technical corrections for this release.

Classification:

```text
pdf_cross_reference_error_candidate
confidence: high
validation impact: none
```

SDK consequence:

```text
Do not derive machine routing or validation rules from unresolved printed cross references.
Preserve them only as documentation diagnostics.
```

### DR3012GC22-002 - German TXT subsection duplicates 3.3.1

The German V2.2 text numbers both DNS-SD subsections as:

```text
3.3.1 Nutzung des SRV-Records
3.3.1 Nutzung des TXT-Records
```

The German introductory references consequently point both SRV and TXT to section 3.3.1.

The English text correctly distinguishes:

```text
3.3.1 Use of SRV Records
3.3.2 Use of TXT Records
```

Classification:

```text
pdf_label_or_heading_error_candidate
confidence: high
validation impact: documentation navigation only
```

A minor duplicate-word typo (`Kapitel Kapitel 3.2`) was also observed in the German SRV context. It is retained as report-only editorial evidence and is not assigned a separate finding ID.

## 5. Existing findings strengthened by V2.2

### DISC-001 / DR3012-001 - German/English IP-allocation conflict becomes stronger

The German V2.2 text materially changes the rule and says in substance:

```text
There are no specifications for IP-address allocation.
Address ranges only need to be consistent between participants.
Fixed addresses or DHCP are described as a best-practice approach.
```

The English text in the same publication still says that decentralized address allocation uses part of ZeroConf, cites RFC 2927 and requires observing the `169.254.x.x` specifications for an interoperable network.

The bibliography lists RFC 3927.

This is therefore not merely a wrong RFC number: the two language tracks express materially different addressing requirements.

Handling remains:

```text
Do not enforce ZeroConf/169.254 as a universal VDV failure from the English text alone.
Do not silently declare one language version the corrected authority.
Expose the source conflict with version/language provenance.
```

### DR3012-002 - SRV Weight semantics still inverted

V2.2 retains wording that, at equal priority, prefers the service with the lower weight.

RFC 2782 defines weighted proportional selection instead; larger positive weights receive correspondingly greater selection probability.

This extends the historical evidence chain of `DR3012-002` into V2.2.

### SUB-001 - `TerminateSubscribe*` persists

The V2.2 operation-notation table still maps:

```text
UnsubscribeData request  -> TerminateSubscribeRequestStructure
UnsubscribeData response -> TerminateSubscribeResponseStructure
```

while the executable Common family uses:

```text
UnsubscribeRequestStructure
UnsubscribeResponseStructure
```

The affected-document history of `SUB-001` therefore explicitly includes:

```text
VDV 301-2 V1.0
Base Services V2.0
Base Services V2.1
General Conventions V2.2
and the already checked V2.3/V2.4 conventions
```

No executable `TerminateSubscribe*` aliases are introduced.

### DR3012V21-001 - stale DMS document reference persists

The V2.2 system-start text still points the DeviceManagementService to:

```text
VDV 301-2-2
```

although in the separated V2.2 document family DeviceManagementService is `VDV 301-2-0`, while `301-2-2` is BeaconLocationService.

The existing stale-reference finding is therefore extended into V2.2 rather than duplicated.

Several low-impact spelling errors also occur in the system-start example (`DeviceManagmenService`, `CustomumerInformationService`, `DeviceManagmentServices`). These are retained report-only.

## 6. DNS-SD TXT extension is a real V2.2 architecture change

The V2.2 TXT table documents the extended discovery profile, including:

```text
ver          mandatory for all IBIS-IP services
path         optional
multicast    mandatory for UDP services
sntp-server  mandatory for the time-synchronisation service
coachnumber  mandatory in a train-set IBIS-IP network
deviceclass  mandatory from IBIS-IP 2.2 onwards
deviceID     mandatory from IBIS-IP 2.2 onwards
```

The version history records extension of the DNS-SD TXT record.

Classification:

```text
ok_with_note / intentional V2.2 discovery-profile extension
```

This belongs to versioned discovery validation, not XSD validation.

## 7. HTTP and Content-Type authority

The fresh V2.2 read confirms the General-Conventions transport rule:

```text
operations passing data to a service use HTTP POST;
operations passing no data use HTTP GET;
Get operations use HTTP GET.
```

However, the full text search found no explicit V2.2 requirement using the literal terms:

```text
Content-Type
application/xml
text/xml
```

Therefore the existing SDK authority rule remains unchanged:

```text
Content-Type checks are useful and can be normative/derived from applicable HTTP/XML media-type standards,
but must not be falsely attributed as an explicit VDV 301-2 V2.2 sentence.
```

This preserves the project's `NORMATIVE` / `DERIVED` / `ROBUSTNESS` source separation.

## 8. Deliberate V2.2 service-model changes

The V2.2 history records, among other changes:

```text
DNS-SD TXT record extended
SystemDocumentation removed
SystemManagement renamed/separated as SystemMonitoring
DeviceManagement activation/deactivation control removed/simplified
new CombiDevice concept
system start simplified
```

The fresh text correspondingly says that currently only Restart is planned among the device-control operations in this General-Conventions model.

These are intentional version changes, not PDF/XSD mismatch findings by themselves.

## 9. XML/XSD authority language

V2.2 continues to describe interface objects as XML and explicitly refers to XML Schema validation.

Response modelling is described through the familiar alternative between normal response data and `OperationErrorMessage`.

This supports, but does not alter, the existing project rule:

```text
selected XSD -> executable XML structure authority
General Conventions/service documents -> protocol/operation semantics
external standards -> separately attributed lower-layer rules where applicable
```

## 10. Old-audit comparison

The earlier audit was opened only after the fresh read.

It already contained:

```text
DISC-001 German/English V2.2/V2.4 IP-allocation conflict
DISC-002 RFC 2927 reference problem
versioned DNS-SD TXT profile
no explicit Content-Type rule in the checked General Conventions
```

The prior subscription audit originally documented `SUB-001` explicitly for V2.3/V2.4. The fresh Deep Read proves the same table defect also exists in V2.2 and extends its historical chain accordingly.

The fresh pass additionally found two V2.2-specific issues that were not present in those earlier closure documents:

```text
DR3012GC22-001 repeated unresolved Word cross references
DR3012GC22-002 German duplicate TXT subsection number 3.3.1
```

## 11. Deep-read conclusion

```text
textual fresh read: complete
exact official VDV-301-2.2 tag inventory: complete
additional official XSD backfill required: no
old-audit comparison: complete
independent OCR: not found
visual page closure: pending after repeated VDV PDF cache error
deep_read_state: needs_visual_review
```

## 12. Next document

```text
VDV301-2_GC_V2.3
General Conventions V2.3
```

Fresh-read priorities:

```text
compare V2.2 -> V2.3 IP-address language by both language tracks
check whether German TXT 3.3.1 duplication is repaired
check unresolved Word references
check SRV Weight semantics
check SUB-001 TerminateSubscribe notation
check HTTP/1.1 change introduced in V2.3
check service-version/discovery semantics
inventory exact VDV-301-2.3 release/tag and authority status before old-audit comparison
```
