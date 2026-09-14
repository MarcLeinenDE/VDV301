#!/usr/bin/env python3
"""Fail-closed aggregate evidence gate for frozen VideoDisplayService findings VDS-001..008.

EV-164 revalidates the VDS block without mutating the finding registry, CURRENT_STATE,
the frozen inventory, or any XSD. The caller supplies the exact byte-pinned VDS V1.0
and V2.0 PDFs; executable V2.0 compositor behaviour is rerun separately via EV-103.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

FROZEN = ROOT / "audit_registry/finding_inventory_frozen_2026-09-03.json"
REGISTRY = ROOT / "audit_registry/finding_revalidation_registry_v0.1.json"
STATE = ROOT / "00_START_HERE/CURRENT_STATE.json"
SOURCE_REGISTRY = ROOT / "audit_registry/pdf_source_registry_v0.1.json"
SOURCE_PINS = ROOT / "audit_registry/pdf_source_pins_v0.1.json"
EVIDENCE_GATE = ROOT / "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md"
ADDENDUM = ROOT / "docs/pdf_xsd_semantic_audit/VIDEO_DISPLAY_SERVICE_FINDINGS_REGISTER_ADDENDUM.md"
CORRECTION = ROOT / "docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_CHOICE_NOTATION_2026-08-29.md"
DEEP_V10 = ROOT / "docs/pdf_xsd_semantic_audit/deep_read/VDS_V1.0.md"
DEEP_V20 = ROOT / "docs/pdf_xsd_semantic_audit/deep_read/VDS_V2.0.md"
DEEP_VLS10 = ROOT / "docs/pdf_xsd_semantic_audit/deep_read/VLS_V1.0.md"
DEEP_VRS10 = ROOT / "docs/pdf_xsd_semantic_audit/deep_read/VRS_V1.0.md"
EV103_DOC = ROOT / "docs/pdf_xsd_semantic_audit/24c_executable_validation_video_compositors.md"
EV103 = ROOT / "tools/validate_video_v20_compositors.py"
XSD_POOL = ROOT / "tools/validate_xsd_pool.py"
VDS20 = ROOT / "IBIS-IP_VideoDisplayService_V2.0.xsd"
COMMON20 = ROOT / "IBIS-IP_common_V2.0.xsd"
ENUM20 = ROOT / "IBIS-IP_Enumerations_V2.0.xsd"

EXPECTED_BLOBS = {
    FROZEN: "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
    REGISTRY: "13ef10dfe353ad51b2cecd371333bd12e35c8e6b",
    STATE: "81d24c501c5fd483853075fbdc9edeecdc7d6df7",
    SOURCE_REGISTRY: "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
    SOURCE_PINS: "88349638b423689799af700e8a1c8ec99bbfb67b",
    EVIDENCE_GATE: "969cce8b14b50ded2ca5eb745674b894428ecf1a",
    ADDENDUM: "d5d2903ed04448ba3793b4eb1b7aa2c192ca5b3a",
    CORRECTION: "fe024798ba1b9803ec70ee3b97def63ee03d298f",
    DEEP_V10: "9ee386d7b2c869b1dd74c330797a30a49aedde1d",
    DEEP_V20: "0989aa830dba52a8b562c7abc8d72f63b8c27f3d",
    DEEP_VLS10: "1fa2c8949144c902feeba4aeaa714e029f993fa0",
    DEEP_VRS10: "f3ae1d90bfdb2f7bb65042e152b0b29a43bf0987",
    EV103_DOC: "77bceaea8c3a6d4f113d9b38ba6ef4062859c6d7",
    EV103: "9c85d362a597b357a69577477bacc8dc8fcbe177",
    XSD_POOL: "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd",
    VDS20: "fcfdadd3b62a584370cae326004050b4dc832e23",
    COMMON20: "8608e3dcd665c197c34da7f6ec6af5a3758da164",
    ENUM20: "27e3c183b00381d959622d13c10543123af8eef6",
}

PDF_EXPECTED = {
    "VDS_V1.0": {
        "sha256": "9280cc239cf71bb158ab5941b522a2c4c822420e07ed44f4d4111d9689418480",
        "size": 1202943,
        "url": "https://www.vdv.de/301-2-13-sds.pdfx",
        "pin_run": "33225713193",
        "visual_run": "33225843645",
        "visual_artifact": "9706815054",
        "visual_digest": "sha256:ff288301329a8fc3ea7e5e1fa568f06b0b6b5c4e76270f9c720a3a60eb29c9cd",
    },
    "VDS_V2.0": {
        "sha256": "c287df20d8225af2afcd37dfdb487eb4922b89ce78c287da91745d12b410c8a2",
        "size": 903444,
        "url": "https://www.vdv.de/301-2-13-sdes-v2-0-video-display-service.pdfx",
        "pin_run": "33226181059",
        "visual_run": "33226294383",
        "visual_artifact": "9706970109",
        "visual_digest": "sha256:a8f9a098f7bbf534d41c1586230a45518ada62c67482494d8ba9b0debb617fb1",
    },
}

EV103_META = {
    "run": "33111119723",
    "job": "98653897734",
    "artifact": "9662552176",
    "digest": "sha256:b97d2e4506ffd63b8ff7985765131826d409e32769fb3a08193084134ca00ec0",
    "head": "d4ffe09067cb38bf7f78ba295e029902078ed18d",
}

TARGETS = {
    "VDS-001": "context_verified",
    "VDS-002": "executable_confirmed",
    "VDS-003": "executable_confirmed",
    "VDS-004": "executable_confirmed",
    "VDS-005": "context_verified",
    "VDS-006": "context_verified",
    "VDS-007": "context_verified",
    "VDS-008": "context_verified",
}
TERMINAL = {"context_verified", "executable_confirmed", "contextual_not_defect", "withdrawn", "unresolved", "superseded"}


def fail(message: str) -> None:
    print(f"FAIL {message}")
    raise SystemExit(1)


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)
    print(f"OK  {message}")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def counts(entries: list[dict]) -> tuple[int, int]:
    return (
        sum(x.get("revalidation_state") in TERMINAL for x in entries),
        sum(x.get("revalidation_state") == "pending" for x in entries),
    )


def first_pending(entries: list[dict]) -> str | None:
    return next((x.get("finding_id") for x in entries if x.get("revalidation_state") == "pending"), None)


def source_entry(registry: dict, source_id: str) -> dict:
    return next((x for x in registry.get("sources", []) if x.get("source_id") == source_id), {})


def require_tokens(path: Path, tokens: list[str], label: str) -> None:
    content = text(path)
    for token in tokens:
        require(token in content, f"{label} contains authoritative token: {token}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vds-v10-pdf", required=True, type=Path)
    parser.add_argument("--vds-v20-pdf", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    for path, expected in EXPECTED_BLOBS.items():
        require(path.is_file(), f"required file exists: {path.relative_to(ROOT)}")
        require(blob(path) == expected, f"exact blob {path.relative_to(ROOT)} = {expected}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory remains exactly 192")
    require(all(fid in frozen.get("finding_ids", []) for fid in TARGETS), "all VDS targets are frozen inventory members")

    registry = load(REGISTRY)
    entries = registry["inventory"]["entries"]
    ids = [x["finding_id"] for x in entries]
    require(len(ids) == len(set(ids)) == 192, "registry contains exactly 192 unique findings")
    require(registry.get("next_revalidation_block") == "VDS", "prestate next block is VDS")
    require(counts(entries) == (168, 24), f"pre-VDS counts are 168/24, got {counts(entries)}")
    require(first_pending(entries) == "VDS-001", "pre-VDS first pending is VDS-001")
    by_id = {x["finding_id"]: x for x in entries}
    for fid in TARGETS:
        require(by_id[fid].get("revalidation_state") == "pending", f"{fid} is pending")
        require(by_id[fid].get("terminal_state_source") is None, f"{fid} has no premature terminal source")
    require(by_id["VLS-001"].get("revalidation_state") == "pending", "VLS-001 remains pending before VDS closure")
    require(registry.get("revalidation_blocks", {}).get("TVS", {}).get("state") == "completed", "TVS is the prior completed block")
    require("VDS" not in registry.get("revalidation_blocks", {}), "VDS block is not already closed")

    audit = load(STATE)["audit"]
    require(audit.get("finding_revalidation_completed_findings") == 168, "CURRENT_STATE terminal count is 168")
    require(audit.get("finding_revalidation_pending_findings") == 24, "CURRENT_STATE pending count is 24")
    require(audit.get("finding_revalidation_next_block") == "VDS", "CURRENT_STATE next block is VDS")
    require(audit.get("finding_revalidation_latest_completed_block") == "TVS", "TVS is prior CURRENT_STATE completed block")
    require(audit.get("latest_revalidation_evidence_id") == "EV-163", "EV-163 is prior revalidation evidence")

    sources = load(SOURCE_REGISTRY)
    pins = load(SOURCE_PINS)
    pin_map = {x["source_id"]: x for x in pins.get("sources", [])}
    pdf_paths = {"VDS_V1.0": args.vds_v10_pdf, "VDS_V2.0": args.vds_v20_pdf}
    for source_id, expected in PDF_EXPECTED.items():
        src = source_entry(sources, source_id)
        pin = pin_map.get(source_id, {})
        require(src.get("official_url") == expected["url"], f"{source_id} official URL pinned")
        require(pin.get("expected_sha256") == expected["sha256"], f"{source_id} registry SHA-256 pinned")
        require(pin.get("expected_size_bytes") == expected["size"], f"{source_id} registry size pinned")
        require(str(pin.get("evidence_run_id")) == expected["pin_run"], f"{source_id} pin run pinned")
        pdf = pdf_paths[source_id]
        require(pdf.is_file(), f"{source_id} PDF supplied")
        require(pdf.stat().st_size == expected["size"], f"{source_id} PDF byte size exact")
        require(sha256_file(pdf) == expected["sha256"], f"{source_id} PDF SHA-256 exact")

    require_tokens(
        DEEP_V10,
        [
            "no VideoDisplayService V1.0 service XSD",
            "VDS V2.0 XSD must NOT be substituted for V1.0",
            "Targeted material findings are visually confirmed",
            "Fehler! Verweisquelle konnte nicht gefunden werden.",
            "VideoDisplayService v1.1 1.0, 05/2017",
        ],
        "VDS V1.0 deep read",
    )
    require_tokens(
        DEEP_V20,
        [
            "fcfdadd3b62a584370cae326004050b4dc832e23",
            "Targeted material findings are visually confirmed",
            "VDS-005 is V1.0-only",
            "RTP  Real Time Protocol",
            "SOA  Server Oriented Architecture",
            "EV-103 / run `33111119723`",
        ],
        "VDS V2.0 deep read",
    )
    require_tokens(
        CORRECTION,
        [
            "A prefixed minus sign denotes XML choice.",
            "VDS-006 - refined, not a cardinality error",
            "pdf_choice_notation_application_anomaly_candidate",
            "incomplete or degenerate application",
            "VDS-002: remains executable-confirmed",
            "VDS-004: remains executable-confirmed",
        ],
        "choice-notation correction",
    )
    require_tokens(
        DEEP_VLS10,
        ["VideoDisplayService v1.1 1.0, 05/2017", "cross-document follow-up"],
        "VLS V1.0 cross-document evidence",
    )
    require_tokens(
        DEEP_VRS10,
        ["VideoDisplayService `v1.1` label", "dedicated VDS V1.0 read"],
        "VRS V1.0 cross-document evidence",
    )
    require_tokens(
        EV103_DOC,
        [
            "VDS-002 remains executable-confirmed.",
            "VDS-003 remains executable-confirmed",
            "VDS-004 remains executable-confirmed",
            "GitHub Actions run: 33111119723",
            "job: 98653897734",
        ],
        "EV-103 evidence record",
    )
    require_tokens(
        ADDENDUM,
        [
            "VDS-001 strongly confirmed V1.0 provenance gap",
            "VDS-002 executable-confirmed",
            "VDS-003 executable-confirmed",
            "VDS-004 executable-confirmed",
            "VDS-005 V1.0-only, corrected in V2.0",
            "VDS-006 refined: choice-notation application anomaly",
            "VDS-007 cross-document V1.1 label error confirmed",
            "VDS-008 RTP/SOA abbreviation expansion error",
        ],
        "VDS finding register",
    )

    projected = [dict(x) for x in entries]
    projected_by_id = {x["finding_id"]: x for x in projected}
    for fid, target in TARGETS.items():
        projected_by_id[fid]["revalidation_state"] = target
        projected_by_id[fid]["terminal_state_source"] = "EV-164 projection only"
    require(counts(projected) == (176, 16), f"projected post-VDS counts are 176/16, got {counts(projected)}")
    require(first_pending(projected) == "VLS-001", f"projected first pending is VLS-001, got {first_pending(projected)}")

    manifest = {
        "evidence_id": "EV-164",
        "scope": "VideoDisplayService frozen findings VDS-001..VDS-008",
        "prestate": {"terminal": 168, "pending": 24, "first_pending": "VDS-001", "next_block": "VDS"},
        "projected_poststate": {"terminal": 176, "pending": 16, "first_pending": "VLS-001", "next_block": "VLS"},
        "target_terminal_states": TARGETS,
        "authority": {
            "vds_v1_0": "official public PDF; exact official V1.0 service XSD unresolved; no V2.0 substitution",
            "vds_v2_0": {
                "official_tag": "VDV-301-2.0",
                "official_commit": "f2569a91f0a7c737a0ca7c0280b28ad223d7ee08",
                "service_blob": EXPECTED_BLOBS[VDS20],
                "common_blob": EXPECTED_BLOBS[COMMON20],
                "enumerations_blob": EXPECTED_BLOBS[ENUM20],
            },
            "pdfs": PDF_EXPECTED,
            "ev103": EV103_META,
            "external_terminology": {
                "RTP": "RFC 3550 / real-time transport protocol",
                "SOA": "OASIS Reference Model / Service Oriented Architecture",
                "validation_behavior_impact": "none",
            },
        },
        "finding_rationale": {
            "VDS-001": "context-verified provenance gap; unresolved strict V1.0 routing is the consequence, not an unverified finding claim",
            "VDS-002": "official V2.0 PDF/XSD mismatch plus EV-103 executable compositor evidence",
            "VDS-003": "official V2.0 PDF/XSD mismatch plus EV-103 executable compositor evidence",
            "VDS-004": "official V2.0 PDF/XSD mismatch plus EV-103 executable compositor evidence",
            "VDS-005": "byte-pinned V1.0 visual confirmation; corrected/absent in V2.0; documentation-only",
            "VDS-006": "corrected claim only: valid leading-minus choice notation, but visually verified incomplete/degenerate application; documentation-only",
            "VDS-007": "cross-document v1.1 reference-label error verified against dedicated VDS V1.0 identity/catalog; no V1.1 schema/profile alias",
            "VDS-008": "RTP/SOA expansion error verified against external terminology; no XML/XSD impact",
        },
        "visual_evidence": {
            source_id: {
                "run": data["visual_run"],
                "artifact": data["visual_artifact"],
                "digest": data["visual_digest"],
            }
            for source_id, data in PDF_EXPECTED.items()
        },
        "immutability": {"xsd_mutation": False, "frozen_inventory_mutation": False, "registry_mutation": False, "current_state_mutation": False},
        "closure_authorized_only_after_ci_success": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"PASSED: EV-164 VDS aggregate evidence gate; wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
