#!/usr/bin/env python3
"""EV-152: fail-closed terminal revalidation of JIS-001..JIS-005.

Authority lane:
- official byte-pinned VDV 301-2-6 JourneyInformationService V1.0 PDF,
- exact historical service XSD plus Common V1.0 and Enumerations V1.0,
- frozen finding inventory and the current Evidence Gate.

The selected XSD remains normative for executable XML validation. PDF/XSD
mismatches are explanatory audit knowledge only; this validator performs no
schema mutation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

from lxml import etree

FROZEN_INVENTORY_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
FIRST_PASS_BLOB = "6add2ad2fe836767de9606232d0e70823c9c2212"
FIRST_PASS_CLOSURE_BLOB = "922f541f58b394803a69c4c58ec2e213dcb34d1f"
EVIDENCE_GATE_BLOB = "969cce8b14b50ded2ca5eb745674b894428ecf1a"
CENTRAL_PRESTATE_BLOB = "226c0a0f129ad9fbe2a0d8dbf269925435add112"
CURRENT_STATE_PRESTATE_BLOB = "c8662264f00986b017bbf7ef02f849e06ab64245"
PDF_SOURCE_REGISTRY_BLOB = "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8"
PIN_WORKFLOW_BLOB = "f653439d84ec4016df3222294ce5a7d089c6ab09"

SERVICE_XSD = "IBIS-IP_JourneyInformationService_V1.0.xsd"
COMMON_XSD = "IBIS-IP_common_V1.0.xsd"
ENUM_XSD = "IBIS-IP_Enumerations_V1.0.xsd"
SERVICE_BLOB = "8c303db5a9c0548d66b90174d9c329d33092ad24"
COMMON_BLOB = "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c"
ENUM_BLOB = "a9bea5bc73003ed91ded8519db06c32c4067831d"

PDF_SOURCE_ID = "JIS_V1.0"
PDF_URL = "https://www.vdv.de/301-2-6sds-v1-0.pdfx"
PDF_FILENAME = "JIS_V1.0.pdf"
PDF_SHA256 = "424181b4932e18b6ac059843fa3978fdcc07a9c6acb553f9fbe8b71ef583da73"
PDF_SIZE = 772125
PIN_RUN_ID = "34103529949"
PIN_ARTIFACT_ID = "10011459459"

PDF_PAGES = [9, 11, 12, 13, 17, 19, 22]
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}


def git_blob(root: Path, rel: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{rel}"], cwd=root, text=True
    ).strip()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def one(nodes, what: str):
    assert len(nodes) == 1, f"expected one {what}, got {len(nodes)}"
    return nodes[0]


def text_page(pdf: Path, page: int, out: Path) -> str:
    target = out / f"page-{page}-layout.txt"
    subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(pdf), str(target)],
        check=True,
    )
    return target.read_text(encoding="utf-8", errors="replace")


def render_page(pdf: Path, page: int, out: Path) -> Path:
    prefix = out / f"page-{page}"
    subprocess.run(
        [
            "pdftoppm", "-f", str(page), "-singlefile", "-r", "180",
            "-png", str(pdf), str(prefix),
        ],
        check=True,
    )
    result = prefix.with_suffix(".png")
    assert result.exists() and result.stat().st_size > 0
    return result


def validate_xml(schema: etree.XMLSchema, xml: str) -> tuple[bool, str]:
    doc = etree.fromstring(xml.encode("utf-8"))
    ok = schema.validate(doc)
    errors = "\n".join(str(x) for x in schema.error_log)
    return ok, errors


def line_information_xml(count: int) -> str:
    entries = "\n".join(
        f"<LineInformation><LineRef><Value>L{i}</Value></LineRef></LineInformation>"
        for i in range(1, count + 1)
    )
    return f"""<JourneyInformationService.ListAllLineInformationResponse>
  <AllLineInformationData>
    <TimeStamp><Value>2026-09-07T10:00:00Z</Value></TimeStamp>
    {entries}
  </AllLineInformationData>
