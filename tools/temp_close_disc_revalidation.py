#!/usr/bin/env python3
"""Apply the DISC-001..003 legacy-finding revalidation closure.

Temporary helper. The closure workflow removes this file before committing.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "audit_registry/finding_revalidation_registry_v0.1.json"
PINS = ROOT / "audit_registry/pdf_source_pins_v0.1.json"
STATE = ROOT / "00_START_HERE/CURRENT_STATE.json"
FROZEN = ROOT / "audit_registry/finding_inventory_frozen_2026-09-03.json"
REGISTER = ROOT / "docs/pdf_xsd_semantic_audit/NETWORK_DISCOVERY_FINDINGS_REGISTER_ADDENDUM.md"
REPORT = ROOT / "docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_DISC_2026-09-03.md"

TERMINAL = {
    "context_verified",
    "executable_confirmed",
    "contextual_not_defect",
    "withdrawn",
    "unresolved",
    "superseded",
}

NEW_PINS = [
    {
        "source_id": "VDV301-2_V1.0_DE",
        "expected_sha256": "2214b36f83cfcac7fade934fa8b2bfc866a84be85f2f8b615957972238f2ed75",
        "expected_size_bytes": 1790447,
        "pinned_at_utc": "2026-09-03T11:54:32Z",
        "deep_read_source_ready": True,
        "evidence_run_id": "33752224704",
        "evidence_job_id": "100638164877",
        "evidence_artifact_id": "9892036202",
        "artifact_digest_sha256": "263b468f0d5752fa160e7d03e5097482c49e3e56650c8b33d014cc0cf5297030",
        "page_count": 86,
        "fulltext_sha256": "f18ee076f675e8e4ce71222ab782770d54f49e0107683a661bf6f3cb1f760cf2",
        "targeted_visual_pages": [20, 80],
        "pin_note": "DISC legacy revalidation: fresh official retrieval plus targeted visible source review.",
    },
    {
        "source_id": "VDV301-2_BASE_V2.0",
        "expected_sha256": "fc67ed1c028cfc3815fbd03dd10e7027f0babbc21145da930289b93527e77f37",
        "expected_size_bytes": 2374295,
        "pinned_at_utc": "2026-09-03T11:54:45Z",
        "deep_read_source_ready": True,
        "evidence_run_id": "33752224704",
        "evidence_job_id": "100638164877",
        "evidence_artifact_id": "9892036202",
        "artifact_digest_sha256": "263b468f0d5752fa160e7d03e5097482c49e3e56650c8b33d014cc0cf5297030",
        "page_count": 115,
        "fulltext_sha256": "093c67f67afd600bb4a9540950a6a98aabbe0b8fbb5b7f305b107c9727a9ef02",
        "targeted_visual_pages": [21],
        "pin_note": "DISC legacy revalidation: fresh official retrieval plus targeted visible bilingual IP-address review.",
    },
    {
        "source_id": "VDV301-2_BASE_V2.1",
        "expected_sha256": "685fdca55dbb4f525390bad6bdbb00700be78a408dc4c2fa770b094edf4afe0a",
        "expected_size_bytes": 2671005,
        "pinned_at_utc": "2026-09-03T11:55:02Z",
        "deep_read_source_ready": True,
        "evidence_run_id": "33752224704",
        "evidence_job_id": "100638164877",
        "evidence_artifact_id": "9892036202",
        "artifact_digest_sha256": "263b468f0d5752fa160e7d03e5097482c49e3e56650c8b33d014cc0cf5297030",
        "page_count": 130,
        "fulltext_sha256": "d59f28ecc22e7d14cf8ca83a657881082b48945b7437432d3f120dce9e9dd77b",
        "targeted_visual_pages": [22],
        "pin_note": "DISC legacy revalidation: fresh official retrieval plus targeted visible bilingual IP-address review.",
    },
    {
        "source_id": "VDV301-2_GC_V2.2",
        "expected_sha256": "96cf4a146e0c7bfc12eb21a5701d73ed3c570d7689c9f738450cc783206af051",
        "expected_size_bytes": 1562305,
        "pinned_at_utc": "2026-09-03T11:55:19Z",
        "deep_read_source_ready": True,
        "evidence_run_id": "33752224704",
        "evidence_job_id": "100638164877",
        "evidence_artifact_id": "9892036202",
        "artifact_digest_sha256": "263b468f0d5752fa160e7d03e5097482c49e3e56650c8b33d014cc0cf5297030",
        "page_count": 79,
        "fulltext_sha256": "79f27be364a478f1e8899ee64035dc54e78efcf29d0455953ffaa2066f647195",
        "targeted_visual_pages": [17, 20],
        "pin_note": "DISC legacy revalidation: fresh official retrieval plus targeted visible German/English rule-conflict review.",
    },
]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ev-run-id", required=True)
    args = ap.parse_args()

    frozen_before = FROZEN.read_bytes()

    reg = load(REGISTRY)
    entries = reg["inventory"]["entries"]
    by_id = {e["finding_id"]: e for e in entries}
    for fid in ("DISC-001", "DISC-002", "DISC-003"):
        assert by_id[fid]["revalidation_state"] == "pending", (fid, by_id[fid])
        by_id[fid]["revalidation_state"] = "context_verified"
        by_id[fid]["terminal_state_source"] = "docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_DISC_2026-09-03.md"

    reg["next_revalidation_block"] = "DMS"
    blocks = reg.setdefault("revalidation_blocks", {})
    assert "DISC" not in blocks
    blocks["DISC"] = {
        "date": "2026-09-03",
        "state": "completed",
        "authority_lane": "official_byte_pinned_VDV_General_Conventions_Base_Services_plus_RFC_Editor_definition_provenance",
        "evidence_id": "EV-126",
        "evidence_run_id": args.ev_run_id,
        "source_pin_run_id": "33752224704",
        "source_pin_job_id": "100638164877",
        "source_pin_artifact_id": "9892036202",
        "source_pin_artifact_digest_sha256": "263b468f0d5752fa160e7d03e5097482c49e3e56650c8b33d014cc0cf5297030",
        "source_hashes": {p["source_id"]: p["expected_sha256"] for p in NEW_PINS} | {
            "VDV301-2_GC_V2.3": "4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603",
            "VDV301-2_GC_V2.4": "048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d",
        },
        "visual_pages_checked": {
            "VDV301-2_V1.0_DE": [20, 80],
            "VDV301-2_BASE_V2.0": [21],
            "VDV301-2_BASE_V2.1": [22],
            "VDV301-2_GC_V2.2": [17, 20],
            "VDV301-2_GC_V2.3": [27],
            "VDV301-2_GC_V2.4": [20, 23, 30, 31, 75],
        },
        "rfc_definition_sources": {
            "RFC2927": "https://www.rfc-editor.org/rfc/rfc2927.txt",
            "RFC3927": "https://www.rfc-editor.org/rfc/rfc3927.txt",
        },
        "findings": {
            "DISC-001": "context_verified",
            "DISC-002": "context_verified",
            "DISC-003": "context_verified",
        },
        "active_disproof_attempts": {
            "DISC-001": "Rejected the hypothesis that the discrepancy is only an RFC-number translation typo: exact V2.2+ German pages remove prescribed IP allocation while exact English pages retain ZeroConf/169.254 requirements.",
            "DISC-002": "Rejected the hypothesis that RFC 2927 could define IPv4 Link-Local addressing: RFC Editor identifies 2927 as LDAP-schema MIME profile and 3927 as IPv4 Link-Local 169.254/16.",
            "DISC-003": "Rejected the hypothesis that the V2.4 history line is only editorial: V2.3 German Table 3 lacks coachnumber/deviceclass/deviceID and V2.4 German Table 3 contains them.",
        },
        "executable_evidence_reason_not_applicable": "DISC-001..003 are cross-language/reference/version-history documentation findings in the non-XSD discovery/profile lane. They make no XML-validity or schema-shape claim.",
        "sdk_handling": "Do not hard-enforce ZeroConf/169.254 as a universal VDV rule from the stale English language track; keep language/version provenance and external-RFC diagnostics separate from VDV rule attribution.",
        "xsd_mutation": False,
        "terminal_state_source": "docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_DISC_2026-09-03.md",
    }
    dump(REGISTRY, reg)

    pins = load(PINS)
    source_list = pins["sources"]
    existing = {x["source_id"]: x for x in source_list}
    for new in NEW_PINS:
        assert new["source_id"] not in existing, new["source_id"]
        source_list.append(new)
    # Existing V2.3/V2.4 pins must agree with EV-126 source bytes.
    assert existing["VDV301-2_GC_V2.3"]["expected_sha256"] == "4a59cb71d9559b9c197f39eccf17f38bd2dd315246f5020be3c8d0f45b639603"
    assert existing["VDV301-2_GC_V2.4"]["expected_sha256"] == "048f805fe3ddc894556899a94e36ec1b5d93eea31b8cdc5a88fac5ad87235e4d"
    dump(PINS, pins)

    state = load(STATE)
    audit = state["audit"]
    active = audit.setdefault("pinned_active_sources", [])
    for sid in [p["source_id"] for p in NEW_PINS]:
        if sid not in active:
            active.append(sid)
    audit["pdf_sources_byte_pinned"] = len(pins["sources"])
    terminal_count = sum(1 for e in entries if e["revalidation_state"] in TERMINAL)
    pending_count = len(entries) - terminal_count
    assert terminal_count == 50, terminal_count
    assert pending_count == 142, pending_count
    audit["finding_revalidation_next_block"] = "DMS"
    audit["finding_revalidation_completed_findings"] = terminal_count
    audit["finding_revalidation_pending_findings"] = pending_count
    audit["finding_revalidation_current_block"] = "DISC"
    audit["finding_revalidation_latest_completed_block"] = "DISC"
    audit["finding_revalidation_latest_terminal_state_source"] = "docs/pdf_xsd_semantic_audit/FINDING_REVALIDATION_DISC_2026-09-03.md"
    audit["latest_revalidation_evidence_id"] = "EV-126"
    audit["disc_revalidation"] = {
        "status": "completed",
        "evidence_id": "EV-126",
        "evidence_run_id": args.ev_run_id,
        "source_pin_run_id": "33752224704",
        "source_pin_artifact_id": "9892036202",
        "findings": {
            "DISC-001": "context_verified",
            "DISC-002": "context_verified",
            "DISC-003": "context_verified",
        },
        "xsd_mutation": False,
    }
    dump(STATE, state)

    report = f"""# Finding revalidation - DISC-001..DISC-003\n\nDate: 2026-09-03\nState: completed under current `FINDING_EVIDENCE_GATE.md`\nEvidence: `EV-126` (run `{args.ev_run_id}`)\nSource pin/render run: `33752224704`, job `100638164877`, artifact `9892036202`\nArtifact digest: `sha256:263b468f0d5752fa160e7d03e5097482c49e3e56650c8b33d014cc0cf5297030`\n\n## Authority lane\n\nThese findings are non-XSD discovery/documentation findings. The authoritative evidence is the exact official VDV publication by version/language plus RFC Editor definition provenance where an external RFC number is being classified. No XML schema contract is inferred from this block.\n\nFour previously unpinned General-Conventions/Base-Service sources were freshly retrieved and pinned during this revalidation. V2.3 and V2.4 were also re-fetched and matched their existing pins byte-for-byte.\n\n## DISC-001 - German/English IP-address allocation conflict\n\nTerminal state: `context_verified`.\n\nVisible exact-source evidence establishes the version chain:\n\n- V1.0 German page 20 uses ZeroConf, RFC 2927 and 169.254.xxx.xxx.\n- V2.0 page 21 and V2.1 page 22 use RFC 3927 in German but RFC 2927 in English for the same link-local rule.\n- V2.2 pages 17/20, V2.3 pages 17/20 and V2.4 pages 20/23 are materially divergent: German says there are no prescribed IP-address allocation rules and gives fixed IP/DHCP as best practice; English retains ZeroConf, RFC 2927 and 169.254.xxx.xxx requirements.\n\nStrongest counter-hypothesis rejected: this is not merely a wrong RFC number in an otherwise equivalent translation. The V2.2+ language tracks state different allocation semantics.\n\nSDK consequence retained: do not hard-enforce ZeroConf or 169.254/16 as a universal VDV requirement from the stale English track alone. Preserve version/language provenance when reporting the conflict.\n\n## DISC-002 - RFC 2927 reference mismatch\n\nTerminal state: `context_verified`.\n\nV1.0 page 20 cites RFC 2927 for automatic 169.254 addressing; the same publication's page 80 bibliography labels RFC 2927 `MIME Directory Profile for LDAP Schema`. Official RFC Editor definition provenance independently confirms:\n\n- RFC 2927: MIME Directory Profile for LDAP Schema.\n- RFC 3927: Dynamic Configuration of IPv4 Link-Local Addresses, including 169.254/16.\n\nStrongest counter-hypothesis rejected: RFC 2927 is not an alternate IPv4 Link-Local specification.\n\nThis remains a reference-number/documentation finding only. It does not independently turn RFC 3927 into a universal VDV allocation requirement and does not override DISC-001.\n\n## DISC-003 - V2.4 German DNS-SD table repair\n\nTerminal state: `context_verified`.\n\nV2.4 page 75 explicitly records that missing entries in the German version of Table 3 were added. The visible table comparison confirms the repair is real:\n\n- V2.3 German Table 3 page 27 ends after the earlier attributes and lacks `coachnumber`, `deviceclass` and `deviceID`.\n- V2.4 German Table 3 pages 30-31 contains `coachnumber`, `deviceclass` and `deviceID`.\n\nStrongest counter-hypothesis rejected: the V2.4 history note is not merely editorial wording without a corresponding document change.\n\n## Executable-evidence decision\n\nNo XML-validity, schema-shape, compositor, cardinality, enum or root behavior is claimed by DISC-001..003. Therefore XSD executable validation is not applicable. EV-126 is a deterministic exact-source/RFC-provenance evidence check, not an XSD conformance test.\n\nNo XSD changed. The frozen 192-finding inventory remains immutable.\n\nNext revalidation block: `DMS`.\n"""
    REPORT.write_text(report.rstrip() + "\n", encoding="utf-8")

    marker = "## Legacy finding revalidation - 2026-09-03"
    register = REGISTER.read_text(encoding="utf-8")
    assert marker not in register
    register += f"""\n{marker}\n\nCurrent Evidence-Gate terminal states:\n\n```text\nDISC-001  context_verified  EV-126 run {args.ev_run_id}\nDISC-002  context_verified  EV-126 run {args.ev_run_id}\nDISC-003  context_verified  EV-126 run {args.ev_run_id}\n```\n\nThe V1.0, Base V2.0, Base V2.1 and General-Conventions V2.2 PDFs were freshly byte-pinned in source run `33752224704`; V2.3/V2.4 were re-fetched byte-identically. Targeted rendered pages closed the material visual-source gap for these three findings. RFC 2927/3927 definition provenance was checked against RFC Editor. No XSD contract applies to these findings and no XSD was changed.\n"""
    REGISTER.write_text(register.rstrip() + "\n", encoding="utf-8")

    assert FROZEN.read_bytes() == frozen_before
    print(f"DISC_CLOSURE_WRITTEN terminal={terminal_count} pending={pending_count} pins={len(pins['sources'])}")


if __name__ == "__main__":
    main()
