# Finding version-scope boundary policy

Status: **canonical / mandatory**  
Adopted: 2026-10-07

A finding can be correctly proven inside one version while its affected-version scope is still wrong. Re-reading the same version does not establish where the defect starts or ends.

## Mandatory proof

For every potentially affected release:
- inspect the exact publication;
- inspect exact XSD/dependency authority when relevant;
- establish the last available non-affected predecessor when one exists;
- establish the first affected version;
- inspect every materially adjacent release that could carry the same issue;
- establish the last affected version;
- establish the first corrected/non-affected successor when one exists;
- explicitly record when no predecessor/successor exists;
- evaluate German and English tracks independently when both exist.

A one-language correction is only a partial correction.

## Identity

Persistence into another version does not create a new finding ID when it is the same semantic defect. Extend the existing finding scope.

## Registry and gate

Registry: `audit_registry/finding_version_scope_boundary_verification_v0.1.json`  
Validator: `tools/validate_finding_version_boundaries_v0_1.py`

At adoption, all already locator-complete findings are tracked. Structural locator expansion is frozen at that baseline until the retroactive pending count reaches zero.

After that backlog closes, each newly completed locator must enter the boundary registry as `verified` in the same terminal block.

Boundary verification is separate from semantic classification, locator structural completeness, visible-body verification and runtime mapping.

## Package execution for the retroactive pass

The retroactive pass may be executed in packages to reduce user interaction overhead.

Default package size: **5 findings**.

This is an orchestration convenience only. Each finding remains an independent terminal work cycle with its own:

- evidence report;
- registry/current-state write;
- `gate_pending` recovery state;
- full validation gate;
- `terminal_clean` handoff commit;
- final handoff-integrity gate.

A package must stop at the first failed gate, ambiguous boundary or material scope correction.
