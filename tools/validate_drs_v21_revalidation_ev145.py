#!/usr/bin/env python3
"""EV-145: fail-closed legacy revalidation for DoorStateService findings DRS-001..004.

The validator preserves the exact VDV-301-2.1 mixed-version authority route,
rechecks byte-pinned PDF context, re-runs EV-111 for material executable
behaviour, and proves DRS-004 remains annotation-only. No normative XSD is
modified.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from lxml import etree

SOURCE_ID = "DOOR_V2.1"
PDF_SHA256 = "7413c99f2910f125947213561658ae9c808952d5b57700d155b939c899de26e8"
PDF_SIZE = 851513
FROZEN_INVENTORY_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
DEEP_READ_BLOB = "ef81d838be8d42ae9250cddb7e506f978ba75655"
REGISTER_BLOB = "88b0f0c6d92d48a5e992b75f3058501d3c0c0d2a"
DOOR_XSD_BLOB = "abff0f3960e2ec7a9caaa9ddeb6efff8f4183805"
COMMON_XSD_BLOB = "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c"
ENUM_XSD_BLOB = "a9bea5bc73003ed91ded8519db06c32c4067831d"
EV111_SCRIPT_BLOB = "75c7528c2f18dfe35d74a6b27e104ec006661ce1"
EV111_RUN = "33242337308"
EV111_JOB = "99073684198"
TARGET_PAGES = [9, 10, 11, 12]
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
    return re.sub(r"\s+", " ", text).strip().lower()


def page_text(pdf: Path, page: int, out_dir: Path) -> str:
    target = out_dir / f"page-{page:02d}.txt"
    subprocess.run(["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(pdf), str(target)], check=True)
    return target.read_text(encoding="utf-8", errors="replace")


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


def require(text: str, page: int, *tokens: str) -> None:
    n = norm(text)
    missing = [t for t in tokens if norm(t) not in n]
    if missing:
        fail(f"page {page}: missing tokens {missing}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--output-dir", default="artifacts/ev145")
    args = ap.parse_args()
    root = Path(args.repo_root).resolve()
    out = (root / args.output_dir).resolve()
    render_dir = out / "renders"
    text_dir = out / "page_text"
    render_dir.mkdir(parents=True, exist_ok=True)
    text_dir.mkdir(parents=True, exist_ok=True)

    guards = {
        "audit_registry/finding_inventory_frozen_2026-09-03.json": FROZEN_INVENTORY_BLOB,
        "docs/pdf_xsd_semantic_audit/deep_read/DOOR_V2.1.md": DEEP_READ_BLOB,
        "docs/pdf_xsd_semantic_audit/DOOR_STATE_SERVICE_FINDINGS_REGISTER_ADDENDUM.md": REGISTER_BLOB,
        "IBIS-IP_DoorStateService_V2.1.xsd": DOOR_XSD_BLOB,
        "IBIS-IP_common_V1.0.xsd": COMMON_XSD_BLOB,
        "IBIS-IP_Enumerations_V1.0.xsd": ENUM_XSD_BLOB,
        "tools/validate_door_v21_ev111.py": EV111_SCRIPT_BLOB,
    }
    for rel, expected in guards.items():
        actual = git_blob(root, rel)
        if actual != expected:
            fail(f"canonical authority changed: {rel}: {actual} != {expected}")

    sources = load_json(root / "audit_registry/pdf_source_registry_v0.1.json")
    pins = load_json(root / "audit_registry/pdf_source_pins_v0.1.json")
    source = next(x for x in sources["sources"] if x["source_id"] == SOURCE_ID)
    pin = next(x for x in pins["sources"] if x["source_id"] == SOURCE_ID)
    assert source["official_url"] == "https://www.vdv.de/301-2-15-sd-v2-1-doorstateservice.pdfx"
    assert source["local_filename"] == "DOOR_V2.1.pdf"
    assert pin["expected_sha256"] == PDF_SHA256
    assert int(pin["expected_size_bytes"]) == PDF_SIZE

    pdf = root / "local_sources/vdv_pdfs" / source["local_filename"]
    if not pdf.exists():
        fail(f"missing fetched PDF {pdf}")
    if pdf.stat().st_size != PDF_SIZE or sha256(pdf) != PDF_SHA256:
        fail("DOOR V2.1 PDF byte pin mismatch")

    # Central registry must still present the four legacy findings as pending.
    central = load_json(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    assert central["next_revalidation_block"] == "DRS"
    by_id = {x["finding_id"]: x for x in central["inventory"]["entries"]}
    scope = ["DRS-001", "DRS-002", "DRS-003", "DRS-004"]
    for fid in scope:
        assert by_id[fid]["revalidation_state"] == "pending"
        assert by_id[fid]["terminal_state_source"] is None

    # Fresh source-bound context and visual evidence.
    texts = {p: page_text(pdf, p, text_dir) for p in TARGET_PAGES}
    require(texts[9], 9, "GetDoorOperationStates", "SubscribeDoorOpenStates", "UnsubscribeDoorOpenStates")
    require(texts[12], 12, "OperationErrorMessage", "RetrieveSpecificDoorOpenState", "RetrieveSpecificDoorOperationState")
    render_hashes = {}
    for p in TARGET_PAGES:
        png = render_page(pdf, p, render_dir)
        render_hashes[str(p)] = {
            "sha256": sha256(png),
            "bytes": png.stat().st_size,
            "file": str(png.relative_to(out)),
        }

    # Exact XSD structure checks for DRS-001..004.
    xsd_path = root / "IBIS-IP_DoorStateService_V2.1.xsd"
    tree = etree.parse(str(xsd_path))
    ns = {"xs": XS}

    group_names = tree.xpath("//xs:group[@name='DoorStateServiceGroup']//xs:element/@name", namespaces=ns)
    for name in (
        "DoorStateService.SubscribeDoorOpenStatesRequest",
        "DoorStateService.UnsubscribeDoorOpenStatesRequest",
        "DoorStateService.SubscribeDoorOperationStatesRequest",
        "DoorStateService.UnsubscribeDoorOperationStatesRequest",
    ):
        assert name in group_names
    assert "DoorStateService.SubscribeDoorOperationStateRequest" not in group_names

    for typename in (
        "DoorStateService.RetrieveSpecificDoorOpenStateResponseStructure",
        "DoorStateService.RetrieveSpecificDoorOperationStateResponseStructure",
    ):
        elems = tree.xpath(f"//xs:complexType[@name='{typename}']/xs:choice/xs:element/@name", namespaces=ns)
        assert "ErrorMessage" in elems and "OperationErrorMessage" not in elems

    for name in (
        "DoorStateService.GetDoorOpenStatesRequest",
        "DoorStateService.GetDoorOperationStatesRequest",
    ):
        elems = tree.xpath(f"//xs:group[@name='DoorStateServiceGroup']//xs:element[@name='{name}']", namespaces=ns)
        assert len(elems) == 1
        elem = elems[0]
        assert "type" not in elem.attrib
        assert elem.find(f"{{{XS}}}complexType") is None and elem.find(f"{{{XS}}}simpleType") is None

    docs = "\n".join(tree.xpath("//xs:documentation/text()", namespaces=ns))
    assert "GetDoorOpeationStates" in docs
    assert "RetrieveSpecificDoorOperationnState" in docs
    assert "operationn state" in docs
    executable_identifiers = "\n".join(tree.xpath("//@name | //@type", namespaces=ns))
    assert "GetDoorOpeationStates" not in executable_identifiers
    assert "RetrieveSpecificDoorOperationnState" not in executable_identifiers
    assert "DoorStateService.GetDoorOperationStatesResponse" in executable_identifiers
    assert "DoorStateService.RetrieveSpecificDoorOperationStateResponse" in executable_identifiers

    # Re-run the already-canonical executable boundary for DRS-002 and DRS-003.
    ev111 = subprocess.run(
        ["python", "tools/validate_door_v21_ev111.py"],
        cwd=root, text=True, capture_output=True
    )
    (out / "ev111_rerun.log").write_text(ev111.stdout + ev111.stderr, encoding="utf-8")
    if ev111.returncode != 0:
        fail(f"EV-111 rerun failed\n{ev111.stdout}\n{ev111.stderr}")
    assert "PASSED: EV-111 DoorState V2.1 DRS-002/DRS-003 executable behaviour confirmed" in ev111.stdout
    assert "<ErrorMessage> branch -> valid" in ev111.stdout
    assert "<OperationErrorMessage> branch -> invalid" in ev111.stdout
    assert "arbitrary unexpected child content under xs:anyType -> valid" in ev111.stdout

    result = {
        "evidence_id": "EV-145",
        "result": "PASS",
        "scope": scope,
        "recommended_terminal_states": {
            "DRS-001": "context_verified",
            "DRS-002": "executable_confirmed",
            "DRS-003": "executable_confirmed",
            "DRS-004": "context_verified",
        },
        "authority": {
            "source_id": SOURCE_ID,
            "pdf_sha256": PDF_SHA256,
            "pdf_size_bytes": PDF_SIZE,
            "official_release_tag": "VDV-301-2.1",
            "door_xsd_blob": DOOR_XSD_BLOB,
            "common_v1_0_blob": COMMON_XSD_BLOB,
            "enumerations_v1_0_blob": ENUM_XSD_BLOB,
            "mixed_version_dependency_is_authoritative": True,
            "latest_xsd_wins": False,
        },
        "prior_executable_evidence": {
            "evidence_id": "EV-111",
            "run_id": EV111_RUN,
            "job_id": EV111_JOB,
            "rerun_result": "PASS",
        },
        "fresh_visual_pages": TARGET_PAGES,
        "fresh_render_hashes": render_hashes,
        "finding_checks": {
            "DRS-001": "page 9 operation overview repeats OpenStates subscription names after GetDoorOperationStates while exact XSD has distinct OperationStates subscription operations",
            "DRS-002": "page 12 names OperationErrorMessage; exact RetrieveSpecific response choices accept ErrorMessage and reject OperationErrorMessage, re-confirmed by EV-111",
            "DRS-003": "exact local Get request declarations remain untyped; EV-111 re-confirms xs:anyType default semantics including arbitrary nested content",
            "DRS-004": "known misspellings occur only inside xs:documentation; executable @name/@type identifiers retain correct spellings",
        },
        "active_disproof": {
            "DRS-001": "shared/generic subscription-name hypothesis rejected by distinct exact XSD operations",
            "DRS-002": "generic prose-label hypothesis rejected by table element-name role and exact XSD Get-vs-RetrieveSpecific distinction",
            "DRS-003": "no-request-structure-means-empty hypothesis rejected by exact untyped declaration and XML Schema anyType semantics",
            "DRS-004": "executable-identifier-impact hypothesis rejected by annotation-only location and correctly spelled executable identifiers",
        },
        "choice_notation_guard": "page-12 a/b -1:1 choice notation is not treated as negative cardinality; no new cardinality finding",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
    }
    (out / "ev145_results.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED: EV-145 DRS V2.1 legacy finding revalidation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
