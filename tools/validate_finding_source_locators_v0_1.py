#!/usr/bin/env python3
"""Validate the canonical VDV301 finding source-locator manifest."""
from __future__ import annotations

import json
import re
import subprocess
import urllib.parse
import urllib.request
from pathlib import Path

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "audit_registry/finding_source_locators_v0.1.json"
SCHEMA = ROOT / "audit_registry/finding_source_locators_v0.1.schema.json"
SEMANTIC = ROOT / "audit_registry/finding_semantic_classification_v0.1.json"
RUNTIME = ROOT / "sdk_manifest/known_issues_runtime_mapping_v0.1.json"
PDF_REGISTRY = ROOT / "audit_registry/pdf_source_registry_v0.1.json"
PDF_PINS = ROOT / "audit_registry/pdf_source_pins_v0.1.json"

UPSTREAM_REPOSITORY = "VDVde/VDV301"
_UPSTREAM_CACHE: dict[tuple[str, str, str], str] = {}


def load(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def git_blob(p: Path) -> str:
    return subprocess.check_output(
        ["git", "hash-object", str(p)], cwd=ROOT, text=True
    ).strip()


def require(cond: bool, msg: str):
    if not cond:
        raise SystemExit("FAIL: " + msg)
    print("OK  " + msg)


def upstream_blob(repository: str, ref: str, file: str) -> str:
    key = (repository, ref, file)
    if key in _UPSTREAM_CACHE:
        return _UPSTREAM_CACHE[key]
    api = (
        f"https://api.github.com/repos/{repository}/contents/"
        f"{urllib.parse.quote(file, safe='/')}?ref="
        f"{urllib.parse.quote(ref, safe='')}"
    )
    req = urllib.request.Request(
        api,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "VDV301-locator-validator",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.load(resp)
    sha = str(data.get("sha", ""))
    _UPSTREAM_CACHE[key] = sha
    return sha


def infer_official_tag(version: str) -> str | None:
    """Resolve the release context from a version-lane label.

    Common V2.3 consuming Enumerations V2.2 is intentionally checked at the
    VDV-301-2.3 release tag: the dependency blob must be the one actually
    published in that release context, not merely a matching file from another
    tag.
    """
    m = re.search(r"(?<!\d)(\d+\.\d+)(?!\d)", version)
    if not m:
        return None
    return f"VDV-301-{m.group(1)}"


def scope_mentions_version(scopes: list[dict], version: str) -> bool:
    m = re.search(r"(?<!\d)(\d+\.\d+)(?!\d)", version)
    if not m:
        return any(str(x.get("version", "")) == version for x in scopes)
    token = re.escape(m.group(1))
    return any(
        re.search(rf"(?<!\d){token}(?!\d)", str(x.get("version", "")))
        for x in scopes
    )


def main() -> int:
    m = load(MANIFEST)
    s = load(SCHEMA)
    sem = load(SEMANTIC)
    runtime = load(RUNTIME)
    pdf_registry = load(PDF_REGISTRY)
    pdf_pins = load(PDF_PINS)

    pdf_by_id = {x["source_id"]: x for x in pdf_registry["sources"]}
    pin_by_id = {x["source_id"]: x for x in pdf_pins["sources"]}

    errors = sorted(
        Draft202012Validator(s).iter_errors(m), key=lambda e: list(e.path)
    )
    if errors:
        raise SystemExit(
            "\n".join(f"{list(e.path)}: {e.message}" for e in errors)
        )

    require(
        m["source_semantic_registry"]["git_blob"] == git_blob(SEMANTIC),
        "locator manifest pins current semantic-registry blob",
    )
    require(len(sem["entries"]) == 192, "semantic registry has 192 findings")

    by = {e["finding_id"]: e for e in sem["entries"]}
    order = {e["finding_id"]: i for i, e in enumerate(sem["entries"])}
    runtime_by = {
        e["finding_id"]: e for e in runtime.get("mappings", [])
    }
    ids = [e["finding_id"] for e in m["entries"]]

    require(len(ids) == len(set(ids)), "locator entries use unique finding IDs")
    require(
        all(i in by for i in ids), "all locator entries refer to semantic findings"
    )
    require(
        ids == sorted(ids, key=lambda i: order[i]),
        "locator entries follow semantic finding order",
    )

    for e in m["entries"]:
        fid = e["finding_id"]
        src = by[fid]
        runtime_entry = runtime_by.get(fid)

        require(
            e["service"] == src["service"],
            f"{fid} service matches semantic registry",
        )
        require(
            e["scope_claims"] == src["version_scope"],
            f"{fid} scope_claims exactly match semantic version_scope",
        )

        # Runtime Known-Issue scope is an affected-profile scope. Keep it
        # exactly synchronized with the semantic affected scope so a later
        # matcher cannot silently widen or narrow a finding.
        if runtime_entry is not None:
            require(
                runtime_entry["profile_scope"] == src["version_scope"],
                f"{fid} runtime profile_scope exactly matches semantic affected scope",
            )
            require(
                runtime_entry["authority_guard"]
                == "selected_xsd_result_remains_normative",
                f"{fid} runtime mapping preserves selected-XSD authority",
            )

        diagnostic = src.get("diagnostic", {})
        for lang in ("de", "en"):
            require(lang in diagnostic, f"{fid} has {lang.upper()} diagnostic block")
            for field in ("title", "short", "long", "recommendation"):
                require(
                    bool(str(diagnostic[lang].get(field, "")).strip()),
                    f"{fid} has non-empty {lang}.{field}",
                )

        versions = [c["version"] for c in e["coverage"]]
        require(
            len(versions) == len(set(versions)),
            f"{fid} coverage versions are unique",
        )
        if e["coverage_state"] == "complete":
            require(
                all(c["coverage_status"] == "complete" for c in e["coverage"]),
                f"{fid} complete entry has no partial coverage lane",
            )

        for c in e["coverage"]:
            require(
                c["pdf_locators"] or c["xsd_locators"],
                f"{fid} {c['version']} has at least one direct locator",
            )

            # A later fixed version may be retained to prove where a finding
            # ends. It is evidence only and must never become an affected
            # semantic/runtime trigger lane.
            if c.get("scope_role") == "correction_boundary_not_affected":
                require(
                    not scope_mentions_version(src["version_scope"], c["version"]),
                    f"{fid} {c['version']} correction boundary excluded from semantic affected scope",
                )
                if runtime_entry is not None:
                    require(
                        not scope_mentions_version(
                            runtime_entry["profile_scope"], c["version"]
                        ),
                        f"{fid} {c['version']} correction boundary excluded from runtime affected scope",
                    )

            for p_loc in c["pdf_locators"]:
                sid = p_loc["source_id"]
                require(
                    sid in pdf_by_id, f"{fid} PDF source is registered: {sid}"
                )
                require(
                    sid in pin_by_id, f"{fid} PDF source is byte-pinned: {sid}"
                )
                require(
                    pdf_by_id[sid]["official_url"] == p_loc["url"],
                    f"{fid} PDF official URL matches registry: {sid}",
                )
                require(
                    str(pdf_by_id[sid]["version"]) == p_loc["document_version"],
                    f"{fid} PDF version matches registry: {sid}",
                )
                require(
                    pin_by_id[sid]["expected_sha256"] == p_loc["sha256"],
                    f"{fid} PDF SHA-256 matches pin registry: {sid}",
                )

            for x in c["xsd_locators"]:
                if x.get("repository") or x.get("ref"):
                    require(
                        bool(x.get("repository")) and bool(x.get("ref")),
                        f"{fid} external XSD locator has repository and ref: {x['file']}",
                    )
                    require(
                        x["repository"] == UPSTREAM_REPOSITORY,
                        f"{fid} external XSD repository is approved upstream: {x['file']}",
                    )
                    require(
                        upstream_blob(
                            x["repository"], x["ref"], x["file"]
                        )
                        == x["git_blob"],
                        f"{fid} external XSD blob matches {x['repository']}@{x['ref']}: {x['file']}",
                    )
                else:
                    p = ROOT / x["file"]
                    require(p.is_file(), f"{fid} XSD exists: {x['file']}")
                    require(
                        git_blob(p) == x["git_blob"],
                        f"{fid} XSD blob matches: {x['file']}",
                    )

                    # Local copies marked official_release are not trusted
                    # solely because the local blob matches. Cross-check the
                    # exact file against the official release-tag context.
                    if c["authority"] == "official_release":
                        tag = infer_official_tag(c["version"])
                        if tag:
                            require(
                                upstream_blob(
                                    UPSTREAM_REPOSITORY, tag, x["file"]
                                )
                                == x["git_blob"],
                                f"{fid} official XSD blob matches upstream {UPSTREAM_REPOSITORY}@{tag}: {x['file']}",
                            )

    # Regression guards for issues found by the 2026-09-30 full revalidation.
    loc_by = {e["finding_id"]: e for e in m["entries"]}

    ce002 = loc_by.get("CE-002")
    if ce002:
        p = ce002["coverage"][0]["pdf_locators"][0]
        require(
            p["printed_pages"] == [34, 55],
            "CE-002 pins actual PointNumber table page 34 and V2.4 history page 55",
        )
        require(
            "2.50 StopInformation" in p["section"]
            and "4.6 Version 2.4" in p["section"],
            "CE-002 pins StopInformation 2.50 and Version 2.4 history",
        )
        require(
            "Table 50" in p.get("table", ""),
            "CE-002 pins Table 50 StopInformation",
        )

    ce004 = loc_by.get("CE-004")
    if ce004:
        require(
            [c["version"] for c in ce004["coverage"]]
            == ["2.2", "2.3", "2.4"],
            "CE-004 covers V2.2, V2.3 and V2.4 in sequence",
        )
        expected = {
            "2.2": ([40, 49], "Table 86"),
            "2.3": ([41, 50], "Table 86"),
            "2.4": ([44, 53], "Table 85"),
        }
        for c in ce004["coverage"]:
            p = c["pdf_locators"][0]
            pages, table = expected[c["version"]]
            require(
                p["printed_pages"] == pages,
                f"CE-004 {c['version']} pins verified table/history pages",
            )
            require(
                "3.21 ServiceNameEnumeration" in p["section"],
                f"CE-004 {c['version']} pins section 3.21 ServiceNameEnumeration",
            )
            require(
                table in p.get("table", ""),
                f"CE-004 {c['version']} pins verified ServiceName table number",
            )

    for fid in ("CE-025", "CE-026"):
        e = loc_by.get(fid)
        if e:
            boundaries = [
                c
                for c in e["coverage"]
                if c.get("scope_role") == "correction_boundary_not_affected"
            ]
            require(
                len(boundaries) == 1 and boundaries[0]["version"] == "2.4",
                f"{fid} retains exactly one V2.4 non-affected correction boundary",
            )

    counts = m["counts"]
    require(
        counts["locator_entry_count"] == len(m["entries"]),
        "locator_entry_count matches entries",
    )
    require(
        counts["coverage_complete_count"]
        == sum(e["coverage_state"] == "complete" for e in m["entries"]),
        "complete count matches",
    )
    require(
        counts["coverage_partial_count"]
        == sum(e["coverage_state"] == "partial" for e in m["entries"]),
        "partial count matches",
    )
    require(
        counts["remaining_finding_count"] == 192 - len(m["entries"]),
        "remaining count matches 192-finding target",
    )
    if m["state"] == "complete":
        require(
            len(m["entries"]) == 192,
            "complete locator manifest covers all 192 findings",
        )

    print(
        f"PASSED: source locators valid; entries={len(ids)} "
        f"complete={counts['coverage_complete_count']} "
        f"remaining={counts['remaining_finding_count']} "
        f"upstream_checks={len(_UPSTREAM_CACHE)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
