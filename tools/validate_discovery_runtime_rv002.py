#!/usr/bin/env python3
"""Deterministic RV-002 tests for DNS-SD / VDV301 discovery profiles.

No network I/O is performed. The script validates already-observed/parsed
advertisement objects against the reusable discovery classifier.
"""

from __future__ import annotations

from runtime_discovery_profile import (
    DiscoveryAdvertisement,
    check_dns_sd_structure,
    check_general_vdv_discovery,
    check_html_display,
    error_count,
)


def ad(
    *,
    instance_name: str = "CustomerInformationService@device-1",
    service_name: str = "CustomerInformationService",
    protocol_label: str = "_ibisip_http._tcp",
    target: str | None = "device-1.local",
    port: int | None = 8080,
    txt: dict[str, str] | None = None,
    srv_present: bool = True,
    txt_present: bool = True,
    srv_instance_name: str | None = None,
    txt_instance_name: str | None = None,
    discovery_transport: str = "mdns",
) -> DiscoveryAdvertisement:
    return DiscoveryAdvertisement(
        instance_name=instance_name,
        service_name=service_name,
        protocol_label=protocol_label,
        srv_present=srv_present,
        srv_instance_name=instance_name if srv_instance_name is None else srv_instance_name,
        target=target,
        port=port,
        txt_present=txt_present,
        txt_instance_name=instance_name if txt_instance_name is None else txt_instance_name,
        txt={} if txt is None else txt,
        discovery_transport=discovery_transport,
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


def main() -> int:
    # Generic RFC 6763 record semantics.
    base = ad(txt={"ver": "2.2", "deviceclass": "OnBoardUnit", "deviceID": "1"})
    generic = check_dns_sd_structure(base)
    expect("generic DNS-SD SRV/TXT structure passes", error_count(generic) == 0)
    expect("mDNS is accepted as one DNS-SD transport", find(generic, "DNS-X06").ok)

    unicast = check_dns_sd_structure(ad(txt={}, discovery_transport="unicast_dns"))
    expect("unicast DNS is also accepted for DNS-SD semantics", find(unicast, "DNS-X06").ok)

    missing_txt = check_dns_sd_structure(ad(txt_present=False, txt={}))
    expect("missing TXT record is an RFC 6763 error", not find(missing_txt, "DNS-X03").ok)

    wrong_names = check_dns_sd_structure(
        ad(
            txt={},
            srv_instance_name="other-instance",
            txt_instance_name="another-instance",
        )
    )
    expect("SRV instance-name mismatch is detected", not find(wrong_names, "DNS-X02-SRV-NAME").ok)
    expect("TXT instance-name mismatch is detected", not find(wrong_names, "DNS-X02-TXT-NAME").ok)

    bad_endpoint = check_dns_sd_structure(ad(txt={}, target=None, port=70000))
    expect("invalid/missing SRV endpoint is detected", not find(bad_endpoint, "DNS-X04").ok)

    # VDV General Conventions V2.2+ profile.
    http_ok = check_general_vdv_discovery(
        base,
        general_conventions_version="2.2",
        transport_family="http",
    )
    expect("GC V2.2 HTTP discovery profile passes with ver/deviceclass/deviceID", error_count(http_ok) == 0)
    expect("HTTP profile requires _ibisip_http._tcp", find(http_ok, "DISC-V07").ok)

    missing_device_id = check_general_vdv_discovery(
        ad(txt={"ver": "2.2", "deviceclass": "OnBoardUnit"}),
        general_conventions_version="2.2",
        transport_family="http",
    )
    expect("missing deviceID is a VDV profile error", not find(missing_device_id, "DISC-V03").ok)

    udp_ok = check_general_vdv_discovery(
        ad(
            service_name="GNSSLocationService",
            protocol_label="_ibisip_udp._udp",
            port=9000,
            txt={
                "ver": "1.0",
                "deviceclass": "OnBoardUnit",
                "deviceID": "1",
                "multicast": "239.1.2.3",
            },
        ),
        general_conventions_version="2.2",
        transport_family="udp",
    )
    expect("GC V2.2 UDP discovery profile passes with multicast", error_count(udp_ok) == 0)
    expect("UDP multicast TXT is required and present", find(udp_ok, "DISC-V04").ok)

    udp_missing_multicast = check_general_vdv_discovery(
        ad(
            service_name="GNSSLocationService",
            protocol_label="_ibisip_udp._udp",
            txt={"ver": "1.0", "deviceclass": "OnBoardUnit", "deviceID": "1"},
        ),
        general_conventions_version="2.2",
        transport_family="udp",
    )
    expect("missing UDP multicast TXT is a VDV profile error", not find(udp_missing_multicast, "DISC-V04").ok)

    wrong_protocol = check_general_vdv_discovery(
        ad(
            protocol_label="_ibisip_udp._udp",
            txt={"ver": "2.2", "deviceclass": "OnBoardUnit", "deviceID": "1", "multicast": "239.1.2.3"},
        ),
        general_conventions_version="2.2",
        transport_family="http",
    )
    expect("HTTP/UDP VDV protocol-label mismatch is detected", not find(wrong_protocol, "DISC-V07").ok)

    pre22 = check_general_vdv_discovery(
        ad(protocol_label="_http._tcp", txt={}),
        general_conventions_version="2.1",
        transport_family="http",
    )
    expect("V2.2+ TXT-key rules are not retroactively applied to GC V2.1", find(pre22, "DISC-V00").severity == "not_applicable")
    expect("pre-V2.2 helper does not emit DISC-V01", not any(r.check_id == "DISC-V01" for r in pre22))

    # HTMLDisplayService version-specific discovery/endpoint handling.
    h21, endpoint21 = check_html_display(
        ad(
            instance_name="HtmlDisplayService@display-1",
            service_name="HtmlDisplayService",
            protocol_label="_http._tcp",
            target="display-1.local",
            port=8080,
            txt={"content": "MFD", "path": "/screen/index.html"},
        ),
        version="2.1",
    )
    expect("HDS V2.1 profile passes", error_count(h21) == 0)
    expect("HDS V2.1 endpoint is built from SRV target/port plus TXT path", endpoint21 == "http://display-1.local:8080/screen/index.html")

    h22, endpoint22 = check_html_display(
        ad(
            instance_name="HtmlDisplayService@display-2",
            service_name="HtmlDisplayService",
            protocol_label="_http._tcp",
            target="ignored-for-resource.example",
            port=6553,
            txt={"content": "MFD", "url": "http://content.example:8088/ui"},
        ),
        version="2.2",
    )
    expect("HDS V2.2 canonical _http._tcp profile passes", error_count(h22) == 0)
    expect("HDS V2.2 endpoint comes from TXT url, not SRV host/port reconstruction", endpoint22 == "http://content.example:8088/ui")
    expect("HDS V2.2 records service-specific DNS-SD specialization", find(h22, "HDS-X01").authority == "vdv_profile_exception_or_specialization")

    h22_transition, _ = check_html_display(
        ad(
            instance_name="HtmlDisplayService@display-2",
            service_name="HtmlDisplayService",
            protocol_label="_ibisip_http._tcp",
            txt={"content": "MFD", "url": "http://content.example/ui"},
        ),
        version="2.2",
    )
    expect("HDS V2.2 _ibisip_http._tcp transition is accepted only with note", find(h22_transition, "HDS-V02-PROTO").severity == "pass_with_note")

    h22a, endpoint22a = check_html_display(
        ad(
            instance_name="HtmlDisplayService@display-3",
            service_name="HtmlDisplayService",
            protocol_label="_ibisip_http._tcp",
            txt={"content": "Routepath", "url": "http://content.example/route"},
        ),
        version="2.2a",
    )
    expect("HDS V2.2a _ibisip_http._tcp transition label passes", error_count(h22a) == 0)
    expect("HDS V2.2a endpoint follows TXT url", endpoint22a == "http://content.example/route")

    h22a_legacy, _ = check_html_display(
        ad(
            instance_name="HtmlDisplayService@display-3",
            service_name="HtmlDisplayService",
            protocol_label="_http._tcp",
            txt={"content": "Routepath", "url": "http://content.example/route"},
        ),
        version="2.2a",
    )
    expect("HDS V2.2a legacy _http._tcp is accepted but deprecated", find(h22a_legacy, "HDS-V03-PROTO").severity == "pass_with_note")

    h_missing_url, endpoint_missing = check_html_display(
        ad(
            instance_name="HtmlDisplayService@display-4",
            service_name="HtmlDisplayService",
            protocol_label="_http._tcp",
            txt={"content": "MFD"},
        ),
        version="2.2",
    )
    expect("HDS V2.2 missing url is detected", not find(h_missing_url, "HDS-V02-URL").ok)
    expect("HDS V2.2 missing url yields no resolved content endpoint", endpoint_missing is None)

    wrong_service, _ = check_html_display(
        ad(
            instance_name="OtherService@device",
            service_name="OtherService",
            protocol_label="_http._tcp",
            txt={"content": "MFD", "url": "http://content.example/ui"},
        ),
        version="2.2",
    )
    expect("wrong service name is detected by HDS profile", not find(wrong_service, "HDS-SERVICE").ok)

    print("PASSED: RV-002 deterministic DNS-SD / VDV discovery classifier behavior confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
