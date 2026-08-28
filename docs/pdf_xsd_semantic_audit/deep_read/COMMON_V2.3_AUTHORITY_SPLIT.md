# Common V2.3 official / PR #30 authority split

Status: resolved storage/provenance architecture; executable re-validation pending.

Date: 2026-08-28

## Trigger

During the fresh VDV 301-2 General Conventions V2.3 Deep Read, the complete official `VDV-301-2.3` release-tag inventory was compared with the superbranch.

The root path `IBIS-IP_common_V2.3.xsd` was found to contain blob:

```text
456a7db179ce14bc3f04e2bc05e42e16545fb0c5
```

while the exact official `VDV-301-2.3` tag contains:

```text
0d8926c4063c12de9a5e68b6f0addaab35a55dc1
```

## Semantic diff

The difference is not formatting or packaging-only material.

```text
Official VDV-301-2.3:
  InternationalTextType.Value    -> xs:string
  InternationalTextType.Language -> xs:language

Open upstream PR #30 candidate:
  InternationalTextType.Value    -> IBIS-IP.string
  InternationalTextType.Language -> IBIS-IP.language
```

The candidate blob is the head content of open upstream PR `VDVde/VDV301#30`, titled `Fix the definition of InternationalTextType`.

Because the change affects reachable field types, the project same-path collision policy forbids deduplicating the two revisions as if they were equivalent.

## Corrected superbranch storage

The root path is restored to exact official release authority:

```text
IBIS-IP_common_V2.3.xsd
  authority: official
  source tag: VDV-301-2.3
  blob: 0d8926c4063c12de9a5e68b6f0addaab35a55dc1
```

The PR #30 variant remains stored separately:

```text
schema_variants/upstream_pr_30/IBIS-IP_common_V2.3.xsd
  authority: candidate
  source: open upstream PR #30
  PR head: d1f1bf87b20d0cfb4b658555c9bd2779809c1f6d
  blob: 456a7db179ce14bc3f04e2bc05e42e16545fb0c5
```

This duplicate storage is intentional and required because the files differ semantically.

## Resolver rule

```text
Common@2.3 + authority=official
  -> root official release file

Common@2.3 + authority=candidate + schema_variant_id=common-v2.3-upstream-pr30
  -> isolated schema pool using the PR #30 overlay
```

No ordinary service/profile may select the PR #30 bytes merely because they are newer or because the PDF appears to support the candidate type names.

## SDK/audit records

```text
audit_registry/schema_variant_registry_v0.1.json
sdk_manifest/schema_variant_overlays_v0.1.json
docs/pdf_xsd_semantic_audit/COMMON_FINDINGS_REGISTER_ADDENDUM.md -> CE-020
```

## Execution status

This block corrects storage and provenance only.

Do not claim post-split executable success until:

```text
1. the current official root pool is compiled again;
2. generated profiles are regenerated/checked;
3. the candidate PR #30 overlay is compiled in an isolated pool;
4. a targeted InternationalTextType sample confirms the observable official-vs-candidate behaviour where their type restrictions differ.
```

Workflow remains manual-only.

No upstream PR was modified and no XSD content was edited by hand.
