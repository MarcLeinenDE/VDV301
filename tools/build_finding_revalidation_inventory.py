#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
AUDIT_DOCS = ROOT / 'docs' / 'pdf_xsd_semantic_audit'
AUDIT_REGISTRY = ROOT / 'audit_registry'
STATE_PATH = ROOT / '00_START_HERE' / 'CURRENT_STATE.json'
REVALIDATION_REGISTRY_PATH = AUDIT_REGISTRY / 'finding_revalidation_registry_v0.1.json'

ID_RE = re.compile(r'(?<![A-Z0-9-])([A-Z][A-Z0-9]{1,30}-\d{3})(?![A-Z0-9-])')
HEADING_RE = re.compile(r'(?m)^#{1,6}\s+([A-Z][A-Z0-9]{1,30}-\d{3})\b')
TABLE_RE = re.compile(r'(?m)^\|\s*([A-Z][A-Z0-9]{1,30}-\d{3})\s*\|')
BULLET_RE = re.compile(r'(?m)^\s*[-*]\s+(?:`|\*\*)?([A-Z][A-Z0-9]{1,30}-\d{3})\b')
EXCLUDED_PREFIXES = {'EV','RV','VDV','RFC','ISO','IEC','PR','HTTP','XML','XSD','SHA'}


def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8')


def load_json(path: Path) -> Any:
    return json.loads(read_text(path))


def dump_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


def is_finding_id(value: str) -> bool:
    if not ID_RE.fullmatch(value):
        return False
    return value.rsplit('-', 1)[0] not in EXCLUDED_PREFIXES


def ids_in_text(text: str) -> set[str]:
    return {token for token in ID_RE.findall(text) if is_finding_id(token)}


def iter_json_strings_and_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for k, v in value.items():
            yield str(k)
            yield from iter_json_strings_and_keys(v)
    elif isinstance(value, list):
        for item in value:
            yield from iter_json_strings_and_keys(item)
    elif isinstance(value, str):
        yield value


def canonical_source_paths() -> list[Path]:
    paths: set[Path] = set()
    exact = AUDIT_DOCS / 'findings.md'
    if exact.exists():
        paths.add(exact)
    paths.update(AUDIT_DOCS.glob('*_FINDINGS_REGISTER_ADDENDUM.md'))
    paths.update(AUDIT_DOCS.glob('AUDIT_CORRECTION_DELTA_*.md'))
    paths.update((AUDIT_DOCS / 'deep_read').glob('*.md'))
    base = AUDIT_REGISTRY / 'deep_read_findings_v0.1.json'
    if base.exists():
        paths.add(base)
    paths.update(AUDIT_REGISTRY.glob('deep_read_findings_delta_*.json'))
    paths.update(AUDIT_REGISTRY.glob('deep_read_findings_correction_*.json'))
    return sorted(paths)


def all_context_paths() -> list[Path]:
    paths: set[Path] = set()
    paths.update(AUDIT_DOCS.rglob('*.md'))
    paths.update(AUDIT_DOCS.rglob('*.csv'))
    paths.update(AUDIT_REGISTRY.glob('*.json'))
    return sorted(paths)


def discover_candidate_ids() -> tuple[set[str], dict[str, set[str]]]:
    candidates: set[str] = set()
    declarations: dict[str, set[str]] = defaultdict(set)
    for path in canonical_source_paths():
        rel = path.relative_to(ROOT).as_posix()
        text = read_text(path)
        if path.suffix == '.json':
            found: set[str] = set()
            for item in iter_json_strings_and_keys(json.loads(text)):
                found.update(ids_in_text(item))
        else:
            found = ids_in_text(text)
        for fid in found:
            candidates.add(fid)
            declarations[fid].add(rel)
    for path in AUDIT_DOCS.rglob('*.md'):
        rel = path.relative_to(ROOT).as_posix()
        text = read_text(path)
        structured = set(HEADING_RE.findall(text)) | set(TABLE_RE.findall(text)) | set(BULLET_RE.findall(text))
        for fid in structured:
            if is_finding_id(fid):
                candidates.add(fid)
                declarations[fid].add(rel)
    return candidates, declarations


