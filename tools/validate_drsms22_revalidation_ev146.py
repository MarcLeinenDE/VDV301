#!/usr/bin/env python3
"""EV-146: fail-closed revalidation of frozen DRSMS22-001..004 findings.

Authority is the exact byte-pinned SystemMonitoringService V2.2 publication
and the exact official VDV-301-2.2 SMS/Common/Enumerations family. The four
findings are documentation/context findings; EV-116 is rerun as supporting
executable authority evidence. No normative XSD is modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from lxml import etree

SOURCE_ID = "SMS_V2.2"
PDF_SHA256 = "996f639a81cb91ad20a8e78b6213e7c85d41ff0ec42caba4208d6c4652b140f4"
PDF_SIZE = 847416
FROZEN_INVENTORY_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
DEEP_READ_BLOB = "4eb220e43a728a0f719cdcf81fac78df058ecd08"
SMS_XSD_BLOB = "d8d3011965fcf7c5c15ecd6f0d7e917a3f9e6d3c"
COMMON_XSD_BLOB = "468fee6d177e7185dbcd5d3f90cfb114e29e01ae"
ENUM_XSD_BLOB = "2a23b512379b18e8f122ac1272cef8229fb86283"
EV116_SCRIPT_BLOB = "bac849f6c33e6084e899794564f99f0c6cbd338a"
EV116_RUN = "33269006407"
EV116_JOB = "99144006184"
TARGET_PAGES = [5, 9, 10, 11, 12, 13]
XS = "http://www.w3.org/2001/XMLSchema"


def fail(msg: str) -> None:
    raise AssertionError(msg)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob(root: Path, rel: str) -> str:
    return subprocess.check_output(["git", "rev-parse", f"HEAD:{rel}"], cwd=root, text=True).strip()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def norm(text: str) -> str:
    return re.sub(r"\s+", "", text).lower()


def extract_page(pdf: Path, page: int, out_dir: Path) -> tuple[str, str]:
    layout_target = out_dir / f"page-{page:02d}-layout.txt"
    raw_target = out_dir / f"page-{page:02d}-raw.txt"
    subprocess.run(["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(pdf), str(layout_target)], check=True)
    subprocess.run(["pdftotext", "-raw", "-f", str(page), "-l", str(page), str(pdf), str(raw_target)], check=True)
    return (
        layout_target.read_text(encoding="utf-8", errors="replace"),
        raw_target.read_text(encoding="utf-8", errors="replace"),
    )


def render_page(pdf: Path, page: int, out_dir: Path) -> Path:
    prefix = out_dir / f"page-{page:02d}"
    subprocess.run([
        "pdftoppm", "-f", str(page), "-l", str(page), "-singlefile",
        "-png", "-r", "180", str(pdf), str(prefix)
    ], check=True)
    png = prefix.with_suffix(".png")
    if not png.exists() or png.stat().st_size == 0:
        fail(f"render missing for page {page}")
    return png


def require_any(layout: str, raw: str, page: int, *tokens: str) -> None:
    combined = norm(layout + "\n" + raw)
    missing = [t for t in tokens if norm(t) not in combined]
    if missing:
        fail(f"page {page}: missing tokens {missing}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--output-dir", default="artifacts/ev146")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    out = (root / args.output_dir).resolve()
    render_dir = out / "renders"
    text_dir = out / "page_text"
    render_dir.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)

    guards = {
        "audit_registry/finding_inventory_frozen_2026-09-03.json": FROZEN_INVENTORY_BLOB,
        "docs/pdf_xsd_semantic_audit/deep_read/SMS_V2.2.md": DEEP_READ_BLOB,
        "IBIS-IP_SystemMonitoringService_V2.2.xsd": SMS_XSD_BLOB,
        "IBIS-IP_common_V2.2.xsd": COMMON_XSD_BLOB,
        "IBIS-IP_Enumerations_V2.2.xsd": ENUM_XSD_BLOB,
        "tools/validate_sms_v22_ev116.py": EV116_SCRIPT_BLOB,
    }
    for rel, expected in guards.items():
        actual = git_blob(root, rel)
        if actual != expected:
            fail(f"canonical authority changed: {rel}: {actual} != {expected}")

    sources = load_json(root / "audit_registry/pdf_source_registry_v0.1.json")
    pins = load_json(root / "audit_registry/pdf_source_pins_v0.1.json")
    source = next(x for x in sources["sources"] if x["source_id"] == SOURCE_ID)
    pin = next(x for x in pins["sources"] if x["source_id"] == SOURCE_ID)
    assert source["official_url"] == "https://www.vdv.de/301-2-18-sdes-v2-2-systemmonitoringservice.pdfx"
    assert pin["expected_sha256"] == PDF_SHA256
    assert int(pin["expected_size_bytes"]) == PDF_SIZE

    pdf = root / "local_sources/vdv_pdfs" / source["local_filename"]
    if not pdf.exists():
        fail(f"missing fetched PDF {pdf}")
    if pdf.stat().st_size != PDF_SIZE or sha256(pdf) != PDF_SHA256:
        fail("SMS V2.2 PDF byte pin mismatch")

    central = load_json(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    assert central["next_revalidation_block"] == "DRSMS22"
    by_id = {x["finding_id"]: x for x in central["inventory"]["entries"]}
    scope = ["DRSMS22-001", "DRSMS22-002", "DRSMS22-003", "DRSMS22-004"]
    for fid in scope:
        assert by_id[fid]["revalidation_state"] == "pending"
        assert by_id[fid]["terminal_state_source"] is None

    texts = {p: extract_page(pdf, p, text_dir) for p in TARGET_PAGES}
    require_any(*texts[5], 5, "Abbildungsverzeichnis", "Fehler! Textmarke nicht definiert")
    require_any(*texts[9], 9, "UnsubscribeServiceStatus", "UnsubscribeRequestStructure", "UnsubscribeResponseStructure")
    require_any(*texts[10], 10, "GetServiceStatus", "service state of all devices", "device state of all services")
    require_any(*texts[11], 11, "ServiceIdentificationWithStateList", "device state of all services")
    require_any(*texts[12], 12, "302-2", "SystemManagmentService")
    require_any(*texts[13], 13, "VDV 301-2-0", "SystemManagementService", "SystemDocumentationService")

    # DRSMS22-004 is a layout finding: in the exact operation-table segment,
    # the UnsubscribeServiceStatus structures are present but Req./Resp. labels
    # are absent before the table caption.
    layout9 = texts[9][0]
    start = layout9.find("UnsubscribeServiceStatus")
    end = layout9.find("Tabelle 1", start)
    if start < 0 or end < 0:
        fail("page 9: cannot isolate UnsubscribeServiceStatus table segment")
    segment = layout9[start:end]
    if "UnsubscribeRequestStructure" not in segment or "UnsubscribeResponseStructure" not in segment:
        fail("page 9: unsubscribe structures missing from isolated segment")
    if "Req." in segment or "Resp." in segment:
        fail("page 9: expected missing Req./Resp. labels are present in isolated segment")
    (out / "unsubscribe_service_status_segment.txt").write_text(segment, encoding="utf-8")

    render_hashes = {}
    for p in TARGET_PAGES:
        png = render_page(pdf, p, render_dir)
        render_hashes[str(p)] = {
            "sha256": sha256(png),
            "bytes": png.stat().st_size,
            "file": str(png.relative_to(out)),
        }

    service_tree = etree.parse(str(root / "IBIS-IP_SystemMonitoringService_V2.2.xsd"))
    common_tree = etree.parse(str(root / "IBIS-IP_common_V2.2.xsd"))
    ns = {"xs": XS}
    group_names = service_tree.xpath(
        "//xs:group[@name='SystemMonitoringServiceGroup']/xs:sequence/xs:element/@name",
        namespaces=ns,
    )
    assert "SystemMonitoringService.GetServiceStatusResponse" in group_names
    assert "SystemMonitoringService.GetSystemStatusResponse" not in group_names

    service_state_elems = common_tree.xpath(
        "//xs:complexType[@name='ServiceIdentificationWithStateStructure']//xs:element/@name",
        namespaces=ns,
    )
    assert "ServiceIdentification" in service_state_elems
    assert "ServiceState" in service_state_elems
    assert "DeviceState" not in service_state_elems

    ev116 = subprocess.run(["python", "tools/validate_sms_v22_ev116.py"], cwd=root, text=True, capture_output=True)
    (out / "ev116_rerun.log").write_text(ev116.stdout + ev116.stderr, encoding="utf-8")
    if ev116.returncode != 0:
        fail(f"EV-116 rerun failed\n{ev116.stdout}\n{ev116.stderr}")
    assert "PASSED: EV-116 official SMS V2.2 compile, naming boundary and generic-subscription structure evidence confirmed" in ev116.stdout

    states = {fid: "context_verified" for fid in scope}
    result = {
        "evidence_id": "EV-146",
        "result": "PASS",
        "scope": scope,
        "recommended_terminal_states": states,
        "authority": {
            "source_id": SOURCE_ID,
            "pdf_sha256": PDF_SHA256,
            "pdf_size_bytes": PDF_SIZE,
            "official_release_tag": "VDV-301-2.2",
            "sms_xsd_blob": SMS_XSD_BLOB,
            "common_v2_2_blob": COMMON_XSD_BLOB,
            "enumerations_v2_2_blob": ENUM_XSD_BLOB,
            "latest_xsd_wins": False,
        },
        "prior_executable_evidence": {
            "evidence_id": "EV-116",
            "run_id": EV116_RUN,
            "job_id": EV116_JOB,
            "rerun_result": "PASS",
        },
        "fresh_visual_pages": TARGET_PAGES,
        "fresh_render_hashes": render_hashes,
        "finding_checks": {
            "DRSMS22-001": "page 5 visibly/extractably contains the broken list-of-figures bookmark text 'Fehler! Textmarke nicht definiert.'",
            "DRSMS22-002": "pages 10-11 use device wording in ServiceStatus prose while exact Common V2.2 ServiceIdentificationWithStateStructure contains ServiceIdentification plus ServiceState and no DeviceState",
            "DRSMS22-003": "page 12 spells SystemManagementService as SystemManagmentService while page 13 prints the correct service name",
            "DRSMS22-004": "page 9 operation-table segment contains UnsubscribeServiceStatus request/response structures but no Req./Resp. labels before the table caption",
        },
        "active_disproof": {
            "DRSMS22-001": "text-extraction-artifact hypothesis rejected by exact pinned source plus fresh render and extracted printed string",
            "DRSMS22-002": "device-oriented-service-semantics hypothesis rejected by ServiceStatus operation naming and exact Common ServiceState structure",
            "DRSMS22-003": "intentional alternate service-name hypothesis rejected by the correctly spelled SystemManagementService reference on page 13",
            "DRSMS22-004": "missing-structure hypothesis rejected; both structures are present, narrowing the finding to omitted table labels only",
        },
        "choice_notation_guard": "SMS response-table a/b -1:1 notation is XML choice notation and is not promoted as a cardinality defect",
        "executable_xml_evidence_reason_not_applicable": "All four DRSMS22 findings are documentation/layout/terminology findings. EV-116 is rerun only as exact-authority support, not because the findings alter XML acceptance behaviour.",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
    }
    (out / "ev146_results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED: EV-146 DRSMS22 legacy finding revalidation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
