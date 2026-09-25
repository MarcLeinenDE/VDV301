# Known-Issues runtime mapping — Phase A terminal closure — 2026-09-25

Status: **COMPLETED / Phase A terminally closed**.

## Purpose

Phase A reviewed every semantic finding for whether it may later participate in deterministic runtime diagnostics.

This phase does **not** implement runtime matchers. It establishes the reviewed inventory and the authority/trigger boundaries that a later implementation phase must obey.

## Terminal inventory

```text
total           192
reviewed         77
not_applicable  115
candidate         0
not_designed      0
implemented       0
```

Every semantic finding now has a terminal runtime disposition.

## Closure invariants

The closure gate must prove all of the following:

1. the semantic registry contains exactly 192 unique findings;
2. only `reviewed` and `not_applicable` remain as runtime-match states;
3. the 77 Known-Issues mapping entries equal the 77 semantic `reviewed` IDs exactly;
4. the mapping manifest references the exact current semantic-registry Git blob;
5. all 77 mappings remain `reviewed_not_implemented`;
6. trigger descriptions are review metadata, not executable matcher definitions;
7. every mapping preserves `selected_xsd_result_remains_normative`;
8. SDK manifest and `CURRENT_STATE.json` counters agree with the semantic registry;
9. candidate/integration authority is not promoted to official release authority;
10. the complete root-XSD pool still passes and no XSD is mutated.

## Boundary to later phases

Phase A answers:

> Which verified audit findings are suitable for a future runtime diagnostic, and under what authority/profile conditions?

It does **not** yet answer:

> Which service operations are mandatory, optional, conditional or not applicable for a declared service/version?

That second question remains a separate capability-conformance artifact after the source-locator hardening pass, beginning with DeviceManagementService.

No executable matcher or XSD mutation is authorized by this closure.

## Gate history

Initial closure attempt **36098404986** stopped on an over-strict gate-design assertion: older CE V2.4 semantic entries correctly use the canonical field `authority: candidate_integration` but do not redundantly repeat the words “candidate” or “integration” in every free-text note/profile label. No audit data was changed for that failure.

The gate was hardened to compare each reviewed runtime mapping's complete `profile_scope` object directly against the source semantic finding's `version_scope`. This is the stronger provenance invariant.

Corrected Phase-A closure gate **36098481363**: **SUCCESS**.

Verified terminal inventory:

```text
reviewed        77
not_applicable 115
candidate        0
not_designed     0
implemented      0
total           192
```

The final persisted-state consistency run is triggered by recording this closure state.

## Final persisted-state gate

Run **36098583648**: **SUCCESS** on persisted closure HEAD `02fe789c38f255dcb318e80f70dc30dda90870a0`.

Phase A is therefore terminally closed. The canonical runtime-review inventory is **77 reviewed + 115 not_applicable = 192**, with **0 candidate, 0 not_designed and 0 implemented**. Trigger descriptions remain non-executable. No Known-Issues matcher may alter the selected XSD PASS/FAIL result.

## Post-closure scope correction discovered during Phase B

On 2026-09-25 the source-locator pass exposed two metadata-scope errors in the semantic registry. See `docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_CE005_CE006_VERSION_SCOPE_2026-09-25.md`.

- CE-005: terminal scope corrected to V2.0–V2.4 (not V1.0–V2.4).
- CE-006: terminal scope corrected to V2.2–V2.4 (not V2.4-only).

Finding classifications and Phase-A counts are unchanged. The closure remains subject to a fresh consistency gate after persistence of this correction.

## CE-005 / CE-006 correction revalidation

The post-closure scope correction was revalidated successfully in run **36100346868**. Phase-A counts remain **77 reviewed / 115 not_applicable / 0 candidate / 0 not_designed / 0 implemented**. Only evidence-backed version scope and CE-006 explanatory wording changed; PASS/FAIL semantics remain unchanged.

## Post-closure CE-011 scope correction discovered during Phase B

Phase-B locator hardening found that CE-011 was incorrectly narrowed to V2.4 in the semantic registry. Historical closure and version-specific evidence establish V2.2–V2.4, with V2.1 as an aligned negative control. See `docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_CE011_VERSION_SCOPE_2026-09-25.md`.

Classification, runtime disposition, counts and selected-XSD authority are unchanged. A fresh consistency gate is required.
