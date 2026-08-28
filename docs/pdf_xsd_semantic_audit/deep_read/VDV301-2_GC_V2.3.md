# VDV 301-2 Allgemeine Konventionen V2.3 - Deep Read Pass 2

Status: textual fresh read complete; exact source pin, release/authority cross-check and previous-audit comparison complete; visual closure pending because the PDF screenshot backend repeatedly returns cache-miss.

Document ID: `VDV301-2_GC_V2.3`

Official publication:

```text
VDV-Schrift 301-2
Version 2.3
02/2021
Allgemeine Konventionen / General conventions
```

Official PDF:

```text
https://www.vdv.de/301-2-sdes-v2-3-common-conventions.pdfx
```

Pinned source evidence:

```text
sha256: 4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603
size: 1057483 bytes
pin registry: audit_registry/pdf_source_pins_v0.1.json
pin evidence run: 33169314332
```

## 1. Method and source quality

The V2.3 publication was read afresh before the previous General-Conventions audit was used for comparison.

The native text layer was checked across the complete publication structure and the semantically relevant chapters, including:

```text
foreword / document-family model
minimum device requirements and device classes
service versioning and service-document identity
IP addressing and language-track differences
periodic vs event-triggered information
UDP / HTTP / SNTP / RTP boundaries
DNS-SD SRV and TXT records
HTTP / UDP publication profiles
HTTP GET / POST rules
operation naming conventions
Get / Subscribe / Unsubscribe and heartbeat semantics
service states and error handling
XML/XSD naming and table notation
functional and technical service identity
system-start sequence
version history
terms and external references
```

The official source is byte-pinned, but repeated screenshot attempts on the VDV PDF handle failed with `cache miss`. Therefore the source is reproducible but not visually closed in this runtime.

No independent OCR copy was used as a substitute for the original publication.

Result:

```text
textual_fresh_read_complete: true
original_pdf_visual_review: attempted_failed_cache_miss
preferred_reading_source: embedded_text_with_exact_source_pin_and_static_crosschecks; visual confirmation pending
deep_read_state: needs_visual_review
```

`exhaustive_read` is intentionally not assigned.

## 2. V2.3 document-family and resolver model

V2.3 retains the V2.2 architecture in which individual services are maintained as separate `VDV 301-2-x` documents and the General-Conventions document carries the cross-service technical rules.

The publication states that:

```text
each IBIS-IP service is versioned independently;
there is no single common IBIS-IP version;
service-document version corresponds to service version;
client and server service versions must be compatible;
multiple service versions can coexist and must be technically distinguishable by port and/or path.
```

The publication also says that project-specific extensions/deviations must use deliberately invalid version identifiers such as `2.1a` and be agreed project-specifically.

SDK consequence:

```text
service version remains an explicit resolver input;
endpoint identity is not schema identity;
no latest-XSD-wins;
project-specific non-standard version strings must not silently route to a standard schema family.
```

This is consistent with the frozen resolver/authority model.

## 3. Exact V2.3 authority context

The V2.3 release-family cross-check that preceded this Deep Read identified a same-path semantic collision in Common V2.3 and was already resolved structurally:

```text
official Common V2.3 root:
  IBIS-IP_common_V2.3.xsd
  blob 0d8926c4063c12de9a5e68b6f0addaab35a55dc1

explicit PR #30 candidate overlay:
  schema_variants/upstream_pr_30/IBIS-IP_common_V2.3.xsd
  blob 456a7db179ce14bc3f04e2bc05e42e16545fb0c5
```

The current 50-root repository state was subsequently recompiled successfully in run `33169314332`, and EV-106 executes the Common V2.3 official/candidate difference in isolated pools.

This General-Conventions Deep Read does not change that authority decision.

## 4. Deliberate V2.3 change - HTTP/1.1

The V2.3 version history explicitly records one technical addition:

```text
In Kapitel 2.4 wurde die zu nutzende http Version ergänzt.
In chapter 2.4 the http version to be used was added.
```

Chapter 2.4 correspondingly states in the English track:

