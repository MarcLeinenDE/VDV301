# PDF/XSD semantic audit - canonical handoff

Status: consolidated continuation authority after completion of the historical semantic/provenance audit, executable XSD evidence and deterministic runtime/protocol evidence.

Branch:

```text
MarcLeinenDE/VDV301:dev/schema-integration
```

Always fetch the current branch ref before making changes. A remembered commit SHA is context only, never the write base.

## 1. Branch / official-facing policy

```text
dev/schema-integration is the superbranch / integration-audit branch.
Do not open the full branch as an upstream VDVde/VDV301 PR.
Do not describe the full branch as an official VDV release.
Fork master remains untouched.
No upstream PR/comment/review/merge/official-branch action without explicit user approval.
Candidate/integration files remain candidate/integration until officially released/merged by the authoritative source.
```

## 2. Current continuation order

For a new chat or continuation, read in this order:

```text
1. current dev/schema-integration branch HEAD
2. docs/pdf_xsd_semantic_audit/AUDIT_SCOPE_MATRIX.md
3. docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF.md
4. docs/pdf_xsd_semantic_audit/findings.md
5. docs/pdf_xsd_semantic_audit/validation_backlog.md
6. docs/pdf_xsd_semantic_audit/00_index.md
```

Then use detailed service/EV/RV files only for the specific area being worked on.

Core policy documents:

```text
VALIDATION_AUTHORITY.md
MIXED_VERSION_VALIDATION_PREMISE.md
OFFICIAL_RELEASE_BACKFILL_POLICY.md
OFFICIAL_RELEASE_BACKFILL_SAME_PATH_COLLISION_POLICY_ADDENDUM.md
FINDING_CLASSIFICATION_POLICY.md
```

Latest phase deltas:

```text
AUDIT_HANDOFF_DELTA_EXECUTABLE_VALIDATION_24.md
AUDIT_HANDOFF_DELTA_RUNTIME_25.md
```

## 3. Current project state

Completed:

```text
- semantic/provenance first pass across the public VDV301 service scope through V2.4 material available to this project
- Base / General Conventions historical-family closure
- Network Infrastructure 301-3 context audit
- cross-service subscription modelling closure
- deduplicated historical V1.0 superbranch layout
- EV executable XSD evidence phase
- RV deterministic runtime/protocol evidence phase
- consolidated live/integration backlog
```

Still open by environment:

```text
- live device/provider/network integration tests
- packet-capture-backed DNS-SD/mDNS/HTTP/UDP/SNTP/RTSP/RTP validation
- physical/network inventory evidence
```

Canonical open live backlog:

```text
26_live_integration_validation_backlog.md
```

These open live tasks do not block SDK design as long as they remain optional runtime capabilities and are never presented as executed conformance evidence.

## 4. Validation authority

Primary executable rule:

```text
Where an exact selected XSD profile exists, validation follows that XSD family.
PDF/XSD differences are findings/provider notes, not silent XSD rewrites.
```

Additional guards:

```text
No latest-XSD-wins.
No global latest Common/Enums substitution.
No latest-external-protocol-version substitution.
Service identity/version and exact dependency pool matter independently.
Operation/root/context selection may require an operation manifest beyond raw XSD group enumeration.
Non-XSD services use explicit protocol/discovery profiles.
Runtime findings retain authority source separately from severity.
```

VDV 301-2 V2.4 General Conventions explicitly support independently versioned services and state XSD precedence over documentation in inconsistencies; these findings support the architecture already adopted in this project.

## 5. Superbranch historical storage model

The superbranch is a deduplicated operational schema set, not a byte-for-byte mirror of every official tag.

Rules:

```text
byte-identical historical XSD -> store once
same filename/version but packaging-only later official revision -> may use the more self-contained official revision after semantic diff review
actual semantic constraint difference -> preserve separate routing context
missing historical XSD -> backfill only from exact official VDVde/VDV301 release tags
candidate/open-PR material -> separate candidate authority lane
```

Legacy V1.0 type-only root declarations are represented via:

```text
schema_profiles/VDV-301-1.0-root-map.csv
tools/validate_legacy_v1_roots.py
```

Do not reintroduce the old full `IBIS_IP_V1.0.xsd` aggregate into the operational root merely to recreate historical packaging.

## 6. Completed EV evidence

Identifier rule:

```text
EV-* = executable XML/XSD evidence
```

Defined/completed IDs:

