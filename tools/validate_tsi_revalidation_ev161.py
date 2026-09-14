#!/usr/bin/env python3
"""EV-161: fail-closed revalidation evidence for TSI-001.

TSI-001 concerns the official TrainSetInformationService V2.1 modelling of
GetTrainSetCompositionResponse: the writing requires a sequence of coach data
sets (one per coach), while the exact V2.1 XSD contains a single flat coach
record. V2.2 introduces a repeated SingleCoach wrapper; that later correction
is explanatory history only and is not back-applied to V2.1.

This validator does not mutate any XSD or audit state. EV-109 is rerun by CI as
an independent executable control.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

from lxml import etree

SOURCE_RUN = 34816735900
SOURCE_JOB = 103888867262
SOURCE_ARTIFACT = 10336466475
SOURCE_DIGEST = "sha256:30089b9d4f2c86dd57f8bb184844a428ee08e91b0d327517c84f6689ea231bfb"
SOURCE_HEAD = "20785d8ee41e812a5902d49b6d4b800ef238e311"

PDF_SHA256 = "8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e"
PDF_BYTES = 1708401
PDF_PAGES = 51
PDF_FULL_TEXT_SHA256 = "81a051867f271b03c841b0d1d391dfd07209c13c73789cf5f8a8af79987ee13c"
PAGE_HASHES = {
    24: "f27104104999fe9c4e858f38a5b1061bed6ab079ab37cf20daca0146c57d15a9",
    25: "32ab156d5f634c5943bf390fa92c56b5370664f1693c99ec0e905696e211aef6",
}

TARGET_STATE = "executable_confirmed"
XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}


def fail(message: str) -> None:
    raise AssertionError(message)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)
    print(f"OK  {message}")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def text_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def pdftotext(pdf: Path, page: int | None = None) -> str:
    with tempfile.NamedTemporaryFile(suffix=".txt") as tmp:
        cmd = ["pdftotext", "-layout"]
        if page is not None:
            cmd += ["-f", str(page), "-l", str(page)]
        cmd += [str(pdf), tmp.name]
        subprocess.run(cmd, check=True)
        return Path(tmp.name).read_text(encoding="utf-8")


def pdf_pages(pdf: Path) -> int:
    proc = subprocess.run(["pdfinfo", str(pdf)], check=True, text=True, capture_output=True)
    for line in proc.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    fail("pdfinfo did not return page count")
    return -1


def collect_findings(value) -> list[dict]:
    out: list[dict] = []
    if isinstance(value, dict):
        if {"finding_id", "revalidation_state", "terminal_state_source"} <= set(value):
            out.append(value)
        for child in value.values():
            out.extend(collect_findings(child))
    elif isinstance(value, list):
        for child in value:
            out.extend(collect_findings(child))
    return out


def assert_tokens(text: str, tokens: list[str], label: str) -> None:
    missing = [token for token in tokens if token not in text]
    require(not missing, f"{label} contains required semantic tokens" + (f"; missing={missing}" if missing else ""))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--source-evidence-dir", type=Path, required=True)
    ap.add_argument("--pdf", type=Path, required=True)
    ap.add_argument("--output-dir", type=Path, required=True)
    args = ap.parse_args()

    root = args.repo_root.resolve()
    output = args.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)

    state = json.loads((root / "00_START_HERE/CURRENT_STATE.json").read_text(encoding="utf-8"))
    registry = json.loads((root / "audit_registry/finding_revalidation_registry_v0.1.json").read_text(encoding="utf-8"))
    audit = state["audit"]

    require(state["canonical_branch"] == "dev/schema-integration", "canonical branch is dev/schema-integration")
    require(audit["finding_inventory_count"] == 192, "frozen finding inventory count is 192")
    require(audit["finding_revalidation_completed_findings"] == 161, "prestate terminal count is 161")
    require(audit["finding_revalidation_pending_findings"] == 31, "prestate pending count is 31")
    require(audit["finding_revalidation_next_block"] == "TSI", "prestate next block is TSI")
    require(audit["finding_revalidation_latest_completed_block"] == "TSD", "latest completed block is TSD")
    require(audit["latest_executable_evidence_id"] == "EV-160", "latest executable evidence before TSI is EV-160")
    require(registry["next_revalidation_block"] == "TSI", "registry next block is TSI")

    findings = collect_findings(registry)
    by_id: dict[str, dict] = {}
    for item in findings:
        fid = item["finding_id"]
        require(fid not in by_id, f"finding {fid} occurs once in ordered registry")
        by_id[fid] = item
    require(len(by_id) == 192, "registry contains exactly 192 ordered finding states")
    pending = [item["finding_id"] for item in findings if item["revalidation_state"] == "pending"]
    require(len(pending) == 31, "registry contains exactly 31 pending findings")
    require(pending[0] == "TSI-001", "first pending finding is TSI-001")
    require(by_id["TSI-001"]["revalidation_state"] == "pending", "TSI-001 is still pending before EV-161 closure")
    require(by_id["TSI-001"]["terminal_state_source"] is None, "TSI-001 has no premature terminal source")

    projected = [(item["finding_id"], TARGET_STATE if item["finding_id"] == "TSI-001" else item["revalidation_state"]) for item in findings]
    projected_pending = [fid for fid, status in projected if status == "pending"]
    require(len(projected_pending) == 30, "projected post-TSI pending count is dynamically 30")
    require(192 - len(projected_pending) == 162, "projected post-TSI terminal count is dynamically 162")
    require(projected_pending[0] == "TSM-001", "projected next finding is TSM-001")

    source_manifest = json.loads((args.source_evidence_dir / "manifest.json").read_text(encoding="utf-8"))
    require(source_manifest["evidence"] == "EV-160 source acquisition", "reused source artifact identifies EV-160 source acquisition")
    require(source_manifest["head_sha"] == SOURCE_HEAD, "reused source artifact head SHA is exact")
    src = source_manifest["sources"]["TRAINSET_V2.1"]
    require(src["pdf_sha256"] == PDF_SHA256, "source artifact TrainSet V2.1 PDF hash is exact")
    require(src["pdf_bytes"] == PDF_BYTES, "source artifact TrainSet V2.1 byte count is exact")
    require(src["pages"] == PDF_PAGES, "source artifact TrainSet V2.1 page count is exact")
    require(src["full_text_sha256"] == PDF_FULL_TEXT_SHA256, "source artifact TrainSet V2.1 text fingerprint is exact")
    require(sha256(args.source_evidence_dir / "pdfs/TRAINSET_V2.1.pdf") == PDF_SHA256, "source artifact embeds exact TrainSet V2.1 PDF")

    require(args.pdf.is_file(), "TrainSet V2.1 PDF exists")
    require(sha256(args.pdf) == PDF_SHA256, "TrainSet V2.1 PDF SHA-256 is exact")
    require(args.pdf.stat().st_size == PDF_BYTES, "TrainSet V2.1 PDF byte count is exact")
    require(pdf_pages(args.pdf) == PDF_PAGES, "TrainSet V2.1 PDF page count is exact")
    full_text = pdftotext(args.pdf)
    require(text_sha256(full_text) == PDF_FULL_TEXT_SHA256, "TrainSet V2.1 full layout-text fingerprint is exact")

    page24 = pdftotext(args.pdf, 24)
    page25 = pdftotext(args.pdf, 25)
    require(text_sha256(page24) == PAGE_HASHES[24], "TrainSet V2.1 physical page 24 fingerprint is exact")
    require(text_sha256(page25) == PAGE_HASHES[25], "TrainSet V2.1 physical page 25 fingerprint is exact")
    assert_tokens(page24, [
        "Each coach data set consists of the following information:",
        "CoachType", "CoachNumber", "FrontCabin", "RearCabin",
        "CoachPositionInTrainSet", "CoupledSide", "CoachState",
    ], "TSI-001 page 24 coach-data-set definition")
    assert_tokens(page25, [
        "returns a sequence of coach data sets,", "one per coach.",
        "TrainSetInformationService.GetTrainSetCompositionResponseStructure",
    ], "TSI-001 page 25 multi-coach statement")

    v21_path = root / "IBIS-IP_TrainSetInformationService_V2.1.xsd"
    v22_path = root / "IBIS-IP_TrainSetInformationService_V2.2.xsd"
    v21 = etree.parse(str(v21_path))
    v22 = etree.parse(str(v22_path))
    schema21 = etree.XMLSchema(v21)
    etree.XMLSchema(v22)

    seq21 = v21.xpath(
        "/xs:schema/xs:complexType[@name='TrainSetInformationService.GetTrainSetCompositionResponseStructure']/xs:sequence",
        namespaces=NS,
    )
    require(len(seq21) == 1, "V2.1 response structure has exactly one sequence")
    elems21 = seq21[0].xpath("./xs:element", namespaces=NS)
    names21 = [e.get("name") for e in elems21]
    require(names21 == ["CoachType", "CoachNumber", "FrontCabin", "RearCabin", "CoachPositionInTrainSet", "CoupledSide", "CoachState"], "V2.1 response is the exact flat coach-field sequence")
    require(all(e.get("maxOccurs", "1") == "1" for e in elems21), "V2.1 has no repeated coach wrapper or repeated coach field")

    single22 = v22.xpath(
        "/xs:schema/xs:complexType[@name='TrainSetInformationService.GetTrainSetCompositionResponseStructure']/xs:sequence/xs:element[@name='SingleCoach']",
        namespaces=NS,
    )
    require(len(single22) == 1, "V2.2 introduces exactly one SingleCoach wrapper declaration")
    require(single22[0].get("type") == "SingleCoachInATrainSet", "V2.2 SingleCoach uses SingleCoachInATrainSet")
    require(single22[0].get("maxOccurs") == "unbounded", "V2.2 SingleCoach wrapper is repeatable")

    one = '''<TrainSetInformationService.GetTrainSetCompositionResponse>
  <CoachNumber><Value>coach-1</Value></CoachNumber>
  <FrontCabin><Value>A</Value></FrontCabin>
  <RearCabin><Value>B</Value></RearCabin>
  <CoachPositionInTrainSet><Value>1</Value></CoachPositionInTrainSet>
  <CoupledSide>A</CoupledSide>
  <CoachState>Master</CoachState>
</TrainSetInformationService.GetTrainSetCompositionResponse>'''
    two = '''<TrainSetInformationService.GetTrainSetCompositionResponse>
  <CoachNumber><Value>coach-1</Value></CoachNumber>
  <FrontCabin><Value>A</Value></FrontCabin>
  <RearCabin><Value>B</Value></RearCabin>
  <CoachPositionInTrainSet><Value>1</Value></CoachPositionInTrainSet>
  <CoupledSide>A</CoupledSide>
  <CoachState>Master</CoachState>
  <CoachNumber><Value>coach-2</Value></CoachNumber>
  <FrontCabin><Value>A</Value></FrontCabin>
  <RearCabin><Value>B</Value></RearCabin>
  <CoachPositionInTrainSet><Value>2</Value></CoachPositionInTrainSet>
  <CoupledSide>B</CoupledSide>
  <CoachState>Slave</CoachState>
</TrainSetInformationService.GetTrainSetCompositionResponse>'''
    require(schema21.validate(etree.fromstring(one.encode("utf-8"))), "V2.1 validates one flat coach record")
    require(not schema21.validate(etree.fromstring(two.encode("utf-8"))), "V2.1 rejects a second PDF-described coach record")

    manifest = {
        "evidence_id": "EV-161",
        "scope": ["TSI-001"],
        "source_acquisition": {
            "reused_from": "EV-160 source acquisition",
            "run_id": SOURCE_RUN,
            "job_id": SOURCE_JOB,
            "artifact_id": SOURCE_ARTIFACT,
            "artifact_digest": SOURCE_DIGEST,
            "head_sha": SOURCE_HEAD,
        },
        "prestate": {"terminal": 161, "pending": 31, "first_pending": "TSI-001", "next_block": "TSI", "latest_evidence": "EV-160"},
        "target_state": {"TSI-001": TARGET_STATE},
        "projected_poststate": {"terminal": 162, "pending": 30, "first_pending": "TSM-001", "next_block": "TSM"},
        "pdf": {
            "sha256": PDF_SHA256,
            "size_bytes": PDF_BYTES,
            "pages": PDF_PAGES,
            "visual_pages": [24, 25],
            "page_text_sha256": {str(k): v for k, v in PAGE_HASHES.items()},
        },
        "xsd_authority": {
            "v2_1_blob": "897f373e31b76aa23d8bc206854b042524e4c102",
            "v2_2_historical_correction_blob": "7ab1f8f892bfcea2a8b8a055f07de92c143356f9",
            "latest_wins": False,
        },
        "controls": ["EV-109", "50-root-XSD regression pool"],
        "xsd_mutation": False,
        "audit_state_mutation": False,
        "closure_authorized_only_after_ci_success": True,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASSED: EV-161 TSI-001 revalidation gate; projected 162/192 terminal, 30 pending, next TSM-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
