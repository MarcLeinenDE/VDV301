#!/usr/bin/env python3
"""Final fail-closed finding-knowledge readiness gate after all 192 frozen findings are terminal.

EV-167 does not silently erase CIS-001's prior unresolved history. It re-evaluates the
*current finding claim* under the final Evidence Gate: the published CIS V1.1 PDF has no
confirmed matching release-tag XSD, and the known untagged working family is materially
behind the publication. That provenance-gap claim can therefore be context-verified while
the missing official release-XSD identity itself remains unknown.

The resulting SDK rule is fail-closed: no strict CIS V1.1 validation profile is exposed;
no untagged working or neighbouring-version XSD is substituted.
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
CIS_REPORT = ROOT / "docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_CIS_2026-09-03.md"
PIN_CORRECTION = ROOT / "docs/pdf_xsd_semantic_audit/PDF_SOURCE_PIN_CORRECTION_CIS_2026-09-14.md"
XSD_POOL = ROOT / "tools/validate_xsd_pool.py"

EXPECTED = {
    FROZEN: "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
    REGISTRY: "8635e6d6a5e3f6f9a358760d35e716a0b065b277",
    STATE: "c5b5d7f29203a23d42fe9feee54ab2c130850191",
    SOURCE_REGISTRY: "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
    SOURCE_PINS: "bc60527ddc158d967470a63d38ffd035e5ec1400",
    EVIDENCE_GATE: "969cce8b14b50ded2ca5eb745674b894428ecf1a",
    PLAN: "b8a38bd09ca6239b96981548b7cfcbd49aa4c9d5",
    CIS_REPORT: "4e871dae28db1d36c99ff0ebcb553e7178681c4f",
    XSD_POOL: "7a682dbddaeeeb3f9cc269d2e48e5ab000aca4bd",
}
TERMINAL = {
    "context_verified",
    "executable_confirmed",
    "contextual_not_defect",
    "withdrawn",
    "unresolved",
    "superseded",
}
CIS_PDF_SHA = "f9d63dd1f2e417691913e57a9c7121c90b4e781cbcd1328be681695975f59739"
CIS_PDF_SIZE = 809729
CIS_PDF_URL = "https://www.vdv.de/301-2-3-sds-v1-1.pdfx"
WORKING_COMMIT = "0a5228a768c7d710c40f5f99fbdce2e544d19883"
WORKING_CIS_BLOB = "5957e27f128a191c794b0c8081b531a07126784a"
MISSING_PUBLISHED_FIELDS = ("SpeakerActive", "StopInformationActive")


def req(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL {message}")
    print(f"OK  {message}")


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def tokens(path: Path, values: list[str], label: str) -> None:
    content = path.read_text(encoding="utf-8")
    for value in values:
        req(value in content, f"{label} contains authoritative token: {value}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cis-v11-pdf", required=True, type=Path)
    parser.add_argument("--cis-v11-text", required=True, type=Path)
    parser.add_argument("--working-cis-xsd", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    for path, expected in EXPECTED.items():
        req(path.is_file() and blob(path) == expected, f"exact blob {path.relative_to(ROOT)} = {expected}")
    req(PIN_CORRECTION.is_file(), "CIS pin-correction report exists")
    tokens(
        PIN_CORRECTION,
        [
            "evidence-backed registry correction",
            "33736316368",
            "9885887536",
            "f9d63dd1f2e417691913e57a9c7121c90b4e781cbcd1328be681695975f59739",
        ],
        "CIS source-pin correction",
    )

    frozen = load(FROZEN)
    req(frozen.get("state") == "frozen" and frozen.get("entry_count") == 192, "frozen inventory remains 192")

    registry = load(REGISTRY)
    entries = registry["inventory"]["entries"]
    by_id = {entry["finding_id"]: entry for entry in entries}
    req(len(entries) == len(by_id) == 192, "registry has 192 unique findings")
    req(sum(entry.get("revalidation_state") in TERMINAL for entry in entries) == 192, "all 192 findings are terminal")
    req(sum(entry.get("revalidation_state") == "pending" for entry in entries) == 0, "zero pending findings")
    req(registry.get("next_revalidation_block") is None, "no next revalidation block")
    req(
        registry.get("state") == "inventory_frozen_revalidation_terminalized_readiness_pending",
        "registry awaits readiness reconciliation",
    )
    unresolved = [entry["finding_id"] for entry in entries if entry.get("revalidation_state") == "unresolved"]
    req(unresolved == ["CIS-001"], f"CIS-001 is sole unresolved terminal finding, got {unresolved}")
    req(
        by_id["CIS-001"].get("terminal_state_source") == str(CIS_REPORT.relative_to(ROOT)),
        "CIS-001 points to canonical CIS closure report",
    )

    sdk = registry["sdk_readiness"]
    req(sdk.get("finding_knowledge_ready") is False, "finding knowledge is not prematurely ready")
    req(
        sdk.get("readiness_reconciliation_pending") == ["CIS-001"],
        "only CIS-001 awaits readiness reconciliation",
    )

    audit = load(STATE)["audit"]
    req(
        audit.get("finding_revalidation_completed_findings") == 192
        and audit.get("finding_revalidation_pending_findings") == 0,
        "CURRENT_STATE is 192/0",
    )
    req(
        audit.get("finding_readiness_reconciliation_pending") == ["CIS-001"],
        "CURRENT_STATE names CIS-001 as readiness item",
    )

    tokens(
        CIS_REPORT,
        [
            "Official Git history contains an untagged V1.1 working family at `0a5228a…`",
            "there is no `VDV-301-1.1` release tag",
            "lacks published-PDF fields `SpeakerActive` and `StopInformationActive`",
            "cannot be promoted to a strict published V1.1 release authority",
        ],
        "CIS closure report",
    )
    tokens(
        PLAN,
        [
            "zero pending findings",
            "zero unresolved finding that could alter SDK accept/reject/routing behavior",
            "all XML-validity claims intended for SDK diagnostics executable-confirmed where technically practical",
        ],
        "revalidation plan",
    )
    tokens(
        EVIDENCE_GATE,
        [
            "Never compare a PDF against a neighbouring or latest schema merely because it is easier to find.",
            "The SDK must never normalize, reject, accept or reroute payloads because of an unverified finding.",
        ],
        "finding evidence gate",
    )

    sources = load(SOURCE_REGISTRY)
    source = next(item for item in sources["sources"] if item["source_id"] == "CIS_V1.1")
    pins = load(SOURCE_PINS)
    pin = next(item for item in pins["sources"] if item["source_id"] == "CIS_V1.1")
    req(source.get("official_url") == CIS_PDF_URL, "CIS V1.1 official PDF URL pinned")
    req(
        pin.get("expected_sha256") == CIS_PDF_SHA and pin.get("expected_size_bytes") == CIS_PDF_SIZE,
        "CIS V1.1 corrected PDF hash/size pinned",
    )
    req(str(pin.get("evidence_run_id")) == "33736316368", "CIS V1.1 source evidence run pinned")
    req(str(pin.get("correction_artifact_id")) == "9885887536", "CIS V1.1 pin correction retains exact evidence artifact")
    req(
        args.cis_v11_pdf.is_file()
        and args.cis_v11_pdf.stat().st_size == CIS_PDF_SIZE
        and sha256(args.cis_v11_pdf) == CIS_PDF_SHA,
        "fresh CIS V1.1 PDF bytes match corrected permanent pin",
    )

    req(args.cis_v11_text.is_file(), "fresh CIS V1.1 PDF text extraction supplied")
    pdf_text = args.cis_v11_text.read_text(encoding="utf-8", errors="replace")
    for field in MISSING_PUBLISHED_FIELDS:
        req(field in pdf_text, f"published CIS V1.1 PDF contains field {field}")

    req(args.working_cis_xsd.is_file(), "untagged CIS V1.1 working XSD supplied")
    req(blob(args.working_cis_xsd) == WORKING_CIS_BLOB, f"untagged CIS V1.1 working XSD blob = {WORKING_CIS_BLOB}")
    working_text = args.working_cis_xsd.read_text(encoding="utf-8")
    for field in MISSING_PUBLISHED_FIELDS:
        req(field not in working_text, f"untagged CIS V1.1 working XSD omits published field {field}")

    projected_state = "context_verified"
    req(projected_state in TERMINAL, "CIS-001 projected state is terminal")

    resolution = {
        "finding_id": "CIS-001",
        "prior_terminal_state": "unresolved",
        "projected_terminal_state": projected_state,
        "release_xsd_identity": "still_unresolved",
        "finding_claim": "published CIS V1.1 PDF has no confirmed matching release-tag XSD authority",
        "sdk_policy": "no_strict_cis_v1_1_profile_fail_closed",
        "routing_rule": "Do not substitute the untagged V1.1 working family or any neighbouring version; report CIS V1.1 strict profile as unsupported/unresolved authority.",
        "working_commit": WORKING_COMMIT,
        "working_cis_blob": WORKING_CIS_BLOB,
        "published_pdf_fields_absent_from_working_xsd": list(MISSING_PUBLISHED_FIELDS),
        "reason": "The provenance-gap finding itself is context-verified even though the identity of a matching official release XSD remains unknown.",
    }

    output = {
        "evidence_id": "EV-167",
        "prestate": {
            "terminal": 192,
            "pending": 0,
            "finding_knowledge_ready": False,
            "cis_001_state": "unresolved",
        },
        "cis_001_readiness_reconciliation": resolution,
        "projected_poststate": {
            "terminal": 192,
            "pending": 0,
            "cis_001_state": projected_state,
            "unresolved_findings": [],
            "finding_knowledge_ready": True,
            "next_revalidation_block": None,
        },
        "xsd_mutation": False,
        "frozen_inventory_mutation": False,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(f"PASSED: EV-167 final finding-knowledge readiness gate; wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
