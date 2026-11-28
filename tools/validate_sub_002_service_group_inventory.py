#!/usr/bin/env python3
"""SUB-002: exact service-local group inventories; no HTTP/root synthesis."""
from pathlib import Path
import tempfile
import shutil
import urllib.request
from lxml import etree
from validate_sub_001_unsubscribe_type_names import PROFILES, blob, require

ROOT = Path(__file__).resolve().parents[1]
NS = {"xs": "http://www.w3.org/2001/XMLSchema"}
# filename, blob, Common version, direct service group count, named members,
# subscription request/response group members (not HTTP operation count).
CASES = (
    ("IBIS-IP_SystemDocumentationService_v1.0.xsd", "8995c4a230bf81d5e47b9313ee7725ff3cd4b7b5", "1.0", "SystemDocumentationServiceGroup", 0, 0, 0),
    ("IBIS-IP_DeviceManagementService_V1.0.xsd", "602a963f91000d0d39e3c271bacb3c7aba73e6d4", "1.0", "DeviceManagementServiceGroup", 0, 0, 0),
    ("IBIS-IP_SystemDocumentationService_V2.0.xsd", "ab959dddbfa2b8ca420af1b079501f94cff38051", "2.0", "SystemDocumentationServiceGroup", 1, 5, 0),
    ("IBIS-IP_SystemManagementService_V1.0.xsd", "2d32630a0f1981e980e6a466e3f6a69136410f24", "1.0", "SystemManagementServiceGroup", 1, 2, 0),
    ("IBIS-IP_DeviceManagementService_V2.0.xsd", "74189e0da65563eeb084ec2f3c400e9668d1ee1a", "2.0", "DeviceManagementServiceGroup", 1, 10, 0),
    ("IBIS-IP_DeviceManagementService_V2.1.xsd", "191b43e01cdaba14b247725689a913c244a67eed", "2.1", "DeviceManagementServiceGroup", 1, 84, 40),
    ("IBIS-IP_DeviceManagementService_V2.2.xsd", "c589e9f9d9b9a0f60309a275ec36b76b8c5d1f1d", "2.2", "DeviceManagementServiceGroup", 1, 68, 36),
)
OLD_SMS = "85390f99d6c19c88923ed9a5fc8a5706137708af"
AGGREGATE = "41289eaed2674a169fdf77a10a2eff293c76d5c4"


def members(doc, group):
    nodes = doc.xpath("/xs:schema/xs:group[@name=$name]/xs:sequence/xs:element", namespaces=NS, name=group)
    return [(e.get("name"), e.get("type")) for e in nodes]


def inspect(doc, group, counts):
    entries = members(doc, group)
    subs = [(n,t) for n,t in entries if n and (".Subscribe" in n or ".Unsubscribe" in n)]
    groups = len(doc.xpath("/xs:schema/xs:group[@name=$name]", namespaces=NS, name=group))
    require((groups,len(entries),len(subs)) == counts, f"{group} unexpected inventory")
    for n,t in subs:
        expected = ("Unsubscribe" if ".Unsubscribe" in n else "Subscribe") + ("RequestStructure" if n.endswith("Request") else "ResponseStructure")
        require(t == expected, f"{n}: expected {expected}, got {t}")
    return entries


def historical_file(filename, expected, directory):
    # The official historical aggregate is not stored in the worktree.
    # Exact content identity is verified before inspection/compilation.
    url = f"https://raw.githubusercontent.com/VDVde/VDV301/VDV-301-1.0/{filename}"
    req = urllib.request.Request(url, headers={"User-Agent": "VDV301-Audit-SUB002/0.1"})
    with urllib.request.urlopen(req, timeout=60) as response:
        data = response.read()
    path = directory / filename
    path.write_bytes(data)
    require(blob(path) == expected, f"{filename}: historical blob mismatch")
    return path


def main():
    dep = {v: (common_sha, ev, enum_sha) for v, common_sha, ev, enum_sha, _ in PROFILES}
    for filename, pin, version, group, groups, count, subcount in CASES:
        path = ROOT / filename
        require(blob(path) == pin, f"{filename}: blob mismatch")
        common_sha, ev, enum_sha = dep[version]
        common = ROOT / f"IBIS-IP_common_V{version}.xsd"
        enums = ROOT / f"IBIS-IP_Enumerations_V{ev}.xsd"
        require(blob(common) == common_sha and blob(enums) == enum_sha, f"{filename}: dependency pin mismatch")
        doc = etree.parse(str(path))
        require(doc.xpath("/xs:schema/xs:include/@schemaLocation", namespaces=NS) == [common.name, enums.name], f"{filename}: include route mismatch")
        etree.XMLSchema(doc)
        inspect(doc, group, (groups,count,subcount))
        print(f"PASS {filename}: compiled; groups={groups}, members={count}, subscription members={subcount}")
    with tempfile.TemporaryDirectory(prefix="sub002-historical-") as tmp:
        folder = Path(tmp)
        for name in ("IBIS-IP_common_V1.0.xsd", "IBIS-IP_Enumerations_V1.0.xsd"):
            shutil.copyfile(ROOT / name, folder / name)
        sms = historical_file("IBIS-IP_SystemManagementService_V1.0.xsd", OLD_SMS, folder)
        doc = etree.parse(str(sms))
        require(doc.xpath("/xs:schema/xs:include/@schemaLocation", namespaces=NS) == ["IBIS-IP_common_V1.0.xsd","IBIS-IP_Enumerations_V1.0.xsd"], "original SMS include route mismatch")
        etree.XMLSchema(doc)
        inspect(doc, "SystemManagementServiceGroup", (0,0,0))
        print("PASS original VDV-301-1.0 SMS: compiled; no local service group")
        aggregate = historical_file("IBIS_IP_V1.0.xsd", AGGREGATE, folder)
        agg = etree.parse(str(aggregate))
        inspect(agg,"SystemDocumentationServiceGroup",(1,5,0))
        inspect(agg,"SystemManagementServiceGroup",(1,2,0))
        # Static aggregate evidence only; do not pretend to compile a complete
        # historical aggregate from the incomplete deduplicated worktree.
        roots = set(agg.xpath("/xs:schema/xs:element/@name", namespaces=NS))
        require({"SubscribeRequest","SubscribeResponse","UnsubscribeRequest","UnsubscribeResponse"} <= roots,"historical aggregate generic roots missing")
        print("PASS VDV-301-1.0 aggregate: exact blob, sparse service groups, generic global roots (static)")
    print("PASSED: SUB-002 eight service schema compilations plus historical aggregate inventory")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
