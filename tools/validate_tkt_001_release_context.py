#!/usr/bin/env python3
"""TKT-001: exact original aggregate vs later self-contained official service.

No production schema mutations or synthetic historical roots. All 12 historical
files are fetched by immutable upstream commit and checked against the exact
official V1.0 tree before compilation. The later selected service uses exact
Common/Enumerations V1.0 dependencies. This is XML schema evidence only.
"""
from pathlib import Path
import tempfile
import urllib.request
from lxml import etree
from validate_sub_001_unsubscribe_type_names import blob, require

ROOT = Path(__file__).resolve().parents[1]
NS = {"xs": "http://www.w3.org/2001/XMLSchema"}
COMMIT = "f5b53785f703e898632603eec3bfa3555a79fdba"
FILE = "IBIS-IP_TicketInformationService_V1.0.xsd"
AGG = "IBIS_IP_V1.0.xsd"
OLD = {
    "IBIS-IP_CustomerInformationService_V1.0.xsd": "7a95fc03c06c8c84d078bf06d18ef5873a15c215",
    "IBIS-IP_DeviceManagementService_V1.0.xsd": "602a963f91000d0d39e3c271bacb3c7aba73e6d4",
    "IBIS-IP_Enumerations_V1.0.xsd": "a9bea5bc73003ed91ded8519db06c32c4067831d",
    "IBIS-IP_JourneyInformationService_V1.0.xsd": "1ee4d7aeb15f3269c5335313be9e214bdb519d2e",
    "IBIS-IP_LocationService_V1.0.xsd": "2a653ba7d35a6e91b5fd691eb5c606160192ab9e",
    "IBIS-IP_NetworkLocationService_V1.0.xsd": "bd1f83df2dfa83f36666a3ab3df4457242b387e9",
    "IBIS-IP_PassengerCountingService_V1.0.xsd": "600a3ee6290c630a4435fb06ca9803dabaceb788",
    "IBIS-IP_SystemDocumentationService_v1.0.xsd": "8995c4a230bf81d5e47b9313ee7725ff3cd4b7b5",
    "IBIS-IP_SystemManagementService_V1.0.xsd": "85390f99d6c19c88923ed9a5fc8a5706137708af",
    FILE: "017ca64666e25d757fc0cde1f1be817f06a743fc",
    "IBIS-IP_common_V1.0.xsd": "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c",
    AGG: "41289eaed2674a169fdf77a10a2eff293c76d5c4",
}
LATER = "3fda66d872ab0d1c511247f13e715cf3ad56afe7"
EXPECTED = {
    "TicketingService.SetRazziaRequest": "TicketingService.SetRazziaRequestStructure",
    "TicketingService.GetTariffInformationResponse": "TicketingService.GetTariffInformationResponseStructure",
    "TicketingService.RetrieveTariffInformationRequest": "TicketingService.RetrieveTariffInformationRequestStructure",
    "TicketingService.RetrieveTariffInformationResponse": "TicketingService.GetTariffInformationResponseStructure",
    "TicketingService.ValidateTicketRequest": "TicketingService.ValidateTicketRequestStructure",
    "TicketingService.ValidateTicketResponse": "TicketingService.ValidateTicketResponseStructure",
    "TicketingService.GetValidationResult": "TicketingService.GetValidationResultResponseStructure",
}
ORPHANS = {"TicketingService.SetRazziaResponseStructure", "TicketingService.SetRazziaResponseDataStructure"}


def parse(path):
    return etree.parse(str(path), etree.XMLParser(no_network=True))


def roots(doc):
    return {e.get("name"): e.get("type") for e in doc.xpath("/xs:schema/xs:element", namespaces=NS) if e.get("name", "").startswith("TicketingService.")}


def groups(doc):
    return {e.get("name"): e.get("type") for e in doc.xpath("/xs:schema/xs:group[@name='TicketingServiceGroup']/xs:sequence/xs:element", namespaces=NS)}



