#!/usr/bin/env python3
"""Validate the declarative Known-Issues runtime-mapping baseline.

The baseline is an implementation backlog, not an executable matcher set.
It must exactly reflect semantic entries whose runtime_match state is reviewed,
and it must keep all mappings unimplemented at this phase.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import subprocess
import tempfile

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = ROOT / "sdk_manifest/known_issues_runtime_mapping_v0.1.json"
DEFAULT_SCHEMA = ROOT / "sdk_manifest/known_issues_runtime_mapping_v0.1.schema.json"
DEFAULT_SEMANTIC = ROOT / "audit_registry/finding_semantic_classification_v0.1.json"
GENERATOR = ROOT / "tools/generate_known_issues_runtime_mapping_v0_1.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")
    print(f"OK  {message}")


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--semantic", type=Path, default=DEFAULT_SEMANTIC)
    args = parser.parse_args()

    manifest = load(args.manifest)
    schema = load(args.schema)
    semantic = load(args.semantic)

    errors = sorted(Draft202012Validator(schema).iter_errors(manifest), key=lambda e: list(e.path))
    if errors:
        for error in errors:
            where = ".".join(str(part) for part in error.path) or "<root>"
            print(f"SCHEMA ERROR {where}: {error.message}")
        raise SystemExit("FAIL: runtime mapping manifest does not satisfy schema")
    print("OK  runtime mapping manifest satisfies JSON Schema")

    require(semantic["state"] == "complete", "semantic classification source is complete")
    require(len(semantic["entries"]) == 192, "semantic classification source contains 192 findings")
    require(manifest["source_semantic_registry"]["git_blob"] == git_blob(args.semantic), "runtime mapping pins exact semantic registry blob")
    require(manifest["source_frozen_baseline"]["baseline_payload_sha256"] == semantic["source_baseline"]["baseline_payload_sha256"], "runtime mapping pins same frozen baseline payload")

    reviewed = [entry for entry in semantic["entries"] if entry["runtime_match"]["state"] == "reviewed"]
    reviewed_ids = [entry["finding_id"] for entry in reviewed]
    mapped_ids = [entry["finding_id"] for entry in manifest["mappings"]]
    require(len(reviewed_ids) == 30, "semantic registry has exactly 30 reviewed runtime mappings")
    require(mapped_ids == reviewed_ids, "runtime mapping manifest contains exactly the reviewed findings in semantic order")
    require(len(mapped_ids) == len(set(mapped_ids)), "runtime mapping finding IDs are unique")

    semantic_by_id = {entry["finding_id"]: entry for entry in semantic["entries"]}
    for mapping in manifest["mappings"]:
        source = semantic_by_id[mapping["finding_id"]]
        require(mapping["service"] == source["service"], f"{mapping['finding_id']} service matches semantic source")
        require(mapping["semantic_issue_kind"] == source["primary_issue_kind"], f"{mapping['finding_id']} issue kind matches semantic source")
        require(mapping["sdk_behavior"] == source["sdk_behavior"], f"{mapping['finding_id']} SDK behavior matches semantic source")
        require(mapping["profile_scope"] == source["version_scope"], f"{mapping['finding_id']} profile scope matches semantic source")
        require(mapping["trigger_descriptions"] == source["runtime_match"].get("candidate_triggers", []), f"{mapping['finding_id']} trigger descriptions match reviewed source")
        require(mapping["implementation_state"] == "reviewed_not_implemented", f"{mapping['finding_id']} is not prematurely implemented")
        require(mapping["authority_guard"] == "selected_xsd_result_remains_normative", f"{mapping['finding_id']} preserves XSD authority")

    counts = Counter(entry["runtime_match"]["state"] for entry in semantic["entries"])
    require(manifest["counts"]["reviewed_mapping_count"] == 30, "manifest reviewed mapping count is 30")
    require(manifest["counts"]["implemented_count"] == 0, "manifest implemented count is zero")
    require(manifest["counts"]["semantic_candidate_count"] == counts.get("candidate", 0) == 51, "manifest records 51 semantic candidates")
    require(manifest["counts"]["semantic_not_designed_count"] == counts.get("not_designed", 0) == 1, "manifest records one not-designed semantic mapping")
    require(manifest["counts"]["semantic_not_applicable_count"] == counts.get("not_applicable", 0) == 110, "manifest records 110 not-applicable findings")

    with tempfile.TemporaryDirectory() as td:
        regenerated = Path(td) / "runtime-mapping.json"
        subprocess.check_call([
            "python",
            str(GENERATOR),
            "--source",
            str(args.semantic),
            "--output",
            str(regenerated),
        ], cwd=ROOT)
        require(regenerated.read_bytes() == args.manifest.read_bytes(), "committed runtime mapping is byte-identical to deterministic regeneration")

    print("PASSED: Known-Issues runtime mapping baseline valid; 30 reviewed / 0 implemented")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
