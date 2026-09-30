# CE-006 source-locator revalidation — 2026-09-30

## Result

CE-006 remains terminally classified as a confirmed cross-artifact mismatch.

The selected XSD is normative for conformance validation. `DeviceStateEnumeration.warning` is therefore valid where the selected XSD contains it. The omission of `warning` from the corresponding VDV 301-2-1 PDF enumeration tables is a documentation gap and does not make an XSD-valid provider message invalid.

No alias, normalization, XSD rewrite, or provider FAIL is introduced by this finding.

## Version scope

- **V2.2 — official release:** official PDF section 3.5 / Table 70 omits `warning`; exact selected `IBIS-IP_Enumerations_V2.2.xsd` blob `2a23b512379b18e8f122ac1272cef8229fb86283` contains `warning`.
- **V2.3 — official release:** official PDF section 3.5 / Table 70 omits `warning`; the selected V2.3 Common dependency route reuses the exact V2.2 enumerations blob above.
- **V2.4 — candidate/integration XSD lane:** official PDF section 3.5 / Table 69 omits `warning`; selected candidate/integration `IBIS-IP_Enumerations_V2.4.xsd` blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25` contains `warning`.

The V2.4 XSD is not promoted to official-release authority by this review.

## Provider-facing diagnostic

### DE

**Titel:** DeviceState `warning` steht nur in der ausgewählten XSD

**Kurz:** Die ausgewählte XSD akzeptiert `warning`, während die zugehörigen geprüften PDF-Tabellen ab V2.2 diesen Wert nicht aufführen.

**Lang:** Die Abweichung ist für die geprüften V2.2-/V2.3-Profile und den ausgewählten V2.4-Candidate/Integration-Pfad belegt: Die jeweils maßgebliche Enumeration enthält `warning`, die zugehörige PDF-Tabelle nicht. Das ändert die XSD-Konformität nicht.

**Empfehlung:** `warning` bei passender ausgewählter XSD als gültig behandeln und auf die versionsgenaue Dokumentationslücke hinweisen.

### EN

**Title:** DeviceState `warning` exists only in the selected XSD

**Short:** The selected XSD accepts `warning`, while the corresponding checked PDF tables from V2.2 onward omit this value.

**Long:** The mismatch is evidenced for the checked V2.2/V2.3 profiles and the selected V2.4 candidate/integration lane: the applicable enumeration contains `warning` while the corresponding PDF table does not. This does not change XSD conformance.

**Recommendation:** Treat `warning` as valid for the selected XSD and explain the version-specific documentation gap.

## SDK consequence

- semantic issue kind: `semantic_contradiction`
- SDK behavior: `valid_with_advisory`
- activation class: `xsd_valid_advisory`
- required precondition: `xsd_result_valid`
- result effect: `decorate_existing_valid`
- authority guard: selected XSD result remains normative
- runtime implementation remains `reviewed_not_implemented`

## Existing executable evidence

Existing CE/Common executable evidence remains sufficient: EV-124 / run `33735601969`, together with the exact per-version XSD identities pinned in the source-locator manifest.

## Progress accounting

CE-006 already had a complete source locator before this revalidation. This review therefore receives **no duplicate progress credit**.
