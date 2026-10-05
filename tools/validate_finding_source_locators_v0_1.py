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
BODY_VERIFICATION = ROOT / "audit_registry/pdf_locator_body_verification_v0.1.json"
CURRENT_STATE = ROOT / "00_START_HERE/CURRENT_STATE.json"

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
    body_verification = load(BODY_VERIFICATION)
    current_state = load(CURRENT_STATE)

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

    # Visible-body verification is deliberately tracked separately from
    # structural locator completeness. Until the existing complete set has
    # been revalidated under the explicit body-locator rule, freeze structural
    # progress so a future maintainer/chat cannot skip the quality backlog.
    body_entries = body_verification.get("entries", [])
    body_ids = [e["finding_id"] for e in body_entries]
    require(
        body_ids == ids,
        "body-verification registry tracks exactly the current structural locator finding IDs",
    )
    require(
        len(body_ids) == len(set(body_ids)),
        "body-verification registry uses unique finding IDs",
    )
    body_counts = body_verification["counts"]
    require(
        body_counts["tracked_findings"] == len(body_entries),
        "body-verification tracked count matches entries",
    )
    require(
        body_counts["verified_current_standard"]
        == sum(e["state"] == "verified_current_standard" for e in body_entries),
        "body-verification verified count matches entries",
    )
    require(
        body_counts["pending_current_standard"]
        == sum(e["state"] == "pending_current_standard" for e in body_entries),
        "body-verification pending count matches entries",
    )
    require(
        body_counts["verified_current_standard"]
        + body_counts["pending_current_standard"]
        == body_counts["tracked_findings"],
        "body-verification states account for every tracked finding",
    )
    if (
        body_verification.get("state") != "complete"
        and body_verification.get("block_new_structural_progress_until_complete")
    ):
        require(
            len(ids) == body_verification["frozen_structural_entry_count"],
            "structural locator progress remains frozen until visible-body backlog is complete",
        )
    if body_verification.get("state") == "complete":
        require(
            body_counts["pending_current_standard"] == 0,
            "complete body-verification registry has zero pending findings",
        )

    # Keep the restart state machine-readable and synchronized with the body
    # registry. This prevents a future chat from following stale counts or a
    # stale next-finding pointer even when the registry itself is correct.
    progress = current_state["source_locator_progress"]
    require(
        progress["body_verified_current_standard_count"]
        == body_counts["verified_current_standard"],
        "CURRENT_STATE body verified count matches body-verification registry",
    )
    require(
        progress["body_pending_current_standard_count"]
        == body_counts["pending_current_standard"],
        "CURRENT_STATE body pending count matches body-verification registry",
    )
    require(
        progress["structural_progress_freeze_count"]
        == body_verification["frozen_structural_entry_count"],
        "CURRENT_STATE structural freeze count matches body-verification registry",
    )
    pending_ids = [
        e["finding_id"]
        for e in body_entries
        if e["state"] == "pending_current_standard"
    ]
    expected_next = pending_ids[0] if pending_ids else None
    require(
        progress.get("next_body_revalidation_finding") == expected_next,
        "CURRENT_STATE next body-revalidation finding matches first pending registry entry",
    )
    require(
        current_state["audit"]["source_locator_body_verified_current_standard_count"]
        == body_counts["verified_current_standard"],
        "audit body verified count matches body-verification registry",
    )
    require(
        current_state["audit"]["source_locator_body_pending_current_standard_count"]
        == body_counts["pending_current_standard"],
        "audit body pending count matches body-verification registry",
    )
    require(
        current_state["sdk"]["source_locator_body_verified_current_standard_count"]
        == body_counts["verified_current_standard"],
        "sdk body verified count matches body-verification registry",
    )
    require(
        current_state["sdk"]["source_locator_body_pending_current_standard_count"]
        == body_counts["pending_current_standard"],
        "sdk body pending count matches body-verification registry",
    )
    for body_entry in body_entries:
        if body_entry["state"] == "verified_current_standard":
            require(
                bool(body_entry.get("evidence")),
                f"{body_entry['finding_id']} current-standard body verification has evidence",
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

    ara001 = loc_by.get("ARA-001")
    if ara001:
        for lane in ara001["coverage"]:
            p = lane["pdf_locators"][0]
            require(
                p["printed_pages"] == [1],
                f"ARA-001 {lane['version']} pins the official document-identity cover page",
            )
            require(
                p["section"]
                == "Cover — VDV-Schrift 301-2-19 / Dienst – AnalogRadioService / V 2.4",
                f"ARA-001 {lane['version']} pins the visible cover identity",
            )

    ara002 = loc_by.get("ARA-002")
    if ara002:
        lane = ara002["coverage"][0]
        by_page = {
            p["printed_pages"][0]: p
            for p in lane["pdf_locators"]
        }
        require(
            sorted(by_page) == [11, 12, 13],
            "ARA-002 pins the three visible contradiction surfaces on pages 11-13",
        )
        require(
            by_page[11]["section"]
            == "2.2 DataStructure of SendTelegram Operation / 2.2.1 Request",
            "ARA-002 page 11 pins the actual visible request heading",
        )
        require(
            by_page[11].get("table")
            == "AnalogRadioService.RadioTelegramStructure request-structure table/model",
            "ARA-002 page 11 pins the visible RadioTelegramStructure table/model",
        )
        require(
            by_page[12]["section"]
            == "2.2.1 Request — continuation diagram on printed page 12",
            "ARA-002 page 12 pins the request continuation rather than inventing a new heading",
        )
        require(
            by_page[12].get("table")
            == "AnalogRadioService.RadioTelegramStructure diagram",
            "ARA-002 page 12 pins the visible diagram label",
        )
        require(
            by_page[13]["section"]
            == "2.5 Examples / 2.5.2 XML of a complete telegram",
            "ARA-002 page 13 pins the actual visible XML-example heading",
        )

    ara003 = loc_by.get("ARA-003")
    if ara003:
        for lane in ara003["coverage"]:
            p = lane["pdf_locators"][0]
            require(
                p["printed_pages"] == [11],
                f"ARA-003 {lane['version']} pins printed page 11",
            )
            require(
                p["section"]
                == "2.2 DataStructure of SendTelegram Operation / 2.2.1 Request",
                f"ARA-003 {lane['version']} pins the actual visible request heading",
            )
            require(
                p.get("table")
                == "AnalogRadioService.RadioTelegramStructure request-structure table/model",
                f"ARA-003 {lane['version']} pins the visible RadioTelegramStructure table/model",
            )

    ara004 = loc_by.get("ARA-004")
    if ara004:
        lane = ara004["coverage"][0]
        by_page = {}
        for p in lane["pdf_locators"]:
            by_page.setdefault(p["printed_pages"][0], []).append(p)
        require(
            sorted(by_page) == [10, 13],
            "ARA-004 pins operation inventory page 10 and example page 13",
        )
        p10 = by_page[10][0]
        require(
            p10["section"] == "2.1 Operations of the AnalogRadioService",
            "ARA-004 page 10 pins the actual visible operation heading",
        )
        require(
            p10.get("table") == "Operation inventory and Request / Response table",
            "ARA-004 page 10 pins both visible operation tables",
        )
        sections13 = {p["section"] for p in by_page[13]}
        require(
            "2.5 Examples / 2.5.1 URI for the Operation SendTelegram" in sections13,
            "ARA-004 page 13 pins the URI section heading",
        )
        require(
            "2.5 Examples / 2.5.2 XML of a complete telegram" in sections13,
            "ARA-004 page 13 pins the XML example heading",
        )

    arch001 = loc_by.get("ARCH-001")
    if arch001:
        lane = arch001["coverage"][0]
        by_page = {p["printed_pages"][0]: p for p in lane["pdf_locators"]}
        require(
            sorted(by_page) == [7, 10],
            "ARCH-001 pins visible architecture surfaces on pages 7 and 10",
        )
        require(
            by_page[7]["section"] == "2. Anwendungsbereich",
            "ARCH-001 page 7 pins the actual visible application-scope heading",
        )
        require(
            by_page[10]["section"]
            == "3.2. Begriffe — Dienstorientierte Architektur / Dienst bzw. Service / Operationen",
            "ARCH-001 page 10 pins the visible terminology anchors",
        )

    arch002 = loc_by.get("ARCH-002")
    if arch002:
        lane = arch002["coverage"][0]
        by_page = {p["printed_pages"][0]: p for p in lane["pdf_locators"]}
        require(
            sorted(by_page) == [12, 14],
            "ARCH-002 pins hierarchy context on pages 12 and 14",
        )
        require(
            by_page[12]["section"] == "4.1. Ermittlung der Fachkomponenten",
            "ARCH-002 page 12 pins the actual visible 4.1 heading",
        )
        require(
            by_page[14]["section"]
            == "Abbildung 5: Hierarchisierung durch Ordnung der Fachkomponenten nach Aufrufrichtungen / unmittelbar folgende Client-/Server-Regeln",
            "ARCH-002 page 14 pins the actual visible figure/rule anchor instead of inherited 4.2 context",
        )
        require(
            by_page[14].get("table")
            == "Abbildung 5 and following hierarchy-rule bullets",
            "ARCH-002 page 14 pins Figure 5 and the visible hierarchy-rule bullets",
        )

    arch003 = loc_by.get("ARCH-003")
    if arch003:
        lane = arch003["coverage"][0]
        p = lane["pdf_locators"][0]
        require(
            p["printed_pages"] == [16],
            "ARCH-003 pins printed page 16",
        )
        require(
            p["section"]
            == "Fortsetzung der Beschreibung zu Abbildung 6 — Absatz zum gekuppelten Fahrzeug / unmittelbar vor 5. Funktionsgruppen",
            "ARCH-003 page 16 pins the actual visible coupling paragraph anchor",
        )
        require(
            p.get("table") is None,
            "ARCH-003 page 16 does not invent a visible figure/table identifier",
        )

    arch004 = loc_by.get("ARCH-004")
    if arch004:
        lane = arch004["coverage"][0]
        by_page = {p["printed_pages"][0]: p for p in lane["pdf_locators"]}
        require(
            sorted(by_page) == [7, 26],
            "ARCH-004 pins scope/security surfaces on pages 7 and 26",
        )
        require(
            by_page[7]["section"] == "2. Anwendungsbereich",
            "ARCH-004 page 7 pins the actual visible application-scope heading",
        )
        require(
            by_page[26]["section"] == "6. Systemsicherheit",
            "ARCH-004 page 26 pins the actual visible security heading",
        )
        require(
            by_page[26].get("table") is None,
            "ARCH-004 page 26 does not invent a table identifier",
        )

    arch005 = loc_by.get("ARCH-005")
    if arch005:
        lane = arch005["coverage"][0]
        p = lane["pdf_locators"][0]
        require(
            p["printed_pages"] == [26],
            "ARCH-005 pins printed page 26",
        )
        require(
            p["section"] == "7. Kommunikation mit Diensten",
            "ARCH-005 page 26 pins the actual visible communication heading",
        )
        require(
            p.get("table") is None,
            "ARCH-005 page 26 does not invent a table identifier",
        )

    arch006 = loc_by.get("ARCH-006")
    if arch006:
        lane = arch006["coverage"][0]
        by_page = {p["printed_pages"][0]: p for p in lane["pdf_locators"]}
        require(
            sorted(by_page) == [6, 27],
            "ARCH-006 pins Part-1/Part-2 boundary page 6 and XML page 27",
        )
        require(
            by_page[6]["section"] == "1. Einleitung",
            "ARCH-006 page 6 pins the actual visible introduction heading",
        )
        require(
            by_page[27]["section"] == "7.1. Strukturierung der Informationsinhalte",
            "ARCH-006 page 27 pins the actual visible XML-structure heading",
        )
        require(
            by_page[6].get("table") is None and by_page[27].get("table") is None,
            "ARCH-006 does not invent table identifiers",
        )

    arch007 = loc_by.get("ARCH-007")
    if arch007:
        lane = arch007["coverage"][0]
        p = lane["pdf_locators"][0]
        require(
            p["printed_pages"] == [26],
            "ARCH-007 pins printed page 26",
        )
        require(
            p["section"] == "7. Kommunikation mit Diensten",
            "ARCH-007 page 26 pins the actual visible communication heading",
        )
        require(
            p.get("table") is None,
            "ARCH-007 page 26 does not invent a table identifier",
        )

    arch008 = loc_by.get("ARCH-008")
    if arch008:
        lane = arch008["coverage"][0]
        p = lane["pdf_locators"][0]
        require(
            p["printed_pages"] == [10],
            "ARCH-008 pins printed page 10",
        )
        require(
            p["section"]
            == "Fortsetzung der Definition Fachkomponente — Absatz „nur ein Teil der Fachkomponenten … in Form von Diensten bzw. Applikationen …“ / unmittelbar vor Funktionsgruppe",
            "ARCH-008 page 10 pins the actual visible Fachkomponente continuation anchor",
        )
        require(
            p.get("table") is None,
            "ARCH-008 page 10 does not invent a table identifier",
        )

    bg001 = loc_by.get("BG-001")
    if bg001:
        require(
            all(not lane.get("pdf_locators") for lane in bg001["coverage"]),
            "BG-001 is provenance/XSD-only and does not invent PDF locators",
        )
        expected = {
            ("VDV-301-1.0 historical V1.0 service pool", "IBIS-IP_JourneyInformationService_V1.0.xsd"): "1ee4d7aeb15f3269c5335313be9e214bdb519d2e",
            ("VDV-301-1.0 historical V1.0 service pool", "IBIS-IP_PassengerCountingService_V1.0.xsd"): "600a3ee6290c630a4435fb06ca9803dabaceb788",
            ("VDV-301-1.0 historical V1.0 service pool", "IBIS-IP_SystemManagementService_V1.0.xsd"): "85390f99d6c19c88923ed9a5fc8a5706137708af",
            ("VDV-301-1.0 historical V1.0 service pool", "IBIS-IP_TicketInformationService_V1.0.xsd"): "017ca64666e25d757fc0cde1f1be817f06a743fc",
            ("VDV-301-2.0 historical V1.0 service pool", "IBIS-IP_JourneyInformationService_V1.0.xsd"): "8c303db5a9c0548d66b90174d9c329d33092ad24",
            ("VDV-301-2.0 historical V1.0 service pool", "IBIS-IP_PassengerCountingService_V1.0.xsd"): "4161872be76740abfdd1cddf96f8a736333fc8be",
            ("VDV-301-2.0 historical V1.0 service pool", "IBIS-IP_SystemManagementService_V1.0.xsd"): "2d32630a0f1981e980e6a466e3f6a69136410f24",
            ("VDV-301-2.0 historical V1.0 service pool", "IBIS-IP_TicketInformationService_V1.0.xsd"): "3fda66d872ab0d1c511247f13e715cf3ad56afe7",
        }
        actual = {
            (lane["version"], x["file"]): x["git_blob"]
            for lane in bg001["coverage"]
            for x in lane["xsd_locators"]
        }
        require(actual == expected, "BG-001 pins the exact two official historical V1.0 service pools")

    bg002 = loc_by.get("BG-002")
    if bg002:
        require(
            all(not lane.get("pdf_locators") for lane in bg002["coverage"]),
            "BG-002 is provenance/XSD-only and does not invent PDF locators",
        )
        old_lane, later_lane = bg002["coverage"]
        require(
            old_lane["xsd_locators"][0]["git_blob"]
            == "41289eaed2674a169fdf77a10a2eff293c76d5c4",
            "BG-002 pins the VDV-301-1.0 historical aggregate blob",
        )
        require(
            old_lane["xsd_locators"][0]["ref"] == "VDV-301-1.0",
            "BG-002 aggregate is scoped only to VDV-301-1.0",
        )
        require(
            later_lane["xsd_locators"][0]["git_blob"]
            == "8c303db5a9c0548d66b90174d9c329d33092ad24",
            "BG-002 later lane pins an actually published VDV-301-2.0 service XSD",
        )

    ce001 = loc_by.get("CE-001")
    if ce001:
        lane = ce001["coverage"][0]
        require(
            not lane.get("pdf_locators"),
            "CE-001 is XSD/dependency-only and does not invent PDF locators",
        )
        x = {item["file"]: item for item in lane["xsd_locators"]}
        require(
            x["IBIS-IP_common_V2.3.xsd"]["git_blob"]
            == "0d8926c4063c12de9a5e68b6f0addaab35a55dc1",
            "CE-001 pins official Common V2.3 blob",
        )
        require(
            x["IBIS-IP_common_V2.3.xsd"].get("line_hint") == "5",
            "CE-001 pins the explicit Common V2.3 include line",
        )
        require(
            x["IBIS-IP_Enumerations_V2.2.xsd"]["git_blob"]
            == "2a23b512379b18e8f122ac1272cef8229fb86283",
            "CE-001 pins the exact Enumerations V2.2 dependency blob used by V2.3",
        )

    ce003 = loc_by.get("CE-003")
    if ce003:
        lane = ce003["coverage"][0]
        p = lane["pdf_locators"][0]
        require(
            p["printed_pages"] == [1, 63],
            "CE-003 full-document scope remains bounded by printed pages 1 and 63",
        )
        require(
            p["section"] == "complete-document review scope",
            "CE-003 does not misrepresent a review-scope boundary as a defect section",
        )
        require(
            lane["xsd_locators"][0]["git_blob"]
            == "1946fd37e29ced605654f49ea3d98cd2fbbdc8e4",
            "CE-003 pins the selected candidate Common V2.4 schema blob",
        )

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

    ce020 = loc_by.get("CE-020")
    if ce020:
        require(
            [c["version"] for c in ce020["coverage"]] == ["2.3", "2.3-pr30"],
            "CE-020 keeps official V2.3 and explicit PR30 candidate lanes",
        )
        for lane in ce020["coverage"]:
            p = lane["pdf_locators"][0]
            require(
                p["printed_pages"] == [12],
                f"CE-020 {lane['version']} pins InternationalTextType printed page 12",
            )
            require(
                p["section"] == "1.17 InternationalTextType",
                f"CE-020 {lane['version']} pins section 1.17 InternationalTextType",
            )
            require(
                "Table 17" in p.get("table", ""),
                f"CE-020 {lane['version']} pins Table 17 InternationalTextType",
            )

    ce025 = loc_by.get("CE-025")
    if ce025:
        expected_025 = {
            "1.0": (([20], "1.51 SubscribeRequest", "Table 51"), ([22], "1.57 UnsubscribeRequest", "Table 57")),
            "2.0": (([28], "2.54 SubscribeRequest", "Table 54"), ([30], "2.60 UnsubscribeRequest", "Table 60")),
            "2.1": (([30], "2.54 SubscribeRequest", "Table 54"), ([32], "2.60 UnsubscribeRequest", "Table 60")),
            "2.2": (([32], "2.55 SubscribeRequest", "Table 55"), ([34], "2.61 UnsubscribeRequest", "Table 61")),
            "2.3": (([33], "2.55 SubscribeRequest", "Table 55"), ([35], "2.61 UnsubscribeRequest", "Table 61")),
            "2.4": (([35], "2.54 SubscribeRequest", "Table 54"), ([38], "2.60 UnsubscribeRequest", "Table 60")),
        }
        for lane in ce025["coverage"]:
            require(
                len(lane["pdf_locators"]) == 2,
                f"CE-025 {lane['version']} has SubscribeRequest and UnsubscribeRequest PDF locators",
            )
            for p, expected_locator in zip(
                lane["pdf_locators"], expected_025[lane["version"]], strict=True
            ):
                pages, section, table = expected_locator
                require(
                    p["printed_pages"] == pages,
                    f"CE-025 {lane['version']} pins verified printed page for {section}",
                )
                require(
                    p["section"] == section,
                    f"CE-025 {lane['version']} pins verified section {section}",
                )
                require(
                    table in p.get("table", ""),
                    f"CE-025 {lane['version']} pins verified table for {section}",
                )

    ce026 = loc_by.get("CE-026")
    if ce026:
        expected_026 = {
            "1.0": ([8], "1.4 BeaconPoint"),
            "2.0": ([15], "2.4 BeaconPoint"),
            "2.1": ([16], "2.4 BeaconPoint"),
            "2.2": ([17], "2.4 BeaconPoint"),
            "2.3": ([17], "2.4 BeaconPoint"),
            "2.4": ([19], "2.4 BeaconPoint"),
        }
        for lane in ce026["coverage"]:
            p = lane["pdf_locators"][0]
            pages, section = expected_026[lane["version"]]
            require(
                p["printed_pages"] == pages,
                f"CE-026 {lane['version']} pins verified BeaconPoint printed page",
            )
            require(
                p["section"] == section,
                f"CE-026 {lane['version']} pins verified BeaconPoint section",
            )
            require(
                "Table 4" in p.get("table", ""),
                f"CE-026 {lane['version']} pins Table 4 BeaconPoint",
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
