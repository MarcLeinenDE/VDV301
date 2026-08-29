# Audit handoff delta - TicketValidationService V2.1 Deep Read

Date: 2026-08-29
Canonical branch: `dev/schema-integration`

## Scope completed

`TVS_V2.1` was processed under the current `FINDING_EVIDENCE_GATE.md` using the official public VDV writing, exact byte pin, independent exact-XSD authority verification, Fresh Read before reopening historical TicketValidation findings, targeted visible review of pages 10-17, active counter-hypothesis checks and executable evidence where XML behavior was material.

Completion state:

```text
textual fresh read: complete
targeted visible review: pages 10-17 complete
exhaustive visual review: no
Deep Read state: needs_visual_review
```

## PDF source authority

```text
source_id: TVS_V2.1
sha256: 676c05d7615f2f2ce95ec4eb085428cb0c970a4226809566e8968200df69988d
size: 752652 bytes
pin run: 33248946083
pinned-byte visual render run: 33249247106
render job: 99091940668
```

Interactive screenshots returned cache-miss on material pages, so exact pinned bytes were rendered through the repository fallback and pages 10-17 were visibly inspected.

## Exact XSD authority

Official tag: `VDV-301-2.1`.

```text
IBIS-IP_TicketValidationService_V2.1.xsd  f6497e6469b82ee19b185c4de749d13a7ca60bed
IBIS-IP_common_V1.0.xsd                   194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c
IBIS-IP_Enumerations_V1.0.xsd             a9bea5bc73003ed91ded8519db06c32c4067831d
```

The integration-branch copies match the official tag exactly.

Important routing rule:

```text
TVS V2.1 intentionally depends on Common V1.0 + Enumerations V1.0.
Do not substitute later Common/Enums versions.
```

## Existing finding revalidated

### TVS-002

PDF page 16 prints `RouteDirectionEnumeration` for `VehicleData.RouteDeviation`; exact V2.1 XSD uses `RouteDeviationEnumeration`.

EV-112, run `33249561880`, job `99092772643`, proves:

```text
RouteDeviation exact type = RouteDeviationEnumeration
RouteDirectionEnumeration absent from exact Enums V1.0

onroute/offroute/unknown -> valid
NOT_A_ROUTE_DEVIATION    -> invalid
```

State: `executable_confirmed_EV-112`.

TVS-001 (V2.4 scope) and TVS-003 (V2.2+ scope) are not revalidated by this V2.1 block and remain subject to their own Evidence-Gate passes.

## New findings

```text
DRTVS21-001
CurrentTripRef type is printed IBIS-IP.NMToken; exact XSD/Common use case-sensitive IBIS-IP.NMTOKEN.
EV-112 confirms NMTOKEN exists, NMToken does not and a typo probe schema fails compilation.

DRTVS21-002
GetCurrentLine response display omits the service-name separator dot: TicketValidationServiceCurrentLineData.
Only the missing dot is classified; the PDF's recurring omission of Structure in shortened displays is not itself treated as a defect.

DRTVS21-003
German and English flow text say SubscribeCurrentStop, while formal overview, detailed section and exact XSD say SubscribeCurrentStopPoint.

DRTVS21-004
Minor non-executable editorial spelling residue on targeted pages (Unscubscribe, GetrazziaResponsetData, Error Respone).
```

## EV-112 provenance

```text
checker: tools/validate_tvs_v21_ev112.py
run: 33249561880
job: 99092772643
head tested: 5edc3f1d167e93dffcc3978f6e903ee0fba3f960
result: PASS
```

The temporary push-trigger workflow was removed immediately after evidence collection. The permanent reusable checker remains. No XSD changed.

## Files added/updated by the permanent closure

```text
docs/pdf_xsd_semantic_audit/deep_read/TVS_V2.1.md
audit_registry/deep_read_findings_delta_tvs_v21_2026-08-29.json
audit_registry/deep_read_registry_delta_tvs_v21_2026-08-29.json
docs/pdf_xsd_semantic_audit/TICKET_VALIDATION_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/24k_executable_validation_tvs_v21.md
docs/pdf_xsd_semantic_audit/EVIDENCE_ID_POLICY.md
docs/pdf_xsd_semantic_audit/validation_backlog.md
audit_registry/finding_revalidation_registry_v0.1.json
00_START_HERE/CURRENT_STATE.json
```

## Next natural Deep Read target

```text
TVS_V2.2
VDV 301-2-16 TicketValidationService V2.2
```

Required sequence remains:

```text
1. own byte pin of official TVS V2.2 PDF
2. independently establish exact official V2.2 XSD/dependency authority
3. Fresh Read before reopening V2.2 historical findings/history
4. apply current Evidence Gate and visible pinned-byte review where layout/table context matters
5. executable-confirm material XML behavior where practical
6. close as needs_visual_review unless exhaustive visual closure is actually achieved
```

After all remaining Deep Reads, freeze the complete finding inventory and perform mandatory legacy-finding revalidation. SDK finding knowledge and remediation readiness remain false until that gate is complete.

No PR, comment, merge, XSD change or official-facing remediation action was performed.
