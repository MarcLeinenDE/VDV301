# Audit handoff delta - TicketValidationService V2.2 Deep Read

Date: 2026-08-29
Canonical branch: `dev/schema-integration`

## Scope completed

`TVS_V2.2` was processed under the current `FINDING_EVIDENCE_GATE.md` using the official public VDV writing, an exact byte pin, independent exact-XSD authority verification, Fresh Read before reopening historical V2.2 findings, targeted visible review of material pages, active counter-hypothesis checks and executable evidence where XML behavior was material.

Completion state:

```text
textual fresh read: complete
targeted visible review: pages 10-18 complete
historical reconciliation: complete
executable evidence: EV-113 PASS
exhaustive visual review: no
Deep Read state: needs_visual_review
```

## PDF source authority

```text
source_id: TVS_V2.2
sha256: 1915a1b12c24386e9a8ab5638fd88af6a442b5e42586b7b2d48f03e9a4205083
size: 785931 bytes
pin run: 33255245725
pinned_at_utc: 2026-08-29T13:31:54Z
pinned-byte visual render run: 33255450850
render job: 99108219131
artifact: 9715657871
```

Interactive screenshots returned cache-miss on material pages, so exact pinned bytes were rendered through the repository fallback and pages 10-18 were visibly inspected.

## Exact XSD authority

Official tag: `VDV-301-2.2`.

```text
IBIS-IP_TicketValidationService_V2.2.xsd  5a4be2b2ba66860f035777ec0458dba0790880e1
IBIS-IP_common_V2.2.xsd                    468fee6d177e7185dbcd5d3f90cfb114e29e01ae
IBIS-IP_Enumerations_V2.2.xsd              2a23b512379b18e8f122ac1272cef8229fb86283
```

The integration-branch copies checked during this Deep Read match the official tag exactly.

Routing rule:

```text
TVS V2.2 -> Common V2.2 -> Enumerations V2.2
Do not substitute later dependency versions.
```

## Fresh-Read independence

Before historical TicketValidation findings were reopened, the independent V2.2 read had already recorded:

```text
- stale CurrentStopPoint names remain despite explicit CurrentTariffStop rename history;
- CurrentTripRef is printed as IBIS-IP.NMToken;
- CurrentLine response display misses the service-name separator dot;
- flow text still says SubscribeCurrentStop;
- VehicleData.RouteDeviation is printed with RouteDirectionEnumeration although exact XSD uses RouteDeviationEnumeration;
- both V2.2 enum names exist and therefore require version-specific executable disproof rather than inheritance from V2.1.
```

That pre-historical state is permanently recorded in commit `ef81af8fb8189b008ef2e089768859a85863412a` and in `audit_registry/deep_read_registry_delta_tvs_v22_2026-08-29.json` history.

## Existing findings revalidated

### TVS-002

PDF page 16 prints `RouteDirectionEnumeration` for `VehicleData.RouteDeviation`; exact XSD uses `RouteDeviationEnumeration`.

EV-113 establishes that both enum names exist in exact V2.2 but are not interchangeable:

```text
RouteDeviationEnumeration = onroute/offroute/unknown
RouteDirectionEnumeration = Forward/Backward/Clockwise/Counterclockwise/Other

Forward as RouteDeviation -> invalid
onroute as RouteDirection -> invalid
```

State: `executable_confirmed_EV-113`.

### TVS-003

V2.2 version history explicitly documents `CurrentStopPoint -> CurrentTariffStop`, but stale `CurrentStopPoint` residue remains in both operation overviews and in page-14 response/data labels.

EV-113 confirms the exact executable rename boundary:

```text
GetCurrentTariffStopResponse -> exact global root exists and sample validates
GetCurrentStopPointResponse  -> no matching global declaration
CurrentTariffStopDataStructure -> exists
CurrentStopPointDataStructure  -> absent
```

State: `executable_confirmed_EV-113` with V2.2 scope refinement.

## Existing Deep-Read findings with V2.2 scope extension

```text
DRTVS21-001
V2.2 independently repeats IBIS-IP.NMToken; exact Common V2.2 uses IBIS-IP.NMTOKEN.
EV-113 confirms case-sensitive behavior.
State: executable_confirmed for V2.2.

DRTVS21-002
V2.2 independently repeats TicketValidationServiceCurrentLineData without the service-name separator dot.
EV-113 confirms the exact XSD type; PDF display classification remains contextual.
State: context_verified for V2.2.

DRTVS21-003
V2.2 German/English flow text independently repeats SubscribeCurrentStop, while detailed V2.2 section is SubscribeCurrentTariffStop after the documented rename.
State: context_verified for V2.2.
```

No duplicate V2.2-only IDs were opened for these repeated observations.

## No new unique V2.2 finding IDs

After reconciliation and deduplication, the V2.2 Deep Read did not require a new unique finding ID. The substantive V2.2 observations either revalidate/refine `TVS-002`/`TVS-003` or extend the independently recurring scope of `DRTVS21-001..003`.

This is intentional and avoids inflating the later mandatory legacy-revalidation inventory with duplicate findings.

## EV-113 provenance

```text
checker: tools/validate_tvs_v22_ev113.py
run: 33257767942
job: 99114368558
head tested: 28851cfdcf10e5569e512e235ce58ab02adb5167
result: PASS
```

The temporary push-trigger workflow was removed immediately afterward in commit `02512d99a3cfc4f29950e68788ce9233b45ff1f4`. The reusable checker remains. No XSD changed.

## Permanent closure files

```text
docs/pdf_xsd_semantic_audit/deep_read/TVS_V2.2.md
audit_registry/deep_read_findings_delta_tvs_v22_2026-08-29.json
audit_registry/deep_read_registry_delta_tvs_v22_2026-08-29.json
docs/pdf_xsd_semantic_audit/TICKET_VALIDATION_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/24l_executable_validation_tvs_v22.md
docs/pdf_xsd_semantic_audit/EVIDENCE_ID_POLICY.md
docs/pdf_xsd_semantic_audit/validation_backlog.md
audit_registry/finding_revalidation_registry_v0.1.json
00_START_HERE/CURRENT_STATE.json
tools/validate_tvs_v22_ev113.py
```

## Next natural Deep Read target

```text
TVS_V2.3
VDV 301-2-16 TicketValidationService V2.3
```

Required sequence remains:

```text
1. byte-pin the official V2.3 PDF independently
2. independently establish exact official V2.3 XSD/dependency routing before relying on historical routing notes
3. Fresh Read before reopening V2.3 historical findings or treating V2.2 corrections as current evidence
4. apply the current Evidence Gate and visible pinned-byte review where layout/table context matters
5. executable-confirm material XML behavior where practical
6. close as needs_visual_review unless exhaustive visual closure is actually achieved
```

The historical note that V2.3 is a documentation-correction release and routes to the official V2.2 service XSD must be independently re-established in the V2.3 block before it is promoted as current Evidence-Gate proof.

After all remaining Deep Reads, freeze the complete finding inventory and perform mandatory legacy-finding revalidation. SDK finding knowledge and remediation readiness remain false until that gate is complete.

No PR, comment, merge or official-facing remediation action was performed.