</JourneyInformationService.ListAllLineInformationResponse>"""


def gnss_xml(child_name: str) -> str:
    return f"""<JourneyInformationService.RetrieveSpecificGNSSPointInformationResponse>
  <{child_name}>
    <TimeStamp><Value>2026-09-07T10:00:00Z</Value></TimeStamp>
    <GNSSPoint>
      <Longitude><Degree><Value>6.95</Value></Degree><Direction><Value>E</Value></Direction></Longitude>
      <Latitude><Degree><Value>50.93</Value></Degree><Direction><Value>N</Value></Direction></Latitude>
    </GNSSPoint>
  </{child_name}>
</JourneyInformationService.RetrieveSpecificGNSSPointInformationResponse>"""


def require_all(text: str, needles: list[str], label: str) -> None:
    for needle in needles:
        assert needle in text, f"{label}: missing {needle!r}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--output-dir", default="artifacts/ev152")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    out = (root / args.output_dir).resolve()
    text_out = out / "text"
    render_out = out / "renders"
    samples_out = out / "samples"
    for p in (out, text_out, render_out, samples_out):
        p.mkdir(parents=True, exist_ok=True)

    guards = {
        "audit_registry/finding_inventory_frozen_2026-09-03.json": FROZEN_INVENTORY_BLOB,
        "docs/pdf_xsd_semantic_audit/06a_jis_v1_0_pdf_xsd_first_pass.md": FIRST_PASS_BLOB,
        "docs/pdf_xsd_semantic_audit/06b_jis_findings_and_closure.md": FIRST_PASS_CLOSURE_BLOB,
        "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md": EVIDENCE_GATE_BLOB,
        "audit_registry/finding_revalidation_registry_v0.1.json": CENTRAL_PRESTATE_BLOB,
        "00_START_HERE/CURRENT_STATE.json": CURRENT_STATE_PRESTATE_BLOB,
        "audit_registry/pdf_source_registry_v0.1.json": PDF_SOURCE_REGISTRY_BLOB,
        ".github/workflows/temp_pin_jis_v10.yml": PIN_WORKFLOW_BLOB,
        SERVICE_XSD: SERVICE_BLOB,
        COMMON_XSD: COMMON_BLOB,
        ENUM_XSD: ENUM_BLOB,
    }
    for rel, expected in guards.items():
        actual = git_blob(root, rel)
        assert actual == expected, f"authority changed: {rel}: {actual} != {expected}"

    central = load_json(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    assert central["next_revalidation_block"] == "JIS"
    inv = central["inventory"]
    assert inv["state"] == "frozen"
    assert inv["entry_count"] == 192 and len(inv["entries"]) == 192
    terminal = sum(x["revalidation_state"] != "pending" for x in inv["entries"])
    pending = sum(x["revalidation_state"] == "pending" for x in inv["entries"])
    assert (terminal, pending) == (127, 65), (terminal, pending)
    by_id = {x["finding_id"]: x for x in inv["entries"]}
    for fid in ["JIS-001", "JIS-002", "JIS-003", "JIS-004", "JIS-005"]:
        assert by_id[fid] == {
            "finding_id": fid,
            "revalidation_state": "pending",
            "terminal_state_source": None,
        }
    first_pending = next(x["finding_id"] for x in inv["entries"] if x["revalidation_state"] == "pending")
    assert first_pending == "JIS-001"

    state = load_json(root / "00_START_HERE/CURRENT_STATE.json")["audit"]
    assert state["finding_revalidation_next_block"] == "JIS"
    assert state["finding_revalidation_completed_findings"] == 127
    assert state["finding_revalidation_pending_findings"] == 65
    assert state["latest_revalidation_evidence_id"] == "EV-151"

    sources = load_json(root / "audit_registry/pdf_source_registry_v0.1.json")
    source = one([x for x in sources["sources"] if x["source_id"] == PDF_SOURCE_ID], PDF_SOURCE_ID)
    assert source["official_url"] == PDF_URL
    assert source["local_filename"] == PDF_FILENAME
    assert source["document_id"] == PDF_SOURCE_ID
    assert source["vdv_part"] == "301-2-6" and source["version"] == "1.0"

    pdf = root / "local_sources/vdv_pdfs" / PDF_FILENAME
    assert pdf.exists(), f"missing exact PDF: {pdf}"
    assert sha256(pdf) == PDF_SHA256
    assert pdf.stat().st_size == PDF_SIZE

    service_doc = etree.parse(str(root / SERVICE_XSD))
    common_doc = etree.parse(str(root / COMMON_XSD))
    includes = [x.get("schemaLocation") for x in service_doc.xpath("/xs:schema/xs:include", namespaces=NS)]
    assert includes == [COMMON_XSD, ENUM_XSD], includes
    common_includes = [x.get("schemaLocation") for x in common_doc.xpath("/xs:schema/xs:include", namespaces=NS)]
    assert common_includes == [ENUM_XSD], common_includes

    schema = etree.XMLSchema(service_doc)

    # JIS-001 active disproof: shared subscription structures are intentional.
    group = one(service_doc.xpath("//xs:group[@name='JourneyInformationServiceGroup']", namespaces=NS), "JourneyInformationServiceGroup")
    group_names = [x.get("name") for x in group.xpath(".//xs:element", namespaces=NS)]
    assert not any("Subscribe" in (x or "") or "Unsubscribe" in (x or "") for x in group_names)
    for ctype in [
        "SubscribeRequestStructure", "SubscribeResponseStructure",
        "UnsubscribeRequestStructure", "UnsubscribeResponseStructure",
    ]:
        one(common_doc.xpath(f"//xs:complexType[@name='{ctype}']", namespaces=NS), ctype)

    # JIS-002 active disproof: Set responses are shared/common modelling.
    set_requests = [x for x in group_names if (x or "").startswith("JourneyInformationService.Set")]
    assert len(set_requests) == 7, set_requests
    assert all((x or "").endswith("Request") for x in set_requests)
    assert not any((x or "").startswith("JourneyInformationService.Set") and (x or "").endswith("Response") for x in group_names)
    one(common_doc.xpath("//xs:complexType[@name='DataAcceptedResponseStructure']", namespaces=NS), "DataAcceptedResponseStructure")

    # JIS-003 exact declaration plus executable behavior.
    all_line = one(service_doc.xpath("//xs:complexType[@name='JourneyInformationService.AllLineInformationData']", namespaces=NS), "AllLineInformationData")
    line_decl = one(all_line.xpath("./xs:sequence/xs:element[@name='LineInformation']", namespaces=NS), "LineInformation")
    assert line_decl.get("type") == "LineInformationStructure"
    assert line_decl.get("minOccurs") is None
    assert line_decl.get("maxOccurs") is None
    line_pos = line_information_xml(1)
    line_neg = line_information_xml(2)
    (samples_out / "jis003-positive-one-line.xml").write_text(line_pos + "\n", encoding="utf-8")
    (samples_out / "jis003-negative-two-lines.xml").write_text(line_neg + "\n", encoding="utf-8")
    ok1, err1 = validate_xml(schema, line_pos)
    ok2, err2 = validate_xml(schema, line_neg)
    assert ok1, err1
    assert not ok2, "JIS-003 negative unexpectedly validated"

    # JIS-004 exact operation declaration stays RetrieveAllRoutesPerLineRequest.
    routes_req = one(service_doc.xpath("/xs:schema/xs:element[@name='JourneyInformationService.RetrieveAllRoutesPerLineRequest']", namespaces=NS), "RetrieveAllRoutesPerLineRequest")
    assert routes_req.get("type") == "JourneyInformationService.RetrieveAllRoutesPerLineRequestStructure"
    routes_type = one(service_doc.xpath("//xs:complexType[@name='JourneyInformationService.RetrieveAllRoutesPerLineRequestStructure']", namespaces=NS), "RetrieveAllRoutesPerLineRequestStructure")
    line_ref = one(routes_type.xpath("./xs:sequence/xs:element[@name='LineRef']", namespaces=NS), "RetrieveAllRoutesPerLine.LineRef")
    assert line_ref.get("type") == "IBIS-IP.NMTOKEN"

    # JIS-005 exact choice name plus executable positive/negative behavior.
    gnss_resp = one(service_doc.xpath("//xs:complexType[@name='JourneyInformationService.RetrieveSpecificGNSSPointInformationResponseStructure']", namespaces=NS), "RetrieveSpecificGNSSPointInformationResponseStructure")
    gnss_choice = one(gnss_resp.xpath("./xs:choice/xs:element[@name='SpecificGNSSPointInformation']", namespaces=NS), "SpecificGNSSPointInformation choice")
    assert gnss_choice.get("type") == "JourneyInformationService.SpecificGNSSPointInformationData"
    assert not gnss_resp.xpath("./xs:choice/xs:element[@name='SpecificGNSSPointInformationData']", namespaces=NS)
    gnss_pos = gnss_xml("SpecificGNSSPointInformation")
    gnss_neg = gnss_xml("SpecificGNSSPointInformationData")
    (samples_out / "jis005-positive-xsd-element-name.xml").write_text(gnss_pos + "\n", encoding="utf-8")
    (samples_out / "jis005-negative-pdf-row-name.xml").write_text(gnss_neg + "\n", encoding="utf-8")
    ok3, err3 = validate_xml(schema, gnss_pos)
    ok4, err4 = validate_xml(schema, gnss_neg)
    assert ok3, err3
    assert not ok4, "JIS-005 PDF-row-name negative unexpectedly validated"

    page_text = {}
    render_hashes = {}
    for page in PDF_PAGES:
        txt = text_page(pdf, page, text_out)
        page_text[page] = txt
        image = render_page(pdf, page, render_out)
        render_hashes[str(page)] = {
            "sha256": sha256(image),
            "size_bytes": image.stat().st_size,
        }

    require_all(page_text[9], [
        "SubscribeAllData", "SubscribeRequestStructure", "SubscribeResponseStructure",
        "UnsubscribeAllData", "UnsubscribeRequestStructure", "UnsubscribeResponseStructure",
        "SubscribeCurrentBlockRef", "UnsubscribeCurrentBlockRef",
    ], "JIS-001 page 9")
    require_all(page_text[12], [
        "Datenstruktur der Operation SubscribeAllData",
        "VDV 301-2-1 beschriebenen",
        "Datenstruktur der Operation UnsubscribeAllData",
    ], "JIS-001 page 12")
    require_all(page_text[13], [
        "Datenstruktur der Operation SubscribeCurrentBlockRef",
        "Datenstruktur der Operation UnsubscribeCurrentBlockRef",
        "VDV 301-2-1 beschriebenen",
    ], "JIS-001 page 13")

    for opname in [
        "SetBlockNumber", "SetTripRef", "SetDisplayContent", "SetCurrentTripIndex",
        "SetCurrentStopIndex", "SetAdditionalAnnouncement", "SetAdditionalTextMessage",
    ]:
        assert opname in page_text[11], f"JIS-002 page 11 missing {opname}"
    assert page_text[11].count("DataAcceptedResponseStructure") >= 7

    require_all(page_text[19], [
        "Datenstruktur der Operation ListAllLineInformation",
        "JourneyInformationService.AllLineInformat",
        "LineInformation",
        "1:*",
    ], "JIS-003 page 19")

    require_all(page_text[22], [
        "Datenstruktur der Operation RetrieveAllRoutesPerLine",
        "JourneyInformationService.SetBlockNumb",
        "LineRef",
        "Tabelle 38",
        "JourneyInformationService.SetBlockNumberRequest",
    ], "JIS-004 page 22")

    require_all(page_text[17], [
        "Datenstruktur der Operation RetrieveSpecificGNSSPointInformation",
        "SpecificGNSSPointI",
        "nformationData",
        "JourneyInformationService.SpecificGNSSP",
        "ointInformationData",
    ], "JIS-005 page 17")

    result = {
        "evidence_id": "EV-152",
        "result": "PASS",
        "scope": ["JIS-001", "JIS-002", "JIS-003", "JIS-004", "JIS-005"],
        "recommended_terminal_states": {
            "JIS-001": "contextual_not_defect",
            "JIS-002": "contextual_not_defect",
            "JIS-003": "executable_confirmed",
            "JIS-004": "context_verified",
            "JIS-005": "executable_confirmed"
        },
        "authority": {
            "pdf": {
                "source_id": PDF_SOURCE_ID,
                "official_url": PDF_URL,
                "sha256": PDF_SHA256,
                "size_bytes": PDF_SIZE,
                "pin_run_id": PIN_RUN_ID,
                "pin_artifact_id": PIN_ARTIFACT_ID
            },
            "xsd_route": "JIS V1.0 -> Common V1.0 -> Enumerations V1.0",
            "service_blob": SERVICE_BLOB,
            "common_blob": COMMON_BLOB,
            "enumerations_blob": ENUM_BLOB
        },
        "findings": {
            "JIS-001": {
                "classification_after_disproof": "contextual_not_defect",
                "reason": "PDF explicitly delegates subscription structures to VDV 301-2-1 and Common V1.0 contains the four generic Subscribe/Unsubscribe structures; absence from local JIS group is intentional shared modelling.",
                "visual_pages": [9, 12, 13],
                "validation_behavior": "no JIS-local subscribe/unsubscribe element alias inferred"
            },
            "JIS-002": {
                "classification_after_disproof": "contextual_not_defect",
                "reason": "PDF operation overview uses generic DataAcceptedResponseStructure for Set* responses; Common V1.0 defines it while the JIS group contains the seven Set* request elements only.",
                "visual_pages": [11, 22],
                "validation_behavior": "no JIS-local Set*Response element inferred"
            },
            "JIS-003": {
                "classification_after_disproof": "executable_confirmed",
                "reason": "PDF table 29 visibly marks LineInformation 1:*; exact XSD omits maxOccurs so XML Schema default maxOccurs=1 applies.",
                "visual_pages": [19],
                "xsd_declaration": {"minOccurs": "default=1", "maxOccurs": "default=1"},
                "positive_one_line": ok1,
                "negative_two_lines": ok2,
                "negative_error": err2
            },
            "JIS-004": {
                "classification_after_disproof": "context_verified",
                "reason": "PDF section 1.22 RetrieveAllRoutesPerLine visibly carries SetBlockNumberRequest in table 38; exact XSD retains RetrieveAllRoutesPerLineRequest with LineRef.",
                "visual_pages": [22],
                "validation_behavior": "documentation label only; XSD operation is unchanged"
            },
            "JIS-005": {
                "classification_after_disproof": "executable_confirmed",
                "reason": "PDF response choice row visibly names SpecificGNSSPointInformationData, while exact XSD choice element is SpecificGNSSPointInformation typed as JourneyInformationService.SpecificGNSSPointInformationData.",
                "visual_pages": [17],
                "positive_xsd_element_name": ok3,
                "negative_pdf_row_name": ok4,
                "negative_error": err4
            }
        },
        "fresh_visual_evidence": {
            "physical_pages": PDF_PAGES,
            "render_dpi": 180,
            "render_hashes": render_hashes,
            "manual_visual_review_required_before_closure": True
        },
        "prestate": {
            "terminal": terminal,
            "pending": pending,
            "first_pending": first_pending,
            "expected_poststate_if_closed": {"terminal": 132, "pending": 60, "first_pending": "LS-001"}
        },
        "immutable_guards": {
            "frozen_inventory_blob": FROZEN_INVENTORY_BLOB,
            "frozen_inventory_mutated": False,
            "xsd_mutated": False
        }
    }
    (out / "ev152-result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("PASSED: EV-152 JIS-001..JIS-005 revalidation confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
