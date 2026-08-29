# Audit handoff delta – TrainSet V2.1 Deep Read

Date: 2026-08-29  
Branch: `dev/schema-integration`

## Scope completed

`TRAINSET_V2.1` fresh Deep Read completed textually with targeted visual confirmation from byte-pinned source material.

Source pin:

```text
SHA-256  8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e
size      1,708,401 bytes
pin run   33226637254
```

Status remains `needs_visual_review` because only semantically critical pages were rendered/inspected, not every page/figure.

## Exact XSD authority

Official `VDV-301-2.1` blobs, byte-identical in the integration branch:

```text
TSI V2.1  897f373e31b76aa23d8bc206854b042524e4c102
TSM V2.1  add9d1cb37e5759ff7a77855b239108d38373206
TSD V2.1  c2cdb73fcae265a2e4e0349ac6072e3548e36d8b
```

No later schema/dependency substitution.

## EV-109

Canonical manual workflow run:

```text
33228250613  PASS
```

EV-109 confirms:

```text
TSI-001  V2.1 cannot validate a second PDF-described coach record.
TSM-001  executable V2.1 root is GetTrainSetComposition; later ...Response root absent.
TSD-001  service-prefixed Subscribe/Unsubscribe roots/members absent; generic Common subscription infrastructure exists.
```

Full suite on the same run remains green:

```text
50 root XSDs
39 XSD service profiles
84 direct include edges
EV/RV suite PASS
SDK manifest/profile checks PASS
```

## New documentation findings

```text
DRTRAINSET21-001  stale/wrong section reference (9.1 vs material in section 10)
DRTRAINSET21-002  page 44 wrongly refers to equally named TrainSetDataService composition operations
DRTRAINSET21-003  page 44 GetTrainSetCompositon typo
```

All were classified after context/disproof checks. No typo aliases or synthetic TSD composition operations are permitted.

## Rejected observation

Potential `coupledSide`/`CoupledSide` mismatch was rejected after visible original and exact XSD both showed `CoupledSide`.

This rejected candidate is retained as explicit evidence of the disproof-first method.

## Evidence-Gate / legacy revalidation policy added

User required that older findings not touched during the current Deep Read must also be rechecked before SDK/remediation use.

Permanent additions:

```text
docs/pdf_xsd_semantic_audit/LEGACY_FINDING_REVALIDATION_PLAN.md
audit_registry/finding_revalidation_registry_v0.1.json
```

No grandfathering is allowed. After Deep Read Pass 2 the complete finding inventory is frozen and every finding not already explicitly revalidated under the current `FINDING_EVIDENCE_GATE.md` is rechecked.

SDK finding knowledge remains not-ready until the revalidation gate has zero pending SDK-relevant findings.

## Current TrainSet register status

```text
TSI-001  executable_confirmed EV-109
TSM-001  executable_confirmed EV-109
TSD-001  executable_confirmed EV-109 with generic-subscription context note

TSM-002  V2.2 historical EV-104 evidence; pending fresh V2.2 Evidence-Gate revalidation
TSD-002  V2.2 historical candidate; pending fresh V2.2 Evidence-Gate revalidation
TSD-003  V2.2 historical contextual resolution/EV-104; pending fresh V2.2 Evidence-Gate revalidation
```

## Files

```text
docs/pdf_xsd_semantic_audit/deep_read/TRAINSET_V2.1.md
audit_registry/deep_read_findings_delta_trainset_v21_2026-08-29.json
audit_registry/deep_read_registry_delta_trainset_v21_2026-08-29.json
docs/pdf_xsd_semantic_audit/TRAIN_SET_SERVICES_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/24h_executable_validation_trainset_v21.md
docs/pdf_xsd_semantic_audit/EVIDENCE_ID_POLICY.md
docs/pdf_xsd_semantic_audit/validation_backlog.md
00_START_HERE/CURRENT_STATE.json
```

## Next exact action

```text
1. byte-pin official TRAINSET_V2.2 PDF
2. Fresh Read V2.2 independently
3. establish exact V2.2 XSD blobs/dependencies
4. only then open/compare TSM-002, TSD-002, TSD-003 and EV-104
5. apply current Finding Evidence Gate and active disproof attempts
```

No XSD modification, no master change and no upstream/PR action is part of this handoff.