def validate_tkt_002_identity(folder, later, aggregate_schema, later_schema):
    """Distinguish a filename token from executable XML names in both profiles."""
    import json
    # Inspect the complete historical dependency family and the selected later
    # service plus its exact pinned Common/Enumerations, not just the root map.
    paths = [folder / filename for filename in OLD]
    paths += [later, ROOT / "IBIS-IP_common_V1.0.xsd",
              ROOT / "IBIS-IP_Enumerations_V1.0.xsd"]
    for path in paths:
        doc = parse(path)
        names = doc.xpath("/xs:schema//@name", namespaces=NS)
        require(not any(name.startswith("TicketInformationService") for name in names),
                f"TKT-002 no filename-derived executable declaration: {path.name}")
    for path in (folder / FILE, folder / AGG, later):
        require(parse(path).getroot().get("targetNamespace") is None,
                f"TKT-002 dot names are unqualified: {path.name}")
    overrides = json.loads((ROOT / "sdk_manifest/routing_overrides_v0.1.json").read_text(encoding="utf-8"))
    matching = [item for item in overrides["aliases"]
                if item.get("schema_filename_token") == "TicketInformationService"
                and item.get("service_version") == "1.0"]
    require(len(matching) == 1 and matching[0].get("public_service_name") == "TicketingService"
            and matching[0].get("kind") == "legacy_alias",
            "TKT-002 exact filename routing metadata, no XML alias inferred")
    error = "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>"
    samples = {
        "SetRazziaRequest": "<TicketInformationRazziaStatus>razzia</TicketInformationRazziaStatus>",
        "GetTariffInformationResponse": error,
        "RetrieveTariffInformationRequest": "".join(
            f"<{name}><Value>1</Value></{name}>" for name in ("TripRef", "LineRef", "StopRef")),
        "RetrieveTariffInformationResponse": error,
        "ValidateTicketRequest": (
            "<CardType><CardSerialNumber><Value>SERIAL1</Value></CardSerialNumber>"
            "<CardTypeID><Value>TYPE1</Value></CardTypeID></CardType>"
            "<NumberOfCardTicketDataBlocks><Value>1</Value></NumberOfCardTicketDataBlocks>"
            "<CardTicketDataBlock><CardTicketDataID><Value>1</Value></CardTicketDataID>"
            "<CardTicketDataLength><Value>1</Value></CardTicketDataLength>"
            "<CardTicketData><Value>1</Value></CardTicketData></CardTicketDataBlock>"),
        "ValidateTicketResponse": error,
        "GetValidationResult": (
            "<ValidationResultData><TimeStamp><Value>2026-11-28T07:00:00Z</Value></TimeStamp>"
            "<ValidationResult>valid</ValidationResult></ValidationResultData>"),
    }
    require({"TicketingService." + name for name in samples} == set(EXPECTED),
            "TKT-002 all seven global roots covered")
    xsi_type = "{http://www.w3.org/2001/XMLSchema-instance}type"
    for profile, schema in (("original aggregate", aggregate_schema), ("later service", later_schema)):
        for suffix, payload in samples.items():
            root = "TicketingService." + suffix
            node = etree.fromstring(f"<{root}>{payload}</{root}>".encode())
            require(schema.validate(node), f"TKT-002 {profile}: canonical root {root} accepted")
            node.tag = "TicketInformationService." + suffix
            require(not schema.validate(node), f"TKT-002 {profile}: filename alias root rejected {node.tag}")
            require(bool(schema.error_log) and all(e.type_name == "SCHEMAV_CVC_ELT_1" for e in schema.error_log),
                    "TKT-002 rejection is missing global root, not payload shape")
            node.tag = root
            node.set(xsi_type, EXPECTED[root])
            require(schema.validate(node), f"TKT-002 {profile}: exact xsi:type accepted {EXPECTED[root]}")
            node.set(xsi_type, EXPECTED[root].replace("TicketingService.", "TicketInformationService.", 1))
            require(not schema.validate(node), f"TKT-002 {profile}: filename alias xsi:type rejected")
            require(bool(schema.error_log) and all(e.type_name == "SCHEMAV_CVC_ELT_4_2" for e in schema.error_log),
                    "TKT-002 rejection is unresolved type QName, not payload shape")
    print("PASSED TKT-002: 14 canonical roots + 14 exact xsi:type positives; 14 missing-root + 14 unresolved-type alias negatives")



