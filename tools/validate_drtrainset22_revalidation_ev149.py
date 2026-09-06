#!/usr/bin/env python3
"""EV-149: fail-closed revalidation of DRTRAINSET22-001..002.

Both findings concern cross-references inside the byte-pinned TrainSet V2.2 PDF.
XSDs are not semantic authority for these documentation-navigation findings.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

SOURCE_ID = "TRAINSET_V2.2"
PDF_SHA256 = "c1946694a1809933a9a4a23adff1c551effdb0a2fbc6a7f7f68faec0b0c7bd6e"
PDF_SIZE = 1744296
ORIGINAL_PIN_EVIDENCE_RUN = "33239594518"
OFFICIAL_URL = "https://www.vdv.de/301-2-14-sdes-v2-2-trainsetservices.pdfx"
LOCAL_FILENAME = "TRAINSET_V2.2.pdf"
FROZEN_INVENTORY_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
DEEP_READ_BLOB = "61850045c26fb2a848c4670f1418fdb809ab475c"


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


def page_count(pdf: Path) -> int:
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True, errors="replace")
    m = re.search(r"^Pages:\s+(\d+)\s*$", info, flags=re.MULTILINE)
    if not m:
        fail("pdfinfo did not expose a page count")
    count = int(m.group(1))
    if count < 40 or count > 100:
        fail(f"implausible TRAINSET V2.2 PDF page count: {count}")
    return count


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


def locate(texts: dict[int, tuple[str, str]], label: str, *tokens: str) -> int:
    needles = [norm(t) for t in tokens]
    hits = []
    for p, pair in texts.items():
        n = norm(combined(pair))
        if all(t in n for t in needles):
            hits.append(p)
    if len(hits) != 1:
        fail(f"{label}: expected exactly one physical-page hit, got {hits}; tokens={tokens}")
    return hits[0]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--output-dir", default="artifacts/ev149")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    out = (root / args.output_dir).resolve()
    text_dir = out / "page_text"
    render_dir = out / "renders"
    text_dir.mkdir(parents=True, exist_ok=True)
    render_dir.mkdir(parents=True, exist_ok=True)

    guards = {
        "audit_registry/finding_inventory_frozen_2026-09-03.json": FROZEN_INVENTORY_BLOB,
        "docs/pdf_xsd_semantic_audit/deep_read/TRAINSET_V2.2.md": DEEP_READ_BLOB,
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
        fail("TRAINSET V2.2 PDF byte pin mismatch")

    central = load_json(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    assert central["next_revalidation_block"] == "DRTRAINSET22"
    scope = ["DRTRAINSET22-001", "DRTRAINSET22-002"]
    by_id = {x["finding_id"]: x for x in central["inventory"]["entries"]}
    for fid in scope:
        assert by_id[fid]["revalidation_state"] == "pending"
        assert by_id[fid]["terminal_state_source"] is None

    count = page_count(pdf)
    texts = {p: extract_page(pdf, p, text_dir) for p in range(1, count + 1)}

    # DRTRAINSET22-001: bilingual overview says examples are in 9.1, while the
    # same document's table of contents identifies section 10 as Examples.
    p_intro_de = locate(
        texts,
        "DRTRAINSET22-001 German overview",
        "Anhand von Beispielen wird das Zusammenspiel der verschiedenen Dienste erläutert",
        "Abschnitt 9.1",
    )
    p_intro_en = locate(
        texts,
        "DRTRAINSET22-001 English overview",
        "By means of examples the interaction of the different services is explained",
        "section 9.1",
    )
    p_toc = locate(
        texts,
        "DRTRAINSET22-001 table of contents",
        "9.1 Re-initialisation of Service Communication when a Trainset changes the Driving Direction",
        "10 Examples",
    )

    # DRTRAINSET22-002: pin each stale reference to its detailed prose heading,
    # not to operation names that also occur in the table of contents.
    p_unsub_ref = locate(
        texts,
        "DRTRAINSET22-002 UnsubscribeTripRef stale reference",
        "6.5.5.1 Request",
        "The UnsubscribeTripRef request makes use of the",
        "TrainSetUnsubscribeRequestStructure as described in section 6.5.1",
    )
    p_retrieve_info = locate(
        texts,
        "DRTRAINSET22-002 RetrieveTripInformation stale reference",
        "6.5.6 Operation RetrieveTripInformation",
        "In contrast to the operation RetrieveTripRef (cf. 6.5.1)",
    )
    p_unsub_info = locate(
        texts,
        "DRTRAINSET22-002 UnsubscribeTripInformation stale reference",
        "6.5.8.1 Request",
        "The UnsubscribeTripInformation request makes use of the",
        "TrainSetUnsubscribeRequestStructure as described in section 6.5.1",
    )

    # Same-document positive controls for the actual target numbering.
    p_correct_unsubscribe = locate(
        texts,
        "DRTRAINSET22-002 correct 6.5.2 unsubscribe-structure definition",
        "6.5.2 Specific TrainSetUnsubscribeRequestStructure",
        "This TrainSetUnsubscribeRequestStructure is defined only in the context of the TrainSetDataService",
    )
    p_correct_retrieve = locate(
        texts,
        "DRTRAINSET22-002 correct 6.5.3 RetrieveTripRef definition",
        "6.5.3 Operation RetrieveTripRef",
        "The operation RetrieveTripRef is provided by the master OBU in a trainset",
    )

    # Stronger context checks on the stale-reference pages.
    for page, heading in [
        (p_unsub_ref, "UnsubscribeTripRef"),
        (p_retrieve_info, "RetrieveTripInformation"),
        (p_unsub_info, "UnsubscribeTripInformation"),
    ]:
        n = norm(combined(texts[page]))
        if norm("6.5.1") not in n or norm(heading) not in n:
            fail(f"physical page {page}: stale-reference context did not survive extraction")

    evidence_pages = sorted({
        p_intro_de, p_intro_en, p_toc,
        p_unsub_ref, p_retrieve_info, p_unsub_info,
        p_correct_unsubscribe, p_correct_retrieve,
    })
    render_hashes = {}
    for p in evidence_pages:
        png = render_page(pdf, p, render_dir)
        render_hashes[str(p)] = {
            "sha256": sha256(png),
            "bytes": png.stat().st_size,
            "file": str(png.relative_to(out)),
        }

    states = {fid: "context_verified" for fid in scope}
    result = {
        "evidence_id": "EV-149",
        "result": "PASS",
        "scope": scope,
        "recommended_terminal_states": states,
        "source_id": SOURCE_ID,
        "authority": {
            "publication": "VDV 301-2-14 TrainSet Services V2.2, 08/2019",
            "official_url": OFFICIAL_URL,
            "pdf_sha256": PDF_SHA256,
            "pdf_size_bytes": PDF_SIZE,
            "pdf_page_count": count,
            "original_pin_evidence_run": ORIGINAL_PIN_EVIDENCE_RUN,
            "deep_read_blob": DEEP_READ_BLOB,
            "semantic_authority_lane": "byte-pinned official PDF/document navigation",
            "xsd_semantic_authority_required": False,
            "latest_xsd_wins_applicable": False,
        },
        "matched_physical_pages": {
            "DRTRAINSET22-001": {
                "german_overview": p_intro_de,
                "english_overview": p_intro_en,
                "table_of_contents": p_toc,
            },
            "DRTRAINSET22-002": {
                "UnsubscribeTripRef_stale_6_5_1": p_unsub_ref,
                "RetrieveTripInformation_stale_6_5_1": p_retrieve_info,
                "UnsubscribeTripInformation_stale_6_5_1": p_unsub_info,
                "correct_6_5_2_unsubscribe_structure": p_correct_unsubscribe,
                "correct_6_5_3_RetrieveTripRef": p_correct_retrieve,
            },
        },
        "finding_checks": {
            "DRTRAINSET22-001": "German and English overview lists point service-interaction examples to 9.1; the same publication identifies 9.1 as the re-initialisation scenario and section 10 as Examples.",
            "DRTRAINSET22-002": "Three detail-section references still point to 6.5.1 after insertion of new structures; the same V2.2 document defines TrainSetUnsubscribeRequestStructure at 6.5.2 and RetrieveTripRef at 6.5.3.",
        },
        "active_disproof": {
            "DRTRAINSET22-001": "The possibility that 9.1 was intentionally cited because it contains an example-style re-initialisation scenario was considered. As in V2.1, overview item 4 already assigns re-initialisation to sections 7 and 9, while item 5 separately introduces service-interaction examples and the document has a dedicated section 10 Examples. The 9.1 pointer remains a cross-reference error.",
            "DRTRAINSET22-002": "The possibility that 6.5.1 is a stable external or historical identifier was rejected by same-document detail headings: the referenced unsubscribe structure is defined at 6.5.2 and RetrieveTripRef at 6.5.3. The stale references are navigation errors, not schema rules.",
        },
        "executable_evidence": {
            "required_for_terminal_state": False,
            "reason": "Both findings concern PDF navigation/cross-references only and do not change XML validation behaviour.",
        },
        "fresh_visual_physical_pages": evidence_pages,
        "fresh_render_hashes": render_hashes,
        "manual_visual_review_status": "pending_human_inspection_of_EV149_artifact_before_registry_closure",
        "text_extraction_modes": ["pdftotext-layout", "pdftotext-raw"],
        "xsd_pool_role": "repository-regression-only",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
    }
    (out / "ev149_results.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED: EV-149 DRTRAINSET22 revalidation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
