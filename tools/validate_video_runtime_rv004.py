#!/usr/bin/env python3
"""Deterministic RV-004 evidence for the VideoLive RTSP/RTP boundary."""

from __future__ import annotations

from runtime_video_profile import (
    check_rtp_packet,
    check_rtsp_response_compatibility,
    check_rtsp_uri,
    error_count,
    parse_rtp_header,
    parse_rtsp_request_line,
    parse_rtsp_status_line,
    vdv_xml_start_stop_operations,
    video_validation_layers,
    xml_metadata_validity_implies_media_available,
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


def make_rtp(
    *,
    version: int = 2,
    cc: int = 0,
    marker: bool = True,
    pt: int = 96,
    sequence: int = 1234,
    timestamp: int = 0x11223344,
    ssrc: int = 0x55667788,
    csrcs: tuple[int, ...] = (),
) -> bytes:
    if len(csrcs) != cc:
        raise ValueError("csrc count mismatch in test builder")
    b0 = ((version & 0x03) << 6) | (cc & 0x0F)
    b1 = (0x80 if marker else 0) | (pt & 0x7F)
    packet = bytearray()
    packet.extend(bytes((b0, b1)))
    packet.extend(sequence.to_bytes(2, "big"))
    packet.extend(timestamp.to_bytes(4, "big"))
    packet.extend(ssrc.to_bytes(4, "big"))
    for csrc in csrcs:
        packet.extend(csrc.to_bytes(4, "big"))
    return bytes(packet)


def main() -> int:
    # VDV rtspURI / URI boundary.
    valid_uri = check_rtsp_uri("rtsp://camera.example/live/1")
    expect("ordinary rtspURI passes deterministic VDV/RTSP URI checks", error_count(valid_uri) == 0)
    expect("rtspURI host is recognized", find(valid_uri, "VIDEO-V01-HOST").ok)

    missing_uri = check_rtsp_uri(None)
    expect("missing rtspURI is detected", not find(missing_uri, "VIDEO-V01").ok)

    wrong_scheme = check_rtsp_uri("http://camera.example/live/1")
    expect("non-RTSP scheme is detected for VideoLive rtspURI", not find(wrong_scheme, "VIDEO-V01-SCHEME").ok)

    missing_host = check_rtsp_uri("rtsp:///live/1")
    expect("rtspURI without host is detected", not find(missing_host, "VIDEO-V01-HOST").ok)

    # RTSP 1.0/2.0 syntax is observed externally, not pinned by VDV.
    req10 = parse_rtsp_request_line("DESCRIBE rtsp://camera.example/live/1 RTSP/1.0")
    expect("RTSP/1.0 absolute request line parses", req10.version == "1.0" and req10.method == "DESCRIBE")

    req20 = parse_rtsp_request_line("DESCRIBE rtsp://camera.example/live/1 RTSP/2.0")
    expect("RTSP/2.0 absolute request line parses", req20.version == "2.0")

    options_star = parse_rtsp_request_line("OPTIONS * RTSP/2.0")
    expect("RTSP/2.0 OPTIONS asterisk request line parses", options_star.uri == "*")

    try:
        parse_rtsp_request_line("DESCRIBE /live/1 RTSP/1.0")
    except ValueError:
        expect("relative Request-URI is rejected by deterministic request-line parser", True)
    else:
        expect("relative Request-URI is rejected by deterministic request-line parser", False)

    resp10 = parse_rtsp_status_line("RTSP/1.0 200 OK")
    resp20 = parse_rtsp_status_line("RTSP/2.0 200 OK")
    resp505 = parse_rtsp_status_line("RTSP/1.0 505 RTSP Version Not Supported")
    expect("RTSP/1.0 response line parses", resp10.status_code == 200 and resp10.version == "1.0")
    expect("RTSP/2.0 response line parses", resp20.status_code == 200 and resp20.version == "2.0")
    expect("RTSP 505 response line parses as negotiation evidence", resp505.status_code == 505)

    compat10 = check_rtsp_response_compatibility(req10, resp10)
    expect("RTSP/1.0 request with RTSP/1.0 response passes compatibility guard", error_count(compat10) == 0)

    invalid_upgrade = check_rtsp_response_compatibility(req10, resp20)
    expect("RTSP/2.0 response to RTSP/1.0 request is rejected", not find(invalid_upgrade, "RTSP-X02").ok)

    compat20 = check_rtsp_response_compatibility(req20, resp20)
    expect("RTSP/2.0 request with RTSP/2.0 response passes", error_count(compat20) == 0)

    negotiation_note = check_rtsp_response_compatibility(req20, resp505)
    expect("RTSP/2.0 request receiving 1.0/505 is retained as negotiation evidence, not latest-wins success", find(negotiation_note, "RTSP-X02").severity == "profile_note")

    # RTP RFC 3550 fixed-header boundary.
    rtp = make_rtp()
    parsed = parse_rtp_header(rtp)
    expect("minimal 12-byte RTP header parses", parsed.header_length == 12)
    expect("RTP fields parse sequence/timestamp/SSRC", parsed.sequence_number == 1234 and parsed.timestamp == 0x11223344 and parsed.ssrc == 0x55667788)
    rtp_checks = check_rtp_packet(rtp)
    expect("RFC 3550 RTP version 2 packet passes", error_count(rtp_checks) == 0)

    wrong_version = check_rtp_packet(make_rtp(version=1))
    expect("RTP version other than 2 is rejected", not find(wrong_version, "RTP-X01").ok)

    short_packet = check_rtp_packet(bytes(8))
    expect("RTP packet shorter than fixed 12-byte header is rejected", not find(short_packet, "RTP-X01-HEADER").ok)

    csrc_packet = make_rtp(cc=2, csrcs=(0x01020304, 0x05060708))
    csrc_header = parse_rtp_header(csrc_packet)
    expect("RTP CC=2 requires and parses 20-byte header", csrc_header.header_length == 20 and csrc_header.csrc_count == 2)

    malformed_csrc = bytearray(make_rtp())
    malformed_csrc[0] = (2 << 6) | 2  # declares two CSRCs but packet remains 12 bytes
    malformed_checks = check_rtp_packet(bytes(malformed_csrc))
    expect("RTP CSRC count exceeding available bytes is rejected", not find(malformed_checks, "RTP-X01-HEADER").ok)

    # Architecture boundary guards.
    expect("video validation retains discovery/XML, RTSP control and RTP/RTCP media as separate layers", video_validation_layers() == ("vdv_discovery_and_http_xml", "rtsp_uri_and_control", "rtp_rtcp_media"))
    expect("valid XML stream metadata does not imply media availability", xml_metadata_validity_implies_media_available() is False)
    expect("VideoLive START/STOP is not synthesized as VDV XML operations", vdv_xml_start_stop_operations() == ())

    print("PASSED: RV-004 deterministic Video RTSP/RTP boundary behavior confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
