# VDV301 Prüf-SDK manifest baseline

Status: audit-derived SDK baseline v0.1.

This directory converts the completed PDF/XSD/provenance audit into machine-readable SDK rules. It is **not** an official VDV publication and it does not change any XSD.

## Files

```text
manifest_v0.1.json
  global SDK invariants, resolver dimensions, authority model and evidence references

public_result_contract_v0.1.schema.json
  stable external result contract; deliberately does not expose the SDK's internal field-by-field validation topology

routing_overrides_v0.1.json
  only facts that cannot safely be inferred from XSD filenames/includes alone:
  aliases, legacy roots, unresolved profiles, candidate gates and operation/response-context overrides
```

## Design rule

```text
XSD/protocol rule implementation may be detailed internally.
The public API returns stable check/finding identities and evidence.
It must not publish an internal `field_validated` inventory or otherwise reveal the validator's internal schema traversal as a contract.
```

A concrete validation error may naturally name the XML element/value involved when that is necessary to explain the observed failure. That is different from exposing the SDK's complete internal field/check structure.

## Resolver rule

Never resolve by `latest`.

Use the selected service identity/version plus authority and context:

```text
service name
advertised/documented service version
validation kind
authority: official | candidate | integration | unresolved
exact dependency pool / schema profile
release context only where semantically required
operation context where required
```

Candidate profiles are explicit opt-in only.

## Validation lanes

```text
xsd_profile
protocol_discovery_profile
discovery_http_profile
runtime_protocol_profile
network_diagnostic
architecture_inventory
```

The lanes may be combined into one diagnostic result, but their source authority must remain distinguishable.

## Next manifest step

Generate the ordinary service/version schema-profile inventory directly from the superbranch XSD include graph, then overlay `routing_overrides_v0.1.json`.

Do not hand-maintain normal include relationships in two places.
