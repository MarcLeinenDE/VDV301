# HTMLDisplayService findings register addendum

Status: supplemental register; historical first-pass closure completed for HTMLDisplayService V2.1, V2.2 and V2.2a. V2.1 has now also been independently re-read and HDS-001 revalidated under the current Evidence Gate; V2.2/V2.2a Deep Read revalidation remains pending.

Authority rule:

```text
Do not require an XSD for a service that is intentionally not XSD-modelled.
Do not invent a schema or latest-version alias to fill a non-gap.
Version-specific discovery/HTTP profile rules remain executable validation inputs.
```

Source audit files:

```text
docs/pdf_xsd_semantic_audit/10_html_display_service_historical_start.md
docs/pdf_xsd_semantic_audit/10a_html_display_service_protocol_profile_and_closure.md
```

## HDS-001 - no dedicated HTMLDisplayService XSD

State: closed OK with note historically; **V2.1 scope revalidated under the current Evidence Gate**. V2.2/V2.2a scopes remain pending their own Deep Reads.

Classification:

```text
mismatch_kind: service_modelling
likely_source_issue: ok_with_note
classification_confidence: high
version_scope: V2.1, V2.2, V2.2a
validation_behavior: discovery_http_profile_not_service_xsd
final_handling_bucket: no_action_note
```

Observation:

```text
The public VDV documents describe HTMLDisplayService as publishing a URL via DNS-SD and delivering display content through a web browser over HTTP/HTML.
The document states that the service does not define its own protocol.
Official VDV release-tag XSD pools checked for V2.1, V2.2 and V2.3 contain no dedicated HTMLDisplayService XSD.
Current upstream code search finds HTMLDisplayService in shared enumerations, not as a dedicated service schema.
```

Impact:

```text
The future validator must not report a missing-XSD error for HTMLDisplayService.
It must route HTMLDisplayService to a version-specific discovery/HTTP profile validator.
Shared XSD-backed metadata remains valid where used by other schema families.
```

Version profile note:

```text
V2.1: TXT content + path, protocol _http._tcp, access URL derived from host/port/path.
V2.2: TXT content + url, protocol _http._tcp, access URL comes from url.
V2.2a: TXT content + url, _http._tcp deprecated and _ibisip_http._tcp introduced/recommended for future alignment.
```

Next action:

```text
Implement profile tests later; no schema correction/backfill action.
```
## V2.1 Evidence-Gate revalidation

```text
source pin: c8aa91626bf60c8e74200200d63d44d497aeb3ab240c47039333b2c922a0e495 / 734901 bytes / run 33265498869
visible review: pages 7-10 / render run 33265541783
fresh-read freeze: cf27ca153255ce724f7db6730eb4311623b76ac0
RV-002 current rerun: 33266402138 PASS
```

Result for V2.1:

```text
HDS-001 -> context_verified_ok_with_note_runtime_profile_supported_RV-002
No dedicated service XSD is expected.
Route to discovery_http_profile.
Do not apply V2.2/V2.2a url/protocol changes to V2.1.
No live DNS/mDNS or endpoint-reachability conclusion is claimed by RV-002.
```

