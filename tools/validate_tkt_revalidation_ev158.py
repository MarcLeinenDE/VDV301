#!/usr/bin/env python3
"""EV-158: fail-closed TicketingService V1.0 finding revalidation evidence.

Revalidates frozen TKT-001..TKT-009 against the exact official VDV 301-2-9
V1.0 PDF, two official upstream release contexts carrying different
IBIS-IP_TicketInformationService_V1.0.xsd blobs, and executable XSD behaviour.
The validator is read-only with respect to repository content.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Iterable

from lxml import etree

PDF_SHA256 = "96241226c7a25b0384527dd3de5fcd9448c8e75f38bfb4ffd7b607680bfc6b43"
PDF_SIZE = 627099
PDF_PAGES = 16
PDF_TEXT_SHA256 = "8f23aa2b8c7c12b601ca603a4154624c66989acf36642ae64cf119ef0b268ca8"
PDF_URL = "https://www.vdv.de/301-2-9sds-v1-0.pdfx"

UPSTREAM = {
    "v1_0_tag_object": "ef38d3babebfbb72e6bcdc42c7026e13bab77f69",
    "v1_0_commit": "f5b53785f703e898632603eec3bfa3555a79fdba",
    "v1_0_tree": "729bbe3270e52fed3e0641466048a745d5a09b32",
    "v1_0_ticket_blob": "017ca64666e25d757fc0cde1f1be817f06a743fc",
    "v1_0_common_blob": "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c",
    "v1_0_enums_blob": "a9bea5bc73003ed91ded8519db06c32c4067831d",
    "v1_0_aggregate_blob": "41289eaed2674a169fdf77a10a2eff293c76d5c4",
    "v2_0_commit": "f2569a91f0a7c737a0ca7c0280b28ad223d7ee08",
    "v2_0_tree": "11daf0ebb3b26745c036ee19a547ad16d39f922c",
    "v2_0_ticket_blob": "3fda66d872ab0d1c511247f13e715cf3ad56afe7",
    "v2_0_common_v1_blob": "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c",
    "v2_0_enums_v1_blob": "a9bea5bc73003ed91ded8519db06c32c4067831d",
}

EXPECTED_BLOBS = {
    "audit_registry/finding_inventory_frozen_2026-09-03.json": "02fe0d5f71f2b2674319d37f970ecd2b5bfe27cf",
    "audit_registry/finding_revalidation_registry_v0.1.json": "287e3bbcf4130567b288b1d039e8f576b668012b",
    "00_START_HERE/CURRENT_STATE.json": "a911f050fa5e7affc3d03ec9f2b21c68c848d364",
    "audit_registry/pdf_source_registry_v0.1.json": "d3471e1cef9b099dc8764a3ee8bf234b9a658ce8",
    "docs/pdf_xsd_semantic_audit/FINDING_EVIDENCE_GATE.md": "969cce8b14b50ded2ca5eb745674b894428ecf1a",
    "docs/pdf_xsd_semantic_audit/TICKETING_SERVICE_FINDINGS_REGISTER_ADDENDUM.md": "5f526763b2c68beb58b40922b52b6f0c7c9b554b",
    "IBIS-IP_TicketInformationService_V1.0.xsd": "3fda66d872ab0d1c511247f13e715cf3ad56afe7",
    "IBIS-IP_common_V1.0.xsd": "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c",
    "IBIS-IP_Enumerations_V1.0.xsd": "a9bea5bc73003ed91ded8519db06c32c4067831d",
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

XS = "http://www.w3.org/2001/XMLSchema"
NS = {"xs": XS}
TARGETS = tuple(f"TKT-{i:03d}" for i in range(1, 10))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)
    print(f"OK  {message}")


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def pdf_page_count(pdf: Path) -> int:
    done = subprocess.run(
        ["pdfinfo", str(pdf)], check=True, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    for line in done.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise AssertionError("pdfinfo did not expose page count")


def page_text(pdf: Path, page: int) -> str:
    done = subprocess.run(
        ["pdftotext", "-f", str(page), "-l", str(page), "-layout", str(pdf), "-"],
        check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return done.stdout.decode("utf-8", errors="replace")


def flat_text(text: str) -> str:
    # PDF line wrapping may split visible tokens such as CardApplicationIn- / formation.
    dehyphenated = re.sub(r"-\s+", "", text)
    return "".join(dehyphenated.split())


def parse_xsd(path: Path) -> etree._ElementTree:
    return etree.parse(str(path))


def global_elements(tree: etree._ElementTree) -> dict[str, str | None]:
    root = tree.getroot()
    out: dict[str, str | None] = {}
    for el in root.xpath("./xs:element", namespaces=NS):
        out[el.get("name")] = el.get("type")
    return out


def complex_type_names(tree: etree._ElementTree) -> set[str]:
    return set(tree.xpath("./xs:complexType/@name", namespaces=NS))


def sequence_names(tree: etree._ElementTree, type_name: str) -> list[str]:
    return tree.xpath(
        f"./xs:complexType[@name='{type_name}']/xs:sequence/xs:element/@name",
        namespaces=NS,
    )


def choice_names(tree: etree._ElementTree, type_name: str) -> list[str]:
    return tree.xpath(
        f"./xs:complexType[@name='{type_name}']/xs:choice/xs:element/@name",
        namespaces=NS,
    )


def group_sequence_names(tree: etree._ElementTree, group_name: str) -> list[str]:
    return tree.xpath(
        f"./xs:group[@name='{group_name}']/xs:sequence/xs:element/@name",
        namespaces=NS,
    )


def validate_xml(schema: etree.XMLSchema, xml: str) -> tuple[bool, str]:
    doc = etree.fromstring(xml.encode("utf-8"))
    valid = schema.validate(doc)
    messages = " | ".join(e.message for e in schema.error_log)
    return valid, messages


def require_valid(schema: etree.XMLSchema, xml: str, label: str) -> None:
    valid, messages = validate_xml(schema, xml)
    require(valid, f"{label} validates" + (f" [{messages}]" if not valid else ""))


def require_invalid(schema: etree.XMLSchema, xml: str, label: str, expected: Iterable[str] = ()) -> str:
    valid, messages = validate_xml(schema, xml)
    require(not valid, f"{label} is rejected")
    for token in expected:
        require(token in messages, f"{label} rejection mentions {token!r}: {messages}")
    return messages


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
    old_dir = Path(args.upstream_v10_dir).resolve()
    later_dir = Path(args.upstream_v20_dir).resolve()
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    # 1) Exact audit prestate / authority.
    for rel, expected in EXPECTED_BLOBS.items():
        p = root / rel
        require(p.is_file(), f"authority/prestate file exists: {rel}")
        observed = git_blob_sha(p.read_bytes())
        require(observed == expected, f"exact blob {rel} = {observed}")

    registry = load(root / "audit_registry/finding_revalidation_registry_v0.1.json")
    entries = registry["inventory"]["entries"]
    by_id = {e["finding_id"]: e for e in entries}
    terminal = sum(e.get("revalidation_state") in TERMINAL_STATES for e in entries)
    pending = sum(e.get("revalidation_state") == "pending" for e in entries)
    first_pending = next(e["finding_id"] for e in entries if e.get("revalidation_state") == "pending")
    require((terminal, pending) == (146, 46), f"pre-TKT counts = {terminal}/{pending}")
    require(first_pending == "TKT-001", "pre-TKT first pending is TKT-001")
    require(registry.get("next_revalidation_block") == "TKT", "registry next block is TKT")
    for fid in TARGETS:
        require(by_id[fid].get("revalidation_state") == "pending", f"{fid} remains pending before EV-158")
        require(by_id[fid].get("terminal_state_source") is None, f"{fid} has no premature terminal source")

    audit_state = load(root / "00_START_HERE/CURRENT_STATE.json")["audit"]
    require(audit_state.get("finding_revalidation_completed_findings") == 146,
            "CURRENT_STATE terminal count is 146")
    require(audit_state.get("finding_revalidation_pending_findings") == 46,
            "CURRENT_STATE pending count is 46")
    require(audit_state.get("finding_revalidation_next_block") == "TKT",
            "CURRENT_STATE next block is TKT")

    addendum = (root / "docs/pdf_xsd_semantic_audit/TICKETING_SERVICE_FINDINGS_REGISTER_ADDENDUM.md").read_text(encoding="utf-8")
    for fid in TARGETS:
        require(fid in addendum, f"canonical TKT addendum contains {fid}")
    for token in (
        "017ca64666e25d757fc0cde1f1be817f06a743fc",
        "3fda66d872ab0d1c511247f13e715cf3ad56afe7",
        "select by release_context/schema_revision, not version alone",
        "TicketingService.* only",
        "PDF: TimeStamp -> DefaultLanguage",
        "XSD: DefaultLanguage -> TimeStamp",
        "PDF: CardApplicationInformation",
        "XSD: CardApplikationInformation",
        "PDF: TicketingSevice",
    ):
        require(token in addendum, f"canonical TKT addendum preserves evidence token: {token}")

    # 2) Exact official PDF bytes and page-context checks.
    require(pdf.is_file(), "official TicketingService V1.0 PDF exists")
    pdf_bytes = pdf.read_bytes()
    require(pdf_bytes.startswith(b"%PDF-"), "official source is a PDF")
    require(hashlib.sha256(pdf_bytes).hexdigest() == PDF_SHA256, f"PDF SHA-256 = {PDF_SHA256}")
    require(len(pdf_bytes) == PDF_SIZE, f"PDF size = {PDF_SIZE}")
    require(pdf_page_count(pdf) == PDF_PAGES, f"PDF page count = {PDF_PAGES}")
    full_text = subprocess.run(
        ["pdftotext", "-layout", str(pdf), "-"], check=True,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    ).stdout
    require(hashlib.sha256(full_text).hexdigest() == PDF_TEXT_SHA256,
            f"pdftotext byte hash = {PDF_TEXT_SHA256}")

    source_registry = load(root / "audit_registry/pdf_source_registry_v0.1.json")
    sources = {s["source_id"]: s for s in source_registry.get("sources", [])}
    src = sources["TICKETING_V1.0"]
    require(src.get("official_url") == PDF_URL, "official Ticketing V1.0 PDF URL unchanged")

    p7 = flat_text(page_text(pdf, 7))
    p8 = flat_text(page_text(pdf, 8))
    p9 = flat_text(page_text(pdf, 9))
    p10 = flat_text(page_text(pdf, 10))
    p11 = flat_text(page_text(pdf, 11))
    p12 = flat_text(page_text(pdf, 12))

    require("GetValidationResult" in p7 and "TicketingService.ValidationResultStructure" in p7,
            "PDF page 7 overview assigns GetValidationResult response to TicketingService.ValidationResultStructure")
    require("UnsubscribeValidationResult" in p8 and "SubscribeResponseStructure" in p8,
            "PDF page 8 assigns UnsubscribeValidationResult response to SubscribeResponseStructure")
    require("TimeStamp" in p9 and "DefaultLanguage" in p9 and p9.index("TimeStamp") < p9.index("DefaultLanguage"),
            "PDF page 9 lists TimeStamp before DefaultLanguage")
    require("TicketingSevice.GetTariffInformationResponseDataStructure" in p9,
            "PDF page 9 visibly carries TicketingSevice typo")
    require("TicketInformationService.Validation.GetDataRequest" in p10,
            "PDF page 10 carries TicketInformationService.Validation.GetDataRequest heading")
    require("CardApplicationInformation" in p11,
            "PDF page 11 visibly carries CardApplicationInformation spelling")
    require("TicketingService.GetValidationResultResponseStructure" in p12 and "TimeStamp" in p12 and "ValidationResult" in p12,
            "PDF page 12 detailed table labels outer response structure while listing inner result fields")

    # 3) Official upstream release contexts and exact file identities.
    old_ticket = old_dir / "IBIS-IP_TicketInformationService_V1.0.xsd"
    old_common = old_dir / "IBIS-IP_common_V1.0.xsd"
    old_enums = old_dir / "IBIS-IP_Enumerations_V1.0.xsd"
    old_aggregate = old_dir / "IBIS_IP_V1.0.xsd"
    later_ticket = later_dir / "IBIS-IP_TicketInformationService_V1.0.xsd"
    later_common = later_dir / "IBIS-IP_common_V1.0.xsd"
    later_enums = later_dir / "IBIS-IP_Enumerations_V1.0.xsd"

    upstream_files = (
        (old_ticket, UPSTREAM["v1_0_ticket_blob"]),
        (old_common, UPSTREAM["v1_0_common_blob"]),
        (old_enums, UPSTREAM["v1_0_enums_blob"]),
        (old_aggregate, UPSTREAM["v1_0_aggregate_blob"]),
        (later_ticket, UPSTREAM["v2_0_ticket_blob"]),
        (later_common, UPSTREAM["v2_0_common_v1_blob"]),
        (later_enums, UPSTREAM["v2_0_enums_v1_blob"]),
    )
    for p, expected in upstream_files:
        require(p.is_file(), f"materialized upstream file exists: {p}")
        observed = git_blob_sha(p.read_bytes())
        require(observed == expected, f"upstream blob {p.name} = {observed}")

    require(old_ticket.read_bytes() != later_ticket.read_bytes(),
            "same TicketInformationService V1.0 path has distinct official release bytes")
    require((root / "IBIS-IP_TicketInformationService_V1.0.xsd").read_bytes() == later_ticket.read_bytes(),
            "current audit TicketInformationService V1.0 equals official VDV-301-2.0 revision")
    require(old_common.read_bytes() == later_common.read_bytes(),
            "Common V1.0 dependency is identical across both release contexts")
    require(old_enums.read_bytes() == later_enums.read_bytes(),
            "Enumerations V1.0 dependency is identical across both release contexts")

    old_tree = parse_xsd(old_ticket)
    later_tree = parse_xsd(later_ticket)
    common_tree = parse_xsd(later_common)
    old_schema = etree.XMLSchema(old_tree)
    later_schema = etree.XMLSchema(later_tree)
    print("OK  compiled both exact official TicketInformationService V1.0 release-context schemas")

    old_globals = global_elements(old_tree)
    later_globals = global_elements(later_tree)
    require(len(old_globals) == 0, "VDV-301-1.0 service-file revision has no global TicketingService operation roots")
    expected_later_roots = {
        "TicketingService.SetRazziaRequest",
        "TicketingService.GetTariffInformationResponse",
        "TicketingService.RetrieveTariffInformationRequest",
        "TicketingService.RetrieveTariffInformationResponse",
        "TicketingService.ValidateTicketRequest",
        "TicketingService.ValidateTicketResponse",
        "TicketingService.GetValidationResult",
    }
    require(set(later_globals) == expected_later_roots,
            "VDV-301-2.0 service-file revision exposes the expected seven TicketingService global roots")
    aggregate_text = old_aggregate.read_text(encoding="utf-8")
    require("TicketingService" in aggregate_text,
            "VDV-301-1.0 aggregate supplies TicketingService release context outside the old service file")

    # 4) TKT-002: filename token is not an executable XML service alias.
    for label, tree in (("old", old_tree), ("later", later_tree)):
        names = set(tree.xpath("./xs:element/@name | ./xs:complexType/@name | ./xs:group/@name", namespaces=NS))
        require(not any(n.startswith("TicketInformationService") for n in names),
                f"{label} service revision exposes no TicketInformationService.* schema identity")
    require(all(name.startswith("TicketingService.") for name in later_globals),
            "later executable global operation identity is TicketingService.* only")

    # 5) TKT-003: wrong unsubscribe response type name, but no XML-shape delta.
    subscribe_choice = choice_names(common_tree, "SubscribeResponseStructure")
    unsubscribe_choice = choice_names(common_tree, "UnsubscribeResponseStructure")
    require(subscribe_choice == ["Active", "OperationErrorMessage"],
            "Common V1.0 SubscribeResponseStructure = Active | OperationErrorMessage")
    require(unsubscribe_choice == ["Active", "OperationErrorMessage"],
            "Common V1.0 UnsubscribeResponseStructure = Active | OperationErrorMessage")
    require(subscribe_choice == unsubscribe_choice,
            "SubscribeResponseStructure and UnsubscribeResponseStructure are structurally identical in Common V1.0")

    # 6) TKT-004: exact ValidateTicket root/type is executable; PDF heading alias is rejected.
    validate_req = """<TicketingService.ValidateTicketRequest>
      <CardType>
        <CardSerialNumber><Value>SERIAL1</Value></CardSerialNumber>
        <CardTypeID><Value>TYPE1</Value></CardTypeID>
      </CardType>
      <NumberOfCardTicketDataBlocks><Value>1</Value></NumberOfCardTicketDataBlocks>
      <CardTicketDataBlock>
        <CardTicketDataID><Value>1</Value></CardTicketDataID>
        <CardTicketDataLength><Value>1</Value></CardTicketDataLength>
        <CardTicketData><Value>1</Value></CardTicketData>
      </CardTicketDataBlock>
    </TicketingService.ValidateTicketRequest>"""
    require(later_globals.get("TicketingService.ValidateTicketRequest") == "TicketingService.ValidateTicketRequestStructure",
            "XSD maps TicketingService.ValidateTicketRequest to its exact request structure")
    require_valid(later_schema, validate_req, "exact TicketingService.ValidateTicketRequest sample")
    wrong_validate_req = validate_req.replace("TicketingService.ValidateTicketRequest", "TicketInformationService.Validation.GetDataRequest")
    require_invalid(later_schema, wrong_validate_req, "PDF-heading ValidateTicket alias sample")

    # 7) TKT-005 and TKT-007: outer response wrapper vs inner field owner.
    require(later_globals.get("TicketingService.GetValidationResult") == "TicketingService.GetValidationResultResponseStructure",
            "GetValidationResult global root maps to GetValidationResultResponseStructure")
    later_types = complex_type_names(later_tree)
    require("TicketingService.ValidationResultStructure" not in later_types,
            "XSD has no TicketingService.ValidationResultStructure type from PDF overview")
    require(choice_names(later_tree, "TicketingService.GetValidationResultResponseStructure") == ["ValidationResultData", "OperationErrorMessage"],
            "outer GetValidationResultResponseStructure is a choice wrapper")
    require(sequence_names(later_tree, "TicketingService.ValidationResultDataStructure") == ["TimeStamp", "ValidationResult"],
            "TimeStamp and ValidationResult belong to TicketingService.ValidationResultDataStructure")
    validation_result = """<TicketingService.GetValidationResult>
      <ValidationResultData>
        <TimeStamp><Value>2026-09-13T12:00:00Z</Value></TimeStamp>
        <ValidationResult>valid</ValidationResult>
      </ValidationResultData>
    </TicketingService.GetValidationResult>"""
    require_valid(later_schema, validation_result, "exact GetValidationResult nested response sample")

    # 8) TKT-006: XSD sequence is DefaultLanguage -> TimeStamp; validation engine enforces it.
    tariff_seq = later_tree.xpath(
        "./xs:complexType[@name='TicketingService.GetTariffInformationResponseDataStructure']/xs:sequence/*",
        namespaces=NS,
    )
    tariff_head = [node.get("name") if node.tag == f"{{{XS}}}element" else f"group:{node.get('ref')}" for node in tariff_seq]
    require(tariff_head[:3] == ["DefaultLanguage", "TimeStamp", "group:TariffInformationGroup"],
            "XSD tariff response order begins DefaultLanguage -> TimeStamp -> TariffInformationGroup")

    correct_prefix = """<TicketingService.GetTariffInformationResponse>
      <TicketingService.GetTariffInformationResponseData>
        <DefaultLanguage><Value>de</Value></DefaultLanguage>
        <TimeStamp><Value>2026-09-13T12:00:00Z</Value></TimeStamp>
      </TicketingService.GetTariffInformationResponseData>
    </TicketingService.GetTariffInformationResponse>"""
    wrong_prefix = """<TicketingService.GetTariffInformationResponse>
      <TicketingService.GetTariffInformationResponseData>
        <TimeStamp><Value>2026-09-13T12:00:00Z</Value></TimeStamp>
        <DefaultLanguage><Value>de</Value></DefaultLanguage>
      </TicketingService.GetTariffInformationResponseData>
    </TicketingService.GetTariffInformationResponse>"""
    correct_prefix_errors = require_invalid(
        later_schema, correct_prefix, "correct-order tariff prefix (intentionally incomplete)", expected=("TripRef",)
    )
    wrong_prefix_errors = require_invalid(
        later_schema, wrong_prefix, "PDF-order tariff prefix", expected=("DefaultLanguage",)
    )
    require("TripRef" in correct_prefix_errors and "DefaultLanguage" in wrong_prefix_errors,
            "validation engine reaches TariffInformationGroup only for XSD order and rejects PDF order at the first field")

    # 9) TKT-008: exact schema spelling is executable; PDF spelling is rejected.
    require(group_sequence_names(later_tree, "CardApplikationValidation") == ["CardApplStatusCode", "CardApplikationInformation"],
            "CardApplikationValidation group uses exact CardApplikationInformation spelling")
    validate_resp = """<TicketingService.ValidateTicketResponse>
      <TicketingService.ValidationResponseData>
        <TimeStamp><Value>2026-09-13T12:00:00Z</Value></TimeStamp>
        <GlobalCardStatus><GlobalCardStausID><Value>1</Value></GlobalCardStausID></GlobalCardStatus>
        <CardType>
          <CardSerialNumber><Value>SERIAL1</Value></CardSerialNumber>
          <CardTypeID><Value>TYPE1</Value></CardTypeID>
        </CardType>
        <CardApplStatusCode><Value>1</Value></CardApplStatusCode>
        <CardApplikationInformation>
          <CardApplInformationLength><Value>1</Value></CardApplInformationLength>
          <CardApplInformationData><Value>1</Value></CardApplInformationData>
        </CardApplikationInformation>
        <CardValidationCode><Value>1</Value></CardValidationCode>
        <CardTicketData>
          <CardTicketDataID><Value>1</Value></CardTicketDataID>
          <CardTicketDataLength><Value>1</Value></CardTicketDataLength>
          <CardTicketData><Value>1</Value></CardTicketData>
        </CardTicketData>
      </TicketingService.ValidationResponseData>
    </TicketingService.ValidateTicketResponse>"""
    require_valid(later_schema, validate_resp, "ValidateTicketResponse sample with CardApplikationInformation")
    wrong_spelling = validate_resp.replace("CardApplikationInformation", "CardApplicationInformation")
    require_invalid(later_schema, wrong_spelling, "PDF-spelling CardApplicationInformation sample", expected=("CardApplikationInformation",))

    # 10) TKT-009: no executable TicketingSevice alias.
    all_schema_names = set(later_tree.xpath("./xs:element/@name | ./xs:complexType/@name | ./xs:group/@name", namespaces=NS))
    require(not any(n.startswith("TicketingSevice") for n in all_schema_names),
            "XSD exposes no TicketingSevice alias")
    wrong_service = validate_req.replace("TicketingService.ValidateTicketRequest", "TicketingSevice.ValidateTicketRequest")
    require_invalid(later_schema, wrong_service, "TicketingSevice typo root sample")

    # Compute expected handoff without mutating the registry.
    remaining_pending = [
        e["finding_id"] for e in entries
        if e.get("revalidation_state") == "pending" and e["finding_id"] not in TARGETS
    ]
    require(len(remaining_pending) == 37, f"post-TKT pending count would be {len(remaining_pending)}")
    next_finding = remaining_pending[0]
    next_block = next_finding.split("-", 1)[0]

    recommendations = {
        "TKT-001": {
            "recommended_terminal_state": "context_verified",
            "finding_result": "release_context_provenance_confirmed",
            "rationale": "The same V1.0 path carries distinct official blobs and executable surfaces in VDV-301-1.0 versus VDV-301-2.0; resolution must include release context/schema revision.",
        },
        "TKT-002": {
            "recommended_terminal_state": "contextual_not_defect",
            "finding_result": "filename_not_executable_alias",
            "rationale": "TicketInformationService is a filename token; executable schema identities are TicketingService.*. This is naming context, not an XSD payload defect.",
        },
        "TKT-003": {
            "recommended_terminal_state": "context_verified",
            "finding_result": "pdf_type_label_discrepancy_no_xml_shape_delta",
            "rationale": "The PDF assigns SubscribeResponseStructure to UnsubscribeValidationResult, while Common V1.0 defines the unsubscribe type as UnsubscribeResponseStructure. Both types have the same Active/OperationErrorMessage choice, so the documentation type-name error creates no XML-shape delta.",
        },
        "TKT-004": {
            "recommended_terminal_state": "executable_confirmed",
            "finding_result": "pdf_heading_alias_rejected",
            "rationale": "The exact TicketingService.ValidateTicketRequest root validates; the PDF heading TicketInformationService.Validation.GetDataRequest is not an executable root and is rejected.",
        },
        "TKT-005": {
            "recommended_terminal_state": "context_verified",
            "finding_result": "pdf_response_type_label_discrepancy",
            "rationale": "The PDF overview names TicketingService.ValidationResultStructure, which does not exist; the executable root maps to TicketingService.GetValidationResultResponseStructure.",
        },
        "TKT-006": {
            "recommended_terminal_state": "executable_confirmed",
            "finding_result": "sequence_order_enforced",
            "rationale": "The exact XSD sequence is DefaultLanguage before TimeStamp. Validation reaches TripRef with the XSD-order prefix but rejects the PDF-order prefix at DefaultLanguage.",
        },
        "TKT-007": {
            "recommended_terminal_state": "context_verified",
            "finding_result": "pdf_detailed_heading_targets_outer_wrapper",
            "rationale": "The PDF detailed table labels the outer response wrapper while its listed TimeStamp/ValidationResult fields belong to TicketingService.ValidationResultDataStructure.",
        },
        "TKT-008": {
            "recommended_terminal_state": "executable_confirmed",
            "finding_result": "schema_spelling_enforced",
            "rationale": "A response using CardApplikationInformation validates; replacing it with the PDF spelling CardApplicationInformation is rejected by the exact XSD.",
        },
        "TKT-009": {
            "recommended_terminal_state": "context_verified",
            "finding_result": "pdf_service_label_typo_no_alias",
            "rationale": "The official PDF visibly uses TicketingSevice in labels, while the XSD exposes no such alias; executable service identity remains TicketingService.",
        },
    }

    result = {
        "evidence_id": "EV-158",
        "result": "PASS",
        "scope": list(TARGETS),
        "prestate": {
            "terminal": terminal,
            "pending": pending,
            "first_pending": first_pending,
            "next_block": registry.get("next_revalidation_block"),
        },
        "expected_poststate": {
            "terminal": terminal + len(TARGETS),
            "pending": len(remaining_pending),
            "first_pending": next_finding,
            "next_block": next_block,
        },
        "pdf": {
            "source_id": "TICKETING_V1.0",
            "official_url": PDF_URL,
            "sha256": PDF_SHA256,
            "size_bytes": PDF_SIZE,
            "pages": PDF_PAGES,
            "pdftotext_sha256": PDF_TEXT_SHA256,
            "visually_reviewed_physical_pages": [7, 8, 9, 10, 11, 12],
        },
        "upstream_authority": UPSTREAM,
        "findings": recommendations,
        "xsd_mutation": "none",
        "frozen_inventory_mutation": "none",
    }
    result_path = out / "ev158_result.json"
    result_path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    print(f"PASS EV-158 -> {result_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
