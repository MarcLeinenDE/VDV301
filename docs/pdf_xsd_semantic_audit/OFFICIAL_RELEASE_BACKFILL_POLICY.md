# Integration branch source policy

Status: active policy for `dev/schema-integration`.

Purpose:

```text
Keep the integration working branch complete for historical, mixed-version VDV301 validation while preserving clear source authority, provenance and candidate/official separation.
```

This policy defines two different intake lanes for the integration working branch.

## 1. Historical official release backfill lane

Policy:

```text
If a schema file is missing from current upstream master but is present in an official VDVde/VDV301 release tag, the file may be copied into dev/schema-integration as historical official release material.
```

Scope of this lane:

```text
This lane is for historical completeness only.
It is used to recover older official XSDs that are needed for version-specific field validation but are no longer visible in current master.
```

Strict source rule for historical backfill:

```text
Allowed source:
  Official VDVde/VDV301 release tags only.

Not sufficient as historical backfill source:
  forks,
  open pull requests,
  closed pull requests,
  user branches,
  local candidate files,
  inferred or reconstructed schemas,
  files copied from vendor or third-party repositories.
```

Required handling for historical release backfill:

```text
1. Record the exact official VDVde/VDV301 source tag.
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

## 2. Current candidate / pull-request integration lane

Policy:

```text
For newer schema work where no official release tag exists yet, open pull requests and explicit candidate branches may be integrated into dev/schema-integration for internal audit, tool development and future validation preparation.
```

Scope of this lane:

```text
This lane is for current or future schema work that is not yet an official VDV release.
It may include our own draft/candidate PR material and other currently relevant PR/candidate material.
```

Classification rule:

```text
Files imported through this lane are candidate/integration material.
They are not official historical release material.
They are not official VDV release content unless later merged/released by VDV.
```

Required handling for PR/candidate integration:

```text
1. Record the exact source PR, branch or commit.
2. Label the file/status as candidate/integration material.
3. Keep it separate in audit wording from official release-tag material.
4. Do not call it official, even if it is useful or likely correct.
5. Do not use it to backfill historical versions.
6. Do not include it in an upstream correction PR unless a separate explicit PR decision is made.
```

Rationale:

```text
The integration working branch is allowed to be more complete than current master so that the tool/SDK can be developed against likely or proposed newer schema states.
This must not blur the authority distinction between official release-tag material and candidate material.
```

## 3. Combined tool/SDK implication

```text
The later validator may use official release-tag backfills for historical version-specific validation.
It may use candidate/integration files only when the user or tool profile explicitly selects a candidate/integration schema family.
It must still select schemas by the requested service version and dependency pool.
No latest-wins substitution is allowed.
```

## 4. Checklist for future imports

Historical release backfill checklist:

```text
[ ] Was the source an official VDVde/VDV301 release tag?
[ ] Was the exact tag name recorded?
[ ] Was the original filename preserved?
[ ] Was the file copied unchanged?
[ ] Was the file classified as historical official release material rather than candidate material?
[ ] Was the version/dependency matrix updated?
```

PR/candidate integration checklist:

```text
[ ] Was the source PR/branch/commit recorded exactly?
[ ] Was the material classified as candidate/integration?
[ ] Was it kept separate from official release-tag material in wording and matrices?
[ ] Was it avoided for historical backfill decisions?
[ ] Was the dependency/version matrix updated?
```
