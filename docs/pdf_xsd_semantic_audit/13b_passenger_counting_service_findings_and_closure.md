# PassengerCountingService V1.0 / V2.1 findings and first-pass closure

Status: semantic/provenance first-pass closure completed. Superbranch V1.0 packaging selection refined after tag1.0->tag2.0 diff review. Local XSD compilation/sample validation remains pending.

## Historical routing closure

### V1.0 source history

Original VDV-301-1.0 tag:

```text
IBIS-IP_PassengerCountingService_V1.0.xsd
blob 600a3ee6290c630a4435fb06ca9803dabaceb788
Common V1.0 + Enums V1.0
operation roots/group supplied by IBIS_IP_V1.0.xsd
```

Official VDV-301-2.0 tag later publishes the same service-version filename as:

```text
blob 4161872be76740abfdd1cddf96f8a736333fc8be
Common V1.0 + Enums V1.0
operation roots/group moved into the service XSD
```

The detailed diff shows the checked PCS payload structures remain the same; the later file is the self-contained packaging revision. The operational superbranch therefore selects `4161872...` and records the original aggregate relationship as provenance rather than storing both copies.

### V2.1

```text
Official service XSD source: VDVde/VDV301 tag VDV-301-2.1
Service blob: 59ef2ddb09b92db0d492974e38bad5b6be03865e
Service dependency pool: Common V1.0 + Enums V1.0.
```

## PCS-001 - OperationNotSupported excluded by selected V2.1 dependency pool

```text
state: confirmed PDF/XSD dependency/value-set discrepancy
mismatch_kind: schema_family_or_dependency_value_set
confidence: high
validation_behavior: exact PCS V2.1 pool excludes OperationNotSupported
handling: local validation + post-audit schema-family clarification candidate
```

Reason:

```text
PDF V2.1 documents OperationNotSupported for new optional operations.
PCS V2.1 explicitly selects Common V1.0 + Enums V1.0.
Enums V1.0 lacks OperationNotSupported.
Enums V2.1 contains it but is not selected.
Common V1.0 response/wrapper types route ErrorCode positions through ErrorCodeEnumeration.
```

No automatic schema/dependency fix is proposed.

## PCS-002 - original V1.0 aggregate packaging

```text
state: OK with note / historical packaging fact
confidence: high
current superbranch handling: later official self-contained V1.0 revision
```

The original tag1.0 service file alone was not the complete root-validation family, but the later official tag2.0 V1.0 revision embeds the same operation roots/group. Therefore the superbranch no longer requires the old aggregate for PCS runtime validation.

## SDK implications

```text
- Preserve PCS V1.0 and V2.1 as separate service profiles.
- PCS V1.0 operational XSD: official self-contained V1.0 blob 4161872...
- Preserve provenance of original tag1.0 blob 600a3ee... and aggregate packaging.
- Preserve PCS V2.1 -> Common V1.0 -> Enums V1.0 exactly.
- Do not latest-wins-map PCS V2.1 to Common/Enums V2.1.
- OperationNotSupported diagnostics must distinguish PDF semantics from XSD-selected value-set authority.
```

## Validation status

```text
Semantic/provenance first pass: closed.
Superbranch packaging selection: source/diff reviewed.
Local XSD compilation: not yet demonstrated.
Sample XML validation: not yet demonstrated.
No XSD content correction performed.
```
