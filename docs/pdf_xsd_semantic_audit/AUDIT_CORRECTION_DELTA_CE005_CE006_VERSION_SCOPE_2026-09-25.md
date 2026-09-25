# Audit correction delta — CE-005 / CE-006 version scope — 2026-09-25

Status: **post-Phase-A scope correction / evidence-backed / no finding reclassification**.

## Trigger

The Phase-B source-locator hardening pass compared the semantic registry against the already completed Common/Enumerations historical closure.

Two scope inconsistencies were found:

- `CE-005` semantic registry said `Common V1.0-V2.3` plus V2.4 candidate/integration, while the historical closure explicitly concluded **V2.0 through V2.4**.
- `CE-006` semantic registry contained only V2.4 candidate/integration, while the historical closure explicitly concluded **V2.2 through V2.4**.

These are metadata/scope defects in the post-classification registry. The underlying finding identities, classification, diagnostics, runtime disposition and XSD PASS/FAIL policy remain unchanged.

## CE-005 corrected scope

Canonical interpretation:

```text
V2.0-V2.3: affected selected Common profiles
V2.4: affected selected candidate/integration Common profile
V1.x: not included in the terminal affected range
```

Evidence trail:

- `04a_common_enums_v1_0_v2_0_history.md`: V2.0 PDF/history says `AdditionalTextMessage` is `0:*` / `maxOccurs=unbounded`, while V2.0 XSD remains max 1; explicitly supports CE-005 for V2.0.
- `04d_common_enums_v2_2_v2_3_history.md`: V2.3 adds named `AdditionalTextMessage1..9`, but the base field remains bounded; CE-005 remains supported.
- `04e_common_enums_v2_3_v2_4_history_and_closure.md`: terminal range consolidation says **CE-005 supported from V2.0 through V2.4**.
- Official V2.2 PDF physical/printed page 33, section 2.58, table 58 visibly documents `AdditionalTextMessage 0:*`; exact Common V2.2 blob `468fee6d177e7185dbcd5d3f90cfb114e29e01ae` declares `TripInformationStructure/AdditionalTextMessage` with no `maxOccurs`, therefore default max 1.
- Official V2.4 PDF printed page 36, section 2.57 visibly documents base and numbered AdditionalTextMessage rows as `0:*`; selected candidate Common V2.4 blob `1946fd37e29ced605654f49ea3d98cd2fbbdc8e4` declares each named field without `maxOccurs`.

The older V1.x publication is explicitly described in the historical audit as a V1.x/V1.1-consolidated source and is not used to extend the final CE-005 range backward.

## CE-006 corrected scope

Canonical interpretation:

```text
V2.2: affected Enumerations V2.2
V2.3: affected because Common V2.3 reuses Enumerations V2.2
V2.4: affected selected candidate/integration Enumerations V2.4
```

Evidence trail:

- `04c_common_enums_v2_1_v2_2_history.md`: V2.2 adds `DeviceStateEnumeration.warning`; PDF table omits it and the file explicitly says this supports CE-006 from V2.2 onward.
- `04d_common_enums_v2_2_v2_3_history.md`: V2.3 reuses the V2.2 enumeration pool containing `warning`, while the V2.3 PDF table omits it.
- `04e_common_enums_v2_3_v2_4_history_and_closure.md`: terminal range consolidation says **CE-006 supported from V2.2 through V2.4**.
- Official V2.2 PDF printed page 37, section 3.5, table 70 lists `defective, notavailable, running, readyForShutdown` and omits `warning`.
- Exact Enumerations V2.2 blob `2a23b512379b18e8f122ac1272cef8229fb86283`, simpleType `DeviceStateEnumeration`, contains enumeration `warning`.
- Official V2.4 PDF printed page 41, section 3.5, table 69 likewise omits `warning`.
- Selected candidate Enumerations V2.4 blob `2afed8cf23afa91db92b0f043cc5b4ad428b0f25`, simpleType `DeviceStateEnumeration`, contains enumeration `warning`.

## Invariants

This correction does **not**:

- change CE-005 or CE-006 finding identity;
- change defect assessment or confidence;
- change SDK behaviour;
- change runtime disposition (`reviewed`);
- change any XSD;
- add compatibility aliases;
- alter the rule that the exact selected XSD controls PASS/FAIL;
- change the Phase-A counts (77 reviewed / 115 not_applicable).

The deterministic Known-Issues mapping must be regenerated so its `profile_scope` equals the corrected semantic `version_scope` exactly.

## Follow-up

Phase A must be re-gated after this post-closure correction. Only after a green revalidation may Phase B source-locator persistence continue.

## Diagnostic alignment

The semantic-basis and bilingual diagnostic text for CE-006 were also updated because the earlier wording still spoke only about V2.4. The revised text now describes the evidence-backed V2.2/V2.3 official-profile range and the separate V2.4 candidate/integration lane. This is explanatory metadata only; `valid_with_advisory`, `runtime_match=reviewed`, the finding assessment and XSD PASS/FAIL behaviour are unchanged.

## Revalidation gate

Post-closure scope-correction gate **36100346868**: **SUCCESS**.

The gate verified the corrected CE-005/CE-006 scopes, preserved finding classifications and runtime states, exact semantic-to-runtime `profile_scope` projection, all Common validation lanes V2.0–V2.4, semantic and runtime-mapping validators, SDK-manifest consistency, the complete root-XSD regression pool and a clean XSD working tree.

## Persisted-state closure

Final persisted-state gate **36100477654**: **SUCCESS** on HEAD `40dfd6a640ac948ccdf308abb73f3ec66328029f`. The temporary correction workflow is removed after this closure.