def validate_tkt_003_response_types(folder, later, aggregate_schema, later_schema):
    """Same content model, distinct named types; no synthetic production roots."""
    names = ("SubscribeResponse", "UnsubscribeResponse")
    for common in (folder / "IBIS-IP_common_V1.0.xsd",
                   ROOT / "IBIS-IP_common_V1.0.xsd"):
        doc = parse(common)
        for root in names:
            typ = doc.xpath("/xs:schema/xs:complexType[@name=$name]",
                            namespaces=NS, name=root + "Structure")
            require(len(typ) == 1, "TKT-003 exact type declaration")
            require(len(typ[0]) == 1 and typ[0][0].tag == "{http://www.w3.org/2001/XMLSchema}choice"
                    and not typ[0][0].attrib, "TKT-003 one required choice")
            require([dict(e.attrib) for e in typ[0][0]] == [
                {"name": "Active", "type": "IBIS-IP.boolean"},
                {"name": "OperationErrorMessage", "type": "IBIS-IP.string"}],
                "TKT-003 identical choice branches and cardinalities")
    agg = parse(folder / AGG)
    for root in names:
        require(agg.xpath("/xs:schema/xs:element[@name=$name]/@type",
                          namespaces=NS, name=root) == [root + "Structure"],
                "TKT-003 original aggregate exact generic root mapping")
    # Later isolated Ticketing profile has no generic global response roots.
    # A test-only wrapper exposes its existing types without inventing production declarations.
    probe = ('<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
             f'<xs:include schemaLocation="{later.name}"/>'
             + "".join(f'<xs:element name="{root}" type="{root}Structure"/>' for root in names)
             + '</xs:schema>')
    test_schema = etree.XMLSchema(etree.fromstring(
        probe.encode(), base_url=(later.parent / "_tkt003_probe.xsd").as_uri()))
    active = "<Active><Value>true</Value></Active>"
    error = "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>"
    xsi = "{http://www.w3.org/2001/XMLSchema-instance}type"
    positive = wrong_type = wrong_choice = missing_root = 0
    for root in names:
        node = etree.fromstring(f"<{root}>{active}</{root}>".encode())
        require(not later_schema.validate(node) and bool(later_schema.error_log)
                and all(e.type_name == "SCHEMAV_CVC_ELT_1" for e in later_schema.error_log),
                "TKT-003 isolated later service has no generic global root " + root)
        missing_root += 1
    for profile, schema in (("original aggregate", aggregate_schema),
                            ("later type probe only", test_schema)):
        for root in names:
            other = next(n for n in names if n != root)
            for payload in (active, error):
                node = etree.fromstring(f"<{root}>{payload}</{root}>".encode())
                require(schema.validate(node), f"TKT-003 {profile} {root} implicit type PASS")
                positive += 1
                node.set(xsi, root + "Structure")
                require(schema.validate(node), f"TKT-003 {profile} {root} exact explicit type PASS")
                positive += 1
                node.set(xsi, other + "Structure")
                require(not schema.validate(node) and bool(schema.error_log)
                        and all(e.type_name == "SCHEMAV_CVC_ELT_4_3" for e in schema.error_log),
                        f"TKT-003 {profile} {root} sibling type is not validly derived")
                wrong_type += 1
            for payload in ("", active + error):
                node = etree.fromstring(f"<{root}>{payload}</{root}>".encode())
                require(not schema.validate(node) and bool(schema.error_log)
                        and all(e.type_name == "SCHEMAV_ELEMENT_CONTENT" for e in schema.error_log),
                        f"TKT-003 {profile} {root} required exclusive choice")
                wrong_choice += 1
    require((positive, wrong_type, wrong_choice, missing_root) == (16, 8, 8, 2),
            "TKT-003 expected regression counts")
    print("PASSED TKT-003: 16 positives, 8 sibling xsi:type negatives, 8 exclusive choice negatives, 2 isolated later missing-root negatives")



