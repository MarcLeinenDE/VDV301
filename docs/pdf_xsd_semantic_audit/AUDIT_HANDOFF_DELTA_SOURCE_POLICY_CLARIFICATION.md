# Audit handoff delta - source policy clarification

Status: policy clarified after user instruction.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

Updated file:

```text
docs/pdf_xsd_semantic_audit/OFFICIAL_RELEASE_BACKFILL_POLICY.md
```

Important clarification:

```text
The integration working branch has two source lanes.

1. Historical official release backfill:
   Only official VDVde/VDV301 release tags may be used.
   This lane is only for historical XSDs that are missing from current master.

2. Current candidate / pull-request integration:
   Newer schema work from open PRs or explicit candidate branches may be integrated into dev/schema-integration for audit/tool development.
   This material must remain labelled candidate/integration and must not be called official unless VDV later releases or merges it.
```

Operational rule:

```text
Do not use PR/candidate material to backfill historical versions.
Do not use release-tag backfill wording for current candidate material.
Always record exact source tag, PR, branch or commit.
Keep version/dependency matrices explicit.
```

Reason:

```text
The branch should be useful for complete historical validation and for current/newer candidate validation work, but source authority must remain clear.
```
