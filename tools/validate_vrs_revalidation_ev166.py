#!/usr/bin/env python3
"""Fail-closed aggregate evidence gate for final frozen VideoRecordingService findings VRS-001..011.

EV-166 validates the final pending block without mutating the registry, CURRENT_STATE,
frozen inventory, PDF pin registries, or any XSD. It preserves the V2.4 candidate-only
authority boundary and the 2026-08-29 VDV choice-notation correction.
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
PLAN = ROOT / "docs/pdf_xsd_semantic_audit/LEGACY_FINDING_REVALIDATION_PLAN.md"
ADDENDUM = ROOT / "docs/pdf_xsd_semantic_audit/VIDEO_RECORDING_SERVICE_FINDINGS_REGISTER_ADDENDUM.md"
CORRECTION = ROOT / "docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_CHOICE_NOTATION_2026-08-29.md"
DEEP_V10 = ROOT / "docs/pdf_xsd_semantic_audit/deep_read/VRS_V1.0.md"
DEEP_V20 = ROOT / "docs/pdf_xsd_semantic_audit/deep_read/VRS_V2.0.md"
DEEP_V24 = ROOT / "docs/pdf_xsd_semantic_audit/deep_read/VRS_V2.4.md"
EV103_DOC = ROOT / "docs/pdf_xsd_semantic_audit/24c_executable_validation_video_compositors.md"
EV103 = ROOT / "tools/validate_video_v20_compositors.py"
XSD_POOL = ROOT / "tools/validate_xsd_pool.py"
VRS20 = ROOT / "IBIS-IP_VideoRecordingService_V2.0.xsd"
VRS24 = ROOT / "IBIS-IP_VideoRecordingService_V2.4.xsd"
COMMON20 = ROOT / "IBIS-IP_common_V2.0.xsd"
ENUM20 = ROOT / "IBIS-IP_Enumerations_V2.0.xsd"

EXPECTED_BLOBS = {
    FROZEN: "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
    REGISTRY: "9fa016a223052e84610d9a47e08a81a5015bcb4d",
    STATE: "5f7e232d7f8b75ea2ff85e88c108dd4646aa0ba4",
    SOURCE_REGISTRY: "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
    SOURCE_PINS: "88349638b423689799af700e8a1c8ec99bbfb67b",
    EVIDENCE_GATE: "969cce8b14b50ded2ca5eb745674b894428ecf1a",
    PLAN: "b8a38bd09ca6239b96981548b7cfcbd49aa4c9d5",
    ADDENDUM: "d9392d85a855717ac8041f9d34b127160244f946",
    CORRECTION: "fe024798ba1b9803ec70ee3b97def63ee03d298f",
    DEEP_V10: "f3ae1d90bfdb2f7bb65042e152b0b29a43bf0987",
    DEEP_V20: "9d0efc0fcf230955fcacab206b1d9de08d699dfd",
    DEEP_V24: "cdcec9be131ea6aa91ed32196b0f1cc32f13442a",
    EV103_DOC: "77bceaea8c3a6d4f113d9b38ba6ef4062859c6d7",
    EV103: "9c85d362a597b357a69577477bacc8dc8fcbe177",
    XSD_POOL: "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd",
    VRS20: "6ef0dae64ce6f4d3aa4f652d6d166896e71aaac7",
    VRS24: "07ff2c41731e63fd85b203e4b8e0186136caaaaf",
    COMMON20: "8608e3dcd665c197c34da7f6ec6af5a3758da164",
    ENUM20: "27e3c183b00381d959622d13c10543123af8eef6",
}

PDF_EXPECTED = {
    "VRS_V1.0": {
        "sha256": "29d0bcb270fdab2119c4653296d4bca01e0f8b127eb9aaf393f66b2b34dcd390",
        "size": 1227302,
        "url": "https://www.vdv.de/301-2-12-sds.pdfx",
        "pin_run": "33204215397",
    },
    "VRS_V2.0": {
        "sha256": "fbe9e68e72de4e5450f562aa6a6117283a94f87a28bded0e05458670527b6c5f",
        "size": 941841,
        "url": "https://www.vdv.de/301-2-12-sdes-v2-0-video-recording-service.pdfx",
        "pin_run": "33206120045",
    },
    "VRS_V2.4": {
        "sha256": "d1a3cf36b4a9719ff8d233a84ade34ed7ff9c3dccb58f8a8688727d82a568a7b",
        "size": 1036423,
        "url": "https://www.vdv.de/301-2-12-sdg-v2.4-videorecordingservice.pdfx",
        "pin_run": "33206809886",
    },
}

TARGETS = {
    "VRS-001": "context_verified",
    "VRS-002": "context_verified",
    "VRS-003": "executable_confirmed",
    "VRS-004": "context_verified",
    "VRS-005": "context_verified",
    "VRS-006": "context_verified",
    "VRS-007": "withdrawn",
    "VRS-008": "context_verified",
    "VRS-009": "context_verified",
    "VRS-010": "context_verified",
    "VRS-011": "context_verified",
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
    parser.add_argument("--vrs-v10-pdf", required=True, type=Path)
    parser.add_argument("--vrs-v20-pdf", required=True, type=Path)
    parser.add_argument("--vrs-v24-pdf", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    for path, expected in EXPECTED_BLOBS.items():
        require(path.is_file(), f"required file exists: {path.relative_to(ROOT)}")
        require(blob(path) == expected, f"exact blob {path.relative_to(ROOT)} = {expected}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory remains exactly 192")
    require(all(fid in frozen.get("finding_ids", []) for fid in TARGETS), "all VRS targets are frozen inventory members")

    registry = load(REGISTRY)
    entries = registry["inventory"]["entries"]
    ids = [x["finding_id"] for x in entries]
    require(len(ids) == len(set(ids)) == 192, "registry contains exactly 192 unique findings")
    require(registry.get("next_revalidation_block") == "VRS", "prestate next block is VRS")
    require(counts(entries) == (181, 11), f"pre-VRS counts are 181/11, got {counts(entries)}")
    require(first_pending(entries) == "VRS-001", "pre-VRS first pending is VRS-001")
    by_id = {x["finding_id"]: x for x in entries}
    for fid in TARGETS:
        require(by_id[fid].get("revalidation_state") == "pending", f"{fid} is pending")
        require(by_id[fid].get("terminal_state_source") is None, f"{fid} has no premature terminal source")
    require(registry.get("revalidation_blocks", {}).get("VLS", {}).get("state") == "completed", "VLS is the prior completed block")
    require("VRS" not in registry.get("revalidation_blocks", {}), "VRS block is not already closed")

    audit = load(STATE)["audit"]
    require(audit.get("finding_revalidation_completed_findings") == 181, "CURRENT_STATE terminal count is 181")
    require(audit.get("finding_revalidation_pending_findings") == 11, "CURRENT_STATE pending count is 11")
    require(audit.get("finding_revalidation_next_block") == "VRS", "CURRENT_STATE next block is VRS")
    require(audit.get("finding_revalidation_latest_completed_block") == "VLS", "VLS is prior CURRENT_STATE completed block")
    require(audit.get("latest_revalidation_evidence_id") == "EV-165", "EV-165 is prior revalidation evidence")

    sources = load(SOURCE_REGISTRY)
    pins = load(SOURCE_PINS)
    pin_map = {x["source_id"]: x for x in pins.get("sources", [])}
    pdf_paths = {
        "VRS_V1.0": args.vrs_v10_pdf,
        "VRS_V2.0": args.vrs_v20_pdf,
        "VRS_V2.4": args.vrs_v24_pdf,
    }
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

    require_tokens(DEEP_V10, [
        "no VideoRecordingService V1.0 service XSD",
        "VRS V2.0 or V2.4 XSD must not be substituted for V1.0",
        "VRS-004 - SubscribeDisplayState / UnsubscribeDisplayState headings",
        "VRS-008 - StopRecording section names StopRecordingERM",
        "targeted material visual checks: complete",
    ], "VRS V1.0 deep read")
    require_tokens(DEEP_V20, [
        "6ef0dae64ce6f4d3aa4f652d6d166896e71aaac7",
        "`VRS-003` is freshly PDF/XSD reconfirmed and remains executable-confirmed.",
        "This is not a PDF/XSD mismatch.",
        "VideoRecordingService.PauseRecordingRRMRequestStruture",
        "targeted visual checks: complete",
    ], "VRS V2.0 deep read")
    require_tokens(DEEP_V24, [
        "state: open",
        "merged: false",
        "head: 0aa728aab47a7f13b6f36da415581d51592c4ca7",
        "service XSD blob: 07ff2c41731e63fd85b203e4b8e0186136caaaaf",
        "V2.4 XSD authority = candidate/integration only",
        "VRS-010 - Pause table caption describes wrong role/name across all checked VRS PDFs",
        "VRS-011 - V2.4 VideoRecordingStateStructure table describes itself as Pause request data",
    ], "VRS V2.4 deep read")
    require_tokens(CORRECTION, [
        "VRS-007 - withdrawn after correction",
        "state: withdrawn_after_deep_read_correction",
        "VRS-003: remains executable-confirmed, description refined",
        "A prefixed minus sign denotes XML choice.",
    ], "choice-notation correction")
    require_tokens(EV103_DOC, [
        "VRS-003 remains executable-confirmed",
        "GitHub Actions run: 33111119723",
        "job: 98653897734",
    ], "EV-103 evidence record")
    require_tokens(ADDENDUM, [
        "VRS-001 confirmed provenance gap",
        "VRS-002 candidate/official authority gap",
        "VRS-003 executable-confirmed",
        "VRS-005 persists as exact typo-like identifier",
        "VRS-007 WITHDRAWN",
        "VRS-011 V2.4-only copy/paste role error",
    ], "VRS finding register")
    require_tokens(PLAN, [
        "zero pending findings",
        "zero unresolved finding that could alter SDK accept/reject/routing behavior",
        "This phase is complete only when the machine-readable revalidation registry contains a terminal state for every frozen finding inventory entry",
    ], "revalidation plan")

    projected = [dict(x) for x in entries]
    projected_by_id = {x["finding_id"]: x for x in projected}
    for fid, target in TARGETS.items():
        projected_by_id[fid]["revalidation_state"] = target
        projected_by_id[fid]["terminal_state_source"] = "docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_VRS_2026-09-14.md"
    require(counts(projected) == (192, 0), f"projected post-VRS counts are 192/0, got {counts(projected)}")
    require(first_pending(projected) is None, "projected post-VRS has no pending finding")

    unresolved = [x["finding_id"] for x in projected if x.get("revalidation_state") == "unresolved"]
    require(unresolved == ["CIS-001"], f"only pre-existing unresolved terminal finding is CIS-001, got {unresolved}")

    evidence = {
        "evidence_id": "EV-166",
        "block": "VRS",
        "prestate": {"terminal": 181, "pending": 11, "first_pending": "VRS-001"},
        "projected_poststate": {"terminal": 192, "pending": 0, "first_pending": None},
        "findings": TARGETS,
        "remaining_unresolved_terminal_findings": unresolved,
        "readiness_reconciliation_required_after_vrs": True,
        "authority_boundary": {
            "VRS_V1.0": "official public VDV PDF authority; exact official V1.0 VideoRecordingService XSD unresolved; no nearby-version substitution",
            "VRS_V2.0": "official VDV-301-2.0 service/Common/Enums family",
            "VRS_V2.4": "official public PDF plus open unmerged PR #27 candidate/integration XSD only",
            "EV-103": "official V2.0 executable compositor evidence for VRS-003; V2.4 candidate control explanatory only",
            "VRS-007": "withdrawn because leading minus is valid VDV XML-choice notation",
        },
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"PASSED: EV-166 VRS final-block aggregate gate; wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
