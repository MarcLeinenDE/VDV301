#!/usr/bin/env python3
"""Validate the post-freeze VDV 301 finding semantic classification layer.

This validator is intentionally read-only. It verifies that the semantic
Known-Issues layer remains anchored to the frozen finding/provenance baseline
and that every reviewed entry carries bilingual user-facing diagnostics.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "audit_registry/finding_semantic_classification_v0.1.json"
DEFAULT_SCHEMA = ROOT / "audit_registry/finding_semantic_classification_schema_v0.1.json"
DEFAULT_BASELINE = ROOT / "audit_registry/finding_provenance_baseline_2026-09-14.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")
    print(f"OK  {message}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    args = parser.parse_args()

    registry = load_json(args.registry)
    schema = load_json(args.schema)
    baseline = load_json(args.baseline)

    errors = sorted(Draft202012Validator(schema).iter_errors(registry), key=lambda e: list(e.path))
    if errors:
        for error in errors:
            where = ".".join(str(part) for part in error.path) or "<root>"
            print(f"SCHEMA ERROR {where}: {error.message}")
        raise SystemExit("FAIL: classification registry does not satisfy schema")
    print("OK  classification registry satisfies JSON Schema")

    src = registry["source_baseline"]
    require(src["path"] == "audit_registry/finding_provenance_baseline_2026-09-14.json", "classification points to canonical frozen baseline")
    require(src["baseline_payload_sha256"] == baseline["baseline_payload_sha256"], "classification pins exact frozen baseline payload digest")
    require(src["finding_entries_sha256"] == baseline["inventory"]["finding_entries_sha256"], "classification pins exact 192-finding entries digest")
    require(src["finding_count"] == baseline["inventory"]["count"] == 192, "classification and frozen baseline both contain 192 source findings")
    require(baseline["state"] == "frozen", "source finding/provenance baseline is frozen")
    require(baseline["readiness"]["finding_knowledge_ready"] is True, "source baseline is finding-knowledge ready")

    policy = registry["policy"]
    require(policy["normative_xsd_result_must_not_be_overridden"] is True, "Known-Issues layer cannot override normative XSD result")
    require(policy["manual_review_required"] is True, "manual semantic review is mandatory")
    require(policy["bilingual_user_text_required"] is True, "bilingual user-facing diagnostics are mandatory")
    require(set(policy["user_languages"]) >= {"de", "en"}, "German and English are mandatory user languages")

    frozen_entries = baseline["inventory"]["entries"]
    frozen_by_id = {entry["finding_id"]: entry for entry in frozen_entries}
    frozen_order = {entry["finding_id"]: idx for idx, entry in enumerate(frozen_entries)}
    require(len(frozen_by_id) == 192, "frozen baseline has 192 unique finding IDs")

    entries = registry["entries"]
    ids = [entry["finding_id"] for entry in entries]
    require(len(ids) == len(set(ids)), "classification entries use unique finding IDs")
    require(all(fid in frozen_by_id for fid in ids), "every classified finding exists in the frozen baseline")
    require(ids == sorted(ids, key=lambda fid: frozen_order[fid]), "classification entries follow frozen 192-finding order")

    allowed_terminal = {
        "context_verified",
        "executable_confirmed",
        "contextual_not_defect",
        "withdrawn",
        "superseded",
        "unresolved",
    }
    require(all(frozen_by_id[fid]["revalidation_state"] in allowed_terminal for fid in ids), "every classified finding comes from a terminal frozen finding")

    for entry in entries:
        fid = entry["finding_id"]
        diagnostic = entry["diagnostic"]
        for lang in ("de", "en"):
            text = diagnostic[lang]
            require(all(text[key].strip() for key in ("title", "short", "long", "recommendation")), f"{fid} has complete {lang} user-facing diagnostic text")
        require(entry["semantic_basis"], f"{fid} has an explicit semantic basis")
        require(entry["source_references"], f"{fid} has source references")
        require(entry["version_scope"], f"{fid} has explicit version/authority scope")
        require(entry["runtime_match"]["state"] != "implemented", f"{fid} runtime mapping is not falsely marked implemented during classification")

    pilot_expected = {"TVS-001", "TVS-002", "TVS-003", "TSM-002", "TSM-003", "TSD-004"}
    if registry["state"] == "pilot":
        require(set(ids) == pilot_expected, "pilot contains exactly the six manually selected representative findings")
        require("progress" not in registry, "pilot has no false block-review progress")
    else:
        progress = registry.get("progress")
        require(isinstance(progress, dict), "in-progress/complete classification has progress metadata")
        require(progress["classified_count"] == len(entries), "progress classified_count matches actual entries")
        require(progress["remaining_count"] == 192 - len(entries), "progress remaining_count matches frozen inventory")
        require(len(progress["reviewed_blocks"]) == len(set(progress["reviewed_blocks"])), "reviewed block list is unique")
        require(progress["latest_block"] in progress["reviewed_blocks"], "latest block is recorded as reviewed")
        require(bool(progress["latest_block_file"]), "latest block source file is recorded")

    if registry["state"] == "complete":
        require(len(entries) == 192, "complete classification contains all 192 findings")
        require(registry["progress"]["remaining_count"] == 0, "complete classification has zero remaining findings")

    print(f"PASSED: semantic classification registry valid; {len(entries)} reviewed entries anchored to frozen baseline")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
