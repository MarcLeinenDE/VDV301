# Audit handoff delta - official release backfill policy

Status: active policy delta.

Branch:

```text
MarcLeinenDE/VDV301 dev/schema-integration
```

New policy file:

```text
docs/pdf_xsd_semantic_audit/OFFICIAL_RELEASE_BACKFILL_POLICY.md
```

Policy summary:

```text
If current upstream master is missing an XSD that is still required for historical/mixed-version validation, the integration working branch may be completed from official VDVde/VDV301 release tags.
```

Strict rule:

```text
Only official VDVde/VDV301 release tags are allowed as backfill authority.
Forks, open PRs, closed PRs, user branches, local candidates, reconstructed schemas and third-party/vendor repositories are not enough for official-release backfill.
```

Required handling:

```text
Record the exact source tag.
Preserve the original filename.
Copy the schema unchanged.
Classify it as historical official release material.
Do not mix it into an upstream correction PR without a separate explicit PR decision.
```

Already applied example:

```text
CIS V1.0 from VDV-301-1.0.
CIS V2.0 from VDV-301-2.0.
CIS V2.2 from VDV-301-2.2.
```

Continuation note:

```text
Before importing any further missing historical XSD into dev/schema-integration, first verify the file in an official VDVde/VDV301 release tag and record that tag in the relevant audit file/matrix.
```
