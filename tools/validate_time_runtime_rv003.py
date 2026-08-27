#!/usr/bin/env python3
"""Deterministic RV-003 evidence for TimeService V1.0 / RFC 4330 SNTP."""

from __future__ import annotations

from runtime_discovery_profile import DiscoveryAdvertisement
from runtime_time_profile import (
    check_sntp_client_request,
    check_sntp_unicast_reply,
    check_time_service_discovery,
    error_count,
    expected_xml_operations,
    parse_sntp_header,
    validation_kind,
)


def ad(
    *,
    service_name: str = "TimeService",
    protocol_label: str = "_ibisip_udp._udp",
    txt: dict[str, str] | None = None,
) -> DiscoveryAdvertisement:
    instance = f"{service_name}@clock-1"
    return DiscoveryAdvertisement(
        instance_name=instance,
        service_name=service_name,
        protocol_label=protocol_label,
        srv_present=True,
        srv_instance_name=instance,
        target="clock-1.local",
        port=123,
        txt_present=True,
        txt_instance_name=instance,
        txt={} if txt is None else txt,
        discovery_transport="mdns",
    )


def find(results, check_id: str):
    matches = [r for r in results if r.check_id == check_id]
    if len(matches) != 1:
        raise AssertionError(f"expected exactly one {check_id}, got {len(matches)}")
    return matches[0]


def expect(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label)
    print(f"OK  {label}")


def make_packet(
    *,
    li: int = 0,
    vn: int = 4,
    mode: int,
    stratum: int = 0,
    originate: int = 0,
    receive: int = 0,
    transmit: int = 0,
    length: int = 48,
) -> bytes:
    if length < 48:
        return bytes(length)
    packet = bytearray(length)
    packet[0] = ((li & 0x03) << 6) | ((vn & 0x07) << 3) | (mode & 0x07)
    packet[1] = stratum & 0xFF
    packet[24:32] = int(originate).to_bytes(8, "big")
    packet[32:40] = int(receive).to_bytes(8, "big")
    packet[40:48] = int(transmit).to_bytes(8, "big")
    return bytes(packet)


