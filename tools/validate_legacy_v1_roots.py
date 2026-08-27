#!/usr/bin/env python3
"""Compile generated legacy V1.0 operation-root adapters.

The VDV-301-1.0 release used IBIS_IP_V1.0.xsd to provide global operation
roots for several service XSDs that otherwise only define complex types.
The deduplicated superbranch does not store that complete aggregate snapshot.
Instead, schema_profiles/VDV-301-1.0-root-map.csv records the exact official
root-element -> type mappings from the aggregate.

This tool creates temporary XSD harnesses from that metadata and compiles them
with lxml. The harnesses are integration validation adapters, not official VDV
schemas and are never written into the repository.
"""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
import tempfile
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

try:
    from lxml import etree
except ImportError:  # pragma: no cover
    print("ERROR: lxml is required. Install with: python -m pip install lxml", file=sys.stderr)
    raise


def link_or_copy(src: Path, dst: Path) -> None:
    try:
        dst.symlink_to(src.resolve())
    except OSError:
        shutil.copy2(src, dst)


def load_profile(path: Path) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            grouped[row["service_xsd"]].append(row)
    return dict(grouped)


def harness_text(service_xsd: str, rows: list[dict[str, str]]) -> str:
    elements = "\n".join(
        f'  <xs:element name="{escape(row["root_element"])}" type="{escape(row["type_name"])}"/>'
        for row in rows
    )
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"
           elementFormDefault="qualified"
           attributeFormDefault="unqualified">
  <xs:include schemaLocation="{escape(service_xsd)}"/>
{elements}
</xs:schema>
'''


def compile_service(repo_root: Path, service_xsd: str, rows: list[dict[str, str]]) -> tuple[bool, str]:
    required = [
        service_xsd,
        "IBIS-IP_common_V1.0.xsd",
        "IBIS-IP_Enumerations_V1.0.xsd",
    ]
    missing = [name for name in required if not (repo_root / name).exists()]
    if missing:
        return False, f"missing required file(s): {', '.join(missing)}"

    with tempfile.TemporaryDirectory(prefix="vdv301_legacy_v1_") as tmp:
        tmpdir = Path(tmp)
        for name in required:
            link_or_copy(repo_root / name, tmpdir / name)

        harness = tmpdir / "_legacy_v1_root_harness.xsd"
        harness.write_text(harness_text(service_xsd, rows), encoding="utf-8")
        try:
            etree.XMLSchema(etree.parse(str(harness)))
            return True, "OK"
        except Exception as exc:  # noqa: BLE001 - diagnostic tool
            return False, str(exc)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument(
        "--profile",
        type=Path,
        default=Path("schema_profiles/VDV-301-1.0-root-map.csv"),
    )
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    profile = args.profile
    if not profile.is_absolute():
        profile = repo_root / profile

    grouped = load_profile(profile)
    errors = 0
    print(f"Legacy V1.0 root adapter compile check: {len(grouped)} service XSD(s)")
    for service_xsd, rows in sorted(grouped.items()):
        ok, message = compile_service(repo_root, service_xsd, rows)
        status = "OK" if ok else "ERR"
        print(f"{status:3} {service_xsd}: {len(rows)} root declaration(s)")
        if not ok:
            errors += 1
            print(f"    {message}")

    if errors:
        print(f"FAILED: {errors} legacy adapter compile error(s)")
        return 1
    print("PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
