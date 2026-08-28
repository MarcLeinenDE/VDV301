# VDV 301-2 Basisdienste V2.0 - Deep Read Pass 2

Status: textual fresh read complete; exact release/XSD and previous-audit comparison complete; visual closure pending.

Document ID: `VDV301-2_BASE_V2.0`

Official publication:

```text
VDV-Schrift 301-2
Version 2.0
02/2018
Basisdienste / Base Services
DeviceManagementService
SystemManagementService
SystemDocumentationService
```

Official PDF:

```text
https://www.vdv.de/301-2-sds-v-2-0.pdfx?forced=false
```

## 1. Method and source quality

This pass followed `DEEP_READ_METHOD.md`:

1. read the original VDV PDF afresh before consulting the old semantic audit,
2. scan the full native text layer across protocol conventions, DNS-SD, HTTP/UDP, operation notation, DMS, SystemDocumentation, SystemManagement, version history and glossary,
3. attempt visual PDF page confirmation,
4. compare against exact official release-tag XSDs and external standards where the VDV text depends on them,
5. only then compare the findings against the existing first-pass audit.

The native text layer is usable but contains normal bilingual table line-wrap artefacts and the literal unresolved Word-reference strings present in the publication itself.

Requested visual page screenshots returned cache-miss/internal retrieval errors. Therefore layout-sensitive findings are retained as `needs_visual_review`; this document is not labelled `exhaustive_read`.

No dedicated independent OCR source was used as authority.

## 2. Exact official V2.0 release family

A complete XSD inventory of official upstream tag `VDV-301-2.0` was compared against the operational superbranch.

Relevant Base-Service routing is deliberately mixed-version:

```text
DeviceManagementService V2.0
  -> IBIS-IP_common_V2.0.xsd
  -> IBIS-IP_Enumerations_V2.0.xsd

SystemDocumentationService V2.0
  -> IBIS-IP_common_V2.0.xsd
  -> IBIS-IP_Enumerations_V2.0.xsd

SystemManagementService V1.0
  -> IBIS-IP_common_V1.0.xsd
  -> IBIS-IP_Enumerations_V1.0.xsd
```

This is direct historical evidence that a V2.0 document context does not imply that every service XSD is V2.0.

### Superbranch gap found during fresh read

The official tag contains:

```text
IBIS-IP_SystemDocumentationService_V2.0.xsd
Git blob: ab959dddbfa2b8ca420af1b079501f94cff38051
```

The superbranch had lacked that exact official XSD. It was backfilled byte-identically under the existing official-release backfill policy.

After that backfill, all XSD paths from official tag `VDV-301-2.0` are represented in the deduplicated operational superbranch, subject to the already documented V1.0 packaging/dedup rules.

Current stored root count is therefore 50. The last actually executed full-root compilation baseline remains 49; no 50/50 compile claim is made in this block.

## 3. New fresh-read findings

### DR3012V20-001 - bilingual RFC 3927 / RFC 2927 conflict

The German ZeroConf/link-local paragraph uses RFC 3927 for the `169.254.x.x` range.

The English translation of the same passage still cites RFC 2927.

The bibliography lists RFC 3927.

External standard cross-check:

```text
RFC 3927 -> Dynamic Configuration of IPv4 Link-Local Addresses
RFC 2927 -> MIME Directory Profile for LDAP Schema
```

Classification:

```text
external_standard_reference_error_candidate
confidence: high
validation impact: documentation/runtime explanation only
```

This strengthens `DR3012-001` and the existing discovery reference finding rather than changing runtime authority silently.

### DR3012V20-002 - SRV Weight semantics still inverted

Both language versions retain the explanation that, at equal priority, the service with the lower weight is preferred.

RFC 2782 instead defines weighted proportional selection; larger positive weights receive proportionally higher selection probability.

Classification:

```text
external_standard_semantics_error_candidate
confidence: high
validation impact: discovery explanation only
```

This extends `DR3012-002` into V2.0.

### DR3012V20-003 - Heartbeat rename claimed in history but stale in tables

The V2.0 history states that the spelling was corrected to:

```text
HeartbeatInterval
```

The actual SystemDocumentation tables still print:

```text
HertbeatIntervall
```

The exact official V2.0 XSD uses:

```xml
<xs:element name="HeartbeatInterval" type="IBIS-IP.duration" minOccurs="0"/>
```

in both `SystemConfigurationData` and `StoreSystemConfigurationRequestStructure`.

Classification:

```text
pdf_version_history_or_documentation_error_candidate
confidence: high
```

Executable rule:

```text
Use HeartbeatInterval from the exact V2.0 XSD.
Do not create HertbeatIntervall or HeartbeatIntervall aliases.
```

