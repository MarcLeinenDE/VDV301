#!/usr/bin/env python3
"""EV-148: fail-closed revalidation of DRTRAINSET21-001..003.

The three findings are documentation/prose defects in VDV 301-2-14 TrainSet
Services V2.1. Exact V2.1 XSD inventories and EV-109 are used as counter-context,
not to turn documentation-only findings into schema defects.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

from lxml import etree

SOURCE_ID = "TRAINSET_V2.1"
PDF_SHA256 = "8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e"
PDF_SIZE = 1708401
ORIGINAL_PIN_EVIDENCE_RUN = "33226637254"
OFFICIAL_URL = "https://www.vdv.de/vdv-301-2-14-v2-1-sds-trainsetservices.pdfx"
LOCAL_FILENAME = "TRAINSET_V2.1.pdf"
FROZEN_INVENTORY_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
DEEP_READ_BLOB = "6d5680f438e7e592aaf1d056e39224e7c2a3f2d9"
EV109_BLOB = "f88208bff7e39bb38a86a310dc121f486984f807"
XSD_BLOBS = {
    "IBIS-IP_TrainSetInformationService_V2.1.xsd": "897f373e31b76aa23d8bc206854b042524e4c102",
    "IBIS-IP_TrainSetManagementService_V2.1.xsd": "add9d1cb37e5759ff7a77855b239108d38373206",
    "IBIS-IP_TrainSetDataService_V2.1.xsd": "c2cdb73fcae265a2e4e0349ac6072e3548e36d8b",
}
EVIDENCE_PAGES = [6, 9, 10, 44]
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}


def fail(msg: str) -> None:
    raise AssertionError(msg)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob(root: Path, rel: str) -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"HEAD:{rel}"], cwd=root, text=True
    ).strip()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def norm(text: str) -> str:
    text = text.replace("\u00ad", "")
    return re.sub(r"\s+", "", text).lower()


def require(text: str, label: str, *tokens: str) -> None:
    n = norm(text)
    missing = [token for token in tokens if norm(token) not in n]
    if missing:
        fail(f"{label}: missing tokens {missing}")


def extract_page(pdf: Path, page: int, out_dir: Path) -> tuple[str, str]:
    layout_target = out_dir / f"page-{page:02d}-layout.txt"
    raw_target = out_dir / f"page-{page:02d}-raw.txt"
    subprocess.run(
        ["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(pdf), str(layout_target)],
        check=True,
    )
    subprocess.run(
        ["pdftotext", "-raw", "-f", str(page), "-l", str(page), str(pdf), str(raw_target)],
        check=True,
    )
    return (
        layout_target.read_text(encoding="utf-8", errors="replace"),
        raw_target.read_text(encoding="utf-8", errors="replace"),
    )


def render_page(pdf: Path, page: int, out_dir: Path) -> Path:
    prefix = out_dir / f"page-{page:02d}"
    subprocess.run(
        [
            "pdftoppm", "-f", str(page), "-l", str(page), "-singlefile",
            "-png", "-r", "180", str(pdf), str(prefix),
        ],
        check=True,
    )
    png = prefix.with_suffix(".png")
    if not png.exists() or png.stat().st_size == 0:
        fail(f"render missing for physical PDF page {page}")
    return png


def combined(pair: tuple[str, str]) -> str:
    return pair[0] + "\n" + pair[1]


def group_names(root: Path, filename: str, group_name: str) -> set[str]:
    tree = etree.parse(str(root / filename))
    names = {
        x.get("name")
        for x in tree.xpath(
            f"/xs:schema/xs:group[@name='{group_name}']//xs:element",
            namespaces=NS,
        )
        if x.get("name")
    }
    if not names:
        fail(f"no operation-group elements found in {filename}:{group_name}")
    return names


def global_names(root: Path, filename: str) -> set[str]:
    tree = etree.parse(str(root / filename))
    return {
        x.get("name")
        for x in tree.xpath("/xs:schema/xs:element", namespaces=NS)
        if x.get("name")
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--output-dir", default="artifacts/ev148")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    out = (root / args.output_dir).resolve()
    text_dir = out / "page_text"
    render_dir = out / "renders"
    text_dir.mkdir(parents=True, exist_ok=True)
    render_dir.mkdir(parents=True, exist_ok=True)

    guards = {
        "audit_registry/finding_inventory_frozen_2026-09-03.json": FROZEN_INVENTORY_BLOB,
        "docs/pdf_xsd_semantic_audit/deep_read/TRAINSET_V2.1.md": DEEP_READ_BLOB,
        "tools/validate_trainset_v21_ev109.py": EV109_BLOB,
        **XSD_BLOBS,
    }
    for rel, expected in guards.items():
        actual = git_blob(root, rel)
        if actual != expected:
            fail(f"canonical authority changed: {rel}: {actual} != {expected}")

    sources = load_json(root / "audit_registry/pdf_source_registry_v0.1.json")
    pins = load_json(root / "audit_registry/pdf_source_pins_v0.1.json")
    source = next(x for x in sources["sources"] if x["source_id"] == SOURCE_ID)
    pin = next(x for x in pins["sources"] if x["source_id"] == SOURCE_ID)
    assert source["official_url"] == OFFICIAL_URL
    assert source["local_filename"] == LOCAL_FILENAME
    assert pin["expected_sha256"] == PDF_SHA256
    assert int(pin["expected_size_bytes"]) == PDF_SIZE
    assert str(pin["evidence_run_id"]) == ORIGINAL_PIN_EVIDENCE_RUN
    assert pin["deep_read_source_ready"] is True

    pdf = root / "local_sources/vdv_pdfs" / LOCAL_FILENAME
    if not pdf.exists():
        fail(f"missing fetched/recovered PDF {pdf}")
    if pdf.stat().st_size != PDF_SIZE or sha256(pdf) != PDF_SHA256:
        fail("TRAINSET V2.1 PDF byte pin mismatch")

    central = load_json(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    assert central["next_revalidation_block"] == "DRTRAINSET21"
    scope = ["DRTRAINSET21-001", "DRTRAINSET21-002", "DRTRAINSET21-003"]
    by_id = {x["finding_id"]: x for x in central["inventory"]["entries"]}
    for fid in scope:
        assert by_id[fid]["revalidation_state"] == "pending"
        assert by_id[fid]["terminal_state_source"] is None

    texts = {p: extract_page(pdf, p, text_dir) for p in EVIDENCE_PAGES}
    p6 = combined(texts[6])
    p9 = combined(texts[9])
    p10 = combined(texts[10])
    p44 = combined(texts[44])

    # DRTRAINSET21-001: the overview's fifth item says the service-interaction
    # examples are in 9.1. The same document's TOC identifies 9.1 as the
    # driving-direction re-initialisation subsection and section 10 as Examples.
    require(
        p9,
        "physical PDF page 9 German overview",
        "Anhand von Beispielen wird das Zusammenspiel der verschiedenen Dienste erläutert",
        "Abschnitt 9.1",
    )
    require(
        p10,
        "physical PDF page 10 English overview",
        "By means of examples the interaction of the different services is explained",
        "section 9.1",
    )
    require(
        p6,
        "physical PDF page 6 table of contents",
        "9.1 Re-initialisation of Service Communication when a Trainset changes the Driving Direction",
        "10 Examples",
        "10.1 The master OBU requests the Status of Devices in a Slave Coach",
    )

    # DRTRAINSET21-002/-003: page 44 visibly contains both the misspelled
    # operation and a claim that equally named composition operations belong to
    # TrainSetDataService.
    require(
        p44,
        "physical PDF page 44 coach-network guidance",
        "GetTrainSetCompositon operation",
        "SubscribeTrainSetComposition operation",
        "both provided by the TrainSetInformationService",
        "equally named operations of the TrainSetDataService",
    )

    tsi_group = group_names(root, "IBIS-IP_TrainSetInformationService_V2.1.xsd", "TrainSetInformationServiceOperations")
    tsm_group = group_names(root, "IBIS-IP_TrainSetManagementService_V2.1.xsd", "TrainSetManagementServiceOperations")
    tsd_group = group_names(root, "IBIS-IP_TrainSetDataService_V2.1.xsd", "TrainSetDataServiceOperations")
    tsi_global = global_names(root, "IBIS-IP_TrainSetInformationService_V2.1.xsd")
    tsm_global = global_names(root, "IBIS-IP_TrainSetManagementService_V2.1.xsd")
    tsd_global = global_names(root, "IBIS-IP_TrainSetDataService_V2.1.xsd")

    correct_tsi_response = "TrainSetInformationService.GetTrainSetCompositionResponse"
    typo_tsi = "TrainSetInformationService.GetTrainSetCompositon"
    assert correct_tsi_response in tsi_group and correct_tsi_response in tsi_global
    assert typo_tsi not in tsi_group and typo_tsi not in tsi_global

    # The exact TrainSetDataService authority is TripRef/TripInformation-only;
    # there are no composition operation names at all.
    assert not any("TrainSetComposition" in name for name in tsd_group)
    assert not any("TrainSetComposition" in name for name in tsd_global)
    assert {
        "TrainSetDataService.RetrieveTripRefRequest",
        "TrainSetDataService.RetrieveTripRefResponse",
        "TrainSetDataService.RetrieveTripInformationRequest",
        "TrainSetDataService.RetrieveTripInformationResponse",
    } <= tsd_group

    # Positive neighbouring-service control: TrainSetManagementService V2.1
    # does contain composition-service context in its exact schema.
    assert "TrainSetManagementService.GetTrainSetComposition" in tsm_group
    assert "TrainSetManagementService.GetTrainSetComposition" in tsm_global

    render_hashes = {}
    for p in EVIDENCE_PAGES:
        png = render_page(pdf, p, render_dir)
        render_hashes[str(p)] = {
            "sha256": sha256(png),
            "bytes": png.stat().st_size,
            "file": str(png.relative_to(out)),
        }

    states = {fid: "context_verified" for fid in scope}
    result = {
        "evidence_id": "EV-148",
        "result": "PASS",
        "scope": scope,
        "recommended_terminal_states": states,
        "source_id": SOURCE_ID,
        "authority": {
            "publication": "VDV 301-2-14 TrainSet Services V2.1, 05/2018",
            "official_url": OFFICIAL_URL,
            "pdf_sha256": PDF_SHA256,
            "pdf_size_bytes": PDF_SIZE,
            "original_pin_evidence_run": ORIGINAL_PIN_EVIDENCE_RUN,
            "deep_read_blob": DEEP_READ_BLOB,
            "xsd_blobs": XSD_BLOBS,
            "ev109_blob": EV109_BLOB,
            "latest_xsd_wins_applicable": False,
        },
        "finding_checks": {
            "DRTRAINSET21-001": "German and English overview text points service-interaction examples to section 9.1, while the same publication's TOC identifies 9.1 as driving-direction re-initialisation and section 10 as Examples.",
            "DRTRAINSET21-002": "Physical page 44 attributes equally named composition operations to TrainSetDataService; exact V2.1 TrainSetDataService operation/global inventories contain no TrainSetComposition operation, while TrainSetManagementService contains composition context.",
            "DRTRAINSET21-003": "Physical page 44 prints GetTrainSetCompositon; exact TrainSetInformationService authority uses Composition and contains no Compositon alias.",
        },
        "active_disproof": {
            "DRTRAINSET21-001": "A literal reading that 9.1 itself contains an example-based re-initialisation use case was considered. It does, but overview item 4 already assigns re-initialisation to sections 7 and 9, while item 5 separately introduces examples of service interaction; the dedicated section 10 is explicitly titled Examples and contains multiple cross-service use cases. The 9.1 pointer is therefore retained as a stale/wrong cross-reference.",
            "DRTRAINSET21-002": "An alternate-alias interpretation was rejected: exact V2.1 TrainSetDataService has only TripRef/TripInformation operation roots and no TrainSetComposition name. The neighbouring TrainSetManagementService has composition context, so the printed TrainSetDataService attribution is not a valid service alias.",
            "DRTRAINSET21-003": "An alternate operation spelling was rejected: exact V2.1 TrainSetInformationService uses GetTrainSetCompositionResponse, and the publication elsewhere consistently uses Composition. No Compositon declaration or alias exists.",
        },
        "executable_evidence": {
            "required_for_terminal_state": False,
            "reason": "All three findings are documentation/navigation/name-context findings; XML validation behaviour is not materially changed by their terminal state.",
            "counter_context": "EV-109 is rerun separately by the workflow to confirm the exact V2.1 schema family remains executable and unchanged.",
        },
        "xsd_operation_inventory": {
            "TrainSetInformationService_group": sorted(tsi_group),
            "TrainSetManagementService_group": sorted(tsm_group),
            "TrainSetDataService_group": sorted(tsd_group),
        },
        "fresh_visual_physical_pages": EVIDENCE_PAGES,
        "fresh_render_hashes": render_hashes,
        "manual_visual_review_status": "pending_human_inspection_of_EV148_artifact_before_registry_closure",
        "text_extraction_modes": ["pdftotext-layout", "pdftotext-raw"],
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
    }
    (out / "ev148_results.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED: EV-148 DRTRAINSET21 revalidation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
