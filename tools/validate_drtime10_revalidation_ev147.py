#!/usr/bin/env python3
"""EV-147: fail-closed revalidation of frozen TimeService findings DRTIME10-001..003.

TimeService is intentionally reviewed on the PDF/API/prose authority lane.
There is no TimeService XSD semantic authority in this review. The repository
XSD pool may be exercised separately as a regression/immutability guard only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

SOURCE_ID = "TIME_V1.0"
PDF_SHA256 = "464be766ef8ccf6a9e80cb8c374110d44d65afca9d938ef3b11210134a23210e"
PDF_SIZE = 369139
OFFICIAL_URL = "https://www.vdv.de/301-2-10sds-v-1-01.pdfx"
LOCAL_FILENAME = "TIME_V1.0.pdf"
FROZEN_INVENTORY_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
DEEP_READ_BLOB = "82a88b8e15f8cc7089e08fa6a58fb20866da6ed8"
TARGET_PAGES = [2, 3, 4, 5, 6]


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


def require(text: str, page: int, *tokens: str) -> None:
    n = norm(text)
    missing = [token for token in tokens if norm(token) not in n]
    if missing:
        fail(f"physical PDF page {page}: missing tokens {missing}")


def forbid(text: str, page: int, *tokens: str) -> None:
    n = norm(text)
    present = [token for token in tokens if norm(token) in n]
    if present:
        fail(f"physical PDF page {page}: unexpected tokens {present}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--output-dir", default="artifacts/ev147")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    out = (root / args.output_dir).resolve()
    text_dir = out / "page_text"
    render_dir = out / "renders"
    text_dir.mkdir(parents=True, exist_ok=True)
    render_dir.mkdir(parents=True, exist_ok=True)

    guards = {
        "audit_registry/finding_inventory_frozen_2026-09-03.json": FROZEN_INVENTORY_BLOB,
        "docs/pdf_xsd_semantic_audit/deep_read/TIME_V1.0.md": DEEP_READ_BLOB,
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
    assert source["expected_sha256"] == PDF_SHA256
    assert int(source["expected_size_bytes"]) == PDF_SIZE
    assert pin["expected_sha256"] == PDF_SHA256
    assert int(pin["expected_size_bytes"]) == PDF_SIZE

    pdf = root / "local_sources/vdv_pdfs" / LOCAL_FILENAME
    if not pdf.exists():
        fail(f"missing fetched PDF {pdf}")
    if pdf.stat().st_size != PDF_SIZE or sha256(pdf) != PDF_SHA256:
        fail("TIME V1.0 PDF byte pin mismatch")

    central = load_json(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    assert central["next_revalidation_block"] == "DRTIME10"
    scope = ["DRTIME10-001", "DRTIME10-002", "DRTIME10-003"]
    by_id = {x["finding_id"]: x for x in central["inventory"]["entries"]}
    for fid in scope:
        assert by_id[fid]["revalidation_state"] == "pending"
        assert by_id[fid]["terminal_state_source"] is None

    texts = {p: extract_page(pdf, p, text_dir) for p in TARGET_PAGES}

    # DRTIME10-001: adjacent German/English normative-reference context.
    p2 = combined(texts[2])
    p3 = combined(texts[3])
    require(p2, 2, "VDV-Schrift 301-1", "VDV-Schrift 301-2-0")
    require(p3, 3, "VDV 301-2-1")

    # DRTIME10-002: German explicitly excludes cyclic time broadcasting;
    # the corresponding English GetTime prose retains only passive response.
    p4 = combined(texts[4])
    p5 = combined(texts[5])
    require(
        p4,
        4,
        "Ein zyklisches Versenden der Uhrzeit ist nicht vorgesehen",
        "Eine Nachricht wird ausschließlich als passive Antwort auf die GetTime-Request-Nachricht versendet",
    )
    require(p5, 5, "A message is sent exclusively as passive response to the GetTime request message")
    # The English counterpart must not independently state a cyclic/non-cyclic broadcast rule.
    forbid(p5, 5, "cyclic", "cyclical", "cyclically", "periodic time")

    # DRTIME10-003: preserve the exact printed version-history artifact without
    # guessing what its intended replacement should have been.
    p6 = combined(texts[6])
    require(p6, 6, "19.04.2016", "cd. 1", "Completion", "Druckschrift")

    # Re-derive the historically documented TimeService invariant from the
    # current byte-pinned source; do not pretend a current RV-003 checker exists.
    cyclic_time_broadcast_expected = False
    assert "nicht vorgesehen" in p4
    assert cyclic_time_broadcast_expected is False

    render_hashes = {}
    for p in TARGET_PAGES:
        png = render_page(pdf, p, render_dir)
        render_hashes[str(p)] = {
            "sha256": sha256(png),
            "bytes": png.stat().st_size,
            "file": str(png.relative_to(out)),
        }

    states = {fid: "context_verified" for fid in scope}
    result = {
        "evidence_id": "EV-147",
        "result": "PASS",
        "scope": scope,
        "recommended_terminal_states": states,
        "semantic_authority_lane": "PDF/API/prose",
        "time_service_xsd_authority": False,
        "xsd_pool_role": "repository-regression-only",
        "authority": {
            "source_id": SOURCE_ID,
            "publication": "VDV 301-2-10 TimeService V1.0",
            "official_url": OFFICIAL_URL,
            "pdf_sha256": PDF_SHA256,
            "pdf_size_bytes": PDF_SIZE,
            "deep_read_blob": DEEP_READ_BLOB,
            "latest_xsd_wins_applicable": False,
        },
        "historical_review_reference": {
            "RV-003": "Referenced by the frozen/current deep-read narrative only; no current RV-003 checker or cyclic_time_broadcast_expected implementation is present on the audited branch HEAD. EV-147 re-derives the relevant invariant directly from the pinned source."
        },
        "rederived_invariants": {
            "cyclic_time_broadcast_expected": cyclic_time_broadcast_expected,
        },
        "fresh_visual_pages": TARGET_PAGES,
        "visual_gap_closure_targets": [3, 6],
        "fresh_render_hashes": render_hashes,
        "text_extraction_modes": ["pdftotext-layout", "pdftotext-raw"],
        "finding_checks": {
            "DRTIME10-001": "German normative-reference context contains VDV-Schrift 301-1 and VDV-Schrift 301-2-0; adjacent English context prints VDV 301-2-1.",
            "DRTIME10-002": "German GetTime prose explicitly says cyclic time sending is not intended and then limits messages to passive GetTime responses; the English counterpart retains the passive-response sentence but no cyclic/non-cyclic rule.",
            "DRTIME10-003": "English version-history row visibly/extractably contains '19.04.2016 cd. 1 Completion Druckschrift'; EV-147 preserves this as an editorial artifact without inventing the intended replacement text.",
        },
        "active_disproof": {
            "DRTIME10-001": "Equivalent-reference hypothesis rejected by the directly adjacent bilingual normative-reference sections in the same pinned publication.",
            "DRTIME10-002": "Implicit-English-equivalence hypothesis rejected because the English counterpart preserves the following passive-response sentence while omitting the preceding explicit non-cyclic rule.",
            "DRTIME10-003": "Extraction-only hypothesis rejected by retaining fresh page render plus independent layout/raw extraction; intended corrected wording remains deliberately unspecified.",
        },
        "non_promoted_findings": [
            "FR-TIM10-SEM-001",
            "FR-TIM10-SEM-004",
        ],
        "executable_xml_evidence_reason_not_applicable": "The three DRTIME10 findings are documentation/prose/version-history findings. TimeService has no XSD semantic authority in this audit lane.",
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
    }
    (out / "ev147_results.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED: EV-147 DRTIME10 TimeService V1.0 revalidation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
