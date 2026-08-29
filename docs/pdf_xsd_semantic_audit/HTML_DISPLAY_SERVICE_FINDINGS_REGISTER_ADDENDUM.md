# HTMLDisplayService findings register addendum

Status: supplemental register; historical first-pass closure completed for HTMLDisplayService V2.1, V2.2 and V2.2a. V2.1, V2.2 and V2.2a have now all been independently re-read and HDS-001 revalidated under the current Evidence Gate.

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

State: closed OK with note; **V2.1, V2.2 and V2.2a scopes are revalidated under the current Evidence Gate**.

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
V2.2a: TXT content + url; the current table recognises both _http._tcp (deprecated / future-not-recommended) and _ibisip_http._tcp as the transition/future label; only the future next service version after 2.2 is stated to delete _http._tcp.
```

Next action:

```text
Keep deterministic version-specific profile tests; no schema correction/backfill action.
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
## V2.2 Evidence-Gate revalidation

```text
source pin: bf62b7a8b6cfdf654181b48da2d85a805118687c7463a46fadfd32679c9b7577 / 802399 bytes / run 33266549282
visible review: pages 7-11 / render-read run 33266588436
fresh-read freeze: da2c000e82640e321d0f5379a120be75dc7a3eb2
RV-002 rerun after freeze: 33266770833 PASS
```

Result for V2.2:

```text
HDS-001 -> context_verified_ok_with_note_runtime_profile_supported_RV-002
canonical protocol: _http._tcp
TXT: content + url
content endpoint: TXT url
SRV port: no content-address meaning
SRV host: publishing device
No dedicated HDS service XSD is expected.
Later V2.2a _ibisip_http._tcp transition is compatibility context, not native V2.2 source wording.
```
## V2.2a Evidence-Gate revalidation

```text
source pin: f3da1994e719572ba1689aea2448b9533faf9e8fbe42720b9e737b98edd8b0f8 / 431875 bytes / run 33266884196
render/read run: 33266920928
fresh-read freeze: 17f036c6257c5c71b94169c02905c2e80f36b847
RV-002 wording correction: 6f0875e80c55f6c1ac6e209c484187a41dbf3d54
corrected RV-002 rerun: 33267198470 PASS
```

Result for V2.2a:

```text
HDS-001 -> context_verified_ok_with_note_runtime_profile_supported_RV-002
current labels: _http._tcp + _ibisip_http._tcp
_http._tcp: deprecated / zukünftig nicht mehr empfohlen
_ibisip_http._tcp: documented transition/future label; project-specific use already permitted in V2.2 by mutual agreement
future next service version after 2.2: delete _http._tcp and use _ibisip_http._tcp
TXT: content + url
content endpoint: TXT url
No dedicated HDS service XSD is expected.
```

The former RV-002 word `preferred` was corrected because it overstated the V2.2a publication. Test behavior did not change.

