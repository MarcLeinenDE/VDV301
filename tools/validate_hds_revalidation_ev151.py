#!/usr/bin/env python3
"""EV-151: fail-closed terminal revalidation of HDS-001.

HTMLDisplayService V2.1/V2.2/V2.2a is intentionally a non-XSD DNS-SD/HTTP
profile. This validator pins the three current source/deep-read lanes, proves
that no dedicated HDS service schema is present in the applicable official
release inventories/current integration root, and delegates executable
discovery-profile semantics to RV-002.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

FROZEN_INVENTORY_BLOB = "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf"
RV002_BLOB = "946488b2b7d08d681089ec5bbbfd6558dab57e35"
RUNTIME_PROFILE_BLOB = "4473b913ad4576982789b2791b44e2cf1cba0c8d"

VERSIONS = {
    "HDS_V2.1": {
        "official_url": "https://www.vdv.de/301-2-17-sds-v2-1-htmldisplayservice.pdfx",
        "local_filename": "HDS_V2.1.pdf",
        "pdf_sha256": "c8aa91626bf60c8e74200200d63d44d497aeb3ab240c47039333b2c922a0e495",
        "pdf_size_bytes": 734901,
        "pin_run": "33265498869",
        "deep_read": "docs/pdf_xsd_semantic_audit/deep_read/HDS_V2.1.md",
        "deep_read_blob": "a71603fd2f1c1ad177da23722d07ee36af5eea87",
        "delta": "audit_registry/deep_read_findings_delta_hds_v21_2026-08-29.json",
        "delta_blob": "3e0c7c13353d3fc868ec57d928afe6e48a0ca19e",
        "prior_rv002_run": "33266402138",
        "official_tag": "VDV-301-2.1",
    },
    "HDS_V2.2": {
        "official_url": "https://www.vdv.de/301-2-17-sdes-v2-2-htmldisplayservice.pdfx",
        "local_filename": "HDS_V2.2.pdf",
        "pdf_sha256": "bf62b7a8b6cfdf654181b48da2d85a805118687c7463a46fadfd32679c9b7577",
        "pdf_size_bytes": 802399,
        "pin_run": "33266549282",
        "deep_read": "docs/pdf_xsd_semantic_audit/deep_read/HDS_V2.2.md",
        "deep_read_blob": "bcee902b1bde7fdd7a705dac4dcabc35f6c1700f",
        "delta": "audit_registry/deep_read_findings_delta_hds_v22_2026-08-29.json",
        "delta_blob": "0706cc787637a9b7e9d9534429c0854fc02de09a",
        "prior_rv002_run": "33266770833",
        "official_tag": "VDV-301-2.2",
    },
    "HDS_V2.2a": {
        "official_url": "https://www.vdv.de/301-2-17-sdes-v2-2a-htmldisplayservice.pdfx",
        "local_filename": "HDS_V2.2a.pdf",
        "pdf_sha256": "f3da1994e719572ba1689aea2448b9533faf9e8fbe42720b9e737b98edd8b0f8",
        "pdf_size_bytes": 431875,
        "pin_run": "33266884196",
        "deep_read": "docs/pdf_xsd_semantic_audit/deep_read/HDS_V2.2a.md",
        "deep_read_blob": "938e44a85256dcffba7e7201c00b6a1254e6d5b0",
        "delta": "audit_registry/deep_read_findings_delta_hds_v22a_2026-08-29.json",
        "delta_blob": "a25aaa64e81a07b41b190047067fbe4030ad3ff9",
        "prior_rv002_run": "33267198470",
        "official_tag": None,
    },
}


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


def tag_paths(root: Path, tag: str) -> list[str]:
    return subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", tag], cwd=root, text=True
    ).splitlines()


def hds_schema_candidates(paths: list[str]) -> list[str]:
    needles = ("htmldisplay", "html_display", "html-display")
    return [
        p for p in paths
        if p.lower().endswith(".xsd") and any(n in p.lower() for n in needles)
    ]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--output-dir", default="artifacts/ev151")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    out = (root / args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    guards = {
        "audit_registry/finding_inventory_frozen_2026-09-03.json": FROZEN_INVENTORY_BLOB,
        "tools/validate_discovery_runtime_rv002.py": RV002_BLOB,
        "tools/runtime_discovery_profile.py": RUNTIME_PROFILE_BLOB,
    }
    for meta in VERSIONS.values():
        guards[meta["deep_read"]] = meta["deep_read_blob"]
        guards[meta["delta"]] = meta["delta_blob"]
    for rel, expected in guards.items():
        actual = git_blob(root, rel)
        assert actual == expected, f"authority changed: {rel}: {actual} != {expected}"

    central = load_json(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    assert central["next_revalidation_block"] == "HDS"
    inv = central["inventory"]
    assert inv["state"] == "frozen"
    assert inv["entry_count"] == 192 and len(inv["entries"]) == 192
    terminal = sum(x["revalidation_state"] != "pending" for x in inv["entries"])
    pending = sum(x["revalidation_state"] == "pending" for x in inv["entries"])
    assert (terminal, pending) == (126, 66), (terminal, pending)
    by_id = {x["finding_id"]: x for x in inv["entries"]}
    assert by_id["HDS-001"] == {
        "finding_id": "HDS-001",
        "revalidation_state": "pending",
        "terminal_state_source": None,
    }
    first_pending = next(x["finding_id"] for x in inv["entries"] if x["revalidation_state"] == "pending")
    assert first_pending == "HDS-001"

    state = load_json(root / "00_START_HERE/CURRENT_STATE.json")["audit"]
    assert state["finding_revalidation_next_block"] == "HDS"
    assert state["finding_revalidation_completed_findings"] == 126
    assert state["finding_revalidation_pending_findings"] == 66
    assert state["latest_revalidation_evidence_id"] == "EV-150"

    sources = load_json(root / "audit_registry/pdf_source_registry_v0.1.json")
    pins = load_json(root / "audit_registry/pdf_source_pins_v0.1.json")
    source_by = {x["source_id"]: x for x in sources["sources"]}
    pin_by = {x["source_id"]: x for x in pins["sources"]}

    pdf_results = {}
    for sid, meta in VERSIONS.items():
        src = source_by[sid]
        pin = pin_by[sid]
        assert src["official_url"] == meta["official_url"]
        assert src["local_filename"] == meta["local_filename"]
        assert pin["expected_sha256"] == meta["pdf_sha256"]
        assert int(pin["expected_size_bytes"]) == meta["pdf_size_bytes"]
        assert str(pin["evidence_run_id"]) == meta["pin_run"]
        assert pin["deep_read_source_ready"] is True

        pdf = root / "local_sources/vdv_pdfs" / meta["local_filename"]
        assert pdf.exists(), f"missing fetched PDF for {sid}: {pdf}"
        actual_sha = sha256(pdf)
        actual_size = pdf.stat().st_size
        assert actual_sha == meta["pdf_sha256"], (sid, actual_sha)
        assert actual_size == meta["pdf_size_bytes"], (sid, actual_size)

        delta = load_json(root / meta["delta"])
        hds = delta["revalidated_findings"]["HDS-001"]
        assert hds["classification"] == "ok_with_note"
        assert hds["validation_behavior"] == "discovery_http_profile_not_service_xsd"
        assert meta["prior_rv002_run"] in hds["state"]

        deep = (root / meta["deep_read"]).read_text(encoding="utf-8")
        assert "non-XSD DNS-SD/HTTP profile" in deep
        assert "HDS-001" in deep
        assert meta["prior_rv002_run"] in deep

        pdf_results[sid] = {
            "sha256": actual_sha,
            "size_bytes": actual_size,
            "deep_read_blob": meta["deep_read_blob"],
            "delta_blob": meta["delta_blob"],
            "prior_rv002_run": meta["prior_rv002_run"],
        }

    official_tag_checks = {}
    for sid in ("HDS_V2.1", "HDS_V2.2"):
        tag = VERSIONS[sid]["official_tag"]
        paths = tag_paths(root, tag)
        candidates = hds_schema_candidates(paths)
        assert candidates == [], f"unexpected dedicated HDS XSD in {tag}: {candidates}"
        official_tag_checks[tag] = {"dedicated_hds_xsd": False, "tree_paths_checked": len(paths)}

    root_xsds = sorted(p.name for p in root.glob("*.xsd"))
    assert len(root_xsds) == 50, len(root_xsds)
    current_candidates = hds_schema_candidates(root_xsds)
    assert current_candidates == [], current_candidates

    result = {
        "evidence_id": "EV-151",
        "result": "PASS",
        "scope": ["HDS-001"],
        "recommended_terminal_states": {"HDS-001": "context_verified"},
        "finding_classification": "intentional_non_xsd_dns_sd_http_profile",
        "finding_claim": (
            "Absence of a dedicated HTMLDisplayService XSD is intentional; "
            "HDS V2.1/V2.2/V2.2a route through version-specific DNS-SD/HTTP "
            "profile validation rather than a service-XSD validator."
        ),
        "authority": pdf_results,
        "runtime_authority": {
            "rv002_blob": RV002_BLOB,
            "runtime_profile_blob": RUNTIME_PROFILE_BLOB,
            "execution_required_by_workflow": True,
            "live_network_claim": False,
        },
        "active_disproof": {
            "official_release_tag_inventory_checks": official_tag_checks,
            "v2_2a_dedicated_release_tag_exists": False,
            "integration_root_xsd_count": len(root_xsds),
            "integration_dedicated_hds_xsd": False,
        },
        "version_boundaries": {
            "2.1": {
                "protocol": "_http._tcp",
                "txt": ["content", "path"],
                "endpoint_source": "SRV target/port plus TXT path",
            },
            "2.2": {
                "canonical_protocol": "_http._tcp",
                "txt": ["content", "url"],
                "endpoint_source": "TXT url",
                "transition_note": "_ibisip_http._tcp only by later V2.2a compatibility context",
            },
            "2.2a": {
                "protocol_labels": ["_http._tcp", "_ibisip_http._tcp"],
                "legacy_label": "_http._tcp deprecated/future-not-recommended",
                "transition_label": "_ibisip_http._tcp documented transition/future label",
                "txt": ["content", "url"],
                "endpoint_source": "TXT url",
            },
        },
        "prior_visual_evidence": {
            "HDS_V2.1": {"pages": [7, 8, 9, 10], "render_run": "33265541783"},
            "HDS_V2.2": {"pages": [7, 8, 9, 10, 11], "render_run": "33266588436"},
            "HDS_V2.2a": {"rendered_pages": list(range(7, 15)), "focus_pages": [8, 10, 11], "render_run": "33266920928"},
            "status": "current canonical deep reads already contain targeted pinned-byte visual review; no unresolved visual gap for HDS-001",
        },
        "immutable_guards": {
            "frozen_inventory_blob": FROZEN_INVENTORY_BLOB,
            "frozen_inventory_mutated": False,
            "xsd_mutated": False,
        },
    }
    (out / "ev151-result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("PASSED: EV-151 HDS-001 intentional non-XSD profile revalidation confirmed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
