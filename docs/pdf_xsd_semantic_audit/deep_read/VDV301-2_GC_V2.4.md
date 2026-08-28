# Deep Read - VDV 301-2 General Conventions V2.4

Status: textual fresh read completed from byte-pinned official source; visual page review attempted but screenshot backend returned cache-miss. Keep `needs_visual_review`.

## Source and authority

```text
document_id: VDV301-2_GC_V2.4
publication: VDV-Schrift 301-2, 01/2023, Allgemeine Konventionen / General conventions V2.4
official URL: https://www.vdv.de/301-2-sde-v2.4-common-conventions.pdfx
SHA-256: 048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d
size: 1767094 bytes
pin evidence run: 33179106915
```

The same evidence run re-executed the deterministic repository validation baseline successfully:

```text
50 root XSDs compile
39 XSD service profiles
84 direct include edges
EV-101..EV-106 and RV-001..RV-004 remain green
```

No XSD is changed by this Deep Read.

## 1. Method

Fresh read was performed independently of the previous General-Conventions audit and then compared with V2.2/V2.3 evidence.

Visual screenshot calls were attempted for relevant pages, including the device-class and version-history areas, but the PDF screenshot backend returned `cache miss`. Native PDF text is good enough for high-confidence text findings, but layout-sensitive closure is deliberately not promoted to `exhaustive_read`.

## 2. Intended V2.4 changes confirmed

The V2.4 version history lists only two technical/documentation changes:

```text
1. Missing entries in the German version of Table 3 were added.
2. Chapter 6 now explicitly says that XSD definitions take precedence over documentation in case of inconsistencies.
```

Both are visible in the document.

### 2.1 German DNS-SD TXT Table 3 completed

The German Table 3 now includes the previously missing train/device attributes, including:

```text
coachnumber
deviceclass
deviceID
```

This is a real V2.4 documentation correction relative to V2.3.

### 2.2 XSD precedence explicitly normative in V2.4

Chapter 6 states in German and English that XSD files should agree with the documentation and that, in case of inconsistency, the XSD definitions have precedence.

This directly supports the audit/tool authority model already used in this repository:

```text
selected exact XSD family/variant = executable XML validation authority
PDF discrepancy = contextual audit/provider note
```

It does not authorize silently changing an XSD.

### 2.3 V2.3 history numbering corrected

The V2.4 publication correctly prints:

```text
7.2 Version 2.3
7.2.1 Funktionale Erweiterungen / Functional Upgrade
7.2.2 Technische Ergänzungen/Korrekturen / Technical Upgrade/Corrections
```

Therefore `DR3012GC23-001` is resolved in the V2.4 publication.

## 3. Existing findings that persist in V2.4

### DISC-001 - German/English IP allocation conflict

German section 2.1.1 says there are no prescribed IP-address allocation rules and gives fixed IP/DHCP as best practice.

English section 2.1.1 still describes decentralized ZeroConf allocation using 169.254/16.

The same-document language conflict therefore persists.

### DR3012-001 - wrong RFC 2927 reference

English section 2.1.1 still cites RFC 2927 for automatic link-local address allocation. The bibliography uses RFC 3927 for IPv4 link-local addressing.

### DR3012-002 - SRV Weight semantics

The SRV table still says that, for equal conditions, the service with the lower weight is preferred. This remains inconsistent with the RFC 2782 weighted-selection semantics already documented in the audit.

### DR3012GC22-002 - duplicate German DNS-SD subsection number

German still numbers both:

```text
3.3.1 Nutzung des SRV-Records
3.3.1 Nutzung des TXT-Records
```

while English correctly uses 3.3.1 / 3.3.2.

### SUB-001 - `TerminateSubscribe*` table names

The operation-notation example still prints:

```text
UnsubscribeData Req.  TerminateSubscribeRequestStructure
                Resp. TerminateSubscribeResponseStructure
```

The executable Common family uses `UnsubscribeRequestStructure` / `UnsubscribeResponseStructure`.

### DR3012V21-001 - stale DeviceManagementService document number

The system-start text still points `DeviceManagementService` to `VDV 301-2-2`, although the separated DMS document is VDV 301-2-0 in this document family.

## 4. Regression of DR3012GC22-001

The literal Word cross-reference failure text:

```text
Fehler! Verweisquelle konnte nicht gefunden werden.
```

was present in General Conventions V2.2, absent in the fresh V2.3 read, and is present again at multiple V2.4 locations.

Observed V2.4 contexts include:

```text
device-class section
English device-class cross-reference
system-start principles
XML/table notation chapter
table-notation example references
```

