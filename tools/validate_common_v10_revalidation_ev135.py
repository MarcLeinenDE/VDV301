#!/usr/bin/env python3
"""EV-135 fail-closed revalidation evidence for COMMON V1.0 DRCOM10-001..007."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from lxml import etree

PDF = Path("local_sources/vdv_pdfs/COMMON_V1.0.pdf")
FROZEN = Path("audit_registry/finding_inventory_frozen_2026-09-03.json")
REGISTRY = Path("audit_registry/finding_revalidation_registry_v0.1.json")
DELTA = Path("audit_registry/deep_read_findings_delta_common_v10_2026-08-30.json")
DEEP_READ = Path("docs/pdf_xsd_semantic_audit/deep_read/COMMON_V1.0.md")
COMMON = Path("IBIS-IP_common_V1.0.xsd")
ENUMS = Path("IBIS-IP_Enumerations_V1.0.xsd")
OUT_DIR = Path(os.environ.get("EV135_OUTPUT_DIR", "artifacts/ev135"))

EXPECTED_PDF_SHA256 = "a4d53163e5e3b2690887ac5e060d982c1135e1e5c2d6e753c9a151441167a0cf"
EXPECTED_PDF_SIZE = 892769
EXPECTED_FROZEN_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
EXPECTED_DELTA_BLOB = "da56c957f654c47207908f9a6e0808ecf9928ea1"
EXPECTED_COMMON_BLOB = "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c"
EXPECTED_ENUM_BLOB = "a9bea5bc73003ed91ded8519db06c32c4067831d"
FINDINGS = [f"DRCOM10-{i:03d}" for i in range(1, 8)]
TERMINAL_RECOMMENDATIONS = {
    "DRCOM10-001": "executable_confirmed",
    "DRCOM10-002": "executable_confirmed",
    "DRCOM10-003": "executable_confirmed",
    "DRCOM10-004": "executable_confirmed",
    "DRCOM10-005": "executable_confirmed",
    "DRCOM10-006": "executable_confirmed",
    "DRCOM10-007": "context_verified",
}
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], text=True).strip()


def sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
            size += len(chunk)
    return h.hexdigest(), size


def norm(text: str) -> str:
    return " ".join(text.replace("\u00ad", "").replace("–", "-").split())


def page_count() -> int:
    out = subprocess.check_output(["pdfinfo", str(PDF)], text=True, errors="replace")
    m = re.search(r"^Pages:\s+(\d+)\s*$", out, re.MULTILINE)
    require(m is not None, "pdfinfo page count missing")
    return int(m.group(1))


def page_text(page: int) -> str:
    return norm(subprocess.check_output(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(PDF), "-"],
        text=True,
        errors="replace",
    ))


def all_pages() -> dict[int, str]:
    return {p: page_text(p) for p in range(1, page_count() + 1)}


def pages_any(pages: dict[int, str], needles: tuple[str, ...]) -> list[int]:
    return [p for p, text in pages.items() if any(n in text for n in needles)]


def pages_all(pages: dict[int, str], needles: tuple[str, ...]) -> list[int]:
    return [p for p, text in pages.items() if all(n in text for n in needles)]


def validate(schema: etree.XMLSchema, xml: str) -> tuple[bool, str]:
    doc = etree.fromstring(xml.encode())
    ok = bool(schema.validate(doc))
    if ok:
        return True, "OK"
    last = schema.error_log.last_error
    return False, str(last) if last is not None else "validation failed"


def probe(schema: etree.XMLSchema, label: str, xml: str, expected: bool) -> None:
    ok, detail = validate(schema, xml)
    if ok != expected:
        fail(f"{label}: got {'VALID' if ok else 'INVALID'}, expected {'VALID' if expected else 'INVALID'}: {detail}")
    print(f"OK {label}: {'VALID' if ok else 'INVALID'} as expected")


def compile_harness() -> etree.XMLSchema:
    text = f'''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="{XS}" elementFormDefault="qualified" attributeFormDefault="unqualified">
  <xs:include schemaLocation="IBIS-IP_common_V1.0.xsd"/>
  <xs:element name="TestConnection" type="ConnectionStructure"/>
  <xs:element name="TestJourneyStopInformation" type="JourneyStopInformationStructure"/>
  <xs:element name="TestShortTripStopList" type="ShortTripStopListStructure"/>
</xs:schema>
'''
    with tempfile.NamedTemporaryFile("w", suffix=".xsd", dir=".", encoding="utf-8", delete=False) as fh:
        fh.write(text)
        tmp = Path(fh.name)
    try:
        return etree.XMLSchema(etree.parse(str(tmp)))
    finally:
        tmp.unlink(missing_ok=True)


def display_content() -> str:
    return (
        "<DisplayContent>"
        "<LineInformation><LineRef><Value>L1</Value></LineRef></LineInformation>"
        "<Destination><DestinationRef><Value>D1</Value></DestinationRef></Destination>"
        "</DisplayContent>"
    )


def journey_prefix() -> str:
    return (
        "<StopRef><Value>S1</Value></StopRef>"
        "<StopName><Value>Stop</Value><Language>de</Language></StopName>"
        + display_content()
    )


def fare_zone_information() -> str:
    return "<FareZoneInformation><FareZoneID><Value>FZ1</Value></FareZoneID></FareZoneInformation>"


def instance_boundaries(schema: etree.XMLSchema, common_root: etree._Element) -> None:
    # DRCOM10-001: document revision says optional/new names; exact V1.0 authority remains required/old names.
    conn_base = (
        "<StopRef><Value>S1</Value></StopRef>"
        "<ConnectionRef><Value>C1</Value></ConnectionRef>"
        "<ConnectionType>Interchange</ConnectionType>"
    )
    good_conn = (
        "<TestConnection>" + conn_base + display_content()
        + "<ExpectedDepatureTime><Value>2026-01-01T00:00:00Z</Value></ExpectedDepatureTime>"
        + "</TestConnection>"
    )
    probe(schema, "DRCOM10-001 exact V1.0 Connection shape", good_conn, True)
    probe(schema, "DRCOM10-001 PDF-revision optional DisplayContent", "<TestConnection>" + conn_base + "</TestConnection>", False)
    probe(schema, "DRCOM10-001 PDF ExpectedDepartureTime alias", "<TestConnection>" + conn_base + display_content() + "<ExpectedDepartureTime><Value>2026-01-01T00:00:00Z</Value></ExpectedDepartureTime></TestConnection>", False)
    probe(schema, "DRCOM10-001 PDF ScheduledDepartureTime addition", "<TestConnection>" + conn_base + display_content() + "<ScheduledDepartureTime><Value>2026-01-01T00:00:00Z</Value></ScheduledDepartureTime></TestConnection>", False)

    # DRCOM10-004: PDF says 0:*; exact XSD is 0:1 for both fields.
    ann = "<Announcement><AnnouncementRef><Value>A1</Value></AnnouncementRef></Announcement>"
    fz = "<FareZone><Value>F1</Value></FareZone>"
    probe(schema, "DRCOM10-004 one Announcement", "<TestJourneyStopInformation>" + journey_prefix() + ann + "</TestJourneyStopInformation>", True)
    probe(schema, "DRCOM10-004 two Announcements", "<TestJourneyStopInformation>" + journey_prefix() + ann + ann + "</TestJourneyStopInformation>", False)
    probe(schema, "DRCOM10-004 one FareZone", "<TestJourneyStopInformation>" + journey_prefix() + fz + "</TestJourneyStopInformation>", True)
    probe(schema, "DRCOM10-004 two FareZones", "<TestJourneyStopInformation>" + journey_prefix() + fz + fz + "</TestJourneyStopInformation>", False)

    # DRCOM10-005: child-name boundary is executable. Type-reference mismatch is declaration-only because
    # ShortTripStopStructure and StopPointTariffInformationStructure are instance-shape equivalent here.
    short_body = "<JourneyStopInformation>" + journey_prefix() + "</JourneyStopInformation>" + fare_zone_information()
    good_short = "<TestShortTripStopList><ShortTripStop>" + short_body + "</ShortTripStop></TestShortTripStopList>"
    bad_short = "<TestShortTripStopList><ShortTripStopList>" + short_body + "</ShortTripStopList></TestShortTripStopList>"
    probe(schema, "DRCOM10-005 XSD ShortTripStop child", good_short, True)
    probe(schema, "DRCOM10-005 PDF ShortTripStopList child alias", bad_short, False)

    short_type = common_root.find("xs:complexType[@name='ShortTripStopListStructure']/xs:sequence/xs:element[@name='ShortTripStop']", NS)
    require(short_type is not None and short_type.get("type") == "ShortTripStopStructure", "DRCOM10-005 exact child type is ShortTripStopStructure")
    tariff = common_root.find("xs:complexType[@name='StopPointTariffInformationStructure']", NS)
    short = common_root.find("xs:complexType[@name='ShortTripStopStructure']", NS)
    require(tariff is not None and short is not None, "DRCOM10-005 both compared XSD structures exist")
    def child_sig(node: etree._Element) -> list[tuple[str | None, str | None, str, str]]:
        return [
            (e.get("name"), e.get("type"), e.get("minOccurs", "1"), e.get("maxOccurs", "1"))
            for e in node.findall("xs:sequence/xs:element", NS)
        ]
    require(child_sig(tariff) == child_sig(short), "DRCOM10-005 type-reference alternatives are instance-shape equivalent in V1.0")


def main() -> int:
    require(PDF.exists(), f"missing PDF {PDF}")
    require(blob(FROZEN) == EXPECTED_FROZEN_BLOB, "frozen inventory changed")
    require(blob(DELTA) == EXPECTED_DELTA_BLOB, "COMMON V1.0 deep-read finding delta changed")
    require(blob(COMMON) == EXPECTED_COMMON_BLOB, "Common V1.0 authority changed")
    require(blob(ENUMS) == EXPECTED_ENUM_BLOB, "Enumerations V1.0 authority changed")

    pdf_hash, pdf_size = sha256_file(PDF)
    require(pdf_hash == EXPECTED_PDF_SHA256, f"PDF hash mismatch {pdf_hash}")
    require(pdf_size == EXPECTED_PDF_SIZE, f"PDF size mismatch {pdf_size}")
    require(page_count() == 36, "COMMON V1.0 page count changed")

    frozen = json.loads(FROZEN.read_text(encoding="utf-8"))
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory invariant failed")
    require(all(fid in frozen.get("finding_ids", []) for fid in FINDINGS), "one or more DRCOM10 findings missing from frozen inventory")

    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    entries = reg.get("inventory", {}).get("entries", [])
    by_id = {x.get("finding_id"): x for x in entries}
    require(reg.get("next_revalidation_block") == "COMMON", f"unexpected next block {reg.get('next_revalidation_block')}")
    require("COMMON_V1.0" not in reg.get("revalidation_blocks", {}), "COMMON V1.0 is already closed")
    for fid in FINDINGS:
        require(fid in by_id and by_id[fid].get("revalidation_state") == "pending", f"{fid} is not pending")

    delta = json.loads(DELTA.read_text(encoding="utf-8"))
    require(delta.get("document_id") == "COMMON_V1.0", "deep-read delta document id changed")
    require(set(delta.get("new_unique_findings", {})) == set(FINDINGS), "deep-read delta finding set changed")
    require(delta.get("exact_xsd_authority", {}).get("common_blob") == EXPECTED_COMMON_BLOB, "delta Common authority changed")
    require(delta.get("exact_xsd_authority", {}).get("enumerations_blob") == EXPECTED_ENUM_BLOB, "delta Enumerations authority changed")
    require(delta.get("exact_xsd_authority", {}).get("common_v1_1_xsd_found") is False, "unexpected Common V1.1 XSD authority")

    deep = DEEP_READ.read_text(encoding="utf-8")
    for fid in FINDINGS:
        require(fid in deep, f"deep-read report missing {fid}")

    # Re-run preserved EV-117 unchanged as the base executable authority evidence.
    ev117 = subprocess.run([sys.executable, "tools/validate_common_v10_ev117.py"], text=True)
    require(ev117.returncode == 0, "preserved EV-117 rerun failed")

    common_root = etree.parse(str(COMMON)).getroot()
    schema = compile_harness()
    instance_boundaries(schema, common_root)

    pages = all_pages()
    evidence_pages: dict[str, list[int]] = {}
    evidence_pages["DRCOM10-001"] = sorted(set(
        pages_any(pages, ("Version 1.1", "ScheduledDepartureTime", "RouteDirectionEnumeration", "ExpectedDepartureTime"))
    ))
    evidence_pages["DRCOM10-002"] = pages_all(pages, ("DataAcceptedResponseData", "OperationErrorMessage"))
    evidence_pages["DRCOM10-003"] = pages_any(pages, ("ServiceSpecificationWithStateList",))
    evidence_pages["DRCOM10-004"] = pages_all(pages, ("JourneyStopInformation", "Announcement", "FareZone"))
    evidence_pages["DRCOM10-005"] = pages_all(pages, ("ShortTripStopList", "StopPointTariffInformation"))
    evidence_pages["DRCOM10-006"] = pages_any(pages, ("Wheelchair", "Others", "WheelChair"))
    evidence_pages["DRCOM10-007"] = pages_any(pages, ("GNSSCoordinateSystemsEnumeration", "enummerations", "Infromation", "dorr operation"))

    for fid, found in evidence_pages.items():
        require(found, f"no PDF evidence page found for {fid}")

    render_pages = sorted({p for vals in evidence_pages.values() for p in vals})
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "render_pages.txt").write_text("\n".join(str(p) for p in render_pages) + "\n", encoding="utf-8")
    result = {
        "evidence_id": "EV-135",
        "finding_block": FINDINGS,
        "pdf_source_id": "COMMON_V1.0",
        "pdf_sha256": EXPECTED_PDF_SHA256,
        "pdf_size_bytes": EXPECTED_PDF_SIZE,
        "pdf_page_count": 36,
        "authority_lane": "exact_official_historical_Common_V1.0_Enumerations_V1.0_family",
        "official_import_commit": "604a5a5c7608977e483072f7e450d7381cc182e4",
        "common_xsd_blob": EXPECTED_COMMON_BLOB,
        "enumerations_xsd_blob": EXPECTED_ENUM_BLOB,
        "base_evidence": "EV-117 rerun unchanged",
        "evidence_pages": evidence_pages,
        "terminal_revalidation_recommendations": TERMINAL_RECOMMENDATIONS,
        "new_executable_boundaries": {
            "DRCOM10-001": [
                "exact V1.0 Connection with required DisplayContent and ExpectedDepatureTime valid",
                "omitted DisplayContent invalid",
                "ExpectedDepartureTime invalid",
                "ScheduledDepartureTime invalid",
            ],
            "DRCOM10-004": [
                "one Announcement valid; two invalid",
                "one FareZone valid; two invalid",
            ],
            "DRCOM10-005": [
                "ShortTripStop child valid",
                "ShortTripStopList child alias invalid",
                "PDF type-reference alternative is declaration-mismatched but instance-shape equivalent in exact V1.0 XSD",
            ],
        },
        "visual_review": "rendered pages required before permanent evidence record and closure",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
        "result": "PASS_PENDING_VISUAL_REVIEW",
    }
    (OUT_DIR / "ev135_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED_TEXT_XSD: EV-135 COMMON V1.0 DRCOM10-001..007; visual artifact review still required")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