def main() -> int:
    # VDV TimeService discovery/profile layer.
    good_discovery = check_time_service_discovery(
        ad(txt={"sntp-server": "192.0.2.10", "timezone": "UTC+1"})
    )
    expect("TimeService discovery profile passes with valid server IP", error_count(good_discovery) == 0)
    expect("TimeService requires _ibisip_udp._udp", find(good_discovery, "TS-V01").ok)
    expect("sntp-server IPv4 address is accepted", find(good_discovery, "TS-V02").ok)
    expect("timezone value is retained verbatim", find(good_discovery, "TS-V03").observed == "UTC+1")

    ipv6_discovery = check_time_service_discovery(
        ad(txt={"sntp-server": "2001:db8::123", "timezone": "UTC"})
    )
    expect("sntp-server IPv6 address is accepted", find(ipv6_discovery, "TS-V02").ok)

    wrong_protocol = check_time_service_discovery(
        ad(protocol_label="_ibisip_http._tcp", txt={"sntp-server": "192.0.2.10"})
    )
    expect("wrong TimeService discovery protocol is detected", not find(wrong_protocol, "TS-V01").ok)

    missing_server = check_time_service_discovery(ad(txt={"timezone": "UTC+1"}))
    expect("missing sntp-server is detected", not find(missing_server, "TS-V02").ok)

    malformed_server = check_time_service_discovery(ad(txt={"sntp-server": "clock.example"}))
    expect("hostname in sntp-server is rejected because selected VDV profile says IP address", not find(malformed_server, "TS-V02").ok)

    no_timezone = check_time_service_discovery(ad(txt={"sntp-server": "192.0.2.10"}))
    expect("missing timezone is not promoted to an invented hard failure", find(no_timezone, "TS-V03").ok and find(no_timezone, "TS-V03").severity == "profile_note")

    wrong_service = check_time_service_discovery(
        ad(service_name="OtherService", txt={"sntp-server": "192.0.2.10"})
    )
    expect("wrong service name is detected", not find(wrong_service, "TS-V00").ok)

    # RFC 4330 request packet layer.
    request_tx = 0xE89ABCDE12345678
    request = make_packet(mode=3, vn=4, transmit=request_tx)
    parsed = parse_sntp_header(request)
    expect("SNTP header parser extracts VN=4 and mode=3", parsed.vn == 4 and parsed.mode == 3)
    expect("SNTP header parser preserves request transmit timestamp", parsed.transmit_timestamp == request_tx)

    request_checks = check_sntp_client_request(request, destination_port=123)
    expect("RFC 4330 client request profile passes", error_count(request_checks) == 0)
    expect("client request mode 3 is accepted", find(request_checks, "SNTP-X01-MODE-REQUEST").ok)
    expect("client request VN 1..4 rule accepts VN4", find(request_checks, "SNTP-X01-VN-REQUEST").ok)
    expect("UDP destination port 123 passes RFC SHOULD check", find(request_checks, "SNTP-X02").ok)

    old_version_request = make_packet(mode=3, vn=1, transmit=request_tx)
    old_version_checks = check_sntp_client_request(old_version_request, destination_port=123)
    expect("RFC 4330 request compatibility range also accepts VN1", find(old_version_checks, "SNTP-X01-VN-REQUEST").ok)

    bad_version = check_sntp_client_request(make_packet(mode=3, vn=5, transmit=request_tx), destination_port=123)
    expect("request VN outside 1..4 is rejected", not find(bad_version, "SNTP-X01-VN-REQUEST").ok)

    bad_mode = check_sntp_client_request(make_packet(mode=4, vn=4, transmit=request_tx), destination_port=123)
    expect("client request with server mode 4 is rejected", not find(bad_mode, "SNTP-X01-MODE-REQUEST").ok)

    nonstandard_port = check_sntp_client_request(request, destination_port=9123)
    expect("non-123 destination is an RFC warning rather than VDV/XSD failure", not find(nonstandard_port, "SNTP-X02").ok and find(nonstandard_port, "SNTP-X02").severity == "warning")

    short_request = check_sntp_client_request(bytes(20), destination_port=123)
    expect("short SNTP packet is rejected structurally", not find(short_request, "SNTP-X00").ok)

    # RFC 4330 unicast server-reply layer.
    reply = make_packet(
        mode=4,
        vn=4,
        stratum=2,
        originate=request_tx,
        receive=0xE89ABCDE22345678,
        transmit=0xE89ABCDE32345678,
    )
    reply_checks = check_sntp_unicast_reply(
        reply,
        request_version=4,
        request_transmit_timestamp=request_tx,
    )
    expect("RFC 4330 unicast reply profile passes", error_count(reply_checks) == 0)
    expect("server reply mode 4 is accepted", find(reply_checks, "SNTP-X01-MODE-REPLY").ok)
    expect("reply version must match request version", find(reply_checks, "SNTP-X01-VN-REPLY").ok)
    expect("usable stratum 1..15 is accepted", find(reply_checks, "SNTP-X01-STRATUM").ok)
    expect("reply transmit timestamp must be non-zero", find(reply_checks, "SNTP-X01-TX").ok)
    expect("reply originate timestamp must echo request transmit timestamp", find(reply_checks, "SNTP-X01-ORIGINATE").ok)

    wrong_origin = check_sntp_unicast_reply(
        make_packet(mode=4, vn=4, stratum=2, originate=request_tx + 1, receive=2, transmit=3),
        request_version=4,
        request_transmit_timestamp=request_tx,
    )
    expect("wrong originate timestamp is detected", not find(wrong_origin, "SNTP-X01-ORIGINATE").ok)

    stratum_zero = check_sntp_unicast_reply(
        make_packet(mode=4, vn=4, stratum=0, originate=request_tx, receive=2, transmit=3),
        request_version=4,
        request_transmit_timestamp=request_tx,
    )
    expect("stratum 0 reply is rejected for client use", not find(stratum_zero, "SNTP-X01-STRATUM").ok)

    zero_tx = check_sntp_unicast_reply(
        make_packet(mode=4, vn=4, stratum=2, originate=request_tx, receive=2, transmit=0),
        request_version=4,
        request_transmit_timestamp=request_tx,
    )
    expect("zero transmit timestamp is detected", not find(zero_tx, "SNTP-X01-TX").ok)

    reply_wrong_mode = check_sntp_unicast_reply(
        make_packet(mode=3, vn=4, stratum=2, originate=request_tx, receive=2, transmit=3),
        request_version=4,
        request_transmit_timestamp=request_tx,
    )
    expect("reply not using mode 4 is detected", not find(reply_wrong_mode, "SNTP-X01-MODE-REPLY").ok)

    reply_wrong_version = check_sntp_unicast_reply(
        make_packet(mode=4, vn=3, stratum=2, originate=request_tx, receive=2, transmit=3),
        request_version=4,
        request_transmit_timestamp=request_tx,
    )
    expect("reply VN differing from request is detected", not find(reply_wrong_version, "SNTP-X01-VN-REPLY").ok)

    # Architectural guard: TimeService is not an XML/XSD service.
    expect("TimeService routes to protocol_discovery_profile", validation_kind() == "protocol_discovery_profile")
    expect("TimeService does not synthesize XML operations", expected_xml_operations() == ())

    print("PASSED: RV-003 deterministic TimeService / RFC 4330 SNTP classifier behavior confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