def validate_tkt_004_pdf_heading(folder, later, aggregate_schema, later_schema, old_schema):
    """Literal PDF heading is distinct from filename aliases; exact profile evidence only."""
    canonical = "TicketingService.ValidateTicketRequest"
    wrong = "TicketInformationService.Validation.GetDataRequest"
    typename = canonical + "Structure"
    for path in (folder / AGG, later):
        doc = parse(path)
        require(doc.xpath("/xs:schema/xs:element[@name=$root]/@type",
                          namespaces=NS, root=canonical) == [typename],
                "TKT-004 authoritative global root/type pair")
    for path in [folder / n for n in OLD] + [later]:
        names = set(parse(path).xpath("/xs:schema//@name", namespaces=NS))
        require(wrong not in names and wrong + "Structure" not in names,
                "TKT-004 no literal PDF heading root or type declaration")
    for path in (folder / FILE, later):
        doc = parse(path)
        members = doc.xpath("/xs:schema/xs:complexType[@name=$name]/xs:sequence/*",
                            namespaces=NS, name=typename)
        require([dict(m.attrib) for m in members] == [
            {"name": "CardType", "type": "CardType"},
            {"name": "CardApplInformation", "type": "CardApplInformations", "minOccurs": "0"},
            {"ref": "CardTicketDataBlocks"}], "TKT-004 exact request member inventory")
        group = doc.xpath("/xs:schema/xs:group[@name='CardTicketDataBlocks']/xs:sequence/xs:element",
                          namespaces=NS)
        require([dict(m.attrib) for m in group] == [
            {"name": "NumberOfCardTicketDataBlocks", "type": "IBIS-IP.unsignedInt"},
            {"name": "CardTicketDataBlock", "type": "CardTicketData", "maxOccurs": "unbounded"}],
            "TKT-004 group expands to exact count and block members")
    payload = (
        "<CardType><CardSerialNumber><Value>SERIAL1</Value></CardSerialNumber>"
        "<CardTypeID><Value>TYPE1</Value></CardTypeID></CardType>"
        "<NumberOfCardTicketDataBlocks><Value>1</Value></NumberOfCardTicketDataBlocks>"
        "<CardTicketDataBlock><CardTicketDataID><Value>1</Value></CardTicketDataID>"
        "<CardTicketDataLength><Value>1</Value></CardTicketDataLength>"
        "<CardTicketData><Value>1</Value></CardTicketData></CardTicketDataBlock>")
    xsi = "{http://www.w3.org/2001/XMLSchema-instance}type"
    positive = wrong_root = wrong_type = other_root = isolated = 0
    for profile, schema in (("original aggregate", aggregate_schema),
                            ("later service", later_schema)):
        node = etree.fromstring(f"<{canonical}>{payload}</{canonical}>".encode())
        require(schema.validate(node), f"TKT-004 {profile} exact request PASS")
        positive += 1
        node.tag = wrong
        require(not schema.validate(node) and bool(schema.error_log)
                and all(e.type_name == "SCHEMAV_CVC_ELT_1" for e in schema.error_log),
                f"TKT-004 {profile} exact PDF heading missing global root")
        wrong_root += 1
        node.tag = canonical
        node.set(xsi, typename)
        require(schema.validate(node), f"TKT-004 {profile} exact explicit type PASS")
        positive += 1
        node.set(xsi, wrong + "Structure")
        require(not schema.validate(node) and bool(schema.error_log)
                and all(e.type_name == "SCHEMAV_CVC_ELT_4_2" for e in schema.error_log),
                f"TKT-004 {profile} invented PDF type unresolved")
        wrong_type += 1
        del node.attrib[xsi]
        for alias in ("TicketInformationService.ValidateTicketRequest",
                      "TicketingService.Validation.GetDataRequest"):
            node.tag = alias
            require(not schema.validate(node) and bool(schema.error_log)
                    and all(e.type_name == "SCHEMAV_CVC_ELT_1" for e in schema.error_log),
                    f"TKT-004 {profile} distinct nonliteral alias rejected {alias}")
            other_root += 1
    for root in (canonical, wrong):
        node = etree.fromstring(f"<{root}>{payload}</{root}>".encode())
        require(not old_schema.validate(node) and bool(old_schema.error_log)
                and all(e.type_name == "SCHEMAV_CVC_ELT_1" for e in old_schema.error_log),
                f"TKT-004 isolated original missing both roots {root}")
        isolated += 1
    require((positive, wrong_root, wrong_type, other_root, isolated) == (4, 2, 2, 4, 2),
            "TKT-004 exact regression counts")
    print("PASSED TKT-004: 4 positives, 2 literal PDF-root negatives, 2 invented-type negatives, 4 distinct alias controls, 2 isolated historical controls")



