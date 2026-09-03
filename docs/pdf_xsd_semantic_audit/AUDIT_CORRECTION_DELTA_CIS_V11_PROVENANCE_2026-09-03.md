# Audit correction delta — CIS V1.1 provenance — 2026-09-03

This overlay corrects earlier first-pass statements that no CIS V1.1 XSD had been confirmed.

Fresh provenance establishes an official-upstream **working** V1.1 family at commit `0a5228a768c7d710c40f5f99fbdce2e544d19883` immediately before the V2.0 release lineage:

- CIS: `5957e27f128a191c794b0c8081b531a07126784a`
- Common: `bdf839813b4b19dd000a32a684ce985878adaca9`
- Enumerations: `5a9957a6931be2e4460665f8a52c76765fbfbcde`

The official tag set contains no `VDV-301-1.1` release tag. The working CIS V1.1 schema also lacks `SpeakerActive` and `StopInformationActive`, both visible in the published V1.1 PDF and executable in V2.0. Therefore the historical files prove development provenance but **do not establish a strict published V1.1 release validation authority**.

Historical reports are preserved; this correction overlay supersedes only their “V1.1 XSD not found” provenance conclusion. No XSD is imported or modified by this correction.
