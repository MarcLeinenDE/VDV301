# Source-locator review — CIS-001 — 2026-10-06

Status: **structurally complete and visible-body verified under the current audit workflow contract**.

## Finding

CIS-001 is a **release-authority gap** for CustomerInformationService V1.1. The official V1.1 PDF is published, but no matching release-tagged official CIS V1.1 XSD authority is established. The historical untagged upstream working snapshot is useful evidence only and must not be promoted to official release authority.

## Exact PDF authority and visible body

Official source:

- source ID: `CIS_V1.1`
- URL: `https://www.vdv.de/301-2-3-sds-v1-1.pdfx`
- pinned SHA-256: `f9d63dd1f2e417691913e57a9c7121c90b4e781cbcd1328be681695975f59739`
- size: **809729 bytes**
- source evidence: run `33736316368`, job `100587592810`, artifact `9885887536`

The interactive renderer cache-missed during this review, so the canonical fallback path was used. The exact existing evidence artifact was downloaded and its embedded PDF SHA-256 and size were reverified against the pin registry before examining the rendered pages.

Visible body checks:

1. **Printed page 13** — continuation of **1.3 Data Structure of GetAllData Operation / 1.3.2 Response**, **Table 3: Description ofCustomerInformationService.AllData**. The visible VehicleInformationGroup contains:
   - `SpeakerActive` — `0:1` — `IBIS-IP.boolean`
   - `StopInformationActive` — `0:1` — `IBIS-IP.boolean`

2. **Printed page 20** — **1.24 Data Structure of GetVehicleData Operation / 1.24.2 Response**, **Table 17: Description of CustomerInformationService.VehicleData**. The visible VehicleInformationGroup again contains both optional boolean members.

These body locators are used directly; no TOC-derived section or inferred table number is substituted.

## Historical XSD evidence

Upstream repository: `VDVde/VDV301`  
Untagged working commit: `0a5228a768c7d710c40f5f99fbdce2e544d19883`  
File: `IBIS-IP_CustomerInformationService_V1.1.xsd`  
Blob: `5957e27f128a191c794b0c8081b531a07126784a`

The upstream tree at that exact commit was rechecked and resolves the V1.1 CIS file to the same blob.

Exact structural evidence:

- `VehicleInformationGroup`, lines 8–42: ends after optional `VehicleMode`; neither `SpeakerActive` nor `StopInformationActive` exists.
- `CustomerInformationService.AllData`, lines 51–64: references `VehicleInformationGroup`.
- `CustomerInformationService.VehicleData`, lines 157–163: references the same group.

Therefore the untagged working schema is materially behind the published V1.1 PDF.

## Active disproof

The strongest counter-explanation is that the untagged V1.1 working snapshot might be the intended normative schema despite the missing release tag. That does not close the authority gap:

- the snapshot is not a release-tagged V1.1 authority;
- its service schema materially disagrees with two fields visibly present in the published V1.1 document;
- promoting it would silently invent release authority.

The existing EV-125 / EV-167 evidence chain already established that no matching `VDV-301-1.1` release authority was found. This review does not infer a missing schema and does not substitute another version.

## SDK consequence

Unchanged:

```text
CIS V1.1 strict XSD profile: unavailable / fail closed.
Do not substitute the untagged working family.
Do not substitute V1.0, V2.0 or a later CIS XSD.
```

No XSD bytes, semantic scope, runtime mapping or diagnostics were changed by this source-locator step.