def validate_tkt_005_response_type(folder, later, aggregate_schema, later_schema, old_schema):
    """Distinguish the absent overview type from the real response and nested data types."""
    root = "TicketingService.GetValidationResult"
    outer = "TicketingService.GetValidationResultResponseStructure"
    inner = "TicketingService.ValidationResultDataStructure"
    wrong = "TicketingService.ValidationResultStructure"
    for path in [folder / n for n in OLD] + [later]:
        doc = parse(path)
        require(not doc.xpath("/xs:schema/xs:complexType[@name=$name] | /xs:schema/xs:simpleType[@name=$name]",
                              namespaces=NS, name=wrong),
                f"TKT-005 overview type absent: {path.name}")
    for path in (folder / AGG, later):
        require(parse(path).xpath("/xs:schema/xs:element[@name=$name]/@type",
                                  namespaces=NS, name=root) == [outer],
                "TKT-005 exact global root and outer type")
    for path in (folder / FILE, later):
        doc = parse(path)
        choice = doc.xpath("/xs:schema/xs:complexType[@name=$name]/xs:choice", namespaces=NS, name=outer)
        require(len(choice) == 1 and not choice[0].attrib and
                [dict(e.attrib) for e in choice[0]] == [
                    {"name": "ValidationResultData", "type": inner},
                    {"name": "OperationErrorMessage", "type": "IBIS-IP.string"}],
                "TKT-005 exact mandatory outer choice")
        seq = doc.xpath("/xs:schema/xs:complexType[@name=$name]/xs:sequence", namespaces=NS, name=inner)
        require(len(seq) == 1 and not seq[0].attrib and
                [dict(e.attrib) for e in seq[0]] == [
                    {"name": "TimeStamp", "type": "IBIS-IP.dateTime"},
                    {"name": "ValidationResult", "type": "TicketValidationEnumeration"}],
                "TKT-005 exact inner type; distinct TKT-007 context")
    payloads = (
        "<ValidationResultData><TimeStamp><Value>2026-11-28T07:00:00Z</Value></TimeStamp>"
        "<ValidationResult>valid</ValidationResult></ValidationResultData>",
        "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>",
    )
    xsi = "{http://www.w3.org/2001/XMLSchema-instance}type"
    positive = absent_type = inner_type = isolated = 0
    for profile, schema in (("original aggregate", aggregate_schema), ("later service", later_schema)):
        for payload in payloads:
            node = etree.fromstring(f"<{root}>{payload}</{root}>".encode())
            require(schema.validate(node), f"TKT-005 {profile} implicit outer type PASS")
            positive += 1
            node.set(xsi, outer)
            require(schema.validate(node), f"TKT-005 {profile} exact explicit outer type PASS")
            positive += 1
            node.set(xsi, wrong)
            require(not schema.validate(node) and bool(schema.error_log) and
                    all(e.type_name == "SCHEMAV_CVC_ELT_4_2" for e in schema.error_log),
                    f"TKT-005 {profile} nonexistent PDF type unresolved")
            absent_type += 1
            node.set(xsi, inner)
            # The inner type exists but is not derived from the declared outer type.
            require(not schema.validate(node) and bool(schema.error_log) and
                    "SCHEMAV_CVC_ELT_4_3" in {e.type_name for e in schema.error_log},
                    f"TKT-005 {profile} inner type is not a valid outer substitute")
            inner_type += 1
            del node.attrib[xsi]
            require(not old_schema.validate(node) and bool(old_schema.error_log) and
                    all(e.type_name == "SCHEMAV_CVC_ELT_1" for e in old_schema.error_log),
                    "TKT-005 isolated original service missing root, not type-name defect")
            isolated += 1
    require((positive, absent_type, inner_type, isolated) == (8, 4, 4, 4),
            "TKT-005 exact regression counts")
    print("PASSED TKT-005: 8 positives, 4 absent-type negatives, 4 inner-type substitution controls, 4 isolated historical controls")



