# Audit correction delta — HDS V2.2a RV-002 wording

Date: 2026-08-29

## Scope

This is an audit-tool diagnostic wording correction only. It does **not** change the accepted protocol labels, severity mapping, endpoint resolution, or any VDV source material.

## Trigger

The independently frozen HDS V2.2a source read (`17f036c6257c5c71b94169c02905c2e80f36b847`) showed that the publication:

- lists both `_http._tcp` and `_ibisip_http._tcp` in the current V2.2a discovery table;
- marks `_http._tcp` as `zukünftig nicht mehr empfohlen` / `deprecated`;
- says the **next service version after 2.2** will use `_ibisip_http._tcp` and delete `_http._tcp`;
- permits project-specific `_ibisip_http._tcp` use already in version 2.2 by mutual agreement;
- describes V2.2a in the foreword as carrying a note on the **future use** of `_ibisip_http._tcp`.

The prior RV-002 diagnostic text used the word `preferred` for `_ibisip_http._tcp`. That wording is directionally compatible with the transition but is stronger than the publication itself.

## Correction

`tools/runtime_discovery_profile.py` keeps its existing V2.2a behavior:

```text
_ibisip_http._tcp -> accepted
_http._tcp        -> accepted with deprecation/future-not-recommended note
other labels      -> rejected
endpoint          -> TXT url
```

Only diagnostic wording changes:

```text
preferred -> documented transition/future label
deprecated legacy wording -> deprecated/future-not-recommended wording
```

`tools/validate_discovery_runtime_rv002.py` likewise changes only the human-readable test label from `preferred` to `transition label`.

## Evidence boundary

This correction does not turn V2.2a into the future next service version. It preserves the dual-label current profile and reserves deletion of `_http._tcp` for the future service version described by the publication.

A fresh RV-002 rerun is required after this correction.
