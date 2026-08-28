#!/usr/bin/env python3
"""Reusable TimeService V1.0 / SNTP runtime-profile helpers.

The module performs deterministic classification only. It does not open a
socket, query DNS-SD, change the system clock, or require XML operations.
VDV-specific discovery rules remain separate from RFC 4330 packet semantics.
"""

from __future__ import annotations

from dataclasses import dataclass
import ipaddress

from runtime_discovery_profile import DiscoveryAdvertisement, check_dns_sd_structure
from runtime_http_profile import CheckResult


@dataclass(frozen=True)
class SntpHeader:
    li: int
    vn: int
    mode: int
    stratum: int
    originate_timestamp: int
    receive_timestamp: int
    transmit_timestamp: int
    packet_length: int


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


def parse_sntp_header(packet: bytes) -> SntpHeader:
    if len(packet) < 48:
        raise ValueError(f"SNTP/NTP packet is {len(packet)} bytes; minimum header is 48 bytes")
    first = packet[0]
    li = (first >> 6) & 0x03
    vn = (first >> 3) & 0x07
    mode = first & 0x07
    return SntpHeader(
        li=li,
        vn=vn,
        mode=mode,
        stratum=packet[1],
        originate_timestamp=int.from_bytes(packet[24:32], "big"),
        receive_timestamp=int.from_bytes(packet[32:40], "big"),
        transmit_timestamp=int.from_bytes(packet[40:48], "big"),
        packet_length=len(packet),
    )


def check_time_service_discovery(ad: DiscoveryAdvertisement) -> list[CheckResult]:
    """Validate VDV 301-2-10 V1.0 TimeService discovery metadata."""
    results = check_dns_sd_structure(ad)

    service_ok = ad.service_name.lower() == "timeservice"
    results.append(
        _result(
            "TS-V00",
            service_ok,
            "pass" if service_ok else "error",
            "vdv_normative",
            "TimeService name matches the selected VDV profile." if service_ok else "Unexpected service name for TimeService profile.",
            observed=ad.service_name,
            expected="TimeService",
        )
    )

    proto_ok = ad.protocol_label == "_ibisip_udp._udp"
    results.append(
        _result(
            "TS-V01",
            proto_ok,
            "pass" if proto_ok else "error",
            "vdv_normative",
            "TimeService uses _ibisip_udp._udp." if proto_ok else "TimeService V1.0 expects _ibisip_udp._udp.",
            observed=ad.protocol_label,
            expected="_ibisip_udp._udp",
        )
    )

    raw_server = ad.txt.get("sntp-server")
    present = raw_server is not None and raw_server != ""
    if not present:
        results.append(
            _result(
                "TS-V02",
                False,
                "error",
                "vdv_normative",
                "TimeService TXT sntp-server is missing or empty.",
                observed=raw_server,
                expected="sntp-server=<IP-address>",
            )
        )
    else:
        try:
            parsed = ipaddress.ip_address(raw_server)
        except ValueError:
            results.append(
                _result(
                    "TS-V02",
                    False,
                    "error",
                    "vdv_normative",
                    "TimeService TXT sntp-server is not an IP address.",
                    observed=raw_server,
                    expected="IPv4 or IPv6 address",
                )
            )
        else:
            results.append(
                _result(
                    "TS-V02",
                    True,
                    "pass",
                    "vdv_normative",
                    "TimeService TXT sntp-server contains a syntactically valid IP address.",
                    observed=str(parsed),
                    expected="IP address",
                )
            )

    timezone = ad.txt.get("timezone")
    if timezone is None:
        results.append(
            _result(
                "TS-V03",
                True,
                "profile_note",
                "vdv_normative",
                "No timezone TXT value is present; this classifier does not invent a hard cardinality rule not established by the current audit evidence.",
                observed=None,
                expected="preserve raw timezone value when advertised",
            )
        )
    elif timezone == "":
        results.append(
            _result(
                "TS-V03",
                False,
                "warning",
                "vdv_normative",
                "TimeService timezone TXT key is present but empty.",
                observed="",
                expected="non-empty raw profile value",
            )
        )
    else:
        results.append(
            _result(
                "TS-V03",
                True,
                "pass_with_note",
                "vdv_normative",
                "TimeService timezone TXT value is retained verbatim; no silent conversion to another timezone syntax is performed.",
                observed=timezone,
                expected="raw VDV-advertised value",
            )
        )

    return results


def cyclic_time_broadcast_expected() -> bool:
    """TimeService V1.0 explicitly says no cyclic transmission of current time is intended."""
    return False


