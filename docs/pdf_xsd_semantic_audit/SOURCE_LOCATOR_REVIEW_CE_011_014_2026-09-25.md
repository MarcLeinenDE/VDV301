# Source-locator review — CE-011 through CE-014 — 2026-09-25

Status: **persisted / closure gate pending**.

## Scope

This Phase-B block adds canonical direct PDF/XSD locations for four Common structure findings:

- `CE-011` — Connection TransportMode/ConnectionMode repeatability;
- `CE-012` — DeviceSpecificationWithStateList empty-list boundary;
- `CE-013` — AdditionalAnnouncement optional choice and InformationAtSpecificPoint/SpecificPoint name boundary;
- `CE-014` — DataVersionList empty-list boundary.

The existing CE-005..CE-010 pilot remains unchanged.

## Authority and version boundaries

### CE-011

The corrected terminal scope is V2.2 through V2.4.

- V2.1 is an explicit aligned negative control: TransportMode is 0:1 and ConnectionMode is not yet the later added field.
- V2.2 and V2.3 are official selected Common XSD lanes.
- V2.4 uses the official PDF paired only with the explicitly selected candidate/integration Common V2.4 XSD.

### CE-012 / CE-013 / CE-014

Each is located from Common V1.0 through V2.4.

V1.0 is preserved exactly rather than normalized to later structures. In particular, the V1.0 DataVersionList XSD declaration is anonymous inside `DeviceInformationStructure`; no synthetic `DataVersionListStructure` is invented for V1.0.

## PDF locations

```text
CE-011
  V2.2 p18  §2.8  Table 8
  V2.3 p18  §2.8  Table 8
  V2.4 p20  §2.8  Table 8

CE-012
  V1.0 p11  §1.18 Table 18
  V2.0 p18  §2.18 Table 18
  V2.1 p20  §2.18 Table 18
  V2.2 p21  §2.18 Table 18
  V2.3 p21  §2.18 Table 18
  V2.4 p23  §2.18 Table 18

CE-013
  V1.0 p7   §1.1 Table 1
  V2.0 p14  §2.1 Table 1
  V2.1 p15  §2.1 Table 1
  V2.2 p16  §2.1 Table 1
  V2.3 p16  §2.1 Table 1
  V2.4 p18  §2.1 Table 1

CE-014
  V1.0 p10  §1.12 Table 12
  V2.0 p17  §2.12 Table 12
  V2.1 p18  §2.12 Table 12
  V2.2 p19  §2.12 Table 12
  V2.3 p19  §2.12 Table 12
  V2.4 p21  §2.12 Table 12
```

All PDF locators carry the official source URL and existing pinned SHA-256.

## XSD locations

Every lane pins the exact Common XSD Git blob and a component path.

- CE-011: `ConnectionStructure/TransportMode` and `ConnectionStructure/ConnectionMode`.
- CE-012: `DeviceSpecificationWithStateListStructure/DeviceSpecificationWithState`.
- CE-013: `AdditionalAnnouncementStructure/xs:choice` and its `SpecificPoint` branch.
- CE-014: V2.0+ `DataVersionListStructure/DataVersion`; V1.0 exact anonymous `DeviceInformationStructure/DataVersionList/DataVersion`.

The stored XPath hints are gate-checked against the exact XSD blobs. Line hints remain non-canonical convenience metadata only.

## Resulting Phase-B inventory after persistence

```text
locator findings      10 / 192
complete               10
partial                 0
remaining             182
coverage lanes         44
```

No finding semantics, runtime mapping state or XSD PASS/FAIL rule is changed.

## Primary gate

Run **36130205489**: **SUCCESS** on HEAD `c2ae3f47e4985e6d2754251a3d9f3a80b6863dc9`.

The gate validated the canonical locator manifest, all **44 stored coverage lanes**, every XSD XPath against its exact blob, the CE-011..CE-014 PDF page/table matrix, corrected CE-011 scope, all Common V1.0–V2.4 executable evidence lanes, semantic/runtime/SDK consistency, full root-XSD regression and a clean XSD tree.
