#!/usr/bin/env python3
"""EV-156: fail-closed SystemMonitoringService V2.2 finding revalidation evidence.

This validator operates on the exact byte-pinned official SMS V2.2 PDF and the
exact official VDV-301-2.2 XSD family. It does not modify repository content.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from lxml import etree

PDF_SHA256 = "996f639a81cb91ad20a8e78b6213e7c85d41ff0ec42caba4208d6c4652b140f4"
PDF_SIZE = 847416
EXPECTED_BLOBS = {
    "IBIS-IP_SystemMonitoringService_V2.2.xsd": "d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c",
    "IBIS-IP_common_V2.2.xsd": "468fee6d177e7185dbcd5d3f90cfb114e29e01ae",
    "IBIS-IP_Enumerations_V2.2.xsd": "2a23b512379b18e8f122ac1272cef8229fb86283",
}
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"OK  {message}")


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def norm(text: str) -> str:
    return " ".join(text.replace("\u2013", "-").replace("\u2014", "-").split())


def page_text(pdf: Path, page: int) -> str:
    completed = subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(pdf), "-"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return completed.stdout.decode("utf-8", errors="replace")


def pdf_page_count(pdf: Path) -> int:
    completed = subprocess.run(
        ["pdfinfo", str(pdf)],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    for line in completed.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise AssertionError("pdfinfo did not expose page count")


def validate_xml(schema: etree.XMLSchema, xml: str, expected: bool, label: str) -> None:
    doc = etree.fromstring(xml.encode("utf-8"))
    actual = schema.validate(doc)
    require(actual is expected, f"{label} -> {'valid' if expected else 'invalid'}")
    if not expected:
        print(f"    evidence: {schema.error_log.last_error}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    root = Path(args.repo_root).resolve()
    pdf = Path(args.pdf).resolve()
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    require(pdf.is_file(), f"pinned SMS PDF exists: {pdf}")
    pdf_bytes = pdf.read_bytes()
    require(pdf_bytes.startswith(b"%PDF-"), "source is a PDF")
    require(hashlib.sha256(pdf_bytes).hexdigest() == PDF_SHA256, f"official SMS V2.2 PDF SHA-256 = {PDF_SHA256}")
    require(len(pdf_bytes) == PDF_SIZE, f"official SMS V2.2 PDF size = {PDF_SIZE}")
    require(pdf_page_count(pdf) == 15, "official SMS V2.2 PDF has 15 pages")

    paths = {name: root / name for name in EXPECTED_BLOBS}
    for name, path in paths.items():
        require(path.is_file(), f"authority XSD exists: {name}")
        observed = git_blob_sha(path.read_bytes())
        require(observed == EXPECTED_BLOBS[name], f"exact official blob {name} = {observed}")

    service = paths["IBIS-IP_SystemMonitoringService_V2.2.xsd"]
    common = paths["IBIS-IP_common_V2.2.xsd"]
    enums = paths["IBIS-IP_Enumerations_V2.2.xsd"]
    service_tree = etree.parse(str(service))
    common_tree = etree.parse(str(common))
    includes = service_tree.xpath("/xs:schema/xs:include/@schemaLocation", namespaces=NS)
    require(
        includes == [common.name, enums.name],
        "SMS V2.2 includes exact Common V2.2 and Enumerations V2.2",
    )
    schema = etree.XMLSchema(service_tree)
    print(f"OK  compiled {service.name}")

    group_names = service_tree.xpath(
        "//xs:group[@name='SystemMonitoringServiceGroup']/xs:sequence/xs:element/@name",
        namespaces=NS,
    )
    require(
        group_names == [
            "SystemMonitoringService.GetDeviceStatusResponse",
            "SystemMonitoringService.GetServiceStatusResponse",
        ],
        "service-local group exposes only the two concrete Get response elements",
    )

    common_types = set(common_tree.xpath("//xs:complexType/@name", namespaces=NS))
    generic_subscription_types = [
        "SubscribeRequestStructure",
        "SubscribeResponseStructure",
        "UnsubscribeRequestStructure",
        "UnsubscribeResponseStructure",
    ]
    for type_name in generic_subscription_types:
        require(type_name in common_types, f"generic Common subscription type exists: {type_name}")

    validate_xml(
        schema,
        "<SystemMonitoringService.GetServiceStatusResponse>"
        "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>"
        "</SystemMonitoringService.GetServiceStatusResponse>",
        True,
        "exact GetServiceStatusResponse root",
    )
    validate_xml(
        schema,
        "<SystemMonitoringService.GetSystemStatusResponse>"
        "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>"
        "</SystemMonitoringService.GetSystemStatusResponse>",
        False,
        "invented GetSystemStatusResponse root",
    )

    p4 = norm(page_text(pdf, 4))
    p9 = norm(page_text(pdf, 9))
    p10 = norm(page_text(pdf, 10))
    p11 = norm(page_text(pdf, 11))
    p12 = norm(page_text(pdf, 12))
    p13 = norm(page_text(pdf, 13))

    # SMS-003: wrong-service paragraph is physically present in the official SMS PDF.
    require("This VDV document describes the SystemMonitoringService and its specific data structures." in p4,
            "page 4 establishes SystemMonitoringService as the document subject")
    require("The HTMLDisplayService provides a URL to a web server for multifunction screens." in p4,
            "page 4 visibly contains unrelated HTMLDisplayService paragraph")

    # SMS-002: PDF operation table and section/body disagree; XSD resolves executable name.
    for token in ("GetServiceStatus", "SubscribeServiceStatus", "UnsubscribeServiceStatus"):
        require(token in p9, f"page 9 operation table contains {token}")
    require("Data Structure of Operation GetSystemStatus" in p10,
            "page 10 heading names GetSystemStatus")
    require("Because of being a GetServiceStatus operation" in p10,
            "page 10 body names GetServiceStatus inside GetSystemStatus section")
    require("Data Structure of Operation SubscribeSystemStatus" in p11,
            "page 11 heading names SubscribeSystemStatus")
    require("Data Structure of Operation UnsubscribeSystemStatus" in p11,
            "page 11 heading names UnsubscribeSystemStatus")

    # SMS-001: service document itself routes subscription payloads to common VDV 301-2-1.
    require("Data Structure of Operation SubscribeDeviceStatus" in p10 and
            "For this subscription the data structures from chapters VDV 301-2-1 are used." in p10,
            "page 10 routes SubscribeDeviceStatus to generic VDV 301-2-1 structures")
    require("Data Structure of Operation UnsubscribeDeviceStatus" in p10 and
            "To terminate this subscription the structures of chapters VDV 301-2-1 are used." in p10,
            "page 10 routes UnsubscribeDeviceStatus to generic VDV 301-2-1 structures")
    require("For this subscription the data structures from chapters VDV 301-2-1 are used." in p11,
            "page 11 routes SubscribeSystemStatus subscription data to VDV 301-2-1")
    require("To terminate this subscription the structures of chapters VDV 301-2-1 are used." in p11,
            "page 11 routes UnsubscribeSystemStatus data to VDV 301-2-1")

    # SMS-004: version history says 302-2 while the same document references Base Services as 301-2-0.
    require("VDV-Schrift 302-2" in p12 and "VDV-requirements 302-2" in p12,
            "page 12 visibly cites VDV 302-2 in both language lines")
    require("VDV 301-2-0" in p13 and "Base Services" in p13 and "SystemManagementService" in p13,
            "page 13 identifies Base Services source as VDV 301-2-0")

    result = {
        "evidence_id": "EV-156",
        "result": "PASS",
        "authority": {
            "pdf_sha256": PDF_SHA256,
            "pdf_size_bytes": PDF_SIZE,
            "pdf_pages": 15,
            "official_xsd_tag": "VDV-301-2.2",
            "xsd_blobs": EXPECTED_BLOBS,
        },
        "visual_pages": [4, 9, 10, 11, 12, 13],
        "finding_results": {
            "SMS-001": {
                "recommended_terminal_state": "contextual_not_defect",
                "executable_context": "PASS",
                "reason": "Generic Subscribe/Unsubscribe structures are Common V2.2 authority and the SMS PDF explicitly routes subscription structures to VDV 301-2-1.",
            },
            "SMS-002": {
                "recommended_terminal_state": "executable_confirmed",
                "executable_result": "PASS",
                "reason": "PDF headings use SystemStatus while operation table/body and exact service XSD use ServiceStatus; GetSystemStatusResponse is rejected.",
            },
            "SMS-003": {
                "recommended_terminal_state": "context_verified",
                "visual_result": "PASS",
                "reason": "Official SMS PDF page 4 visibly contains an unrelated HTMLDisplayService paragraph.",
            },
            "SMS-004": {
                "recommended_terminal_state": "context_verified",
                "visual_result": "PASS",
                "reason": "Official PDF page 12 cites 302-2 while page 13 identifies the Base Services reference as VDV 301-2-0.",
            },
        },
        "expected_poststate_if_closed": {
            "terminal": 144,
            "pending": 48,
            "first_pending": "SUB-001",
            "next_block": "SUB",
        },
        "xsd_mutation_required": False,
        "frozen_inventory_mutation_required": False,
    }

    output = out / "ev156_result.json"
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"PASSED: EV-156 -> {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
