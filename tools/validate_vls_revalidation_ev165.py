#!/usr/bin/env python3
"""Fail-closed aggregate evidence gate for frozen VideoLiveService findings VLS-001..005.

EV-165 revalidates the VLS block without mutating the finding registry, CURRENT_STATE,
the frozen inventory, or any XSD. Exact byte-pinned VLS V1.0/V2.0 PDFs are supplied
by CI; executable V2.0 compositor behaviour is rerun separately through EV-103.
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
ADDENDUM = ROOT / "docs/pdf_xsd_semantic_audit/VIDEO_LIVE_SERVICE_FINDINGS_REGISTER_ADDENDUM.md"
CORRECTION = ROOT / "docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_CHOICE_NOTATION_2026-08-29.md"
DEEP_V10 = ROOT / "docs/pdf_xsd_semantic_audit/deep_read/VLS_V1.0.md"
DEEP_V20 = ROOT / "docs/pdf_xsd_semantic_audit/deep_read/VLS_V2.0.md"
EV103_DOC = ROOT / "docs/pdf_xsd_semantic_audit/24c_executable_validation_video_compositors.md"
EV103 = ROOT / "tools/validate_video_v20_compositors.py"
XSD_POOL = ROOT / "tools/validate_xsd_pool.py"
VLS20 = ROOT / "IBIS-IP_VideoLiveService_V2.0.xsd"
COMMON20 = ROOT / "IBIS-IP_common_V2.0.xsd"
ENUM20 = ROOT / "IBIS-IP_Enumerations_V2.0.xsd"

EXPECTED_BLOBS = {
    FROZEN: "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
    REGISTRY: "62a3ecdd3f77c25dc6ed8e6754bc351db824ebb5",
    STATE: "1c496ec0e0f3a45c0120650adf4df1a62659b225",
    SOURCE_REGISTRY: "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
    SOURCE_PINS: "88349638b423689799af700e8a1c8ec99bbfb67b",
    EVIDENCE_GATE: "969cce8b14b50ded2ca5eb745674b894428ecf1a",
    ADDENDUM: "fa3c1be9dfb34726fdf73ae8c518a051021c39ed",
    CORRECTION: "fe024798ba1b9803ec70ee3b97def63ee03d298f",
    DEEP_V10: "1fa2c8949144c902feeba4aeaa714e029f993fa0",
    DEEP_V20: "d719cebafd51d07b486d9f6ccd1b65e9b101329d",
    EV103_DOC: "77bceaea8c3a6d4f113d9b38ba6ef4062859c6d7",
    EV103: "9c85d362a597b357a69577477bacc8dc8fcbe177",
    XSD_POOL: "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd",
    VLS20: "d8c52f5de9ef3f5915524fef12da11eabf0ca041",
    COMMON20: "8608e3dcd665c197c34da7f6ec6af5a3758da164",
    ENUM20: "27e3c183b00381d959622d13c10543123af8eef6",
}

PDF_EXPECTED = {
    "VLS_V1.0": {
        "sha256": "f535673427ff8f495102e1fc7723ca157408949b981572c4342b862f6d9c2a3c",
        "size": 1166329,
        "url": "https://www.vdv.de/301-2-11-sds.pdfx",
        "pin_run": "33197955036",
    },
    "VLS_V2.0": {
        "sha256": "d75a543c138f21c4ad370925ca7f306bcde7d692ce793ddc1d51bdcf6032787b",
        "size": 1218788,
        "url": "https://www.vdv.de/301-2-11-sdes-v2-0-video-live-service.pdfx",
        "pin_run": "33203673347",
    },
}

TARGETS = {
    "VLS-001": "context_verified",
    "VLS-002": "executable_confirmed",
    "VLS-003": "context_verified",
    "VLS-004": "context_verified",
    "VLS-005": "context_verified",
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
    parser.add_argument("--vls-v10-pdf", required=True, type=Path)
    parser.add_argument("--vls-v20-pdf", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    for path, expected in EXPECTED_BLOBS.items():
        require(path.is_file(), f"required file exists: {path.relative_to(ROOT)}")
        require(blob(path) == expected, f"exact blob {path.relative_to(ROOT)} = {expected}")

    frozen = load(FROZEN)
    require(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory remains exactly 192")
    require(all(fid in frozen.get("finding_ids", []) for fid in TARGETS), "all VLS targets are frozen inventory members")

    registry = load(REGISTRY)
    entries = registry["inventory"]["entries"]
    ids = [x["finding_id"] for x in entries]
    require(len(ids) == len(set(ids)) == 192, "registry contains exactly 192 unique findings")
    require(registry.get("next_revalidation_block") == "VLS", "prestate next block is VLS")
    require(counts(entries) == (176, 16), f"pre-VLS counts are 176/16, got {counts(entries)}")
    require(first_pending(entries) == "VLS-001", "pre-VLS first pending is VLS-001")
    by_id = {x["finding_id"]: x for x in entries}
    for fid in TARGETS:
        require(by_id[fid].get("revalidation_state") == "pending", f"{fid} is pending")
        require(by_id[fid].get("terminal_state_source") is None, f"{fid} has no premature terminal source")
    require(by_id["VRS-001"].get("revalidation_state") == "pending", "VRS-001 remains pending before VLS closure")
    require(registry.get("revalidation_blocks", {}).get("VDS", {}).get("state") == "completed", "VDS is the prior completed block")
    require("VLS" not in registry.get("revalidation_blocks", {}), "VLS block is not already closed")

    audit = load(STATE)["audit"]
    require(audit.get("finding_revalidation_completed_findings") == 176, "CURRENT_STATE terminal count is 176")
    require(audit.get("finding_revalidation_pending_findings") == 16, "CURRENT_STATE pending count is 16")
    require(audit.get("finding_revalidation_next_block") == "VLS", "CURRENT_STATE next block is VLS")
    require(audit.get("finding_revalidation_latest_completed_block") == "VDS", "VDS is prior CURRENT_STATE completed block")
    require(audit.get("latest_revalidation_evidence_id") == "EV-164", "EV-164 is prior revalidation evidence")

    sources = load(SOURCE_REGISTRY)
    pins = load(SOURCE_PINS)
    pin_map = {x["source_id"]: x for x in pins.get("sources", [])}
    pdf_paths = {"VLS_V1.0": args.vls_v10_pdf, "VLS_V2.0": args.vls_v20_pdf}
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
        "no `IBIS-IP_VideoLiveService_V1.0.xsd`",
        "VLS V2.0 XSD must NOT be substituted for V1.0",
        "VLS-003 - wrong part number in German foreword",
        "VLS-004 - VideoDisplayService in VideoLive start/stop prose",
        "targeted visual checks: complete for material findings",
    ], "VLS V1.0 deep read")
    require_tokens(DEEP_V20, [
        "d8c52f5de9ef3f5915524fef12da11eabf0ca041",
        "VLS-003 (V1.0 German foreword says 301-2-1): corrected in V2.0.",
        "VLS-004 persists visibly in V2.0.",
        "VLS-002 remains executable-confirmed.",
        "render run: 33203850390",
    ], "VLS V2.0 deep read")
    require_tokens(CORRECTION, [
        "VLS-005 - refined, not withdrawn",
        "pdf_choice_notation_application_anomaly_candidate",
        "VLS-002: remains executable-confirmed",
        "A prefixed minus sign denotes XML choice.",
    ], "choice-notation correction")
    require_tokens(EV103_DOC, [
        "VLS-002 remains executable-confirmed.",
        "GitHub Actions run: 33111119723",
        "job: 98653897734",
    ], "EV-103 evidence record")
    require_tokens(ADDENDUM, [
        "VLS-001 confirmed provenance gap",
        "VLS-002 executable-confirmed",
        "VLS-003 corrected in V2.0",
        "VLS-004 persists through V2.0",
        "VLS-005 refined: choice-notation application anomaly",
    ], "VLS finding register")

    projected = [dict(x) for x in entries]
    projected_by_id = {x["finding_id"]: x for x in projected}
    for fid, target in TARGETS.items():
        projected_by_id[fid]["revalidation_state"] = target
        projected_by_id[fid]["terminal_state_source"] = "docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_VLS_2026-09-14.md"
    require(counts(projected) == (181, 11), f"projected post-VLS counts are 181/11, got {counts(projected)}")
    require(first_pending(projected) == "VRS-001", f"projected first pending is VRS-001, got {first_pending(projected)}")

    evidence = {
        "evidence_id": "EV-165",
        "block": "VLS",
        "prestate": {"terminal": 176, "pending": 16, "first_pending": "VLS-001"},
        "projected_poststate": {"terminal": 181, "pending": 11, "first_pending": "VRS-001"},
        "findings": TARGETS,
        "authority_boundary": {
            "VLS_V1.0": "official public VDV PDF authority; exact official V1.0 VideoLiveService XSD unresolved; V2.0 is not substituted",
            "VLS_V2.0": "official VDV-301-2.0 service/Common/Enums family",
            "EV-103": "official V2.0 executable compositor evidence for VLS-002",
            "VLS-005": "choice-notation application anomaly only; leading minus itself is valid VDV XML-choice notation",
        },
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
    print(f"PASSED: EV-165 VLS aggregate evidence gate; wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