Historical state:

```text
V2.2: present
V2.3: resolved / no literal placeholder found
V2.4: reintroduced
```

Handling: keep the same finding ID `DR3012GC22-001` and record V2.4 as a regression/reintroduction rather than opening a duplicate finding.

## 5. New Deep Read findings

### DR3012GC24-001 - German `OnBordUnit` vs XSD/English `OnBoardUnit`

Classification:

```text
pdf_xsd_enum_spelling_mismatch_candidate
confidence: very high
version scope checked: V2.2-V2.4 General Conventions
```

German device-class Table 1 says that these terms are used as XML enumeration values, but prints:

```text
OnBordUnit
```

The English table prints:

```text
OnBoardUnit
```

Exact Enumerations V2.2 and Enumerations V2.4 XSDs both define:

```xml
<xs:enumeration value="OnBoardUnit"/>
```

The German glossary also retains `OnBordUnit`.

Impact:

```text
A provider copying the German spelling as an XML DeviceClass value will fail exact XSD validation.
Do not create an OnBordUnit alias.
Validation follows OnBoardUnit.
```

### DR3012GC24-002 - German subnet/gateway subsection numbered 2.1.1

Classification: `pdf_label_or_heading_error_candidate`.

Checked V2.2, V2.3 and V2.4 German publications all use:

```text
2.1.1 IP-Adressen
2.1.1 Subnetzmasken/Gateways
```

The English text correctly uses:

```text
2.1.1 IP Addresses
2.1.2 Subnet Masks/Gateways
```

Impact: documentation navigation only.

### DR3012GC24-003 - English version-character list duplicates `2`

Classification: `minor_pdf_editorial_duplicate_candidate`.

Checked English V2.2-V2.4 text prints the allowed version characters as:

```text
'0','1','2','2','3','4','5','6','7','8','9' or '.'
```

The German list contains the expected single occurrence of each digit.

Impact: none on actual service-version routing; the duplication does not add a new character. Keep as an editorial completeness finding.

### DR3012GC24-004 - misspelled technical service identifiers in examples/glossary

Classification: `pdf_example_terminology_mismatch_candidate`.

Checked V2.2-V2.4 system-start/DNS-SD examples contain typo-like service identifiers such as:

```text
DeviceManagmenService
CustomumerInformationService
DeviceManagmentServices
```

The glossary additionally uses:

```text
PassengerCountigService
```

Correct surrounding names and XSD/service identifiers are `DeviceManagementService`, `CustomerInformationService` and `PassengerCountingService`.

Impact:

```text
These strings occur in technical discovery/system-start contexts and must not be synthesized as alternate service names or DNS-SD identities by the SDK/tool.
```

### DR3012GC24-005 - no common IBIS-IP version vs `Version 1.0 of IBIS-IP`

Classification: `pdf_internal_version_terminology_inconsistency_candidate`.

Section 1.5 explicitly states that every IBIS-IP service is versioned independently and therefore there is no common IBIS-IP version.

Section 2.5 nevertheless says, in both languages, that protocols beyond the discussed set are not considered by `Version 1.0 of IBIS-IP`.

The wording persists in checked V2.2-V2.4 publications.

Impact:

```text
Do not infer a global/umbrella IBIS-IP schema version from this sentence.
Version routing remains service-specific as defined by section 1.5 and the exact schema/profile manifest.
```

## 6. Minor editorial residue not split into separate findings

The document contains additional ordinary language/typing defects, for example `Standarad`, `PassengerCountigService` and several grammatical errors. Technical identifier errors are covered by DR3012GC24-004; ordinary prose typos are not multiplied into separate finding IDs unless they affect routing, validation or interpretation.

## 7. V2.4 result

```text
textual fresh read: complete
byte-pinned source: yes
visual screenshot review: attempted, cache-miss
state: needs_visual_review
new Deep Read findings: DR3012GC24-001 .. DR3012GC24-005
reintroduced existing finding: DR3012GC22-001
strengthened existing findings: DISC-001, DR3012-001, DR3012-002, DR3012GC22-002, SUB-001, DR3012V21-001
resolved in this publication: DR3012GC23-001
XSD changes: none
```

## 8. Tool / SDK consequences

```text
- Continue exact service/version/authority routing.
- `OnBordUnit` must not be normalized or accepted as an alias for `OnBoardUnit`.
- Misspelled service identifiers from prose/examples must not become discovery aliases.
- Do not derive a global IBIS-IP version from the stale 2.5 wording.
- XSD precedence is now expressly stated by General Conventions V2.4 itself.
```
