# Block 25b - HTTP/XML and Content-Type runtime profile

Runtime evidence ID: `RV-001`

Status: deterministic classifier implemented and executable-tested. No live device/network claim is made.

## Evidence run

```text
GitHub Actions run: 33112730418
head tested: 9584a07e5abd70dd34d122fbbb230dd03bb6e83b
job: 98659465458
environment: Ubuntu 24.04 / Python 3.12.14 / lxml 6.1.2
RV-001 status: 0 / PASS
```

Historical note:

```text
The executable tool was originally named tools/validate_http_runtime_ev25b.py before the EV/RV namespace split.
The filename is retained as provenance for the already executed run.
Future runtime evidence uses RV-* identifiers; runtime evidence must not be named EV-25b/EV25b.
```

The run also re-confirmed all prior XSD evidence checks with status 0.

## Reusable implementation

```text
tools/runtime_http_profile.py
tools/validate_http_runtime_ev25b.py   # historical filename; evidence ID is RV-001
```

`runtime_http_profile.py` is intentionally network-independent and separates:

```text
check ID
authority source class
severity
observed value
expected value
human-readable finding
```

This is intended as an SDK building block rather than a one-off audit script.

## Content-Type rules

### HTTP-X01 - syntax

```text
authority: external_normative
source: RFC 9110 media-type syntax
malformed Content-Type -> error
```

The parser handles case-insensitive type/subtype tokens and media-type parameters, including quoted parameter values.

### HTTP-X02 - missing Content-Type

```text
authority: external_normative
source: RFC 9110 section 8.3 SHOULD
body present + Content-Type absent -> warning
no body -> not applicable
```

This is deliberately **not** emitted as an explicit VDV hard failure because the checked VDV documents do not mandate a particular Content-Type header.

### HTTP-X03/X04/X05 - XML-capable media types

Executable classifier results:

```text
application/xml -> compatible / pass
text/xml -> compatible alias / pass_with_note
application/vnd.example.ibis+xml -> XML-capable / pass_with_note
```

For `+xml`, the classifier does not claim that the custom media type itself is VDV-defined.

### HTTP-X06 - declared non-XML media type for an XSD-backed operation

```text
example: text/plain; charset=utf-8
selected payload profile: XML/XSD
result: error
```

Authority is explicitly labelled:

```text
combined_vdv_payload_and_external_media_semantics
```

This means:

```text
VDV supplies the operation/payload expectation;
HTTP/XML standards supply media-type semantics;
the SDK must not phrase the result as if the VDV writing explicitly required `application/xml`.
```

### HTMLDisplayService guard

Executable control:

```text
Content-Type: text/html; charset=utf-8
expected_xml: false
result: informational / no XSD-XML media-type failure
```

This preserves the service-specific VDV rule that HTMLDisplayService does not define its own HTTP-content requirements and does not use an XSD payload profile.

## VDV method rules

The deterministic tests confirm the existing General-Conventions profile:

```text
request data absent -> GET valid, POST invalid
request data present -> POST valid, GET invalid
```

These results carry `vdv_normative`, not external HTTP authority.

## VDV HTTP version rule

The classifier intentionally preserves historical version scope:

```text
General Conventions V2.2 + observed HTTP/2
  -> explicit HTTP/1.1 gate not retroactively applied / not_applicable

General Conventions V2.3 + HTTP/1.1
  -> pass

General Conventions V2.3 + HTTP/2
  -> VDV profile error; expected HTTP/1.1
```

This is not a statement that HTTP/2 is generally invalid HTTP. It is a selected VDV-profile compatibility result.

## Deterministic cases passed

```text
1. case-insensitive application/xml parsing
2. quoted charset parameter parsing
3. application/xml compatibility
4. text/xml alias handling
5. +xml structured-syntax handling
6. missing Content-Type with body -> external warning
7. no-body missing Content-Type -> not applicable
8. malformed Content-Type -> external error
9. non-XML declared type for XSD-backed XML -> media/payload error
10. authority label for media/payload mismatch
11. HTMLDisplay exclusion from XSD-backed XML expectation
12. GET for payloadless VDV operation
13. reject POST for payloadless VDV operation
14. POST for request-data operation
15. reject GET for request-data operation
16. no retroactive HTTP/1.1 gate for V2.2
17. HTTP/1.1 accepted for V2.3
18. non-HTTP/1.1 rejected for V2.3 profile
```

## Sources

VDV source context:

```text
General Conventions audit / block 21
HTMLDisplayService profile / block 10a
```

External protocol sources:

```text
RFC 9110 - HTTP Semantics, section 8.3/8.3.1
RFC 7303 - XML Media Types
```

## Not yet executed

This block does not claim live checks for:

```text
actual device HTTP responses
real HTTP protocol negotiation
actual Content-Type headers from providers
charset-vs-byte-stream correctness
Content-Encoding
redirect behavior
connection timing/reachability
```

Those are runtime integration tests built on top of this classifier.

## Next

```text
RV-002 / block 25c DNS-SD/service discovery classifier
- generic RFC 6763 record semantics
- VDV ver/deviceclass/deviceID/multicast rules
- version-sensitive service labels
- HTMLDisplay V2.1/V2.2/V2.2a special endpoint construction
- explicit DNS-SD vs mDNS transport separation
```
