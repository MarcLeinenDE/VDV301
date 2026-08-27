#!/usr/bin/env python3
"""Deterministic tests for block 25b HTTP/XML runtime classification.

These tests prove the classifier's authority/severity behavior. They do not
perform live HTTP requests and therefore make no claim about any device.
"""

from __future__ import annotations

from runtime_http_profile import (
    check_content_type,
    check_vdv_http_method,
    check_vdv_http_version,
    parse_content_type,
)


def require(condition: bool, label: str) -> int:
    if condition:
        print(f"OK  {label}")
        return 0
    print(f"ERR {label}")
    return 1


def result_by_id(results, check_id: str):
    matches = [result for result in results if result.check_id == check_id]
    if len(matches) != 1:
        raise AssertionError(f"expected one {check_id}, got {len(matches)}")
    return matches[0]


def main() -> int:
    failures = 0

    media = parse_content_type('Application/XML; Charset="utf-8"')
    failures += require(media.normalized == "application/xml", "Content-Type type/subtype normalizes case-insensitively")
    failures += require(media.parameters == (("charset", "utf-8"),), "quoted charset parameter parses")

    app_xml = check_content_type("application/xml", body_present=True, expected_xml=True)
    failures += require(result_by_id(app_xml, "HTTP-X03").ok, "application/xml accepted for XSD-backed XML payload")

    text_xml = check_content_type("text/xml", body_present=True, expected_xml=True)
    r = result_by_id(text_xml, "HTTP-X04")
    failures += require(r.ok and r.severity == "pass_with_note", "text/xml accepted as RFC 7303 alias with note")

    suffix_xml = check_content_type("application/vnd.example.ibis+xml", body_present=True, expected_xml=True)
    r = result_by_id(suffix_xml, "HTTP-X05")
    failures += require(r.ok and r.severity == "pass_with_note", "+xml media type recognized without claiming VDV-defined type")

    missing = check_content_type(None, body_present=True, expected_xml=True)
    r = result_by_id(missing, "HTTP-X02")
    failures += require((not r.ok) and r.severity == "warning" and r.authority == "external_normative", "missing Content-Type is external RFC warning, not VDV hard failure")

    no_body = check_content_type(None, body_present=False, expected_xml=True)
    r = result_by_id(no_body, "HTTP-X02")
    failures += require(r.ok and r.severity == "not_applicable", "no-body message does not trigger missing Content-Type warning")

    malformed = check_content_type("application/xml; charset", body_present=True, expected_xml=True)
    r = result_by_id(malformed, "HTTP-X01")
    failures += require((not r.ok) and r.severity == "error", "malformed Content-Type classified as external protocol error")

    non_xml = check_content_type("text/plain; charset=utf-8", body_present=True, expected_xml=True)
    r = result_by_id(non_xml, "HTTP-X06")
    failures += require((not r.ok) and r.severity == "error", "declared non-XML type rejected for XSD-backed VDV XML payload")
    failures += require(r.authority == "combined_vdv_payload_and_external_media_semantics", "media/payload mismatch carries combined authority label")

    hds = check_content_type("text/html; charset=utf-8", body_present=True, expected_xml=False)
    r = result_by_id(hds, "HTTP-X-MEDIA")
    failures += require(r.ok and r.severity == "informational", "HTMLDisplay profile is not forced through XSD-backed XML media expectation")

    method = check_vdv_http_method("GET", request_data_present=False)
    failures += require(method.ok and method.check_id == "HTTP-V03", "payloadless VDV operation accepts GET")
    method = check_vdv_http_method("POST", request_data_present=False)
    failures += require((not method.ok) and method.expected == "GET", "payloadless VDV operation rejects POST")
    method = check_vdv_http_method("POST", request_data_present=True)
    failures += require(method.ok and method.check_id == "HTTP-V02", "VDV operation with request data accepts POST")
    method = check_vdv_http_method("GET", request_data_present=True)
    failures += require((not method.ok) and method.expected == "POST", "VDV operation with request data rejects GET")

    http_v22 = check_vdv_http_version("HTTP/2", general_conventions_version="2.2")
    failures += require(http_v22.ok and http_v22.severity == "not_applicable", "HTTP/1.1 pin is not retroactively applied to GC V2.2")
    http_v23 = check_vdv_http_version("HTTP/1.1", general_conventions_version="2.3")
    failures += require(http_v23.ok, "GC V2.3 accepts explicitly required HTTP/1.1")
    http_v23_bad = check_vdv_http_version("HTTP/2", general_conventions_version="2.3")
    failures += require((not http_v23_bad.ok) and http_v23_bad.expected == "1.1", "GC V2.3 rejects non-HTTP/1.1 profile")

    if failures:
        print(f"FAILED: {failures} block-25b deterministic check(s) failed")
        return 1
    print("PASSED: block 25b HTTP/XML runtime classifier behavior confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
