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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