```text
IBIS-IP uses the established http version 1.1.
```

Classification:

```text
ok_with_note / intentional V2.3 transport-profile addition
```

SDK/runtime consequence:

```text
HTTP/1.1 can now be attributed directly to VDV 301-2 V2.3.
```

The full V2.3 text still contains no literal requirement for:

```text
Content-Type
application/xml
text/xml
```

Therefore the project's source-separation rule remains:

```text
HTTP/1.1 requirement: directly VDV-derived for V2.3
Content-Type/media-type requirements: separately attributed to applicable HTTP/XML standards, not falsely quoted as a VDV 301-2 V2.3 sentence
```

## 5. Existing findings strengthened by V2.3

### DISC-001 / DR3012-001 - material German/English IP-allocation conflict persists

The German V2.3 track says that there are no specifications for IP-address allocation and presents fixed address allocation or DHCP as best practice.

The English V2.3 track still states decentralized ZeroConf allocation, cites `RFC 2927` and says the `169.254.x.x` specifications must be observed for an interoperable network.

The bibliography, however, lists:

```text
RFC 3927 Dynamic Configuration of IPv4 Link-Local Addresses
```

Thus the V2.2 language conflict is not repaired in V2.3 and the incorrect English RFC number remains.

Handling remains:

```text
do not silently choose one language track as corrected normative authority;
do not enforce the English ZeroConf/169.254 wording as a universal VDV failure without exposing the conflict;
attribute RFC-level diagnostics separately.
```

### DR3012-002 - SRV Weight semantics still conflict with RFC 2782

The V2.3 SRV table states that, for equal service names, the service with the lower weight is preferred.

RFC 2782 instead defines `Weight` as a relative weight among equal-priority records, with larger weights receiving proportionately higher selection probability.

The historical `DR3012-002` evidence chain therefore extends through V2.3.

Runtime consequence:

```text
do not implement RFC 2782 service selection as simple ascending-weight preference merely from the VDV table wording;
retain the source conflict as discovery/runtime audit knowledge.
```

### DR3012GC22-002 - German TXT subsection remains incorrectly numbered 3.3.1

The V2.3 German table of contents and body still use:

```text
3.3.1 Nutzung des SRV-Records
3.3.1 Nutzung des TXT-Records
```

The English track correctly uses:

```text
3.3.1 Use of SRV Records
3.3.2 Use of TXT Records
```

The V2.2 finding therefore persists unchanged in V2.3.

### SUB-001 - `TerminateSubscribe*` operation notation persists

V2.3 Table 4 still maps:

```text
UnsubscribeData request  -> TerminateSubscribeRequestStructure
UnsubscribeData response -> TerminateSubscribeResponseStructure
```

The exact official Common V2.3 XSD defines instead:

```text
UnsubscribeRequestStructure
UnsubscribeResponseStructure
```

No executable `TerminateSubscribe*` alias is introduced.

Handling:

```text
validation/routing follows the selected exact XSD family;
the printed notation remains an explanatory documentation defect only.
```

### DR3012V21-001 - stale DeviceManagementService document reference persists

Both language tracks of the V2.3 system-start section still point DeviceManagementService to:

```text
VDV 301-2-2
```

In the separated V2.x service-document family DeviceManagementService is `VDV 301-2-0`; `301-2-2` is BeaconLocationService.

The stale-reference chain therefore extends through V2.3.

## 6. Predecessor defect resolved in V2.3

### DR3012GC22-001 - unresolved Word cross-reference placeholders no longer found

The V2.2 publication contained repeated literal Word-generation placeholders equivalent to:

```text
Fehler! Verweisquelle konnte nicht gefunden werden.
```

Fresh full-text searches in V2.3 found no occurrence of:

```text
Verweisquelle
reference source
```

and no corresponding literal unresolved Word-reference marker was found in the relevant sections.

Classification for V2.3:

```text
resolved_in_successor_version
```

The historical V2.2 finding remains valid for V2.2 and must not be erased.

## 7. New V2.3-specific finding

