# Official release backfill policy

Status: active policy for `dev/schema-integration`.

Purpose:

```text
Keep the integration working branch complete for historical, mixed-version VDV301 validation while preserving clear source authority and provenance.
```

Policy:

```text
If a schema file is missing from current upstream master but is present in an official VDVde/VDV301 release tag, the file may be copied into dev/schema-integration as historical official release material.
```

Strict source rule:

```text
Allowed source:
  Official VDVde/VDV301 release tags only.

Not sufficient as source:
  forks,
  open pull requests,
  closed pull requests,
  user branches,
  local candidate files,
  inferred or reconstructed schemas,
  files copied from vendor or third-party repositories.
```

Required handling:

```text
1. Record the exact source tag.
2. Keep the original filename unchanged.
3. Do not modify the copied schema while importing it.
4. Treat it as official historical release material, not as a new correction.
5. Do not include this import in an upstream correction PR unless a separate explicit PR decision is made.
6. Keep candidate/integration files clearly labelled separately from official release-tag material.
```

Rationale:

```text
Current upstream master may not contain every historical XSD needed for field validation.
Real systems may still expose older service versions.
The integration working branch therefore needs a complete version-scoped validation source set.
Official VDV release tags are acceptable authority for restoring historical XSDs into that integration branch.
```

Example already applied:

```text
IBIS-IP_CustomerInformationService_V1.0.xsd imported from VDVde/VDV301 tag VDV-301-1.0.
IBIS-IP_CustomerInformationService_V2.0.xsd imported from VDVde/VDV301 tag VDV-301-2.0.
IBIS-IP_CustomerInformationService_V2.2.xsd imported from VDVde/VDV301 tag VDV-301-2.2.
```

Tool/SDK implication:

```text
The later validator may use these imported historical official-release schemas for version-specific validation.
It must still select schemas by the requested service version and dependency pool.
No latest-wins substitution is allowed.
```

Open checklist for every future backfill:

```text
[ ] Was the source an official VDVde/VDV301 release tag?
[ ] Was the exact tag name recorded?
[ ] Was the original filename preserved?
[ ] Was the file copied unchanged?
[ ] Was the file classified as historical official release material rather than candidate material?
[ ] Was the version/dependency matrix updated?
```