def _parse_result(packet: bytes) -> tuple[SntpHeader | None, list[CheckResult]]:
    try:
        header = parse_sntp_header(packet)
    except ValueError as exc:
        return None, [
            _result(
                "SNTP-X00",
                False,
                "error",
                "external_normative_referenced_by_vdv",
                str(exc),
                observed=str(len(packet)),
                expected=">=48-byte NTP/SNTP header",
            )
        ]
    return header, [
        _result(
            "SNTP-X00",
            True,
            "pass",
            "external_normative_referenced_by_vdv",
            "SNTP/NTP base header is at least 48 bytes.",
            observed=str(header.packet_length),
            expected=">=48 bytes",
        )
    ]


def check_sntp_client_request(packet: bytes, *, destination_port: int) -> list[CheckResult]:
    """Check the RFC 4330 unicast-client request profile used by TimeService."""
    header, results = _parse_result(packet)
    if header is None:
        return results

    results.append(
        _result(
            "SNTP-X01-MODE-REQUEST",
            header.mode == 3,
            "pass" if header.mode == 3 else "error",
            "external_normative_referenced_by_vdv",
            "SNTP unicast client request uses mode 3." if header.mode == 3 else "SNTP unicast client request does not use client mode 3.",
            observed=str(header.mode),
            expected="3",
        )
    )
    version_ok = 1 <= header.vn <= 4
    results.append(
        _result(
            "SNTP-X01-VN-REQUEST",
            version_ok,
            "pass" if version_ok else "error",
            "external_normative_referenced_by_vdv",
            "SNTP request version is within RFC 4330's client range." if version_ok else "SNTP request version is outside RFC 4330's client range.",
            observed=str(header.vn),
            expected="1..4",
        )
    )
    results.append(
        _result(
            "SNTP-X02",
            destination_port == 123,
            "pass" if destination_port == 123 else "warning",
            "external_normative_referenced_by_vdv",
            "SNTP client request uses UDP destination port 123." if destination_port == 123 else "SNTP client request does not use the RFC 4330 SHOULD destination port 123.",
            observed=str(destination_port),
            expected="123",
        )
    )
    return results


def check_sntp_unicast_reply(
    packet: bytes,
    *,
    request_version: int,
    request_transmit_timestamp: int,
) -> list[CheckResult]:
    """Check high-value RFC 4330 reply semantics without doing clock discipline."""
    header, results = _parse_result(packet)
    if header is None:
        return results

    results.append(
        _result(
            "SNTP-X01-MODE-REPLY",
            header.mode == 4,
            "pass" if header.mode == 4 else "error",
            "external_normative_referenced_by_vdv",
            "SNTP unicast server reply uses mode 4." if header.mode == 4 else "SNTP unicast server reply does not use server mode 4.",
            observed=str(header.mode),
            expected="4",
        )
    )
    results.append(
        _result(
            "SNTP-X01-VN-REPLY",
            header.vn == request_version,
            "pass" if header.vn == request_version else "error",
            "external_normative_referenced_by_vdv",
            "SNTP reply version matches the request version." if header.vn == request_version else "SNTP reply version does not match the request version.",
            observed=str(header.vn),
            expected=str(request_version),
        )
    )
    stratum_ok = 1 <= header.stratum <= 15
    results.append(
        _result(
            "SNTP-X01-STRATUM",
            stratum_ok,
            "pass" if stratum_ok else "error",
            "external_normative_referenced_by_vdv",
            "SNTP reply carries a usable synchronized-server stratum." if stratum_ok else "SNTP reply stratum is not usable for this client profile; stratum 0 indicates unsynchronized/invalid service for client use.",
            observed=str(header.stratum),
            expected="1..15",
        )
    )
    tx_ok = header.transmit_timestamp != 0
    results.append(
        _result(
            "SNTP-X01-TX",
            tx_ok,
            "pass" if tx_ok else "error",
            "external_normative_referenced_by_vdv",
            "SNTP reply transmit timestamp is non-zero." if tx_ok else "SNTP reply transmit timestamp is zero.",
            observed=str(header.transmit_timestamp),
            expected="non-zero",
        )
    )
    originate_ok = header.originate_timestamp == request_transmit_timestamp
    results.append(
        _result(
            "SNTP-X01-ORIGINATE",
            originate_ok,
            "pass" if originate_ok else "error",
            "external_normative_referenced_by_vdv",
            "SNTP reply originate timestamp matches the request transmit timestamp." if originate_ok else "SNTP reply originate timestamp does not match the request transmit timestamp.",
            observed=str(header.originate_timestamp),
            expected=str(request_transmit_timestamp),
        )
    )
    return results


def validation_kind() -> str:
    """TimeService is a protocol/discovery profile, not an XML/XSD service."""
    return "protocol_discovery_profile"


def expected_xml_operations() -> tuple[str, ...]:
    return ()


def error_count(results: list[CheckResult]) -> int:
    return sum(1 for r in results if not r.ok and r.severity == "error")
