#!/usr/bin/env python3
"""Self-test for the audit-derived VDV301 SDK manifest baseline v0.1."""

from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
SDK = ROOT / "sdk_manifest"
XS_NS = "http://www.w3.org/2001/XMLSchema"


def load_json(name: str):
    path = SDK / name
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def expect(label: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(label)
    print(f"OK  {label}")


def main() -> int:
    manifest = load_json("manifest_v0.1.json")
    result_schema = load_json("public_result_contract_v0.1.schema.json")
    overrides = load_json("routing_overrides_v0.1.json")

    expect("manifest version is 0.1", manifest["manifest_version"] == "0.1")
    expect("routing overrides version matches manifest", overrides["manifest_version"] == manifest["manifest_version"])
    expect("public result schema is JSON Schema 2020-12", result_schema["$schema"].endswith("2020-12/schema"))

    invariants = manifest["invariants"]
    expect("latest-XSD-wins is disabled", invariants["latest_xsd_wins"] is False)
    expect("latest-dependency-wins is disabled", invariants["latest_dependency_wins"] is False)
    expect("latest external protocol version wins is disabled", invariants["latest_external_protocol_version_wins"] is False)
    expect("candidate selection is explicit only", invariants["candidate_selection_is_explicit_only"] is True)
    expect("operation inventory is not derived from XSD group only", invariants["operation_inventory_from_xsd_group_only"] is False)

    forbidden = set(manifest["public_result_contract"]["forbidden_contract_fields"])
    public_props = set(result_schema.get("properties", {}))
    expect("public contract exposes none of the forbidden internal fields", forbidden.isdisjoint(public_props))
    expect("field_validated is explicitly forbidden", "field_validated" in forbidden)
    expect("public result carries check_id", "check_id" in public_props)
    expect("public result carries authority", "authority" in public_props)
    expect("public result carries severity", "severity" in public_props)

    root_map = ROOT / manifest["storage_model"]["legacy_root_metadata"]
    expect("legacy V1.0 root map exists", root_map.is_file())

    # Candidate dependency resources must exist and must never be implicit official.
    for item in overrides.get("candidate_dependency_resources", []):
        schema = ROOT / item["schema"]
        expect(f"candidate dependency exists: {item['schema']}", schema.is_file())
        expect(f"candidate dependency authority is candidate: {item['schema']}", item["authority"] == "candidate")
        expect(f"candidate dependency requires explicit context: {item['schema']}", item.get("explicit_candidate_context_required") is True)

    for item in overrides.get("candidate_gates", []):
        schema = ROOT / item["schema"]
        expect(f"candidate schema exists: {item['schema']}", schema.is_file())
        expect(f"candidate authority is candidate: {item['schema']}", item["authority"] == "candidate")
        expect(f"candidate opt-in is required: {item['schema']}", item.get("explicit_opt_in_required") is True)

    for item in overrides.get("integration_only_gates", []):
        schema = ROOT / item["schema"]
        expect(f"integration-only schema exists: {item['schema']}", schema.is_file())
        expect(f"integration-only authority is integration: {item['schema']}", item["authority"] == "integration")
        expect(f"integration-only opt-in is required: {item['schema']}", item.get("explicit_opt_in_required") is True)

    for item in overrides.get("legacy_root_profiles", []):
        expect(f"legacy service XSD exists: {item['service_xsd']}", (ROOT / item["service_xsd"]).is_file())
        expect(f"legacy root-map reference exists for {item['service_name']}", (ROOT / item["root_map"]).is_file())

    # Non-XSD routes should not silently claim an ordinary XSD profile.
    non_xsd = {(x["service_name"], x["service_version"]): x for x in overrides.get("non_xsd_routes", [])}
    expect("TimeService V1.0 non-XSD route exists", ("TimeService", "1.0") in non_xsd)
    expect("TimeService uses protocol_discovery_profile", non_xsd[("TimeService", "1.0")]["validation_kind"] == "protocol_discovery_profile")
    expect("HTMLDisplay V2.1 non-XSD route exists", ("HTMLDisplayService", "2.1") in non_xsd)
    expect("HTMLDisplay V2.2 non-XSD route exists", ("HTMLDisplayService", "2.2") in non_xsd)
    expect("HTMLDisplay V2.2a non-XSD route exists", ("HTMLDisplayService", "2.2a") in non_xsd)

    # Special routing facts must be present.
    aliases = overrides.get("aliases", [])
    expect(
        "TicketingService legacy alias is preserved",
        any(x.get("public_service_name") == "TicketingService" and x.get("schema_filename_token") == "TicketInformationService" for x in aliases),
    )
    doc_routes = overrides.get("document_to_schema_routes", [])
    expect(
        "TVS document 2.3 -> schema 2.2 route is preserved",
        any(x.get("service_name") == "TicketValidationService" and x.get("document_version") == "2.3" and x.get("schema_version") == "2.2" for x in doc_routes),
    )
    op_overrides = overrides.get("operation_context_overrides", [])
    expect("TSM-002 override is present", any(x.get("finding") == "TSM-002" for x in op_overrides))
    expect("TSD-003 contextual overrides are present", sum(1 for x in op_overrides if x.get("finding") == "TSD-003") == 2)

    # Parse all root XSDs and ensure every direct include resolves in the stored superbranch.
    xsd_files = sorted(ROOT.glob("*.xsd"))
    expect("root XSD inventory is non-empty", bool(xsd_files))
    include_count = 0
    for path in xsd_files:
        tree = ET.parse(path)
        root = tree.getroot()
        for include in root.findall(f"{{{XS_NS}}}include"):
            location = include.get("schemaLocation")
            if not location:
                continue
            include_count += 1
            target = path.parent / location
            expect(f"include resolves: {path.name} -> {location}", target.is_file())
    expect("at least one XSD include was checked", include_count > 0)

    # Candidate Common/Enums V2.4 must be recognized because candidate service profiles may depend on them.
    candidate_dependencies = {x["schema"] for x in overrides.get("candidate_dependency_resources", [])}
    expect("Common V2.4 candidate dependency classified", "IBIS-IP_common_V2.4.xsd" in candidate_dependencies)
    expect("Enumerations V2.4 candidate dependency classified", "IBIS-IP_Enumerations_V2.4.xsd" in candidate_dependencies)

    print(f"PASSED: SDK manifest v0.1 self-test; root_xsds={len(xsd_files)} includes_checked={include_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
