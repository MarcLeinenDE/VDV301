# Version-scope boundary review — DISC-002 — 2026-10-08

Status: **verified / wrong external RFC reference / scope unchanged**.

## Finding
VDV 301-2 passages addressing automatic IPv4 Link-Local addressing `169.254/16` incorrectly cite **RFC 2927**. External original RFC Editor authority establishes that RFC 2927 is *MIME Directory Profile for LDAP Schema* (https://www.rfc-editor.org/info/rfc2927/), while RFC 3927 is *Dynamic Configuration of IPv4 Link-Local Addresses* (https://www.rfc-editor.org/info/rfc3927/). The older VDV V1.0 German publication itself calls RFC2927 the LDAP MIME profile in its bibliography.

## First affected publication
**V1.0 German** printed p20 §2.1.1 uses RFC2927 when describing automatic `169.254.xxx.xxx` allocation, contradicted by its own bibliography p80. No independent V1.0 English publication is established.

## Language-specific continuity
- **Base V2.0 p21 / V2.1 p22:** German track correctly refers to **RFC3927**; English track incorrectly retains **RFC2927**. Both otherwise describe link-local configuration; the German citation is an explicit unaffected-language control.
- **General Conventions V2.2 p20 EN / V2.3 p20 EN / V2.4 p23 EN:** English still cites RFC2927 for link-local configuration. German allocation text is materially different starting V2.2, as handled by DISC-001, and does not create a new German RFC2927 defect.
- **No corrected English successor** after the latest pinned V2.4 publication is established.

## Boundary and SDK
Keep DISC-002 as an independent external-reference documentation error: **V1.0 German, V2.0–V2.4 English** (within the retained reviewed publication lineage). Changing a wrong RFC number to RFC3927 does **not** resolve DISC-001's allocation-policy contradiction, promote the English wording over German, or establish a universal ZeroConf/169.254 obligation. This finding has **no XML/XSD conformance impact**.

PDF visible body and pins: `docs/pdf_xsd_semantic_audit/SOURCE_LOCATOR_REVIEW_DISC_002_2026-10-06.md`; EV-126 run `33754189273`.
