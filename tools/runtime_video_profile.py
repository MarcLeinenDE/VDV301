#!/usr/bin/env python3
"""Reusable VideoLive RTSP/RTP boundary helpers for VDV301.

The module is deliberately deterministic and network-independent. VDV-specific
metadata/control expectations are kept separate from external RTSP/RTP protocol
semantics. It does not claim that a syntactically valid URI is reachable or
that an RTP stream is actually available.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from urllib.parse import urlsplit

from runtime_http_profile import CheckResult


RTSP_REQUEST_RE = re.compile(r"^(?P<method>[A-Z_]+) (?P<uri>\S+) RTSP/(?P<major>\d+)\.(?P<minor>\d+)$")
RTSP_RESPONSE_RE = re.compile(r"^RTSP/(?P<major>\d+)\.(?P<minor>\d+) (?P<status>\d{3})(?: (?P<reason>.*))?$")


@dataclass(frozen=True)
class RtspRequestLine:
    method: str
    uri: str
    version: str


@dataclass(frozen=True)
class RtspStatusLine:
    version: str
    status_code: int
    reason: str


@dataclass(frozen=True)
class RtpHeader:
    version: int
    padding: bool
    extension: bool
    csrc_count: int
    marker: bool
    payload_type: int
    sequence_number: int
    timestamp: int
    ssrc: int
    header_length: int


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


def check_rtsp_uri(raw: str | None) -> list[CheckResult]:
    """Check the VDV VideoLive rtspURI boundary without performing I/O."""
    if raw is None or raw == "":
        return [
            _result(
                "VIDEO-V01",
                False,
                "error",
                "vdv_normative",
                "VideoLive stream metadata does not provide an rtspURI.",
                observed=raw,
                expected="usable RTSP URI",
            )
        ]

    try:
        parsed = urlsplit(raw)
    except ValueError as exc:
        return [
            _result(
                "VIDEO-V01",
                False,
                "error",
                "combined_vdv_and_external_uri_semantics",
                f"rtspURI cannot be parsed: {exc}",
                observed=raw,
                expected="absolute RTSP URI with host",
            )
        ]

    results: list[CheckResult] = []
    scheme = parsed.scheme.lower()
    scheme_ok = scheme == "rtsp"
    results.append(
        _result(
            "VIDEO-V01-SCHEME",
            scheme_ok,
            "pass" if scheme_ok else "error",
            "combined_vdv_and_external_uri_semantics",
            "rtspURI uses the ordinary rtsp scheme." if scheme_ok else "VideoLive rtspURI does not use the ordinary rtsp scheme selected for the deterministic VDV profile.",
            observed=scheme or None,
            expected="rtsp",
        )
    )
    host_ok = parsed.hostname is not None
    results.append(
        _result(
            "VIDEO-V01-HOST",
            host_ok,
            "pass" if host_ok else "error",
            "combined_vdv_and_external_uri_semantics",
            "rtspURI contains a host." if host_ok else "rtspURI is missing a host.",
            observed=parsed.hostname,
            expected="host",
        )
    )
    absolute_ok = bool(parsed.scheme and parsed.netloc)
    results.append(
        _result(
            "RTSP-X01-URI",
            absolute_ok,
            "pass" if absolute_ok else "error",
            "external_normative",
            "RTSP resource identifier is an absolute URI." if absolute_ok else "RTSP request resource is not represented as an absolute URI.",
            observed=raw,
            expected="absolute URI",
        )
    )
    return results


def parse_rtsp_request_line(line: str) -> RtspRequestLine:
    match = RTSP_REQUEST_RE.fullmatch(line.strip())
    if not match:
        raise ValueError("invalid RTSP request-line shape")
    version = f"{match.group('major')}.{match.group('minor')}"
    uri = match.group("uri")
    if uri != "*":
        parsed = urlsplit(uri)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("RTSP Request-URI is not absolute")
    return RtspRequestLine(method=match.group("method"), uri=uri, version=version)


def parse_rtsp_status_line(line: str) -> RtspStatusLine:
    match = RTSP_RESPONSE_RE.fullmatch(line.strip())
    if not match:
        raise ValueError("invalid RTSP status-line shape")
    version = f"{match.group('major')}.{match.group('minor')}"
    return RtspStatusLine(
        version=version,
        status_code=int(match.group("status")),
        reason=match.group("reason") or "",
    )


def check_rtsp_version_observation(version: str) -> CheckResult:
    known = version in {"1.0", "2.0"}
    return _result(
        "RTSP-X01",
        known,
        "profile_note" if known else "warning",
        "external_normative",
        "RTSP version is recorded as an external protocol observation; the checked VDV profile does not pin one RTSP RFC version."
        if known
        else "Observed RTSP version is outside the two standards tracked by this audit.",
        observed=version,
        expected="observe 1.0 or 2.0 without latest-wins substitution",
    )


def check_rtsp_response_compatibility(request: RtspRequestLine, response: RtspStatusLine) -> list[CheckResult]:
    """Apply high-value RTSP 2.0/1.0 version-negotiation guards.

    RFC 7826 states RTSP 2.0 is not backwards compatible except basic version
    negotiation and that a server must not send an RTSP/2.0 response to an
    RTSP/1.0 request.
    """
    results = [check_rtsp_version_observation(request.version), check_rtsp_version_observation(response.version)]

    if request.version == "1.0":
        ok = response.version != "2.0"
        results.append(
            _result(
                "RTSP-X02",
                ok,
                "pass" if ok else "error",
                "external_normative",
                "RTSP response does not upgrade an RTSP/1.0 request to RTSP/2.0." if ok else "RTSP/2.0 response to an RTSP/1.0 request violates the RTSP 2.0 version-negotiation rule.",
                observed=f"request {request.version} -> response {response.version}",
                expected="no RTSP/2.0 response to RTSP/1.0 request",
            )
        )
    elif request.version == "2.0":
        if response.version == "2.0":
            results.append(
                _result(
                    "RTSP-X02",
                    True,
                    "pass",
                    "external_normative",
                    "RTSP/2.0 request received an RTSP/2.0 response.",
                    observed="2.0 -> 2.0",
                    expected="RTSP/2.0 response or explicit unsupported-version handling by a non-2.0 peer",
                )
            )
        else:
            results.append(
                _result(
                    "RTSP-X02",
                    True,
                    "profile_note",
                    "external_normative",
                    "RTSP/2.0 request did not receive an RTSP/2.0 response; retain exact status/version as negotiation evidence rather than treating RTSP 2.0 as a drop-in replacement for RTSP 1.0.",
                    observed=f"request 2.0 -> response {response.version} status {response.status_code}",
                    expected="version negotiation evidence",
                )
            )
    return results


def parse_rtp_header(packet: bytes) -> RtpHeader:
    if len(packet) < 12:
        raise ValueError(f"RTP packet is {len(packet)} bytes; fixed header requires at least 12")
    b0 = packet[0]
    b1 = packet[1]
    version = (b0 >> 6) & 0x03
    padding = bool((b0 >> 5) & 0x01)
    extension = bool((b0 >> 4) & 0x01)
    csrc_count = b0 & 0x0F
    marker = bool((b1 >> 7) & 0x01)
    payload_type = b1 & 0x7F
    header_length = 12 + (4 * csrc_count)
    if len(packet) < header_length:
        raise ValueError(
            f"RTP packet is {len(packet)} bytes but CC={csrc_count} requires at least {header_length} bytes"
        )
    return RtpHeader(
        version=version,
        padding=padding,
        extension=extension,
        csrc_count=csrc_count,
        marker=marker,
        payload_type=payload_type,
        sequence_number=int.from_bytes(packet[2:4], "big"),
        timestamp=int.from_bytes(packet[4:8], "big"),
        ssrc=int.from_bytes(packet[8:12], "big"),
        header_length=header_length,
    )


def check_rtp_packet(packet: bytes) -> list[CheckResult]:
    try:
        header = parse_rtp_header(packet)
    except ValueError as exc:
        return [
            _result(
                "RTP-X01-HEADER",
                False,
                "error",
                "external_normative",
                str(exc),
                observed=str(len(packet)),
                expected="RFC 3550 fixed header + declared CSRC list",
            )
        ]

    results = [
        _result(
            "RTP-X01-HEADER",
            True,
            "pass",
            "external_normative",
            "RTP fixed header and declared CSRC list are structurally present.",
            observed=f"header_length={header.header_length}",
            expected=">=12 + 4*CC bytes",
        ),
        _result(
            "RTP-X01",
            header.version == 2,
            "pass" if header.version == 2 else "error",
            "external_normative",
            "RTP version is 2 as defined by RFC 3550." if header.version == 2 else "RTP version is not RFC 3550 version 2.",
            observed=str(header.version),
            expected="2",
        ),
    ]
    return results


def video_validation_layers() -> tuple[str, ...]:
    return (
        "vdv_discovery_and_http_xml",
        "rtsp_uri_and_control",
        "rtp_rtcp_media",
    )


def xml_metadata_validity_implies_media_available() -> bool:
    return False


def vdv_xml_start_stop_operations() -> tuple[str, ...]:
    """VideoLive stream start/stop is delegated to RTSP, not synthesized XML."""
    return ()


def error_count(results: list[CheckResult]) -> int:
    return sum(1 for r in results if not r.ok and r.severity == "error")
