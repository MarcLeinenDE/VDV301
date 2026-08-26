# Schema integration superbranch status

Status: working branch for the VDV301 Tool, not an upstream pull-request branch.

Branch:

```text
dev/schema-integration
```

Purpose:

- collect the practically usable VDV301 XSD state from the official repository, open upstream pull requests, and documented V2.4 schema candidates;
- provide a stable working source for the VDV301 Tool while the official `VDVde/VDV301` repository still lacks several V2.4 schema files;
- keep review notes and validation helpers together with the integration state.

Do not open this branch as a pull request against `VDVde/VDV301`. It intentionally contains working documentation and helper scripts in addition to schema files.

## Included schema candidate areas

Currently integrated against the upstream master baseline used by this fork:

```text
IBIS-IP_common_V2.4.xsd
IBIS-IP_Enumerations_V2.4.xsd
IBIS-IP_TicketValidationService_V2.4.xsd include alignment
IBIS-IP_DeviceManagementService_V2.4.xsd
IBIS-IP_DeviceManagementService_V2.3.xsd
IBIS-IP_TicketValidationService_V2.3.xsd
IBIS-IP_CustomerInformationService_V2.4.xsd
IBIS-IP_AnalogRadioService_V2.4.xsd
IBIS-IP_VideoRecordingService_V2.4.xsd
```

Additional isolated upstream fix integrated for the working schema set:

```text
IBIS-IP_common_V2.3.xsd InternationalTextType type fix from VDVde/VDV301#30
```

## Upstream PR relationship

- `VDVde/VDV301#31` is the clean draft PR for the DMS V2.4 schema candidate.
- `VDVde/VDV301#30` is an isolated V2.3 common-structure fix and has been applied to this working branch.
- `VDVde/VDV301#29` largely represents the broader V2.4 candidate aggregation; its visible file set is already represented in this superbranch, but its own PR body states that no comparison with the VDV301 documents was made.
- `VDVde/VDV301#27` contributes AnalogRadioService V2.4 and VideoRecordingService V2.4; those files are represented here, but the include-version suggestions in the PR discussion still need local validation in the final schema pool.
- `VDVde/VDV301#25` contributes CustomerInformationService V2.4, DeviceManagementService V2.3 and common V2.4; those areas are represented here, but the PR is broad and still needs individual source/diff review.
- This superbranch may contain broader material than PR #31 and must therefore remain separate.

## Validation helpers

The branch includes local helper scripts under `tools/` for derivation and XSD-pool validation. These tools are intended for local review and for the VDV301 Tool workflow; they are not intended to be submitted in a schema-only upstream PR.

## Current caution

This branch is an integration candidate, not an official VDV release. For user-facing Tool output, label it as an integrated working schema set and keep the official VDV master plus open PR provenance visible.
