# Source-locator review — DISC-001 — 2026-10-06

Status: **structurally complete / visible-body verified / documentation-only conflict preserved**.

## Finding

DISC-001 is a cross-artifact/documentation conflict about IP-address allocation in VDV 301-2.

No XML/XSD conformance rule applies. The exact official publication, version and language are the relevant authority surfaces.

## Visible version chain

### V1.0 German

- source `VDV301-2_V1.0_DE`
- printed page **20**
- `2.1 Adressierung / 2.1.1 IP-Adressen`
- visibly prescribes decentralized allocation using part of “Zero Conf”, cites **RFC 2927**, and identifies `169.254.xxx.xxx`.

### Base V2.0

- source `VDV301-2_BASE_V2.0`
- printed page **21**
- bilingual visible section `2.1 Adressierung / Adressing`
- German text cites **RFC 3927** for the ZeroConf/link-local rule.
- English text on the same page still cites **RFC 2927** and retains `169.254.xxx.xxx`.

### Base V2.1

- source `VDV301-2_BASE_V2.1`
- printed page **22**
- same visible bilingual split: German **RFC 3927**, English **RFC 2927**, with the same ZeroConf/169.254 semantics otherwise retained.

### General Conventions V2.2

- source `VDV301-2_GC_V2.2`
- printed page **17**, German: `Vorgaben für die IP-Adressvergabe existieren nicht`; consistency is required and fixed IP/DHCP is stated as best practice.
- printed page **20**, English: still says IP addresses are allocated using part of “Zero Conf”, cites **RFC 2927**, and says the `169.254.xxx.xxx` range must be observed.

### General Conventions V2.3

- source `VDV301-2_GC_V2.3`
- printed pages **17 / 20**
- the same material German/English split remains visible.

### General Conventions V2.4

- source `VDV301-2_GC_V2.4`
- printed pages **20 / 23**
- German continues to say no allocation method is prescribed and recommends fixed IP/DHCP as best practice.
- English continues to require ZeroConf/RFC 2927/169.254.xxx.xxx.

## Active disproof

The strongest alternative explanation is that the bilingual difference is only the already-known RFC-number typo.

That explanation fails from V2.2 onward. The German and English tracks no longer merely cite different RFC numbers; they express different allocation semantics:

- German: no prescribed allocation procedure.
- English: ZeroConf/link-local allocation with a stated 169.254 range requirement.

Therefore the finding remains a real language/version semantic conflict.

## Authority and SDK consequence

This is **documentation-only discovery guidance**:

- no XSD locator is applicable;
- do not synthesize an XML validation rule;
- do not hard-enforce universal ZeroConf or 169.254/16 solely from the stale English track;
- preserve version/language provenance in diagnostics;
- do not silently declare the German or English language track to be the corrected normative source.

Existing semantic classification and runtime state remain unchanged.
