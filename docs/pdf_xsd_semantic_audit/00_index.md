# PDF/XSD semantic audit - current index

Status: consolidated current navigation index. Historical detailed audit files remain evidence; this file defines the present project phase and where to resume.

Branch:

```text
dev/schema-integration
```

## 1. Start here

Read in this order:

```text
AUDIT_SCOPE_MATRIX.md
AUDIT_HANDOFF.md
findings.md
validation_backlog.md
```

Core policies:

```text
VALIDATION_AUTHORITY.md
MIXED_VERSION_VALIDATION_PREMISE.md
FINDING_CLASSIFICATION_POLICY.md
OFFICIAL_RELEASE_BACKFILL_POLICY.md
OFFICIAL_RELEASE_BACKFILL_SAME_PATH_COLLISION_POLICY_ADDENDUM.md
```

Always fetch the current branch HEAD before editing.

## 2. Current project phase

Completed:

```text
semantic/provenance PDF-XSD first pass across service scope
historical Common/Enums and service-family audit
Base / General Conventions closure
Network Infrastructure 301-3 context
cross-service subscription modelling
V1.0 superbranch dedup/storage refinement
executable XSD evidence EV-001/002/101-105
deterministic runtime evidence RV-001-RV-004
live/integration backlog consolidation
central findings/backlog/handoff/index consolidation
```

Current next phase:

```text
freeze semantic/audit baseline
-> derive machine-readable SDK manifest and resolver model
-> implement SDK regression baseline
```

Open real-world validation is tracked separately in:

```text
26_live_integration_validation_backlog.md
```

## 3. Validation authority

```text
Selected exact XSD family = executable XML authority where a schema profile exists.
PDF/XSD discrepancies = explanatory/provider findings, not silent XSD rewrites.
No latest-XSD-wins.
No latest Common/Enums substitution.
No latest external-protocol-version substitution.
Candidate material remains candidate/integration.
```

Non-XSD services use explicit protocol/discovery profiles.

Runtime findings retain source authority separately from severity.

## 4. Evidence namespaces

```text
EV-* = executable XML/XSD evidence
RV-* = deterministic runtime/protocol evidence
LI-* = open live/integration task IDs in block 26
```

Defined EV set:

```text
EV-001
EV-002
EV-101
EV-102
EV-103
EV-104
EV-105
```

There were no EV-003 through EV-100.

Defined deterministic RV set:

```text
RV-001 HTTP/XML + Content-Type
RV-002 DNS-SD/service discovery
RV-003 TimeService/SNTP
RV-004 Video RTSP/RTP boundary
```

## 5. Executable evidence files

```text
24_executable_validation_matrix_start.md
24a_executable_validation_pcs_001.md
24b_executable_validation_ce_018.md
24c_executable_validation_video_compositors.md
24d_executable_validation_trainset.md
24e_executable_validation_analog_radio.md
AUDIT_HANDOFF_DELTA_EXECUTABLE_VALIDATION_24.md
```

Evidence runs:

```text
EV-001/002  33109011670
EV-101      33109367265
EV-102      33109768872
EV-103      33111119723
EV-104      33111644388
EV-105      33111831627
```

## 6. Runtime/protocol evidence files

```text
25a_runtime_protocol_authority_matrix.md
25b_http_xml_content_type_profile.md
25c_dns_sd_service_discovery_profile.md
25d_time_service_sntp_profile.md
25e_video_rtsp_rtp_boundary.md
AUDIT_HANDOFF_DELTA_RUNTIME_25.md
generated/runtime_protocol_authority_matrix.csv
```

Evidence runs:

```text
RV-001  33112730418
RV-002  33119080288
RV-003  33119337775
RV-004  33119694991
```

## 7. Current live/integration plan

Canonical source:

```text
26_live_integration_validation_backlog.md
```

Contains live tasks for:

```text
subscriptions/heartbeat
DNS-SD/mDNS/PTR
HTTP endpoints/headers
UDP multicast/network/IGMP
SNTP exchange/clock diagnostics
RTSP/RTP media path
mixed-version end-to-end resolver
physical/network inventory
```

These require devices/provider systems/network access/captures and are not failed findings merely because they remain unexecuted.

## 8. Key architecture findings for the SDK

