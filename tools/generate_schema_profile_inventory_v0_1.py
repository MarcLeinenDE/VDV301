#!/usr/bin/env python3
"""Generate the deterministic VDV301 SDK schema-profile inventory v0.1.

The XSD include graph is discovered from stored files. Authority is never guessed
from filenames: every root-level XSD must be present in the explicit authority
baseline. Unknown/new XSD files make generation fail closed.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import xml.etree.ElementTree as ET

XS = "http://www.w3.org/2001/XMLSchema"
FILENAME_RE = re.compile(r"^IBIS-IP_(?P<token>.+)_[Vv](?P<version>\d+\.\d+)\.xsd$")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def schema_identity(filename: str) -> tuple[str, str, str]:
    m = FILENAME_RE.match(filename)
    if not m:
        raise ValueError(f"unsupported XSD filename: {filename}")
    token = m.group("token")
    version = m.group("version")
    if token == "common":
        return token, version, "common"
    if token == "Enumerations":
        return token, version, "enumerations"
    return token, version, "service"


def direct_includes(path: Path) -> list[str]:
    root = ET.parse(path).getroot()
    result: list[str] = []
    for inc in root.findall(f"{{{XS}}}include"):
        location = inc.get("schemaLocation")
        if location:
            result.append(location)
    return sorted(dict.fromkeys(result))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=None)
    parser.add_argument("--output", default=None)
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve() if args.repo_root else Path(__file__).resolve().parents[1]
    sdk = repo / "sdk_manifest"
    manifest = load_json(sdk / "manifest_v0.1.json")
    overrides = load_json(sdk / "routing_overrides_v0.1.json")
    authority_doc = load_json(sdk / "root_schema_authority_v0.1.json")

    if authority_doc.get("manifest_version") != manifest.get("manifest_version"):
        raise SystemExit("authority baseline manifest_version mismatch")

    authority_by_file: dict[str, str] = {}
    for authority, filenames in authority_doc["classes"].items():
        if authority not in {"official", "candidate", "integration"}:
            raise SystemExit(f"unsupported authority class: {authority}")
        for filename in filenames:
            if filename in authority_by_file:
                raise SystemExit(f"duplicate authority classification: {filename}")
            authority_by_file[filename] = authority

    root_xsds = sorted(p.name for p in repo.glob("*.xsd"))
    root_set = set(root_xsds)
    classified_set = set(authority_by_file)
    missing_classification = sorted(root_set - classified_set)
    stale_classification = sorted(classified_set - root_set)
    if missing_classification or stale_classification:
        raise SystemExit(
            "root XSD authority baseline mismatch\n"
            f"unclassified_root_xsds={missing_classification}\n"
            f"classified_but_missing={stale_classification}"
        )

    includes_by_file: dict[str, list[str]] = {}
    for filename in root_xsds:
        includes = direct_includes(repo / filename)
        for dep in includes:
            if dep not in root_set:
                raise SystemExit(f"unresolved include: {filename} -> {dep}")
        includes_by_file[filename] = includes

    def closure(filename: str) -> list[str]:
        seen: set[str] = set()
        stack = list(includes_by_file[filename])
        while stack:
            dep = stack.pop()
            if dep in seen:
                continue
            seen.add(dep)
            stack.extend(includes_by_file[dep])
        return sorted(seen)

    # An official executable profile may not silently depend on candidate or
    # integration resources. That would upgrade non-official material by transit.
    for filename in root_xsds:
        if authority_by_file[filename] != "official":
            continue
        non_official_deps = [
            dep for dep in closure(filename) if authority_by_file[dep] != "official"
        ]
        if non_official_deps:
            raise SystemExit(
                f"official schema depends on non-official resource: {filename} -> {non_official_deps}"
            )

    alias_by_token = {
        item["schema_filename_token"]: item["public_service_name"]
        for item in overrides.get("aliases", [])
    }

    resources = []
    xsd_profiles = []
    for filename in root_xsds:
        token, version, role = schema_identity(filename)
        record = {
            "filename": filename,
            "token": token,
            "version": version,
            "role": role,
            "authority": authority_by_file[filename],
            "direct_includes": includes_by_file[filename],
            "dependency_closure": closure(filename),
            "dependency_authorities": {
                dep: authority_by_file[dep] for dep in closure(filename)
            },
        }
        resources.append(record)
        if role == "service":
            service_name = alias_by_token.get(token, token)
            xsd_profiles.append(
                {
                    "profile_id": f"xsd:{service_name}@{version}:{authority_by_file[filename]}",
                    "validation_kind": "xsd_profile",
                    "service_name": service_name,
                    "service_version": version,
                    "schema_filename": filename,
                    "schema_authority": authority_by_file[filename],
                    "direct_includes": includes_by_file[filename],
                    "dependency_closure": closure(filename),
                }
            )

    non_xsd_profiles = []
    for route in overrides.get("non_xsd_routes", []):
        non_xsd_profiles.append(
            {
                "profile_id": f"{route['validation_kind']}:{route['service_name']}@{route['service_version']}",
                "validation_kind": route["validation_kind"],
                "service_name": route["service_name"],
                "service_version": route["service_version"],
                "schema_authority": None,
                "profile_sources": route.get("profile_sources", []),
            }
        )

    result = {
        "manifest_version": manifest["manifest_version"],
        "kind": "generated-schema-profile-inventory",
        "generation_rule": "XSD include graph discovered from stored root files; authority from explicit fail-closed baseline; routing overrides applied separately.",
        "counts": {
            "root_xsd_resources": len(resources),
            "xsd_service_profiles": len(xsd_profiles),
            "non_xsd_profiles": len(non_xsd_profiles),
            "official_root_xsds": sum(1 for x in resources if x["authority"] == "official"),
            "candidate_root_xsds": sum(1 for x in resources if x["authority"] == "candidate"),
            "integration_root_xsds": sum(1 for x in resources if x["authority"] == "integration"),
        },
        "resources": resources,
        "xsd_profiles": sorted(xsd_profiles, key=lambda x: x["profile_id"]),
        "non_xsd_profiles": sorted(non_xsd_profiles, key=lambda x: x["profile_id"]),
        "document_to_schema_routes": overrides.get("document_to_schema_routes", []),
        "unresolved_strict_xsd_profiles": overrides.get("unresolved_strict_xsd_profiles", []),
        "operation_context_overrides": overrides.get("operation_context_overrides", []),
    }

    encoded = json.dumps(result, indent=2, ensure_ascii=False, sort_keys=False) + "\n"
    if args.output:
        out = Path(args.output)
        if not out.is_absolute():
            out = repo / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(encoded, encoding="utf-8")
    if not args.check_only:
        print(encoded, end="")
    print(
        "PROFILE_INVENTORY_OK "
        f"root_xsds={result['counts']['root_xsd_resources']} "
        f"service_profiles={result['counts']['xsd_service_profiles']} "
        f"official={result['counts']['official_root_xsds']} "
        f"candidate={result['counts']['candidate_root_xsds']} "
        f"integration={result['counts']['integration_root_xsds']} "
        f"non_xsd={result['counts']['non_xsd_profiles']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
