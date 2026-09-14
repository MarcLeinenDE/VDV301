#!/usr/bin/env python3
"""Merge one manually reviewed semantic-classification block into the Known-Issues registry.

The merger is deliberately conservative:
- the block must pin the exact frozen baseline payload digest;
- every block finding must exist in the frozen 192-finding baseline;
- existing classification entries may not be replaced or silently reclassified;
- output is deterministically ordered by the frozen inventory order;
- the registry moves from pilot to in_progress once a real review block is merged.

This tool does not validate XSDs and does not alter the frozen audit baseline.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "audit_registry/finding_semantic_classification_v0.1.json"
DEFAULT_BASELINE = ROOT / "audit_registry/finding_provenance_baseline_2026-09-14.json"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--block", required=True, type=Path)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    registry = load(args.registry)
    baseline = load(args.baseline)
    block = load(args.block)

    baseline_digest = baseline.get("baseline_payload_sha256")
    if not baseline_digest:
        fail("frozen baseline has no baseline_payload_sha256")
    if block.get("source_baseline_payload_sha256") != baseline_digest:
        fail("classification block does not pin the exact frozen baseline payload digest")
    if registry.get("source_baseline", {}).get("baseline_payload_sha256") != baseline_digest:
        fail("classification registry does not pin the exact frozen baseline payload digest")

    frozen_entries = baseline.get("inventory", {}).get("entries", [])
    frozen_ids = [entry.get("finding_id") for entry in frozen_entries]
    if len(frozen_ids) != 192 or len(set(frozen_ids)) != 192:
        fail("frozen baseline is not the expected 192 unique findings")
    frozen_index = {fid: idx for idx, fid in enumerate(frozen_ids)}

    block_entries = block.get("entries")
    if not isinstance(block_entries, list) or not block_entries:
        fail("classification block has no entries")
    block_ids = [entry.get("finding_id") for entry in block_entries]
    if any(not fid for fid in block_ids):
        fail("classification block contains an entry without finding_id")
    if len(block_ids) != len(set(block_ids)):
        fail("classification block contains duplicate finding IDs")
    unknown = [fid for fid in block_ids if fid not in frozen_index]
    if unknown:
        fail(f"classification block contains findings outside frozen baseline: {unknown}")

    existing_entries = registry.get("entries", [])
    existing_ids = {entry.get("finding_id") for entry in existing_entries}
    duplicates = sorted(existing_ids.intersection(block_ids))
    if duplicates:
        fail(f"refusing to replace already classified findings: {duplicates}")

    merged_entries = existing_entries + block_entries
    merged_entries.sort(key=lambda entry: frozen_index[entry["finding_id"]])

    registry["entries"] = merged_entries
    if registry.get("state") == "pilot":
        registry["state"] = "in_progress"

    progress = registry.setdefault("progress", {})
    progress["classified_count"] = len(merged_entries)
    progress["remaining_count"] = 192 - len(merged_entries)
    reviewed_blocks = progress.setdefault("reviewed_blocks", [])
    block_id = block.get("block_id")
    if block_id and block_id not in reviewed_blocks:
        reviewed_blocks.append(block_id)
    progress["latest_block"] = block_id
    progress["latest_block_file"] = str(args.block).replace(str(ROOT) + "/", "")

    output = args.output or args.registry
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"PASSED: merged block {block_id}; classified={len(merged_entries)} remaining={192-len(merged_entries)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