def validate_tkt_006_tariff_sequence(folder, later, aggregate_schema, later_schema, old_schema):
    """Complete data payload, not just prefix; both shared response roots and exact profiles."""
    roots_to_check = ("TicketingService.GetTariffInformationResponse",
                      "TicketingService.RetrieveTariffInformationResponse")
    outer = "TicketingService.GetTariffInformationResponseStructure"
    inner = "TicketingService.GetTariffInformationResponseDataStructure"
    data = "TicketingService.GetTariffInformationResponseData"
    for path in (folder / AGG, later):
        doc = parse(path)
        for root in roots_to_check:
            require(doc.xpath("/xs:schema/xs:element[@name=$name]/@type",
                              namespaces=NS, name=root) == [outer],
                    "TKT-006 both roots share the exact outer type")
    for path in (folder / FILE, later):
        doc = parse(path)
        seq = doc.xpath("/xs:schema/xs:complexType[@name=$name]/xs:sequence", namespaces=NS, name=inner)
        require(len(seq) == 1 and not seq[0].attrib and
                [dict(e.attrib) for e in seq[0]] == [
                    {"name": "DefaultLanguage", "type": "IBIS-IP.language"},
                    {"name": "TimeStamp", "type": "IBIS-IP.dateTime"},
                    {"ref": "TariffInformationGroup"}], "TKT-006 mandatory exact sequence")
        choice = doc.xpath("/xs:schema/xs:complexType[@name=$name]/xs:choice", namespaces=NS, name=outer)
        require(len(choice) == 1 and not choice[0].attrib and
                [dict(e.attrib) for e in choice[0]] == [
                    {"name": data, "type": inner},
                    {"name": "OperationErrorMessage", "type": "IBIS-IP.string"}],
                "TKT-006 exact outer choice")
    language = "<DefaultLanguage><Value>de</Value></DefaultLanguage>"
    timestamp = "<TimeStamp><Value>2026-11-28T12:00:00Z</Value></TimeStamp>"
    tail = ("<TripRef><Value>T1</Value></TripRef>"
            "<Line><LineRef><Value>L1</Value></LineRef></Line>"
            "<StopPointTariffInformation><JourneyStopInformation>"
            "<StopRef><Value>S1</Value></StopRef>"
            "<StopName><Value>Stop</Value><Language>de</Language></StopName>"
            "<DisplayContent><LineInformation><LineRef><Value>L1</Value></LineRef></LineInformation>"
            "<Destination><DestinationRef><Value>D1</Value></DestinationRef></Destination>"
            "</DisplayContent></JourneyStopInformation>"
            "<FareZoneInformation><FareZoneID><Value>Z1</Value></FareZoneID></FareZoneInformation>"
            "</StopPointTariffInformation>")
    def payload(root, prefix):
        return etree.fromstring(f"<{root}><{data}>{prefix}{tail}</{data}></{root}>".encode())
    positive = pdf_order = missing = isolated = 0
    for profile, schema in (("original aggregate", aggregate_schema), ("later service", later_schema)):
        for root in roots_to_check:
            require(schema.validate(payload(root, language + timestamp)),
                    f"TKT-006 {profile} {root} complete XSD-order payload PASS")
            positive += 1
            err = etree.fromstring(f"<{root}><OperationErrorMessage><Value>test</Value></OperationErrorMessage></{root}>".encode())
            require(schema.validate(err), f"TKT-006 {profile} {root} error choice unaffected")
            positive += 1
            for prefix, actual, expected, is_pdf in (
                    (timestamp + language, "TimeStamp", "DefaultLanguage", True),
                    (timestamp, "TimeStamp", "DefaultLanguage", False),
                    (language, "TripRef", "TimeStamp", False)):
                require(not schema.validate(payload(root, prefix)),
                        f"TKT-006 {profile} {root} targeted invalid sequence")
                errors = list(schema.error_log)
                require(len(errors) == 1 and errors[0].type_name == "SCHEMAV_ELEMENT_CONTENT"
                        and f"Element '{actual}'" in errors[0].message
                        and f"Expected is ( {expected} )" in errors[0].message,
                        f"TKT-006 {profile} {root} exact sequence error: {errors}")
                if is_pdf:
                    pdf_order += 1
                else:
                    missing += 1
    for root in roots_to_check:
        for prefix in (language + timestamp, timestamp + language):
            require(not old_schema.validate(payload(root, prefix)) and bool(old_schema.error_log)
                    and all(e.type_name == "SCHEMAV_CVC_ELT_1" for e in old_schema.error_log),
                    "TKT-006 isolated original missing global declaration, not order defect")
            isolated += 1
    require((positive, pdf_order, missing, isolated) == (8, 4, 8, 4),
            "TKT-006 expected counts")
    print("PASSED TKT-006: 8 positives, 4 PDF-order negatives, 8 omission controls, 4 isolated historical controls")



