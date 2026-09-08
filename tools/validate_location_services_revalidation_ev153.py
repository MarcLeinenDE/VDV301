#!/usr/bin/env python3
"""EV-153: fail-closed terminal revalidation of LS-001..LS-003.

Authority lane:
- official byte-pinned VDV 301-2-2/2-4/2-5/2-7 Location Services V1.0 PDFs,
- exact historical V1.0 service XSDs plus Common V1.0 and Enumerations V1.0,
- frozen finding inventory and the current Evidence Gate.

Executable validation remains XSD-driven. PDF/XSD mismatches and OK-with-note
observations are audit knowledge only. This validator performs no schema or
registry mutation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from lxml import etree

FROZEN_SOURCE_HEAD = "7fad145f528205ef5c40e58a3a23374379b08189"
FROZEN_INVENTORY_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
HIST_START_BLOB = "37c6258d55c38b70f0215b0d9a853f6a83040565"
FIRST_PASS_BLOB = "6c7219d535eaa8ea966a73ebd3b8c881835b926e"
FIRST_PASS_CLOSURE_BLOB = "b54fb0bfd061109570c7156536a2bdf301a263c9"
ADDENDUM_BLOB = "c1e8c7e6f6bfd8179006931b043ffffca122b475"
EVIDENCE_GATE_BLOB = "969cce8b14b50ded2ca5eb745674b894428ecf1a"
CENTRAL_PRESTATE_BLOB = "f3ade5d00f59cb409767b8928ea92e5e11b8b203"
CURRENT_STATE_PRESTATE_BLOB = "c47e024f267751f1d9f8d4e2aea66bca0c200c6b"
PDF_SOURCE_REGISTRY_BLOB = "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8"
PIN_WORKFLOW_BLOB = "45ae18965997e87c599689190e02ef62175992b1"

COMMON_XSD = "IBIS-IP_common_V1.0.xsd"
ENUM_XSD = "IBIS-IP_Enumerations_V1.0.xsd"
COMMON_BLOB = "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c"
ENUM_BLOB = "a9bea5bc73003ed91ded8519db06c32c4067831d"

SERVICE_XSDS = {
    "BLS": ("IBIS-IP_BeaconLocationService_V1.0.xsd", "791e2889f2baa4779ab66ae9e77038ff1b4be915"),
    "DLS": ("IBIS-IP_DistanceLocationService_V1.0.xsd", "e6fdc418b6ddaba75d3fbe8f048d1c6d70e023b6"),
    "GNSS": ("IBIS-IP_GNSSLocationService_V1.0.xsd", "a74a22079af25cdd028a3e519019d9b3326d9971"),
    "NLS": ("IBIS-IP_NetworkLocationService_V1.0.xsd", "bd1f83df2dfa83f36666a3ab3df4457242b387e9"),
}

PDF_SOURCES = {
    "BLS_V1.0": {
        "vdv_part": "301-2-2",
        "url": "https://www.vdv.de/301-2-2sds-v1-0.pdfx",
        "filename": "BLS_V1.0.pdf",
        "sha256": "1756dd8f373defd15988c222bea566a3841af376d987c0b0369f8701f2bc711d",
        "size": 616519,
        "pages": [7, 8],
    },
    "DLS_V1.0": {
        "vdv_part": "301-2-4",
        "url": "https://www.vdv.de/301-2-4sds-v1-0.pdfx",
        "filename": "DLS_V1.0.pdf",
        "sha256": "bdcbb3b2188f109944d687e6511209c5f049f25e1770bb3f4df596542d5009c4",
        "size": 441422,
        "pages": [7],
    },
    "GNSS_V1.0": {
        "vdv_part": "301-2-5",
        "url": "https://www.vdv.de/301-2-5sds-v1-0.pdfx",
        "filename": "GNSS_V1.0.pdf",
        "sha256": "e6a19a333a6c149a2d4b726a189acf16a9891d85dd28a7c5b008cdf254b631f5",
        "size": 449287,
        "pages": [7],
    },
    "NLS_V1.0": {
        "vdv_part": "301-2-7",
        "url": "https://www.vdv.de/301-2-7sds-v1-0.pdfx",
        "filename": "NLS_V1.0.pdf",
        "sha256": "fa45c9ef69635ab8615e4cf7dbd5c0417f8ea154a817ea1c54a73a141c7f4697",
        "size": 447715,
        "pages": [7],
    },
}
PIN_RUN_ID = "34228583786"
PIN_JOB_ID = "102068710920"
PIN_ARTIFACT_ID = "10056787340"
PIN_ARTIFACT_DIGEST = "sha256:ddbcc1774639c3d57a5cdf8efbc5f213a107f804d303cf11af520f5b1d66fe8e"

XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}


def git_blob(root: Path, rel: str, ref: str = "HEAD") -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"{ref}:{rel}"], cwd=root, text=True
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


def validate_xml(schema: etree.XMLSchema, xml: str) -> tuple[bool, str]:
    doc = etree.fromstring(xml.encode("utf-8"))
    ok = schema.validate(doc)
    return ok, "\n".join(str(x) for x in schema.error_log)


def text_page(pdf: Path, page: int, out: Path, label: str) -> str:
    target = out / f"{label}-page-{page}-layout.txt"
    subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(pdf), str(target)],
        check=True,
    )
    return target.read_text(encoding="utf-8", errors="replace")


def render_page(pdf: Path, page: int, out: Path, label: str) -> Path:
    prefix = out / f"{label}-page-{page}"
    subprocess.run(
        ["pdftoppm", "-f", str(page), "-l", str(page), "-singlefile", "-r", "180", "-png", str(pdf), str(prefix)],
        check=True,
    )
    image = prefix.with_suffix(".png")
    assert image.exists() and image.stat().st_size > 0
    return image


def compact(text: str) -> str:
    return re.sub(r"\s+", "", text)


def wrapped(name: str, value: str) -> str:
    return f"<{name}><Value>{value}</Value></{name}>"


def dls_xml(odometer_name: str = "Odometer-Pulses") -> str:
    return (
        "<DistanceLocationService.Data>"
        + wrapped("Distance", "12.5")
        + wrapped(odometer_name, "42")
        + "</DistanceLocationService.Data>"
    )


def gnss_xml(hdop_name: str) -> str:
    return f"""<GNSSLocationService.Data>
  <latitude><Degree><Value>50.93</Value></Degree><Direction><Value>N</Value></Direction></latitude>
  <longitude><Degree><Value>6.95</Value></Degree><Direction><Value>E</Value></Direction></longitude>
  <{hdop_name}><Value>1.1</Value></{hdop_name}>
  <GNSSType>GPS</GNSSType>
