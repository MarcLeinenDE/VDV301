# Legacy finding revalidation — Base / General — 2026-09-03

Status: completed under the current Finding Evidence Gate.

## Exact provenance reconstruction

Fresh upstream comparison of `VDVde/VDV301` tags `VDV-301-1.0` and `VDV-301-2.0` reconfirms the four same-path V1.0 blob transitions and removal of the original aggregate `IBIS_IP_V1.0.xsd`. The exact transitions are:

- JourneyInformationService V1.0: `1ee4d7ae...` → `8c303db5...`
- PassengerCountingService V1.0: `600a3ee6...` → `4161872b...`
- SystemManagementService V1.0: `85390f99...` → `2d32630a...`
- TicketInformationService V1.0: `017ca646...` → `3fda66d8...`

The strongest disproof hypothesis was also retained: **different blob does not automatically mean a different payload-validity model**. The prior semantic diff remains controlling for that distinction: these four transitions are primarily packaging/self-containment changes. Therefore `BG-001` is not a rule to duplicate every release snapshot or require `release_context` merely because bytes differ. Exact release context is needed where semantic constraints differ or strict historical reproduction is requested.

## BG-001

Terminal state: `context_verified`.

The provenance/routing warning survives: service name + version token alone does not prove byte identity. The refined interpretation also survives: blob difference alone is insufficient to infer a semantic validation difference. Exact selected blob/pool remains authority; latest-wins is forbidden.

## BG-002

Terminal state: `contextual_not_defect`.

Upstream tag comparison confirms that `IBIS_IP_V1.0.xsd` belongs to the original VDV-301-1.0 packaging and is removed in VDV-301-2.0. It remains historical packaging/root-declaration evidence, not an active dependency to mix with later self-contained V1.0 service files. No synthetic later aggregate is to be invented.

## Executable support — EV-123

Run `33726364976` executes the existing `tools/validate_legacy_v1_roots.py` against the current deduplicated superbranch. The generated harnesses are adapters only; they compile the exact legacy root mappings without modifying or pretending to replace official VDV XSDs.

Frozen inventory remains unchanged at 192 IDs. Live revalidation total after this block: **16 terminal / 176 pending**. Next block: `CE`. No XSD was changed.