def validate_tkt_007_inner_field_ownership(folder, later, aggregate_schema, later_schema, old_schema):
    """Test actual field nesting and inner xsi:type, distinct from TKT-005 overview type."""
    root = "TicketingService.GetValidationResult"
    outer = "TicketingService.GetValidationResultResponseStructure"
    inner = "TicketingService.ValidationResultDataStructure"
    for path in (folder / AGG, later):
        require(parse(path).xpath("/xs:schema/xs:element[@name=$name]/@type",
                                  namespaces=NS, name=root) == [outer],
                "TKT-007 exact root and outer type")
    for path in (folder / FILE, later):
        doc = parse(path)
        choice = doc.xpath("/xs:schema/xs:complexType[@name=$name]/xs:choice", namespaces=NS, name=outer)
        seq = doc.xpath("/xs:schema/xs:complexType[@name=$name]/xs:sequence", namespaces=NS, name=inner)
        require(len(choice) == len(seq) == 1 and not choice[0].attrib and not seq[0].attrib,
                "TKT-007 mandatory outer choice and inner sequence")
        require([dict(e.attrib) for e in choice[0]] == [
                    {"name": "ValidationResultData", "type": inner},
                    {"name": "OperationErrorMessage", "type": "IBIS-IP.string"}],
                "TKT-007 exact outer field ownership")
        require([dict(e.attrib) for e in seq[0]] == [
                    {"name": "TimeStamp", "type": "IBIS-IP.dateTime"},
                    {"name": "ValidationResult", "type": "TicketValidationEnumeration"}],
                "TKT-007 exact inner field ownership")
    stamp = "<TimeStamp><Value>2026-11-28T07:00:00Z</Value></TimeStamp>"
    result = "<ValidationResult>valid</ValidationResult>"
    data = f"<ValidationResultData>{stamp}{result}</ValidationResultData>"
    error = "<OperationErrorMessage><Value>test</Value></OperationErrorMessage>"
    xsi = "{http://www.w3.org/2001/XMLSchema-instance}type"
    def payload(body):
        return etree.fromstring(f"<{root}>{body}</{root}>".encode())
    positive = flattened = wrong_inner = content = isolated = 0
    for profile, schema in (("original aggregate", aggregate_schema), ("later service", later_schema)):
        for body in (data, error):
            require(schema.validate(payload(body)), f"TKT-007 {profile} valid branch")
            positive += 1
        node = payload(data)
        node[0].set(xsi, inner)
        require(schema.validate(node), f"TKT-007 {profile} exact explicit inner type")
        positive += 1
        node[0].set(xsi, outer)
        require(not schema.validate(node) and bool(schema.error_log)
                and all(e.type_name == "SCHEMAV_CVC_ELT_4_3" for e in schema.error_log),
                f"TKT-007 {profile} outer type cannot replace inner type")
        wrong_inner += 1
        node = payload(stamp + result)
        require(not schema.validate(node) and len(schema.error_log) == 1
                and schema.error_log[0].type_name == "SCHEMAV_ELEMENT_CONTENT"
                and "Element 'TimeStamp'" in schema.error_log[0].message
                and "Expected is one of ( ValidationResultData, OperationErrorMessage )" in schema.error_log[0].message,
                f"TKT-007 {profile} flattened fields rejected at outer choice")
        flattened += 1
        for body in ("", data + error, f"<ValidationResultData>{stamp}</ValidationResultData>",
                     f"<ValidationResultData>{result}</ValidationResultData>",
                     f"<ValidationResultData>{result}{stamp}</ValidationResultData>"):
            require(not schema.validate(payload(body)) and bool(schema.error_log)
                    and all(e.type_name == "SCHEMAV_ELEMENT_CONTENT" for e in schema.error_log),
                    f"TKT-007 {profile} mandatory choice/sequence control")
            content += 1
    for body in (data, stamp + result):
        require(not old_schema.validate(payload(body)) and bool(old_schema.error_log)
                and all(e.type_name == "SCHEMAV_CVC_ELT_1" for e in old_schema.error_log),
                "TKT-007 isolated original missing root, distinct from field ownership")
        isolated += 1
    require((positive, flattened, wrong_inner, content, isolated) == (6, 2, 2, 10, 2),
            "TKT-007 expected counts")
    print("PASSED TKT-007: 6 positives, 2 flattened negatives, 2 wrong-inner-type negatives, 10 content controls, 2 isolated historical controls")


