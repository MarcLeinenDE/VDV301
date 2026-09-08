#!/usr/bin/env python3
"""EV-154: fail-closed terminal revalidation of NET-001..NET-003.

Authority lane:
- official byte-pinned VDV-Schrift 301-3 Network Infrastructure 02/2020 PDF,
- independent frozen-head Deep Read / historical reconciliation,
- frozen finding inventory and current Evidence Gate.

VDV 301-3 has deliberately no XSD lane. The 50-root XSD suite is therefore a
regression/no-mutation guard, not executable proof for these documentation findings.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

FROZEN_INVENTORY_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
CENTRAL_PRESTATE_BLOB = "c63feaaa2e88f36185e1b3b90a4aa41c5d560ac4"
CURRENT_STATE_PRESTATE_BLOB = "3706ebd462a4d02b6eefe823c433c0897663cd3a"
EVIDENCE_GATE_BLOB = "969cce8b14b50ded2ca5eb745674b894428ecf1a"
PDF_SOURCE_REGISTRY_BLOB = "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8"
PIN_WORKFLOW_BLOB = "30cdb5c0d29bc43bd9edcea4ee82b4fcdd9b6537"
FROZEN_SOURCE_HEAD = "7fad145f528205ef5c40e58a3a23374379b08189"
DEEP_READ_BLOB = "ddb4f49da1e3afa55920e50f9e74e554748f1378"
HANDOFF_BLOB = "69bb404f71eb4173c8757b6c7751f2b3922588b9"

PDF_SOURCE_ID = "VDV301-3_02-2020"
PDF_URL = "https://www.vdv.de/301-3-sdes-network-infrastructure.pdfx"
PDF_FILENAME = "VDV301-3_02-2020.pdf"
PDF_SHA256 = "edfedf36eeb18075b45bf5224f0da6500cdd489438091f18bada42f9668c2a99"
PDF_SIZE = 558005
PIN_RUN_ID = "34232022618"
PIN_JOB_ID = "102080274471"
PIN_ARTIFACT_ID = "10058187809"
PIN_ARTIFACT_DIGEST = "sha256:5f978eccdddf1d20cd6b62b4798bceae12b11438a4cbf59d9d5a98611a17421a"
PDF_PAGES = [6, 7, 8, 11, 14, 20, 29]


def git_blob(root: Path, rel: str, ref: str = "HEAD") -> str:
    return subprocess.check_output(
        ["git", "rev-parse", f"{ref}:{rel}"], cwd=root, text=True
    ).strip()


def git_text(root: Path, rel: str, ref: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{ref}:{rel}"], cwd=root, text=True
    )


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def text_page(pdf: Path, page: int, out: Path, mode: str) -> str:
    target = out / f"page-{page}-{mode}.txt"
    cmd = ["pdftotext", "-f", str(page), "-l", str(page)]
    if mode == "raw":
        cmd.append("-raw")
    elif mode == "layout":
        cmd.append("-layout")
    else:
        raise AssertionError(mode)
    cmd.extend([str(pdf), str(target)])
    subprocess.run(cmd, check=True)
    return target.read_text(encoding="utf-8", errors="replace")


def render_page(pdf: Path, page: int, out: Path) -> Path:
    prefix = out / f"page-{page}"
    subprocess.run(
        ["pdftoppm", "-f", str(page), "-l", str(page), "-singlefile", "-png", "-r", "180", str(pdf), str(prefix)],
        check=True,
    )
    result = prefix.with_suffix(".png")
    assert result.exists() and result.stat().st_size > 0
    return result


def require(text: str, needle: str, label: str) -> None:
    assert needle in text, f"{label}: missing {needle!r}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--output-dir", default="artifacts/ev154")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    out = (root / args.output_dir).resolve()
    text_out = out / "text"
    render_out = out / "renders"
    for p in (out, text_out, render_out):
        p.mkdir(parents=True, exist_ok=True)

    # Immutable/current authority guards.
    current_guards = {
        "audit_registry/finding_inventory_frozen_2026-09-03.json": FROZEN_INVENTORY_BLOB,
        "audit_registry/finding_revalidation_registry_v0.1.json": CENTRAL_PRESTATE_BLOB,
        "00_START_HERE/CURRENT_STATE.json": CURRENT_STATE_PRESTATE_BLOB,
        "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md": EVIDENCE_GATE_BLOB,
        "audit_registry/pdf_source_registry_v0.1.json": PDF_SOURCE_REGISTRY_BLOB,
        ".github/workflows/temp_pin_network_vdv301_3_ev154.yml": PIN_WORKFLOW_BLOB,
    }
    for rel, expected in current_guards.items():
        actual = git_blob(root, rel)
        assert actual == expected, f"authority changed: {rel}: {actual} != {expected}"

    frozen_guards = {
        "docs/pdf_xsd_semantic_audit/deep_read/VDV301-3_02-2020.md": DEEP_READ_BLOB,
        "docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_VDV301_3_02_2020_DEEP_READ_2026-08-29.md": HANDOFF_BLOB,
    }
    for rel, expected in frozen_guards.items():
        actual = git_blob(root, rel, FROZEN_SOURCE_HEAD)
        assert actual == expected, f"frozen authority changed: {rel}: {actual} != {expected}"

    # Frozen inventory/current revalidation ordering.
    central = load_json(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    assert central["next_revalidation_block"] == "NET"
    inv = central["inventory"]
    entries = inv["entries"]
    assert inv["state"] == "frozen" and inv["entry_count"] == 192 and len(entries) == 192
    terminal = sum(x["revalidation_state"] != "pending" for x in entries)
    pending = sum(x["revalidation_state"] == "pending" for x in entries)
    assert (terminal, pending) == (135, 57), (terminal, pending)
    by_id = {x["finding_id"]: x for x in entries}
    for fid in ["NET-001", "NET-002", "NET-003"]:
        assert by_id[fid] == {
            "finding_id": fid,
            "revalidation_state": "pending",
            "terminal_state_source": None,
        }
    first_pending = next(x["finding_id"] for x in entries if x["revalidation_state"] == "pending")
    assert first_pending == "NET-001", first_pending

    audit = load_json(root / "00_START_HERE/CURRENT_STATE.json")["audit"]
    assert audit["finding_revalidation_next_block"] == "NET"
    assert audit["finding_revalidation_completed_findings"] == 135
    assert audit["finding_revalidation_pending_findings"] == 57
    assert audit["finding_revalidation_current_block"] == "LS_V1.0"
    assert audit["finding_revalidation_latest_completed_block"] == "LS_V1.0"
    assert audit["latest_revalidation_evidence_id"] == "EV-153"

    # Exact PDF authority route and bytes.
    sources = load_json(root / "audit_registry/pdf_source_registry_v0.1.json")
    matches = [x for x in sources["sources"] if x["source_id"] == PDF_SOURCE_ID]
    assert len(matches) == 1
    source = matches[0]
    assert source["official_url"] == PDF_URL
    assert source["local_filename"] == PDF_FILENAME
    assert source["vdv_part"] == "301-3"
    assert source["version"] == "02-2020"

    pdf = root / "local_sources/vdv_pdfs" / PDF_FILENAME
    assert pdf.exists(), f"missing exact PDF: {pdf}"
    assert sha256(pdf) == PDF_SHA256
    assert pdf.stat().st_size == PDF_SIZE

    # Definition provenance: independent source read before historical reconciliation.
    deep = git_text(root, "docs/pdf_xsd_semantic_audit/deep_read/VDV301-3_02-2020.md", FROZEN_SOURCE_HEAD)
    handoff = git_text(root, "docs/pdf_xsd_semantic_audit/AUDIT_HANDOFF_DELTA_VDV301_3_02_2020_DEEP_READ_2026-08-29.md", FROZEN_SOURCE_HEAD)
    require(deep, "Historical Network findings/registers and RV-002 were not used to generate the observations below.", "independence boundary")
    require(deep, "This document has no XSD lane.", "authority lane")
    require(deep, "FR-NET20-OBS-001", "NET-001 provenance")
    require(deep, "FR-NET20-OBS-002", "NET-002 provenance")
    require(deep, "visible `IEE 802.3` on German page 11", "NET-003 provenance")
    require(deep, "historical `NET-001`", "NET-001 reconciliation")
    require(deep, "historical `NET-002`", "NET-002 reconciliation")
    require(deep, "historical `NET-003`", "NET-003 reconciliation")
    require(handoff, "Historical findings revalidated: `NET-001`, `NET-002`, `NET-003`.", "handoff provenance")
    require(handoff, "No XSD changed. No live network task was falsely marked passed.", "handoff boundary")

    page_raw: dict[int, str] = {}
    page_layout: dict[int, str] = {}
    render_hashes: dict[str, dict[str, int | str]] = {}
    for page in PDF_PAGES:
        page_raw[page] = text_page(pdf, page, text_out, "raw")
        page_layout[page] = text_page(pdf, page, text_out, "layout")
        image = render_page(pdf, page, render_out)
        render_hashes[str(page)] = {
            "sha256": sha256(image),
            "size_bytes": image.stat().st_size,
        }

    # NET-001 active disproof: wrong number is local English prose, not document identity.
    require(page_raw[8], "The VDV 303-3 describes requirements", "NET-001 English Scope")
    require(page_raw[8], "VDV-Schrift 301-3", "NET-001 English footer identity")
    require(page_raw[7], "Die VDV 301-3 beschreibt Anforderungen", "NET-001 German Scope identity")
    assert "VDV 303-3" not in page_raw[7]

    # NET-002 active disproof: same bilingual section has inconsistent numbering and the English ToC skips 2.3.4.
    require(page_raw[14], "2.3.4 Verkabelung von Endgeräten mit Switches", "NET-002 German section")
    require(page_raw[20], "2.3.5 Cabling of end devices with switches", "NET-002 English section")
    require(page_raw[6], "2.3.3 Coding and pin assignment", "NET-002 preceding English sequence")
    require(page_raw[6], "2.3.5 Cabling of end devices with switches", "NET-002 English ToC")
    assert "2.3.4 Cabling of end devices with switches" not in page_raw[6]

    # NET-003 active disproof: local typo is contradicted by correct IEEE spelling elsewhere in same exact writing.
    require(page_raw[11], "IEE 802.3", "NET-003 typo")
    require(page_raw[7], "IEEE 802.3", "NET-003 correct German context")
    require(page_raw[8], "IEEE 802.3", "NET-003 correct English context")
    require(page_raw[29], "IEEE 802.3af/at/bt", "NET-003 correct PoE reference")

    # The independent Deep Read already attempted broader falsification and rejected non-findings.
    for needle in [
        "CAT6/55 m is not promoted as an independent technical defect",
        "Figure/Table 2 and 3 naming is not promoted",
        "Empty version-history section is not promoted",
        "No XSD-gap finding",
        "No interactive-render failure finding",
    ]:
        require(deep, needle, "active falsification")

    result = {
        "evidence_id": "EV-154",
        "result": "PASS",
        "scope": ["NET-001", "NET-002", "NET-003"],
        "prestate": {
            "terminal": terminal,
            "pending": pending,
            "first_pending": first_pending,
            "expected_poststate_if_closed": {
                "terminal": 138,
                "pending": 54,
                "first_pending": "PCS-001",
            },
        },
        "authority": {
            "source_id": PDF_SOURCE_ID,
            "official_url": PDF_URL,
            "pdf_sha256": PDF_SHA256,
            "pdf_size_bytes": PDF_SIZE,
            "pin_run_id": PIN_RUN_ID,
            "pin_job_id": PIN_JOB_ID,
            "pin_artifact_id": PIN_ARTIFACT_ID,
            "pin_artifact_digest": PIN_ARTIFACT_DIGEST,
            "frozen_source_head": FROZEN_SOURCE_HEAD,
            "deep_read_blob": DEEP_READ_BLOB,
            "handoff_blob": HANDOFF_BLOB,
            "validation_lane": "physical/network/protocol documentation; no XSD lane",
        },
        "finding_results": {
            "NET-001": {
                "recommended_terminal_state": "context_verified",
                "classification_after_disproof": "English documentation-number typo",
                "physical_pages": [7, 8],
                "observed_wrong": "VDV 303-3",
                "document_identity_confirmed": "VDV 301-3",
                "alternate_document_identity_rejected": True,
            },
            "NET-002": {
                "recommended_terminal_state": "context_verified",
                "classification_after_disproof": "bilingual subsection-numbering editorial error",
                "physical_pages": [6, 14, 20],
                "german_number": "2.3.4",
                "english_number": "2.3.5",
                "english_toc_skip_confirmed": True,
            },
            "NET-003": {
                "recommended_terminal_state": "context_verified",
                "classification_after_disproof": "local IEEE spelling typo",
                "physical_pages": [7, 8, 11, 29],
                "observed_wrong": "IEE 802.3",
                "correct_spelling_elsewhere_same_writing": True,
            },
        },
        "fresh_visual_evidence": {
            "physical_pages": PDF_PAGES,
            "render_dpi": 180,
            "render_hashes": render_hashes,
            "manual_visual_review_required_before_closure": True,
        },
        "executable_evidence": {
            "applicable": False,
            "reason": "VDV 301-3 intentionally has no XSD lane; findings are documentation/editorial context findings.",
        },
        "regression_requirement": {
            "full_xsd_pool_count": 50,
            "purpose": "no-mutation/regression guard only",
        },
        "immutable_guards": {
            "frozen_inventory_blob": FROZEN_INVENTORY_BLOB,
            "frozen_inventory_mutated": False,
            "xsd_mutation_expected": False,
        },
    }
    (out / "ev154-result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("EV154_PASS NET-001=context_verified NET-002=context_verified NET-003=context_verified")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
