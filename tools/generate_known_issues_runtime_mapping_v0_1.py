#!/usr/bin/env python3
"""Generate the reviewed Known-Issues runtime-mapping inventory from the complete semantic registry.

This generator intentionally does NOT create executable matchers. It only promotes
entries whose semantic runtime_match state is already "reviewed" into a structured
implementation backlog. Free-text trigger descriptions remain non-executable until
a later profile-specific implementation/evidence phase.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "audit_registry/finding_semantic_classification_v0.1.json"
DEFAULT_OUTPUT = ROOT / "sdk_manifest/known_issues_runtime_mapping_v0.1.json"

BEHAVIOR_MAP = {
    "unsupported_profile": ("profile_resolution_failure", "strict_profile_resolution_failed", "emit_unsupported_profile"),
    "error_with_advisory": ("xsd_invalid_advisory", "xsd_result_invalid", "decorate_existing_invalid"),
    "valid_with_advisory": ("xsd_valid_advisory", "xsd_result_valid", "decorate_existing_valid"),
    "warning": ("resolver_or_profile_warning", "resolver_context_matched", "emit_warning"),
    "no_runtime_diagnostic": ("routing_only", "routing_context_matched", "routing_only_no_public_diagnostic"),
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", str(path)], cwd=ROOT, text=True).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    registry = load(args.source)
    if registry.get("state") != "complete":
        raise SystemExit("FAIL: semantic classification registry must be complete before runtime-mapping generation")
    entries = registry.get("entries", [])
    if len(entries) != 192:
        raise SystemExit(f"FAIL: expected 192 semantic findings, got {len(entries)}")
    if any(entry.get("runtime_match", {}).get("state") == "implemented" for entry in entries):
        raise SystemExit("FAIL: semantic classification must not pre-mark runtime mappings implemented")

    runtime_counts = Counter(entry["runtime_match"]["state"] for entry in entries)
    reviewed = [entry for entry in entries if entry["runtime_match"]["state"] == "reviewed"]

    mappings = []
    for entry in reviewed:
        behavior = entry["sdk_behavior"]
        if behavior not in BEHAVIOR_MAP:
            raise SystemExit(f"FAIL: reviewed finding {entry['finding_id']} has unsupported sdk_behavior {behavior}")
        activation_class, required_precondition, result_effect = BEHAVIOR_MAP[behavior]
        triggers = entry["runtime_match"].get("candidate_triggers", [])
        if not triggers:
            raise SystemExit(f"FAIL: reviewed finding {entry['finding_id']} has no trigger descriptions")
        mappings.append({
            "finding_id": entry["finding_id"],
            "service": entry["service"],
            "semantic_issue_kind": entry["primary_issue_kind"],
            "sdk_behavior": behavior,
            "activation_class": activation_class,
            "required_precondition": required_precondition,
            "result_effect": result_effect,
            "implementation_state": "reviewed_not_implemented",
            "authority_guard": "selected_xsd_result_remains_normative",
            "profile_scope": entry["version_scope"],
            "trigger_descriptions": triggers,
            "diagnostic_source": {
                "registry": "audit_registry/finding_semantic_classification_v0.1.json",
                "finding_id": entry["finding_id"],
            },
        })

    result = {
        "manifest_version": "0.1",
        "kind": "known-issues-runtime-mapping",
        "state": "reviewed_inventory",
        "source_semantic_registry": {
            "path": "audit_registry/finding_semantic_classification_v0.1.json",
            "git_blob": git_blob(args.source),
            "classification_state": "complete",
            "finding_count": 192,
        },
        "source_frozen_baseline": {
            "path": "audit_registry/finding_provenance_baseline_2026-09-14.json",
            "baseline_payload_sha256": registry["source_baseline"]["baseline_payload_sha256"],
        },
        "policy": {
            "normative_xsd_result_must_not_be_overridden": True,
            "generated_only_from_runtime_match_reviewed": True,
            "trigger_descriptions_are_not_executable_matchers": True,
            "implementation_requires_separate_profile_specific_validation": True,
        },
        "counts": {
            "reviewed_mapping_count": len(mappings),
            "implemented_count": 0,
            "semantic_candidate_count": runtime_counts.get("candidate", 0),
            "semantic_not_designed_count": runtime_counts.get("not_designed", 0),
            "semantic_not_applicable_count": runtime_counts.get("not_applicable", 0),
        },
        "mappings": mappings,
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"PASSED: generated {len(mappings)} reviewed runtime mappings; implemented=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