### DR3012GC23-001 - German V2.3 version-history subsection numbers remain in the 7.1 namespace

Under:

```text
7.2 Version 2.3
```

the German headings are printed as:

```text
7.1.3 Funktionale Erweiterungen
7.1.4 Technische Ergänzungen/Korrekturen
```

while the immediately adjacent English headings correctly use:

```text
7.2.1 Functional Upgrade
7.2.2 Technical Upgrade/Corrections
```

Classification:

```text
pdf_label_or_heading_error_candidate
confidence: high from native text; visual page closure pending
validation impact: documentation navigation/version-history presentation only
```

No resolver or XSD alias is implied.

## 8. Subscription semantics reconfirmed

V2.3 explicitly keeps the cross-operation convention:

```text
Get-able data -> Subscribe and/or Unsubscribe exists
Subscribe-able data -> corresponding Unsubscribe and Get exists
Unsubscribe-able data -> corresponding Subscribe and Get exists
```

For heartbeat monitoring it states that the service sends current subscribed data at the latest when the heartbeat interval expires. The heartbeat is provided via `SubscribeResponseStructure`; absent or zero means the server does not provide subscription monitoring.

This strengthens the existing cross-service subscription model but does not define a new XML response structure for the subscriber's HTTP callback reception.

## 9. Network/XML error-level separation reconfirmed

V2.3 distinguishes:

```text
network / HTTP / UDP errors -> transport protocol error mechanisms;
wrong HTTP address -> normal HTTP 404 example;
successful transport but malformed XML request -> XML error response from the addressed service;
partial/estimated values -> IBIS-IP wrapper types may carry ErrorCode.
```

This remains consistent with the SDK's separation between transport diagnostics and schema/application diagnostics.

## 10. XML/XSD notation and validation authority

The V2.3 publication again says that IBIS-IP information contents are transmitted in XML structures and can be validated with XML Schema/XSD.

Its table notation describes cardinality, choice, references, complex structures and abbreviated type names. It also points to downloadable XSD files as the digital form of the interfaces.

Project consequence remains:

```text
selected exact XSD family/variant = executable XML authority;
PDF tables and examples = semantic/documentation evidence;
PDF/XSD disagreement = finding, not silent schema rewrite.
```

## 11. Additional report-only editorial observations

Several low-impact editorial defects persist or appear in examples, including forms such as:

```text
HTPP services
DeviceManagmenService
CustomumerInformationService
DeviceManagmentServices
```

They do not receive separate finding IDs because they do not create a credible alternative operation/schema identity after context is considered.

## 12. Old-audit comparison

The prior audit already contained the main long-running General-Conventions issues:

```text
DISC-001 German/English IP-allocation conflict
DR3012-001 RFC 2927 / RFC 3927 problem
DR3012-002 SRV Weight semantics
SUB-001 TerminateSubscribe notation
DR3012V21-001 stale DMS document reference
DR3012GC22-002 duplicate German TXT subsection number
```

The fresh V2.3 read independently confirms their persistence.

It also establishes two V2.3 delta facts that should not be lost:

```text
DR3012GC22-001 unresolved Word references are repaired in V2.3;
DR3012GC23-001 introduces a new German version-history heading-number defect.
```

## 13. Deep-read conclusion

```text
byte-pinned official source: yes
textual fresh read: complete
V2.2 -> V2.3 delta review: complete
release/authority cross-check: complete
old-audit comparison: complete
independent OCR: not used
visual screenshot review: attempted, failed with source cache-miss
visual closure: pending
deep_read_state: needs_visual_review
```

The document must not be promoted to `exhaustive_read` until the pinned PDF bytes can be rendered locally or the visual backend becomes reliable.

## 14. Next active Deep Read

The next priority document is:

```text
COMMON_V2.3
VDV 301-2-1 V2.3
Common Data Structures and Enumerations
```

Reason:

```text
its official source is already byte-pinned;
CE-020 has original-table visual evidence plus EV-106 executable evidence;
the remainder of Common V2.3 still requires the normal fresh exhaustive document pass.
```