Use `findings.md` for the central index. Especially important:

```text
PCS-001  exact dependency/value-set routing matters
CE-018   XSD may be intentionally/mistakenly more permissive than PDF cardinality
VLS-002  VideoLive V2.0 xs:choice vs multi-field PDF record
VRS-003  VideoRecording V2.0 xs:choice vs grouped state
VDS-002/003/004 VideoDisplay compositor conflicts
TSM-002  operation group can disagree with valid global root
TSD-003  same lexical response name can require different schema by response context
ARA-003  candidate-only cardinality mismatch; authority guard mandatory
```

Cross-service consequence:

```text
Do not derive the SDK operation inventory solely from XSD groups.
```

## 9. Historical/Base architecture files

Important consolidation blocks:

```text
21_base_general_conventions_historical_family_closure.md
22_network_infrastructure_discovery_context.md
23_cross_service_subscription_modelling_closure.md
```

These establish:

```text
deduplicated V1.0 schema storage
legacy root-map model
independent service versions
XSD precedence
network/discovery authority separation
operation-manifest requirement
```

## 10. Common/Enumerations history

Primary historical chain:

```text
04_common_enums_historical_v1_0_to_v2_4_plan.md
04a_common_enums_v1_0_v2_0_history.md
04b_common_enums_v2_0_v2_1_history.md
04c_common_enums_v2_1_v2_2_history.md
04d_common_enums_v2_2_v2_3_history.md
04e_common_enums_v2_3_v2_4_history_and_closure.md
```

The older `01*` files remain detailed V2.4 evidence and should not be treated as the current continuation point.

## 11. Service audit evidence

Detailed service files and `*_FINDINGS_REGISTER_ADDENDUM.md` / `*_VALIDATION_BACKLOG_ADDENDUM.md` files remain the source for exact version-specific findings.

The semantic first pass is **not pending** for CustomerInformationService or the later services; old references saying they are next/pending have been superseded by this consolidated index and `AUDIT_SCOPE_MATRIX.md`.

## 12. Generated machine-readable artifacts

Current high-value generated artifacts include:

```text
generated/audit_scope_matrix.csv
generated/runtime_protocol_authority_matrix.csv
generated/cross_service_subscription_modelling_matrix.csv
generated/device_management_service_historical_scope_matrix.csv
service-specific generated scope/findings matrices
Common/Enums historical diff/inventory CSVs
```

Exact generated artifacts should be regenerated/updated when their source model changes; do not infer current state from an old generated file over the current Markdown authority.

## 13. Tools / regression harnesses

Key tools added during audit:

```text
tools/validate_xsd_pool.py
tools/validate_legacy_v1_roots.py
tools/validate_pcs_v21_operation_not_supported.py
tools/validate_ce018_service_identification_with_state_list.py
tools/validate_video_v20_compositors.py
tools/validate_trainset_ev104.py
tools/validate_analog_radio_ev105.py
tools/runtime_http_profile.py
tools/validate_http_runtime_ev25b.py
tools/runtime_discovery_profile.py
tools/validate_discovery_runtime_rv002.py
tools/runtime_time_profile.py
tools/validate_time_runtime_rv003.py
tools/runtime_video_profile.py
tools/validate_video_runtime_rv004.py
```

Historical filename note:

```text
validate_http_runtime_ev25b.py retains its old filename for provenance, but its evidence ID is RV-001.
```

## 14. Workflow

```text
.github/workflows/schema-audit-validation.yml
trigger: workflow_dispatch only
```

Do not leave a temporary push trigger active after a controlled evidence run.

## 15. Candidate / official-facing work

Use:

```text
OFFICIAL_PR_CANDIDATES_AFTER_AUDIT.md
service-specific OFFICIAL_PR_CANDIDATES_ADDENDUM_*.md
```

These are candidate registers only.

No official-facing action is authorized simply because an audit finding exists.

## 16. Immediate next task

```text
Design/freeze the SDK machine-readable manifest and resolver baseline from the consolidated audit.
```

Minimum manifest domains:

```text
schema profiles and exact dependencies
service/version/authority routing
legacy root mappings
operation and response-context mapping
non-XSD protocol/discovery profiles
runtime rule authority/severity
known discrepancy/provider notes
candidate selection guards
regression evidence references
```
