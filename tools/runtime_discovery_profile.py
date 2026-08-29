#!/usr/bin/env python3
"""Reusable DNS-SD / VDV301 discovery profile classifier.

The module validates an already-observed advertisement. It deliberately does
not perform DNS or mDNS queries itself, so discovery transport and record/profile
semantics remain separable.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlunsplit

from runtime_http_profile import CheckResult


@dataclass(frozen=True)
class DiscoveryAdvertisement:
    instance_name: str
    service_name: str
    protocol_label: str
    srv_present: bool
    srv_instance_name: str | None
    target: str | None
    port: int | None
    txt_present: bool
    txt_instance_name: str | None
    txt: dict[str, str]
    discovery_transport: str = "unknown"  # unknown | unicast_dns | mdns


def _result(
    check_id: str,
    ok: bool,
    severity: str,
    authority: str,
    message: str,
    *,
    observed: str | None = None,
    expected: str | None = None,
) -> CheckResult:
    return CheckResult(check_id, ok, severity, authority, message, observed, expected)


def check_dns_sd_structure(ad: DiscoveryAdvertisement) -> list[CheckResult]:
    """Generic RFC 6763 record-level checks for a parsed service instance."""
    results: list[CheckResult] = []

    results.append(
        _result(
            "DNS-X02-SRV",
            ad.srv_present,
            "pass" if ad.srv_present else "error",
            "external_normative",
            "DNS-SD service instance has an SRV record." if ad.srv_present else "DNS-SD service instance is missing its SRV record.",
            expected="SRV record with the service-instance name",
        )
    )
    results.append(
        _result(
            "DNS-X03",
            ad.txt_present,
            "pass" if ad.txt_present else "error",
            "external_normative",
            "DNS-SD service instance has a TXT record." if ad.txt_present else "DNS-SD service instance is missing its mandatory TXT record.",
            expected="TXT record, even if empty",
        )
    )

    if ad.srv_present:
        same = ad.srv_instance_name == ad.instance_name
        results.append(
            _result(
                "DNS-X02-SRV-NAME",
                same,
                "pass" if same else "error",
                "external_normative",
                "SRV record name matches the discovered service instance." if same else "SRV record name does not match the discovered service instance.",
                observed=ad.srv_instance_name,
                expected=ad.instance_name,
            )
        )
        endpoint_complete = bool(ad.target) and isinstance(ad.port, int) and 0 <= ad.port <= 65535
        results.append(
            _result(
                "DNS-X04",
                endpoint_complete,
                "pass" if endpoint_complete else "error",
                "external_normative",
                "SRV supplies a target host and valid port." if endpoint_complete else "SRV does not supply a usable target host and port.",
                observed=f"{ad.target}:{ad.port}",
                expected="target host + port 0..65535",
            )
        )

    if ad.txt_present:
        same = ad.txt_instance_name == ad.instance_name
        results.append(
            _result(
                "DNS-X02-TXT-NAME",
                same,
                "pass" if same else "error",
                "external_normative",
                "TXT record name matches the discovered service instance." if same else "TXT record name does not match the discovered service instance.",
                observed=ad.txt_instance_name,
                expected=ad.instance_name,
            )
        )

    transport_known = ad.discovery_transport in {"unicast_dns", "mdns", "unknown"}
    results.append(
        _result(
            "DNS-X06",
            transport_known,
            "informational" if transport_known else "warning",
            "external_normative",
            "DNS-SD record semantics are evaluated independently of unicast-DNS vs mDNS transport.",
            observed=ad.discovery_transport,
            expected="unicast_dns, mdns, or unknown",
        )
    )
    return results


def _required_txt(ad: DiscoveryAdvertisement, key: str, check_id: str) -> CheckResult:
    present = key in ad.txt and ad.txt[key] != ""
    return _result(
        check_id,
        present,
        "pass" if present else "error",
        "vdv_normative",
        f"VDV TXT key {key!r} is present." if present else f"VDV TXT key {key!r} is missing or empty.",
        observed=ad.txt.get(key),
        expected=key,
    )


def check_general_vdv_discovery(
    ad: DiscoveryAdvertisement,
    *,
    general_conventions_version: str,
    transport_family: str,
) -> list[CheckResult]:
    """Check General-Conventions V2.2+ discovery metadata.

    transport_family is 'http' or 'udp'. This describes the selected VDV
    service profile, not whether DNS-SD itself was obtained via mDNS.
    """
    results = check_dns_sd_structure(ad)
    if tuple(int(p) for p in general_conventions_version.split(".")) < (2, 2):
        results.append(
            _result(
                "DISC-V00",
                True,
                "not_applicable",
                "vdv_normative",
                "This helper only applies the established General-Conventions V2.2+ discovery-key profile.",
                observed=general_conventions_version,
            )
        )
        return results

    results.extend(
        [
            _required_txt(ad, "ver", "DISC-V01"),
            _required_txt(ad, "deviceclass", "DISC-V02"),
            _required_txt(ad, "deviceID", "DISC-V03"),
        ]
    )

    expected_protocol = "_ibisip_http._tcp" if transport_family == "http" else "_ibisip_udp._udp"
    protocol_ok = ad.protocol_label == expected_protocol
    results.append(
        _result(
            "DISC-V07",
            protocol_ok,
            "pass" if protocol_ok else "error",
            "vdv_normative",
            "VDV protocol label matches the selected service transport family." if protocol_ok else "VDV protocol label does not match the selected service transport family.",
            observed=ad.protocol_label,
            expected=expected_protocol,
        )
    )

    if transport_family == "udp":
        results.append(_required_txt(ad, "multicast", "DISC-V04"))
    return results


def _join_http_path(target: str, port: int, path: str) -> str:
    normalized_path = path if path.startswith("/") else f"/{path}"
    netloc = target if port == 80 else f"{target}:{port}"
    return urlunsplit(("http", netloc, normalized_path, "", ""))


def check_html_display(ad: DiscoveryAdvertisement, *, version: str) -> tuple[list[CheckResult], str | None]:
    """Validate HDS V2.1/V2.2/V2.2a discovery and resolve the access endpoint."""
    results = check_dns_sd_structure(ad)
    endpoint: str | None = None

    service_ok = ad.service_name.lower() == "htmldisplayservice"
    results.append(
        _result(
            "HDS-SERVICE",
            service_ok,
            "pass" if service_ok else "error",
            "vdv_normative",
            "HTMLDisplayService name matches profile." if service_ok else "Unexpected service name for HTMLDisplayService profile.",
            observed=ad.service_name,
            expected="HtmlDisplayService",
        )
    )

    if version == "2.1":
        proto_ok = ad.protocol_label == "_http._tcp"
        results.append(_result("HDS-V01-PROTO", proto_ok, "pass" if proto_ok else "error", "vdv_normative", "V2.1 uses _http._tcp." if proto_ok else "V2.1 expects _http._tcp.", observed=ad.protocol_label, expected="_http._tcp"))
        results.append(_required_txt(ad, "content", "HDS-V01-CONTENT"))
        results.append(_required_txt(ad, "path", "HDS-V01-PATH"))
        if ad.target and isinstance(ad.port, int) and "path" in ad.txt and ad.txt.get("path"):
            endpoint = _join_http_path(ad.target, ad.port, ad.txt["path"])

    elif version == "2.2":
        proto_ok = ad.protocol_label in {"_http._tcp", "_ibisip_http._tcp"}
        severity = "pass" if ad.protocol_label == "_http._tcp" else "pass_with_note"
        message = "V2.2 uses _http._tcp." if ad.protocol_label == "_http._tcp" else "_ibisip_http._tcp is accepted only as the later V2.2a-documented project-agreement transition for V2.2."
        results.append(_result("HDS-V02-PROTO", proto_ok, severity if proto_ok else "error", "vdv_normative", message if proto_ok else "V2.2 protocol label is not a documented HDS profile label.", observed=ad.protocol_label, expected="_http._tcp (or project-agreed _ibisip_http._tcp transition)"))
        results.append(_required_txt(ad, "content", "HDS-V02-CONTENT"))
        results.append(_required_txt(ad, "url", "HDS-V02-URL"))
        endpoint = ad.txt.get("url") or None
        results.append(_result("HDS-X01", True, "profile_note", "vdv_profile_exception_or_specialization", "V2.2 access uses TXT url; the SRV port is retained as discovery metadata but is not used to construct the content endpoint.", observed=endpoint))

    elif version == "2.2a":
        proto_ok = ad.protocol_label in {"_ibisip_http._tcp", "_http._tcp"}
        deprecated = ad.protocol_label == "_http._tcp"
        results.append(
            _result(
                "HDS-V03-PROTO",
                proto_ok,
                "pass_with_note" if deprecated else ("pass" if proto_ok else "error"),
                "vdv_normative",
                "V2.2a accepts _http._tcp but marks it deprecated/future-not-recommended." if deprecated else ("V2.2a recognises _ibisip_http._tcp as the documented transition/future protocol label." if proto_ok else "V2.2a protocol label is not documented for HDS."),
                observed=ad.protocol_label,
                expected="_ibisip_http._tcp transition/future label or _http._tcp (deprecated/future-not-recommended)",
            )
        )
        results.append(_required_txt(ad, "content", "HDS-V03-CONTENT"))
        results.append(_required_txt(ad, "url", "HDS-V03-URL"))
        endpoint = ad.txt.get("url") or None
        results.append(_result("HDS-X01", True, "profile_note", "vdv_profile_exception_or_specialization", "V2.2a access follows TXT url rather than reconstructing the resource URL from SRV host/port.", observed=endpoint))
    else:
        results.append(_result("HDS-VERSION", False, "error", "profile_context", "Unsupported HTMLDisplayService profile version.", observed=version, expected="2.1, 2.2, or 2.2a"))

    return results, endpoint


def error_count(results: list[CheckResult]) -> int:
    return sum(1 for r in results if not r.ok and r.severity == "error")
