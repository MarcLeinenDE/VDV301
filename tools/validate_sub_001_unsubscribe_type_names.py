#!/usr/bin/env python3
"""SUB-001: exact declared type names, not service/production XML roots."""
from pathlib import Path
import hashlib
from lxml import etree

ROOT = Path(__file__).resolve().parents[1]
NS = {"xs": "http://www.w3.org/2001/XMLSchema"}
PROFILES = (
    ("1.0", "194f73adfb9a62dfff8ce6a7b6a0cdc9b1c6a36c", "1.0", "a9bea5bc73003ed91ded8519db06c32c4067831d", "official_VDV-301-1.0"),
    ("2.0", "8608e3dcd665c197c34da7f6ec6af5a3758da164", "2.0", "27e3c183b00381d959622d13c10543123af8eef6", "official_VDV-301-2.0"),
    ("2.1", "05977c9f86c7c9dd0b48f36a4a4e9be32e94659e", "2.1", "311464690ad60749ed8d326217787e4b8ed0b718", "official_VDV-301-2.1"),
    ("2.2", "468fee6d177e7185dbcd5d3f90cfb114e29e01ae", "2.2", "2a23b512379b18e8f122ac1272cef8229fb86283", "official_VDV-301-2.2"),
    ("2.3", "0d8926c4063c12de9a5e68b6f0addaab35a55dc1", "2.2", "2a23b512379b18e8f122ac1272cef8229fb86283", "official_VDV-301-2.3"),
    ("2.4", "1946fd37e29ced605654f49ea3d98cd2fbbdc8e4", "2.4", "2afed8cf23afa91db92b0f043cc5b4ad428b0f25", "candidate_integration_PR31"),
)


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def blob(path):
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def probe(common, typename):
    # A test-only global element allows type resolution without asserting a
    # production root, particularly for Common V1.0 and V2.0.
    xml = f'<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema"><xs:include schemaLocation="{common}"/><xs:element name="Sub001TypeResolutionProbe" type="{typename}"/></xs:schema>'
    return etree.fromstring(xml.encode(), base_url=(ROOT / "_sub001_probe.xsd").as_uri())


def main():
    positive = negative = 0
    for v, common_sha, ev, enum_sha, authority in PROFILES:
        common = ROOT / f"IBIS-IP_common_V{v}.xsd"
        enums = ROOT / f"IBIS-IP_Enumerations_V{ev}.xsd"
        require(blob(common) == common_sha, f"{authority}: Common pin mismatch")
        require(blob(enums) == enum_sha, f"{authority}: Enum pin mismatch")
        doc = etree.parse(str(common))
        require(doc.xpath("/xs:schema/xs:include/@schemaLocation", namespaces=NS) == [enums.name], f"{authority}: dependency route mismatch")
        etree.XMLSchema(doc)
        types = set(doc.xpath("/xs:schema/xs:complexType/@name | /xs:schema/xs:simpleType/@name", namespaces=NS))
        for kind in ("Request", "Response"):
            correct = f"Unsubscribe{kind}Structure"
            invented = f"TerminateSubscribe{kind}Structure"
            require(correct in types and invented not in types, f"{authority}: unexpected type inventory")
            etree.XMLSchema(probe(common.name, correct))
            positive += 1
            print(f"PASS {authority}: {correct} type reference compiles")
            try:
                etree.XMLSchema(probe(common.name, invented))
            except etree.XMLSchemaParseError as exc:
                errors = [x for x in exc.error_log if x.level_name in ("ERROR", "FATAL")]
                require(bool(errors) and all(x.type_name == "SCHEMAP_SRC_RESOLVE" and invented in x.message and "type definition" in x.message for x in errors), f"{authority}: wrong rejection cause {exc.error_log}")
                negative += 1
                print(f"PASS {authority}: {invented} rejected as unresolved type (SCHEMAP_SRC_RESOLVE)")
            else:
                raise AssertionError(f"{authority}: invented type unexpectedly compiles")
    require((positive, negative) == (12, 12), "unexpected test count")
    print("PASSED: SUB-001 12 positive, 12 targeted negative type-reference compilations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
