# Complete revalidation of all currently source-locator-complete findings — 2026-09-30

## Scope

This pass revalidated all 40 findings currently marked `coverage_state=complete` in
`audit_registry/finding_source_locators_v0.1.json`:

`ARA-001..ARA-004`, `ARCH-001..ARCH-008`, `BG-001..BG-002`, and `CE-001..CE-026`.

The purpose was defensive SDK hardening after an authority-classification mistake was detected and corrected for CE-007. The work was deliberately performed in two layers: first a semantic/authority/runtime revalidation of all 40 findings, then a second locator-quality pass across all eight referenced PDF source families to detect plausible-but-wrong page/section/table references that a structural JSON gate alone cannot detect. The pass checks finding identity, version scope, release/candidate authority, exact XSD provenance, PDF/XSD interpretation, PASS/FAIL consequence, runtime scope, DE/EN diagnostics and locator quality.

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

### CE-020 — PDF source-locator correction

The technical finding remains unchanged: official Common V2.3 uses primitive `xs:string` / `xs:language` in the selected XSD, while the official PDF documents `IBIS-IP.string` / `IBIS-IP.language`; PR #30 is an explicit candidate overlay that aligns those two member types with the PDF.

The stored PDF locator was wrong for both the official and PR30 lanes. The exact official V2.3 source location is:

- **1.17 InternationalTextType**
- **Table 17 Description of InternationalTextType**
- printed page **12**

The prior `2.61 / Table 61 / page 36` locator was unrelated to InternationalTextType and has been removed.

Finding identity, official-vs-candidate authority split and PASS/FAIL behavior do not change.

### CE-025 — affected-scope and PDF source-locator correction

V2.4 is an explicit **non-affected correction boundary**: PDF and selected V2.4 XSD align on `ReplyPath`.

V2.4 is therefore removed from the semantic/runtime affected scope. It remains in source-locator coverage only to prove the correction boundary. Affected runtime scope is now only Common V1.0-V2.3.

The second locator-quality pass also found that several stored SubscribeRequest/UnsubscribeRequest page, section and table references had been derived from an incorrect numbering sequence. The exact visible body locations are now pinned per version:

- V1.0: SubscribeRequest **1.51 / Table 51 / p.20**; UnsubscribeRequest **1.57 / Table 57 / p.22**
- V2.0: **2.54 / Table 54 / p.28**; **2.60 / Table 60 / p.30**
- V2.1: **2.54 / Table 54 / p.30**; **2.60 / Table 60 / p.32**
- V2.2: actual body headings **2.55 / Table 55 / p.32** and **2.61 / Table 61 / p.34**
- V2.3: **2.55 / Table 55 / p.33** and **2.61 / Table 61 / p.35**
- V2.4: **2.54 / Table 54 / p.35** and **2.60 / Table 60 / p.38**

The V2.2 distinction is intentional: its table of contents and visible body numbering are internally inconsistent in this area; locators follow the actual visible body heading/table, not a synthesized sequence.

### CE-026 — affected-scope and PDF source-locator correction

V2.4 corrects BeaconPoint to `Description`; it is an explicit **non-affected correction boundary**.

V2.4 is therefore removed from the semantic/runtime affected scope. It remains in source-locator coverage only to prove that the historical `Desciption` finding ends with V2.3. Affected runtime scope is now only Common V1.0-V2.3.

The second locator-quality pass also corrected the BeaconPoint source matrix. The exact visible PDF locations are:

- V1.0: **1.4 BeaconPoint / Table 4 / p.8**
- V2.0: **2.4 / Table 4 / p.15**
- V2.1: **2.4 / Table 4 / p.16**
- V2.2: **2.4 / Table 4 / p.17**
- V2.3: **2.4 / Table 4 / p.17**
- V2.4: **2.4 / Table 4 / p.19**

The earlier 1.5/2.5 and Table-5 references pointed to the following CardApplInformation section and were incorrect.

## Reaffirmed findings

The other 35 complete findings were rechecked without a terminal finding/scope/PASS-FAIL change:

- ARA-001..ARA-004
- ARCH-001..ARCH-008
- BG-001..BG-002
- CE-001
- CE-003
- CE-005..CE-024 excluding CE-020, which required a locator correction
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
4. CE-002 and CE-004 retain regression assertions for their corrected source locations/scope;
5. CE-020 retains exact 1.17 / Table 17 / page-12 assertions for both official and PR30 lanes;
6. CE-025 retains a version-by-version SubscribeRequest/UnsubscribeRequest source matrix and correction-boundary guard;
7. CE-026 retains a version-by-version BeaconPoint source matrix and correction-boundary guard.

## Progress accounting

This is a revalidation/correction pass. No existing finding identity is duplicated and no already-complete finding receives new progress credit.

Source-locator progress remains:

`40 / 192 complete · 0 partial · 152 remaining`

## Gate

Final strengthened validation gate after the second locator-quality pass:

- GitHub Actions run: **36716551728**
- result: **SUCCESS**
- validated commit: `2ec8a7a856888dd9950f3414da707575f167844a`
- source-locator validator result: `entries=40 complete=40 remaining=152 upstream_checks=19`

The gate explicitly passed the corrected CE-002, CE-004, CE-020, CE-025 and CE-026 regression matrices, semantic/runtime scope synchronization, non-affected correction-boundary exclusion, upstream release-tag XSD verification and the full existing schema/audit regression suite. No XSD bytes were changed.