This also shows the V1.0 issue evolved: V2.0 fixes the executable name/type, while the table text remained stale.

### DR3012V20-004 - `SystemDocumenationService` typo

Narrative text contains the misspelled service name `SystemDocumenationService`, whereas the heading, operation table and official schema use `SystemDocumentationService`.

Classification: `minor_pdf_editorial_typo_candidate`.

### DR3012V20-005 - unresolved SystemManagement chapter range

The SystemManagement introductory task description contains an unresolved chapter-range reference (`Kapitel bis` / `capitel bis`).

Classification: `pdf_cross_reference_error_candidate`.

### DR3012V20-006 - missing SubscribeDeviceInformation subsection heading

The DMS operation inventory includes `SubscribeDeviceInformation`, but the detailed subsection sequence jumps from `GetDeviceInformation` to `UnsubscribeDeviceInformation`. The surrounding text still explains subscription use of the generic VDV 301-2-1 structures.

Classification: `pdf_label_or_heading_error_candidate`.

SDK consequence: operation support must not be inferred solely from the presence of a dedicated PDF subsection heading.

### DR3012V20-007 - GetDeviceConfiguration described as setter

The `GetDeviceConfiguration` description says that the operation enables setting the variable device parameter. The following `SetDeviceConfiguration` operation is the actual setter.

Classification: `pdf_table_or_documentation_error_candidate`.

No operation semantics are inverted in the SDK because of this prose error.

### DR3012V20-008 - GetDeviceInformation response labelled request

The response table describes `GetDeviceInformationResponseStructure` / response data as a request structure.

Classification: `pdf_label_or_heading_error_candidate`.

Validation impact: none.

## 4. Existing findings strengthened or deliberately not duplicated

### DR3012-005

The V2.0 operation table uses:

```text
GetServiceStatus
SubscribeServiceStatus
UnsubscribeServiceStatus
```

while detailed headings still use `GetSystemStatus`, `SubscribeSystemStatus`, `UnsubscribeSystemStatus`.

The exact official SystemManagement V1.0 schema uses `ServiceStatus` names. Therefore the existing terminology finding persists into V2.0. No `SystemStatus` aliases are created.

### SUB-001

The V2.0 notation table still maps `UnsubscribeData` to:

```text
TerminateSubscribeRequestStructure
TerminateSubscribeResponseStructure
```

where Common V2.0 provides `UnsubscribeRequestStructure` / `UnsubscribeResponseStructure`.

The historical span of `SUB-001` therefore includes V1.0 and V2.0, as well as the later already checked General Conventions publications.

### SUB-002

SystemDocumentation V2.0 and SystemManagement V1.0 add further evidence that documented generic subscription operations need not appear as equivalent service-prefixed entries in the local service operation group.

Resolver/SDK rule remains:

```text
Do not derive complete operation support solely from service-XSD group membership.
Use the separate version-sharp operation manifest.
```

### DMS-001 / DMS-002 / DMS-003

Fresh read reconfirms the existing DMS findings:

```text
DMS-001:
  documented V2.0 operation inventory exceeds local service-XSD group/global modelling.

DMS-002:
  repeated literal unresolved Word-reference text is present in the V2.0 publication.

DMS-003:
  ErrorMessage 10:* is genuinely PDF/XSD-aligned in V2.0.
  Official DMS V2.0 XSD uses minOccurs="10" maxOccurs="unbounded".
```

No duplicate finding is opened for those points.

## 5. Deep-read conclusion for V2.0

The second pass materially improved the project state:

1. it found and repaired a historical official-XSD storage omission without changing schema content,
2. it proved another mixed-version release family,
3. it exposed a bilingual standards-reference conflict,
4. it exposed a version-history/table/XSD contradiction around `HeartbeatInterval`,
5. it extended existing historical findings without multiplying duplicate IDs,
6. it rejected the tempting but wrong assumption that unusual `ErrorMessage 10:*` must itself be a PDF/XSD mismatch.

Status:

```text
textual fresh read: complete
exact release/XSD cross-check: complete
old-audit comparison: complete
visual page closure: pending
deep_read_state: needs_visual_review
```

## 6. Next document

```text
VDV301-2_BASE_V2.1
```

Primary delta checks:

```text
- whether the bilingual RFC 3927/2927 conflict is corrected,
- whether SRV Weight wording is corrected,
- whether HeartbeatInterval is consistently corrected,
- whether ServiceStatus/SystemStatus headings are corrected,
- whether DMS broken Word references / missing headings are repaired,
- complete official VDV-301-2.1 tag inventory vs superbranch.
```
