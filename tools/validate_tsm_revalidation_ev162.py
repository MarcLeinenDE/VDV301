#!/usr/bin/env python3
"""EV-162: fail-closed revalidation evidence for TSM-001..TSM-003.

The block combines exact official TrainSetServices V2.1/V2.2 writings with the
matching official TrainSetManagementService schemas. EV-109 independently
covers the V2.1 response-root behaviour and EV-104 independently covers the
V2.2 global-root/operation-group mismatch. TSM-003 is documentation-only and
uses a byte-pinned visual gate for the stale embedded page-31 XSD diagram.

No XSD or audit state is mutated by this validator.
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

PDF = {
    "v21": {
        "sha256": "8eb53f2e960d125382e22d9c58dff8685c041001cf39a87ed4d12bb266bbe12e",
        "bytes": 1708401,
        "pages": 51,
        "full_text_sha256": "81a051867f271b03c841b0d1d391dfd07209c13c73789cf5f8a8af79987ee13c",
        "page_hashes": {30: "cd92cce547f5614c9010d7ffdb4acba3032395ffa8752ee33745c7966b39dcb8"},
    },
    "v22": {
        "sha256": "c1946694a1809933a9a4a23adff1c551effdb0a2fbc6a7f7f68faec0b0c7bd6e",
        "bytes": 1744296,
        "pages": 54,
        "full_text_sha256": "a4480d9a425c55ca3e488136d64c5c367e924144dd53dadd677f7a5ae4711882",
        "page_hashes": {
            31: "f7da20532d693569c3f03f208e802d504f7f0d049f8308467f98f45e4881378d",
            51: "fef217acc534eeb09e9072f07092544f3786d53cf63c3e33a1e5c787243b3427",
        },
    },
}

TARGET_STATES = {
    "TSM-001": "executable_confirmed",
    "TSM-002": "executable_confirmed",
    "TSM-003": "context_verified",
}

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
    fail(f"pdfinfo did not return page count for {pdf}")
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


def inspect_schema(path: Path) -> tuple[dict[str, str | None], dict[str, str | None], etree._ElementTree]:
    tree = etree.parse(str(path))
    etree.XMLSchema(tree)
    globals_ = {n.get("name"): n.get("type") for n in tree.xpath("/xs:schema/xs:element", namespaces=NS)}
    group = {
        n.get("name"): n.get("type")
        for n in tree.xpath("/xs:schema/xs:group[@name='TrainSetManagementServiceOperations']//xs:element", namespaces=NS)
    }
    return globals_, group, tree


def check_pdf(label: str, path: Path, spec: dict) -> dict[int, str]:
    require(path.is_file(), f"{label} PDF exists")
    require(sha256(path) == spec["sha256"], f"{label} PDF SHA-256 is exact")
    require(path.stat().st_size == spec["bytes"], f"{label} PDF byte count is exact")
    require(pdf_pages(path) == spec["pages"], f"{label} PDF page count is exact")
    full = pdftotext(path)
    require(text_sha256(full) == spec["full_text_sha256"], f"{label} full layout-text fingerprint is exact")
    pages: dict[int, str] = {}
    for page, expected in spec["page_hashes"].items():
        text = pdftotext(path, page)
        require(text_sha256(text) == expected, f"{label} physical page {page} fingerprint is exact")
        pages[page] = text
    return pages


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", type=Path, required=True)
    ap.add_argument("--source-evidence-dir", type=Path, required=True)
    ap.add_argument("--v21-pdf", type=Path, required=True)
    ap.add_argument("--v22-pdf", type=Path, required=True)
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
    require(audit["finding_revalidation_completed_findings"] == 162, "prestate terminal count is 162")
    require(audit["finding_revalidation_pending_findings"] == 30, "prestate pending count is 30")
    require(audit["finding_revalidation_next_block"] == "TSM", "prestate next block is TSM")
    require(audit["finding_revalidation_latest_completed_block"] == "TSI", "latest completed block is TSI")
    require(audit["latest_executable_evidence_id"] == "EV-161", "latest executable evidence before TSM is EV-161")
    require(registry["next_revalidation_block"] == "TSM", "registry next block is TSM")

    findings = collect_findings(registry)
    ids = [x["finding_id"] for x in findings]
    require(len(ids) == len(set(ids)) == 192, "registry contains exactly 192 unique ordered finding states")
    by_id = {x["finding_id"]: x for x in findings}
    pending = [x["finding_id"] for x in findings if x["revalidation_state"] == "pending"]
    require(len(pending) == 30 and pending[0] == "TSM-001", "registry prestate has 30 pending with TSM-001 first")
    for fid in TARGET_STATES:
        require(by_id[fid]["revalidation_state"] == "pending" and by_id[fid]["terminal_state_source"] is None, f"{fid} has no premature terminal state")

    projected = [(x["finding_id"], TARGET_STATES.get(x["finding_id"], x["revalidation_state"])) for x in findings]
    projected_pending = [fid for fid, status in projected if status == "pending"]
    require(len(projected_pending) == 27, "projected post-TSM pending count is dynamically 27")
    require(192 - len(projected_pending) == 165, "projected post-TSM terminal count is dynamically 165")
    require(projected_pending[0] == "TVS-001", "projected next finding is TVS-001")

    source_manifest = json.loads((args.source_evidence_dir / "manifest.json").read_text(encoding="utf-8"))
    require(source_manifest["evidence"] == "EV-160 source acquisition", "reused source artifact identifies EV-160 acquisition")
    require(source_manifest["head_sha"] == SOURCE_HEAD, "reused source artifact head SHA is exact")
    for source_key, spec_key in (("TRAINSET_V2.1", "v21"), ("TRAINSET_V2.2", "v22")):
        src = source_manifest["sources"][source_key]
        spec = PDF[spec_key]
        require(src["pdf_sha256"] == spec["sha256"], f"source artifact {source_key} hash is exact")
        require(src["pdf_bytes"] == spec["bytes"], f"source artifact {source_key} byte count is exact")
        require(src["pages"] == spec["pages"], f"source artifact {source_key} page count is exact")
        require(src["full_text_sha256"] == spec["full_text_sha256"], f"source artifact {source_key} text fingerprint is exact")

    v21_pages = check_pdf("TrainSet V2.1", args.v21_pdf, PDF["v21"])
    v22_pages = check_pdf("TrainSet V2.2", args.v22_pdf, PDF["v22"])

    assert_tokens(v21_pages[30], [
        "5.5.3   GetTrainSetComposition",
        "GetTrainSetCompositionResponseStructure of the",
        "TrainSetInformationService is used.",
    ], "TSM-001 V2.1 page 30")
    assert_tokens(v22_pages[51], [
        "TrainSetManagementService.GetTrainSetCompositionResponse instead",
        "of TrainSetManagementService.GetTrainSetComposition",
        "now correctly entitled",
    ], "TSM-001/002 V2.2 correction history page 51")

    v21_globals, v21_group, _ = inspect_schema(root / "IBIS-IP_TrainSetManagementService_V2.1.xsd")
    old = "TrainSetManagementService.GetTrainSetComposition"
    corrected = "TrainSetManagementService.GetTrainSetCompositionResponse"
    response_type = "TrainSetInformationService.GetTrainSetCompositionResponseStructure"
    require(v21_globals.get(old) == response_type and v21_group.get(old) == response_type, "TSM-001 V2.1 exact XSD uses old root in both global and operation-group contexts")
    require(corrected not in v21_globals and corrected not in v21_group, "TSM-001 later corrected root is absent from exact V2.1 XSD")

    assert_tokens(v22_pages[31], [
        "5.5.3   GetTrainSetComposition",
        "GetTrainSetCompositionResponseStructure of the",
        "TrainSetInformationService is used.",
    ], "TSM-002/003 V2.2 page 31 prose")
    print("OK  TSM-002/003 page 31 embedded XSD graphics are byte-pinned visual evidence; diagram labels are not a Poppler text gate")

    v22_globals, v22_group, _ = inspect_schema(root / "IBIS-IP_TrainSetManagementService_V2.2.xsd")
    require(v22_globals.get(corrected) == response_type, "TSM-002 V2.2 corrected global response root exists")
    require(old not in v22_globals, "TSM-002 stale old name is absent as V2.2 global root")
    require(v22_group.get(old) == response_type, "TSM-002 V2.2 operation group still contains stale old name")
    require(corrected not in v22_group, "TSM-002 V2.2 operation group still lacks corrected response name")

    tsi22 = etree.parse(str(root / "IBIS-IP_TrainSetInformationService_V2.2.xsd"))
    etree.XMLSchema(tsi22)
    immediate = tsi22.xpath(
        "/xs:schema/xs:complexType[@name='TrainSetInformationService.GetTrainSetCompositionResponseStructure']/xs:sequence/xs:element",
        namespaces=NS,
    )
    require(len(immediate) == 1 and immediate[0].get("name") == "SingleCoach", "TSM-003 exact reused V2.2 response structure has SingleCoach as its immediate child")
    require(immediate[0].get("type") == "SingleCoachInATrainSet" and immediate[0].get("maxOccurs") == "unbounded", "TSM-003 exact V2.2 SingleCoach wrapper is repeatable and typed correctly")

    deep_read = (root / "docs/pdf_xsd_semantic_audit/deep_read/TRAINSET_V2.2.md").read_text(encoding="utf-8")
    assert_tokens(deep_read, [
        "TSM-003 - stale V2.1-style composition diagram on page 31",
        "It does not show the V2.2 repeated `SingleCoach -> SingleCoachInATrainSet` wrapper",
        "this is not merely a collapsed wrapper view",
    ], "TSM-003 independent visual-review record")

    manifest = {
        "evidence_id": "EV-162",
        "scope": ["TSM-001", "TSM-002", "TSM-003"],
        "source_acquisition": {
            "reused_from": "EV-160 source acquisition",
            "run_id": SOURCE_RUN,
            "job_id": SOURCE_JOB,
            "artifact_id": SOURCE_ARTIFACT,
            "artifact_digest": SOURCE_DIGEST,
            "head_sha": SOURCE_HEAD,
        },
        "prestate": {"terminal": 162, "pending": 30, "first_pending": "TSM-001", "next_block": "TSM", "latest_evidence": "EV-161"},
        "target_states": TARGET_STATES,
        "projected_poststate": {"terminal": 165, "pending": 27, "first_pending": "TVS-001", "next_block": "TVS"},
        "pdfs": {
            "TRAINSET_V2.1": {**PDF["v21"], "visual_pages": [30]},
            "TRAINSET_V2.2": {**PDF["v22"], "visual_pages": [31, 51], "page_31_embedded_diagram_evidence_mode": "visual_not_Poppler_text"},
        },
        "xsd_authority": {
            "TSM_V2.1_blob": "add9d1cb37e5759ff7a77855b239108d38373206",
            "TSM_V2.2_blob": "da9465d6683e3f7d54a546ab4a13739fb3c3e902",
            "TSI_V2.2_blob": "7ab1f8f892bfcea2a8b8a055f07de92c143356f9",
            "latest_wins": False,
        },
        "controls": ["EV-109", "EV-104", "50-root-XSD regression pool"],
        "xsd_mutation": False,
        "audit_state_mutation": False,
        "closure_authorized_only_after_ci_success": True,
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("PASSED: EV-162 TSM revalidation gate; projected 165/192 terminal, 27 pending, next TVS-001")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
