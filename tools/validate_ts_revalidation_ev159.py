#!/usr/bin/env python3
"""EV-159: fail-closed revalidation of frozen TimeService findings TS-001..002.

TS-001 is evaluated on the protocol/discovery authority lane: the official
VDV 301-2-10 TimeService V1.0 writing, the shared ServiceNameEnumeration,
exact official VDV-301-1.0 / VDV-301-2.0 release trees, and the deterministic
RV-003 SNTP/DNS-SD runtime profile. No TimeService XML schema is invented.

TS-002 is a documentation finding. Its physical-page evidence is carried by
the byte-pinned source acquisition and fresh renders; Poppler text extraction
is used only as a byte-derived fingerprint, not as the semantic authority.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path

from lxml import etree

PDF_URL = "https://www.vdv.de/301-2-10sds-v-1-01.pdfx"
PDF_SHA256 = "d040f503be8e82f5500220ba5cc9b0b41a2fa10db80d9f3980eed191378594d3"
PDF_SIZE = 515920
PDF_PAGES = 10
PDF_TEXT_HASHES = {
    "full": "d082a1b888fe820fff61b886ed27839b9050df8866034e19c150ecc663bf7c0d",
    3: "260684a5d055f86183d7a5d1e522268e431d548ad27616a630dcd20ed921862e",
    4: "8d12268029c58f7af5053d4c62da021ab194b0e42204a0ad5010069f3a130432",
    5: "d938f64fe3ad46d54c10aaaa5dc183f1c975e23e9d99557f1dbe3d5e8fd292cd",
    6: "446b55d53264de78555566eaa43d00604e798e8b75eaf016b1578b5041879897",
}

SOURCE_PIN = {
    "run_id": 34814542791,
    "job_id": 103882386972,
    "artifact_id": 10336172299,
    "artifact_digest": "sha256:c24cfc7d8b80652a5caaeafa4d131f31c32fcbe85e45cfb4a6bb5edb2f789c94",
    "head_sha": "bd158b2a6121a3f7e4612acca5607875ab7ab852",
}

UPSTREAM = {
    "v1_0_commit": "f5b53785f703e898632603eec3bfa3555a79fdba",
    "v1_0_tree": "729bbe3270e52fed3e0641466048a745d5a09b32",
    "v2_0_commit": "f2569a91f0a7c737a0ca7c0280b28ad223d7ee08",
    "v2_0_tree": "11daf0ebb3b26745c036ee19a547ad16d39f922c",
    "enum_v1_blob": "a9bea5bc73003ed91ded8519db06c32c4067831d",
}

EXPECTED_BLOBS = {
    "audit_registry/finding_inventory_frozen_2026-09-03.json": "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
    "audit_registry/finding_revalidation_registry_v0.1.json": "0a4bfcb5d895f25381afd56c32fe5c7d349e4de0",
    "00_START_HERE/CURRENT_STATE.json": "f3c248261066c3760ac093e73c6bfaca484c67c1",
    "audit_registry/pdf_source_registry_v0.1.json": "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
    "audit_registry/pdf_source_pins_v0.1.json": "88349638b423689799af700e8a1c8ec99bbfb67b",
    "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md": "969cce8b14b50ded2ca5eb745674b894428ecf1a",
    "docs/pdf_xsd_semantic_audit/TIME_SERVICE_FINDINGS_REGISTER_ADDENDUM.md": "23723fbb6bb99ffa3aa1eb8c13feae6aa95a0170",
    "docs/pdf_xsd_semantic_audit/deep_read/TIME_V1.0.md": "82a88fbd6dae5d22f472bf144770d915fcc902ea",
    "IBIS-IP_Enumerations_V1.0.xsd": "a9bea5bc73003ed91ded8519db06c32c4067831d",
    "tools/runtime_discovery_profile.py": "4473b913ad4576982789b2791b44e2cf1cba0c8d",
    "tools/runtime_http_profile.py": "937a50223a5e4545ce3d33f4f0d8b0ce05b1cb4d",
    "tools/runtime_time_profile.py": "acd28ca0bd6ac1917b3d2db29745555b7e17d8dd",
    "tools/validate_time_runtime_rv003.py": "ff6e3fcd35d4c2f6bff760b3e86f5adb0e72156c",
}

TARGET_STATES = {
    "TS-001": "contextual_not_defect",
    "TS-002": "context_verified",
}

TERMINAL_STATES = {
    "context_verified",
    "field_validated",
    "executable_confirmed",
    "contextual_not_defect",
    "withdrawn",
    "unresolved",
    "superseded",
}

NS = {"xs": "http://www.w3.org/2001/XMLSchema"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"OK  {message}")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def pdf_page_count(pdf: Path) -> int:
    out = subprocess.check_output(["pdfinfo", str(pdf)], text=True, errors="replace")
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise AssertionError("pdfinfo did not expose page count")


def extract_text(pdf: Path, out: Path, page: int | None = None) -> None:
    cmd = ["pdftotext", "-layout"]
    if page is not None:
        cmd += ["-f", str(page), "-l", str(page)]
    cmd += [str(pdf), str(out)]
    subprocess.run(cmd, check=True)


def render_page(pdf: Path, page: int, out_dir: Path) -> Path:
    prefix = out_dir / f"time-{page:02d}"
    subprocess.run([
        "pdftoppm", "-png", "-r", "180", "-f", str(page), "-l", str(page),
        "-singlefile", str(pdf), str(prefix)
    ], check=True)
    png = prefix.with_suffix(".png")
    require(png.is_file() and png.stat().st_size > 0, f"rendered physical page {page} exists")
    return png


def tracked_root_xsds(repo: Path) -> list[str]:
    names = git(repo, "ls-files", "*.xsd").splitlines()
    return [n for n in names if n and "/" not in n]


def upstream_guard(repo: Path, expected_commit: str, expected_tree: str, label: str) -> dict:
    commit = git(repo, "rev-parse", "HEAD")
    tree = git(repo, "rev-parse", "HEAD^{tree}")
    require(commit == expected_commit, f"{label} exact commit = {commit}")
    require(tree == expected_tree, f"{label} exact tree = {tree}")
    xsds = tracked_root_xsds(repo)
    time_xsds = [n for n in xsds if "timeservice" in n.lower()]
    require(not time_xsds, f"{label} contains no dedicated TimeService XSD")
    enum_blob = git(repo, "rev-parse", "HEAD:IBIS-IP_Enumerations_V1.0.xsd")
    require(enum_blob == UPSTREAM["enum_v1_blob"], f"{label} V1.0 enumeration blob is exact")
    return {"commit": commit, "tree": tree, "root_xsd_count": len(xsds), "time_service_xsds": time_xsds}


def next_after_targets(entries: list[dict]) -> tuple[int, int, str | None, str | None]:
    projected = copy.deepcopy(entries)
    by_id = {e["finding_id"]: e for e in projected}
    for fid, state in TARGET_STATES.items():
        by_id[fid]["revalidation_state"] = state
        by_id[fid]["terminal_state_source"] = "PROJECTED_EV159"
    terminal = sum(e.get("revalidation_state") in TERMINAL_STATES for e in projected)
    pending = sum(e.get("revalidation_state") == "pending" for e in projected)
    first = next((e["finding_id"] for e in projected if e.get("revalidation_state") == "pending"), None)
    block = first.split("-", 1)[0] if first else None
    return terminal, pending, first, block


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--upstream-v10-dir", required=True)
    ap.add_argument("--upstream-v20-dir", required=True)
    ap.add_argument("--output-dir", required=True)
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    pdf = Path(args.pdf).resolve()
    upstream_v10 = Path(args.upstream_v10_dir).resolve()
    upstream_v20 = Path(args.upstream_v20_dir).resolve()
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    # Exact post-TKT / pre-TS audit authority.
    for rel, expected in EXPECTED_BLOBS.items():
        p = root / rel
        require(p.is_file(), f"authority file exists: {rel}")
        observed = git_blob_sha(p.read_bytes())
        require(observed == expected, f"exact blob {rel} = {observed}")

    registry = load(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    entries = registry["inventory"]["entries"]
    by_id = {e["finding_id"]: e for e in entries}
    terminal = sum(e.get("revalidation_state") in TERMINAL_STATES for e in entries)
    pending = sum(e.get("revalidation_state") == "pending" for e in entries)
    first_pending = next(e["finding_id"] for e in entries if e.get("revalidation_state") == "pending")
    require((terminal, pending) == (155, 37), f"pre-TS counts = {terminal}/{pending}")
    require(first_pending == "TS-001", "pre-TS first pending is TS-001")
    require(registry.get("next_revalidation_block") == "TS", "registry next block is TS")
    for fid in TARGET_STATES:
        require(by_id[fid].get("revalidation_state") == "pending", f"{fid} remains pending before EV-159")
        require(by_id[fid].get("terminal_state_source") is None, f"{fid} has no premature terminal source")

    audit = load(root / "00_START_HERE/CURRENT_STATE.json")["audit"]
    require(audit.get("finding_revalidation_completed_findings") == 155, "CURRENT_STATE terminal count is 155")
    require(audit.get("finding_revalidation_pending_findings") == 37, "CURRENT_STATE pending count is 37")
    require(audit.get("finding_revalidation_next_block") == "TS", "CURRENT_STATE next block is TS")

    addendum = (root / "docs/pdf_xsd_semantic_audit/TIME_SERVICE_FINDINGS_REGISTER_ADDENDUM.md").read_text(encoding="utf-8")
    for token in (
        "TS-001 - no dedicated TimeService XSD",
        "non_xsd_service_by_design",
        "protocol_discovery_profile",
        "_ibisip_udp._udp",
        "SNTP / RFC 4330",
        "No IBIS-IP_TimeService_V1.0.xsd was found",
        "ServiceNameEnumeration V1.0 nevertheless contains TimeService",
        "TS-002 - English foreword wrong document number",
        "The English foreword says VDV 301-2-1 describes the TimeService",
    ):
        require(token in addendum, f"canonical TimeService addendum contains {token!r}")

    # Byte-exact official writing. Text is fingerprint-only; visual semantics were
    # reviewed from the pinned rendered pages and are preserved again below.
    require(pdf.is_file(), "fresh TimeService PDF exists")
    require(sha256(pdf) == PDF_SHA256, "fresh TimeService PDF SHA-256 matches pin")
    require(pdf.stat().st_size == PDF_SIZE, "fresh TimeService PDF size matches pin")
    require(pdf_page_count(pdf) == PDF_PAGES, f"fresh TimeService PDF page count = {PDF_PAGES}")

    text_dir = out / "page_text"
    render_dir = out / "renders"
    text_dir.mkdir(exist_ok=True)
    render_dir.mkdir(exist_ok=True)
    full_text = text_dir / "document.txt"
    extract_text(pdf, full_text)
    require(sha256(full_text) == PDF_TEXT_HASHES["full"], "full Poppler text fingerprint matches source-pin run")
    page_text_hashes: dict[str, str] = {}
    for p in (3, 4, 5, 6):
        target = text_dir / f"page-{p:02d}.txt"
        extract_text(pdf, target, p)
        observed = sha256(target)
        require(observed == PDF_TEXT_HASHES[p], f"physical page {p} text fingerprint matches source-pin run")
        page_text_hashes[str(p)] = observed

    render_hashes = {}
    for p in (4, 6):
        png = render_page(pdf, p, render_dir)
        render_hashes[str(p)] = {"sha256": sha256(png), "bytes": png.stat().st_size, "file": str(png.relative_to(out))}

    # Shared schema identity: TimeService is a valid ServiceName, while there is
    # intentionally no dedicated TimeService XML schema in the integration pool.
    enum_tree = etree.parse(str(root / "IBIS-IP_Enumerations_V1.0.xsd"))
    service_names = enum_tree.xpath(
        "./xs:simpleType[@name='ServiceNameEnumeration']/xs:restriction/xs:enumeration/@value",
        namespaces=NS,
    )
    require("TimeService" in service_names, "ServiceNameEnumeration V1.0 contains TimeService")
    root_xsds = tracked_root_xsds(root)
    require(len(root_xsds) == 50, "integration root XSD pool contains exactly 50 schemas")
    require(not [n for n in root_xsds if "timeservice" in n.lower()], "integration root XSD pool contains no dedicated TimeService XSD")

    v10 = upstream_guard(upstream_v10, UPSTREAM["v1_0_commit"], UPSTREAM["v1_0_tree"], "official VDV-301-1.0 release")
    v20 = upstream_guard(upstream_v20, UPSTREAM["v2_0_commit"], UPSTREAM["v2_0_tree"], "official VDV-301-2.0 release")

    # Executable protocol/discovery behaviour: positive and negative SNTP/DNS-SD
    # cases, the no-cyclic invariant and the no-XML routing guard all rerun here.
    rv = subprocess.run(
        ["python", "tools/validate_time_runtime_rv003.py"], cwd=root, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    (out / "rv003.log").write_text(rv.stdout, encoding="utf-8")
    require(rv.returncode == 0, "RV-003 deterministic TimeService runtime profile passes")
    require("PASSED: RV-003 deterministic TimeService / RFC 4330 SNTP classifier behavior confirmed" in rv.stdout,
            "RV-003 completion marker is present")
    require("TimeService routes to protocol_discovery_profile" in rv.stdout,
            "RV-003 confirms protocol/discovery routing")
    require("TimeService does not synthesize XML operations" in rv.stdout,
            "RV-003 confirms no invented XML operations")
    require("TimeService does not expect cyclic transmission of current time" in rv.stdout,
            "RV-003 confirms no-cyclic delivery invariant")

    post_terminal, post_pending, next_finding, next_block = next_after_targets(entries)
    require((post_terminal, post_pending) == (157, 35), f"projected post-TS counts = {post_terminal}/{post_pending}")
    require(next_finding is not None, "a next pending finding remains after TS")

    result = {
        "evidence_id": "EV-159",
        "result": "PASS",
        "scope": list(TARGET_STATES),
        "recommended_terminal_states": TARGET_STATES,
        "prestate": {"terminal": terminal, "pending": pending, "first_pending": first_pending, "next_block": "TS"},
        "projected_poststate": {"terminal": post_terminal, "pending": post_pending, "first_pending": next_finding, "next_block": next_block},
        "source_pin": SOURCE_PIN,
        "pdf_authority": {
            "source_id": "TIME_V1.0",
            "official_url": PDF_URL,
            "sha256": PDF_SHA256,
            "size_bytes": PDF_SIZE,
            "pages": PDF_PAGES,
            "semantic_evidence_mode": "byte-pinned rendered visual; Poppler text hashes are fingerprint-only",
            "visual_findings": {
                "TS-002": "physical page 4: German foreword identifies VDV 301-2-10 while adjacent English foreword says VDV 301-2-1",
                "TS-001": "physical page 6: TimeService is SNTP/RFC-4330 and DNS-SD profile using _ibisip_udp._udp / sntp-server; cyclic current-time transmission is not intended",
            },
            "page_text_sha256": page_text_hashes,
            "render_hashes": render_hashes,
        },
        "xsd_authority": {
            "integration_enum_blob": EXPECTED_BLOBS["IBIS-IP_Enumerations_V1.0.xsd"],
            "integration_root_xsd_count": len(root_xsds),
            "integration_time_service_xsd": False,
            "official_v1_0": v10,
            "official_v2_0": v20,
        },
        "runtime_evidence": {
            "validator": "tools/validate_time_runtime_rv003.py",
            "validator_blob": EXPECTED_BLOBS["tools/validate_time_runtime_rv003.py"],
            "profile_blob": EXPECTED_BLOBS["tools/runtime_time_profile.py"],
            "result": "PASS",
            "validation_kind": "protocol_discovery_profile",
            "xml_operations": [],
            "cyclic_time_broadcast_expected": False,
        },
        "active_disproof": {
            "TS-001": "Checked exact official VDV-301-1.0 and VDV-301-2.0 release trees plus the 50-root integration pool for a dedicated TimeService XSD; none exists. Shared ServiceNameEnumeration still contains TimeService and RV-003 exercises the protocol/discovery path.",
            "TS-002": "The byte-identical official writing was freshly rendered. The contradictory document number is on physical page 4 of the pinned source, so it is not an inferred XSD defect or a source-identity mismatch.",
        },
        "xsd_mutated": False,
        "frozen_inventory_mutated": False,
    }
    (out / "ev159_result.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("PASSED: EV-159 TS TimeService revalidation")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