def main():
    later = ROOT / FILE
    require(blob(later) == LATER, "selected later service blob")
    for filename in ("IBIS-IP_common_V1.0.xsd", "IBIS-IP_Enumerations_V1.0.xsd"):
        require(blob(ROOT / filename) == OLD[filename], f"later dependency {filename}")
    with tempfile.TemporaryDirectory(prefix="tkt001-official-v1-") as tmp:
        folder = Path(tmp)
        for filename, pin in OLD.items():
            url = f"https://raw.githubusercontent.com/VDVde/VDV301/{COMMIT}/{filename}"
            req = urllib.request.Request(url, headers={"User-Agent": "VDV301-Audit-TKT001/0.1"})
            with urllib.request.urlopen(req, timeout=60) as response:
                data = response.read()
            path = folder / filename
            path.write_bytes(data)
            require(blob(path) == pin, f"exact original tree blob {filename}")
        for filename in OLD:
            doc = parse(folder / filename)
            includes = set(doc.xpath("/xs:schema/xs:include/@schemaLocation", namespaces=NS))
            require(includes <= OLD.keys(), f"closed exact dependency family {filename}")
        original = parse(folder / FILE)
        agg = parse(folder / AGG)
        new = parse(later)
        require(not roots(original) and not groups(original), "original service file has no Ticketing operation roots/group")
        require(roots(agg) == groups(agg) == EXPECTED, "original aggregate supplies exactly seven root/type pairs and group")
        require(roots(new) == groups(new) == EXPECTED, "later service supplies same seven root/type pairs and group")
        original_types = set(original.xpath("/xs:schema/xs:complexType/@name", namespaces=NS))
        later_types = set(new.xpath("/xs:schema/xs:complexType/@name", namespaces=NS))
        require(ORPHANS <= original_types and not ORPHANS & later_types and not ORPHANS & set(EXPECTED.values()), "historical SetRazzia response types are not mapped by Ticketing roots and removed later")
        old_schema = etree.XMLSchema(original)
        aggregate_schema = etree.XMLSchema(agg)
        later_schema = etree.XMLSchema(new)
        print("PASS exact original service, complete original aggregate and later service compiled")
        samples = (
            "<TicketingService.SetRazziaRequest><TicketInformationRazziaStatus>razzia</TicketInformationRazziaStatus></TicketingService.SetRazziaRequest>",
            "<TicketingService.GetValidationResult><ValidationResultData><TimeStamp><Value>2026-11-28T07:00:00Z</Value></TimeStamp><ValidationResult>valid</ValidationResult></ValidationResultData></TicketingService.GetValidationResult>",
        )
        for xml in samples:
            node = etree.fromstring(xml.encode())
            require(aggregate_schema.validate(node), f"original aggregate accepts {node.tag}")
            require(later_schema.validate(node), f"later self-contained service accepts {node.tag}")
            require(not old_schema.validate(node), f"original isolated service rejects {node.tag}")
            errors = list(old_schema.error_log)
            require(bool(errors) and all(e.type_name == "SCHEMAV_CVC_ELT_1" for e in errors), f"isolated service rejection is missing global declaration, not payload shape: {errors}")
        print("PASSED TKT-001: 3 exact schema compilations, 4 positive / 2 missing-root negative instances; full historical aggregate")
        validate_tkt_002_identity(folder, later, aggregate_schema, later_schema)
        validate_tkt_003_response_types(folder, later, aggregate_schema, later_schema)
        validate_tkt_004_pdf_heading(folder, later, aggregate_schema, later_schema, old_schema)
        validate_tkt_005_response_type(folder, later, aggregate_schema, later_schema, old_schema)
        validate_tkt_006_tariff_sequence(folder, later, aggregate_schema, later_schema, old_schema)
        validate_tkt_007_inner_field_ownership(folder, later, aggregate_schema, later_schema, old_schema)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
