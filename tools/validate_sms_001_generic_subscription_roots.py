#!/usr/bin/env python3
"""SMS-001: exact generic roots, not invented operation-qualified roots."""
from lxml import etree
from validate_sms_v22_ev116 import SERVICE, COMMON, NS, main as ev116, require

def main():
    require(ev116() == 0, "EV-116 historical checker succeeds")
    schema = etree.XMLSchema(etree.parse(str(SERVICE)))
    common = etree.parse(str(COMMON))
    request = "<Client-IP-Address><Value>192.0.2.1</Value></Client-IP-Address>"
    active = "<Active><Value>true</Value></Active>"
    cases = {
        "SubscribeRequest": request, "SubscribeResponse": active,
        "UnsubscribeRequest": request, "UnsubscribeResponse": active,
    }
    for root, payload in cases.items():
        require(common.xpath(
            "/xs:schema/xs:element[@name=$root]/@type",
            namespaces=NS, root=root,
        ) == [root + "Structure"], "exact generic root/type " + root)
        doc = etree.fromstring(f"<{root}>{payload}</{root}>".encode())
        require(schema.validate(doc), "generic root PASS " + root)
        verb = "Unsubscribe" if root.startswith("Unsubscribe") else "Subscribe"
        suffix = root[len(verb):]
        for target in ("DeviceStatus", "ServiceStatus"):
            alias = f"SystemMonitoringService.{verb}{target}{suffix}"
            doc = etree.fromstring(f"<{alias}>{payload}</{alias}>".encode())
            require(not schema.validate(doc), "invented qualified root FAIL " + alias)
            error = schema.error_log.last_error
            require(error is not None and error.type_name == "SCHEMAV_CVC_ELT_1"
                    and "No matching global declaration" in error.message,
                    "targeted missing-global-declaration rejection " + alias)
    print("PASSED: SMS-001 four generic roots and eight invented qualified roots")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