```text
EV-001 + EV-002  run 33109011670
  46 root XSDs compile
  DMS V2.4 regression samples 6/6
  legacy V1.0 root adapters compile

EV-101  run 33109367265
  PCS-001 OperationNotSupported exact-dependency mismatch confirmed

EV-102  run 33109768872
  CE-018 ServiceIdentificationWithStateList XSD 0:* behavior confirmed V1.0-V2.4

EV-103  run 33111119723
  VLS-002 / VRS-003 / VDS-002/003/004 compositor findings confirmed

EV-104  run 33111644388
  TSM-002 internal V2.2 operation-group/global-root mismatch confirmed
  TSD-003 resolved as acknowledgement-vs-data-event contextual routing rule

EV-105  run 33111831627
  AnalogRadio ARA-003 candidate XSD permits Transmitter 0:1
```

There were never EV-003 through EV-100; EV-101+ is the finding-specific namespace.

## 7. Completed deterministic RV evidence

Identifier rule:

```text
RV-* = runtime/protocol evidence
```

Completed:

```text
RV-001  run 33112730418
  HTTP/XML + Content-Type classifier

RV-002  run 33119080288
  DNS-SD / VDV discovery + HTMLDisplay profiles

RV-003  run 33119337775
  TimeService V1.0 / RFC 4330 SNTP classifier

RV-004  run 33119694991
  Video rtspURI / RTSP-version boundary / RTP header classifier
```

These are deterministic classifier tests, not live-device claims.

## 8. High-impact current findings

Central index:

```text
findings.md
```

Especially important for SDK architecture:

```text
PCS-001  exact dependency/value-set mismatch; no enum latest-wins
CE-018   XSD permits empty state list despite PDF 1:*
VLS-002  official V2.0 LiveStreamData xs:choice conflicts with PDF multi-field record
VRS-003  official V2.0 recording-state xs:choice conflicts with grouped PDF semantics
VDS-002/003/004 official V2.0 compositor conflicts
TSM-002  official V2.2 operation group uses stale name while global corrected root exists
TSD-003  not a defect: same response name has acknowledgement vs callback-data context
ARA-003  candidate-only V2.4 Transmitter PDF 1:1 vs candidate XSD 0:1
```

## 9. Important non-XSD profiles

### TimeService V1.0

```text
validation kind: protocol_discovery_profile
functional protocol: SNTP per VDV-selected RFC 4330
no synthesized XML operations
```

### HTMLDisplayService V2.1/V2.2/V2.2a

```text
validation kind: discovery_http_profile
no dedicated service XSD by design
version-specific DNS-SD endpoint semantics
```

## 10. Subscription / operation-manifest architecture

Cross-service audit established:

```text
Do not derive supported operations solely from XSD service groups.
```

Minimum future operation-manifest dimensions:

```text
service_id
service_version
operation_name
operation_kind
HTTP method / transport
request payload schema ref
immediate response schema ref
callback payload schema ref
response context
callback endpoint fields
heartbeat semantics
selection parameters
schema authority/pool id
source provenance
```

This is required for TrainSet contextual responses and protects against stale operation-group members such as TSM-002.

## 11. Runtime authority model

Machine-readable source:

```text
generated/runtime_protocol_authority_matrix.csv
```

Authority classes include:

```text
vdv_normative
external_normative
external_normative_referenced_by_vdv
vdv_profile_exception_or_specialization
combined_semantics
diagnostic_heuristic
```

Example guards:

```text
missing Content-Type with a known body/media -> external HTTP warning, not invented explicit VDV error
DNS-SD != mandatory mDNS
RFC 5905 does not latest-wins replace TimeService's selected RFC 4330 profile
RTSP 2.0 does not latest-wins replace RTSP 1.0 and is not a VDV-pinned requirement from current evidence
valid VideoLive XML metadata does not prove playable media
```

## 12. Workflow state

```text
.github/workflows/schema-audit-validation.yml
trigger: workflow_dispatch only
```

Do not leave a push trigger enabled after evidence collection; repeated Actions failures previously generated unwanted email notifications.

## 13. Next phase

Current active transition:

```text
central audit consolidation -> freeze audit baseline -> derive SDK manifest/resolver baseline
```

The semantic audit does not need to restart service-by-service.

SDK baseline should convert the audited knowledge into machine-readable profiles for:

```text
schema routing
service/version authority
exact dependencies
legacy root mappings
operation/context routing
non-XSD protocol profiles
runtime check authority/severity
known PDF/XSD discrepancy notes
candidate guards
```

Live/integration tasks from block 26 then become SDK/tool integration tests rather than a prerequisite for defining the SDK architecture.

## 14. Working style

After a meaningful block:

```text
1. work only on dev/schema-integration unless user says otherwise
2. keep candidate/official authority explicit
3. run real tests before claiming pass/fail
4. update central control docs only when the continuation point materially changes
5. prefer concise phase deltas over duplicated historical state
6. report current branch SHA to the user
```
