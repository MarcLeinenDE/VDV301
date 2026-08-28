#!/usr/bin/env python3
"""Executable evidence for Common V2.3 official vs PR #30 candidate overlay.

The test is intentionally isolated. It never mutates repository-root XSD files.
It verifies:
- the stored official/candidate Git blob identities declared by the overlay manifest;
- compilation of Common V2.3 and CustomerInformationService V2.3 in both pools;
- the observable InternationalTextType instance-shape difference introduced by PR #30.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile

from lxml import etree


REPO = Path(__file__).resolve().parents[1]
OVERLAY_MANIFEST = REPO / "sdk_manifest" / "schema_variant_overlays_v0.1.json"
ENUMS = REPO / "IBIS-IP_Enumerations_V2.2.xsd"
OFFICIAL_COMMON = REPO / "IBIS-IP_common_V2.3.xsd"
CANDIDATE_COMMON = REPO / "schema_variants" / "upstream_pr_30" / "IBIS-IP_common_V2.3.xsd"
CIS = REPO / "IBIS-IP_CustomerInformationService_V2.3.xsd"

PROBE_XSD = """<?xml version=\"1.0\"?>
<xs:schema xmlns:xs=\"http://www.w3.org/2001/XMLSchema\" elementFormDefault=\"qualified\">
  <xs:include schemaLocation=\"IBIS-IP_common_V2.3.xsd\"/>
  <xs:element name=\"Probe\" type=\"InternationalTextType\"/>
</xs:schema>
"""

FLAT_INSTANCE = b"""<Probe><Value>Hello</Value><Language>de</Language></Probe>"""
WRAPPED_INSTANCE = b"""<Probe><Value><Value>Hello</Value></Value><Language><Value>de</Value></Language></Probe>"""


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def compile_schema(path: Path) -> etree.XMLSchema:
    return etree.XMLSchema(etree.parse(str(path)))


def valid(schema: etree.XMLSchema, payload: bytes) -> bool:
    return schema.validate(etree.fromstring(payload))


def make_pool(base: Path, common_source: Path) -> Path:
    base.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ENUMS, base / ENUMS.name)
    shutil.copy2(common_source, base / OFFICIAL_COMMON.name)
    shutil.copy2(CIS, base / CIS.name)
    (base / "probe.xsd").write_text(PROBE_XSD, encoding="utf-8")
    return base


def main() -> int:
    manifest = json.loads(OVERLAY_MANIFEST.read_text(encoding="utf-8"))
    overlays = [o for o in manifest.get("overlays", []) if o.get("variant_id") == "common-v2.3-upstream-pr30"]
    if len(overlays) != 1:
        raise RuntimeError("Expected exactly one common-v2.3-upstream-pr30 overlay")
    overlay = overlays[0]

    expected_official = overlay["official_default"]["blob"]
    expected_candidate = overlay["overlay"]["blob"]
    actual_official = git_blob_sha1(OFFICIAL_COMMON)
    actual_candidate = git_blob_sha1(CANDIDATE_COMMON)

    if actual_official != expected_official:
        raise RuntimeError(f"Official blob mismatch: expected {expected_official}, got {actual_official}")
    if actual_candidate != expected_candidate:
        raise RuntimeError(f"Candidate blob mismatch: expected {expected_candidate}, got {actual_candidate}")

    with tempfile.TemporaryDirectory(prefix="vdv301-common-v23-") as tmp:
        root = Path(tmp)
        official_pool = make_pool(root / "official", OFFICIAL_COMMON)
        candidate_pool = make_pool(root / "candidate", CANDIDATE_COMMON)

        # Both isolated dependency families must compile, including a real V2.3 service.
        compile_schema(official_pool / OFFICIAL_COMMON.name)
        compile_schema(candidate_pool / OFFICIAL_COMMON.name)
        compile_schema(official_pool / CIS.name)
        compile_schema(candidate_pool / CIS.name)

        official_probe = compile_schema(official_pool / "probe.xsd")
        candidate_probe = compile_schema(candidate_pool / "probe.xsd")

        results = {
            "official_flat": valid(official_probe, FLAT_INSTANCE),
            "official_wrapped": valid(official_probe, WRAPPED_INSTANCE),
            "candidate_flat": valid(candidate_probe, FLAT_INSTANCE),
            "candidate_wrapped": valid(candidate_probe, WRAPPED_INSTANCE),
        }

    expected = {
        "official_flat": True,
        "official_wrapped": False,
        "candidate_flat": False,
        "candidate_wrapped": True,
    }
    if results != expected:
        raise RuntimeError(f"Unexpected InternationalTextType behaviour: {results!r}; expected {expected!r}")

    evidence = {
        "evidence_id": "EV-106",
        "finding": "CE-020",
        "variant_id": "common-v2.3-upstream-pr30",
        "official_blob": actual_official,
        "candidate_blob": actual_candidate,
        "common_compile_official": "ok",
        "common_compile_candidate": "ok",
        "cis_v2_3_compile_official": "ok",
        "cis_v2_3_compile_candidate": "ok",
        "international_text_type": results,
        "repository_root_mutated": False,
    }
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise
