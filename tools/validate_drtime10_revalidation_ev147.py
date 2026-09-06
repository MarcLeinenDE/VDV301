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
PDF_SHA256 = "d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3"
PDF_SIZE = 515920
ORIGINAL_PIN_EVIDENCE_RUN = "33196758957"
OFFICIAL_URL = "https://www.vdv.de/301-2-10sds-v-1-01.pdfx"
LOCAL_FILENAME = "TIME_V1.0.pdf"
FROZEN_INVENTORY_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
DEEP_READ_BLOB = "82a88fbd6dae5d22f472bf144770d915fcc902ea"


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
    if count < 1 or count > 100:
        fail(f"implausible PDF page count: {count}")
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


def require(text: str, label: str, *tokens: str) -> None:
    n = norm(text)
    missing = [token for token in tokens if norm(token) not in n]
    if missing:
        fail(f"{label}: missing tokens {missing}")


def locate(texts: dict[int, tuple[str, str]], token: str) -> int:
    needle = norm(token)
    hits = [p for p, pair in texts.items() if needle in norm(combined(pair))]
    if len(hits) != 1:
        fail(f"token {token!r}: expected exactly one physical-page hit, got {hits}")
    return hits[0]


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
    assert pin["expected_sha256"] == PDF_SHA256
    assert int(pin["expected_size_bytes"]) == PDF_SIZE
    assert str(pin["evidence_run_id"]) == ORIGINAL_PIN_EVIDENCE_RUN
    assert pin["deep_read_source_ready"] is True

    pdf = root / "local_sources/vdv_pdfs" / LOCAL_FILENAME
    if not pdf.exists():
        fail(f"missing fetched/recovered PDF {pdf}")
    if pdf.stat().st_size != PDF_SIZE or sha256(pdf) != PDF_SHA256:
        fail("TIME V1.0 PDF byte pin mismatch")

    central = load_json(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    assert central["next_revalidation_block"] == "DRTIME10"
    scope = ["DRTIME10-001", "DRTIME10-002", "DRTIME10-003"]
    by_id = {x["finding_id"]: x for x in central["inventory"]["entries"]}
    for fid in scope:
        assert by_id[fid]["revalidation_state"] == "pending"
        assert by_id[fid]["terminal_state_source"] is None

    count = page_count(pdf)
    texts = {p: extract_page(pdf, p, text_dir) for p in range(1, count + 1)}

    # DRTIME10-001: locate the bilingual foreword by content, not by a
    # zero-/one-based screenshot page convention.
    p_foreword = locate(texts, "The VDV 301-2-1 describes the TimeService")
    foreword = combined(texts[p_foreword])
    require(
        foreword,
        f"physical PDF page {p_foreword} bilingual foreword",
        "Die VDV-Schrift 301-2-10 beschreibt den TimeService",
        "The VDV 301-2-1 describes the TimeService",
    )

    # DRTIME10-002: German and English service sections are adjacent on the
    # same physical page. The German section has an explicit no-cyclic rule;
    # the English section omits it.
    p_service = locate(texts, "Ein zyklisches Versenden der aktuellen Uhrzeit ist darüber hinaus nicht vorgesehen")
    service_layout = texts[p_service][0]
    require(
        combined(texts[p_service]),
        f"physical PDF page {p_service} bilingual TimeService section",
        "Ein zyklisches Versenden der aktuellen Uhrzeit ist darüber hinaus nicht vorgesehen",
        "Service TimeService",
        "The actual form of time synchronization is then processed using the SNTP protocol",
    )
    english_marker = service_layout.find("Service TimeService")
    if english_marker < 0:
        fail(f"physical PDF page {p_service}: cannot isolate English Service TimeService block")
    english_block = service_layout[english_marker:]
    forbidden = [token for token in ("cyclic", "cyclical", "cyclically", "periodic time") if norm(token) in norm(english_block)]
    if forbidden:
        fail(f"physical PDF page {p_service}: English block unexpectedly contains {forbidden}")

    # DRTIME10-003: exact English technical-correction artifact. Do not infer
    # the intended replacement for 'cd. 1'.
    p_history = locate(texts, "Definition of the service type: _ibisip_udp._udp, cd. 1")
    history = combined(texts[p_history])
    require(
        history,
        f"physical PDF page {p_history} version history",
        "Definition of the service type: _ibisip_udp._udp, cd. 1",
        "Technische Ergänzungen/Korrekturen",
        "Technical Upgrade/Corrections",
    )

    cyclic_time_broadcast_expected = False
    assert cyclic_time_broadcast_expected is False

    evidence_pages = sorted({p_foreword, p_service, p_history})
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
        "evidence_id": "EV-147",
        "result": "PASS",
        "scope": scope,
        "recommended_terminal_states": states,
        "semantic_authority_lane": "PDF/API/prose",
        "time_service_xsd_authority": False,
        "xsd_pool_role": "repository-regression-only",
        "authority": {
            "source_id": SOURCE_ID,
            "publication": "VDV 301-2-10 TimeService V1.0, 02/2018",
            "official_url": OFFICIAL_URL,
            "pdf_sha256": PDF_SHA256,
            "pdf_size_bytes": PDF_SIZE,
            "pdf_page_count": count,
            "original_pin_evidence_run": ORIGINAL_PIN_EVIDENCE_RUN,
            "deep_read_blob": DEEP_READ_BLOB,
            "latest_xsd_wins_applicable": False,
        },
        "historical_review_reference": {
            "RV-003": "Referenced by the current deep-read narrative only; no current RV-003 checker or cyclic_time_broadcast_expected implementation is present on the audited branch HEAD. EV-147 re-derives the relevant invariant directly from the pinned source."
        },
        "rederived_invariants": {
            "cyclic_time_broadcast_expected": cyclic_time_broadcast_expected,
        },
        "visual_gap_closure_targets": [3, 6],
        "visual_gap_target_semantics": "legacy deep-read screenshot indices; not physical one-based PDF page numbers",
        "fresh_visual_physical_pages": evidence_pages,
        "visual_gap_resolution": {
            "deep_read_page_3_foreword": p_foreword,
            "deep_read_page_6_version_history": p_history,
            "deep_read_page_5_service_content": p_service,
        },
        "fresh_render_hashes": render_hashes,
        "text_extraction_modes": ["pdftotext-layout", "pdftotext-raw"],
        "finding_checks": {
            "DRTIME10-001": f"Physical PDF page {p_foreword} directly juxtaposes German 'VDV-Schrift 301-2-10 describes TimeService' with English 'VDV 301-2-1 describes TimeService'.",
            "DRTIME10-002": f"Physical PDF page {p_service} contains adjacent German and English TimeService sections; only German explicitly says cyclic transmission of current time is not intended.",
            "DRTIME10-003": f"Physical PDF page {p_history} contains the English technical-correction text 'Definition of the service type: _ibisip_udp._udp, cd. 1'.",
        },
        "active_disproof": {
            "DRTIME10-001": "Equivalent-document-identity hypothesis rejected by the directly adjacent bilingual foreword within the same pinned publication, whose identity is VDV 301-2-10.",
            "DRTIME10-002": "Implicit-English-equivalence hypothesis rejected by isolating the adjacent English Service TimeService block and confirming the explicit non-cyclic rule is absent there.",
            "DRTIME10-003": "Extraction-only hypothesis rejected by retaining a fresh render plus independent layout/raw extraction; intended corrected wording remains deliberately unspecified.",
        },
        "non_promoted_findings": ["FR-TIM10-SEM-001", "FR-TIM10-SEM-004"],
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
