#!/usr/bin/env python3
"""EV-144: fail-closed revalidation for frozen VDV 301-3 Network findings.

Scope: DRNET20-001..003 only.  VDV 301-3 is a non-XSD physical/network/
protocol-profile document, so executable XML evidence is deliberately not
manufactured for these documentation-only findings.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

SOURCE_ID = "VDV301-3_02-2020"
PDF_SHA256 = "edfedf36eeb18075b45bf5224f0da6500cdd489438091f18bada42f9668c2a99"
PDF_SIZE = 558005
PDF_PAGES = 37
FROZEN_INVENTORY_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
DEEP_READ_BLOB = "ddb4f49da1e3afa55920e50f9e74e554748f1378"
FINDINGS_DELTA_BLOB = "f1d879dafba78533158448c55ff475d234308d36"
REGISTRY_DELTA_BLOB = "c46bf8ee10c1c83d4c3cea0a5f305b4fbc23638b"
ORIGINAL_VISUAL_RUN = "33270251357"
ORIGINAL_VISUAL_JOB = "99147343832"
ORIGINAL_VISUAL_ARTIFACT = "9719880284"
ORIGINAL_VISUAL_ARTIFACT_DIGEST = "sha256:2cc403407a354af07c2dfc1cc78666e0f16fc753af6eebfaf090b0300214d930"
FRESH_READ_FREEZE = "f359aa0160d2f8a0834db9274a4ecf0a18321dea"
TARGET_PAGES = [7, 8, 10, 17, 18, 19, 29]


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


def normalize(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def page_text(pdf: Path, page: int, out_dir: Path) -> str:
    target = out_dir / f"page-{page:02d}.txt"
    subprocess.run(
        ["pdftotext", "-layout", "-f", str(page), "-l", str(page), str(pdf), str(target)],
        check=True,
    )
    return target.read_text(encoding="utf-8", errors="replace")


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
        fail(f"render missing for page {page}")
    return png


def require_tokens(text: str, page: int, *tokens: str) -> None:
    n = normalize(text)
    missing = [t for t in tokens if normalize(t) not in n]
    if missing:
        fail(f"page {page}: missing expected tokens {missing}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--output-dir", default="artifacts/ev144")
    ap.add_argument("--ieee-publication-html", required=True)
    ap.add_argument("--ieee-interpretations-html", required=True)
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    out = (root / args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    render_dir = out / "renders"
    text_dir = out / "page_text"
    render_dir.mkdir(exist_ok=True)
    text_dir.mkdir(exist_ok=True)

    # Immutable/canonical audit source guards.
    guards = {
        "audit_registry/finding_inventory_frozen_2026-09-03.json": FROZEN_INVENTORY_BLOB,
        "docs/pdf_xsd_semantic_audit/deep_read/VDV301-3_02-2020.md": DEEP_READ_BLOB,
        "audit_registry/deep_read_findings_delta_vdv301_3_02_2020_2026-08-29.json": FINDINGS_DELTA_BLOB,
        "audit_registry/deep_read_registry_delta_vdv301_3_02_2020_2026-08-29.json": REGISTRY_DELTA_BLOB,
    }
    for rel, expected in guards.items():
        actual = git_blob(root, rel)
        if actual != expected:
            fail(f"canonical source changed: {rel}: {actual} != {expected}")

    source_registry = load_json(root / "audit_registry/pdf_source_registry_v0.1.json")
    pin_registry = load_json(root / "audit_registry/pdf_source_pins_v0.1.json")
    source = next(x for x in source_registry["sources"] if x["source_id"] == SOURCE_ID)
    pin = next(x for x in pin_registry["sources"] if x["source_id"] == SOURCE_ID)
    assert source["official_url"] == "https://www.vdv.de/301-3-sdes-network-infrastructure.pdfx"
    assert source["local_filename"] == "VDV301-3_02-2020.pdf"
    assert pin["expected_sha256"] == PDF_SHA256
    assert int(pin["expected_size_bytes"]) == PDF_SIZE
    assert pin["evidence_run_id"] == ORIGINAL_VISUAL_RUN

    pdf = root / "local_sources/vdv_pdfs" / source["local_filename"]
    if not pdf.exists():
        fail(f"missing fetched PDF: {pdf}")
    if pdf.stat().st_size != PDF_SIZE:
        fail(f"PDF size mismatch: {pdf.stat().st_size} != {PDF_SIZE}")
    if sha256(pdf) != PDF_SHA256:
        fail("PDF SHA-256 mismatch")

    pdfinfo = subprocess.check_output(["pdfinfo", str(pdf)], text=True, errors="replace")
    m = re.search(r"^Pages:\s+(\d+)\s*$", pdfinfo, re.MULTILINE)
    if not m or int(m.group(1)) != PDF_PAGES:
        fail("unexpected PDF page count")

    findings_delta = load_json(root / "audit_registry/deep_read_findings_delta_vdv301_3_02_2020_2026-08-29.json")
    rd = load_json(root / "audit_registry/deep_read_registry_delta_vdv301_3_02_2020_2026-08-29.json")
    doc = rd["document_updates"][SOURCE_ID]
    assert findings_delta["fresh_read_freeze"] == FRESH_READ_FREEZE
    assert doc["fresh_read_freeze_commit"] == FRESH_READ_FREEZE
    assert doc["authority_status"]["xsd_required"] is False
    assert doc["authority_status"]["xsd_lane"] == "network_protocol"
    assert doc["authority_status"]["validation_lane"] == "physical_network_protocol_profile"
    assert doc["authority_status"]["latest_external_protocol_version_wins"] is False
    vis = doc["render_read_evidence"]
    assert str(vis["run"]) == ORIGINAL_VISUAL_RUN
    assert str(vis["job"]) == ORIGINAL_VISUAL_JOB
    assert str(vis["artifact"]) == ORIGINAL_VISUAL_ARTIFACT
    assert vis["artifact_zip_digest"] == ORIGINAL_VISUAL_ARTIFACT_DIGEST
    assert vis["pdf_page_count"] == PDF_PAGES and vis["all_pages_rendered"] is True

    expected_findings = {
        "DRNET20-001": "pdf_network_media_terminology_error_candidate",
        "DRNET20-002": "pdf_translation_semantic_safety_security_error_candidate",
        "DRNET20-003": "pdf_editorial_spelling_errors_grouped",
    }
    unique = findings_delta["new_unique_findings"]
    assert set(unique) == set(expected_findings)
    for fid, classification in expected_findings.items():
        assert unique[fid]["state"] == "context_verified"
        assert unique[fid]["classification"] == classification
        assert unique[fid]["executable_effect"] is False

    # Frozen inventory contains these IDs and central revalidation registry still has them pending.
    frozen = load_json(root / "audit_registry/finding_inventory_frozen_2026-09-03.json")
    assert frozen["state"] == "frozen" and frozen["entry_count"] == 192
    for fid in expected_findings:
        assert fid in frozen["finding_ids"]
    central = load_json(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    state_by_id = {x["finding_id"]: x for x in central["inventory"]["entries"]}
    for fid in expected_findings:
        assert state_by_id[fid]["revalidation_state"] == "pending"
        assert state_by_id[fid]["terminal_state_source"] is None

    # Page-specific text anchors bind the claims to the exact bytes; fresh renders provide visual artifacts.
    texts = {p: page_text(pdf, p, text_dir) for p in TARGET_PAGES}
    require_tokens(texts[10], 10, "1000Base-X", "1 GBase-T")
    require_tokens(texts[17], 17, "1000Base-X", "1 GBase-T")
    require_tokens(texts[7], 7, "sicherheitsrelevant")
    require_tokens(texts[8], 8, "safety", "security")
    require_tokens(texts[18], 18, "Connection methodes")
    require_tokens(texts[19], 19, "Not describede")
    # Keep NET-003 distinct: page 11 IEE typo is historical NET-003, not DRNET20-003.
    require_tokens(texts[29], 29, "IEEE 802.3af/at/bt")

    render_hashes = {}
    for p in TARGET_PAGES:
        png = render_page(pdf, p, render_dir)
        render_hashes[str(p)] = {"file": str(png.relative_to(out)), "sha256": sha256(png), "bytes": png.stat().st_size}

    # External material is falsification/terminology context only; it never replaces VDV authority.
    ieee_pub = Path(args.ieee_publication_html).resolve()
    ieee_interp = Path(args.ieee_interpretations_html).resolve()
    pub_text = normalize(ieee_pub.read_text(encoding="utf-8", errors="replace"))
    interp_text = normalize(ieee_interp.read_text(encoding="utf-8", errors="replace"))
    if "clause 40" not in pub_text or "1000base-t" not in pub_text:
        fail("IEEE publication page no longer exposes Clause 40 / 1000BASE-T marker")
    if "1000base-x" not in interp_text or "1000base-t" not in interp_text:
        fail("IEEE interpretation page lacks distinct 1000BASE-X and 1000BASE-T markers")

    # Active disproof boundaries from the canonical fresh read remain explicit.
    rejected = " ".join(doc["rejected_suspicions"])
    assert "CAT6 55m" in rejected
    assert "Figure/Table 2 and 3" in rejected
    assert "absence of XSD is intentional" in rejected
    runtime = doc["adjacent_runtime_evidence"]
    assert runtime["evidence_id"] == "RV-002" and runtime["result"] == "PASS"
    assert "no live discovery" in runtime["boundary"]

    result = {
        "evidence_id": "EV-144",
        "result": "PASS",
        "scope": ["DRNET20-001", "DRNET20-002", "DRNET20-003"],
        "recommended_terminal_states": {fid: "context_verified" for fid in expected_findings},
        "authority": {
            "source_id": SOURCE_ID,
            "pdf_sha256": PDF_SHA256,
            "pdf_size_bytes": PDF_SIZE,
            "pdf_page_count": PDF_PAGES,
            "validation_lane": "physical_network_protocol_profile",
            "xsd_required": False,
            "latest_external_protocol_version_wins": False,
            "fresh_read_freeze": FRESH_READ_FREEZE,
            "prior_visual_run": ORIGINAL_VISUAL_RUN,
            "prior_visual_job": ORIGINAL_VISUAL_JOB,
            "prior_visual_artifact": ORIGINAL_VISUAL_ARTIFACT,
            "prior_visual_artifact_digest": ORIGINAL_VISUAL_ARTIFACT_DIGEST,
        },
        "fresh_visual_pages": TARGET_PAGES,
        "fresh_render_hashes": render_hashes,
        "external_falsification_context": {
            "ieee_publication_url": "https://www.ieee802.org/3/publication/index.html",
            "ieee_publication_sha256": sha256(ieee_pub),
            "ieee_interpretations_url": "https://www.ieee802.org/3/interp/index.html",
            "ieee_interpretations_sha256": sha256(ieee_interp),
            "authority_role": "interpretation/falsification only; not substituted VDV authority",
        },
        "finding_checks": {
            "DRNET20-001": "exact PDF pages 10/17 contain 1000Base-X in copper section and own 1 GBase-T table; IEEE context confirms 1000BASE-T Clause 40 and distinguishes X/T terminology",
            "DRNET20-002": "exact PDF pages 7/8 preserve German functional-safety context while English page 8 contains safety/security conflict",
            "DRNET20-003": "exact PDF pages 18/19/29 retain grouped spelling/editorial residue; historical page-11 IEE item remains NET-003 and is excluded",
        },
        "executable_xml_evidence": "not_applicable_documentation_only_non_xsd_network_profile",
        "rv002_boundary": runtime["boundary"],
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
    }
    result_path = out / "ev144_results.json"
    result_path.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED: EV-144 Network V2.0 frozen finding revalidation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
