# AUDIT HANDOFF DELTA - HTMLDisplayService 10A

Status: supplemental delta after HTMLDisplayService historical first-pass closure.

Branch:

```text
dev/schema-integration
```

Starting head for this block:

```text
1e4e690a25dff05dd6b75ba33173427b558340f8
```

New files:

```text
docs/pdf_xsd_semantic_audit/10_html_display_service_historical_start.md
docs/pdf_xsd_semantic_audit/10a_html_display_service_protocol_profile_and_closure.md
docs/pdf_xsd_semantic_audit/HTML_DISPLAY_SERVICE_FINDINGS_REGISTER_ADDENDUM.md
docs/pdf_xsd_semantic_audit/generated/html_display_service_historical_scope_matrix.csv
```

Result:

```text
HTMLDisplayService V2.1/V2.2/V2.2a first-pass historical audit closed.
No dedicated service XSD exists in the checked official release-tag pools.
This absence is classified as intentional non-XSD service modelling, not a schema/provenance gap.
No historical XSD backfill is required.
No XSD was added or modified.
```

HDS-001:

```text
No dedicated HTMLDisplayService XSD.
Classification: ok_with_note / service_modelling.
Validator behaviour: route to discovery_http_profile, not service-XSD compiler.
```

Version routing facts:

```text
V2.1 -> _http._tcp + TXT content/path + derived host:port/path URL
V2.2 -> _http._tcp + TXT content/url + direct URL
V2.2a -> content/url + _http._tcp deprecated + _ibisip_http._tcp introduced/recommended
```

Important HTTP-content note:

```text
VDV 301-2-17 itself intentionally does not define detailed HTTP-content requirements.
Any Content-Type or other HTTP compliance checks in the later SDK must be sourced separately from General Conventions and/or applicable HTTP standards, not invented from HTMLDisplayService.
```

Next planned audit block:

```text
docs/pdf_xsd_semantic_audit/11_system_monitoring_service_historical_start.md
```