def prior_revalidations(registry: dict[str, Any]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = defaultdict(list)
    explicit = registry.get('explicit_revalidations_during_deep_read_pass_2', {})
    if not isinstance(explicit, dict):
        return result
    for scope, records in explicit.items():
        if not isinstance(records, dict):
            continue
        for fid, record in records.items():
            if is_finding_id(fid):
                result[fid].append({'scope': scope, 'record': str(record)})
    return result


def infer_status_hints(fid: str, source_texts: dict[str, str]) -> list[str]:
    hints: set[str] = set()
    keywords = ('withdrawn','superseded','contextual_not_defect','executable_confirmed','context_verified','source_verified','unresolved')
    token = re.compile(rf'\b{re.escape(fid)}\b')
    for text in source_texts.values():
        for match in token.finditer(text):
            lo = max(0, match.start() - 500)
            hi = min(len(text), match.end() + 900)
            window = text[lo:hi].lower().replace('-', '_')
            for kw in keywords:
                if kw in window:
                    hints.add(kw)
    return sorted(hints)


def build_inventory(date: str, source_head: str | None) -> dict[str, Any]:
    revalidation_registry = load_json(REVALIDATION_REGISTRY_PATH)
    candidates, declarations = discover_candidate_ids()
    priors = prior_revalidations(revalidation_registry)
    context_texts = {p.relative_to(ROOT).as_posix(): read_text(p) for p in all_context_paths()}
    references: dict[str, list[str]] = defaultdict(list)
    for rel, text in context_texts.items():
        for fid in candidates.intersection(ids_in_text(text)):
            references[fid].append(rel)
    entries = []
    for fid in sorted(candidates):
        entries.append({
            'finding_id': fid,
            'declaration_sources': sorted(declarations.get(fid, set())),
            'reference_sources': sorted(set(references.get(fid, []))),
            'prior_current_gate_records': priors.get(fid, []),
            'status_hints_non_authoritative': infer_status_hints(fid, context_texts),
            'revalidation_state': 'pending',
            'terminal_state_source': None,
            'notes': 'Frozen inventory entry. Prior current-gate records are evidence inputs only; terminal state is assigned during explicit legacy revalidation reconciliation.'
        })
    return {
        'inventory_version': '0.1',
        'date': date,
        'state': 'frozen',
        'source_branch': 'dev/schema-integration',
        'source_head': source_head,
        'evidence_gate': 'docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md',
        'revalidation_plan': 'docs/pdf_xsd_semantic_audit/LEGACY_FINDING_REVALIDATION_PLAN.md',
        'discovery_policy': {
            'canonical_sources': [
                'docs/pdf_xsd_semantic_audit/findings.md',
                'docs/pdf_xsd_semantic_audit/*_FINDINGS_REGISTER_ADDENDUM.md',
                'docs/pdf_xsd_semantic_audit/deep_read/*.md',
                'docs/pdf_xsd_semantic_audit/AUDIT_CORRECTION_DELTA_*.md',
                'audit_registry/deep_read_findings_v0.1.json',
                'audit_registry/deep_read_findings_delta_*.json',
                'audit_registry/deep_read_findings_correction_*.json'
            ],
            'historical_first_pass_safety_net': 'structured finding IDs declared in headings/table rows/bullets across docs/pdf_xsd_semantic_audit/**/*.md',
            'context_reference_sources': ['docs/pdf_xsd_semantic_audit/**/*.md','docs/pdf_xsd_semantic_audit/**/*.csv','audit_registry/*.json'],
            'excluded_non_finding_prefixes': sorted(EXCLUDED_PREFIXES),
            'latest_wins': False,
            'xsd_mutation_allowed': False
        },
        'entry_count': len(entries),
        'finding_ids': [e['finding_id'] for e in entries],
        'entries': entries
    }


def update_revalidation_registry(inventory: dict[str, Any], snapshot_rel: str, source_head: str | None) -> None:
    registry = load_json(REVALIDATION_REGISTRY_PATH)
    registry['date'] = inventory['date']
    registry['state'] = 'inventory_frozen_revalidation_in_progress'
    registry['inventory'] = {
        'state': 'frozen',
        'frozen_on': inventory['date'],
        'source_branch': inventory['source_branch'],
        'source_head': source_head,
        'snapshot': snapshot_rel,
        'entry_count': inventory['entry_count'],
        'entries': [{'finding_id': e['finding_id'], 'revalidation_state': 'pending', 'terminal_state_source': None} for e in inventory['entries']]
    }
    registry['next_revalidation_block'] = 'ARA_V2.4'
    registry['sdk_readiness']['finding_knowledge_ready'] = False
    registry['remediation_readiness']['ready'] = False
    dump_json(REVALIDATION_REGISTRY_PATH, registry)


def update_current_state(inventory: dict[str, Any], snapshot_rel: str) -> None:
    state = load_json(STATE_PATH)
    audit = state.setdefault('audit', {})
    audit['legacy_finding_revalidation_state'] = 'inventory_frozen_revalidation_in_progress'
    audit['finding_inventory_snapshot'] = snapshot_rel
    audit['finding_inventory_count'] = inventory['entry_count']
    audit['finding_inventory_source_head'] = inventory['source_head']
    audit['finding_revalidation_next_block'] = 'ARA_V2.4'
    audit['finding_revalidation_completed_findings'] = 0
    audit['finding_revalidation_pending_findings'] = inventory['entry_count']
    dump_json(STATE_PATH, state)


def build_freeze_note(inventory: dict[str, Any], snapshot_rel: str) -> str:
    return f'''# Finding inventory freeze — {inventory["date"]}\n\nStatus: frozen input set for mandatory legacy finding revalidation.\n\n- Branch: `dev/schema-integration`\n- Source head: `{inventory["source_head"]}`\n- Frozen findings: **{inventory["entry_count"]}**\n- Machine-readable snapshot: `{snapshot_rel}`\n- Evidence Gate: `docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md`\n- Revalidation plan: `docs/pdf_xsd_semantic_audit/LEGACY_FINDING_REVALIDATION_PLAN.md`\n- Next block: `ARA_V2.4`\n\nThe snapshot is conservative: every entry begins `pending`. Existing Deep Read / EV / RV records are retained as prior evidence inputs but do not silently become terminal states. Each terminal state must be written during explicit revalidation reconciliation.\n\nNo XSD file is modified by this freeze.\n'''


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', default='2026-09-03')
    parser.add_argument('--source-head', default=os.environ.get('GITHUB_SHA'))
    parser.add_argument('--snapshot', default='audit_registry/finding_inventory_frozen_2026-09-03.json')
    parser.add_argument('--note', default='docs/pdf_xsd_semantic_audit/FINDING_INVENTORY_FREEZE_2026-09-03.md')
    args = parser.parse_args()
    inventory = build_inventory(args.date, args.source_head)
    dump_json(ROOT / args.snapshot, inventory)
    update_revalidation_registry(inventory, args.snapshot, args.source_head)
    update_current_state(inventory, args.snapshot)
    (ROOT / args.note).write_text(build_freeze_note(inventory, args.snapshot), encoding='utf-8')
    print(f'FROZEN_FINDING_COUNT={inventory["entry_count"]}')
    print(f'SNAPSHOT={args.snapshot}')
    print('NEXT_BLOCK=ARA_V2.4')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