</GNSSLocationService.Data>"""


def bls_xml() -> str:
    return """<BeaconLocationService.GetDataResponse>
  <Data>
    <TimeStamp><Value>2026-09-08T12:00:00Z</Value></TimeStamp>
    <BeaconCode><Value>B1</Value></BeaconCode>
    <BeaconDistance><Value>10.0</Value></BeaconDistance>
  </Data>
</BeaconLocationService.GetDataResponse>"""


def nls_xml() -> str:
    return """<NetworkLocationService.Data>
  <CurrentTripRef><Value>T1</Value></CurrentTripRef>
  <NextPointRef><Value>P1</Value></NextPointRef>
  <DistanceToNextPoint><Value>10.0</Value></DistanceToNextPoint>
  <NextStopPointRef><Value>S1</Value></NextStopPointRef>
  <DistanceToNextStopPoint><Value>20.0</Value></DistanceToNextStopPoint>
</NetworkLocationService.Data>"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--output-dir", default="artifacts/ev153")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    out = (root / args.output_dir).resolve()
    text_out = out / "text"
    render_out = out / "renders"
    samples_out = out / "samples"
    for p in (out, text_out, render_out, samples_out):
        p.mkdir(parents=True, exist_ok=True)

    head_guards = {
        "audit_registry/finding_inventory_frozen_2026-09-03.json": FROZEN_INVENTORY_BLOB,
        "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md": EVIDENCE_GATE_BLOB,
        "audit_registry/finding_revalidation_registry_v0.1.json": CENTRAL_PRESTATE_BLOB,
        "00_START_HERE/CURRENT_STATE.json": CURRENT_STATE_PRESTATE_BLOB,
        "audit_registry/pdf_source_registry_v0.1.json": PDF_SOURCE_REGISTRY_BLOB,
        ".github/workflows/temp_pin_location_services_v10.yml": PIN_WORKFLOW_BLOB,
        COMMON_XSD: COMMON_BLOB,
        ENUM_XSD: ENUM_BLOB,
    }
    for _, (rel, blob) in SERVICE_XSDS.items():
        head_guards[rel] = blob
    for rel, expected in head_guards.items():
        actual = git_blob(root, rel)
        assert actual == expected, f"authority changed: {rel}: {actual} != {expected}"

    historical_guards = {
        "docs/pdf_xsd_semantic_audit/07_location_services_historical_start.md": HIST_START_BLOB,
        "docs/pdf_xsd_semantic_audit/07a_location_services_v1_0_pdf_xsd_first_pass.md": FIRST_PASS_BLOB,
        "docs/pdf_xsd_semantic_audit/07b_location_services_findings_and_closure.md": FIRST_PASS_CLOSURE_BLOB,
        "docs/pdf_xsd_semantic_audit/LOCATION_SERVICES_FINDINGS_REGISTER_ADDENDUM.md": ADDENDUM_BLOB,
    }
    for rel, expected in historical_guards.items():
        actual = git_blob(root, rel, FROZEN_SOURCE_HEAD)
        assert actual == expected, f"frozen authority changed: {rel}: {actual} != {expected}"

    central = load_json(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    assert central["next_revalidation_block"] == "LS"
    inv = central["inventory"]
    assert inv["state"] == "frozen"
    assert inv["entry_count"] == 192 and len(inv["entries"]) == 192
    terminal = sum(x["revalidation_state"] != "pending" for x in inv["entries"])
    pending = sum(x["revalidation_state"] == "pending" for x in inv["entries"])
    assert (terminal, pending) == (132, 60), (terminal, pending)
    by_id = {x["finding_id"]: x for x in inv["entries"]}
    for fid in ["LS-001", "LS-002", "LS-003"]:
        assert by_id[fid] == {
            "finding_id": fid,
            "revalidation_state": "pending",
            "terminal_state_source": None,
        }
    assert next(x["finding_id"] for x in inv["entries"] if x["revalidation_state"] == "pending") == "LS-001"

    state = load_json(root / "00_START_HERE/CURRENT_STATE.json")["audit"]
    assert state["finding_revalidation_next_block"] == "LS"
    assert state["finding_revalidation_completed_findings"] == 132
    assert state["finding_revalidation_pending_findings"] == 60
    assert state["latest_revalidation_evidence_id"] == "EV-152"

    registry = load_json(root / "audit_registry/pdf_source_registry_v0.1.json")
    by_source = {x["source_id"]: x for x in registry["sources"]}
    pdf_results = {}
    for source_id, spec in PDF_SOURCES.items():
        src = by_source[source_id]
        assert src["official_url"] == spec["url"]
        assert src["local_filename"] == spec["filename"]
        assert src["document_id"] == source_id
        assert src["vdv_part"] == spec["vdv_part"] and src["version"] == "1.0"
        pdf = root / "local_sources/vdv_pdfs" / spec["filename"]
        assert pdf.exists(), f"missing exact PDF: {pdf}"
        assert sha256(pdf) == spec["sha256"]
        assert pdf.stat().st_size == spec["size"]
        pdf_results[source_id] = {
            "sha256": spec["sha256"],
            "size_bytes": spec["size"],
            "pages": spec["pages"],
        }

    docs = {}
    schemas = {}
    for key, (rel, _) in SERVICE_XSDS.items():
        doc = etree.parse(str(root / rel))
        includes = [x.get("schemaLocation") for x in doc.xpath("/xs:schema/xs:include", namespaces=NS)]
        assert includes == [COMMON_XSD, ENUM_XSD], (key, includes)
        docs[key] = doc
        schemas[key] = etree.XMLSchema(doc)

    # LS-001: PDF spelling vs executable XSD spelling.
    gnss_doc = docs["GNSS"]
    gnss_type = one(gnss_doc.xpath("//xs:complexType[@name='GNSSLocationService.DataStructure']", namespaces=NS), "GNSSLocationService.DataStructure")
    xsd_hdop = one(gnss_type.xpath("./xs:sequence/xs:element[@name='HoriziontalDilutionOfPrecision']", namespaces=NS), "XSD typo-like HDOP element")
    assert xsd_hdop.get("type") == "IBIS-IP.double" and xsd_hdop.get("minOccurs") == "0"
    assert not gnss_type.xpath("./xs:sequence/xs:element[@name='HorizontalDilutionOfPrecision']", namespaces=NS)
    gnss_pos = gnss_xml("HoriziontalDilutionOfPrecision")
    gnss_neg = gnss_xml("HorizontalDilutionOfPrecision")
    (samples_out / "ls001-positive-xsd-spelling.xml").write_text(gnss_pos + "\n", encoding="utf-8")
    (samples_out / "ls001-negative-pdf-spelling.xml").write_text(gnss_neg + "\n", encoding="utf-8")
    ok, err = validate_xml(schemas["GNSS"], gnss_pos)
    assert ok, err
    bad_ok, bad_err = validate_xml(schemas["GNSS"], gnss_neg)
    assert not bad_ok, "LS-001 PDF-spelled negative unexpectedly validated"

    # LS-002: exact hyphenated name is aligned in PDF and XSD and executable.
    dls_doc = docs["DLS"]
    dls_type = one(dls_doc.xpath("//xs:complexType[@name='DistanceLocationService.DataStructure']", namespaces=NS), "DistanceLocationService.DataStructure")
    odo = one(dls_type.xpath("./xs:sequence/xs:element[@name='Odometer-Pulses']", namespaces=NS), "Odometer-Pulses")
    assert odo.get("type") == "IBIS-IP.int" and odo.get("minOccurs") == "0"
    assert not dls_type.xpath("./xs:sequence/xs:element[@name='OdometerPulses' or @name='Odometer_Pulses']", namespaces=NS)
    dls_pos = dls_xml("Odometer-Pulses")
    dls_neg = dls_xml("OdometerPulses")
    (samples_out / "ls002-positive-hyphenated.xml").write_text(dls_pos + "\n", encoding="utf-8")
    (samples_out / "ls002-negative-normalized.xml").write_text(dls_neg + "\n", encoding="utf-8")
    ok, err = validate_xml(schemas["DLS"], dls_pos)
    assert ok, err
    bad_ok, bad_err = validate_xml(schemas["DLS"], dls_neg)
    assert not bad_ok, "LS-002 normalized negative unexpectedly validated"

    # LS-003: service-specific top-level modelling is intentional and routable.
    root_names = {
        key: [x.get("name") for x in doc.xpath("/xs:schema/xs:element", namespaces=NS)]
        for key, doc in docs.items()
    }
    assert root_names["BLS"] == ["BeaconLocationService.GetDataResponse"]
    assert root_names["DLS"] == ["DistanceLocationService.Data"]
    assert root_names["GNSS"] == ["GNSSLocationService.Data"]
    assert root_names["NLS"] == ["NetworkLocationService.Data"]

    samples = {"BLS": bls_xml(), "DLS": dls_pos, "GNSS": gnss_pos, "NLS": nls_xml()}
    routing_results = {}
    for key, xml in samples.items():
        (samples_out / f"ls003-{key.lower()}-positive.xml").write_text(xml + "\n", encoding="utf-8")
        ok, err = validate_xml(schemas[key], xml)
        assert ok, f"{key} own-route failed: {err}"
        routing_results[key] = {"own_schema_valid": True}
    cross_checks = [("BLS", "DLS"), ("DLS", "BLS"), ("GNSS", "NLS"), ("NLS", "GNSS")]
    for sample_key, schema_key in cross_checks:
        ok, _ = validate_xml(schemas[schema_key], samples[sample_key])
        assert not ok, f"LS-003 cross-route unexpectedly valid: {sample_key} -> {schema_key}"
        routing_results[sample_key][f"rejected_by_{schema_key}"] = True

    page_text = {}
    render_hashes = {}
    for source_id, spec in PDF_SOURCES.items():
        pdf = root / "local_sources/vdv_pdfs" / spec["filename"]
        for page in spec["pages"]:
            label = source_id.replace("_V1.0", "")
            text = text_page(pdf, page, text_out, label)
            page_text[(source_id, page)] = text
            image = render_page(pdf, page, render_out, label)
            render_hashes[f"{source_id}:{page}"] = {"sha256": sha256(image), "size_bytes": image.stat().st_size}

    assert "HorizontalDilutionOfPrecision" in compact(page_text[("GNSS_V1.0", 7)])
    assert "HoriziontalDilutionOfPrecision" not in compact(page_text[("GNSS_V1.0", 7)])
    assert "Odometer-Pulses" in page_text[("DLS_V1.0", 7)]
    bls8 = compact(page_text[("BLS_V1.0", 8)])
    assert "BeaconLocationService.GetDataResponse" in bls8
    assert "OperationErrorMessage" in bls8
    assert "BeaconLocationService.DataContent" in bls8
    assert "NetworkLocationService.Data" in compact(page_text[("NLS_V1.0", 7)])

    evidence = {
        "evidence_id": "EV-153",
        "block": "LS_V1.0",
        "findings": {
            "LS-001": {
                "recommended_terminal_state": "executable_confirmed",
                "classification": "confirmed PDF/XSD spelling discrepancy",
                "pdf_spelling": "HorizontalDilutionOfPrecision",
                "xsd_spelling": "HoriziontalDilutionOfPrecision",
                "positive_xsd_sample_valid": True,
                "negative_pdf_spelling_rejected": True,
            },
            "LS-002": {
                "recommended_terminal_state": "contextual_not_defect",
                "classification": "OK with note; exact XML name aligned",
                "exact_name": "Odometer-Pulses",
                "positive_exact_name_valid": True,
                "normalized_alias_rejected": True,
            },
            "LS-003": {
                "recommended_terminal_state": "contextual_not_defect",
                "classification": "OK with note; intentional service-specific root modelling",
                "roots": root_names,
                "routing": routing_results,
            },
        },
        "prestate": {"terminal": 132, "pending": 60, "next_block": "LS", "latest_evidence": "EV-152"},
        "poststate_if_closed": {"terminal": 135, "pending": 57, "next_block": "NET"},
        "pdf_pin": {
            "run_id": PIN_RUN_ID,
            "job_id": PIN_JOB_ID,
            "artifact_id": PIN_ARTIFACT_ID,
            "artifact_digest": PIN_ARTIFACT_DIGEST,
            "sources": pdf_results,
        },
        "xsd_blobs": {key: {"path": rel, "blob": blob} for key, (rel, blob) in SERVICE_XSDS.items()},
        "dependency_blobs": {COMMON_XSD: COMMON_BLOB, ENUM_XSD: ENUM_BLOB},
        "frozen_source_head": FROZEN_SOURCE_HEAD,
        "rendered_pages": render_hashes,
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }
    (out / "ev153-result.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

    # Preserve validation diagnostics for audit reproducibility.
    (out / "negative-diagnostics.txt").write_text(
        "LS-001 negative (PDF spelling):\n" + bad_err + "\n",
        encoding="utf-8",
    )
    manifest_files = sorted(p for p in out.rglob("*") if p.is_file() and p.name != "manifest.sha256")
    with (out / "manifest.sha256").open("w", encoding="utf-8") as f:
        for p in manifest_files:
            f.write(f"{sha256(p)}  {p.relative_to(out)}\n")

    print("EV153_OK LS-001=executable_confirmed LS-002=contextual_not_defect LS-003=contextual_not_defect")
    print(json.dumps(evidence["poststate_if_closed"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
