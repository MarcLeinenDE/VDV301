# Complete revalidation of all currently source-locator-complete findings — 2026-09-30

## Scope

This pass revalidated all 40 findings currently marked `coverage_state=complete` in
`audit_registry/finding_source_locators_v0.1.json`:

`ARA-001..ARA-004`, `ARCH-001..ARCH-008`, `BG-001..BG-002`, and `CE-001..CE-026`.

The purpose was defensive SDK hardening after an authority-classification mistake was detected and corrected for CE-007. The pass checks finding identity, version scope, release/candidate authority, exact XSD provenance, PDF/XSD interpretation, PASS/FAIL consequence, runtime scope, DE/EN diagnostics and locator quality.

## Global invariants revalidated

- The exact selected XSD remains the executable source of truth for XML conformance.
- A PDF/XSD mismatch never creates an alias, normalization or waiver.
- A payload that violates the exact selected XSD remains FAIL, even if the XSD spelling is typo-like.
- Candidate/integration XSDs are selectable executable authorities only when explicitly selected and must never be relabelled as official releases.
- Non-affected later correction versions may be retained as source/history boundaries but must not enter the affected runtime trigger scope.
- All 40 findings contain both German and English provider-facing diagnostic blocks.
- No XSD bytes are modified by this revalidation.

## Official-XSD provenance backcheck

All official-release XSD source identities currently pinned by the 40 complete source-locator findings were rechecked against the corresponding official `VDVde/VDV301` release tags where a tag-based XSD lane applies.

Result: **19 exact upstream tag/file/blob checks, 19 matches, 0 mismatches.**

This includes the V1.0 Common/Enumerations family:

- `VDV-301-1.0 / IBIS-IP_common_V1.0.xsd` -> `194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c`
- `VDV-301-1.0 / IBIS-IP_Enumerations_V1.0.xsd` -> `a9bea5bc73003ed91ded8519db06c32c4067831d`

The public Common V1.0 document contains internal Version-1.1 document/data-definition history. That does not downgrade the official release-tag authority of the V1.0 XSDs. Document revision history and executable XSD release authority remain separate concepts.

## Current V2.4 authority backcheck

The current upstream master still does not provide the selected Common/Enumerations/AnalogRadioService V2.4 XSD family as an official release family. The selected V2.4 Common/Enumerations files remain candidate/integration material and are not promoted by this review.

Open candidate/variant work is kept provenance-distinct from official release tags.

## Corrections found by this pass

### CE-002 — source locator correction

The technical finding remains correct: the V2.4 version history says `StopPointNumber`, while the actual StopInformation table and selected candidate XSD use `PointNumber`.

The stored PDF locator was wrong. Correct official V2.4 locations are:

- **2.50 StopInformation**, Table 50, printed page **34** — `PointNumber`
- **4.6 Version 2.4**, printed page **55** — history says `StopPointNumber` and carries the stale section reference `(2.51)`

Finding classification, SDK behavior and PASS/FAIL behavior do not change.

### CE-004 — affected scope and source locator correction

The current canonical scope was incorrectly narrowed to V2.4 candidate/integration only.

Exact historical evidence establishes the mismatch from V2.2 onward:

- V2.2 official PDF: 3.21 ServiceNameEnumeration / Table 86 / page 40 still lists `SystemDocumentationService` and `SystemManagementService`; V2.2 history on page 49 says both were deleted and `SystemMonitoringService` added.
- Official Enumerations V2.2 omits both stale values and contains `SystemMonitoringService`.
- V2.3 official PDF repeats the stale table; official Common V2.3 reuses the exact Enumerations V2.2 pool.
- V2.4 official PDF repeats the stale table; selected V2.4 candidate/integration Enumerations XSD also omits the stale values.

Correct affected scope:

- Enumerations V2.2-V2.3 — official release authority
- Enumerations V2.4 — selected candidate/integration authority

The previous V2.4 locator also incorrectly named section 3.28. The correct section is **3.21 ServiceNameEnumeration**.

SDK consequence remains XSD-invalid + advisory. The stale PDF service names are never aliases.

### CE-025 — runtime affected-scope correction

V2.4 is an explicit **non-affected correction boundary**: PDF and selected V2.4 XSD align on `ReplyPath`.

V2.4 is therefore removed from the semantic/runtime affected scope. It remains in source-locator coverage only to prove the correction boundary.

Affected runtime scope is now only Common V1.0-V2.3.

### CE-026 — runtime affected-scope correction

V2.4 corrects BeaconPoint to `Description`; it is an explicit **non-affected correction boundary**.

V2.4 is therefore removed from the semantic/runtime affected scope. It remains in source-locator coverage only to prove that the historical `Desciption` finding ends with V2.3.

Affected runtime scope is now only Common V1.0-V2.3.

## Reaffirmed findings

The other 36 complete findings were rechecked without a terminal finding/scope/PASS-FAIL change:

- ARA-001..ARA-004
- ARCH-001..ARCH-008
- BG-001..BG-002
- CE-001
- CE-003
- CE-005..CE-024 excluding the corrected CE-025 boundary case above
- CE-007 official V1.0 release-tag authority was specifically rechecked and remains `official_release`
- CE-008/CE-009 current identities are correct; the historical swapped-label delta remains quarantined by its explicit correction overlay

## Runtime/diagnostic checks

All 40 complete findings were checked for DE/EN diagnostics.

For findings with runtime mappings:

- selected-XSD authority guard remains mandatory;
- PASS/FAIL is not overridden by Known-Issue context;
- affected profile scope must match the semantic affected scope;
- a correction-boundary-not-affected lane must never be a runtime trigger lane.

## Validator hardening

The source-locator gate is strengthened by this revalidation to guard against recurrence:

1. semantic and runtime affected profile scopes must remain synchronized where a runtime mapping exists;
2. `correction_boundary_not_affected` coverage lanes are forbidden from affected semantic/runtime scope;
3. official-release local XSD locators are cross-checked against the corresponding upstream VDV release tag when a deterministic release tag can be resolved;
4. CE-002 and CE-004 retain regression assertions for their corrected source locations/scope.

## Progress accounting

This is a revalidation/correction pass. No existing finding identity is duplicated and no already-complete finding receives new progress credit.

Source-locator progress remains:

`40 / 192 complete · 0 partial · 152 remaining`

## Gate

Final strengthened validation gate:

- GitHub Actions run: **36715477452**
- result: **SUCCESS**
- validated commit: `869daa8f5c7f6760b88a7fbe9399c955edbd472e`
- source-locator validator result: `entries=40 complete=40 remaining=152 upstream_checks=19`

The gate also passed the full existing schema/audit regression suite. No XSD bytes were changed.
